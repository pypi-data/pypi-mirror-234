from morphonet.tools import get_name, printv


class Object():
    """ Object
    """

    def __init__(self, t, id):
        self.t = t
        self.id = id
        self.daughters = []
        self.mothers=[]

    def get_name(self):
        return get_name(self.t, self.id)

    def clear_temporal_links(self):
        self.daughters.clear()
        self.mothers.clear()

    # PAST LINKS
    def add_mother(self, m):
        if m is not None:
            return m.add_daughter(self)
        return False

    def del_mother(self, m):
        if m is not None:
            return m.del_daughter(self)
        return False

    # FUTUR LINKS
    def add_daughter(self, d):
        if d is not None and d not in self.daughters:
            printv("Add temporal link for " + str(self.id) + " at " + str(self.t) + " with " + str(d.id) + " at " + str(d.t), 2)
            self.daughters.append(d)
            if self not in d.mothers:
                d.mothers.append(self)
            return True
        return False

    def del_daughter(self, d):
        if d in self.daughters:
            printv("Remove temporal link for "+str(self.id)+ " at "+str(self.t)+" with "+str(d.id)+ " at "+str(d.t),2)
            self.daughters.remove(d)
            d.mothers.remove(self)
            return True
        return False

    def del_daughters(self):
        if len(self.daughters)>0:
            printv("Clear all daughters for  " + str(self.id) + " at " + str(self.t) , 2)
            self.daughters.clear()
            return True
        return False


    def nb_daughters(self):
        return len(self.daughters)

    def nb_mothers(self):
        return len(self.mothers)
