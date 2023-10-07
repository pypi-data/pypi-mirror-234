# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import numpy as np
from ..functions import _centerInShape,get_seeds_in_image,watershed,gaussian
from ...tools import printv


class On_Raw(MorphoPlugin):
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

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Watershed segmentation on raw images")
        self.add_inputfield("Gaussian Sigma",default=2)
        self.add_inputfield("Volume Minimum",default=1000)
        self.add_inputfield("Box size", default=50)
        self.add_coordinates("Add a Seed")
        self.set_parent("Segmentation from seeds")
        self.set_description("This plugins generate one or multiple new cells from seed generated or placed in "
                             "MorphoNet Viewer. \n The new cells are computed on the raw data image, after applying a smoothing , "
                             "for each seed that is not in another object, inside a box defined by the 'box size' "
                             "parameter (in voxels). If the generated objects are under the volume threshold defined "
                             "by the user, the object is not created.")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,objects_require=False):
            return None
        #Get the smoothing applied to the raw images from user
        s_sigma=int(self.get_inputfield("Gaussian Sigma"))
        #Get the threshold volume for new cells from user
        min_vol=int(self.get_inputfield("Volume Minimum"))
        #Get the box size around the seed to watershed from user
        box_size = int(self.get_inputfield("Box size"))

        #Load segmentation in memory
        data=dataset.get_seg(t)
        #Load raw images in memory
        rawdata=dataset.get_raw(t)
        #Plugin can't work without raw images
        if rawdata is None:
            return
        #If segmentation is empty , we can still work with an empty image
        if data is None:
            data=np.zeros(rawdata.shape).astype(np.uint16)
        #Get the list of morphonet seed
        seeds = self.get_coordinates("Add a Seed")
        if len(seeds) == 0:
            printv("no seeds for watershed",0)
            return None
        printv("Found " + str(len(seeds)) + " seeds ",1)
        #Get the segmentation center
        dataset.get_center(data)
        #Seeds from morphonet space to segmentation space
        seeds = get_seeds_in_image(dataset, seeds)
        new_seed=[]
        for seed in seeds:
            #If the seed is inside the segmentation
            if _centerInShape(seed,data.shape):
                olid=data[seed[0],seed[1],seed[2]]
                #If the seed is in the backgrund, we can create a cell
                if olid==dataset.background: 
                    new_seed.append(seed)
                    printv("add seed "+str(seed),1)
                # if not, remove the seed from working list
                else:
                    printv("remove this seed "+str(seed)+ " which already correspond to cell "+str(olid),1)
            else:
                printv("this seed "+str(seed)+ " is out of the image",1)
        #If no seeds are correct , stop here
        if len(new_seed)==0:
            self.restart()
            return None

        #Create a working box around the seeds to constrain the segmentation
        if box_size>0:
            seedsa = np.array(new_seed)
            box_coords = {}
            for i in range(3):
                mi=max(0,seedsa[:,i].min()-box_size)
                ma=min(data.shape[i],seedsa[:,i].max()+box_size)
                box_coords[i]=[mi,ma]

            #Only get theraw data around the boxes
            ndata=data[box_coords[0][0]:box_coords[0][1],box_coords[1][0]:box_coords[1][1],box_coords[2][0]:box_coords[2][1]]
            rawdata = rawdata[box_coords[0][0]:box_coords[0][1], box_coords[1][0]:box_coords[1][1],
                      box_coords[2][0]:box_coords[2][1]]
            #Smooth the raw data if needed
            if s_sigma>0:
                printv("Perform gaussian with sigma=" + str(s_sigma) +" for box "+str(box_coords),0)
                rawdata = gaussian(rawdata, sigma=s_sigma, preserve_range=True)

            #Seed replaced in the box
            box_seed=[]
            for s in new_seed:
                box_seed.append([s[0]-box_coords[0][0],s[1]-box_coords[1][0],s[2]-box_coords[2][0]])
            new_seed=box_seed
        #If no box specified, gaussian the raw data
        else:
            rawdata = self.gaussian_rawdata(t, sigma=s_sigma, preserve_range=True)
            ndata=data

        # Mark the box borders for the segmentation
        markers=np.zeros(ndata.shape,dtype=np.uint16)
        markers[0,:,:]=1
        markers[:,0,:]=1
        markers[:,:,0]=1
        markers[ndata.shape[0]-1,:,:]=1
        markers[:,ndata.shape[1]-1,:]=1
        markers[:,:,ndata.shape[2]-1]=1

        #Mark the seeds in the watershed markers (seeds source) images, with unique ids
        newId=2
        for seed in new_seed: #For Each Seeds ...
            markers[seed[0],seed[1],seed[2]]=newId
            newId+=1

        #Create the mark to work on for the watershed from the box
        mask=np.ones(ndata.shape,dtype=bool)
        mask[ndata!=dataset.background]=False

        #Watershed on the rawdata , constrained by the mask  , using seed images computed
        printv("Process watershed with "+str( len(new_seed))+" seeds",0)
        labelw=watershed(rawdata,markers=markers, mask=mask)

        #next id is the segmentation max + 1
        cMax=data.max()+1
        nbc = 0
        #Compute the id new cells created by watershed
        new_ids=np.unique(labelw)
        #Borders are not cells
        new_ids=new_ids[new_ids>1] #REMOVE THE BORDERS
        #If we created at least a cell
        if len(new_ids)>0:
            printv("Combine new objects",1)
            cells_updated = []
            #For each cell
            for new_id in new_ids:
                #Compute its mask coordinates
                newIdCoord=np.where(labelw==new_id)
                #If the volume is above the user threshold
                if len(newIdCoord[0])>min_vol:
                    #Compute its coordinate in the segmentation space
                    if box_size>0:
                        newIdCoord=(newIdCoord[0]+box_coords[0][0],newIdCoord[1]+box_coords[1][0],newIdCoord[2]+box_coords[2][0])
                    #Write the new cell in the segmentation
                    data[newIdCoord]=cMax+nbc
                    printv("add object "+str(nbc+cMax)+' with  '+str(len(newIdCoord[0]))+ " voxels",0)
                    cells_updated.append(cMax + nbc)
                    nbc+=1
                else:
                    printv("remove object with  "+str(len(newIdCoord[0]))+ " voxels",0)
            if len(cells_updated)>0:
                #Save the new cells in morphonet data
                dataset.set_seg(t, data, cells_updated=cells_updated)
        printv("Found  "+str(nbc)+" new labels",0)
        #Send everything back to MorphoNet
        self.restart()




