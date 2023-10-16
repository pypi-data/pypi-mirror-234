"""
Functions for creating color gradients.
"""
import numpy as np

from ..geometry import lerp
from .color_types import AColor, Color, ColorPair

__all__ = [
    "rainbow_gradient",
    "lerp_colors",
    "gradient",
]

SomeColor = Color | AColor | ColorPair


def rainbow_gradient(
    n: int, *, color_type: type[Color | AColor] = Color
) -> list[Color | AColor]:
    """
    Return a rainbow gradient of `n` colors.

    Parameters
    ----------
    n : int
        Number of colors in gradient.
    color_type : Color | AColor, default: Color
        Color type of gradient.
    """
    TAU = 2 * np.pi
    OFFSETS = np.array([0, TAU / 3, 2 * TAU / 3])
    THETA = TAU / n

    return [
        color_type(*(int(j) for j in (np.sin(THETA * i + OFFSETS) * 127 + 128)))
        for i in range(n)
    ]


def lerp_colors(start: SomeColor, end: SomeColor, p: float) -> SomeColor:
    """
    Linear interpolation from `start` to `end` with proportion `p`.

    Parameters
    ----------
    start : SomeColor
        Start color.
    end : SomeColor
        End Color
    p : float
        Proportion from start to end.
    """
    return type(start)(*(round(lerp(a, b, p)) for a, b in zip(start, end)))


def gradient(start: SomeColor, end: SomeColor, ncolors: int) -> list[SomeColor]:
    """
    Return a gradient from `start` to `end` with `ncolors` (> 1) colors.

    Parameters
    ----------
    start : SomeColor
        Start color or colorpair.
    end : SomeColor
        End color of colorpair.
    ncolors : int
        Number of colors in gradient.
    """
    if ncolors < 2:
        raise ValueError(f"not enough colors ({ncolors=})")

    return [lerp_colors(start, end, i / (ncolors - 1)) for i in range(ncolors)]
