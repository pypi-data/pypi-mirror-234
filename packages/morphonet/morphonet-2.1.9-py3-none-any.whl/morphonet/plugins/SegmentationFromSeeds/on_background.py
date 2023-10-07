# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np
from ..functions import _centerInShape, get_seeds_in_image, watershed
from ...tools import printv


class On_Background(MorphoPlugin):
    """ This plugin perform a watershed algorithm on the background of the image based on seeds pass in parameters

    Parameters
    ----------
    Gaussian_Sigma : int, default :2
        sigma parameters from the gaussian algorithm (from skimage) aplied on the rawdata
    Volume_Minimum: int, default : 1000
        minimum volume under wichi new object are created
    Inverse: Dropdown
        applied the watershed on inverted rawdata (for image on black or white background)
    Seeds: Coordinate List
        List of seeds added on the MorphoNet Window

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_name("Watershed segmentation on missing masks")
        self.add_inputfield("Volume Minimum", default=1000)
        self.add_inputfield("Box size", default=50)
        self.add_coordinates("Add a Seed")
        self.set_parent("Segmentation from seeds")
        self.set_description("This plugins generate one or multiple new cells from seed generated or placed in "
                             "MorphoNet Viewer. \n The new cells are computed on the segmentation image , "
                             "for each seed that is not in another object, inside a box defined by the 'box size' "
                             "parameter (in voxels). If the generated objects are under the volume threshold defined "
                             "by the user, the object is not created.")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None
        # User chosen min volume accepted as a cell to segment
        min_vol = int(self.get_inputfield("Volume Minimum"))
        # Size of the bounding box around to work around the seeds
        box_size = int(self.get_inputfield("Box size"))

        # Load segmentation in memory
        data = dataset.get_seg(t)
        # Get list of seeds coordinates from MorphoNet seed system
        seeds = self.get_coordinates("Add a Seed")
        if len(seeds) == 0:
            printv("no seeds for watershed", 0)
            return None
        printv("Found " + str(len(seeds)) + " seeds ", 1)
        # Compute center of the segmentation
        dataset.get_center(data)
        # Get coordinates of the seeds in the image (coordinates in morphonet != coordinates in images)
        seeds = get_seeds_in_image(dataset, seeds)
        new_seed = []
        # For each seed
        for seed in seeds:
            # if seed is in image
            if _centerInShape(seed, data.shape):
                # Get the cell id at the seed
                olid = data[seed[0], seed[1], seed[2]]
                # if it's background , it will be used for segmentation
                if olid == dataset.background:
                    new_seed.append(seed)
                    printv("add seed " + str(seed), 1)
                # else we skip it
                else:
                    printv("remove this seed " + str(seed) + " which already correspond to cell " + str(olid), 1)
            else:
                printv("this seed " + str(seed) + " is out of the image", 1)

        # If no seed found, we can stop
        if len(new_seed) == 0:
            self.restart()
            return None

        # Compute a box around the seed, according to the box size given by user
        if box_size > 0:
            seedsa = np.array(new_seed)
            box_coords = {}
            for i in range(3):
                mi = max(0, seedsa[:, i].min() - box_size)
                ma = min(data.shape[i], seedsa[:, i].max() + box_size)
                box_coords[i] = [mi, ma]

            # Crop the data around the box
            ndata = data[box_coords[0][0]:box_coords[0][1], box_coords[1][0]:box_coords[1][1],
                    box_coords[2][0]:box_coords[2][1]]

            # Replace the seed in the box
            box_seed = []
            for s in new_seed:
                box_seed.append([s[0] - box_coords[0][0], s[1] - box_coords[1][0], s[2] - box_coords[2][0]])
            new_seed = box_seed
        else:
            ndata = data

        # mark the box sides with background in the mask image
        markers = np.zeros(ndata.shape, dtype=np.uint16)
        markers[0, :, :] = 1
        markers[:, 0, :] = 1
        markers[:, :, 0] = 1
        markers[ndata.shape[0] - 1, :, :] = 1
        markers[:, ndata.shape[1] - 1, :] = 1
        markers[:, :, ndata.shape[2] - 1] = 1

        # Mark the seeds in the mask image with a separate id for each
        newId = 2
        for seed in new_seed:
            markers[seed[0], seed[1], seed[2]] = newId
            newId += 1

        # Create a new mask images, , with background at true
        mask = np.ones(ndata.shape, dtype=bool)
        mask[ndata != dataset.background] = False

        #watershed from seeds
        printv("Process watershed with " + str(len(new_seed)) + " seeds", 0)
        labelw = watershed(mask, markers=markers, mask=mask)

        #Compute the identifiers of the cells created during watershed
        cMax = data.max() + 1
        nbc = 0
        new_ids = np.unique(labelw)
        #Do not create cells at the bounding box borders
        new_ids = new_ids[new_ids > 1]
        # If we created an object
        if len(new_ids) > 0:
            printv("Combine new objects", 1)
            cells_updated = []
            #For each id of cell created by watershed
            for new_id in new_ids:
                #Get its coordinates
                newIdCoord = np.where(labelw == new_id)
                #If the cell is big enough compared to user volume threshold
                if len(newIdCoord[0]) > min_vol:
                    #Get the cell coord in the segmentation image
                    if box_size > 0:
                        newIdCoord = (newIdCoord[0] + box_coords[0][0], newIdCoord[1] + box_coords[1][0],
                                      newIdCoord[2] + box_coords[2][0])
                    #Mark it as the next id in the images
                    data[newIdCoord] = cMax + nbc
                    printv("add object " + str(nbc + cMax) + ' with  ' + str(len(newIdCoord[0])) + " voxels", 0)
                    #Add cell to refresh in morphonet
                    cells_updated.append(cMax + nbc)
                    nbc += 1
                else:
                    printv("remove object with  " + str(len(newIdCoord[0])) + " voxels", 0)
            #Save segmentation
            if len(cells_updated) > 0:
                dataset.set_seg(t, data, cells_updated=cells_updated)
        printv(" --> Found  " + str(nbc) + " new labels", 0)
        #Send data to MorphoNet
        self.restart()
