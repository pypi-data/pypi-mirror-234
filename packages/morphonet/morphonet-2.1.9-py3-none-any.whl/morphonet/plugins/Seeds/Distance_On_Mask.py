# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from skimage.feature import peak_local_max
import numpy as np
from scipy import ndimage as ndi
from ..functions import  get_borders
from ...tools import printv


class Distance_On_Mask(MorphoPlugin):
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
        self.set_name("Compute the peaks of the distance to the border of the selected mask")
        self.add_inputfield("Nb_Seeds", default=2)
        self.add_inputfield("Distance_Min", default=30)
        self.set_description( "This plugin generates seeds that can be used in other (mainly segmentation) algorithms "
                              "\n \n The maximal distance between points is computed, and this distance is split in N "
                              "segments, N being the number of seeds the user want. \n The different seeds are placed "
                              "at the contact point of the segments")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, backup=False):
            return None

        Nb_Seeds = int(self.get_inputfield("Nb_Seeds"))
        min_distance = int(self.get_inputfield("Distance_Min"))

        nbc = 0
        # For each time point in cells labeled
        for t in dataset.get_times(objects):
            data = dataset.get_seg(t)
            #For each cell to this time point
            for o in dataset.get_objects_at(objects, t):
                #Get the coordinates in the image
                cellCoords=dataset.np_where(o)
                printv('Look for object ' + str(o.get_name()) + " with " + str( len(cellCoords[0])) + " voxels ",0)
                #Get the bounding box of the ojects
                xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data, cellCoords)
                cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
                mask = np.zeros(cellShape, dtype=bool)
                mask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True
                #Get the array of distances to the background for each voxel
                distance = ndi.distance_transform_edt(mask)
                #Get the local maximas of this distances
                peak_idx = peak_local_max(distance, min_distance=min_distance, num_peaks=Nb_Seeds)
                #Add a seed to each maxima
                for i in range(len(peak_idx)):
                    cc=peak_idx[i]
                    coord = [cc[0] + xmin, cc[1] + ymin, cc[2] + zmin]
                    dataset.add_seed(coord)
                    nbc += 1
        #Restart to morphonet
        printv("Found " + str(nbc) + " new seeds",0)
        self.restart()

