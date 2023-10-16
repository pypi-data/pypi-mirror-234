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
CORE-POS commands
"""

import sys
import warnings

from rattail import commands
from rattail_corepos import __version__
from rattail_corepos.corepos.office.commands import ExportCSV, ImportCSV


def main(*args):
    """
    Primary entry point for Crepes command system
    """
    if args:
        args = list(args)
    else:
        args = sys.argv[1:]

    cmd = Command()
    cmd.run(*args)


class Command(commands.Command):
    """
    Primary command for Crepes (CORE-POS)
    """
    name = 'crepes'
    version = __version__
    description = "Crepes -- command line interface for CORE-POS"
    long_description = ""


class ImportToCore(commands.ImportSubcommand):
    """
    Generic base class for commands which import *to* a CORE DB.
    """


class ExportCore(commands.ImportSubcommand):
    """
    Export data to another CORE database
    """
    name = 'export-core'
    description = __doc__.strip()
    handler_key = 'to_corepos_db_office_op.from_corepos_db_office_op.export'
    default_dbkey = 'host'

    def add_parser_args(self, parser):
        super(ExportCore, self).add_parser_args(parser)
        parser.add_argument('--dbkey', metavar='KEY', default=self.default_dbkey,
                            help="Config key for database engine to be used as the \"target\" "
                            "CORE DB, i.e. where data will be exported.  This key must be "
                            "defined in the [rattail_corepos.db] section of your config file.")

    def get_handler_kwargs(self, **kwargs):
        if 'args' in kwargs:
            kwargs['dbkey'] = kwargs['args'].dbkey
        return kwargs


class LegacyExportCSV(ExportCSV):

    def __init__(self, *args, **kwargs):
        warnings.warn("the `crepes export-csv` command is deprecated; "
                      "please use `core-office export-csv` instead",
                      DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)


class ImportCore(ImportToCore):
    """
    Import data from another CORE database
    """
    name = 'import-core'
    description = __doc__.strip()
    handler_key = 'to_corepos_db_office_op.from_corepos_db_office_op.import'
    accepts_dbkey_param = True

    def add_parser_args(self, parser):
        super(ImportCore, self).add_parser_args(parser)
        if self.accepts_dbkey_param:
            parser.add_argument('--dbkey', metavar='KEY', default='host',
                                help="Config key for database engine to be used as the CORE "
                                "\"host\", i.e. the source of the data to be imported.  This key "
                                "must be defined in the [rattail_corepos.db] section of your config file.  "
                                "Defaults to 'host'.")

    def get_handler_kwargs(self, **kwargs):
        if self.accepts_dbkey_param:
            if 'args' in kwargs:
                kwargs['dbkey'] = kwargs['args'].dbkey
        return kwargs


class LegacyImportCSV(ImportCSV):

    def __init__(self, *args, **kwargs):
        warnings.warn("the `crepes import-csv` command is deprecated; "
                      "please use `core-office import-csv` instead",
                      DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)
