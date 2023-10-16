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
Rattail Commands
"""

from rattail import commands
from rattail.util import load_object


class ExportCore(commands.ImportSubcommand):
    """
    Export data from Rattail to CORE-POS
    """
    name = 'export-corepos'
    description = __doc__.strip()
    handler_key = 'to_corepos_api.from_rattail.export'


class ImportCOREPOSAPI(commands.ImportSubcommand):
    """
    Import data from a CORE POS API
    """
    name = 'import-corepos-api'
    description = __doc__.strip()
    handler_key = 'to_rattail.from_corepos_api.import'


class ImportCOREPOSDB(commands.ImportSubcommand):
    """
    Import data from a CORE POS database
    """
    name = 'import-corepos-db'
    description = __doc__.strip()
    handler_key = 'to_rattail.from_corepos_db_office_op.import'

    def add_parser_args(self, parser):
        super().add_parser_args(parser)

        parser.add_argument('--corepos-dbtype', metavar='TYPE', default='office_op',
                            choices=['office_op', 'office_trans'],
                            help="Config *type* for CORE-POS database engine to be used as "
                            "host.  Default type is 'office_op' - this determines which "
                            "config section is used with regard to the --corepos-dbkey arg.")

        parser.add_argument('--corepos-dbkey', metavar='KEY', default='default',
                            help="Config key for CORE POS database engine to be used as the \"host\", "
                            "i.e. the source of the data to be imported.  This key " "must be "
                            "defined in the [rattail_corepos.db] section of your config file.  "
                            "Defaults to 'default'.")

    def get_handler_kwargs(self, **kwargs):
        if 'args' in kwargs:
            kwargs['corepos_dbtype'] = kwargs['args'].corepos_dbtype
            kwargs['corepos_dbkey'] = kwargs['args'].corepos_dbkey
        return kwargs


class CoreImportSquare(commands.ImportFromCSV):
    """
    Import transaction data from Square into CORE
    """
    name = 'corepos-import-square'
    description = __doc__.strip()
    handler_key = 'to_corepos_db_office_trans.from_square_csv.import'
