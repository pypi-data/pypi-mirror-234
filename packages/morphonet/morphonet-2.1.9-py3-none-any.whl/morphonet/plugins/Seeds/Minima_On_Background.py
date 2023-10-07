# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from skimage.morphology import extrema
from skimage.filters import gaussian
from skimage.measure import label
import numpy as np
from ...tools import printv


class Minima_On_Background(MorphoPlugin):
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
        self.set_name("Create seeds on local minium intensity from the raw images on empty area")
        self.add_inputfield("Gaussian_Sigma", default=8)
        self.add_dropdown("Method", ["H Minima", "Local Minima"])
        self.add_inputfield("h_value", default=2)
        self.set_description( "This plugin generates seeds that can be used in other (mainly segmentation) algorithms "
                              "\n \n This plugin uses the Raw Images (where user can apply a smoothing before "
                              "execution) to compute the minimas of the segmentation image using one of the following "
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
        method = self.get_dropdown("Method")

        nbc = 0
        #Load segmentation data in memory
        data = dataset.get_seg(t)
        #Load raw image data in memory
        rawdata = dataset.get_raw(t)

        # If user wants to smooth
        if s_sigma > 0.0:  # Smoothing
            printv("Perform gaussian with sigma=" + str(s_sigma),0)
            rawdata = gaussian(rawdata, sigma=s_sigma, preserve_range=True)

        # Compute the minimas depending on the method
        if method == "H Minima":
            local = extrema.h_minima(rawdata, h_value)
        if method == "Local Minima":
            local = extrema.local_minima(rawdata)


        printv("Perform  labelisation",0)
        #Get the labels of the local minimas in the segmentation
        label_maxima, nbElts = label(local, return_num=True)
        if nbElts > 100:
            printv("Found too many seeds : " + str(nbElts),0)
        else:
            #For each local minima found
            for elt in range(1, nbElts + 1):
                #Get the coordinate of the local minima
                coord = np.where(label_maxima == elt)
                v = dataset.background
                #If segmentation is loaded , check if the minima is inside a cell
                if data is not None:
                    v = data[coord[0][0], coord[1][0], coord[2][0]]
                #If minima is not a cell , add seed to morphonet
                if v == dataset.background:
                    dataset.add_seed([coord[0][0], coord[1][0], coord[2][0]])
                    nbc += 1

            printv("Found " + str(nbc) + " new seeds",0)
        #Send data back to morphonet
        self.restart()

