# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np

from morphonet.tools import printv, imsave


class RemoveUnder(MorphoPlugin):
    """ This plugin remove opbjects under a certain volume in the segmented image

    Parameters
    ----------
    Voxel Size: int, default 20
        The volume under which objecs as to be remove
    """

    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_parent("Remove objects")
        self.set_name("Delete selected objects below a certain size")
        self.add_inputfield("Voxel Size",default=50)
        self.add_dropdown("Time points",["Current time","All times"])
        self.add_dropdown("Association",["Closest object","Background"])
        self.set_description("This plugin remove all cells that are under a certain volume (in voxel) from the imagse and the "
                             "properties. \n User can choose between : \n \n - Deleting by applying the background value "
                             "to the cell \n - Fuse the cell to remove with the object sharing the most surface in "
                             "contact (can be background) \n \n User can also choose to apply the plugin for a single time point or the whole time sequence")

    def remove_under_at(self,t, dataset, associated,voxel_size):
        from scipy.ndimage.morphology import binary_dilation
        data = dataset.get_seg(t) #Read the data (if not in memory)

        cell_volume=dataset.get_regionprop_at("area",t,ordered=True) # Find the volume of the cell , using scikit properties
        cell_updated = []
        applied_change=False

        for cell in cell_volume: #Loop on all cells existing in the lineage

            if cell_volume[cell] < voxel_size: #if we detect a cell with a small size
                if not applied_change:
                    applied_change=True
                printv("delete object " + str(cell.id) + " at " + str(cell.t) + " with " + str(int(round(cell_volume[cell]))) + " voxels",0)

                id_cell = dataset.background #if not closes object, will be background

                if associated =="Closest object":  #If user specified closest object
                    #Find the cell borders
                    data_cell=dataset.get_mask_cell(cell,border=5)
                    mask_cell = np.zeros_like(data_cell).astype(np.uint8)
                    mask_cell[data_cell==cell.id] = 1

                    dilate_mask = binary_dilation(mask_cell).astype(np.uint8) # dilate the cell borders to get the identifiers of voxels around
                    dilate_mask = np.logical_xor(dilate_mask, mask_cell)
                    id_pixels = data_cell[dilate_mask == 1]
                    ids, counts = np.unique(id_pixels, return_counts=True)

                    idx = np.where(counts == counts.max()) # Find the one with the most contact
                    id_cell = ids[idx][0]

                    printv("fuse object " + str(cell.id) + " at " + str(cell.t) + " with " + str(
                        int(round(cell_volume[cell]))) + " voxels with "+str(id_cell), 0) # Small cell get this neighbor identifier now (can be background)
                else:   #Else , id_cell become background
                    printv("delete object " + str(cell.id) + " at " + str(cell.t) + " with " + str(int(round(cell_volume[cell]))) + " voxels", 0)

                dataset.set_cell_value(cell,id_cell) #Update the cell value in image and morphonet

                for m in cell.mothers: #Destroy the links in the lineage of the old cell
                    dataset.del_mother(cell, m)
                for d in cell.daughters:
                    dataset.del_daughter(cell, d)
                dataset.del_cell_from_properties(cell)
                cell_updated.append(cell.id) #List of cells that have been updated by the delete
        #If the code updated one cell, store the segmentation in morphonet, and recompute everything
        if len(cell_updated) > 0:
            dataset.set_seg(t, data, cells_updated=cell_updated)


    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,objects_require=False):
            return None

        # Get user choice on association , the closest object = the neighbor with most contact, else background
        associated=str(self.get_dropdown("Association"))

        voxel_size=float(self.get_inputfield("Voxel Size"))#Minimum voxel size considered as an object

        if str(self.get_dropdown("Time points")) == "All times": #should we process at current time or all times
            for i in range(self.dataset.begin,self.dataset.end+1):
                self.remove_under_at(i, dataset,associated, voxel_size)
        else:
            self.remove_under_at(t,dataset, associated, voxel_size)

        self.restart() #Send new data and properties to MorphoNet
