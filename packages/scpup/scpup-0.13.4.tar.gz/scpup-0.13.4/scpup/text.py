from __future__ import annotations
from functools import partial
import re
import os
from typing import final
import pygame
import scpup


__all__ = [
  "EauText",
  "EauTextsGroup"
]


class EauTextMeta(type):
  """Metaclass for EauText

  To be able to render text you'll need to call `set_font` and provide the path
  of the font to use before trying to render any text.

  Attributes:
    _fonts_:
      A dictionary in which each key relates to a font size and the value of
      each key is the Font object of that font size
    _partial_font_obj_:
      The partial font object that will be used to render text. This is created
      with pygame.font.Font and the path of the font.
  """
  _fonts_: dict[int, pygame.font.Font] = {}
  _partial_font_obj_: partial

  def set_font(cls, *paths) -> None:
    """Set the path of the font thats going to be used

    Args:
      *path:
        The path segments of the font. The font file has to be placed anywhere
        under the `<root>/assets/fonts/` directory
    """

    if paths and paths[0] is not None:
      fontpath = os.path.join(scpup.BASE_PATH, "fonts", *paths)
      if os.path.exists(fontpath):
        cls._partial_font_obj_ = partial(pygame.font.Font, fontpath)
        cls._fonts_ = {}
        return
    fonts = pygame.font.get_fonts()
    cls._partial_font_obj_ = partial(pygame.font.SysFont, fonts[0])

  def font(cls, fontsize: int, /):
    """Get a font object (or create it if it doesn't exist) given a font size.

    Args:
      fontsize:
        The size of the font

    Raises:
      AttributeError:
        Trying to call this method before `set_font`

    Returns:
      A Font object of the requested size
    """
    if fontsize not in cls._fonts_:
      cls._fonts_[fontsize] = cls._partial_font_obj_(fontsize)
    return cls._fonts_[fontsize]


