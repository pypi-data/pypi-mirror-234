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
Report Commands
"""

import logging

from sqlalchemy import orm

from rattail.commands import Subcommand
from rattail.time import get_sunday, get_monday


log = logging.getLogger(__name__)


class ReportSubcommand(Subcommand):
    """
    Generate and email a report
    """
    report_key = None
    email_key = None
    simple_report_name = "(Unnamed)"

    def ensure_report_key(self):
        if not self.report_key:
            raise RuntimeError("must define {}.report_key".format(
                self.__class__.__name__))


class WeeklyReport(ReportSubcommand):
    """
    Generate and email a weekly report
    """

    def run(self, args):
        self.ensure_report_key()
        session = self.make_session()
        model = self.model

        # first must determine most recent complete Mon-Sun date range
        # TODO: should probably be more flexible about date range..
        today = self.app.today()
        sunday = get_sunday(today)
        monday = get_monday(sunday)
        start_date = monday
        end_date = sunday

        # determine naming for the report
        report_name = "{} {} thru {}".format(
            self.simple_report_name,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"))

        try:
            # see if this report has already been ran
            output = session.query(model.ReportOutput)\
                            .filter(model.ReportOutput.report_type == self.report_key)\
                            .filter(model.ReportOutput.report_name == report_name)\
                            .one()

        except orm.exc.NoResultFound:

            # generate report file and commit result
            handler = self.app.get_report_handler()
            report = handler.get_report(self.report_key)
            params = {'start_date': start_date, 'end_date': end_date}
            user = self.get_runas_user(session=session)
            output = handler.generate_output(session, report, params, user,
                                             progress=self.progress)
            session.commit()

            # try to make url for report
            report_url = None
            base_url = self.config.base_url()
            if base_url:
                report_url = '{}/reports/generated/{}'.format(
                    base_url, output.uuid)

            # send report output as email
            email_key = self.email_key or self.report_key
            handler.email_output(report, output, email_key,
                                 extra_data={'report_url': report_url})

        else:
            log.warning("report output already exists: %s", report_name)

        session.close()
