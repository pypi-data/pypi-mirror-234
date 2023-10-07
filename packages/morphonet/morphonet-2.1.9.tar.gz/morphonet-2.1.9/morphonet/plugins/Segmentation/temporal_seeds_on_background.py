# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ...tools import printv
from .seed_propagation_lib import get_list_of_selections,process_propagation_for_selection



class TemporalSeedsOnBackground(MorphoPlugin):
    """ "TEMPORAL PROPAGATE BARYCENTER". On part d'un pas de temps ou on est content de la segmentation d'une/des cellule(s). On propage en forward et/ou en backward le barycentre pour soit i) spliter une cellule sous-segmentée qui contient deux barycentres (dans un premier temps le watershed sera basé uniquement sur le masque) , soit ii) créer une cellule quand le barycentre propagé est dans le background (taille de la boite ?).


    Parameters
    ----------
    Objects:
        It can be apply either on selected or colored objects
    Axis : Dropdown

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_name("Propagate objects as seeds on the mask of the next time step")
        self.add_dropdown("Direction",["Forward","Backward"])
        self.add_inputfield("Volume_Minimum", default=1000)
        self.set_parent("Segmentation")
        self.set_description( "This plugin propagates the segmentation of existing objects through times. User "
                              "labelizes the object to propagate, and than the corresponding cells (to split or to "
                              "create) on a time range. \n The plugin can be executed Forward (the 'source' cells are "
                              "at the beginning of the time range) or Backward (the 'source' cells are at the end of "
                              "the time range) \n \n. The 'source' cells barycenters are used as seeds for the next "
                              "point time point segmentation (watershed algorithm , applied on the segmentation "
                              "image).\n The cells created are the source of the next time point segmentation, "
                              "until the end of the time range.")


    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects):
            return None

        printv("Propagation of " + str(len(objects)) + " objects", 0)
        #Minimum volume of the cell created by the propagation
        self.min_vol = int(self.get_inputfield("Volume_Minimum"))
        # List Objects by selections , to work on each selection one by one
        selections = get_list_of_selections(dataset,objects)

        new_label = ""
        # Get user direction chosen
        forward = (str(self.get_dropdown("Direction")) == "Forward")
        # For each selection found
        for s in selections:
            new_label += process_propagation_for_selection(selections, s, dataset,forward,self.min_vol,use_raw_images=False,sigma=0)
        #Send back data to MorphoNet
        self.restart(label=new_label)






