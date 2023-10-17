#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class BoostsStatus(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pyrogram.raw.base.stories.BoostsStatus`.

    Details:
        - Layer: ``165``
        - ID: ``E5C1AA5C``

    Parameters:
        level (``int`` ``32-bit``):
            N/A

        current_level_boosts (``int`` ``32-bit``):
            N/A

        boosts (``int`` ``32-bit``):
            N/A

        boost_url (``str``):
            N/A

        my_boost (``bool``, *optional*):
            N/A

        next_level_boosts (``int`` ``32-bit``, *optional*):
            N/A

        premium_audience (:obj:`StatsPercentValue <pyrogram.raw.base.StatsPercentValue>`, *optional*):
            N/A

    Functions:
        This object can be returned by 1 function.

        .. currentmodule:: pyrogram.raw.functions

        .. autosummary::
            :nosignatures:

            stories.GetBoostsStatus
    """

    __slots__: List[str] = ["level", "current_level_boosts", "boosts", "boost_url", "my_boost", "next_level_boosts", "premium_audience"]

    ID = 0xe5c1aa5c
    QUALNAME = "types.stories.BoostsStatus"

    def __init__(self, *, level: int, current_level_boosts: int, boosts: int, boost_url: str, my_boost: Optional[bool] = None, next_level_boosts: Optional[int] = None, premium_audience: "raw.base.StatsPercentValue" = None) -> None:
        self.level = level  # int
        self.current_level_boosts = current_level_boosts  # int
        self.boosts = boosts  # int
        self.boost_url = boost_url  # string
        self.my_boost = my_boost  # flags.2?true
        self.next_level_boosts = next_level_boosts  # flags.0?int
        self.premium_audience = premium_audience  # flags.1?StatsPercentValue

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BoostsStatus":
        
        flags = Int.read(b)
        
        my_boost = True if flags & (1 << 2) else False
        level = Int.read(b)
        
        current_level_boosts = Int.read(b)
        
        boosts = Int.read(b)
        
        next_level_boosts = Int.read(b) if flags & (1 << 0) else None
        premium_audience = TLObject.read(b) if flags & (1 << 1) else None
        
        boost_url = String.read(b)
        
        return BoostsStatus(level=level, current_level_boosts=current_level_boosts, boosts=boosts, boost_url=boost_url, my_boost=my_boost, next_level_boosts=next_level_boosts, premium_audience=premium_audience)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.my_boost else 0
        flags |= (1 << 0) if self.next_level_boosts is not None else 0
        flags |= (1 << 1) if self.premium_audience is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.level))
        
        b.write(Int(self.current_level_boosts))
        
        b.write(Int(self.boosts))
        
        if self.next_level_boosts is not None:
            b.write(Int(self.next_level_boosts))
        
        if self.premium_audience is not None:
            b.write(self.premium_audience.write())
        
        b.write(String(self.boost_url))
        
        return b.getvalue()
