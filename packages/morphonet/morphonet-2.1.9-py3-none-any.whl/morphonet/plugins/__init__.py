# -*- coding: latin-1 -*-
from .MorphoPlugin import MorphoPlugin
__all__ = [
    'MorphoPlugin'
]

#from functions import  get_borders

defaultPlugins=[]

from .deletion import defaultPlugins as DP
defaultPlugins+=DP

from .Seeds import defaultPlugins as DP
defaultPlugins+=DP

from .Segmentation import defaultPlugins as DP
defaultPlugins+=DP

from .SegmentationFromSeeds import defaultPlugins as DP
defaultPlugins+=DP

from .ShapeTransform import defaultPlugins as DM
defaultPlugins+=DM

from .spliting import defaultPlugins as DP
defaultPlugins+=DP

from .temporal import defaultPlugins as DP
defaultPlugins+=DP


