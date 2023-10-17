"""This module contains base sprite classes used in SCPUP.

The exported classes of this module are:

* EauAnimatedSprite
* EauMaskedSprite
* EauSecuence
* EauSecuenceStep
* EauSprite
"""

from __future__ import annotations
from typing import Type, overload
import scpup
import pygame
import os


__all__: list[str] = [
  "EauAnimatedSprite",
  "EauSecuence",
  "EauSecuenceStep",
  "EauSprite",
  "eaucollidesprite",
  "eaucollidegroup",
]


def eaucollidegroup(sprite: EauSprite, group: scpup.EauGroup | list[EauSprite]) -> EauSprite | None:
  """Custom collition detecion function

  Args:
    sprite:
      A sprite with a 'rect' or 'mask' attribute.
    group:
      A EauGroup that has the sprites to check the collition with.
  """
  for spr in group:
    collided = eaucollidesprite(sprite, spr)
    if collided:
      return spr
  return None


def eaucollidesprite(sprite1: EauSprite, sprite2: EauSprite) -> bool:
  """Custom collition detecion function

  Args:
    sprite1:
      A sprite with a 'rect' or 'mask' attribute.
    sprite2:
      Another sprite with a 'rect' or 'mask' attribute.
  """
  # if hasattr(sprite1, 'mask') or hasattr(sprite2, 'mask'):
  if hasattr(sprite1, 'mask') and sprite1.mask and hasattr(sprite2, 'mask') and sprite2.mask:
    return pygame.sprite.collide_mask(sprite1, sprite2)
  else:
    return pygame.sprite.collide_rect(sprite1, sprite2)


