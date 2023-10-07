# -*- coding: latin-1 -*-
defaultPlugins=[]

from .Stardist import Stardist
defaultPlugins.append(Stardist())

from .temporal_seeds_on_background import TemporalSeedsOnBackground
defaultPlugins.append(TemporalSeedsOnBackground())

from .temporal_seeds_on_raw import TemporalSeedsOnRaw
defaultPlugins.append(TemporalSeedsOnRaw())

from .ShapePropagation import ShapePropagation
defaultPlugins.append(ShapePropagation())