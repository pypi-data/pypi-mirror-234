# -*- coding: latin-1 -*-
import skimage.transform

from morphonet.plugins import MorphoPlugin
import numpy as np
from ...tools import printv,imsave


class Stardist(MorphoPlugin):
    """ This plugin perform the stardist algorithm to segment nulcei
    https://github.com/stardist/stardist

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
        self.set_name("Stardist")
        self.add_inputfield("Downsampled", default=2)
        self.set_parent("Segmentation")
        self.set_description( "This plugin use a raw image of nucleus from a MorphoNet local dataset at a spercific "
                              "time point, to compute a segmentation of the nucleus, using the Stardist deep learning"
                              " algorithm.")

    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        from csbdeep.utils import normalize
        from stardist.models import StarDist3D
        from skimage.transform import resize

        Downsampled = int(self.get_inputfield("Downsampled"))

        rawdata = dataset.get_raw(t)
        cancel=False
        if rawdata is None:
            printv("please specify the rawdata",0)
            cancel=True
        else:
            data = np.zeros(rawdata.shape).astype(np.uint16)
            init_shape = rawdata.shape
            if Downsampled>1: rawdata=rawdata[::Downsampled,::Downsampled,::Downsampled]

            printv("normalize the rawdata",0)
            rawdata = normalize(rawdata)
            printv("load the stardist 3D model",0)
            model = StarDist3D.from_pretrained('3D_demo')

            printv("predict the nuclei",0)
            data, _ = model.predict_instances(rawdata)

            #imsave("/Users/bgallean/Desktop/test.nii",data,voxel_size=dataset.get_voxel_size(t))

            #data = data.swapaxes(0, 2)
            if Downsampled > 1:  data = resize(data,init_shape,preserve_range=True,order=0)
            #imsave("/Users/bgallean/Desktop/test2.nii",data,voxel_size=dataset.get_voxel_size(t))

            dataset.set_seg(t, data) #send factor of decimation here
        self.restart(cancel=cancel)




