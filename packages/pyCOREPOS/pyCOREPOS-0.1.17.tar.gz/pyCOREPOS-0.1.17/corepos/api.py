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
CORE-POS webservices API
"""

import json
import logging

import requests
from requests.auth import HTTPDigestAuth


log = logging.getLogger(__name__)


class CoreAPIError(Exception):
    """
    Base class for errors coming from the CORE API proper.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "CORE API returned an error: {}".format(self.message)


class CoreWebAPI(object):
    """
    Client implementation for the CORE webservices API.

    :param str url: URL to the CORE webservices API,
       e.g. ``'http://localhost/fannie/ws/'``

    :param bool verify: How to handle certificate validation for HTTPS
       URLs.  This value is passed as-is to the ``requests`` library,
       so see those docs for more info.  The default value for this is
       ``True`` because the assumption is that security should be on
       by default.  Set it to ``False`` in order to disable validation
       entirely, e.g. for self-signed certs.  (This may also be needed
       for basic HTTP URLs?)  Other values may be possible also; again
       see the ``requests`` docs for more info.

    :param htdigest_username: Username for htdigest authentication, if
       applicable.

    :param htdigest_password: Password for htdigest authentication, if
       applicable.
    """

    def __init__(
            self,
            url,
            verify=True,
            htdigest_username=None,
            htdigest_password=None,
    ):
        self.url = url
        self.verify = verify

        self.session = requests.Session()

        if htdigest_username and htdigest_password:
            self.session.auth = HTTPDigestAuth(htdigest_username,
                                               htdigest_password)

    def post(self, params, method=None):
        """
        Issue a POST request to the API, with the given ``params``.  If not
        specified, ``method`` will be CORE's ``FannieEntity`` webservice.
        """
        if not method:
            method = 'FannieEntity'
        if '\\' not in method:
            method = r'\COREPOS\Fannie\API\webservices\{}'.format(method)

        payload = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params,
            # we're not dealing with async here, so KISS for this 'id'
            # https://stackoverflow.com/questions/4390369/json-rpc-how-can-one-make-a-unique-id#comment4786119_4391070
            'id': 1,
        }

        response = self.session.post(self.url, data=json.dumps(payload),
                                     verify=self.verify)
        response.raise_for_status()
        return response

    def parse_response(self, response, method=None):
        """
        Generic method to "parse" a response from the API.  Really this just
        converts the JSON to a dict (etc.), and then checks for error.  If an
        error is found in the response, it will be raised here.
        """
        try:
            js = response.json()
        except:
            raise CoreAPIError("Received invalid response: {}".format(response.content))

        if 'error' in js:
            raise CoreAPIError(js['error'])

        # note, the result data format may depend on the API method involved
        if method == 'FannieMember':
            return js['result']

        # assuming typical FannieEntity result here
        assert set(js.keys()) == set(['jsonrpc', 'id', 'result'])
        assert set(js['result'].keys()) == set(['result'])
        return js['result']['result']

    def get_member_types(self):
        """
        Fetch all Member Type records from CORE.

        :returns: A (potentially empty) list of member type dict records.
        """
        params = {
            'entity': 'Memtype',
            'submethod': 'get',
            'columns': {},
        }

        response = self.post(params)
        result = self.parse_response(response)
        return [json.loads(rec) for rec in result]

    def get_members(self):
        """
        Fetch all Member records from CORE.

        :returns: A (potentially empty) list of member dict records.
        """
        params = {
            'method': 'get',
            'cardNo': None,
        }
        response = self.post(params, method='FannieMember')
        result = self.parse_response(response, method='FannieMember')
        return result

    def get_member(self, cardNo):
        """
        Fetch an existing Member record from CORE.

        :returns: Either a member dict record, or ``None``.
        """
        params = {
            'cardNo': cardNo,
            'method': 'get',
        }
        response = self.post(params, method='FannieMember')
        result = self.parse_response(response, method='FannieMember')
        if result:
            return result

    def set_member(self, cardNo, **kwargs):
        """
        Update an existing Member record in CORE.

        :returns: Boolean indicating success of the operation.

        .. warning::
           Only simple updates have been attempted thus far; have yet to try
           creation or deletion.  Neither of those should be expected to work.
        """
        kwargs['cardNo'] = cardNo
        params = {
            'cardNo': cardNo,
            'method': 'set',
            'member': kwargs,
        }
        response = self.post(params, method='FannieMember')
        result = self.parse_response(response, method='FannieMember')
        if result:
            return result

    def get_stores(self, **columns):
        """
        Fetch some or all of Store records from CORE.

        :returns: A (potentially empty) list of store dict records.

        To fetch all stores::

           api.get_stores()

        To fetch only stores named "Headquarters"::

           api.get_stores(description='Headquarters')
        """
        params = {
            'entity': 'Stores',
            'submethod': 'get',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        return [json.loads(rec) for rec in result]

    def get_departments(self, **columns):
        """
        Fetch some or all of Department records from CORE.

        :returns: A (potentially empty) list of department dict records.

        To fetch all departments::

           api.get_departments()

        To fetch only departments named "Grocery"::

           api.get_departments(dept_name='Grocery')
        """
        params = {
            'entity': 'Departments',
            'submethod': 'get',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        return [json.loads(rec) for rec in result]

    def get_department(self, dept_no, **columns):
        """
        Fetch an existing Department record from CORE.

        :returns: Either a department dict record, or ``None``.
        """
        columns['dept_no'] = dept_no
        params = {
            'entity': 'Departments',
            'submethod': 'get',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        if result:
            if len(result) > 1:
                log.warning("CORE API returned %s department results", len(result))
            return json.loads(result[0])

    def set_department(self, dept_no, **columns):
        """
        Update an existing Department record in CORE.

        :returns: Boolean indicating success of the operation.

        .. note::
           Currently this is being used to create a *new* department also.  CORE's
           ``departments`` table does not use auto-increment for its PK, which
           means we must provide one even when creating; therefore this method
           may be used for that.
        """
        columns['dept_no'] = dept_no
        params = {
            'entity': 'Departments',
            'submethod': 'set',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        return json.loads(result)

    def get_subdepartments(self, **columns):
        """
        Fetch some or all of Subdepartment records from CORE.

        :returns: A (potentially empty) list of subdepartment dict records.

        To fetch all subdepartments::

           api.get_subdepartments()

        To fetch only subdepartments named "Grocery"::

           api.get_subdepartments(subdept_name='Grocery')
        """
        params = {
            'entity': 'SubDepts',
            'submethod': 'get',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        return [json.loads(rec) for rec in result]

    def get_subdepartment(self, subdept_no, **columns):
        """
        Fetch an existing Subdepartment record from CORE.

        :returns: Either a subdepartment dict record, or ``None``.
        """
        columns['subdept_no'] = subdept_no
        params = {
            'entity': 'SubDepts',
            'submethod': 'get',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        if result:
            if len(result) > 1:
                log.warning("CORE API returned %s subdepartment results", len(result))
            return json.loads(result[0])

    def set_subdepartment(self, subdept_no, **columns):
        """
        Update an existing Subdepartment record in CORE.

        :returns: Boolean indicating success of the operation.

        .. note::
           Currently this is being used to create a *new* subdepartment also.  CORE's
           ``subdepartments`` table does not use auto-increment for its PK, which
           means we must provide one even when creating; therefore this method
           may be used for that.
        """
        columns['subdept_no'] = subdept_no
        params = {
            'entity': 'SubDepts',
            'submethod': 'set',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        return json.loads(result)

    def get_vendors(self, **columns):
        """
        Fetch some or all of Vendor records from CORE.

        :returns: A (potentially empty) list of vendor dict records.

        To fetch all vendors::

           api.get_vendors()

        To fetch only vendors named "UNFI"::

           api.get_vendors(vendorName='UNFI')
        """
        params = {
            'entity': 'Vendors',
            'submethod': 'get',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        return [json.loads(rec) for rec in result]

    def get_vendor(self, vendorID, **columns):
        """
        Fetch an existing Vendor record from CORE.

        :returns: Either a vendor dict record, or ``None``.
        """
        columns['vendorID'] = vendorID
        params = {
            'entity': 'Vendors',
            'submethod': 'get',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        if result:
            if len(result) > 1:
                log.warning("CORE API returned %s vendor results", len(result))
            return json.loads(result[0])

    def set_vendor(self, vendorID, **columns):
        """
        Update an existing Vendor record in CORE.

        :returns: Boolean indicating success of the operation.

        .. note::
           Currently this is being used to create a *new* vendor also.  CORE's
           ``vendors`` table does not use auto-increment for its PK, which
           means we must provide one even when creating; therefore this method
           may be used for that.
        """
        columns['vendorID'] = vendorID
        params = {
            'entity': 'Vendors',
            'submethod': 'set',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        return json.loads(result)

    def get_products(self, **columns):
        """
        Fetch some or all of Product records from CORE.

        :returns: A (potentially empty) list of product dict records.

        To fetch all products::

           api.get_products()

        To fetch only products with brand name "Braggs"::

           api.get_products(brand='Braggs')
        """
        params = {
            'entity': 'Products',
            'submethod': 'get',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        return [json.loads(rec) for rec in result]

    def get_product(self, upc, **columns):
        """
        Fetch an existing Product record from CORE.

        :returns: Either a product dict record, or ``None``.
        """
        columns['upc'] = upc
        params = {
            'entity': 'Products',
            'submethod': 'get',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        if result:
            if len(result) > 1:
                log.warning("CORE API returned %s product results", len(result))
            return json.loads(result[0])

    def set_product(self, upc, **columns):
        """
        Update an existing Product record in CORE.

        :returns: Boolean indicating success of the operation.

        .. note::
           Currently this is being used to create a *new* product also.  CORE's
           ``products`` table does not use auto-increment for its PK, which
           means we must provide one even when creating; therefore this method
           may be used for that.
        """
        columns['upc'] = upc
        params = {
            'entity': 'Products',
            'submethod': 'set',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        return json.loads(result)

    def get_vendor_items(self, **columns):
        """
        Fetch some or all of VendorItem records from CORE.

        :returns: A (potentially empty) list of vendor item dict records.

        To fetch all vendor items::

           api.get_vendor_items()

        To fetch only products with brand name "Braggs"::

           api.get_vendor_items(brand='Braggs')
        """
        params = {
            'entity': 'VendorItems',
            'submethod': 'get',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        return [json.loads(rec) for rec in result]

    def get_vendor_item(self, sku, vendorID, **columns):
        """
        Fetch an existing VendorItem record from CORE.

        :returns: Either a vendor item dict record, or ``None``.
        """
        columns['sku'] = sku
        columns['vendorID'] = vendorID
        params = {
            'entity': 'VendorItems',
            'submethod': 'get',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        if result:
            if len(result) > 1:
                log.warning("CORE API returned %s VendorItem results", len(result))
            return json.loads(result[0])

    def set_vendor_item(self, sku, vendorID, **columns):
        """
        Update an existing VendorItem record in CORE.

        :returns: Boolean indicating success of the operation.

        .. note::
           Currently this is being used to create a *new* product also.  CORE's
           ``vendorItems`` table does not use auto-increment for its PK, which
           means we must provide one even when creating; therefore this method
           may be used for that.
        """
        columns['sku'] = sku
        columns['vendorID'] = vendorID
        params = {
            'entity': 'VendorItems',
            'submethod': 'set',
            'columns': columns,
        }
        response = self.post(params)
        result = self.parse_response(response)
        return json.loads(result)
