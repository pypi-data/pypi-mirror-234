# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv


class GaussianMixture(MorphoPlugin):
    """ This plugin split objects based on Gaussian Mixture Algorithm from sklearn
    https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html

    Parameters
    ----------
    Objects:
        It can be apply either on selected or colored objects
    Axis : Dropdown
        It can be X,Y or Z axis

    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_name("Gaussian Mixture")
        self.add_dropdown("Method",["kmeans", "randomFromData", "k-means++", "random"])
        self.add_inputfield("Number of Objects", default=2)

        self.set_parent("Split objects")


    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        import numpy as np
        from sklearn.mixture import GaussianMixture

        method=self.get_dropdown("Method")
        n_components= int(self.get_inputfield("Number of Objects"))
        for t in dataset.get_times(objects): #For each time point in objects to split

            data = dataset.get_seg(t)  #Load the segmentations
            cells_updated = []
            for o in dataset.get_objects_at(objects, t): #For each object at time point
                printv('Split Object '+str(o.get_name())+ " with  "+str(method),0)

                coords = dataset.np_where(o)
                X = np.array(coords).transpose()
                r = np.random.RandomState(seed=1234)
                gmm = GaussianMixture(n_components=n_components, init_params=method, tol=1e-9, max_iter=0,random_state=r).fit(X)

                cells_updated.append(o.id)
                lastID = int(data.max())+1
                for i in range(1,n_components):
                    w = gmm.predict(X) == i
                    data[coords[0][w], coords[1][w], coords[2][w]] = lastID
                    printv('Create a new ID ' + str(lastID) + " with " + str(len(coords[0][w])) + " pixels", 0)
                    cells_updated.append(lastID)
                    lastID += 1

            if len(cells_updated)>0:  dataset.set_seg(t,data,cells_updated=cells_updated) #If we created a cell ,save it to seg

        self.restart()   #send data back to morphonet
