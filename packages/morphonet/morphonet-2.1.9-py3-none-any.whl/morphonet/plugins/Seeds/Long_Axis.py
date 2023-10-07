# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class Long_Axis(MorphoPlugin):
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
        self.set_name("Create seeds on the long axis of the selected mask")
        self.add_inputfield("factor", default=8)
        self.set_description( "This plugin generates seeds that can be used in other (mainly segmentation) algorithms "
                              "\n \n The longest axis of the segmentation is computed, and this axis is split in 2 , "
                              "at 1/3 and 2/3 of the axis distance. \n These 2 positions are the positions of the new "
                              "generated seeds")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, backup=False):
            return None
        #Get user elongation factor for the long axis found, for the seed positioning
        factor = int(self.get_inputfield("factor"))
        import numpy as np
        from scipy.spatial.distance import cdist
        nbc = 0
        # For each time point in cells labeled
        for t in dataset.get_times(objects):
            #Forces to load the segmentation in memory
            data = dataset.get_seg(t)
            # For each cell to this time point
            for o in dataset.get_objects_at(objects, t):
                #Get the cell coordinates
                coords =dataset.np_where(o)
                printv('ook for object ' + str(o.get_name()) + " with " + str(factor*len(coords[0])) + " voxels ",0)
                vT = np.zeros([len(coords[0]), len(coords)])
                #Create distance matrix for each axis
                for s in range(len(coords)):
                    vT[:, s] = coords[s]
                #Compute distance matrix of the image
                dist = cdist(vT, vT)
                #Get the maximum distance from the matrix
                maxi = dist.max()
                #Find the corresponding coordinates
                coords_maxi = np.where(dist == maxi)
                if len(coords_maxi[0]) >= 2:
                    ipt1 = coords_maxi[0][0]
                    ipt2 = coords_maxi[0][1]
                    #Get the this long distance according to the factor of elongation
                    pt1 = np.array([coords[0][ipt1], coords[1][ipt1], coords[2][ipt1]])*factor
                    pt2 = np.array([coords[0][ipt2], coords[1][ipt2], coords[2][ipt2]])*factor
                    v = pt2 - pt1
                    #Compute seed along the axis , at 1/3 and 2/3 of the distance
                    seed1 = np.int32(pt1 + v * 1.0 / 3.0)
                    seed2 = np.int32(pt1 + v * 2.0 / 3.0)
                    #add the seeds to MorphoNet
                    for seed in [seed1,seed2]:
                        dataset.add_seed(seed)
                        nbc += 1

        printv(" --> Found " + str(nbc) + " new seeds",0)
        #Send the new data to MorphoNet
        self.restart()

