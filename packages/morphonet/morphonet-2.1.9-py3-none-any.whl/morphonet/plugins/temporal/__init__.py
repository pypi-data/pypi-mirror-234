# -*- coding: latin-1 -*-
defaultPlugins=[]

from .addTemporalLink import AddTemporalLink
defaultPlugins.append(AddTemporalLink())

from .delTemporalLink import DelTemporalLink
defaultPlugins.append(DelTemporalLink())

from .overlaptracking import OverlapTracking
defaultPlugins.append(OverlapTracking())