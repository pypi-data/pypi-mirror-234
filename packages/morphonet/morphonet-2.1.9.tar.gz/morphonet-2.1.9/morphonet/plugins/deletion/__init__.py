from .deleteSelectedObjects import *
from .removeUnder import *


# -*- coding: latin-1 -*-
defaultPlugins=[]

from .deleteSelectedObjects import DeleteSelectedObjects
defaultPlugins.append(DeleteSelectedObjects())

from .removeUnder import RemoveUnder
defaultPlugins.append(RemoveUnder())
