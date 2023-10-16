# -*- coding: utf-8; -*-
################################################################################
#
#  pyCOREPOS -- Python Interface to CORE POS
#  Copyright © 2018-2020 Lance Edgar
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
CORE POS Database Utilities
"""

import sqlalchemy as sa

from corepos.db.office_op import model as corepos


def get_last_card_number(session):
    """
    Convenience function, to return the "last" (max) value for the
    ``custdata.CardNo`` field, for use when generating new values.
    """
    return session.query(sa.func.max(corepos.Customer.card_number))\
                  .scalar() or 0


def table_exists(session, model_class):
    """
    Determine if a table exists in the database.

    :param session: SQLAlchemy session object, opened against the database in
       question.

    :param model_class: The model class associated with the table in question.

    :returns: Boolean indicating if the table exists.
    """
    try:
        session.query(model_class).count()
    except sa.exc.ProgrammingError as error:
        if "doesn't exist" in str(error):
            return False
        else:
            raise
    else:
        return True
