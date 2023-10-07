
# -*- coding: latin-1 -*-
defaultPlugins=[]

from .fuseSelectedObjects import FuseSelectedObjects
defaultPlugins.append(FuseSelectedObjects())

from .Mesh_Deformation import MeshDeformation
defaultPlugins.append(MeshDeformation())