@final
class EauText(metaclass=EauTextMeta):
  """A text object used for rendering text in pygame surfaces.

  This class supports plain texts or updateable texts (explained below), and
  also it automatically wraps the text in new lines if needed (When specifying
  maxwidth). This class also supports subgrouping text so that you can easily
  search and find a group of texts within a EauTextsGroup.

  Remember to call `EauText.set_font` before instanciating this class.

  Attributes:
    _text:
      The actual text that this object stores
    image:
      The surface where the text is rendered
    rect:
      The rectangle of the surface where the text is rendered
    updatedict:
      A dictionary of the values that can be updated where each key is the name
      of the updateable value and each value is the current value of that
      updateable value. To set an updateable value in a text pass it in between
      brackets, for example:

      ```python
      txt = EauText("Hello {name}! How are you?", ...)
      ```

      In this example updatedict would be equal to `{"name": ""}` and then
      to update that value you would do this:

      ```python
      txt.update(name="Ivan")
      ```

    color:
      A tuple of 3 numbers from 0 to 255 for the RGB color. (I don't know if you
      can add a fourth one for alpha values). Defaults to (0, 0, 0) which is
      black.
    fontsize:
      The size of the font to be used for this text.
    showing:
      Whether the text should be drawn or not
    maxwidth:
      If set, the text will be wrapped in multiple lines (If it doesn't fit the
      maxwidth). Defaults to None.
    subgroup:
      A string holding the name of the subgroup that this text belongs to.
      Defaults to None.
    _drawn_rect:
      Private attribute that stores the last rectangle drawn to a surface
    position:
      The Position of the text in an EauPosition object
      The topleft corner of the text to be rendered
  """
  __slots__ = (
    "_text",
    "image",
    "rect",
    "updatedict",
    "color",
    "fontsize",
    "showing",
    "maxwidth",
    "subgroup",
    "_drawn_rect",
    "position"
  )

  def __init__(self,
               text: str, /, *,
               fontsize: int,
               position: scpup.EauPosition,
               color: tuple[int, int, int] | None = None,
               maxwidth: int | None = None,
               subgroup: str | None = None):
    """Initializes an EauText object

    Args:
      text:
        The text to be rendered
      fontsize:
        The size of the font to use
      position:
        The Position of the text in an EauPosition object
      color:
        The color of the text. Defaults to None.
      maxwidth:
        The maximum allowed with. Defaults to None.
      subgroup:
        The name of the subgroup that this text belongs to. Defaults to None.
    """
    self._text = text
    self.fontsize = fontsize
    self.position = position
    self.color = color or (0, 0, 0)
    self.maxwidth = maxwidth
    self.subgroup = subgroup
    self.showing = True
    results = re.findall(r'{([a-zA-Z0-9_]+)}', text)
    self.updatedict = dict.fromkeys(results, '') if results else None
    self.image: pygame.Surface | None = None
    self.rect: pygame.rect.Rect | None = None
    self._drawn_rect: pygame.Rect | None = None
    if not self.updatedict:
      self._render()

  def __eq__(self, value: object) -> bool:
    if isinstance(value, EauText):
      return self._text == value._text
    elif isinstance(value, str):
      return self._text == value
    return False

  def __str__(self) -> str:
    return self._text

  def draw(self, dest: pygame.Surface) -> None:
    """Draw the render of this text to a surface

    Args:
      dest:
        The target surface
    """
    if self.showing and self.image and self.rect:
      self._drawn_rect = dest.blit(self.image, self.rect, None)  # type: ignore

  def clear(self, dest: pygame.Surface, bg: pygame.Surface) -> None:
    """Clear the last drawn rectangle of this text from a surface using a
    background

    Args:
      dest:
        The target surface
      bg:
        The background of the target surface
    """
    if self._drawn_rect:
      dest.blit(bg, self._drawn_rect, self._drawn_rect)
      self._drawn_rect = None

  def update(self, **values) -> None:
    """Update the rendered text. Use this when an updateable value needs to be
    updated

    If this method is called without any matching keys or new values then the
    renders of the text won't get created again. Furthermore, if the text
    doesn't have values to update then the method won't do anything.

    Example:

    ```python
    # if the _text is "Values: {value1}, {value2}."
    txt.update(key1="value1", key2="value2")
    ```

    Args:
      **values:
        The dict entries to replace
    """
    if self.updatedict is None:
      return
    needs_update = False
    for key, value in values.items():
      if key in self.updatedict and self.updatedict[key] != value:
        self.updatedict[key] = value
        needs_update = True
    if needs_update:
      self._render()

  def _render(self):
    """Prepare the text to render the image surface and positionate its rect.

    This method replaces all updateable values with their current values and
    calls the method `_word_wrap` to get the surface of the text, and then gets
    the rect of the image.
    """
    text = self._text.format_map(self.updatedict) if self.updatedict else self._text
    self.image = self._word_wrap(text)
    self.rect = self.image.get_rect(**self.position.as_rectargs())

  def _word_wrap(self, text: str) -> pygame.surface.Surface:
    """Builds a surface with the text rendered.

    Args:
      text:
        The text that will be drawn on the surface

    Raises:
      ValueError:
        The word is too wide and does not fit the specified maxwidth.

    Returns:
      pygame.Surface:
        The surface with the text rendered.
    """
    font = self.__class__.font(self.fontsize)
    if self.maxwidth is None:
      return font.render(text, True, self.color, None)
    else:
      x, y, rows = 0, 0, []
      words = text.split(' ')
      space: float = font.size(' ')[0]
      maxheight = 0
      rowtext = ''
      for word in words:
        size: tuple[float, float] = font.size(word)
        if size[0] > self.maxwidth:
          raise ValueError()
        if size[0] + x <= self.maxwidth:
          rowtext += word
          x += size[0] + space
          maxheight = max(maxheight, size[1])
          if len(words) - 1 == words.index(word):
            surface = font.render(rowtext, True, self.color, None)
            rows.append((
              surface,
              (0, y)
            ))
            y += maxheight
        else:
          surface = font.render(rowtext, True, self.color, None)
          rows.append((
            surface,
            (0, y)
          ))
          rowtext = word
          y += maxheight
          x = size[0]
          maxheight = size[1]
      total_surf = pygame.Surface((self.maxwidth, maxheight))
      for row in rows:
        total_surf.blit(row[0], row[1], None)
      return total_surf

  def is_colliding(self, obj: tuple[float, float] | pygame.Rect | EauText | scpup.EauSprite) -> bool:  # type: ignore
    """Test if this text is colliding with a point, rectangle, sprite, or text

    Args:
      obj:
        The point, rectangle, sprite, or text to test collition with

    Returns:
      bool:
        Whether the text is colliding or not
    """
    if self.rect is not None:
      if isinstance(obj, (pygame.Rect, pygame.rect.Rect)):
        return self.rect.colliderect(obj)
      elif isinstance(obj, (EauText, scpup.EauSprite)):
        return bool(obj.rect) and self.rect.colliderect(obj.rect)
      else:
        return self.rect.collidepoint(obj)
    return False


