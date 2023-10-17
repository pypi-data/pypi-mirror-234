from __future__ import annotations

from enum import Enum, auto
import pygame
import pygame.event
import pygame.mixer
import scpup
from typing import Any, Literal, final, overload


__all__: list[str] = [
  "EauService",
  "EauDisplayService",
  "EauEventService",
  "EauEventSubtype",
  "EauAudioService"
]


class EauServiceMeta(type):
  _instances_: dict[str, EauService] = {}

  def __call__(cls, *args, **kwds) -> Any:
    if cls.__name__ not in cls._instances_:
      instance = super().__call__(*args, **kwds)
      cls._instances_[cls.__name__] = instance
    return cls._instances_[cls.__name__]


class EauService(metaclass=EauServiceMeta):
  """Base class for scpup services. If you want to use a service you'll need to
  call EauService.get and pass the service name as an argument

  Class Attributes:
    view:
      The view currently being displayed.
  """
  view: scpup.EauView | None = None

  __slots__ = ()

  def _on_set_view(self) -> None:
    """This method is a hook for the subclasses of EauService so that they can
    do tasks when loading a new view"""
    ...

  @overload
  @classmethod
  def get(cls, service_name: Literal['EauDisplayService']) -> EauDisplayService:
    """Get the display service"""
  @overload
  @classmethod
  def get(cls, service_name: Literal['EauEventService']) -> EauEventService:
    """Get the event service"""
  @overload
  @classmethod
  def get(cls, service_name: Literal['EauAudioService']) -> EauAudioService:
    """Get the audio service"""
  @classmethod
  def get(cls, service_name: str) -> EauService:
    service = cls._instances_.get(service_name, None)
    if not service:
      raise RuntimeError(f"Service '{service_name}' does not exist or has not been initialized.")
    return service

  @classmethod
  def set_view(cls, view: scpup.EauView | str):
    """Set the current view

    This method is very important since it calls a hook on all EauService
    subclasses to perform some tasks when loading a new view

    Args:
      view:
        The view to set
    """
    if isinstance(view, str):
      view_cls = scpup.EauView.get(view)
      if view_cls:
        view = view_cls()
        cls.view = view
      else:
        raise RuntimeError(f"View '{view}' was not found.")
    else:
      cls.view = view
    for service in cls._instances_.values():
      service._on_set_view()


@final
class EauDisplayService(EauService):
  """A service used for all display related tasks

  Attributes:
    _display:
      The main display of the game
    _background:
      The background of the current view
    _default_bg:
      The default background used in views that don't have a background
    viewport:
      The main display rect
  """

  __slots__: tuple = (
    "_display",
    "_background",
    "_default_bg",
    "viewport"
  )

  def __init__(self, *, size: tuple[int, int], icon_path: str | None, caption: str | None):
    """Initialize the display service"""
    self.viewport = pygame.Rect(0, 0, *size)
    self._display: pygame.Surface = pygame.display.set_mode(size)
    if icon_path:
      img, _ = scpup.load_image(icon_path)
      pygame.display.set_icon(img)
    if caption:
      pygame.display.set_caption(caption)
    pygame.mouse.set_visible(0)
    bg = pygame.Surface(self.size)
    bg.fill(pygame.Color(86, 193, 219))
    self._default_bg = bg.convert()
    self._background: pygame.surface.Surface = self._default_bg

  @property
  def size(self) -> tuple[int, int]:
    return self.viewport.size

  def _on_set_view(self) -> None:
    """Set the current view and the players sprites"""
    if self.view:
      self._background = self.view.background or self._default_bg
      scpup.EauPlayer.set_sprites(self.view.player_sprite)
    self._display.blit(self._background, (0, 0))

  def update_view(self, *args, **kwargs) -> None:
    """Main display update method

    This method calls the `clear` method, then the `update` method, and then the
    `draw` method of the view and the players. This method also checks for
    collitions between the players sprites and the view sprites, and then
    between the players sprites and the other players sprites.

    Args:
      *args, **kwargs:
        Any arguments to pass to the sprites update method
    """
    if self.view:
      self.view.clear(self._display, self._background)
      scpup.EauPlayer.clear(self._display, self._background)
      self.view.update(*args, rect=self.viewport, **kwargs)
      scpup.EauPlayer.update(*args, rect=self.viewport, **kwargs)
      self.view.draw(self._display)
      scpup.EauPlayer.draw(self._display)
      # scpup.EauPlayer.check_collitions()
      # scpup.EauPlayer.check_collitions(self.view.sprites)
    pygame.display.flip()


EAU_EVENT = pygame.event.custom_type()


class EauEventSubtype(Enum):
  """A subtype of the EAU_EVENT events"""
  NAV = auto()
  QUIT = auto()
  VIEW = auto()


