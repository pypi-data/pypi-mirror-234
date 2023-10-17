from __future__ import annotations
from enum import Enum, auto
from typing import overload
import scpup


__all__ = [
  "EauLayoutType",
  "EauLayout",
  "EauPosition",
  "EauGrid"
]


class EauLayoutType(Enum):
  """Enumeration of the different layout types"""
  Position = auto()
  Top = auto()
  Bottom = auto()
  Center = auto()
  Left = auto()
  Right = auto()


class EauLayout:
  """A value used for setting the position of a coordinate

  Attributes:
    type: The type of layout.
    value: The value that will be used to calculate the position
  """

  __slots__ = (
    "type",
    "value"
  )

  def __init__(self, type: EauLayoutType, value: int = 0):
    """Initialize a layout object with the type and a value.

    Layouts can be created directly but it is highly recommended to use the
    respective classmethod of this class instead.

    EauLayout objects are not aware of what axis are they being used on (x or y)

    Args:
      type: The type of layout.
      value: The value that will be used to calculate the position.
    """
    self.type = type
    self.value = value

  @classmethod
  def Position(cls, value: int):
    """Create an EauLayout of Position type

    - Positioning: value
    - Anchor: centerx, centery
    """
    return cls(EauLayoutType.Position, value)

  @classmethod
  def Top(cls, value: int):
    """Create an EauLayout of Top type

    - Positioning: abs(value)
    - Anchor: centerx, top
    """
    return cls(EauLayoutType.Top, value)

  @classmethod
  def Bottom(cls, value: int):
    """Create an EauLayout of Bottom type

    - Positioning: size - abs(value)
    - Anchor: centerx, bottom
    """
    return cls(EauLayoutType.Bottom, value)

  @classmethod
  def Center(cls, value: int = 0):
    """Create an EauLayout of Center type

    - Positioning: size // 2 + value
    - Anchor: centerx, centery
    """
    return cls(EauLayoutType.Center, value)

  @classmethod
  def Left(cls, value: int):
    """Create an EauLayout of Left type

    - Positioning: abs(value)
    - Anchor: left, centery
    """
    return cls(EauLayoutType.Left, value)

  @classmethod
  def Right(cls, value: int):
    """Create an EauLayout of Right type

    - Positioning: size - abs(value)
    - Anchor: right, centery
    """
    return cls(EauLayoutType.Right, value)

  def parse(self, size: int) -> int:
    """Parse the layout and return the computed value. For types that require a
    size you have to pass it here

    Args:
      size:
        The width or height of where this layout will be positionated. Only
        needed in some layout types.

    Raises:
      ValueError: The type of this EayLayout is not a valid layout type.

    Returns:
      int: The computed value of this EauLayout (given it's type and value).
    """
    if self.type == EauLayoutType.Position:
      return self.value
    elif self.type == EauLayoutType.Top or self.type == EauLayoutType.Left:
      return abs(self.value)
    elif self.type == EauLayoutType.Right or self.type == EauLayoutType.Bottom:
      return size - abs(self.value)
    elif self.type == EauLayoutType.Center:
      return size // 2 + (self.value)
    raise ValueError(f"Unknown layout type: {self.type}")


class EauPosition:
  """A position (x, y)

  Attributes:
    x: The EauLayout object for the x coordinate
    y: The EauLayout object for the y coordinate
    margin:
      The space between the boundaries of an imaginary rectangle and the
      boundaries of the game window, if this value is 0 then that imaginary
      rectangle would be the game window rectangle.
  """

  __slots__ = (
    "x",
    "y",
    "margin"
  )

  def __init__(
    self,
    x: int | EauLayout,
    y: int | EauLayout,
    *,
    margin: int | tuple[int, int] | tuple[int, int, int, int] = 0
  ):
    """Initialize a position object

    Args:
      x: The EauLayout describing the x coordinate of this position.
      y: The EauLayout describing the y coordinate of this position.
      margin:
        A value that can be either and int (an equal margin for all sides), a
        tuple with 2 values (first value for left and right, and second value
        for top and bottom), or a tuple with 4 values (each for one side in the
        following order: left, right, top, bottom).
    """
    self.x = x if isinstance(x, EauLayout) else EauLayout.Position(x)
    self.y = y if isinstance(y, EauLayout) else EauLayout.Position(y)
    self.margin = margin

  def as_rectargs(self) -> dict[str, int]:
    """Convert this EauPosition instance to a dict with each key being the
    position argument for a pygame.Rect and each value the value for that
    argument."""
    displayService = scpup.EauService.get("EauDisplayService")
    width, height = displayService.size
    if isinstance(self.margin, int):
      ml = mr = mt = mb = self.margin
    elif len(self.margin) == 2:
      (ml, mt), (mr, mb) = self.margin, self.margin
    else:
      ml, mr, mt, mb = self.margin
    xarg = self.x.type.name.lower() if self.x.type in [EauLayoutType.Left, EauLayoutType.Right] else "centerx"
    yarg = self.y.type.name.lower() if self.y.type in [EauLayoutType.Top, EauLayoutType.Bottom] else "centery"
    if self.x.type == EauLayoutType.Right:
      ml = 0
      width -= mr
    if self.y.type == EauLayoutType.Bottom:
      mt = 0
      height -= mb
    return {
      xarg: ml + self.x.parse(width - (ml + mr)),
      yarg: mt + self.y.parse(height - (mt + mb))
    }