@final
class EauTextsGroup:
  """A group of texts.

  This class is what EauGroup is to EauSprite. It has common methods for drawing
  texts, updating them, clearing them and detecting collitions with other texts
  and sprites

  Attributes:
    _texts:
      A list of the texts that belong to this group
  """
  __slots__ = (
    "_texts",
  )

  def __init__(self, *texts: EauText) -> None:
    """Initializes a text group

    Optionally you can pass any number of EauTexts to the constructor to add
    them to this group.
    """
    self._texts: list[EauText] = list(texts)

  def __iter__(self):
    return self._texts.__iter__()

  def __next__(self):
    return self.texts.__next__()

  def __contains__(self, value) -> bool:
    return value in self._texts

  def draw(self, dest: pygame.Surface) -> None:
    """Draw the texts to a surface

    Args:
      dest:
        The target surface
    """
    for text in self._texts:
      text.draw(dest)

  def clear(self, dest: pygame.Surface, background: pygame.Surface) -> None:
    """Clear the texts from a surface using a background

    Args:
      dest:
        The target surface
      background:
        The background of the surface
    """
    for text in self._texts:
      text.clear(dest, background)

  def empty(self) -> None:
    """Remove all texts from this group"""
    self._texts.clear()

  def add(self, text: EauText) -> None:
    """Add a text to this group

    Args:
      text:
        The text to add
    """
    self._texts.append(text)

  def remove(self, text: EauText) -> None:
    """Remove a text from this group

    Args:
      text:
        The text to remove
    """
    if text in self._texts:
      self._texts.remove(text)

  def texts(self, subgroup: str | None = None) -> list[EauText]:
    """Get all the texts of a subgroup or the whole group

    Args:
      subgroup:
        The subgroup of texts to get, if it is None then all the texts within
        this group will be retrieved. Defaults to None.

    Returns:
      list[EauText]:
        A list of texts
    """
    if subgroup is None:
      return self._texts
    else:
      return [txt for txt in self._texts if txt.subgroup == subgroup]

  def text(self, value: str, subgroup=None) -> None | EauText:
    """Get a text given its value. Optionally you can specify the subgroup so
    that the text is only searched in that subgroup.

    Args:
      value:
        The string value of the text
      subgroup:
        The name of the subrgoup to be searched. Defaults to None:

    Returns:
      The EauText object found or None if it wasn't found
    """
    return next((txt for txt in self.texts(subgroup) if txt == value), None)

  def update(self, **new_data) -> None:
    """Update the updateable texts in this group

    Args:
      **new_data:
        The values to update the texts with
    """
    for text in self._texts:
      text.update(**new_data)

  def showing(self, showing, *, subgroup=None):
    """Set the visibility of the texts in this group

    Args:
      showing:
        The value to set the texts visibility to
      subgroup:
        The subgroup to narrow the affected texts. Defaults to None.
    """
    for text in self.texts(subgroup):
      text.showing = showing

  def get_collition(self,
                    obj: tuple[float, float] | EauText | scpup.EauSprite | pygame.Rect,
                    subgroup=None) -> EauText | None:
    """Tests whether any text in this group (or subgroup if specified) collides
    an object

    Args:
      obj:
        The object to test the collition with. It can be a point, a rectangle, a
        EauSprite or another EauText
      subgroup:
        The subgroup to narrow the texts to test. Defaults to None.

    Returns:
      The EauText that the obj collided with or None if it didn't collide with
      any text
    """
    clicked_texts = [
      txt for txt in self.texts(subgroup)
      if txt.is_colliding(obj)
    ]
    return clicked_texts[0] if len(clicked_texts) > 0 else None
