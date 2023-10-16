# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2019 Lance Edgar
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
Web Database Sessions

As with ``tailbone.db.Session``, the idea here is that we want to tie our
database sessions to the effective web "transaction" so that they are
auto-committed and -closed when the request has finished processing.
"""

from sqlalchemy.orm import sessionmaker, scoped_session
from zope.sqlalchemy import register


CoreOfficeSession = scoped_session(sessionmaker())
register(CoreOfficeSession)

CoreTransSession = scoped_session(sessionmaker())
register(CoreTransSession)

CoreTransArchiveSession = scoped_session(sessionmaker())
register(CoreTransArchiveSession)

# empty dict for now, this may be populated on app startup
ExtraCoreOfficeSessions = {}

# empty dict for now, this may be populated on app startup
ExtraCoreTransSessions = {}

# empty dict for now, this may be populated on app startup
ExtraCoreTransArchiveSessions = {}
