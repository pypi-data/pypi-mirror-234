from typing import Any, Optional

from pytablewriter.style import Cell, Style
from tcolorpy import Color


DEFAULT_COLOR = "white"


def _calc_other_ground_color(color: Color) -> Color:
    invert_threshold = 385

    if (color.red + color.green + color.blue) > invert_threshold:
        return Color("black")

    return Color("white")


def style_filter(cell: Cell, **kwargs: Any) -> Optional[Style]:
    fg_color: Optional[Color] = None
    bg_color: Optional[Color] = None

    color = Color(kwargs.get("color", DEFAULT_COLOR))
    other_color = _calc_other_ground_color(color)

    if cell.col % 2 == 0:
        fg_color = other_color
        bg_color = color
    else:
        fg_color = color
        bg_color = other_color

    if fg_color or bg_color:
        if cell.is_header_row():
            return Style(color=fg_color, bg_color=bg_color, align="center")
        else:
            return Style(color=fg_color, bg_color=bg_color)

    return None
