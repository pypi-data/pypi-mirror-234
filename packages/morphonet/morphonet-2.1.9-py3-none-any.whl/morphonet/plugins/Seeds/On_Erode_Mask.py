# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ..functions import  get_borders
from ...tools import printv


class On_Erode_Mask(MorphoPlugin):
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
        self.set_name("Create seeds from mask erosion")
        self.add_inputfield("Iteration", default=2)
        self.add_inputfield("Volume_Minimum", default=1000)
        self.set_description( "This plugin generates seeds that can be used in other (mainly segmentation) algorithms "
                              "\n \n This plugin applies multiple erosions step of each labeled (or selected) objects "
                              "on MorphoNet, until object is split in multiple parts. \n A seed is than generated at "
                              "the barycenter of each part computed. ")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects,backup=False):
            return None

        from skimage.morphology import binary_erosion
        from skimage.measure import label

        # Number of erosion interation
        iteration = int(self.get_inputfield("Iteration"))
        #Treshold of volume of cells to consider ok to get a seed
        min_vol = int(self.get_inputfield("Volume_Minimum"))
        import numpy as np
        nbc = 0
        #For each time points in the labeled cells
        for t in dataset.get_times(objects):
            #Load the segmentation data
            data = dataset.get_seg(t)
            #For each cell
            for o in dataset.get_objects_at(objects, t):
                #Get cells coordinate
                cellCoords = dataset.np_where(o)
                #compute a mask around the cell
                printv('Look for object ' + str(o.get_name()) + " with " + str(len(cellCoords[0])) + " voxels ",0)
                xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data, cellCoords)
                cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
                omask = np.zeros(cellShape, dtype=bool)
                omask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True
                mask = np.copy(omask)
                #apply the erosion iteration on the mask
                for n in range(iteration):
                    mask = binary_erosion(mask)
                #Determine the number of shards the cells has been split into due to erosion
                splitted = label(mask)
                new_objects = np.unique(splitted)
                #Get the list of cell shards except background
                new_objects = new_objects[new_objects != dataset.background]
                nbc = 0
                #If the cell has been split at least in 2
                if len(new_objects)>=2:
                    #For each shard
                    for no in new_objects:
                        #Get its coordinates
                        coords = np.where(splitted == no)
                        #If it's too small depending on the treshold , do not create a seed
                        if len(coords[0]) <= min_vol:
                            printv("found a small cell with  only " + str(len(coords[0])) + " voxels",0)
                        else:
                            printv("add a cell with " + str(len(coords[0])) + " voxels",0)
                            #Get cell barycenter
                            cc = np.uint16([coords[0].mean(), coords[1].mean(), coords[2].mean()])
                            #Add seed at this barycenter point
                            dataset.add_seed(cc)
                            nbc += 1
                #If didn't find two shards big enough to get a seed, warn the user
                if nbc <= 2:
                    printv("not splittable with this erosion iteration value " + str(iteration),0)
        #Send back to morphonet
        printv("Found " + str(nbc) + " new seeds",0)
        self.restart()

