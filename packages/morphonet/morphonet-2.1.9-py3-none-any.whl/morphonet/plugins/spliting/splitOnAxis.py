# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class SplitOnAxis(MorphoPlugin):
    """ This plugin split objects in two on a given axis

    Parameters
    ----------
    Objects: 
        It can be apply either on selected or colored objects
    Axis : Dropdown
        It can be X,Y or Z axis

    """
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Split mask in the middle of a given axis")
        self.add_dropdown("Axis",["X","Y","Z"])
        self.set_parent("Split objects")
        self.set_description("This plugin splits all the selected (or labeled) objects (from multiple time points) , "
                             "along the axis (image axis) provided by the user as a parameter. \n The split is "
                             "operated in the middle of the axis, creating two new objects.")


    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        import numpy as np
        #Determine which axis in the image
        which=self.get_dropdown("Axis")
        xyz=-1
        if which=="X":
            xyz=0
        elif which=="Y":
            xyz=1
        elif which=="Z":
            xyz=2
        if xyz==-1:
            printv('ERROR' + which+ " unknown ....",2)
        else:
            #For each time point in objects to split
            for t in dataset.get_times(objects):
                #Load the segmentations
                data = dataset.get_seg(t)
                cells_updated = []
                #For each object at time point
                for o in dataset.get_objects_at(objects, t):
                    printv('Split Object '+str(o.get_name())+ " in "+str(which),0)
                    #Get the object to split coordinates in image
                    coords=dataset.np_where(o)
                    #Get the object coords in axis
                    xyzList=np.unique(coords[xyz])
                    xyzList.sort()
                    #Find the object new id (max id of seg +1)
                    lastID=int(data.max())
                    lastID=lastID+1
                    #get the upper half of the object along the choosen axis
                    w=np.where(coords[xyz]>int(xyzList.mean()))
                    new_coords=(coords[0][w],coords[1][w],coords[2][w])
                    #apply the new ids to the upper coords
                    data[new_coords]=lastID
                    printv('Create a new ID '+str(lastID)+ " with "+str(len(new_coords[0]))+ " pixels",0)
                    #add to refresh in morphonet
                    cells_updated.append(o.id)
                    cells_updated.append(lastID)
                if len(cells_updated)>0:
                    #If we created a cell ,s ave it to seg
                    dataset.set_seg(t,data,cells_updated=cells_updated)
        #send data back to morphonet
        self.restart()