class EauSprite:
  """A basic sprite.

  This sprite class can be used for any static sprite, and it is the base class
  for all the other sprite classes. This class is basically a copy of the
  pygame.sprite.Sprite class just with __slots__ added for optimization.


  Attributes:
    __g:
      A private dict used to store the groups that this sprite belongs to.
    image:
      The pygame.Surface image that will be rendered.
    rect:
      The pygame.Rect around the image.
    mask:
      A bitmask used for perfect collition detection. By default sprites don't
      have one. To create a sprite with a bitmask specify it in the constructor
      or with the method create_mask
    owner:
      The parent player of the sprite if it applies. If None then it means it is
      not owned by a player.
    name:
      The sprite name. This works as an identifier so is easier to find.
    subgroup:
      The subgroup that this sprite belongs to. This is only a logical grouping
      between sprites, meaning that this won't actually create an instance of
      anything, just to help with searching sprites and stuff.

  Class Attributes:
    base_speed:
      Class attribute that determinates how fast sprites move
    subclasses:
      dict of subclasses of EauSprite where each key is the name of the class
      and each value is the class itself.
    base_path:
      Private class attribute that stores the base path of the images of an
      EauSprite subclass
  """
  base_speed = 4
  subclasses: dict[str, Type[EauSprite]] = {}
  base_path = ''

  __slots__: tuple = (
    "__g",
    "image",
    "rect",
    "mask",
    "owner",
    "name",
    "subgroup"
  )

  @classmethod
  def __init_subclass__(cls, /, *, path: str | None = None, **kwargs):
    """This method is used to set the base path of the images of the instances
    of a subclass. This method also stores the subclass in a dict with its name
    as the key so that you can get a reference to a subclass with its name.

    Examples:

    ---

    * Using the path parameter:

    ```python
    import os
    class SomeSprite(EauSprite, path=os.path.join("path", "to", "image.png"):
      ...

    sprite1 = SomeSprite()
    sprite2 = SomeSprite()
    ```

    You can also pass the path partially, like this:

    ```python
    import os
    class SomeSprite(EauSprite, path=os.path.join("path", "to"):
      ...

    sprite1 = SomeSprite("image1.png")
    sprite2 = SomeSprite("image2.png")
    ```

    ---

    * Using the subclasses dict:

    ```python
    # In file1.py
    class SomeSprite(EauSprite):
      ...

    # In file2.py
    from scpup import EauSprite

    cls = EauSprite.subclasses.get('SomeSprite')
    cls(...)
    ```

    This way of instantiating sprites is used by the EauPlayerMeta to set the
    player's sprites, by getting the subclass of the sprite of each EauView

    ---

    Args:
      path:
        The path under `<root>/assets/images/` of where the image of
        the subclass exist. It can be partially specified or None.
    """
    super().__init_subclass__(**kwargs)
    if path:
      cls.base_path = path
    EauSprite.subclasses[cls.__name__] = cls

  def __init__(self,
               *paths: str,
               name: str | None = None,
               masked: bool = False,
               position: scpup.EauPosition | None = None,
               owner: str | None = None,
               subgroup: str | None = None):
    """Initializes a sprite with an image and the position.

    Args:
      *paths:
        Path segmente of where the image is stored. It should exists under
        `<root>/assets/images/<path>/` where <path> is the path passed to the
        class when inheriting from EauSprite
      masked:
        Whether to create a bitmask or not for this sprite.
      position:
        The Position of the sprite in an EauPosition object
      owner:
        The player id of the owner of this sprite, or None if it is not a player
        sprite. Defaults to None.
      subgroup:
        The subgroup of sprites that this sprite belongs to. This is only
        logical, no actual group will be created. Defaults to None.
    """
    self.image = self.mask = None
    self.owner = owner
    self.subgroup = subgroup
    self.__g = {}
    self.name = name or os.path.basename(paths[-1]).rsplit('.')[0]
    if len(paths) > 0:
      self.image, self.rect = scpup.load_image(
        self.__class__.base_path,
        *paths,
        alpha=True,
        position=position
      )
      if masked:
        self.mask = pygame.mask.from_surface(self.image)
    else:
      self.rect = pygame.Rect(0, 0, 0, 0)

  @property
  def topleft(self) -> tuple[int, int]:
    """Get the topleft attribute of this sprite's rect.

    Returns:
      tuple[int, int]:
        The topleft coordinates. Index 0 is the left (or x) coordinate and index
        1 is the top (or y) coordinate.
    """
    return self.rect.topleft

  @topleft.setter
  def topleft(self, value: tuple[int, int]) -> None:
    """Sets the topleft attribute of this sprite's rect.

    Args:
      value:
        The topleft value to be assigned where the index 0 is the left (or x)
        coordinate and the index 1 is the top (or y) coordinate.
    """
    self.rect.topleft = value

  @property
  def center(self) -> tuple[int, int]:
    """Get the center attribute of this sprite's rect.

    Returns:
      tuple[int, int]:
        The center coordinates. Index 0 is the center x coordinate and index
        1 is the center y coordinate.
    """
    return self.rect.center

  @center.setter
  def center(self, value: tuple[int, int]) -> None:
    """Sets the center attribute of this sprite's rect.

    Args:
      value:
        The center value to be assigned where the index 0 is the center x
        coordinate and the index 1 is the center y coordinate.
    """
    self.rect.center = value

  def add(self, *groups) -> None:
    """Add this sprite to groups.

    Args:
      *groups:
        The groups to be added to. These can be either pygame.srite.Group or
        scpup.EauGroup.
    """
    for g in groups:
      if hasattr(g, "_spritegroup") and g not in self.__g:
        g.add_internal(self)
        self.add_internal(g)

  def remove(self, *groups) -> None:
    """Remove this sprite from groups.

    Args:
      *groups:
        The groups to be removed from. These can be either pygame.srite.Group or
        scpup.EauGroup.
    """
    for g in groups:
      if g in self.__g:
        g.remove_internal(self)
        self.remove_internal(g)

  def add_internal(self, group) -> None:
    """Private method used to register a group that this sprite belongs to.

    Args:
      group:
        The group to register.
    """
    self.__g[group] = 0

  def remove_internal(self, group) -> None:
    """Private method used to remove a registered group.

    Args:
      group:
        The group to remove.
    """
    del self.__g[group]

  def update(self, *_, **__) -> None:
    """Update method placeholder so that subclasses can use it if needed."""
    pass

  def on_action(self, _: scpup.EauAction) -> None:
    """Action handler placeholder so that subclasses can use it if needed.

    Args:
      action:
        The action to handle
    """
    pass

  def on_collition(self, other: EauSprite) -> None:
    """Actions to do when detecting a colition

    Args:
      other:
        The sprite that collided with this sprite
    """

  def clamp(self, rect: pygame.Rect):
    """Move this sprite completely inside of a rect

    Args:
      rect:
        The rectangle to clamp this sprite"""
    if rect:
      self.rect = self.rect.clamp(rect)
      # self.rect.clamp_ip(rect)

  def move(self, dist: tuple[float, float], speed: float | None = None) -> None:
    """Move the sprite.

    Args:
      dist:
        The distance to move. Index 0 is horizontal movement, and index 1 is
        vertical movement
      speed:
        The speed in which the sprite will move, if None EauSprite.base_speed
        will be used. Defaults to None.
    """
    sp = speed or self.base_speed
    self.rect.move_ip(dist[0] * sp, dist[1] * sp)

  def kill(self) -> None:
    """Removes this sprite from all the groups that it belongs to."""
    for g in self.__g:
      g.remove_internal(self)
    self.__g.clear()

  def groups(self) -> list:
    """List all groups that this sprite belongs to."""
    return list(self.__g)

  def alive(self) -> bool:
    """Whether this sprite belongs to any group or not."""
    return bool(self.__g)


