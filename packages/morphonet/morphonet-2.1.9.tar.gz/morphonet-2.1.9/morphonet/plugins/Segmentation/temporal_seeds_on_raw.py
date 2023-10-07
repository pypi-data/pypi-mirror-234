# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ...tools import printv
from .seed_propagation_lib  import get_list_of_selections,process_propagation_for_selection
def remove_background(value,background):
    if value == background:
          return False

    return True

def get_coords_indexes_in_image(image,list_ids):
    import numpy as np
    coordstemp = []
    result = np.where(image==list_ids[0])
    i = 0
    for cell in list_ids:
        if i > 0:
            result = np.concatenate((result,np.where(image==cell)),axis=1)
        i += 1
    return result
class TemporalSeedsOnRaw(MorphoPlugin):
    """ "TEMPORAL PROPAGATE BARYCENTER". On part d'un pas de temps ou on est content de la segmentation d'une/des cellule(s). On propage en forward et/ou en backward le barycentre pour soit i) spliter une cellule sous-segmentée qui contient deux barycentres (dans un premier temps le watershed sera basé uniquement sur le masque) , soit ii) créer une cellule quand le barycentre propagé est dans le background (taille de la boite ?).


    Parameters
    ----------
    Objects:
        It can be apply either on selected or colored objects
    Axis : Dropdown

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_name("Propagate objects as seeds on empty area of the next time step")
        self.add_dropdown("Direction",["Forward","Backward"])
        self.add_inputfield("Volume_Minimum", default=1000)
        self.add_inputfield("Gaussian_Sigma", default=2)
        self.set_parent("Segmentation")
        self.set_description( "This plugin propagates the segmentation of existing objects through times. User "
                              "labelizes the object to propagate, and than the corresponding cells (to split or to "
                              "create) on a time range. \n The plugin can be executed Forward (the 'source' cells are "
                              "at the beginning of the time range) or Backward (the 'source' cells are at the end of "
                              "the time range) \n \n. The 'source' cells barycenters are used as seeds for the next "
                              "point time point segmentation (watershed algorithm , using the raw images associated) "
                              ".\n The cells created are the source of the next time point segmentation, "
                              "until the end of the time range.")


    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        #Minimum volume of the cell created by the propagation
        self.min_vol = int(self.get_inputfield("Volume_Minimum"))
        #value of the gaussian sigma to apply to the raw data (0 = no smoothing)
        self.s_sigma = int(self.get_inputfield("Gaussian_Sigma"))

        printv("Propagation of " + str(len(objects)) + " objects", 0)

        # List Objects by selections , to work on each selection one by ones
        selections = get_list_of_selections(dataset,objects)

        new_label = ""
        # Get user direction chosen
        forward = (str(self.get_dropdown("Direction")) == "Forward")
        # For each selection found
        for s in selections:
            new_label += process_propagation_for_selection(selections,s,dataset,forward,self.min_vol,use_raw_images=True,sigma=self.s_sigma)
        # Send back data to MorphoNet
        self.restart(label=new_label)