@final
class EauEventService(EauService):
  """A service used for event related tasks"""
  __slots__ = ()

  def __init__(self) -> None:
    """Initializes the event service"""
    pygame.key.set_repeat()
    pygame.key.stop_text_input()
    pygame.event.set_blocked([
        pygame.MOUSEMOTION,
        pygame.WINDOWLEAVE,
        pygame.WINDOWENTER,
        pygame.WINDOWFOCUSLOST,
        pygame.WINDOWFOCUSGAINED,
        pygame.WINDOWSHOWN,
        pygame.WINDOWCLOSE,
        pygame.ACTIVEEVENT,
        pygame.MOUSEBUTTONDOWN,
        pygame.MOUSEBUTTONUP,
        pygame.VIDEOEXPOSE,
        pygame.VIDEORESIZE,
        pygame.WINDOWEXPOSED,
        pygame.AUDIODEVICEADDED,
        pygame.AUDIODEVICEREMOVED
    ])
    # pygame.event.clear()

  def process_queue(self):
    """Main method which handles the event queue

    This method handles the event queue. It is intended to be so generic that
    it can be used in scpup as well as in other games, but work still in
    progress....
    """
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          return False
      elif event.type == pygame.JOYDEVICEADDED:
        j: pygame.joystick.Joystick = pygame.joystick.Joystick(event.device_index)
        scpup.EauCtrl.create(j)
      elif event.type == pygame.JOYDEVICEREMOVED:
        scpup.EauPlayer.remove_player(event.instance_id)
        scpup.EauCtrl.remove_ctrl(event.instance_id)
      elif event.type in [pygame.JOYAXISMOTION, pygame.JOYBUTTONDOWN]:
        player: scpup.EauPlayer | None = scpup.EauPlayer(event.instance_id)
        if player:
          if event.type == pygame.JOYAXISMOTION:
            player.handle_joystick_input(event.axis, event.value)
          else:
            player.handle_joystick_input(event.button)
        elif event.type == pygame.JOYBUTTONDOWN:
          ctrl = scpup.EauCtrl(event.instance_id)
          if ctrl.action(event.button) == scpup.EauAction.START:
            scpup.EauPlayer.create(with_ctrl=ctrl)
      elif event.type == EAU_EVENT:
        if event.subtype == EauEventSubtype.QUIT:
          return False
        elif event.subtype == EauEventSubtype.VIEW:
          if self.view:
            self.view.on(
              event_name=event.event_name,
              actioner=event.actioner,
              **(event.data if 'data' in event.__dict__ else {})
            )
        elif event.subtype == EauEventSubtype.NAV:
          EauService.set_view(event.to_view)
    return True

  @overload
  def post(
    self,
    subtype: Literal[EauEventSubtype.VIEW],
    *,
    event_name: str,
    actioner: scpup.EauSprite,
    data: dict[str, Any] = {}
  ):
    """Post an EAU_EVENT of VIEW subtype

    This method sends an event to the view so sprites can comunicate with it

    Args:
      event_name:
        The name of the event for the view to handle
    """
  @overload
  def post(self, subtype: Literal[EauEventSubtype.QUIT]):
    """Post en EAU_EVENT of QUIT subtype

    This method sends a quit event, and when received the game closes.
    """
  @overload
  def post(self, subtype: Literal[EauEventSubtype.NAV], *, to_view: str | scpup.EauView):
    """Post an EAU_EVENT of NAV subtype

    This method is used to navigate to another view

    Args:
      view_name:
        The name of the class or the class of the view to navigate to
    """
  def post(self, subtype: EauEventSubtype, **kwargs):
    ev = pygame.event.Event(EAU_EVENT, {
      "subtype": subtype,
      **kwargs
    })
    pygame.event.post(ev)


class EauAudioService(EauService):
  __slots__ = (
    "sfx",
    "bg",
    "soundsdict"
  )

  def __init__(self, *, bg_sound_path: str | None = None):
    """Initializes the audio service

    Args:
      bg_sound_path:
        The path segments of the background music, None means no background
        music. Defaults to None.
    """
    pygame.mixer.set_num_channels(6)
    self.bg = pygame.mixer.Channel(0)
    self.sfx = (
      pygame.mixer.Channel(1),
      pygame.mixer.Channel(2),
      pygame.mixer.Channel(3),
      pygame.mixer.Channel(4),
      pygame.mixer.Channel(5)
    )
    self.soundsdict: dict[str | int, pygame.mixer.Sound] = {}
    if bg_sound_path:
      self.load("background", bg_sound_path)

  def load(self, sound_id: str | int, *paths: str) -> bool:
    """Load a sound given its file path and store it

    Args:
      sound_id:
        The key of the saved sound
      path:
        The path segments of the sound. It has to be somewhere under
        `<root>/assets/sounds/`.

    Returns:
      bool:
        Whether the sound was loaded successfully or not
    """
    try:
      self.soundsdict[sound_id] = scpup.load_sound(*paths)
      return True
    except ValueError:
      return False

  def play(self, name: str | int) -> None:
    """Play a sound previously registered

    Args:
      name:
        The key that was used to store the sound
    """
    channel = next((c for c in self.sfx if c.get_queue() is None), None)
    if not channel or name not in self.soundsdict:
      return
    channel.play(self.soundsdict[name])

  def louder(self):
    ...

  def quiet(self):
    ...

  def toggle(self, channel: Literal['bg', 'sfx']):
    ...

  def pause(self):
    ...
