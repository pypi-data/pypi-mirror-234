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
Data model for CORE POS "lane_op" DB
"""

import sqlalchemy as sa
from sqlalchemy import orm


Base = orm.declarative_base()


class Department(Base):
    """
    Represents a department within the organization.
    """
    __tablename__ = 'departments'

    number = sa.Column('dept_no', sa.SmallInteger(), nullable=False,
                       primary_key=True, autoincrement=False)

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

    line_item_discount = sa.Column(sa.Boolean(), nullable=True)

    wicable = sa.Column('dept_wicable', sa.Boolean(), nullable=True)

    def __str__(self):
        return self.name or ""


class Product(Base):
    """
    Represents a product, purchased and/or sold by the organization.
    """
    __tablename__ = 'products'
    # __table_args__ = (
    #     sa.ForeignKeyConstraint(['department'], ['departments.dept_no']),
    #     sa.ForeignKeyConstraint(['subdept'], ['subdepts.subdept_no']),
    #     sa.ForeignKeyConstraint(['tax'], ['taxrates.id']),
    # )

    id = sa.Column(sa.Integer(), nullable=False, 
                   primary_key=True, autoincrement=True)

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

    special_limit = sa.Column(sa.SmallInteger(), nullable=True)

    start_date = sa.Column(sa.DateTime(), nullable=True)

    end_date = sa.Column(sa.DateTime(), nullable=True)

    department_number = sa.Column('department', sa.SmallInteger(), nullable=True)
    # department = orm.relationship(
    #     Department,
    #     primaryjoin=Department.number == department_number,
    #     foreign_keys=[department_number],
    #     doc="""
    #     Reference to the :class:`Department` to which the product belongs.
    #     """)

    size = sa.Column(sa.String(length=9), nullable=True)

    tax_rate_id = sa.Column('tax', sa.SmallInteger(), nullable=True)
    # tax_rate = orm.relationship(TaxRate)

    foodstamp = sa.Column(sa.Boolean(), nullable=True)

    scale = sa.Column(sa.Boolean(), nullable=True)

    scale_price = sa.Column('scaleprice', sa.Float(), nullable=True)

    mix_match_code = sa.Column('mixmatchcode', sa.String(length=13), nullable=True)

    created = sa.Column(sa.DateTime(), nullable=True)

    modified = sa.Column(sa.DateTime(), nullable=True)

    # TODO: what to do about this 'replaces' thing?
    # 'batchID'=>array('type'=>'TINYINT', 'replaces'=>'advertised'),
    # batch_id = sa.Column('batchID', sa.SmallInteger(), nullable=True)
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

    special_cost = sa.Column(sa.Float(), nullable=True)

    received_cost = sa.Column(sa.Float(), nullable=True)

    in_use = sa.Column('inUse', sa.Boolean(), nullable=True)

    flags = sa.Column('numflag', sa.Integer(), nullable=True)

    subdepartment_number = sa.Column('subdept', sa.SmallInteger(), nullable=True)
    # subdepartment = orm.relationship(
    #     Subdepartment,
    #     primaryjoin=Subdepartment.number == subdepartment_number,
    #     foreign_keys=[subdepartment_number],
    #     doc="""
    #     Reference to the :class:`Subdepartment` to which the product belongs.
    #     """)

    deposit = sa.Column(sa.Float(), nullable=True)

    local = sa.Column(sa.Integer(), nullable=True,
                      default=0) # TODO: do we want a default here?

    store_id = sa.Column(sa.SmallInteger(), nullable=True)

    default_vendor_id = sa.Column(sa.Integer(), nullable=True)
    # default_vendor = orm.relationship(
    #     Vendor,
    #     primaryjoin=Vendor.id == default_vendor_id,
    #     foreign_keys=[default_vendor_id],
    #     doc="""
    #     Reference to the default :class:`Vendor` from which the product is obtained.
    #     """)

    current_origin_id = sa.Column(sa.Integer(), nullable=True)

    auto_par = sa.Column(sa.Float(), nullable=True,
                         default=0) # TODO: do we want a default here?

    price_rule_id = sa.Column(sa.Integer(), nullable=True)

    # TODO: some older DB's might not have this?  guess we'll see
    last_sold = sa.Column(sa.DateTime(), nullable=True)


class CustomerClassic(Base):
    """
    Represents a customer of the organization.

    https://github.com/CORE-POS/IS4C/blob/master/pos/is4c-nf/lib/models/op/CustdataModel.php
    """
    __tablename__ = 'custdata'
    # __table_args__ = (
    #     sa.ForeignKeyConstraint(['memType'], ['memtype.memtype']),
    # )

    id = sa.Column(sa.Integer(), nullable=False, primary_key=True, autoincrement=True)

    card_number = sa.Column('CardNo', sa.Integer(), nullable=True)

    person_number = sa.Column('personNum', sa.SmallInteger(), nullable=True)

    first_name = sa.Column('FirstName', sa.String(length=30), nullable=True)

    last_name = sa.Column('LastName', sa.String(length=30), nullable=True)

    cash_back = sa.Column('CashBack', sa.Numeric(precision=10, scale=2), nullable=True)

    balance = sa.Column('Balance', sa.Numeric(precision=10, scale=2), nullable=True)

    discount = sa.Column('Discount', sa.SmallInteger(), nullable=True)

    member_discount_limit = sa.Column('MemDiscountLimit', sa.Numeric(precision=10, scale=2), nullable=True)

    charge_limit = sa.Column('ChargeLimit', sa.Numeric(precision=10, scale=2), nullable=True)
    
    charge_ok = sa.Column('ChargeOk', sa.Boolean(), nullable=True, default=True)

    write_checks = sa.Column('WriteChecks', sa.Boolean(), nullable=True, default=True)

    store_coupons = sa.Column('StoreCoupons', sa.Boolean(), nullable=True, default=True)

    type = sa.Column('Type', sa.String(length=10), nullable=True, default='PC')

    member_type_id = sa.Column('memType', sa.SmallInteger(), nullable=True)
    # member_type = orm.relationship(
    #     MemberType,
    #     primaryjoin=MemberType.id == member_type_id,
    #     foreign_keys=[member_type_id],
    #     doc="""
    #     Reference to the :class:`MemberType` to which this member belongs.
    #     """)

    staff = sa.Column(sa.Boolean(), nullable=True, default=False)

    ssi = sa.Column('SSI', sa.Boolean(), nullable=True, default=False)

    purchases = sa.Column('Purchases', sa.Numeric(precision=10, scale=2), nullable=True, default=0)

    number_of_checks = sa.Column('NumberOfChecks', sa.SmallInteger(), nullable=True, default=0)

    member_coupons = sa.Column('memCoupons', sa.Integer(), nullable=True, default=1)

    blue_line = sa.Column('blueLine', sa.String(length=50), nullable=True)

    shown = sa.Column('Shown', sa.Boolean(), nullable=True, default=True)

    last_change = sa.Column('LastChange', sa.DateTime(), nullable=True)

    def __str__(self):
        return "{} {}".format(self.first_name or '', self.last_name or '').strip()


# TODO: deprecate / remove this
CustData = CustomerClassic