class EauGrid:
  """A grid for positioning objects in the game window

  Attributes:
    rows:
      The number of rows that this grid has. If None then this grid won't be
      able to calculate values for 'y' coordinates
    cols:
      The number of columns that this grid has. If None then this grid won't be
      able to calculate values for 'x' coordinates
    margin:
      The space between the boundaries of an imaginary rectangle and the
      boundaries of the game window, if this value is 0 then that imaginary
      rectangle would be the game window rectangle.
  """
  __slots__ = (
    "rows",
    "cols",
    "margin"
  )

  def __init__(self,
               rows: int | None = None,
               cols: int | None = None,
               *,
               margin: int | tuple[int, int] | tuple[int, int, int, int] = 0):
    """Initializes a grid object

    Args:
      rows: The number of rows that this grid has. Defaults to None.
      cols: The number of columns that this grid has. Defaults to None.
      margin:
        A value that can be either and int (an equal margin for all sides), a
        tuple with 2 values (first value for left and right, and second value
        for top and bottom), or a tuple with 4 values (each for one side in the
        following order: left, right, top, bottom).
    """
    self.rows = rows
    self.cols = cols
    if isinstance(margin, int):
      self.margin = (margin, margin, margin, margin)
    elif len(margin) == 2:
      self.margin = (margin[0], margin[0], margin[1], margin[1])
    else:
      self.margin = margin

  @overload
  def __call__(self, n: int) -> EauLayout:
    """Get the EauLayout of a row / column. This is used when either rows or
    cols is None.

    Args:
      n: The row / column to get.

    Returns:
      EauLayout: The calculated layout of the row / column.
    """
  @overload
  def __call__(self, x: int, y: int) -> EauPosition:
    """Get the EauPosition of a cell

    Args:
      x: The column to get
      y: The row to get

    Returns:
      EauPosition: The calculated position of the cell
    """
  def __call__(self, x: int, y: int | None = None) -> EauPosition | EauLayout:  # type: ignore
    if y is not None:
      return self.cell(x, y)
    elif self.rows is None:
      return self.x(x)
    else:
      return self.y(x)

  def x(self, num: int) -> EauLayout:
    """Get the EauLayout of a column.

    Args:
      num: The column to get.

    Returns:
      EauLayout: The calculated layout of the column.
    """
    if not self.cols:
      raise ValueError("Columns were not specified for this grid.")
    elif 1 > num > self.cols:
      raise ValueError(f"Column value must be between 1 and {self.cols}.")
    size = scpup.EauService.get("EauDisplayService").size
    w = (size[0] - (self.margin[0] + self.margin[1])) // (self.cols * 2)
    t = num * 2 - 1
    return EauLayout.Position(self.margin[0] + w * t)

  def y(self, num: int) -> EauLayout:
    """Get the EauLayout of a row.

    Args:
      n: The row to get.

    Returns:
      EauLayout: The calculated layout of the row.
    """
    if not self.rows:
      raise ValueError("Rows were not specified for this grid.")
    elif 1 > num > self.rows:
      raise ValueError(f"Row value must be between 1 and {self.rows}.")
    size = scpup.EauService.get("EauDisplayService").size
    w = (size[1] - (self.margin[2] + self.margin[3])) // (self.rows * 2)
    t = num * 2 - 1
    return EauLayout.Position(self.margin[2] + w * t)

  def cell(self, x: int, y: int) -> EauPosition:
    """Get the EauPosition of a cell

    Args:
      x: The column to get
      y: The row to get

    Returns:
      EauPosition: The calculated position of the cell
    """
    if not self.rows or not self.cols:
      raise ValueError("Grid is not made for 2 axis.")
    elif 1 > x > self.cols or 1 > y > self.rows:
      raise ValueError("Row and column values must be between 1 and the total of each axis.")
    return EauPosition(
      self.x(x),
      self.y(y)
    )
