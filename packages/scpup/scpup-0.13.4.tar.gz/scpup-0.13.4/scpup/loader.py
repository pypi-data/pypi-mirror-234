"""SCPUP loader module

This module has all the functions needed to load files.
"""

from __future__ import annotations
import os
import scpup
import pygame
import importlib

__all__ = [
  "load_image",
  "load_sound",
  "BASE_PATH"
]

BASE_PATH = os.path.join(os.getcwd(), "assets")


def load_image(
  *paths: str,
  alpha=True,
  position: scpup.EauPosition | None = None
) -> tuple[pygame.Surface, pygame.Rect]:
  """Loads an image located somewhere in <root>/assets/images/...

  Args:
    *paths: The path segments of where the image file exists.
    alpha:
      Whether the image should convert pixel format considering transparency or
      not. Defaults to True.
    position: The rectangle position as an EauPosition object

  Raises:
    ValueError: The given image path does not exist.

  Returns:
    tuple[pygame.Surface, pygame.Rect]:
      The image as a pygame.Surface and the covering rectangle of that image.
  """
  path = os.path.join(BASE_PATH, "images", *paths)
  if not os.path.exists(path):
    raise ValueError(f"Path: '{path}' does not exist")
  image = pygame.image.load(path)
  if alpha:
    image = image.convert_alpha()
  else:
    image = image.convert()
  rect = image.get_rect(**(position.as_rectargs() if position else {}))
  return image, rect


def load_sound(*paths: str) -> pygame.mixer.Sound:
  """Loads a sound file located somewhere in <root>/assets/sounds...

  Args:
    *paths: The path segments of where the sound file exists

  Raises:
    ValueError: The given sound path does not exist.

  Returns:
    pygame.mixer.Sound: The loaded sound.
  """
  path: str = os.path.join(BASE_PATH, "sounds", *paths)
  if not os.path.exists(path):
    raise ValueError(f"Path: '{path}' does not exist")
  sound = pygame.mixer.Sound(path)
  return sound


def load_package(package_path: str) -> None:
  """This function imports all python files recursively in a directory

  This function is only meant to be used in the `scpup.init` function, and it's
  needed because by importing all python files in a directory, scpup can be
  aware of the EauView and EauSprite subclasses

  Args:
    package_path: The path of the directory to load
  """
  if os.path.exists(package_path) and os.path.isdir(package_path):
    for f in os.listdir(package_path):
      if '__init__' not in f and '__pycache__' not in f:
        path = os.path.join(package_path, f)
        if os.path.isdir(path) and '__pycache__' not in path:
          load_package(path)
        elif f.endswith('.py'):
          importlib.import_module(f"{package_path.lstrip(' ./').replace('/', '.')}.{f.removesuffix('.py')}")
