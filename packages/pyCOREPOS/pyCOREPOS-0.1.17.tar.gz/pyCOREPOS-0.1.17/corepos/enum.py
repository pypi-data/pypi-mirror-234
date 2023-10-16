# -*- coding: utf-8; -*-
################################################################################
#
#  pyCOREPOS -- Python Interface to CORE POS
#  Copyright © 2018-2019 Lance Edgar
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
CORE POS enumeration constants
"""

from __future__ import unicode_literals, absolute_import

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


BATCH_DISCOUNT_TYPE_PRICE_CHANGE        = 0
BATCH_DISCOUNT_TYPE_SALE_EVERYONE       = 1
BATCH_DISCOUNT_TYPE_SALE_RESTRICTED     = 2

BATCH_DISCOUNT_TYPE = OrderedDict([
    (BATCH_DISCOUNT_TYPE_PRICE_CHANGE,          "Price Change"),
    (BATCH_DISCOUNT_TYPE_SALE_EVERYONE,         "Sale for everyone"),
    (BATCH_DISCOUNT_TYPE_SALE_RESTRICTED,       "Member/Owner only sale"),
])


HOUSE_COUPON_MEMBER_ONLY_NO     = 0
HOUSE_COUPON_MEMBER_ONLY_YES    = 1
HOUSE_COUPON_MEMBER_ONLY_PLUS   = 2

HOUSE_COUPON_MEMBER_ONLY = OrderedDict([
    (HOUSE_COUPON_MEMBER_ONLY_NO,       "No"),
    (HOUSE_COUPON_MEMBER_ONLY_YES,      "Yes"),
    (HOUSE_COUPON_MEMBER_ONLY_PLUS,     "Plus"),
])


HOUSE_COUPON_DISCOUNT_TYPE_QUANTITY     = 'Q'

HOUSE_COUPON_DISCOUNT_TYPE = OrderedDict([
    (HOUSE_COUPON_DISCOUNT_TYPE_QUANTITY,       "Quantity Discount"),
])


HOUSE_COUPON_MINIMUM_TYPE_TOTAL_AT_LEAST                = '$'
HOUSE_COUPON_MINIMUM_TYPE_TOTAL_MORE_THAN               = '$+'
HOUSE_COUPON_MINIMUM_TYPE_MIXED_DEPT_ITEM               = 'MX'
HOUSE_COUPON_MINIMUM_TYPE_MIXED_ITEM_ITEM               = 'M'
HOUSE_COUPON_MINIMUM_TYPE_DEPT_SALES_MORE_THAN          = 'D+'
HOUSE_COUPON_MINIMUM_TYPE_DEPT_SALES_AT_LEAST           = 'D'
HOUSE_COUPON_MINIMUM_TYPE_DEPT_NO_SALES_MORE_THAN       = 'C^'
HOUSE_COUPON_MINIMUM_TYPE_DEPT_NO_SALES_AT_LEAST        = 'C!'
HOUSE_COUPON_MINIMUM_TYPE_DEPT_QTY_MORE_THAN            = 'C+'
HOUSE_COUPON_MINIMUM_TYPE_DEPT_QTY_AT_LEAST             = 'C'
HOUSE_COUPON_MINIMUM_TYPE_QTY_PER_ITEM_MAX              = 'Q-'
HOUSE_COUPON_MINIMUM_TYPE_QTY_MORE_THAN                 = 'Q+'
HOUSE_COUPON_MINIMUM_TYPE_QTY_AT_LEAST                  = 'Q'

HOUSE_COUPON_MINIMUM_TYPE = OrderedDict([
    (HOUSE_COUPON_MINIMUM_TYPE_TOTAL_AT_LEAST,          "Total (at least $)"),
    (HOUSE_COUPON_MINIMUM_TYPE_TOTAL_MORE_THAN,         "Total (more than $)"),
    (HOUSE_COUPON_MINIMUM_TYPE_MIXED_DEPT_ITEM,         "Mixed (Department+Item)"),
    (HOUSE_COUPON_MINIMUM_TYPE_MIXED_ITEM_ITEM,         "Mixed (Item+Item)"),
    (HOUSE_COUPON_MINIMUM_TYPE_DEPT_SALES_MORE_THAN,    "Department (more than $)"),
    (HOUSE_COUPON_MINIMUM_TYPE_DEPT_SALES_AT_LEAST,     "Department (at least $)"),
    (HOUSE_COUPON_MINIMUM_TYPE_DEPT_NO_SALES_MORE_THAN, "Dept w/o sales (more than qty)"),
    (HOUSE_COUPON_MINIMUM_TYPE_DEPT_NO_SALES_AT_LEAST,  "Dept w/o sales (at least qty)"),
    (HOUSE_COUPON_MINIMUM_TYPE_DEPT_QTY_MORE_THAN,      "Department (more than qty)"),
    (HOUSE_COUPON_MINIMUM_TYPE_DEPT_QTY_AT_LEAST,       "Department (at least qty)"),
    (HOUSE_COUPON_MINIMUM_TYPE_QTY_PER_ITEM_MAX,        "Quantity (Per-Item Max)"),
    (HOUSE_COUPON_MINIMUM_TYPE_QTY_MORE_THAN,           "Quantity (more than)"),
    (HOUSE_COUPON_MINIMUM_TYPE_QTY_AT_LEAST,            "Quantity (at least)"),
])


MEMBER_CONTACT_PREFERENCE_NO_CONTACT                    = 0
MEMBER_CONTACT_PREFERENCE_POSTAL_MAIL_ONLY              = 1
MEMBER_CONTACT_PREFERENCE_EMAIL_ONLY                    = 2
MEMBER_CONTACT_PREFERENCE_BOTH                          = 3

MEMBER_CONTACT_PREFERENCE = OrderedDict([
    (MEMBER_CONTACT_PREFERENCE_NO_CONTACT,              "no contact"),
    (MEMBER_CONTACT_PREFERENCE_POSTAL_MAIL_ONLY,        "postal mail only"),
    (MEMBER_CONTACT_PREFERENCE_EMAIL_ONLY,              "email only"),
    (MEMBER_CONTACT_PREFERENCE_BOTH,                    "both (postal mail and email)"),
])


PRODUCT_PRICE_METHOD_DISABLED           = 0
PRODUCT_PRICE_METHOD_ALWAYS             = 1
PRODUCT_PRICE_METHOD_FULL_SETS          = 2

PRODUCT_PRICE_METHOD = OrderedDict([
    (PRODUCT_PRICE_METHOD_DISABLED,     "Disabled"),
    (PRODUCT_PRICE_METHOD_ALWAYS,       "Always use this price"),
    (PRODUCT_PRICE_METHOD_FULL_SETS,    "Use this price for full sets"),
])
