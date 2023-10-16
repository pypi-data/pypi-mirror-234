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
CORE-POS -> Catapult Inventory Workbook
"""

import re
import datetime
import decimal
import logging
from collections import OrderedDict

from sqlalchemy.exc import ProgrammingError
from sqlalchemy import orm
from sqlalchemy.orm.exc import NoResultFound

from corepos import enum as corepos_enum
from corepos.db.office_op import model as corepos
from corepos.db.util import table_exists

from rattail.gpc import GPC
from rattail.core import get_uuid
from rattail.importing.handlers import ToFileHandler
from rattail_corepos.corepos.importing.db.corepos import FromCoreHandler, FromCore
from rattail_onager.catapult.importing import inventory as catapult_importing


log = logging.getLogger(__name__)


class FromCoreToCatapult(FromCoreHandler, ToFileHandler):
    """
    Handler for CORE -> Catapult (Inventory Workbook)
    """
    host_title = "CORE-POS"
    local_title = "Catapult (Inventory Workbook)"
    direction = 'export'

    def get_importers(self):
        importers = OrderedDict()
        importers['InventoryItem'] = InventoryItemImporter
        return importers


class InventoryItemImporter(FromCore, catapult_importing.model.InventoryItemImporter):
    """
    Inventory Item data importer.
    """
    host_model_class = corepos.Product
    # note that we use a "dummy" uuid key here, so logic will consider each row
    # to be unique, even when duplicate item_id's are present
    key = 'uuid'
    supported_fields = [
        'uuid',
        'item_id',
        'dept_id',
        'dept_name',
        'receipt_alias',
        'brand',
        'item_name',
        'size',
        # 'sugg_retail',
        'last_cost',
        'price_divider',
        'base_price',
        # 'disc_mult',
        'ideal_margin',
        'bottle_deposit',
        # 'pos_menu_group',
        'scale_label',
        'sold_by_ea_or_lb',
        'quantity_required',
        'weight_profile',
        'tax_1',
        'tax_2',
        'spec_tend_1',
        'spec_tend_2',
        'age_required',
        'location',
        # 'family_line',
        'alt_id',
        'alt_receipt_alias',
        'alt_pkg_qty',
        'alt_pkg_price',
        'auto_discount',
        'supplier_unit_id',
        'supplier_id',
        'unit',
        'num_pkgs',
        # 'cs_pk_multiplier',
        # 'dsd',
        'pf1',
        # 'pf2',
        # 'pf3',
        # 'pf4',
        # 'pf5',
        # 'pf6',
        # 'pf7',
        # 'pf8',
        'memo',
        'scale_shelf_life',
        'scale_shelf_life_type',
        'scale_ingredient_text',
    ]

    # we want to add a "duplicate" column at the end
    include_duplicate_column = True

    # we want to add an "alternate for" column at the end
    include_alt_for_column = True

    type2_upc_pattern = re.compile(r'^2(\d{5})00000\d')

    def setup(self):
        super(InventoryItemImporter, self).setup()

        # this is used for sorting, when a value has no date
        self.old_datetime = datetime.datetime(1900, 1, 1)

        self.exclude_invalid_upc = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.exclude_invalid_upc',
            default=False)

        self.warn_invalid_upc = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_invalid_upc',
            default=True)

        self.ignored_upcs = self.config.getlist(
            'corepos', 'exporting.catapult_inventory.ignored_upcs')

        self.exclude_missing_department = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.exclude_missing_department',
            default=False)

        self.warn_missing_department = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_missing_department',
            default=True)

        self.warn_empty_subdepartment = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_empty_subdepartment',
            default=True)

        self.warn_truncated_receipt_alias = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_truncated_receipt_alias',
            default=True)

        self.warn_size_null_byte = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_size_null_byte',
            default=True)

        self.warn_unknown_deposit = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_unknown_deposit',
            default=True)

        self.warn_scale_label_non_plu = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_scale_label_non_plu',
            default=True)

        self.warn_scale_label_short_plu = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_scale_label_short_plu',
            default=True)

        self.warn_weight_profile_non_plu = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_weight_profile_non_plu',
            default=True)

        self.warn_multiple_vendor_items = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_multiple_vendor_items',
            default=True)

        self.warn_no_valid_vendor_items = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_no_valid_vendor_items',
            default=True)

        self.warn_truncated_memo = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_truncated_memo',
            default=True)

        self.warn_scale_ingredients_newline = self.config.getbool(
            'corepos', 'exporting.catapult_inventory.warn_scale_ingredients_newline',
            default=True)

        self.floor_sections_exist = table_exists(self.host_session,
                                                 corepos.FloorSection)
        self.tax_components_exist = table_exists(self.host_session,
                                                 corepos.TaxRateComponent)

        self.tax_rate_ids_1 = self.config.getlist(
            'corepos', 'exporting.catapult_inventory.tax_rate_ids_1', default=[])
        self.tax_rate_ids_1 = [int(id) for id in self.tax_rate_ids_1]
        self.tax_rate_ids_2 = self.config.getlist(
            'corepos', 'exporting.catapult_inventory.tax_rate_ids_2', default=[])
        self.tax_rate_ids_2 = [int(id) for id in self.tax_rate_ids_2]

        # TODO: should add component id levels too?
        # tax_component_ids_1 = (1,)
        # tax_component_ids_2 = (2,)

        self.cache_bottle_deposits()
        self.cache_like_codes()

    def cache_bottle_deposits(self):
        self.deposits = {}
        deposits = self.host_session.query(corepos.Product.deposit.distinct())\
                                    .all()

        def cache(deposit, i):
            assert isinstance(deposit, tuple)
            assert len(deposit) == 1
            deposit = deposit[0]
            if deposit:
                deposit = int(deposit)
                upc = "{:013d}".format(deposit)
                try:
                    product = self.host_session.query(corepos.Product)\
                                               .filter(corepos.Product.upc == upc)\
                                               .one()
                except NoResultFound:
                    pass        # we will log warnings per-item later
                else:
                    self.deposits[deposit] = product

        self.progress_loop(cache, deposits,
                           message="Caching product deposits data")

    def cache_like_codes(self):
        self.like_codes = {}
        mappings = self.host_session.query(corepos.ProductLikeCode)\
                                    .order_by(corepos.ProductLikeCode.like_code_id,
                                              corepos.ProductLikeCode.upc)\
                                    .all()

        def cache(mapping, i):
            self.like_codes.setdefault(mapping.like_code_id, []).append(mapping)

        self.progress_loop(cache, mappings,
                           message="Caching like codes data")

    def query(self):
        query = self.host_session.query(corepos.Product)\
                                 .order_by(corepos.Product.upc)\
                                 .options(orm.joinedload(corepos.Product.department))\
                                 .options(orm.joinedload(corepos.Product.subdepartment))\
                                 .options(orm.joinedload(corepos.Product.vendor_items)\
                                          .joinedload(corepos.VendorItem.vendor))\
                                 .options(orm.joinedload(corepos.Product.default_vendor))\
                                 .options(orm.joinedload(corepos.Product.scale_item))\
                                 .options(orm.joinedload(corepos.Product.user_info))\
                                 .options(orm.joinedload(corepos.Product.tax_rate))\
                                 .options(orm.joinedload(corepos.Product._like_code))
        if self.floor_sections_exist:
            query = query.options(orm.joinedload(corepos.Product.physical_location)\
                                  .joinedload(corepos.ProductPhysicalLocation.floor_section))
        return query

    def normalize_host_data(self, host_objects=None):
        normalized = super(InventoryItemImporter, self).normalize_host_data(host_objects=host_objects)

        # re-sort the results by item_id, since e.g. original UPC from CORE may
        # have been replaced with a PLU.  also put non-numeric first, to bring
        # them to user's attention
        numeric = []
        non_numeric = []
        for row in normalized:
            if row['item_id'] and row['item_id'].isdigit():
                numeric.append(row)
            else:
                non_numeric.append(row)
        numeric.sort(key=lambda row: int(row['item_id']))
        non_numeric.sort(key=lambda row: row['item_id'])
        normalized = non_numeric + numeric

        # now we must check for duplicate item ids, and mark rows accordingly.
        # but we *do* want to include/preserve all rows, hence we mark them
        # instead of pruning some out. first step is to group all by item_id
        items = {}

        def collect(row, i):
            items.setdefault(row['item_id'], []).append(row)

        self.progress_loop(collect, normalized,
                           message="Grouping rows by Item ID")

        # now we go through our groupings and for any item_id with more than 1
        # row, we'll mark each row as having a duplicate item_id.  note that
        # this modifies such a row "in-place" for our overall return value
        def inspect(rows, i):
            if len(rows) > 1:
                for row in rows:
                    row['__duplicate__'] = True

        self.progress_loop(inspect, list(items.values()),
                           message="Marking any duplicate Item IDs")

        # finally, we must inspect the like codes and figure out which
        # product(s) should potentially be considered "alternate for" another.
        # first step here will be to create mapping of item_id values for each
        # CORE product in our result set
        item_ids = {}

        def mapp(row, i):
            product = row['__product__']
            item_ids[product.upc] = row['item_id']

        self.progress_loop(mapp, normalized,
                           message="Mapping item_id for CORE products")

        # next step here is to check each product and mark "alt for" as needed
        def inspect(row, i):
            product = row['__product__']
            if product.like_code:
                others = self.like_codes.get(product.like_code.id)
                if others:
                    first = others[0]
                    if first.upc != product.upc:
                        row['__alternate_for__'] = item_ids[first.upc]

        self.progress_loop(inspect, normalized,
                           message="Marking any \"alternate for\" items")

        return normalized

    def normalize_host_object(self, product):
        item_id = product.upc

        if self.ignored_upcs and item_id in self.ignored_upcs:
            log.debug("ignoring UPC %s for product: %s", product.upc, product)
            return

        if not item_id:
            logger = log.warning if self.warn_invalid_upc else log.debug
            logger("product id %s has no upc: %s", product.id, product)
            if self.exclude_invalid_upc:
                return

        if not item_id.isdigit():
            logger = log.warning if self.warn_invalid_upc else log.debug
            logger("product %s has non-numeric upc: %s",
                   product.upc, product)
            if self.exclude_invalid_upc:
                return

        # convert item_id either to a PLU, or formatted UPC
        is_plu = False
        if item_id.isdigit():   # can only convert if it's numeric!
            if len(str(int(item_id))) < 6:
                is_plu = True
                item_id = str(int(item_id))
            else: # must add check digit, and re-format
                upc = GPC(item_id, calc_check_digit='upc')
                item_id = str(upc)
                assert len(item_id) == 14
                # drop leading zero(s)
                if item_id[1] == '0': # UPC-A
                    item_id = item_id[2:]
                    assert len(item_id) == 12
                else: # EAN13
                    item_id = item_id[1:]
                    assert len(item_id) == 13

        # figure out the "scale label" data, which may also affect item_id
        scale_item = product.scale_item
        scale_label = None
        if scale_item:
            scale_label = 'Y'
            if item_id.isdigit():
                if len(item_id) < 5:
                    logger = log.warning if self.warn_scale_label_short_plu else log.debug
                    logger("product %s has scale label, but PLU is less than 5 digits (%s): %s",
                           product.upc, item_id, product)
                elif len(item_id) > 5:
                    match = self.type2_upc_pattern.match(item_id)
                    if match:
                        # convert type-2 UPC to PLU
                        is_plu = True
                        item_id = str(int(match.group(1)))
                        log.debug("converted type-2 UPC %s to PLU %s for: %s",
                                  product.upc, item_id, product)
                    else:
                        logger = log.warning if self.warn_scale_label_non_plu else log.debug
                        logger("product %s has scale label, but non-PLU item_id: %s",
                               product.upc, product)

        department = product.department
        if not department:
            logger = log.warning if self.warn_missing_department else log.debug
            logger("product %s has no department: %s", product.upc, product)
            if self.exclude_missing_department:
                return

        # size may come from one of two fields, or combination thereof
        pack_size = (product.size or '').strip()
        uom = (product.unit_of_measure or '').strip()
        numeric_pack = False
        if pack_size:
            try:
                decimal.Decimal(pack_size)
            except decimal.InvalidOperation:
                pass
            else:
                numeric_pack = True
        if numeric_pack:
            size = "{} {}".format(pack_size, uom).strip()
        else:
            size = pack_size or uom or None
        # TODO: this logic may actually be client-specific?  i just happened to
        # find some null chars in a client DB and needed to avoid them, b/c the
        # openpyxl lib said IllegalCharacterError
        if size is not None and '\x00' in size:
            logger = log.warning if self.warn_size_null_byte else log.debug
            logger("product %s has null byte in size field: %s",
                   product.upc, product)
            size = size.replace('\x00', '')

        price_divider = None
        if (product.quantity and product.group_price and
            product.price_method == corepos_enum.PRODUCT_PRICE_METHOD_ALWAYS):
            diff = (product.quantity * product.normal_price) - product.group_price
            if abs(round(diff, 2)) > .01:
                log.warning("product %s has multi-price with $%0.2f diff: %s",
                            product.upc, diff, product)
            price_divider = product.quantity

        bottle_deposit = None
        if product.deposit:
            deposit = int(product.deposit)
            if deposit in self.deposits:
                bottle_deposit = self.deposits[deposit].normal_price
            else:
                logger = log.warning if self.warn_unknown_deposit else log.debug
                logger("product %s has unknown deposit %s which will be ignored: %s",
                       product.upc, deposit, product)

        sold_by_ea_or_lb = None
        if is_plu:
            sold_by_ea_or_lb = 'LB' if product.scale else 'EA'

        weight_profile = None
        if product.scale or scale_item:
            if not is_plu:
                logger = log.warning if self.warn_weight_profile_non_plu else log.debug
                logger("product %s has weight profile, but non-PLU item_id %s: %s",
                       product.upc, item_id, product)
            weight_profile = 'LBNT'

        # calculate tax rates according to configured "mappings"
        tax_1 = 0
        tax_2 = 0
        if product.tax_rate:

            # TODO: need to finish the logic to handle tax components
            if self.tax_components_exist and product.tax_rate.components:
                # for component in product.tax_rate.components:
                #     if tax_component_ids_1 and component.id in tax_component_ids_1:
                #         tax_1 += component.rate
                #     if tax_component_ids_2 and component.id in tax_component_ids_2:
                #         tax_2 += component.rate
                raise NotImplementedError

            else: # no components
                rate = product.tax_rate
                if self.tax_rate_ids_1 and rate.id in self.tax_rate_ids_1:
                    tax_1 += rate.rate
                if self.tax_rate_ids_2 and rate.id in self.tax_rate_ids_2:
                    tax_2 += rate.rate
                if not (self.tax_rate_ids_1 or self.tax_rate_ids_2) and rate.rate:
                    log.warning("product %s has unknown tax rate %s (%s) which will "
                                "be considered as tax 1: %s",
                                product.upc, rate.rate, rate.description, product)
                    tax_1 += rate.rate

        location = None
        if self.floor_sections_exist and product.physical_location and product.physical_location.floor_section:
            location = product.physical_location.floor_section.name
            if len(location) > 30:
                log.warning("product %s has location length %s; will truncate: %s",
                            product.upc, len(location), location)
                location = location[:30]

        # no alt item (or auto discount) by default
        alt_id = None
        alt_receipt_alias = None
        alt_pkg_qty = None
        alt_pkg_price = None
        auto_discount = None

        # make an alt item, when main item has pack pricing (e.g. Zevia sodas)
        # note that in this case the main item_id and alt_id are the same
        if (product.quantity and product.group_price and
            product.price_method == corepos_enum.PRODUCT_PRICE_METHOD_FULL_SETS):
            alt_id = item_id
            suffix = "{}-PK".format(product.quantity)
            alt_receipt_alias = "{} {}".format(product.description, suffix)
            if len(alt_receipt_alias) > 32:
                logger = log.warning if self.warn_truncated_receipt_alias else log.debug
                logger("alt receipt alias for %s is %s chars; must truncate: %s",
                       alt_id, len(alt_receipt_alias), alt_receipt_alias)
                overage = len(alt_receipt_alias) - 32
                alt_receipt_alias = "{} {}".format(
                    product.description[:-overage], suffix)
                assert len(alt_receipt_alias) == 32
            alt_pkg_qty = product.quantity
            alt_pkg_price = product.group_price

            # we also must declare an "auto discount" to get pack price
            auto_discount = "{} @ ${:0.2f}".format(alt_pkg_qty, alt_pkg_price)

        # no supplier info by default
        supplier_unit_id = None
        supplier_id = None
        supplier_unit = None
        supplier_num_pkgs = None

        # maybe add supplier info, for "default" `vendorItems` record.  we'll
        # have to get a little creative to figure out which is the default
        vendor_items = []

        # first we try to narrow down according to product's default vendor
        if product.default_vendor:
            vendor_items = [item for item in product.vendor_items
                            if item.vendor is product.default_vendor]

        # but if that didn't work, just use any "valid" vendorItems
        if not vendor_items:
            # valid in this context means, not missing vendor
            vendor_items = [item for item in product.vendor_items
                            if item.vendor]
            if not vendor_items and product.vendor_items:
                logger = log.warning if self.warn_no_valid_vendor_items else log.debug
                logger("product %s has %s vendorItems but each is missing (valid) vendor: %s",
                       product.upc, len(product.vendor_items), product)

        if vendor_items:
            if len(vendor_items) > 1:

                # try to narrow down a bit further, based on valid 'units' amount
                valid_items = [item for item in vendor_items
                               if item.units]
                if valid_items:
                    vendor_items = valid_items

                # warn if we still have more than one "obvious" vendor item
                if len(vendor_items) > 1:
                    logger = log.warning if self.warn_multiple_vendor_items else log.debug
                    logger("product %s has %s vendorItems to pick from: %s",
                           product.upc, len(vendor_items), product)

                    # sort the list so most recently modified is first
                    vendor_items.sort(key=lambda item: item.modified or self.old_datetime,
                                      reverse=True)

            # use the "first" vendor item available
            item = vendor_items[0]
            supplier_unit_id = item.sku
            supplier_id = item.vendor.name
            supplier_num_pkgs = item.units or 1
            if supplier_num_pkgs == 1:
                supplier_unit = 'LB' if product.scale else 'EA'
            else:
                supplier_unit = 'CS'

        pf1 = None
        if product.subdepartment:
            if not product.subdepartment.number:
                logger = log.warning if self.warn_empty_subdepartment else log.debug
                logger("product %s has 'empty' subdepartment number: %s",
                       product.upc, product)
            else:
                pf1 = "{} {}".format(product.subdepartment.number,
                                     product.subdepartment.name)

        memo = None
        if product.user_info and product.user_info.long_text is not None:
            memo = str(product.user_info.long_text)
        if memo and len(memo) > 254:
            logger = log.warning if self.warn_truncated_memo else log.debug
            logger("product %s has memo of length %s; will truncate: %s",
                   product.upc, len(memo), memo)
            memo = memo[:254]

        scale_ingredient_text = None
        if scale_item:
            scale_ingredient_text = scale_item.text
            if "\n" in scale_ingredient_text:
                logger = log.warning if self.warn_scale_ingredients_newline else log.debug
                logger("must remove carriage returns for scale ingredients: %s",
                       scale_ingredient_text)
                scale_ingredient_text = scale_ingredient_text.replace("\n", " ")

        return {
            '__product__': product,
            '__original_item_id__': product.upc,
            'uuid': get_uuid(),
            'item_id': item_id,
            'dept_id': department.number if department else None,
            'dept_name': department.name if department else None,
            'receipt_alias': product.description,
            'brand': product.brand,
            'item_name': product.description,
            'size': size,

            # TODO: does CORE have this?
            # 'sugg_retail': None,

            'last_cost': product.cost,
            'price_divider': price_divider,
            'base_price': product.normal_price,
            'ideal_margin': department.margin * 100 if department and department.margin else None,

            # TODO: does CORE have these?
            # 'disc_mult': None,

            'bottle_deposit': bottle_deposit,

            # TODO: does CORE have this?
            # 'pos_menu_group': None,

            'scale_label': scale_label,
            'sold_by_ea_or_lb': sold_by_ea_or_lb,
            'quantity_required': 'Y' if product.quantity_enforced else None,
            'weight_profile': weight_profile,
            'tax_1': tax_1 or None, # TODO: logic above is unfinished
            'tax_2': tax_2 or None, # TODO: logic above is unfinished
            'spec_tend_1': 'EBT' if product.foodstamp else None,
            'spec_tend_2': 'WIC' if product.wicable else None,
            'age_required': product.id_enforced or None,
            'location': location,

            # TODO: does CORE have these?
            # 'family_line': None,

            'alt_id': alt_id,
            'alt_receipt_alias': alt_receipt_alias,
            'alt_pkg_qty': alt_pkg_qty,
            'alt_pkg_price': alt_pkg_price,
            'auto_discount': auto_discount,
            'supplier_unit_id': supplier_unit_id,
            'supplier_id': supplier_id,
            'unit': supplier_unit,
            'num_pkgs': supplier_num_pkgs,

            # TODO: does CORE have these?
            # 'cs_pk_multiplier': None,
            # 'dsd': None,

            'pf1': pf1,

            # TODO: are these needed?
            # 'pf2',
            # 'pf3',
            # 'pf4',
            # 'pf5',
            # 'pf6',
            # 'pf7',
            # 'pf8',

            'memo': memo,
            'scale_shelf_life': scale_item.shelf_life if scale_item else None,
            'scale_shelf_life_type': 0 if scale_item else None,
            'scale_ingredient_text': scale_ingredient_text,
        }
