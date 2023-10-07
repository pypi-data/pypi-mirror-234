# -*- coding: latin-1 -*-
defaultPlugins=[]

from .splitOnAxis import SplitOnAxis
defaultPlugins.append(SplitOnAxis())

from .splitUnconnected import SplitUnconnected
defaultPlugins.append(SplitUnconnected())

from .GaussianMixture import GaussianMixture
defaultPlugins.append(GaussianMixture())