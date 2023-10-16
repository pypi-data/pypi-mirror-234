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
Handler for Vendor Catalog batches
"""

import decimal

from rattail.batch import vendorcatalog as base


class VendorCatalogHandler(base.VendorCatalogHandler):
    """
    Handler for vendor catalog batches.
    """
    # default logic tries to update versions after execution, but since we just
    # update CORE-POS via API there's no need
    version_catchup_execute = None

    def add_row(self, batch, row):

        # CORE unit costs seem to be rounded to 3 decimal places
        if row.unit_cost:
            row.unit_cost = row.unit_cost.quantize(decimal.Decimal('0.123'))

        # CORE bases its cost off the unit instead of case.  so here we make
        # sure the case cost is cleanly derived from unit cost.
        if row.case_cost and row.unit_cost and row.case_size:
            row.case_cost = row.unit_cost * row.case_size

        # okay now continue as normal
        super(VendorCatalogHandler, self).add_row(batch, row)

    def describe_execution(self, batch, **kwargs):
        return ("The `vendorItems` table in CORE-POS will be updated directly "
                "via API, for all rows indicating a change etc.  You may also "
                "update `products.cost` if desired.")

    def execute(self, batch, progress=None, **kwargs):
        """
        Update CORE-POS etc.
        """
        rows = [row for row in batch.active_rows()
                if row.status_code in (row.STATUS_NEW_COST,
                                       row.STATUS_UPDATE_COST,
                                       row.STATUS_CHANGE_VENDOR_ITEM_CODE,
                                       row.STATUS_CHANGE_CASE_SIZE,
                                       row.STATUS_CHANGE_COST)]

        if rows:
            vendor_id = batch.vendor.corepos_id
            if not vendor_id:
                raise ValueError("Batch vendor does not have valid CORE-POS ID")

            self.api = self.app.get_corepos_handler.make_webapi()
            self.update_corepos(batch, rows, vendor_id, progress=progress,
                                # update_product_costs=kwargs.get('update_product_costs', False),
            )

        return True

    def update_corepos(self, batch, rows, vendor_id, progress=None,
                       # TODO: this kwarg seems perhaps useful, but for now we
                       # are auto-detecting when such an update is needed
                       #update_product_costs=False,
    ):
        """
        Update the `vendorItems` table in CORE-POS (and maybe `products` too).
        """
        def update(row, i):
            # we may need this value in a couple places
            unit_cost = float(row.unit_cost)

            # we will want to set default vendor for the product, if it does
            # not yet have one
            first_vendor = False
            if not row.product.costs:
                first_vendor = True
            # core_product = self.api.get_product(row.item_id)
            # if not core_product['default_vendor_id']:
            #     first_vendor = True

            # figure out if we are "updating the same, primary" cost record,
            # b/c if so we will want to update product accordingly also.  this
            # is always the case when this is the first vendor for product.
            updating_primary = first_vendor
            if not updating_primary:
                cost = row.product.cost
                if cost and cost is row.cost:
                    updating_primary = True
                # core_items = self.api.get_vendor_items(upc=row.item_id)
                # if core_items:
                #     core_item = core_items[0]
                #     if core_item['sku'] == row.vendor_code:
                #         updating_primary = True

            # create or update the `vendorItems` record in CORE
            self.api.set_vendor_item(sku=row.vendor_code,
                                     vendorID=vendor_id,
                                     upc=row.item_id,
                                     brand=row.brand_name,
                                     description=row.description,
                                     size=row.size,
                                     units=row.case_size,
                                     cost=unit_cost,
                                     # TODO: we (may) have vendor SRP, but pretty
                                     # sure CORE has different plans for its `srp`
                                     #srp=row.suggested_retail,
            )

            # TODO: CORE does not have the concept of a true "default"
            # `vendorItems` record, but rather uses the `modified` timestamp
            # for pseudo-default.  this means any given product may wind up
            # with a new/different pseudo-default when the above operation
            # completes.  in which case, perhaps we should *always* update
            # `products.cost` accordingly (below)..?  er, still only if the
            # product's `default_vendor_id` matches at least, i guess...  for
            # now we are only doing so if it "obviously" needs it.

            # maybe also update `products` record in CORE
            if updating_primary:
                kwargs = {'cost': unit_cost}
                if first_vendor:
                    kwargs['default_vendor_id'] = vendor_id
                self.api.set_product(upc=row.item_id, **kwargs)

        self.progress_loop(update, rows, progress,
                           message="Updating CORE-POS via API")
