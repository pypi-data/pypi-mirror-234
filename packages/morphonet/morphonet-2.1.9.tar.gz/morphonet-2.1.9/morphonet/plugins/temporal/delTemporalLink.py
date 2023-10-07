# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class DelTemporalLink(MorphoPlugin):
    """This plugin delete any temporal links between objects

    Parameters
    ----------
    Objects: 
        It can be apply either on selected or colored objects
    """
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Delete temporal links on selected objects")
        self.set_parent("Temporal Relation")
        self.set_description("This plugins use a list of labeled objects on MorphoNet, and for each consecutive time "
                             "points pair , the plugin delete a lineage (temportal) link in the embryo properties, "
                             "for the objects sharing the same labels.")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        links_deleted=0
        # For each object to remove the link from
        for cid in objects:
            o=dataset.get_object(cid)
            if o is not None:
                #If we have temporal links
                if len(o.mothers)>0 or len(o.daughters)>0:
                    printv("remove "+str(len(o.mothers))+ " mothers and "+str(len(o.daughters))+ " daughters for object "+str(o.id)+" at "+str(o.t),0)
                    #Remove mother links in lineage
                    for m in o.mothers:
                        if dataset.del_mother(o,m):
                            links_deleted+=1
                    #Remove daughter links in lineage
                    for d in o.daughters:
                        if dataset.del_daughter(o,d):
                            links_deleted+=1
        printv(str(links_deleted) + " links where deleted", 0)
        #Send data to morphonet
        self.restart(cancel=links_deleted==0)
