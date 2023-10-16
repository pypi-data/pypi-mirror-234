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
CORE-POS -> "self" data import
"""

import logging
from collections import OrderedDict

from corepos.db.office_op import model as corepos

from rattail import importing
from rattail_corepos.corepos.office.importing import db as corepos_importing
from rattail_corepos.corepos.office.importing.db.corepos import FromCoreHandler
from rattail_corepos.corepos.office.util import get_blueline_template, make_blueline


log = logging.getLogger(__name__)


class FromCoreOfficeToSelf(FromCoreHandler, corepos_importing.model.ToCoreHandler):
    """
    Common base class for import handlers which read data from the
    CORE Office DB for the sake of updating misc. other tables in that
    same DB.
    """
    local_key = 'self'

    def begin_local_transaction(self):
        self.session = self.host_session

    def rollback_transaction(self):
        self.rollback_host_transaction()

    def commit_transaction(self):
        self.commit_host_transaction()

    def get_importers(self):
        importers = OrderedDict()
        importers['CustomerClassic'] = CustomerClassicImporter
        return importers


class FromCoreOffice(importing.FromSQLAlchemy):
    """
    Common base class for the "host" side of importers which read data
    from the CORE Office DB for the sake of updating misc. other
    tables in that same DB.
    """


class CustomerClassicImporter(FromCoreOffice, corepos_importing.model.CustomerClassicImporter):
    """
    custdata -> custdata

    Primarily used to update the ``blueLine`` field.
    """
    host_model_class = corepos.CustomerClassic
    supported_fields = [
        'id',
        'blue_line',
    ]
    allow_create = False
    allow_delete = False

    def setup(self):
        super().setup()
        self.blueline_template = get_blueline_template(self.config)

    def normalize_host_object(self, customer):

        if not customer.member_type:
            log.warning("skipping customer #%s with no member type: %s",
                        customer.card_number, customer)
            return

        blueline = make_blueline(self.config, customer, template=self.blueline_template)
        return {
            'id': customer.id,
            'blue_line': blueline,
        }