class EauSecuenceStep:
  """A step or frame of an animation secuence.

  Attributes:
    idx:
      The index of the image on the host images attribute.
    frames:
      An integer representing the number of frames that this step will live for.
  """
  __slots__: tuple = (
    "idx",
    "frames"
  )

  def __init__(self, idx: int, frames: int):
    self.idx: int = idx
    self.frames: int = frames


class EauSecuence:
  """A sprite's animation secuence.

  Attributes:
    name:
      A string that labels this secuence. It must match the key in the host's
      images dict where the images of this secuence live.
    steps:
      A list of the steps of this secuence.
    frame_count:
      The counter storing information about the current frame.
    step_count:
      The counter storing information about the current step.
    is_infinite:
      Whether the secuence never stops or not, defaults to False
    has_sound:
      Whether the secuence has a sound or not
  """
  __slots__: tuple = (
    "name",
    "steps",
    "frame_count",
    "step_count",
    "is_infinite",
    "has_sound"
  )

  def __init__(
    self,
    name: str,
    *steps: EauSecuenceStep | tuple[int, int],
    is_infinite: bool = False,
    sound_path: str | None = None
  ):
    """Initializes a secuence given a name and the corresponding steps.

    Args:
      name:
        The name of this secuence.
      *steps:
        The steps of this secuence. This can be either a EauSecuenceStep object
        or a tuple of 2 ints, where the first is the indeof the image and the
        second the number of frames.
      is_infinite:
        Whether the secuence never stops or not, Default is False.
      sound_path:
        The path of the sound file to play when triggering this secuence. It has
        to be under `<root>/assets/sounds/` and it has to be a `.wav` file. The
        sound won't be saved in the instance.
    """
    self.name: str = name
    self.steps = tuple(EauSecuenceStep(s[0], s[1]) if isinstance(s, tuple) else s for s in steps)
    self.frame_count: int = 0
    self.step_count: int = 0
    self.is_infinite = is_infinite
    audioService = scpup.EauService.get('EauAudioService')
    if sound_path:
      loaded = audioService.load(id(self), sound_path)
    else:
      loaded = False
    self.has_sound = loaded

  def __iter__(self) -> "EauSecuence":
    """Return itself because this class is basically an Iterable/Iterator."""
    return self

  def __next__(self) -> "EauSecuenceStep":
    """Retrieves the next step of the animation secuence.

    When you call the next() on this object and it raises a StopIteration, the
    object restarts itself so that you can call next() again without raising an
    exception.

    Raises:
      StopIteration:
        The secuence has finished iterating over its steps.

    Returns:
      EauSecuenceStep:
        The current step of the animation secuence.
    """
    if self.frame_count == self.steps[self.step_count].frames:
      self.frame_count = 0
      self.step_count += 1
    self.frame_count = self.frame_count + 1
    if self.step_count >= len(self.steps):
      self.frame_count = 0
      self.step_count = 0
      if not self.is_infinite:
        raise StopIteration
    return self.steps[self.step_count]

  def add_step(self, idx: int, frames: int) -> None:
    """Add a step to this secuence.

    Args:
      idx:
        The index of the image of this step.
      frames:
        The amount of frames of this step.
    """
    self.steps = self.steps + (EauSecuenceStep(idx, frames),)


