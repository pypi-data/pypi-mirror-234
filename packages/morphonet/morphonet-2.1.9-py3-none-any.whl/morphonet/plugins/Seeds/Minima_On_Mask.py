# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from skimage.morphology import extrema, binary_dilation
from skimage.filters import gaussian
from skimage.measure import label
import numpy as np
from ..functions import shift_bbox
from ...tools import printv


class Minima_On_Mask(MorphoPlugin):
    """ This plugin create new seeds from a h min (or max) algorithm on the rawdata image
  If objects are selected, the function will be applied only on their mask
    If not, the function will be applied everywhere else there is no objects

    Parameters
    ----------
    Gaussian_Sigma : int, default :8
        sigma parameters from the gaussian algorithm (from skimage) applied on the rawdata in otder to perform the h minimum or maximum algorithm
    h_value : int, default :2
        the h value of h_minima or h_maxumum algorithm (see https://scikit-image.org/docs/stable/api/skimage.morphology.html )

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_parent("Create Seeds")
        self.set_name("Create seeds on local minium intensity from the raw images on the selected mask")
        self.add_inputfield("Gaussian_Sigma", default=8)
        self.add_dropdown("Method", ["H Minima", "Local Minima"])
        self.add_inputfield("h_value", default=2)
        self.set_description( "This plugin generates seeds that can be used in other (mainly segmentation) algorithms. User have to select (or label) to generate seeds "
                              "\n \n This plugin uses the Raw Images (where user can apply a smoothing before "
                              "execution) to compute the minimas inside a mask (object) of the segmentation image using one of the following "
                              "methods : \n \n - H Minima \n -Local minima \n \n Seeds are generated at the minimas "
                              "where no segmentation values are found (in the background) ")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, backup=False):
            return None
        # Value of the smoothing user want to apply on raw data to find the seeds
        s_sigma = int(self.get_inputfield("Gaussian_Sigma"))
        #Minimal depths of the minima to find in the image , if using H Minima method
        h_value = float(self.get_inputfield("h_value"))
        # h-minima or local minima
        method=self.get_dropdown("Method")

        nbc = 0
        # For eahc time point in the labeled objects
        for t in dataset.get_times(objects):
            #Load segmentation data in memory
            data = dataset.get_seg(t)
            #Load raw data in memory
            rawdata = dataset.get_raw(t)
            #If we didn't find any raw data, no need to continue
            if rawdata is None:
                break
            # Get the maximum intensity in rawdata
            maxi = np.max(rawdata)
            # For each labeled cells in this time point
            for o in dataset.get_objects_at(objects, t):
                #Get the bounding box using scikit property
                xmin, xmax, ymin, ymax, zmin, zmax  = shift_bbox(dataset.get_property("bbox",o),shape=data.shape)
                #Get the cell volume property
                volume=dataset.get_property("area",o)
                printv('Look for object ' + str(o.get_name()) + " with " + str(volume) + " voxels ",0)
                # If user wants to smooth
                if s_sigma > 0.0:  # Smoothing
                    printv("Perform gaussian with sigma=" + str(s_sigma),0)
                    #Get the mask after smoothing
                    raw_mask = gaussian(rawdata[xmin:xmax + 1, ymin:ymax + 1, zmin:zmax + 1], sigma=s_sigma,preserve_range=True)
                else:
                    #Get the mask
                    raw_mask = rawdata[xmin:xmax + 1, ymin:ymax + 1, zmin:zmax + 1]
                # Get the data of the mask
                data_cell = data[xmin:xmax + 1, ymin:ymax + 1, zmin:zmax + 1]
                #Get the a boolean matrix  : True = voxels at border (other cell or background) , False = voxels in the cell
                data_cell = data_cell != o.id  # Convert in Bool
                #Dilate the border
                data_cell = binary_dilation(binary_dilation(data_cell))  # dilate to avoid seeds at the border
                #Max of the cell has high intensity
                raw_mask[data_cell] = maxi  # Create a Mask with high intensity

                # Compute the minimas depending on the method
                if method=="H Minima":
                    local = extrema.h_minima(raw_mask, h_value)
                if method=="Local Minima":
                    local = extrema.local_minima(raw_mask)

                printv("Perform labelisation",0)
                # Get the labels of the local minimas in the segmentation
                label_maxima, nbElts = label(local, return_num=True)
                if nbElts>100:
                    printv("Found too much seeds : "+str(nbElts)+" Please, change parameters ",1)
                else:
                    # For each local minima found
                    for elt in range(1, nbElts + 1):
                        #Get the coordinate of seed in image
                        coord = np.where(label_maxima == elt)
                        coord = [coord[0][0] + xmin, coord[1][0] + ymin, coord[2][0] + zmin]
                        #If the coordinate correspond to a voxel of the cell , create seed
                        if data[coord[0], coord[1], coord[2]] == o.id:
                            dataset.add_seed(coord)
                            nbc += 1
                        else:
                            #Else do nothing for this minima
                            printv("Seed out of mask at " + str(coord[0]) + "," + str(coord[1]) + "," + str(coord[2]),1)

        printv(" --> Found " + str(nbc) + " new seeds",0)
        #Send back data to MorphoNet
        self.restart()

