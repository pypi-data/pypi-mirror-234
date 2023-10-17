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
Telemetry Commands
"""

import logging
import pprint

from rattail.commands import Subcommand


log = logging.getLogger(__name__)


class Telemetry(Subcommand):
    """
    Submit telemetry data to a server
    """
    name = 'telemetry'
    description = __doc__.strip()

    def add_parser_args(self, parser):

        parser.add_argument('--profile', '-p', metavar='KEY',
                            help="Profile (type) of telemetry data to collect.  "
                            "This also determines where/how data is submitted.  "
                            "If not specified, default logic is assumed.")

        parser.add_argument('--dry-run', action='store_true',
                            help="Go through all the motions but do not submit "
                            "the data to server.")

    def run(self, args):
        self.handler = self.app.get_telemetry_handler()

        data = self.handler.collect_all_data(profile=args.profile)
        log.info("data collected okay: %s", ', '.join(sorted(data)))
        log.debug("%s", data)

        if self.verbose:
            print("COLLECTED DATA:")
            pprint.pprint(data)

        if args.dry_run:
            log.info("dry run, so will not submit data to server")
        else:
            self.handler.submit_all_data(data, profile=args.profile)
            log.info("data submitted okay")
