# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class AddTemporalLink(MorphoPlugin):
    """This plugin create a temporal link between objects

    Parameters
    ----------
    Objects: 
        It can be apply either on selected objects or on colored objects where temporal link will done by selection id

    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Create temporal links between selected objects")
        self.set_parent("Temporal Relation")
        self.set_description("This plugins use a list of labeled objects on MorphoNet, and for each consecutive time "
                             "points pair , the plugin creates a lineage (temportal) link in the embryo properties, "
                             "for the objects sharing the same labels.")
    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects): 
            return None

        link_created=0
        #Work by selections
        selections={}
        #Group objects by selections, each selection will be linked together
        for cid in objects:
            o=dataset.get_object(cid)
            if o is not None:
                if o.s not in selections:
                    selections[o.s]=[]
                selections[o.s].append(o)
        #If user didn't select cell, restart
        if len(selections)==0:
            printv("please, selected some cells first", 0)
        else:
            printv("found  "+str(len(selections))+ " selections ",0)
            #For each selection, group cells by times
            for s in selections:
                #Order objects by time
                times={}  #List all times
                for o in selections[s]:
                    if o.t not in times:
                        times[o.t]=[]
                    times[o.t].append(o)
                #For each time point, starting from first
                for t in sorted(times):
                    #if we can link to the next time
                    if t+1 in times:
                        #link all cells at t with cells at t+1
                        for daughter in times[t+1]:
                            for mother in times[t]:
                                if dataset.add_daughter(mother,daughter):
                                    link_created +=1
                                    printv("link object " + str(daughter.id) + " at " + str(daughter.t) + " with " + str(mother.id) + " at " + str(mother.t), 0)
        printv(str(link_created)+" new links where created", 0)
        #restart to morphonet
        self.restart(cancel=link_created==0)
