# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
POS Batch Handler
"""

from sqlalchemy import orm

from rattail.batch import BatchHandler
from rattail.db.model import POSBatch


class POSBatchHandler(BatchHandler):
    """
    Handler for POS batches
    """
    batch_model_class = POSBatch

    def get_terminal_id(self):
        """
        Returns the ID string for current POS terminal.
        """
        return self.config.get('rattail', 'pos.terminal_id')

    def init_batch(self, batch, **kwargs):
        batch.terminal_id = self.get_terminal_id()

    def make_row(self, **kwargs):
        row = super().make_row(**kwargs)
        row.timestamp = self.app.make_utc()
        return row

    # TODO: should also filter this by terminal
    def get_current_batch(self, user, create=True, return_created=False, **kwargs):
        """
        Get the "current" POS batch for the given user, creating it as
        needed.
        """
        if not user:
            raise ValueError("must specify a user")

        created = False
        model = self.model
        session = self.app.get_session(user)

        try:
            batch = session.query(model.POSBatch)\
                           .filter(model.POSBatch.created_by == user)\
                           .filter(model.POSBatch.executed == None)\
                           .one()
        except orm.exc.NoResultFound:
            if not create:
                if return_created:
                    return None, False
                return
            batch = self.make_batch(session, created_by=user)
            session.add(batch)
            session.flush()
            created = True

        if return_created:
            return batch, created

        return batch

    def get_screen_txn_display(self, batch, **kwargs):
        """
        Should return the text to be used for displaying transaction
        identifier within the header of POS screen.
        """
        return batch.id_str

    def get_screen_cust_display(self, batch=None, customer=None, **kwargs):
        """
        Should return the text to be used for displaying customer
        identifier / name etc. within the header of POS screen.
        """
        if not customer and batch:
            customer = batch.customer
        if not customer:
            return

        key_field = self.app.get_customer_key_field()
        customer_key = getattr(customer, key_field)
        return str(customer_key or '')

    # TODO: this should account for shoppers somehow too
    def set_customer(self, batch, customer, user=None, **kwargs):
        """
        Assign the customer account for POS transaction.
        """
        if customer and batch.customer:
            row_type = self.enum.POS_ROW_TYPE_SWAP_CUSTOMER
        elif customer:
            row_type = self.enum.POS_ROW_TYPE_SET_CUSTOMER
        else:
            if not batch.customer:
                return
            row_type = self.enum.POS_ROW_TYPE_DEL_CUSTOMER

        batch.customer = customer

        row = self.make_row()
        row.user = user
        row.row_type = row_type
        if customer:
            key = self.app.get_customer_key_field()
            row.item_entry = getattr(customer, key)
        row.description = str(customer) if customer else 'REMOVE CUSTOMER'
        self.add_row(batch, row)

    def process_entry(self, batch, entry, quantity=1, user=None, **kwargs):
        """
        Process an "entry" value direct from POS.  Most typically,
        this is effectively "ringing up an item" and hence we add a
        row to the batch and return the row.
        """
        session = self.app.get_session(batch)
        model = self.model

        if isinstance(entry, model.Product):
            product = entry
            entry = product.uuid
        else:
            product = self.app.get_products_handler().locate_product_for_entry(session, entry)
        if product:

            # product located, so add item row
            row = self.make_row()
            row.user = user
            row.item_entry = kwargs.get('item_entry', entry)
            row.upc = product.upc
            row.item_id = product.item_id
            row.product = product
            row.brand_name = product.brand.name if product.brand else None
            row.description = product.description
            row.size = product.size
            row.full_description = product.full_description
            dept = product.department
            if dept:
                row.department_number = dept.number
                row.department_name = dept.name
            subdept = product.subdepartment
            if subdept:
                row.subdepartment_number = subdept.number
                row.subdepartment_name = subdept.name
            row.foodstamp_eligible = product.food_stampable
            row.sold_by_weight = product.weighed # TODO?
            row.quantity = quantity

            regprice = product.regular_price
            if regprice:
                row.reg_price = regprice.price

            txnprice = product.current_price or product.regular_price
            if txnprice:
                row.txn_price = txnprice.price

            if row.txn_price:
                row.sales_total = row.txn_price * row.quantity
                batch.sales_total = (batch.sales_total or 0) + row.sales_total

            row.tax1 = product.tax1
            row.tax2 = product.tax2

            if row.txn_price:
                row.row_type = self.enum.POS_ROW_TYPE_SELL
            else:
                row.row_type = self.enum.POS_ROW_TYPE_BADPRICE

            self.add_row(batch, row)
            session.flush()
            return row

    def record_badscan(self, batch, entry, quantity=1, user=None, **kwargs):
        """
        Add a row to the batch which represents a "bad scan" at POS.
        """
        row = self.make_row()
        row.user = user
        row.row_type = self.enum.POS_ROW_TYPE_BADSCAN
        row.item_entry = entry
        row.description = "BADSCAN"
        row.quantity = quantity
        self.add_row(batch, row)
        return row

    def get_tender(self, session, key, **kwargs):
        """
        Return the tender record for Cash.

        :param session: Current DB session.

        :param key: Either a tender UUID, or "true" tender code (i.e.
           :attr:`rattail.db.model.sales.Tender.code` value) or a
           "pseudo-code" for common tenders (e.g. ``'cash'``).
        """
        model = self.model

        # Tender.uuid match?
        tender = session.get(model.Tender, key)
        if tender:
            return tender

        # Tender.code match?
        try:
            return session.query(model.Tender)\
                          .filter(model.Tender.code == key)\
                          .one()
        except orm.exc.NoResultFound:
            pass

        # try settings, if value then recurse
        # TODO: not sure why get_vendor() only checks settings?
        # for now am assuming we should also check config file
        #key = self.app.get_setting(session, f'rattail.tender.{key}')
        key = self.config.get('rattail', f'tender.{key}')
        if key:
            return self.get_tender(session, key, **kwargs)

    def refresh_row(self, row):
        # TODO (?)
        row.status_code = row.STATUS_OK
        row.status_text = None

    def clone(self, oldbatch, created_by, progress=None):
        newbatch = super().clone(oldbatch, created_by, progress=progress)
        newbatch.tender_total = 0
        newbatch.void = False
        return newbatch

    def get_clonable_rows(self, batch, **kwargs):
        # TODO: row types..ugh
        return [row for row in batch.data_rows
                if row.row_type != self.enum.POS_ROW_TYPE_TENDER]

    def override_price(self, row, user, txn_price, **kwargs):
        """
        Override the transaction price for the given batch row.
        """
        batch = row.batch

        # update price for given row
        orig_row = row
        orig_txn_price = orig_row.txn_price
        orig_sales_total = orig_row.sales_total
        orig_row.txn_price = txn_price
        orig_row.sales_total = orig_row.quantity * orig_row.txn_price

        # adjust totals
        batch.sales_total = (batch.sales_total or 0) - orig_sales_total + orig_row.sales_total

        # add another row indicating who/when
        row = self.make_row()
        row.user = user
        row.row_type = self.enum.POS_ROW_TYPE_ADJUST_PRICE
        row.item_entry = orig_row.item_entry
        row.txn_price = txn_price
        row.description = (f"ROW {orig_row.sequence} PRICE ADJUST "
                           f"FROM {self.app.render_currency(orig_txn_price)}")
        self.add_row(batch, row)
        return row

    def void_row(self, row, user, **kwargs):
        """
        Apply "void" status to the given batch row.
        """
        batch = row.batch

        # mark given row as void
        orig_row = row
        orig_row.void = True

        # adjust batch totals
        if orig_row.sales_total:
            batch.sales_total = (batch.sales_total or 0) - orig_row.sales_total

        # add another row indicating who/when
        row = self.make_row()
        row.user = user
        row.row_type = self.enum.POS_ROW_TYPE_VOID_LINE
        row.item_entry = orig_row.item_entry
        row.description = f"VOID ROW {orig_row.sequence}"
        self.add_row(batch, row)
        return row

    def void_batch(self, batch, user, **kwargs):
        """
        Void the given POS batch.
        """
        # add another row indicating who/when
        row = self.make_row()
        row.user = user
        row.row_type = self.enum.POS_ROW_TYPE_VOID_TXN
        row.description = "VOID TXN"
        self.add_row(batch, row)

        # void/execute batch
        batch.void = True
        batch.executed = self.app.make_utc()
        batch.executed_by = user

    def apply_tender(self, batch, user, tender, amount, **kwargs):
        """
        Apply the given tender amount to the batch.

        :param tender: Reference to a
           :class:`~rattail.db.model.sales.Tender` or similar object, or dict
           with similar keys, or can be just a tender code.

        :param amount: Amount to apply.  Note, this usually should be
           a *negative* number.

        :returns: List of rows which were added to the batch.
        """
        session = self.app.get_session(batch)

        # TODO: this could probably be improved. any validation needed?
        if isinstance(tender, str):
            item_entry = tender
            description = f"TENDER '{tender}'"
        elif hasattr(tender, 'code'):
            item_entry = tender.code
            description = tender.name
        else:
            item_entry = tender['code']
            description = tender['name']

        rows = []

        # add row for tender
        row = self.make_row()
        row.user = user
        row.row_type = self.enum.POS_ROW_TYPE_TENDER
        row.item_entry = item_entry
        row.description = description
        row.tender_total = amount
        batch.tender_total = (batch.tender_total or 0) + row.tender_total
        self.add_row(batch, row)
        rows.append(row)

        # nothing more to do for now, if balance remains
        balance = batch.get_balance()
        if balance > 0:
            return rows

        # give change back if tender overpaid
        if balance < 0:

            # but some tenders do not allow cash back
            if hasattr(tender, 'is_cash') and not tender.is_cash:
                if not tender.allow_cash_back:
                    raise ValueError(f"tender '{tender.name}' does not allow "
                                     f" cash back: ${-balance:0.2f}")

            row = self.make_row()
            row.user = user
            row.row_type = self.enum.POS_ROW_TYPE_CHANGE_BACK
            row.item_entry = item_entry
            row.description = "CHANGE BACK"
            row.tender_total = -balance
            batch.tender_total = (batch.tender_total or 0) + row.tender_total
            self.add_row(batch, row)
            rows.append(row)

        # all paid up, so finalize
        session.flush()
        assert batch.get_balance() == 0
        self.do_execute(batch, user, **kwargs)
        return rows

    def execute(self, batch, progress=None, **kwargs):
        # TODO
        return True
