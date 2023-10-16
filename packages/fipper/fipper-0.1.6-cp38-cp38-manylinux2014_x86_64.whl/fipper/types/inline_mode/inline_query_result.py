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

from uuid import uuid4

import fipper
from fipper import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~fipper.types.InlineQueryResultCachedAudio`
    - :obj:`~fipper.types.InlineQueryResultCachedDocument`
    - :obj:`~fipper.types.InlineQueryResultCachedAnimation`
    - :obj:`~fipper.types.InlineQueryResultCachedPhoto`
    - :obj:`~fipper.types.InlineQueryResultCachedSticker`
    - :obj:`~fipper.types.InlineQueryResultCachedVideo`
    - :obj:`~fipper.types.InlineQueryResultCachedVoice`
    - :obj:`~fipper.types.InlineQueryResultArticle`
    - :obj:`~fipper.types.InlineQueryResultAudio`
    - :obj:`~fipper.types.InlineQueryResultContact`
    - :obj:`~fipper.types.InlineQueryResultDocument`
    - :obj:`~fipper.types.InlineQueryResultAnimation`
    - :obj:`~fipper.types.InlineQueryResultLocation`
    - :obj:`~fipper.types.InlineQueryResultPhoto`
    - :obj:`~fipper.types.InlineQueryResultVenue`
    - :obj:`~fipper.types.InlineQueryResultVideo`
    - :obj:`~fipper.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "fipper.Client"):
        pass
