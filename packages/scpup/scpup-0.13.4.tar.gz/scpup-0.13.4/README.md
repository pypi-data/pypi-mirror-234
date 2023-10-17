# AramEau - pyeau 

## SCPUP Description

Library for Super Crystal Pokebros Ultimate Party game. This library contains the SCPUP ABC and related python classes

This library is not meant to be used in other projects other than AramEau's SCPUP and maybe other games made by AramEau.
So, if for any reason you decide to use this library, it is at your own risk. Sorry but the aim of this library is to
acomplish a personal goal.

## Install

```bash
python -m pip install -U scpup
```

## Usage

Any exported member of any module within this package can be accessed from the root scope, for example:

```python
from scpup import EauSprite
class SomeSprite(EauSprite): ...
# or
import scpup
class SomeSprite(scpup.EauSprite): ...
# or
from scpup import sprite
class SomeSprite(sprite.EauSprite): ...
# or
from scpup.sprite import EauSprite
class SomeSprite(EauSprite): ...
```

> **_Note_**: Maybe this changes in the future so that not all modules are loaded when importing scpup, instead only the modules that will be used are loaded when importing them


## Modules

The following modules are available within the scpup package:

* services
  * Needed classes like EauDisplayService which handles all the display related stuff
* sprite
  * Base sprite classes
* group
  * Base group classes
* ctrl
  * Game controllers classes and mappings
* loader
  * Has functions for loading images, sounds, fonts, or whatever needs to be loaded
* view
  * Base view classes
* player
  * Utility module that helps handling players related stuff
* text
  * Classes for text and text groups

For more information on a module listed above, see its documentation.
