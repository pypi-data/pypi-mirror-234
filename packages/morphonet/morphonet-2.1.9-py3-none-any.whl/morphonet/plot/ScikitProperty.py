
class ScikitProperty():
    """ Quantitative Information extract from Regions Properties from scikit image
    Parameters
    ----------
    name : string
        the name of the info
    info_type : string
        the type of the info as definied in the MorphoNet format  https://morphonet.org/help_format

    """

    def __init__(self, dataset, name,type):
        self.name = name
        self.dataset = dataset
        self.data = {}
        self.updated = False
        self.loaded=False
        self.type=type

    def set(self,mo,value):
        if mo.t not in self.data: self.data[mo.t]={}
        self.data[mo.t][mo] =value
        self.updated=True

    def get(self,mo):
        if mo.t not in self.data: return None
        if mo not in  self.data[mo.t]: return None
        return self.data[mo.t][mo]

    def get_at(self,t):
        if t not in self.data: return None
        return self.data[t]

    def get_txt(self):
        Text =  "#MorphoPlot" + '\n'
        Text += "#"+self.name+" property computed from Scikit image\n"
        Text += "type:" + self.type + "\n"
        for t in self.data:
            for o in self.data[t]:
                Text += o.get_name() + ':' + str(self.data[t][o])
                Text += '\n'
        return Text
