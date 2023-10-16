# -*- coding: utf-8; -*-
################################################################################
#
#  pyCOREPOS -- Python Interface to CORE POS
#  Copyright © 2018-2023 Lance Edgar
#
#  This file is part of pyCOREPOS.
#
#  pyCOREPOS is free software: you can redistribute it and/or modify it under
#  the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  pyCOREPOS is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  pyCOREPOS.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Data model for CORE POS "office_op" DB
"""

import datetime
import logging

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.ext.associationproxy import association_proxy


log = logging.getLogger(__name__)

Base = orm.declarative_base()


class StringableDateTime(sa.TypeDecorator):
    """
    Sort of a hack, to let us string-ify certain DateTime values when
    generating "raw" SQL output.

    cf. https://docs.sqlalchemy.org/en/14/faq/sqlexpressions.html#rendering-bound-parameters-inline
    """
    impl = sa.DateTime

    def process_literal_param(self, value, dialect):
        if value is None:
            return 'NULL'
        if isinstance(value, datetime.datetime):
            return "'{}'".format(value.strftime('%Y-%m-%d %H:%M:%S'))
        raise NotImplementedError


class Change(Base):
    """
    Represents a changed (or deleted) record, which is pending synchronization
    to another system(s).

    .. note::
       This table may or may not be installed to a given CORE Office Op DB.  Its
       presence is required if Rattail datasync needs to "watch" the DB.
    """
    __tablename__ = 'datasync_changes'

    id = sa.Column(sa.Integer(), nullable=False, primary_key=True)
    object_type = sa.Column(sa.String(length=255), nullable=False)
    object_key = sa.Column(sa.String(length=255), nullable=False)
    deleted = sa.Column(sa.Boolean(), nullable=False, default=False)


class Parameter(Base):
    """
    Represents a "parameter" value.
    """
    __tablename__ = 'parameters'

    store_id = sa.Column(sa.SmallInteger(), primary_key=True, nullable=False)

    lane_id = sa.Column(sa.SmallInteger(), primary_key=True, nullable=False)

    param_key = sa.Column(sa.String(length=100), primary_key=True, nullable=False)

    param_value = sa.Column(sa.String(length=255), nullable=True)

    is_array = sa.Column(sa.Boolean(), nullable=True)

    def __str__(self):
        return "{}-{} {}".format(self.store_id, self.lane_id, self.param_key)


class TableSyncRule(Base):
    """
    Represents a "table sync rule" value.
    """
    __tablename__ = 'TableSyncRules'

    id = sa.Column('tableSyncRuleID', sa.Integer(), nullable=False, primary_key=True, autoincrement=True)

    table_name = sa.Column('tableName', sa.String(length=255), nullable=False, primary_key=True)

    rule = sa.Column(sa.String(length=255), nullable=True)

    def __str__(self):
        return "{}: {}".format(self.table_name, self.rule)


class UserGroup(Base):
    """
    Represents a user/group assignment.
    """
    __tablename__ = 'userGroups'

    group_id = sa.Column('gid', sa.Integer(), nullable=False,
                         primary_key=True, autoincrement=False)

    name = sa.Column(sa.String(length=50), nullable=True)

    username = sa.Column(sa.String(length=50), nullable=False,
                         primary_key=True)

    def __str__(self):
        return self.name or ""


class User(Base):
    """
    Represents a user within CORE Office.
    """
    __tablename__ = 'Users'

    name = sa.Column(sa.String(length=50), nullable=False, primary_key=True)

    password = sa.Column(sa.String(length=255), nullable=True)

    salt = sa.Column(sa.String(length=10), nullable=True)

    uid = sa.Column(sa.String(length=4), nullable=True)

    session_id = sa.Column(sa.String(length=50), nullable=True)

    real_name = sa.Column(sa.String(length=75), nullable=True)

    email = sa.Column(sa.String(length=75), nullable=True)

    totp_url = sa.Column('totpURL', sa.String(length=255), nullable=True)

    def __str__(self):
        return self.name or ""


class Store(Base):
    """
    Represents a known store.
    """
    __tablename__ = 'Stores'

    storeID = sa.Column(sa.Integer(), nullable=False, primary_key=True, autoincrement=True)
    id = orm.synonym('storeID')

    description = sa.Column(sa.String(length=50), nullable=True)

    db_host = sa.Column('dbHost', sa.String(length=50), nullable=True)

    db_driver = sa.Column('dbDriver', sa.String(length=15), nullable=True)

    db_user = sa.Column('dbUser', sa.String(length=25), nullable=True)

    db_password = sa.Column('dbPassword', sa.String(length=25), nullable=True)

    trans_db = sa.Column('transDB', sa.String(length=20), nullable=True)

    op_db = sa.Column('opDB', sa.String(length=20), nullable=True)

    push = sa.Column(sa.Boolean(), nullable=True, default=True)

    pull = sa.Column(sa.Boolean(), nullable=True, default=True)

    has_own_items = sa.Column('hasOwnItems', sa.Boolean(), nullable=True, default=True)

    web_service_url = sa.Column('webServiceUrl', sa.String(length=255), nullable=True)

    def __str__(self):
        return self.description or ""


class SuperDepartment(Base):
    """
    Represents a "super" (parent/child) department mapping.
    """
    __tablename__ = 'superdepts'
    __table_args__ = (
        sa.ForeignKeyConstraint(['superID'], ['departments.dept_no']),
        sa.ForeignKeyConstraint(['dept_ID'], ['departments.dept_no']),
    )

    parent_id = sa.Column('superID', sa.Integer(), primary_key=True, autoincrement=False, nullable=False)
    parent = orm.relationship(
        'Department',
        foreign_keys=[parent_id],
        doc="""
        Reference to the parent department for this mapping.
        """,
        backref=orm.backref('_super_children'))

    child_id = sa.Column('dept_ID', sa.Integer(), primary_key=True, autoincrement=False, nullable=False)
    child = orm.relationship(
        'Department',
        foreign_keys=[child_id],
        doc="""
        Reference to the child department for this mapping.
        """,
        backref=orm.backref(
            '_super_parents',
            order_by=parent_id))

    def __str__(self):
        return "{} / {}".format(self.parent, self.child)


class Department(Base):
    """
    Represents a department within the organization.
    """
    __tablename__ = 'departments'

    number = sa.Column('dept_no', sa.SmallInteger(), primary_key=True, autoincrement=False, nullable=False)

    name = sa.Column('dept_name', sa.String(length=30), nullable=True)

    tax = sa.Column('dept_tax', sa.Boolean(), nullable=True)

    food_stampable = sa.Column('dept_fs', sa.Boolean(), nullable=True)

    limit = sa.Column('dept_limit', sa.Float(), nullable=True)

    minimum = sa.Column('dept_minimum', sa.Float(), nullable=True)

    discount = sa.Column('dept_discount', sa.Boolean(), nullable=True)

    see_id = sa.Column('dept_see_id', sa.SmallInteger(), nullable=True)

    modified = sa.Column(sa.DateTime(), nullable=True)

    modified_by_id = sa.Column('modifiedby', sa.Integer(), nullable=True)

    margin = sa.Column(sa.Float(), nullable=False)

    sales_code = sa.Column('salesCode', sa.Integer(), nullable=False)

    member_only = sa.Column('memberOnly', sa.SmallInteger(), nullable=False)

    def __str__(self):
        return self.name or ''


class Subdepartment(Base):
    """
    Represents a subdepartment within the organization.
    """
    __tablename__ = 'subdepts'
    __table_args__ = (
        sa.ForeignKeyConstraint(['dept_ID'], ['departments.dept_no']),
    )

    number = sa.Column('subdept_no', sa.SmallInteger(), primary_key=True, autoincrement=False, nullable=False)

    name = sa.Column('subdept_name', sa.String(length=30), nullable=True)

    department_number = sa.Column('dept_ID', sa.SmallInteger(), nullable=True)
    department = orm.relationship(
        Department,
        doc="""
        Reference to the parent :class:`Department` for this subdepartment.
        """)

    def __str__(self):
        return self.name or ''


class Vendor(Base):
    """
    Represents a vendor from which product may be purchased.
    """
    __tablename__ = 'vendors'
    
    # TODO: this maybe should be the pattern we use going forward, for all
    # models?  for now it was deemed necessary to "match" the API output
    vendorID = sa.Column(sa.Integer(), primary_key=True, autoincrement=False, nullable=False)
    id = orm.synonym('vendorID')

    name = sa.Column('vendorName', sa.String(length=50), nullable=True)

    abbreviation = sa.Column('vendorAbbreviation', sa.String(length=10), nullable=True)

    discount_rate = sa.Column('discountRate', sa.Float(), nullable=True)

    contact = orm.relationship(
        'VendorContact',
        uselist=False, doc="""
        Reference to the :class:`VendorContact` instance for this vendor.
        """)

    phone = association_proxy(
        'contact', 'phone',
        creator=lambda p: VendorContact(phone=p))

    fax = association_proxy(
        'contact', 'fax',
        creator=lambda f: VendorContact(fax=f))

    email = association_proxy(
        'contact', 'email',
        creator=lambda e: VendorContact(email=e))

    website = association_proxy(
        'contact', 'website',
        creator=lambda w: VendorContact(website=w))

    notes = association_proxy(
        'contact', 'notes',
        creator=lambda n: VendorContact(notes=n))

    def __str__(self):
        return self.name or ''


class VendorContact(Base):
    """
    A general contact record for a vendor.
    """
    __tablename__ = 'vendorContact'

    vendor_id = sa.Column('vendorID', sa.Integer(), sa.ForeignKey('vendors.vendorID'), primary_key=True, autoincrement=False, nullable=False)

    phone = sa.Column(sa.String(length=15), nullable=True)

    fax = sa.Column(sa.String(length=15), nullable=True)

    email = sa.Column(sa.String(length=50), nullable=True)

    website = sa.Column(sa.String(length=100), nullable=True)

    notes = sa.Column(sa.Text(), nullable=True)


class VendorDepartment(Base):
    """
    Represents specific details / settings for a given vendor in the context of
    a given department.
    """
    __tablename__ = 'vendorDepartments'
    __table_args__ = (
        sa.ForeignKeyConstraint(['vendorID'], ['vendors.vendorID']),
        sa.ForeignKeyConstraint(['deptID'], ['departments.dept_no']),
    )

    vendor_id = sa.Column('vendorID', sa.Integer(), primary_key=True, nullable=False)
    vendor = orm.relationship(
        Vendor,
        doc="""
        Reference to the :class:`Vendor` to which this record applies.
        """)

    department_id = sa.Column('deptID', sa.Integer(), primary_key=True, nullable=False)
    department = orm.relationship(
        Department,
        doc="""
        Reference to the :class:`Department` to which this record applies.
        """)

    name = sa.Column(sa.String(length=125), nullable=True)

    margin = sa.Column(sa.Float(), nullable=True)

    testing = sa.Column(sa.Float(), nullable=True)

    pos_department_id = sa.Column('posDeptID', sa.Integer(), nullable=True)


class TaxRate(Base):
    """
    Represents a tax rate.  Note that this may be a "combo" of various local
    tax rates / levels.
    """
    __tablename__ = 'taxrates'

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=False, nullable=False)

    rate = sa.Column(sa.Float(), nullable=True)

    description = sa.Column(sa.String(length=50), nullable=True)

    # TODO: this was not in some older DBs
    # sales_code = sa.Column('salesCode', sa.Integer(), nullable=True)

    def __str__(self):
        return self.description or ""


class TaxRateComponent(Base):
    """
    Represents a "component" of a tax rate.
    """
    __tablename__ = 'TaxRateComponents'
    __table_args__ = (
        sa.ForeignKeyConstraint(['taxRateID'], ['taxrates.id']),
    )

    taxRateComponentID = sa.Column(sa.Integer(), primary_key=True, autoincrement=True, nullable=False)
    id = orm.synonym('taxRateComponentID')

    tax_rate_id = sa.Column('taxRateID', sa.Integer())
    tax_rate = orm.relationship(TaxRate, backref='components')

    rate = sa.Column(sa.Float(), nullable=True)

    description = sa.Column(sa.String(length=50), nullable=True)

    def __str__(self):
        return self.description or ""


class LikeCode(Base):
    """
    Represents a "like code" for sake of product pricing.
    """
    __tablename__ = 'likeCodes'

    likeCode = sa.Column(sa.Integer(), primary_key=True, autoincrement=False, nullable=False)
    id = orm.synonym('likeCode')

    description = sa.Column('likeCodeDesc', sa.String(length=50), nullable=True)

    strict = sa.Column(sa.Boolean(), nullable=True, default=False)

    organic = sa.Column(sa.Boolean(), nullable=True, default=False)

    preferred_vendor_id = sa.Column('preferredVendorID', sa.Integer(), nullable=True, default=0)

    multi_vendor = sa.Column('multiVendor', sa.Boolean(), nullable=True, default=False)

    sort_retail = sa.Column('sortRetail', sa.String(length=255), nullable=True)

    sort_internal = sa.Column('sortInternal', sa.String(length=255), nullable=True)

    products = association_proxy(
        '_products', 'product',
        creator=lambda p: ProductLikeCode(product=p),
    )

    def __str__(self):
        return self.description or ""


class OriginCountry(Base):
    """
    Represents a country which relates to the "origin" for some product(s).
    """
    __tablename__ = 'originCountry'

    id = sa.Column('countryID', sa.Integer(), primary_key=True, autoincrement=True, nullable=False)

    name = sa.Column(sa.String(length=50), nullable=True)

    abbreviation = sa.Column('abbr', sa.String(length=5), nullable=True)

    def __str__(self):
        return self.name or self.abbreviation or ""


class OriginStateProv(Base):
    """
    Represents a state/province which relates to the "origin" for some product(s).
    """
    __tablename__ = 'originStateProv'

    id = sa.Column('stateProvID', sa.Integer(), primary_key=True, autoincrement=True, nullable=False)

    name = sa.Column(sa.String(length=50), nullable=True)

    abbreviation = sa.Column('abbr', sa.String(length=5), nullable=True)

    def __str__(self):
        return self.name or self.abbreviation or ""


class OriginCustomRegion(Base):
    """
    Represents a custom region which relates to the "origin" for some product(s).
    """
    __tablename__ = 'originCustomRegion'

    id = sa.Column('customID', sa.Integer(), primary_key=True, autoincrement=True, nullable=False)

    name = sa.Column(sa.String(length=50), nullable=True)

    def __str__(self):
        return self.name or ""


class Origin(Base):
    """
    Represents a location which is the "origin" for some product(s).
    """
    __tablename__ = 'origins'
    __table_args__ = (
        sa.ForeignKeyConstraint(['countryID'], ['originCountry.countryID']),
        sa.ForeignKeyConstraint(['stateProvID'], ['originStateProv.stateProvID']),
        sa.ForeignKeyConstraint(['customID'], ['originCustomRegion.customID']),
    )

    id = sa.Column('originID', sa.Integer(), primary_key=True, autoincrement=True, nullable=False)

    country_id = sa.Column('countryID', sa.Integer(), nullable=True)
    country = orm.relationship(OriginCountry)

    state_prov_id = sa.Column('stateProvID', sa.Integer(), nullable=True)
    state_prov = orm.relationship(OriginStateProv)

    custom_id = sa.Column('customID', sa.Integer(), nullable=True)
    custom_region = orm.relationship(OriginCustomRegion)

    local = sa.Column(sa.Boolean(), nullable=True, default=0)

    name = sa.Column(sa.String(length=100), nullable=True)

    short_name = sa.Column('shortName', sa.String(length=50), nullable=True)

    def __str__(self):
        return self.name or self.short_name or ""


class Product(Base):
    """
    Represents a product, purchased and/or sold by the organization.
    """
    __tablename__ = 'products'
    __table_args__ = (
        sa.ForeignKeyConstraint(['department'], ['departments.dept_no']),
        sa.ForeignKeyConstraint(['subdept'], ['subdepts.subdept_no']),
        sa.ForeignKeyConstraint(['tax'], ['taxrates.id']),
    )

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True, nullable=False)

    upc = sa.Column(sa.String(length=13), nullable=True)

    description = sa.Column(sa.String(length=30), nullable=True)

    brand = sa.Column(sa.String(length=30), nullable=True)

    formatted_name = sa.Column(sa.String(length=30), nullable=True)

    normal_price = sa.Column(sa.Float(), nullable=True)

    price_method = sa.Column('pricemethod', sa.SmallInteger(), nullable=True)

    group_price = sa.Column('groupprice', sa.Float(), nullable=True)

    quantity = sa.Column(sa.SmallInteger(), nullable=True)

    special_price = sa.Column(sa.Float(), nullable=True)

    special_price_method = sa.Column('specialpricemethod', sa.SmallInteger(), nullable=True)

    special_group_price = sa.Column('specialgroupprice', sa.Float(), nullable=True)

    special_quantity = sa.Column('specialquantity', sa.SmallInteger(), nullable=True)

    start_date = sa.Column(sa.DateTime(), nullable=True)

    end_date = sa.Column(sa.DateTime(), nullable=True)

    department_number = sa.Column('department', sa.SmallInteger(), nullable=True)
    department = orm.relationship(
        Department,
        primaryjoin=Department.number == department_number,
        foreign_keys=[department_number],
        doc="""
        Reference to the :class:`Department` to which the product belongs.
        """)

    size = sa.Column(sa.String(length=9), nullable=True)

    tax_rate_id = sa.Column('tax', sa.SmallInteger(), nullable=True)
    tax_rate = orm.relationship(TaxRate)

    foodstamp = sa.Column(sa.Boolean(), nullable=True)

    scale = sa.Column(sa.Boolean(), nullable=True)

    # TODO: yikes, did i just code this all wrong the first time?  pretty sure
    # this needs to change to a decimal column...
    scale_price = sa.Column('scaleprice', sa.Boolean(), nullable=True)
    # scale_price = sa.Column('scaleprice', sa.Numeric(precision=10, scale=2), nullable=True)

    mix_match_code = sa.Column('mixmatchcode', sa.String(length=13), nullable=True)

    created = sa.Column(StringableDateTime(), nullable=True)

    modified = sa.Column(sa.DateTime(), nullable=True)

    # advertised = sa.Column(sa.Boolean(), nullable=True)

    tare_weight = sa.Column('tareweight', sa.Float(), nullable=True)

    discount = sa.Column(sa.SmallInteger(), nullable=True)

    discount_type = sa.Column('discounttype', sa.SmallInteger(), nullable=True)

    line_item_discountable = sa.Column(sa.Boolean(), nullable=True)

    unit_of_measure = sa.Column('unitofmeasure', sa.String(length=15), nullable=True)

    wicable = sa.Column(sa.SmallInteger(), nullable=True)

    quantity_enforced = sa.Column('qttyEnforced', sa.Boolean(), nullable=True)

    id_enforced = sa.Column('idEnforced', sa.SmallInteger(), nullable=True)

    cost = sa.Column(sa.Float(), nullable=True)

    in_use = sa.Column('inUse', sa.Boolean(), nullable=True)

    flags = sa.Column('numflag', sa.Integer(), nullable=True)

    subdepartment_number = sa.Column('subdept', sa.SmallInteger(), nullable=True)
    subdepartment = orm.relationship(
        Subdepartment,
        primaryjoin=Subdepartment.number == subdepartment_number,
        foreign_keys=[subdepartment_number],
        doc="""
        Reference to the :class:`Subdepartment` to which the product belongs.
        """)

    deposit = sa.Column(sa.Float(), nullable=True)

    local = sa.Column(sa.Integer(), nullable=True)

    store_id = sa.Column(sa.SmallInteger(), nullable=True)

    default_vendor_id = sa.Column(sa.Integer(), nullable=True)
    default_vendor = orm.relationship(
        Vendor,
        primaryjoin=Vendor.id == default_vendor_id,
        foreign_keys=[default_vendor_id],
        doc="""
        Reference to the default :class:`Vendor` from which the product is obtained.
        """)
    # TODO: deprecate / remove this?
    vendor = orm.synonym('default_vendor')

    current_origin_id = sa.Column(sa.Integer(), nullable=True)

    # TODO: some older DB's might not have this?  guess we'll see
    last_sold = sa.Column(sa.DateTime(), nullable=True)

    like_code = association_proxy(
        '_like_code', 'like_code',
        creator=lambda lc: ProductLikeCode(like_code=lc),
    )

    @property
    def full_description(self):
        fields = ['brand', 'description', 'size']
        fields = [getattr(self, f) or '' for f in fields]
        fields = filter(bool, fields)
        return ' '.join(fields)

    @property
    def complete_size(self):
        """
        Returns the "complete" size string for the product.  This is based on
        the :attr:`size` and :attr:`unit_of_measure` attributes.
        """
        parts = [self.size, self.unit_of_measure]
        parts = [(part or '').strip()
                 for part in parts]
        parts = [part for part in parts if part]
        return " ".join(parts).strip()

    def __str__(self):
        return self.description or ''


class ProductLikeCode(Base):
    """
    Represents the association between a product and like code.
    """
    __tablename__ = 'upcLike'
    __table_args__ = (
        sa.ForeignKeyConstraint(['upc'], ['products.upc']),
        sa.ForeignKeyConstraint(['likeCode'], ['likeCodes.likeCode']),
    )

    upc = sa.Column(sa.String(length=13), primary_key=True, nullable=False)
    product = orm.relationship(
        Product,
        primaryjoin=Product.upc == orm.foreign(upc),
        doc="""
        Reference to the product to which this association applies.
        """,
        backref=orm.backref(
            '_like_code',
            uselist=False,
            doc="""
            Reference to the like code association for the product.
            """))

    like_code_id = sa.Column('likeCode', sa.Integer(), nullable=True)
    like_code = orm.relationship(
        LikeCode,
        doc="""
        Reference to the LikeCode to which this association applies.
        """,
        backref=orm.backref(
            '_products',
            doc="""
            List of product associations for this like code.
            """))


class ProductFlag(Base):
    """
    Represents a product flag attribute.
    """
    __tablename__ = 'prodFlags'

    bit_number = sa.Column(sa.SmallInteger(), primary_key=True, autoincrement=False, nullable=False, default=0)

    description = sa.Column(sa.String(length=50), nullable=True)

    active = sa.Column(sa.Boolean(), nullable=True, default=True)

    def __str__(self):
        return self.description or ''


class ProductUser(Base):
    """
    Represents extended "user" info for a product (e.g. sale signage).
    """
    __tablename__ = 'productUser'

    upc = sa.Column(sa.String(length=13), primary_key=True, nullable=False)
    product = orm.relationship(
        Product,
        primaryjoin=Product.upc == upc,
        foreign_keys=[upc],
        doc="""
        Reference to the :class:`Product` to which this record applies.
        """,
        backref=orm.backref(
            'user_info',
            uselist=False,
            cascade='all, delete-orphan',
            doc="""
            Reference to the :class:`ProductUser` record for this product, if any.
            """))

    description = sa.Column(sa.String(length=255), nullable=True)

    brand = sa.Column(sa.String(length=255), nullable=True)

    sizing = sa.Column(sa.String(length=255), nullable=True)

    photo = sa.Column(sa.String(length=255), nullable=True)

    # TODO: this was not in some older DBs
    # nutrition_facts = sa.Column('nutritionFacts', sa.String(length=255), nullable=True)

    long_text = sa.Column(sa.Text(), nullable=True)

    enable_online = sa.Column('enableOnline', sa.Boolean(), nullable=True)

    sold_out = sa.Column('soldOut', sa.Boolean(), nullable=True)

    # TODO: this was not in some older DBs
    # sign_count = sa.Column('signCount', sa.SmallInteger(), nullable=True, default=1)

    # TODO: this was not in some older DBs
    # narrow = sa.Column(sa.Boolean(), nullable=True, default=False)

    def __str__(self):
        return str(self.product or '')


class VendorItem(Base):
    """
    Represents a "source" for a given item, from a given vendor.
    """
    __tablename__ = 'vendorItems'
    __table_args__ = (
        sa.ForeignKeyConstraint(['vendorID'], ['vendors.vendorID']),
    )

    sku = sa.Column(sa.String(length=13), primary_key=True, nullable=False)

    vendor_id = sa.Column('vendorID', sa.Integer(), primary_key=True, nullable=False)
    vendor = orm.relationship(
        Vendor,
        doc="""
        Reference to the :class:`Vendor` from which the product is obtained.
        """)

    # TODO: this should be autoincrement, but not primary key??
    vendor_item_id = sa.Column('vendorItemID', sa.Integer(), nullable=False)

    upc = sa.Column(sa.String(length=13), nullable=False)
    product = orm.relationship(
        Product,
        primaryjoin=Product.upc == upc,
        foreign_keys=[upc],
        doc="""
        Reference to the :class:`Product` to which this record applies.
        """,
        backref=orm.backref(
            'vendor_items',
            order_by=vendor_item_id,
            doc="""
            List of :class:`VendorItem` records for this product.
            """))

    brand = sa.Column(sa.String(length=50), nullable=True)

    description = sa.Column(sa.String(length=50), nullable=True)

    size = sa.Column(sa.String(length=25), nullable=True)

    units = sa.Column(sa.Float(), nullable=True, default=1)

    cost = sa.Column(sa.Numeric(precision=10, scale=3), nullable=True)

    sale_cost = sa.Column('saleCost', sa.Numeric(precision=10, scale=3),
                          nullable=True, default=0)

    vendor_department_id = sa.Column('vendorDept', sa.Integer(), nullable=True,
                                     default=0)

    srp = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)

    modified = sa.Column(sa.DateTime(), nullable=True)

    def __str__(self):
        return "{} from {}".format(self.sku, self.vendor)


class ScaleItem(Base):
    """
    Represents deli scale info for a given item.
    """
    __tablename__ = 'scaleItems'

    plu = sa.Column(sa.String(length=13), primary_key=True, nullable=False)
    product = orm.relationship(
        Product,
        primaryjoin=Product.upc == plu,
        foreign_keys=[plu],
        doc="""
        Reference to the :class:`Product` to which this record applies.
        """,
        backref=orm.backref(
            'scale_item',
            uselist=False,
            doc="""
            Reference to the :class:`ScaleItem` record for this product.
            """))

    price = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)

    item_description = sa.Column('itemdesc', sa.String(length=100), nullable=True)

    exception_price = sa.Column('exceptionprice', sa.Numeric(precision=10, scale=2), nullable=True)

    weight = sa.Column(sa.SmallInteger(), nullable=True, default=0)

    by_count = sa.Column('bycount', sa.Boolean(), nullable=True, default=False)

    tare = sa.Column(sa.Float(), nullable=True, default=0)

    shelf_life = sa.Column('shelflife', sa.SmallInteger(), nullable=True, default=0)

    net_weight = sa.Column('netWeight', sa.SmallInteger(), nullable=True, default=0)

    text = sa.Column(sa.Text(), nullable=True)

    reporting_class = sa.Column('reportingClass', sa.String(length=6), nullable=True)

    label = sa.Column(sa.Integer(), nullable=True)

    graphics = sa.Column(sa.Integer(), nullable=True)

    modified = sa.Column(sa.DateTime(), nullable=True)

    # TODO: the following 3 columns are not in some older DBs; maybe need to
    # figure out a "simple" way to conditionally include them?

    linked_plu = sa.Column('linkedPLU', sa.String(length=13), nullable=True)

    mosa_statement = sa.Column('mosaStatement', sa.Boolean(), nullable=True, default=False)

    origin_text = sa.Column('originText', sa.String(length=100), nullable=True)

    def __str__(self):
        return str(self.product)


class FloorSection(Base):
    """
    Represents a physical "floor section" within a store.
    """
    __tablename__ = 'FloorSections'

    floorSectionID = sa.Column(sa.Integer(), primary_key=True, autoincrement=True, nullable=False)
    id = orm.synonym('floorSectionID')

    store_id = sa.Column('storeID', sa.Integer(), nullable=True, default=1)

    name = sa.Column(sa.String(length=50), nullable=True)

    # TODO: this was not in some older DBs
    # map_x = sa.Column('mapX', sa.Integer(), nullable=True, default=0)

    # TODO: this was not in some older DBs
    # map_y = sa.Column('mapY', sa.Integer(), nullable=True, default=0)

    # TODO: this was not in some older DBs
    # map_rotate = sa.Column('mapRotate', sa.Integer(), nullable=True, default=0)


class ProductPhysicalLocation(Base):
    """
    Represents a physical location for a product
    """
    __tablename__ = 'prodPhysicalLocation'
    __table_args__ = (
        sa.ForeignKeyConstraint(['floorSectionID'], ['FloorSections.floorSectionID']),
    )

    upc = sa.Column(sa.String(length=13), primary_key=True, nullable=False)
    product = orm.relationship(
        Product,
        primaryjoin=Product.upc == upc,
        foreign_keys=[upc],
        doc="""
        Reference to the :class:`Product` to which this record applies.
        """,
        backref=orm.backref(
            'physical_location',
            uselist=False,
            doc="""
            Reference to the :class:`ProductPhysicalLocation` record for this
            product.
            """))

    store_id = sa.Column(sa.SmallInteger(), nullable=True, default=0)

    floor_section_id = sa.Column('floorSectionID', sa.Integer(), nullable=True)
    floor_section = orm.relationship(
        FloorSection,
        doc="""
        Reference to the :class:`FloorSection` with which this location is
        associated.
        """)

    section = sa.Column(sa.SmallInteger(), nullable=True, default=0)

    subsection = sa.Column(sa.SmallInteger(), nullable=True, default=0)

    shelf_set = sa.Column(sa.SmallInteger(), nullable=True, default=0)

    shelf = sa.Column(sa.SmallInteger(), nullable=True, default=0)

    location = sa.Column(sa.SmallInteger(), nullable=True, default=0)


class Employee(Base):
    """
    Represents an employee within the organization.
    """
    __tablename__ = 'employees'

    number = sa.Column('emp_no', sa.SmallInteger(), primary_key=True, autoincrement=False, nullable=False)

    cashier_password = sa.Column('CashierPassword', sa.String(length=50), nullable=True)

    admin_password = sa.Column('AdminPassword', sa.String(length=50), nullable=True)

    first_name = sa.Column('FirstName', sa.String(length=255), nullable=True)

    last_name = sa.Column('LastName', sa.String(length=255), nullable=True)

    job_title = sa.Column('JobTitle', sa.String(length=255), nullable=True)

    active = sa.Column('EmpActive', sa.Boolean(), nullable=True)

    frontend_security = sa.Column('frontendsecurity', sa.SmallInteger(), nullable=True)

    backend_security = sa.Column('backendsecurity', sa.SmallInteger(), nullable=True)

    birth_date = sa.Column('birthdate', sa.DateTime(), nullable=True)

    def __str__(self):
        return ' '.join([self.first_name or '', self.last_name or '']).strip()


class MemberType(Base):
    """
    Represents a type of membership within the organization.
    """
    __tablename__ = 'memtype'

    id = sa.Column('memtype', sa.SmallInteger(), primary_key=True, nullable=False, default=0)

    description = sa.Column('memDesc', sa.String(length=20), nullable=True)

    customer_type = sa.Column('custdataType', sa.String(length=10), nullable=True)

    discount = sa.Column(sa.SmallInteger(), nullable=True)

    staff = sa.Column(sa.Boolean(), nullable=True)

    ssi = sa.Column(sa.Boolean(), nullable=True)

    # TODO: this was apparently added "recently" - isn't present in all DBs
    # (need to figure out how to conditionally include it in model?)
    # sales_code = sa.Column('salesCode', sa.Integer(), nullable=True)

    def __str__(self):
        return self.description or ""


class CustomerAccount(Base):
    """
    This represents the customer account itself, and not a "person" per se.

    https://github.com/CORE-POS/IS4C/blob/master/fannie/classlib2.0/data/models/op/CustomerAccountsModel.php
    """
    __tablename__ = 'CustomerAccounts'

    id = sa.Column('customerAccountID', sa.Integer(), primary_key=True, autoincrement=True, nullable=False)

    card_number = sa.Column('cardNo', sa.Integer(), nullable=True,
                            unique=True, index=True)

    member_status = sa.Column('memberStatus', sa.String(length=10), nullable=True,
                              default='PC')

    active_status = sa.Column('activeStatus', sa.String(length=10), nullable=True,
                              default='')

    customer_type_id = sa.Column('customerTypeID', sa.Integer(), nullable=True,
                                 default=1)
    customer_type = orm.relationship(
        MemberType,
        primaryjoin=MemberType.id == customer_type_id,
        foreign_keys=[customer_type_id],
        doc="""
        Reference to the :class:`MemberType` with which this account is associated.
        """)

    charge_balance = sa.Column('chargeBalance', sa.Numeric(precision=10, scale=2), nullable=True,
                               default=0)

    charge_limit = sa.Column('chargeLimit', sa.Numeric(precision=10, scale=2), nullable=True,
                             default=0)

    id_card_upc = sa.Column('idCardUPC', sa.String(length=13), nullable=True)

    start_date = sa.Column('startDate', sa.DateTime(), nullable=True)

    end_date = sa.Column('endDate', sa.DateTime(), nullable=True)

    address_first_line = sa.Column('addressFirstLine', sa.String(length=100), nullable=True)

    address_second_line = sa.Column('addressSecondLine', sa.String(length=100), nullable=True)

    city = sa.Column(sa.String(length=50), nullable=True)

    state = sa.Column(sa.String(length=10), nullable=True)

    zip = sa.Column(sa.String(length=10), nullable=True)

    contact_allowed = sa.Column('contactAllowed', sa.Boolean(), nullable=True,
                                default=True)

    contact_method = sa.Column('contactMethod', sa.String(length=10), nullable=True,
                               default='mail')

    modified = sa.Column(sa.DateTime(), nullable=True)

    def __str__(self):
        return "Account ID-{}".format(self.id)


class Customer(Base):
    """
    This really represents a "person" attached to a proper "customer account".

    https://github.com/CORE-POS/IS4C/blob/master/fannie/classlib2.0/data/models/op/CustomersModel.php
    """
    __tablename__ = 'Customers'

    id = sa.Column('customerID', sa.Integer(), primary_key=True, autoincrement=True, nullable=False)

    account_id = sa.Column('customerAccountID', sa.Integer(),
                           sa.ForeignKey('CustomerAccounts.customerAccountID'),
                           nullable=True)
    account = orm.relationship(CustomerAccount)

    card_number = sa.Column('cardNo', sa.Integer(), nullable=True)

    first_name = sa.Column('firstName', sa.String(length=50), nullable=True)

    last_name = sa.Column('lastName', sa.String(length=50), nullable=True)

    charge_allowed = sa.Column('chargeAllowed', sa.Boolean(), nullable=True,
                               default=True)

    checks_allowed = sa.Column('checksAllowed', sa.Boolean(), nullable=True,
                               default=True)

    discount = sa.Column(sa.Boolean(), nullable=True,
                         default=False)

    account_holder = sa.Column('accountHolder', sa.Boolean(), nullable=True,
                               default=False)

    staff = sa.Column(sa.Boolean(), nullable=True,
                      default=False)

    phone = sa.Column(sa.String(length=20), nullable=True)

    alternate_phone = sa.Column('altPhone', sa.String(length=20), nullable=True)

    email = sa.Column(sa.String(length=100), nullable=True)

    member_pricing_allowed = sa.Column('memberPricingAllowed', sa.Boolean(), nullable=True,
                                       default=False)

    member_coupons_allowed = sa.Column('memberCouponsAllowed', sa.Boolean(), nullable=True,
                                       default=False)

    low_income_benefits = sa.Column('lowIncomeBenefits', sa.Boolean(), nullable=True,
                                    default=False)

    modified = sa.Column(sa.DateTime(), nullable=True)

    def __str__(self):
        return "{} {}".format(self.first_name or '', self.last_name or '').strip()


class CustomerClassic(Base):
    """
    Represents a customer of the organization.

    https://github.com/CORE-POS/IS4C/blob/master/fannie/classlib2.0/data/models/op/CustdataModel.php
    """
    __tablename__ = 'custdata'
    __table_args__ = (
        sa.ForeignKeyConstraint(['memType'], ['memtype.memtype']),
    )

    id = sa.Column(sa.Integer(), primary_key=True, autoincrement=True, nullable=False)

    card_number = sa.Column('CardNo', sa.Integer(), nullable=True)

    person_number = sa.Column('personNum', sa.SmallInteger(), nullable=False, default=1)

    first_name = sa.Column('FirstName', sa.String(length=30), nullable=True)

    last_name = sa.Column('LastName', sa.String(length=30), nullable=True)

    cash_back = sa.Column('CashBack', sa.Numeric(precision=10, scale=2), nullable=False, default=60)

    balance = sa.Column('Balance', sa.Numeric(precision=10, scale=2), nullable=False, default=0)

    discount = sa.Column('Discount', sa.SmallInteger(), nullable=True)

    member_discount_limit = sa.Column('MemDiscountLimit', sa.Numeric(precision=10, scale=2), nullable=False, default=0)

    charge_limit = sa.Column('ChargeLimit', sa.Numeric(precision=10, scale=2), nullable=False, default=0)
    
    charge_ok = sa.Column('ChargeOk', sa.Boolean(), nullable=False, default=False)

    write_checks = sa.Column('WriteChecks', sa.Boolean(), nullable=False, default=True)

    store_coupons = sa.Column('StoreCoupons', sa.Boolean(), nullable=False, default=True)

    type = sa.Column('Type', sa.String(length=10), nullable=False, default='pc')

    member_type_id = sa.Column('memType', sa.SmallInteger(), nullable=True)
    member_type = orm.relationship(
        MemberType,
        primaryjoin=MemberType.id == member_type_id,
        foreign_keys=[member_type_id],
        doc="""
        Reference to the :class:`MemberType` to which this member belongs.
        """)

    staff = sa.Column(sa.Boolean(), nullable=False, default=False)

    ssi = sa.Column('SSI', sa.Boolean(), nullable=False, default=False)

    purchases = sa.Column('Purchases', sa.Numeric(precision=10, scale=2), nullable=False, default=0)

    number_of_checks = sa.Column('NumberOfChecks', sa.SmallInteger(), nullable=False, default=0)

    member_coupons = sa.Column('memCoupons', sa.Integer(), nullable=False, default=1)

    blue_line = sa.Column('blueLine', sa.String(length=50), nullable=True)

    shown = sa.Column('Shown', sa.Boolean(), nullable=False, default=True)

    last_change = sa.Column('LastChange', sa.DateTime(), nullable=False)

    member_info = orm.relationship(
        'MemberInfo',
        primaryjoin='MemberInfo.card_number == CustomerClassic.card_number',
        foreign_keys=[card_number],
        uselist=False,
        back_populates='customers',
        doc="""
        Reference to the :class:`MemberInfo` instance for this customer.
        """)

    def __str__(self):
        return "{} {}".format(self.first_name or '', self.last_name or '').strip()


# TODO: deprecate / remove this
CustData = CustomerClassic


class MemberInfo(Base):
    """
    Contact info regarding a member of the organization.
    """
    __tablename__ = 'meminfo'

    card_number = sa.Column('card_no', sa.Integer(), primary_key=True, autoincrement=False, nullable=False)

    last_name = sa.Column(sa.String(length=30), nullable=True)

    first_name = sa.Column(sa.String(length=30), nullable=True)

    other_last_name = sa.Column('othlast_name', sa.String(length=30), nullable=True)

    other_first_name = sa.Column('othfirst_name', sa.String(length=30), nullable=True)

    street = sa.Column(sa.String(length=255), nullable=True)

    city = sa.Column(sa.String(length=20), nullable=True)

    state = sa.Column(sa.String(length=2), nullable=True)

    zip = sa.Column(sa.String(length=10), nullable=True)

    phone = sa.Column(sa.String(length=30), nullable=True)

    email = sa.Column('email_1', sa.String(length=50), nullable=True)

    email2 = sa.Column('email_2', sa.String(length=50), nullable=True, doc="""
    NB. this is labeled "Alt. Phone" in CORE Office member view, and
    is named `altPhone` when dealing with CORE Office webservices API.
    """)

    ads_ok = sa.Column('ads_OK', sa.Boolean(), nullable=True, default=True)

    customers = orm.relationship(
        CustomerClassic,
        primaryjoin=CustomerClassic.card_number == card_number,
        order_by=CustomerClassic.person_number,
        foreign_keys=[CustomerClassic.card_number],
        back_populates='member_info',
        remote_side=CustomerClassic.card_number,
        doc="""
        List of :class:`CustomerClassic` instances which are associated with this member info.
        """)

    dates = orm.relationship(
        'MemberDate',
        primaryjoin='MemberDate.card_number == MemberInfo.card_number',
        foreign_keys='MemberDate.card_number',
        cascade='all, delete-orphan',
        doc="""
        List of date records for the member.
        """,
        backref=orm.backref(
            'member',
            doc="""
            Reference to the member to whom the date record applies.
            """))

    barcodes = orm.relationship(
        'MemberBarcode',
        primaryjoin='MemberBarcode.card_number == MemberInfo.card_number',
        foreign_keys='MemberBarcode.card_number',
        order_by='MemberBarcode.upc',
        # cascade='all, delete-orphan',
        doc="""
        List of extra barcode records for the member.
        """,
        backref=orm.backref(
            'member_info',
            doc="""
            Reference to the :class:`MemberInfo` record to which the barcode applies.
            """))

    notes = orm.relationship(
        'MemberNote',
        primaryjoin='MemberNote.card_number == MemberInfo.card_number',
        foreign_keys='MemberNote.card_number',
        order_by='MemberNote.timestamp',
        cascade='all, delete-orphan',
        doc="""
        List of note records for the member.
        """,
        backref=orm.backref(
            'member_info',
            doc="""
            Reference to the :class:`MemberInfo` record to which the note applies.
            """))

    suspension = orm.relationship(
        'Suspension',
        primaryjoin='Suspension.card_number == MemberInfo.card_number',
        foreign_keys='Suspension.card_number',
        uselist=False,
        doc="""
        Suspension record for the member, if applicable.
        """,
        backref=orm.backref(
            'member_info',
            doc="""
            Reference to the :class:`MemberInfo` record to which the suspension
            applies.
            """))

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name or '', self.last_name or '').strip()

    def __str__(self):
        name = self.full_name
        if name:
            return name
        return "Member Info #{}".format(self.card_number)

    def split_street(self):
        """
        Tries to split the :attr:`street` attribute into 2 separate lines, e.g.
        "street1" and "street2" style.  Always returns a 2-tuple even if the
        second line would be empty.
        """
        address = (self.street or '').strip()
        lines = address.split('\n')
        street1 = lines[0].strip() or None
        street2 = None
        if len(lines) > 1:
            street2 = lines[1].strip() or None
            if len(lines) > 2:
                log.warning("member #%s has %s address lines: %s",
                            self.card_number, len(lines), self)
        return (street1, street2)


class MemberDate(Base):
    """
    Join/exit dates for members
    """
    __tablename__ = 'memDates'

    card_number = sa.Column('card_no', sa.Integer(), primary_key=True, autoincrement=False, nullable=False)

    start_date = sa.Column(sa.DateTime(), nullable=True)

    end_date = sa.Column(sa.DateTime(), nullable=True)

    def __str__(self):
        return "{} thru {}".format(
            self.start_date.date() if self.start_date else "??",
            self.end_date.date() if self.end_date else "??")


class MemberContact(Base):
    """
    Contact preferences for members
    """
    __tablename__ = 'memContact'

    card_number = sa.Column('card_no', sa.Integer(), primary_key=True, autoincrement=False, nullable=False)

    preference = sa.Column('pref', sa.Integer(), nullable=True)

    member = orm.relationship(
        MemberInfo,
        primaryjoin=MemberInfo.card_number == card_number,
        foreign_keys=[MemberInfo.card_number],
        uselist=False,
        doc="""
        Reference to the member to whom the contact record applies.
        """,
        backref=orm.backref(
            'contact',
            uselist=False,
            doc="""
            Reference to contact preference record for the member.
            """))

    def __str__(self):
        return str(self.preference)


class MemberBarcode(Base):
    """
    Additional barcode for a member.
    """
    __tablename__ = 'memberCards'

    card_number = sa.Column('card_no', sa.Integer(), nullable=False,
                            primary_key=True, autoincrement=False)

    upc = sa.Column(sa.String(length=13), nullable=False, primary_key=True)

    def __str__(self):
        return self.upc or ""


class MemberNote(Base):
    """
    Additional notes for a member.
    """
    __tablename__ = 'memberNotes'

    id = sa.Column('memberNoteID', sa.Integer(), nullable=False, primary_key=True, autoincrement=True)

    card_number = sa.Column('cardno', sa.Integer(), nullable=True)

    note = sa.Column(sa.Text(), nullable=True)

    timestamp = sa.Column('stamp', sa.DateTime(), nullable=True)

    username = sa.Column(sa.String(length=50), nullable=True)

    def __str__(self):
        return self.note or ""


class CustomerNotification(Base):
    """
    Represents a customer notification for display at the lane.

    https://github.com/CORE-POS/IS4C/blob/master/fannie/classlib2.0/data/models/op/CustomerNotificationsModel.php
    """
    __tablename__ = 'CustomerNotifications'

    id = sa.Column('customerNotificationID', sa.Integer(), primary_key=True, autoincrement=True, nullable=False)
    card_number = sa.Column('cardNo', sa.Integer(), nullable=True)
    customer_id = sa.Column('customerID', sa.Integer(), nullable=True)
    source = sa.Column(sa.String(length=50), nullable=True)
    type = sa.Column(sa.String(length=50), nullable=True)
    message = sa.Column(sa.String(length=255), nullable=True)
    modifier_module = sa.Column('modifierModule', sa.String(length=50), nullable=True)

    def __str__(self):
        return self.message or ''


class ReasonCode(Base):
    """
    Reason codes for legacy account suspensions.
    """
    __tablename__ = 'reasoncodes'

    mask = sa.Column(sa.Integer(), nullable=False, primary_key=True, autoincrement=False)

    text_string = sa.Column('textStr', sa.String(length=100), nullable=True)

    def __str__(self):
        return "#{}: {}".format(self.mask, self.text_string)


class Suspension(Base):
    """
    Suspension status for legacy customer accounts.
    """
    __tablename__ = 'suspensions'
    __table_args__ = (
        sa.ForeignKeyConstraint(['reasoncode'], ['reasoncodes.mask']),
    )

    card_number = sa.Column('cardno', sa.Integer(), nullable=False, primary_key=True, autoincrement=False)

    type = sa.Column(sa.String(length=1), nullable=True)

    memtype1 = sa.Column(sa.Integer(), nullable=True)

    memtype2 = sa.Column(sa.String(length=6), nullable=True)

    suspension_date = sa.Column('suspDate', sa.DateTime(), nullable=True)

    reason = sa.Column(sa.Text(), nullable=True)

    mail_flag = sa.Column('mailflag', sa.Integer(), nullable=True)

    discount = sa.Column(sa.Integer(), nullable=True)

    charge_limit = sa.Column('chargelimit', sa.Numeric(precision=10, scale=2), nullable=True)

    reason_code = sa.Column('reasoncode', sa.Integer(), nullable=True)
    reason_object = orm.relationship(ReasonCode)

    def __str__(self):
        return "#{} on {}".format(self.card_number,
                                  self.suspension_date)


class HouseCoupon(Base):
    """
    Represents a "house" (store) coupon.
    """
    __tablename__ = 'houseCoupons'
    __table_args__ = (
        sa.ForeignKeyConstraint(['department'], ['departments.dept_no']),
    )

    coupon_id = sa.Column('coupID', sa.Integer(), primary_key=True, nullable=False)

    description = sa.Column(sa.String(length=30), nullable=True)

    start_date = sa.Column('startDate', sa.DateTime(), nullable=True)

    end_date = sa.Column('endDate', sa.DateTime(), nullable=True)

    limit = sa.Column(sa.SmallInteger(), nullable=True)

    member_only = sa.Column('memberOnly', sa.SmallInteger(), nullable=True)

    discount_type = sa.Column('discountType', sa.String(length=2), nullable=True)

    discount_value = sa.Column('discountValue', sa.Numeric(precision=10, scale=2), nullable=True)

    min_type = sa.Column('minType', sa.String(length=2), nullable=True)

    min_value = sa.Column('minValue', sa.Numeric(precision=10, scale=2), nullable=True)

    department_id = sa.Column('department', sa.Integer(), nullable=True)
    department = orm.relationship(Department)

    auto = sa.Column(sa.Boolean(), nullable=True, default=False)

    # TODO: this isn't yet supported in all production DBs
    # virtual_only = sa.Column('virtualOnly', sa.Boolean(), nullable=True, default=False)

    def __str__(self):
        return self.description or ''


class Tender(Base):
    """
    Represents a tender for payment at POS
    """
    __tablename__ = 'tenders'

    tender_id = sa.Column('TenderID', sa.Integer(), primary_key=True, nullable=False)

    tender_code = sa.Column('TenderCode', sa.String(length=2), nullable=True)
    tender_name = sa.Column('TenderName', sa.String(length=25), nullable=True)
    tender_type = sa.Column('TenderType', sa.String(length=2), nullable=True)
    change_message = sa.Column('ChangeMessage', sa.String(length=25), nullable=True)
    min_amount = sa.Column('MinAmount', sa.Numeric(precision=10, scale=2), nullable=True)
    max_amount = sa.Column('MaxAmount', sa.Numeric(precision=10, scale=2), nullable=True)
    max_refund = sa.Column('MaxRefund', sa.Numeric(precision=10, scale=2), nullable=True)
    tender_module = sa.Column('TenderModule', sa.String(length=50), nullable=True)
    sales_code = sa.Column('SalesCode', sa.Integer(), nullable=True)

    def __str__(self):
        return self.tender_name or ''


class BatchType(Base):
    """
    Represents the definition of a batch type.
    """
    __tablename__ = 'batchType'

    id = sa.Column('batchTypeID', sa.Integer(), primary_key=True, autoincrement=False, nullable=False)

    description = sa.Column('typeDesc', sa.String(length=50), nullable=True)

    discount_type = sa.Column('discType', sa.Integer(), nullable=True)

    dated_signs = sa.Column('datedSigns', sa.Boolean(), nullable=True, default=True)

    special_order_eligible = sa.Column('specialOrderEligible', sa.Boolean(), nullable=True, default=True)

    editor_ui = sa.Column('editorUI', sa.Boolean(), nullable=True, default=True)

    allow_single_store = sa.Column('allowSingleStore', sa.Boolean(), nullable=True, default=False)

    exit_inventory = sa.Column('exitInventory', sa.Boolean(), nullable=True, default=False)

    def __str__(self):
        return self.description or ""


class Batch(Base):
    """
    Represents a batch.
    """
    __tablename__ = 'batches'
    __table_args__ = (
        sa.ForeignKeyConstraint(['batchType'], ['batchType.batchTypeID']),
    )

    id = sa.Column('batchID', sa.Integer(), primary_key=True, autoincrement=True, nullable=False)

    start_date = sa.Column('startDate', sa.DateTime(), nullable=True)

    end_date = sa.Column('endDate', sa.DateTime(), nullable=True)

    name = sa.Column('batchName', sa.String(length=80), nullable=True)

    batch_type_id = sa.Column('batchType', sa.Integer(), nullable=True)
    batch_type = orm.relationship(BatchType)

    discount_type = sa.Column('discountType', sa.Integer(), nullable=True)

    priority = sa.Column(sa.Integer(), nullable=True)

    owner = sa.Column(sa.String(length=50), nullable=True)

    trans_limit = sa.Column('transLimit', sa.Boolean(), nullable=True, default=False)

    notes = sa.Column(sa.Text(), nullable=True)

    def __str__(self):
        return self.name or ""


class BatchItem(Base):
    """
    Represents a batch "list" item.
    """
    __tablename__ = 'batchList'
    __table_args__ = (
        sa.ForeignKeyConstraint(['batchID'], ['batches.batchID']),
    )

    id = sa.Column('listID', sa.Integer(), primary_key=True, autoincrement=True, nullable=False)

    batch_id = sa.Column('batchID', sa.Integer(), nullable=True)
    batch = orm.relationship(Batch, backref=orm.backref('items'))

    upc = sa.Column(sa.String(length=13), nullable=True)

    sale_price = sa.Column('salePrice', sa.Numeric(precision=9, scale=3), nullable=True)

    group_sale_price = sa.Column('groupSalePrice', sa.Numeric(precision=9, scale=3), nullable=True)

    active = sa.Column(sa.Boolean(), nullable=True)

    price_method = sa.Column('pricemethod', sa.Integer(), nullable=True, default=0)

    quantity = sa.Column(sa.Integer(), nullable=True, default=0)

    sign_multiplier = sa.Column('signMultiplier', sa.Boolean(), nullable=True, default=True)

    cost = sa.Column(sa.Numeric(precision=9, scale=3), nullable=True, default=0)

    def __str__(self):
        return self.upc or ""


class PurchaseOrder(Base):
    """
    Represents a purchase order.
    """
    __tablename__ = 'PurchaseOrder'
    # TODO: would be simpler to declare these, but is it safe?
    # __table_args__ = (
    #     sa.ForeignKeyConstraint(['vendorID'], ['vendors.vendorID']),
    #     sa.ForeignKeyConstraint(['storeID'], ['Stores.storeID']),
    # )

    orderID = sa.Column(sa.Integer(), nullable=False, primary_key=True, autoincrement=True)
    id = orm.synonym('orderID')

    vendor_id = sa.Column('vendorID', sa.Integer(), nullable=True)
    vendor = orm.relationship(
        Vendor,
        primaryjoin=Vendor.id == vendor_id,
        foreign_keys=[vendor_id])

    store_id = sa.Column('storeID', sa.Integer(), nullable=True)
    store = orm.relationship(
        Store,
        primaryjoin=Store.id == store_id,
        foreign_keys=[store_id])

    creation_date = sa.Column('creationDate', sa.DateTime(), nullable=True)

    placed = sa.Column(sa.Boolean(), nullable=True, default=False)

    placed_date = sa.Column('placedDate', sa.DateTime(), nullable=True)

    user_id = sa.Column('userID', sa.Integer(), nullable=True)

    vendor_order_id = sa.Column('vendorOrderID', sa.String(length=25), nullable=True)

    vendor_invoice_id = sa.Column('vendorInvoiceID', sa.String(length=25), nullable=True)

    standing_id = sa.Column('standingID', sa.Integer(), nullable=True)

    inventory_ignore = sa.Column('inventoryIgnore', sa.Boolean(), nullable=True, default=False)

    transfer_id = sa.Column('transferID', sa.Integer(), nullable=True)

    notes = association_proxy('notes', 'notes')

    def __str__(self):
        return "#{} for {}".format(self.id, self.vendor or "??")


class PurchaseOrderItem(Base):
    """
    Represents a line item in a purchase order.
    """
    __tablename__ = 'PurchaseOrderItems'
    __table_args__ = (
        sa.ForeignKeyConstraint(['orderID'], ['PurchaseOrder.orderID']),
    )

    order_id = sa.Column('orderID', sa.Integer(), nullable=False,
                         primary_key=True, autoincrement=False)
    order = orm.relationship(PurchaseOrder, backref=orm.backref('items'))

    sku = sa.Column(sa.String(length=13), nullable=False,
                    primary_key=True)

    quantity = sa.Column(sa.Numeric(precision=10, scale=2), nullable=True)

    unit_cost = sa.Column('unitCost', sa.Numeric(precision=10, scale=4), nullable=True)

    case_size = sa.Column('caseSize', sa.Float(), nullable=True)

    received_date = sa.Column('receivedDate', sa.DateTime(), nullable=True)

    received_quantity = sa.Column('receivedQty', sa.Float(), nullable=True)

    received_total_cost = sa.Column('receivedTotalCost', sa.Numeric(precision=10, scale=4), nullable=True)

    unit_size = sa.Column('unitSize', sa.String(length=25), nullable=True)

    brand = sa.Column(sa.String(length=50), nullable=True)

    description = sa.Column(sa.String(length=50), nullable=True)

    internal_upc = sa.Column('internalUPC', sa.String(length=13), nullable=True)

    sales_code = sa.Column('salesCode', sa.Integer(), nullable=True)

    is_special_order = sa.Column('isSpecialOrder', sa.Boolean(), nullable=True,
                                 default=False)

    # TODO: this probably is FK to e.g. User.id ?
    received_by = sa.Column('receivedBy', sa.Integer(), nullable=True,
                            default=0)

    def __str__(self):
        return self.description or ""


class PurchaseOrderNote(Base):
    """
    Represents a note attached to a purchase order.
    """
    __tablename__ = 'PurchaseOrderNotes'
    __table_args__ = (
        sa.ForeignKeyConstraint(['orderID'], ['PurchaseOrder.orderID']),
    )

    order_id = sa.Column('orderID', sa.Integer(), nullable=False,
                         primary_key=True, autoincrement=False)
    order = orm.relationship(PurchaseOrder, backref=orm.backref('notes'))

    notes = sa.Column(sa.Text(), nullable=True)

    def __str__(self):
        return self.notes or ""
