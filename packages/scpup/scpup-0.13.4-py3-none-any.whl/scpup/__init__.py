"""scpup package contains the classes, constants, types, etc., needed in the
game SCPUP (Super Crystal Pokebros Ultimate Party) and any other AramEau game.

This package exports all modules so that importing them is easier.

This package also exports a function called `init` that has to be executed
before using any scpup module.
"""

from __future__ import annotations

from .services import EauService, EauEventSubtype  # noqa
from .text import *  # noqa
from .loader import *  # noqa
from .sprite import *  # noqa
from .group import *  # noqa
from .view import *  # noqa
from .player import *  # noqa
from .ctrl import *  # noqa
from .position import *  # noqa

__name__ = "scpup"
__package__ = "scpup"


def init(
  *,
  initial_view_name: str,
  font_path: str | None = None,
  window_size: tuple[int, int] = (1200, 800),
  caption: str | None = None,
  icon_path: str | None = None,
  background_music_path: str | None = None,
  views_path: str = "./src/views",
  sprites_path: str = "./src/sprites"
):
  import pygame
  from .services import EauDisplayService, EauEventService, EauAudioService
  from .text import EauText
  from .loader import load_package

  load_package(views_path)
  load_package(sprites_path)

  EauText.set_font(font_path)

  pygame.init()

  EauDisplayService(size=window_size, caption=caption, icon_path=icon_path)
  EauEventService()
  EauAudioService(bg_sound_path=background_music_path)

  EauService.set_view(initial_view_name)