class EauAnimatedSprite(EauSprite):
  """An animated sprite.

  This is a subclass of the EauSprite which stores the information and images
  needed to create an animation. This Sprite is not masked.

  Attributes:
    images:
      A dict where each key is the name of an animation and each value is a
      list of the images of that animation.
    default:
      A pygame.Surface holding the default image. The default image is the
      image rendered when no animation is active.
    secuences:
      A list of EauSecuence objects.
    current_secuence:
      The current secuence of an active animation or None if no animation is
      active.
  """
  __slots__: tuple = (
    "images",
    "default",
    "secuences",
    "current_secuence"
  )

  def __init__(self,
               *defaultpath: str,
               name: str | None = None,
               images: dict[str, str | list[str | tuple[str, ...]]] | None = None,
               secuences: list[EauSecuence] | None = None,
               position: scpup.EauPosition | None = None,
               subgroup: str | None = None,
               owner: str | None = None):
    """Initializes the sprite loading its default image and initial position.

    Args:
      *defaultpath:
        Path segments of where the default image of this sprite exists.
      name:
        The sprite name. This works as an identifier so is easier to find.
      images:
        The paths of the images used in the animations of this sprite. Each key
        of this argument is the name of an animation of this sprite, and each
        value is either a path (if the animation only consists of another image)
        or a list of paths (which can be passed in a tuple containing the
        segments of each image or the whole path).
      secuences:
        A list of EauSecuence objects that belong to this sprite.
      position:
        The Position of the sprite in an EauPosition object
      subgroup:
        The subgroup that this sprite belongs to. This is only a logical
        grouping between sprites, meaning that this won't actually create an
        instance of anything, just to help with searching sprites and stuff.
      owner:
        The player id of the owner of this sprite, or None if it is not a player
        sprite. Defaults to None.
    """
    super().__init__(*defaultpath, name=name, masked=False, position=position, subgroup=subgroup, owner=owner)
    self.default: pygame.Surface = self.image
    self.images: dict[str, list[pygame.Surface]] = {
      key: [
        scpup.load_image(self.__class__.base_path, paths)[0]
      ] if isinstance(paths, str) else [
        scpup.load_image(self.__class__.base_path, path)[0] if isinstance(path, str) else
        scpup.load_image(self.__class__.base_path, *path)[0] for path in paths
      ] for key, paths in images.items()
    } if images is not None else {}
    self.secuences: list[EauSecuence] = secuences or []
    self.current_secuence: EauSecuence | None = None

  def add_image(self, name: str, *paths: str) -> None:
    """Adds an image to an animation of this sprite.

    Args:
      name:
        The name of the animation that this image belongs to.
      *paths:
        Path segments of where the image exists. It should be a file in
        `<root>/assets/images/`.
    """
    img: pygame.Surface = scpup.load_image(*paths)[0]
    if name in self.images:
      self.images[name].append(img)
    else:
      self.images[name] = [img]

  @overload
  def set_secuence(self, name: str, *steps: EauSecuenceStep | tuple[int, int]) -> None:
    """Sets an animation secuence.

    Args:
      name:
        The name of the secuence. This has to match the key in this sprite's
        images from when the animation secuence will be taking its images.
      *steps:
        The steps of the secuence or a tuple where the index 0 is the idx of
        the image and the index 1 is the number of frames of that step.
    """
  @overload
  def set_secuence(self, secuence: EauSecuence) -> None:
    """Sets an animation secuence.

    Args:
      secuence:
        The secuence to set.
    """
  def set_secuence(self,  # type: ignore
                   name_or_secuence: str | EauSecuence,
                   *steps: EauSecuenceStep | tuple[int, int]) -> None:
    if isinstance(name_or_secuence, EauSecuence):
      self.secuences.append(name_or_secuence)
    else:
      self.secuences.append(EauSecuence(name_or_secuence, *steps))

  def reset(self) -> None:
    """Reset the sprite to its default state"""
    self.image = self.default
    # Not sure if I have to do self.rect = self.image.get_rect(**rectargs)
    self.current_secuence = None

  def update(self, *args, **kwargs) -> None:
    """Updates the sprite image based on the current secuence.

    Args:
      *args:
        Positional arguments to pass to the super().update() call.
      *kwargs:
        Keyword arguments to pass to the super().update() call.
    """
    super().update(*args, **kwargs)
    if self.current_secuence is not None:
      try:
        step: EauSecuenceStep = next(self.current_secuence)
        self.image = self.images[self.current_secuence.name][step.idx]
      except StopIteration:
        self.reset()

  def trigger(self, name: str) -> None:
    """Start an animation secuence.

    Args:
      name:
        The name of the secuence.
    """
    for s in self.secuences:
      if s.name == name:
        self.current_secuence = s
        if s.has_sound:
          scpup.EauService.get('EauAudioService').play(id(s))
        break
