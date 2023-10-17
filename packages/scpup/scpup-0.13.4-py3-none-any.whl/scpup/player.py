"""SCPUP Players helper module

This module has a class used to handle all player logic, meaning movement,
interaction with the game and with the other players.

Colors:

* p1: #7F1791
* p2: #028713
* p3: #808000
* p4: #008DD4
* search color: #dddddd
"""

from __future__ import annotations
import scpup
import pygame
from typing import final, overload
from typing import Literal

from scpup.sprite import EauSprite

__all__: list[str] = [
  "PlayerIdType",
  "EauPlayer"
]

PlayerIdType = Literal["p1", "p2", "p3", "p4"]


class EauPlayerMeta(type):
  """Metaclass for EauPlayer class. Implements a Singleton but instead of
  storing only 1 instance, it stores a maximum of 4 instances"""
  _instances: dict[str, EauPlayer] = {}
  _current_sprite: str | None = None

  @overload
  def __call__(cls) -> list[EauPlayer]:
    """Get a list of all the player instances."""
  @overload
  def __call__(cls, iid: int) -> EauPlayer | None:
    """Get a player given a controller instance id."""
  @overload
  def __call__(cls, pid: str) -> EauPlayer:
    """Get or create a player given a player id."""
  def __call__(cls, pid_iid: int | str | None) -> list[EauPlayer] | EauPlayer | None:  # type: ignore
    if pid_iid is None:
      return list(cls._instances.values())
    elif isinstance(pid_iid, int):
      return next((p for p in cls._instances.values() if p.iid == pid_iid), None)
    else:
      if pid_iid not in cls._instances:
        instance = super().__call__(pid_iid)
        cls._instances[pid_iid] = instance
      return cls._instances[pid_iid]

  def __len__(cls) -> int:
    """Get the number of player instances

    Returns:
      int:
        The number of player instances
    """
    return len(cls._instances)

  def create(cls, with_ctrl: scpup.EauCtrl | None = None) -> None:
    """Create a EauPlayer instance.

    This method will know which player id goes next. If 4 players are already
    playing then this method will return None.

    Args:
      with_ctrl:
        Optionally you can pass a controller to assign it to the new player.
    """
    if len(cls._instances) < 4:
      new_player = cls.__call__(f"p{len(cls._instances) + 1}")
      if with_ctrl:
        new_player.assign_ctrl(with_ctrl)

  @overload
  def remove_player(cls, iid: int) -> None:
    """Remove a player instance given a controller instance id

    Args:
      iid:
        The controller instance id to find the player that has it assigned
    """
  @overload
  def remove_player(cls, player: EauPlayer) -> None:
    """Remove a player instance.

    This method does all the logic needed to remove a player instance, like
    unassigning the controller that the player has currently assigned, and stuff
    like that.

    Args:
      player:
        The player instance to remove.
    """
  def remove_player(cls, iid_or_player: EauPlayer | int) -> None:  # type: ignore
    if isinstance(iid_or_player, int):
      player = EauPlayer(iid_or_player)
    else:
      player = iid_or_player
    if player is not None and player in cls._instances.values():
      player.unassign_ctrl()
      cls._instances.pop(player.pid)
      players = list(cls._instances.values())
      cls._instances = {}
      for i in range(len(players)):
        players[i].pid = f"p{i + 1}"
        cls._instances[players[i].pid] = players[i]

  def draw(cls, surface) -> None:
    """Calls the draw method of each EauPlayer instance

    Args:
      surface:
        The target surface
    """
    for p in cls._instances.values():
      p.sprites.draw(surface, subgroup="active")

  def update(cls, *args, **kwargs) -> None:
    """Calls the update method of each EauPlayer instance"""
    for p in cls._instances.values():
      p.move(kwargs.get('rect', None))
      p.sprites.update(*args, subgroup="active", **kwargs)

  def clear(cls, surface, background) -> None:
    """Calls the clear method of each EauPlayer instance

    Args:
      surface:
        The target surface
      background:
        The background surface
    """
    for p in cls._instances.values():
      p.sprites.clear(surface, background)

  def check_collitions(cls, group: scpup.EauGroup | None) -> None:
    """Check collitions for each EauPlayer instance.

    If a group is passed then it check the collitions against that group, else
    if group is not passed or is None then it checks collitions between player
    sprites.

    # TODO: Fix checking collitions against other players sprites

    Args:
      group:
        The group of sprites to test collitions against
    """
    if group:
      for p in cls._instances.values():
        p.check_collition(group)
    else:
      for p in cls._instances:
        for other in [id for id in cls._instances if id != p]:
          cls._instances[p].check_collition(cls._instances[other].sprites)

  def set_sprites(cls, sprite_cls_name: str) -> None:
    """Sets the active sprite of each EauPlayer instance

    Args:
      sprite_cls_name:
        The name of the class of the sprite to instanciate and assign to each
        EauPlayer instance.
    """
    cls._current_sprite = sprite_cls_name
    sprite_cls = scpup.EauSprite.subclasses.get(sprite_cls_name)
    if sprite_cls:
      for p in cls._instances.values():
        p.set_sprite(sprite_cls(f"{p.pid}.png", masked=True, owner=p.pid))


