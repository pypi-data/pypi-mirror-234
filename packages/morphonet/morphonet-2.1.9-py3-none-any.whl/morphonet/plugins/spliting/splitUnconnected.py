# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np

from morphonet.tools import printv


class SplitUnconnected(MorphoPlugin):
    """ This plugin split unconnected objtes

    Parameters
    ----------
    Objects:
        It can be apply either on selected or colored objects
    Axis : Dropdown

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_name("Split mask for unconnected objects with same id")
        self.add_dropdown("Time points",["Current time","All times"])
        self.set_parent("Split objects")
        self.set_description("For a single or all time points, this plugins detects , for all objects, if they have "
                             "multiple parts that are not in contact. \n If multiple parts are detected, "
                             "all parts are split in new objects.")

    def split_unconnected_at(self, t,dataset,objects):
        import numpy as np
        from skimage.measure import label
        data = dataset.get_seg(t)  #Get segmentations at the time
        lastID = np.max(data) + 1 #new id = max of segmentation +1
        labels = label(data, background=dataset.background)  # #Labelize the segmentations FROM SKIMAGE
        cells_updated = []
        applied_change = False
        printv('Searching in all cells at : '+str(t),0)
        #For all objects in segmentation from morphonet
        for o in dataset.get_all_objects_at(t):
            #Get the ids generated sooner
            which_label = labels[data == o.id]
            #Get the differents  connected components
            ids, counts = np.unique(which_label, return_counts=True)
            #If we have 2 connected components
            if len(ids) > 1:  # CHECK IF ARRAY ARRAY
                printv('Found Object to split ' + str(o.get_name()) + " at " + str(t),0)
                #backup the first time we split
                if not applied_change:  applied_change = True
                #from all the connected components to split, the biggest will get the previous cell ids
                idx = np.where(counts == counts.max())
                id_cell = ids[idx][0]  # OK
                printv("Let's keep id : "+str(id_cell),1)
                #for each other connected components
                for other_cell in ids:
                    if other_cell != id_cell:
                        printv("We need to update cell with id : "+str(other_cell),1)
                        #Each component get a new id in the segmentation
                        data[labels == other_cell] = lastID
                        lastID += 1
                        printv('Create a new ID ' + str(lastID),0)
                        #cell to refresh
                        cells_updated.append(lastID)
                cells_updated.append(o.id)
        #If we changed a cell , write segmentation
        if len(cells_updated) > 0:
            dataset.set_seg(t, data, cells_updated=cells_updated)

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,objects_require=False):
            return None
        #Start the split for the sequence of times or the single times depending of user choice
        if str(self.get_dropdown("Time points")) == "All times":
            for i in range(self.dataset.begin, self.dataset.end + 1):
                self.split_unconnected_at(i,dataset,objects)
        else:
            self.split_unconnected_at(t,dataset,objects)
        self.restart()
