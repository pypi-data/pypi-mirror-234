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

import decimal

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
            # TODO: maybe should only search by product key (or GPC?) etc.
            product = self.app.get_products_handler().locate_product_for_entry(session, entry)

        # TODO: if product not found, should auto-record a badscan
        # entry?  maybe only if config says so, e.g. might be nice to
        # only record badscan if entry truly came from scanner device,
        # in which case only the caller would know that
        if not product:
            return

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

        tax = product.tax
        if tax:
            row.tax_code = tax.code
            row.tax_rate = tax.rate

        if row.txn_price:
            row.row_type = self.enum.POS_ROW_TYPE_SELL
            if tax:
                self.update_tax(batch, row, tax)
        else:
            row.row_type = self.enum.POS_ROW_TYPE_BADPRICE

        self.add_row(batch, row)
        session.flush()
        return row

    def update_tax(self, batch, row, tax=None, tax_code=None, **kwargs):
        """
        Update the tax totals for the batch, basd on given row.
        """
        if not tax and not tax_code:
            raise ValueError("must specify either tax or tax_code")

        session = self.app.get_session(batch)
        if not tax:
            tax = self.get_tax(session, tax_code)

        btax = batch.taxes.get(tax.code)
        if not btax:
            btax = self.model.POSBatchTax()
            btax.tax = tax
            btax.tax_code = tax.code
            btax.tax_rate = tax.rate
            session.add(btax)
            btax.batch = batch
            session.flush()

        # calculate relevant sales
        rows = [r for r in batch.active_rows()
                if r.tax_code == tax.code
                and not r.void]
        sales = sum([r.sales_total for r in rows])
        # nb. must add row separately if not yet in batch
        if not row.batch and not row.batch_uuid:
            sales += row.sales_total

        # total for this tax
        before = btax.tax_total or 0
        btax.tax_total = (sales * (tax.rate / 100)).quantize(decimal.Decimal('0.02'))
        batch.tax_total = (batch.tax_total or 0) - before + btax.tax_total

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

    def get_tax(self, session, code, **kwargs):
        """
        Return the tax record corresponding to the given code.

        :param session: Current DB session.

        :param code: Tax code to fetch.
        """
        model = self.model
        return session.query(model.Tax)\
                      .filter(model.Tax.code == code)\
                      .one()

    def get_tender(self, session, key, **kwargs):
        """
        Return the tender record corresponding to the given key.

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
        if orig_row.tax_code:
            self.update_tax(batch, orig_row, tax_code=orig_row.tax_code)

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
        if orig_row.tax_code:
            self.update_tax(batch, orig_row, tax_code=orig_row.tax_code)

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
        model = self.model

        tender_info = tender
        tender = None
        item_entry = None
        description = None

        if isinstance(tender_info, model.Tender):
            tender = tender_info
        else:
            if isinstance(tender_info, str):
                tender_code = tender_info
            else:
                tender_code = tender_info['code']
            item_entry = tender_code
            description = f"TENDER '{tender_code}'"
            tender = self.get_tender(session, tender_code)

        if tender:
            item_entry = tender.code
            description = tender.name

            if tender.disabled:
                # TODO: behavior here should be configurable, probably
                # needs a dedicated email etc. ..or maybe just ignore
                log.error("disabled tender '%s' being applied to POS batch: %s",
                          tender, batch)

        rows = []

        # add row for tender
        row = self.make_row()
        row.user = user
        row.row_type = self.enum.POS_ROW_TYPE_TENDER
        row.item_entry = item_entry
        row.description = description
        row.tender_total = amount
        row.tender = tender
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

            if tender and tender.is_cash:
                cash = tender
            else:
                cash = self.get_tender(session, 'cash')

            row = self.make_row()
            row.user = user
            row.row_type = self.enum.POS_ROW_TYPE_CHANGE_BACK
            row.item_entry = item_entry
            row.description = "CHANGE DUE"
            row.tender_total = -balance
            row.tender = cash
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
