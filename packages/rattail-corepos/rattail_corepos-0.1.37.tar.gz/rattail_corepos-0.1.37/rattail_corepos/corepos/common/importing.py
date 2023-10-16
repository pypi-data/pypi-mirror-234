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
Common importing logic for CORE-POS
"""

from rattail import importing


class ToCore(importing.ToSQLAlchemy):
    """
    Base class for all CORE model importers; i.e. anything which uses
    a CORE DB for the local side.
    """

    def create_object(self, key, host_data):

        # NOTE! some tables in CORE DB may be using the MyISAM storage engine,
        # which means it is *not* transaction-safe and therefore we cannot rely
        # on "rollback" if in dry-run mode!  in other words we better not touch
        # the record at all, for dry run
        if self.dry_run:
            return host_data

        return super(ToCore, self).create_object(key, host_data)

    def update_object(self, obj, host_data, **kwargs):

        # NOTE! some tables in CORE DB may be using the MyISAM storage engine,
        # which means it is *not* transaction-safe and therefore we cannot rely
        # on "rollback" if in dry-run mode!  in other words we better not touch
        # the record at all, for dry run
        if self.dry_run:
            return obj

        return super(ToCore, self).update_object(obj, host_data, **kwargs)

    def delete_object(self, obj):

        # NOTE! some tables in CORE DB may be using the MyISAM storage engine,
        # which means it is *not* transaction-safe and therefore we cannot rely
        # on "rollback" if in dry-run mode!  in other words we better not touch
        # the record at all, for dry run
        if self.dry_run:
            return True

        return super(ToCore, self).delete_object(obj)
