#  Fipper - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Fipper.
#
#  Fipper is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Fipper is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Fipper.  If not, see <http://www.gnu.org/licenses/>.

from .advanced import Advanced
from .auth import Auth
from .ayiin import Ayiin
from .bots import Bots
from .calls import Calls
from .chats import Chats
from .contacts import Contacts
from .decorators import Decorators
from .invite_links import InviteLinks
from .messages import Messages
from .mongo import Mongo
from .password import Password
from .users import Users
from .utilities import Utilities


class Methods(
    Advanced,
    Auth,
    Ayiin,
    Bots,
    Calls,
    Contacts,
    Chats,
    Decorators,
    InviteLinks,
    Messages,
    Mongo,
    Password,
    Users,
    Utilities,
):
    pass
