"""This module contains base group classes used in SCPUP
"""

from __future__ import annotations
from typing import Any, Iterator
import pygame
import scpup

__all__: list[str] = [
  "EauGroup",
]


class EauGroup:
  """A sprite group

  This sprite group class is the base clase for all the other group classes.
  This class is basically a copy of the pygame.sprite.Group class with
  __slots__ added for optimization and spritedict changed to __s, but it has a
  property called spritedict so that its compatible with pygame's groups

  Attributes:
    __s:
      Private attribute that stores the sprites that belong to this group
    lostsprites:
      Private attribute that is used to clear correctly the screen after
      removing sprites from this group
    _spritegroup:
      Class attribute that is only for compatibility with pygame groups
  """
  _spritegroup = True

  __slots__: tuple = (
    "__s",
    "lostsprites"
  )

  def __init__(self, *sprites: scpup.EauSprite) -> None:
    """Initializes a sprite group.

    Args:
      *sprites:
        Optionally the constructor can recieve any number of sprites that belong
        to it (To add them to this group)
    """
    self.__s: dict[scpup.EauSprite, Any] = {}
    self.lostsprites = []
    self.add(*sprites)

  def __bool__(self) -> bool:
    """Tests whether this group is empty or not"""
    return len(self) > 0

  def __len__(self) -> int:
    """Get the amount of sprites in this group"""
    return len(self.__s)

  def __iter__(self) -> Iterator:
    """Returns an iterator of the sprites in this group"""
    return iter(self.sprites())

  def __contains__(self, sprite: scpup.EauSprite) -> bool:
    """Tests whether a sprite exists or not in this group"""
    return sprite in self.__s

  def __getitem__(self, idx: int) -> scpup.EauSprite:
    """Get a sprite, given a numeric index."""
    if 0 < idx < self.__len__():
      return list(self.__s)[idx]
    raise IndexError('Index out of range')

  @property
  def spritedict(self) -> dict[scpup.EauSprite, Any]:
    """Get the self.__s attribute. Basically this is just for compatibility
    issues with pygame.sprite.Group and its subclasses

    Returns:
      dict:
        The attribute __s
    """
    return self.__s

  def add_internal(self, sprite: scpup.EauSprite) -> None:
    """Private method used to register a sprite that belongs to this group

    Args:
      sprite: The sprite to register
    """
    self.__s[sprite] = 0

  def remove_internal(self, sprite: scpup.EauSprite) -> None:
    """Private method used to remove a registered sprite

    Args:
      sprite: The sprite to remove
    """
    lost_rect = self.__s[sprite]
    if lost_rect:
      self.lostsprites.append(lost_rect)
    del self.__s[sprite]

  def sprites(self, subgroup: str | None = None) -> list[scpup.EauSprite]:
    """Get a list of the sprites in this group

    Args:
      subgroup:
        Narrow the list by only getting the sprites that belong to a subgroup

    Returns:
      list: A list of the sprites that belong to this group
    """
    return [s for s in self.__s if s.subgroup == subgroup] if subgroup else list(self.__s)

  def add(self, *sprites: scpup.EauSprite) -> None:
    """Add sprites to this group

    Args:
      *sprites:
        The sprites to be added. These can be either pygame.srite.Sprite or
        scpup.EauSprite or any subclass of these.
    """
    for sprite in sprites:
      if sprite not in self.__s:
        self.add_internal(sprite)
        sprite.add_internal(self)

  def remove(self, *sprites: scpup.EauSprite) -> None:
    """Remove sprites from this group

    Args:
      *sprites:
        The sprites to be removed. These can be either pygame.srite.Sprite or
        scpup.EauSprite or any subclass of these
    """
    for sprite in sprites:
      if sprite in self.__s:
        self.remove_internal(sprite)
        sprite.remove_internal(self)

  def update(self, *args, subgroup: str | None = None, **kwargs) -> None:
    """Call the update method of the sprites in this group

    Args:
      subgroup: If not None update only the sprites that belong to a subgroup.
    """
    for sprite in self.sprites(subgroup):
      sprite.update(*args, **kwargs)

  def draw(self, surface: pygame.Surface, subgroup: str | None = None) -> None:
    """Draws the sprites that belong to this group on a given surface

    Args:
      surface: The pygame.Surface to draw the sprites to.
      subgroup: The subgroup of sprites to draw, None by Default.
    """
    sprites: list[scpup.EauSprite] = self.sprites(subgroup)
    if hasattr(surface, "blits"):
      self.__s.update(
        zip(
          sprites,
          surface.blits(
            (spr.image, spr.rect, None) for spr in sprites
          )  # type: ignore
        )
      )
    else:
      for spr in sprites:
        if spr.image is not None and spr.rect is not None:
          self.__s[spr] = surface.blit(spr.image, spr.rect, None)
    self.lostsprites = []

  def clear(self, surface: pygame.Surface, bg: pygame.Surface) -> None:
    """Clear the sprites that were last drawn from a surface using a background

    Args:
      surface:
        The pygame.Surface to clear the sprites from
      bg:
        The pygame.Surface that will be used to clear the sprites from the
        surface
    """
    for lost_clear_rect in self.lostsprites:
      surface.blit(bg, lost_clear_rect, lost_clear_rect)
    for clear_rect in self.__s.values():
      if clear_rect:
        surface.blit(bg, clear_rect, clear_rect)

  def empty(self, subgroup: str | None = None) -> None:
    """Remove all sprites from this group. THIS STILL HAS THE FUNCTIONALITY IT
    HAD BEFORE COMMENTED OUT BECAUSE IT HAS NOT BEEN TESTED

    Args:
      subgroup:
        If not None then remove only a subgroup of sprites from this group.
    """
    self.remove(*self.sprites(subgroup))
    # for sprite in self.__s:
    #   self.remove_internal(sprite)
    #   sprite.remove_internal(self)
