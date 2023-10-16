# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
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
Products Handler
"""

from corepos.db.office_op import Session as CoreSession

from rattail import products as base


class CoreProductsHandlerMixin(object):
    """
    Products handler mixin for CORE-POS integration
    """

    def find_wild_uoms_in_corepos(self, session, **kwargs):
        core_session = CoreSession()

        wild_uoms = core_session.execute("""
        SELECT DISTINCT UPPER(TRIM(unitofmeasure))
        FROM products
        WHERE unitofmeasure IS NOT NULL AND TRIM(unitofmeasure) != ''
        ORDER BY 1
        """).fetchall()

        core_session.close()
        return [row[0] for row in wild_uoms]


class CoreProductsHandler(base.ProductsHandler, CoreProductsHandlerMixin):
    """
    Custom products handler for use with CORE-POS. 
    """

    def find_wild_uoms(self, session, **kwargs):
        return self.find_wild_uoms_in_corepos(session, **kwargs)
