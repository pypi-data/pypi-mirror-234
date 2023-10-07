# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np
from ..functions import  get_borders, apply_new_label,get_seed_at,get_seeds_in_mask,get_seeds_in_image,watershed,gaussian,get_barycenter
from ...tools import printv

class With_Mask_On_Raw(MorphoPlugin):
    """ This plugin perform a watershed algorithm on a segmented region with new seeds passed in parameters

    Parameters
    ----------
    Gaussian_Sigma : int, default :2
        sigma parameters from the gaussian algorithm (from skimage) aplied on the rawdata
    Volume_Minimum: int, default : 1000
        minimum volume under wichi new object are created
    Seeds: Coordinate List
        List of seeds added on the MorphoNet Window

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_name("Watershed segmentation on current masks using raw images")
        self.add_inputfield("Gaussian_Sigma", default=2)
        self.add_inputfield("Volume_Minimum", default=1000)
        self.add_coordinates("Add a Seed")
        self.set_parent("Segmentation from seeds")
        self.set_description("This plugins generate one or multiple new cells from seed generated or placed in "
                             "MorphoNet Viewer. \n The new cells are computed on the raw data image, after applying a smoothing , "
                             "for each seed that is in another object, inside its mask. \n If the generated objects are under the volume threshold defined "
                             "by the user, the object is not created.")

    # Perform a watershed on a list of seed
    def _water_on_seed(self, dataset, t, data, seeds, objects, rawdata):
        printv("perform watershed at " + str(t),1)
        cells_updated = []
        #For each object, get its coord
        for o in dataset.get_objects_at(objects,t):
            cellCoords = np.where(data == o.id)
            printv('Look in object ' + str(o.get_name()) + " with " + str(len(cellCoords[0])) + " voxels ",0)
            #compute bounding box and create a mask around it
            xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data, cellCoords)
            cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
            mask = np.zeros(cellShape, dtype=bool)
            mask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True


            #Get the seeds that are in the mask only
            nseeds = get_seed_at(seeds, xmin, ymin, zmin)
            seeds_in_cell_mask = get_seeds_in_mask(nseeds, mask)
            #We need 2 seeds at least to split a cell
            if len(seeds_in_cell_mask) < 2:  # If we have some seeds in this mask
                printv(str(len(seeds_in_cell_mask)) + "  is not enough  seeds in this mask",0)
            else:
                printv("Found " + str(len(seeds_in_cell_mask)) + " seeds in this mask",0)
                #Create markers (seed) images for watershed, with specific ids for each seed
                markers = np.zeros(mask.shape, dtype=np.uint16)
                newId = 1
                for seed in seeds_in_cell_mask:  # For Each Seeds ...
                    markers[seed[0], seed[1], seed[2]] = newId
                    newId += 1
                #Crop raw image around the box
                seed_preimage = rawdata[xmin:xmax + 1, ymin:ymax + 1, zmin:zmax + 1]
                #If we need to smooth, do it
                if self.s_sigma > 0.0:
                    printv("Perform gaussian with sigma=" + str(self.s_sigma) + " at " + str(t),0)
                    seed_preimage = gaussian(seed_preimage, sigma=self.s_sigma, preserve_range=True)
                # apply watershed on mask from seeds, using raw images as source
                printv(" --> Process watershed ",0)
                labelw = watershed(seed_preimage, markers=markers, mask=mask)
                #Apply the labels to the segmentations , if volume is ok
                data, c_newIds = apply_new_label(data, xmin, ymin, zmin, labelw, minVol=self.min_vol)
                #if we created new cells, add them to refresh in morphonet
                if len(c_newIds) > 0:
                    c_newIds.append(o.id)
                    cells_updated += c_newIds

        if len(cells_updated) > 0:
            # Set segmentation in MorphoNet
            dataset.set_seg(t, data, cells_updated=cells_updated)
            #Compute seeds from the new cells barycenter, for next time points
            new_seeds=[]
            for c in cells_updated:
                new_seeds.append(get_barycenter(data,c))
            return new_seeds
        return []

    def _water_time(self, dataset, t, seeds, objects):
        #Get the segmentation at t
        data = dataset.get_seg(t)
        #Get the raw data at t
        rawdata = dataset.get_raw(t)
        if rawdata is None:
            return
        #Apply watershed and get the new cells barycenters as next seeds
        new_seeds = self._water_on_seed(dataset, t, data, seeds, objects, rawdata)
        #Continue if we're in the time is in working times, and that we generated seeds
        if len(new_seeds) > 0 and t+1 in self.times:
            self._water_time(dataset, t + 1, new_seeds, objects)


    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects):
            return None
        # Get the value of the smoothing  from morphonet
        self.s_sigma = int(self.get_inputfield("Gaussian_Sigma"))
        #Get the min volume for cell to create from morphonet
        self.min_vol = int(self.get_inputfield("Volume_Minimum"))
        #get the seeds position from morphonet
        seeds = self.get_coordinates("Add a Seed")
        #If no seeds, nothing to do
        if len(seeds) == 0:
            printv("no seeds for watershed",0)
        #Else propagate watershed in time from seeds
        else:
            printv("Found " + str(len(seeds)) + " seeds ",0)
            seeds=get_seeds_in_image(dataset,seeds)
            self.times=dataset.get_times(objects)
            self._water_time(dataset, self.times[0], seeds, objects)
        self.restart()