@final
class EauPlayer(metaclass=EauPlayerMeta):
  """ A player instance

  Attributes:
    pid:
      The player id. It can be one of 'p1', 'p2', 'p3', and 'p4'.
    iid:
      The controller instance id of the controller assigned to this player.
    sprites:
      A named group of the sprites that belong to this player.
  """
  __slots__: tuple = (
    "pid",
    "iid",
    "sprites"
  )

  @overload
  def __init__(self):
    """Get a list of all the player instances"""
  @overload
  def __init__(self, instance_id: int):
    """Get a player given a controller instance id, or None if no player has the
    provided instance id assigned

    Args:
      instance_id: The joystick instance id.
    """
  @overload
  def __init__(self, player_id: PlayerIdType):
    """Initializes a player with an ID.

    Since EauPlayers are implemented with a Singleton pattern, if the player id
    received already exists in the stored players then that one will be returned
    instead of creating a new one.

    Args:
      player_id: The player id. It can be one of 'p1', 'p2', 'p3', and 'p4'.
    """
  def __init__(self, player_id: PlayerIdType):  # type: ignore
    self.pid = player_id
    self.iid: int | None = None
    self.sprites = scpup.EauGroup()
    if self.__class__._current_sprite:
      cls = EauSprite.subclasses.get(self.__class__._current_sprite)
      if cls:
        self.set_sprite(cls(f"{self.pid}.png", masked=True, owner=self.pid))

  @property
  def sprite(self) -> scpup.EauSprite | None:
    """Get the active sprite of this player

    Returns:
      EauSprite:
        The active sprite or None if there is no active sprite. Active sprite
        means the sprite that the player is currently using
    """
    spr_list = self.sprites.sprites('active')
    if spr_list:
      return spr_list[0]
    return None

  @property
  def ctrl(self) -> scpup.EauCtrl | None:
    """Get the controller assigned to this player

    Returns:
      EauCtrl:
        The assigned controller. If this player does not have a controller
        assigned this method will return None.
    """
    return None if self.iid is None else scpup.EauCtrl(self.iid)

  @overload
  def assign_ctrl(self, iid: int) -> None:
    """Assign a controller to this player given its joystick instance id

    Args:
      iid: The joystick instance id.
    """
  @overload
  def assign_ctrl(self, ctrl: scpup.EauCtrl) -> None:
    """Assign a controller to this player

    Args:
      ctrl: The controller to assign
    """
  def assign_ctrl(self, iid_or_ctrl: scpup.EauCtrl | int) -> None:  # type: ignore
    if isinstance(iid_or_ctrl, int):
      self.iid = iid_or_ctrl
    else:
      self.iid = iid_or_ctrl.iid

  def unassign_ctrl(self) -> None:
    """Unassign the currently assigned controller of this player"""
    self.iid = None

  @overload
  def handle_joystick_input(self, button_num: int) -> None:
    """Handle a button down event.

    Args:
      button_num: The button num corresponding to the button that was pressed.
    """
  @overload
  def handle_joystick_input(self, axis_num: int, value: float) -> None:
    """Handle a button down event.

    Args:
      axis_num: The axis num corresponding to the axis that was moved.
      value: The amount of movement of the axis
    """
  def handle_joystick_input(self, num: int, value: float | None = None) -> None:  # type: ignore
    ctrl = self.ctrl
    if ctrl:
      action = ctrl.action(num) if value is None else ctrl.action(num, value)
      sprite = self.sprite
      if action and sprite:
        sprite.on_action(action)

  def move(self, area: pygame.Rect | None = None) -> None:
    """Move the player's active sprite

    Args:
      area:
        The area to clamp the sprite in after moving it, if None is passed then
        the sprite won't be clamped. Defaults to None.
    """
    ctrl, sprite = self.ctrl, self.sprite
    if ctrl and sprite:
      sprite.move(ctrl.LS)
      if area:
        sprite.clamp(area)

  def check_collition(self, group: scpup.EauGroup):
    """Check collitions with a group of sprites

    Args:
      group:
        The group of sprites to check the collition with
    """
    sprite = self.sprite
    if sprite:
      collided_sprite = pygame.sprite.spritecollideany(sprite, group, collided=scpup.eaucollidesprite)
      if collided_sprite:
        ...
        # Commented this out because I'm still working on it
        # sprite.on_collition(collided_sprite)
        # collided_sprite.on_collition(sprite)

  def set_sprite(self, sprite: scpup.EauSprite):
    """Sets the active sprite

    TODO: Maybe cache the active sprite instead of killing it

    Args:
      sprite:
        The sprite that's going to be set as the active sprite
    """
    sprt = self.sprite
    if sprt:
      sprt.kill()
    sprite.subgroup = "active"
    self.sprites.add(sprite)
