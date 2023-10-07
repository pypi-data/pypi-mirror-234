# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


def get_iou(bb1, bb2):
    '''
    Calculate the Intersection over Union (IoU) of two bounding boxes.
    '''

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1[0], bb2[0])
    y_top = max(bb1[1], bb2[1])
    z_up = max(bb1[2], bb2[2])
    x_right = min(bb1[3], bb2[3])
    y_bottom = min(bb1[4], bb2[4])
    z_down = min(bb1[5], bb2[5])

    if x_right < x_left or y_bottom < y_top  or z_down< z_up :
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top) * (z_down - z_up)

    # compute the area of both AABBs
    bb1_area = (bb1[3] - bb1[0]) * (bb1[4] - bb1[1]) * (bb1[5] - bb1[2])
    bb2_area = (bb2[3] - bb2[0]) * (bb2[4] - bb2[1]) * (bb2[5] - bb2[2])

    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    return iou



def get_best_oberlap(bbox,bboxs):
    o=0
    best=None
    #computing the best = one by one computing
    for mo in bboxs:
        #get the iou count for the box
        ov=get_iou(bbox,bboxs[mo])
        #if iou is more than the previous best, choose this box
        if ov>o:
            o=ov
            best=mo
    return best




class OverlapTracking(MorphoPlugin):
    """This plugin perform a objet tracking maximizing the overlap between temporal objects

    Parameters
    ----------
    Objects: 
        It can be apply either on selected or colored objects
    """
    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Create temporal links using maks overlap between time steps")
        self.set_parent("Temporal Relation")
        self.add_dropdown("Direction", ["forward", "backward"])
        self.set_description("This plugin generate the lineage information for the complete time sequence of the "
                             "MorphoNet dataset, in forward or backwards (in time) direction. \n It uses the best "
                             "overlapping between cells a t time t and next time point thanks to their bounding box , "
                             "and link the cells in the time for the most overlapping boxes.")

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,objects_require=False):
            return None
        #Get the lineage propagation direction
        direction=self.get_dropdown("Direction")
        printv("start overlap tracking from "+str(t),0)
        if direction=="forward" :
            #From t to t max
            while t<self.dataset.end:
                #compute lineage by overlaping
                self.compute_links(t,t+1)
                t+=1
        if direction == "backward":
            #from t to t min
            while t > self.dataset.begin:
                # compute lineage by overlaping
                self.compute_links(t, t - 1)
                t -= 1

        self.restart()

    def compute_links(self,t, tp):
        printv("compute links at " + str(t), 0)
        #Get the different cells bounding box
        bboxs = self.dataset.get_regionprop_at("bbox", t)
        #Get the next time points bounding box
        next_bboxs = self.dataset.get_regionprop_at("bbox", tp)
        for mo in bboxs:
            #For each box at t , find the best overlapping one at t+1
            next_mo = get_best_oberlap(bboxs[mo], next_bboxs)
            #link the corresponding cells in lineage
            self.dataset.add_daughter(mo, next_mo)