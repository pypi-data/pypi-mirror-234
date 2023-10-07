from os.path import join

from morphonet.plot.Annotation import Annotation
from morphonet.tools import isfile, printv, rm, file_write_thread,get_name, get_id_t
from numpy import int64


class Property():
    """ Property that can be added in the Properties menu on the MorphoNet windows

    Parameters
    ----------
    name : string
        the name of the property
    property_type : string
        the type of the property as definied in the MorphoNet format  https://morphonet.org/help_format

    """

    def __init__(self, dataset, name, property_type):
        self.name = name
        self.dataset = dataset
        self.property_type = property_type
        self.data = {}
        self.updated = True
        self.todelete=False

    def delete(self):
        #Delete also associated file
        self.data.clear()
        filename = join(self.dataset.properties_path, self.name + ".txt")
        if isfile(filename):
            printv("delete "+filename,1)
            rm(filename)
        filename = join(self.dataset.annotations_path, self.name + ".txt")
        if isfile(filename):
            printv("delete " + filename, 1)
            rm(filename)
        del self.dataset.properties[self.name] #Compteltu remove from the list

    def clear(self):
        self.data.clear()

    def add_data(self, data):
        if data is None:
            return False
        if type(data) == str:  # Parse Text Property as in MorphoNet
            for d in data.split('\n'):
                if not d.startswith("#") and not d.startswith(("type")):
                    dos = d.split(":")
                    if len(dos) == 2:
                        mo = self.dataset.get_object(dos[0].strip())
                        self.set(mo, dos[1].strip())
        else:
            self.data = data

    def set(self, mo, value, date=None):
        '''
        Add a value to the property with the currente date and time
        Parameters
        ----------
        mo : MorphoObject : the cell object
        value : string  : the value
        Examples
        --------
        >>> prop.add(mo,"a7.8")
        '''

        if mo not in self.data: self.data[mo] = []

        if self.property_type!="time" and self.property_type!="selection" and self.property_type!="label": #NO annotation FOR LABEL AND LINEAGE
            for mc in self.data[mo]: #Inactive Previous annotation
                mc.active = False

        if type(value) == str and value.strip()=="":
            return False

        if self.property_type == "time":
            if type(value) == str:
                value = self.dataset.get_object(value)
                if value.t<mo.t: value.add_daughter(mo)
                else: mo.add_daughter(value)
            if type(value) == list:
                for val in value:
                    if type(val) == str:
                        val = self.dataset.get_object(val)
                    if val.t<mo.t: val.add_daughter(mo)
                    else: mo.add_daughter(val)

        if self.property_type == "selection" or self.property_type == "label":
            if type(value) == str:
                value = int(value)

        if self.property_type == "float":
            if type(value) == str:
                value = float(value)


        mc = Annotation(value, date=date, active=True)

        self.data[mo].append(mc)
        self.updated = True

    def del_annotation(self, mo, value,date=None):
        if mo not in self.data:
            return False

        to_remove = None
        for mc in reversed(self.data[mo]) :
            if to_remove is None and mc.value==value:
                if date is not None :
                    if mc.date==date:to_remove=mc
                else:
                    to_remove = mc
        if to_remove is not None:
            self.data[mo].remove(to_remove)
            #reactivate last then
            if len(self.data[mo])>0:
                self.data[mo][-1].active = True
            return True
        return False

    def get(self, mo):
        if mo is None:
            return None
        if mo not in self.data:
            return None
        list_properties = []
        for mc in self.data[mo]:
            if mc.active:
                list_properties.append(mc.value)
        if len(list_properties) == 0:
            return None
        if len(list_properties) == 1:
            return list_properties[0]
        return list_properties

    def get_annotations(self, mo):
        if mo is None:  return []
        if mo not in self.data: return []
        return self.data[mo]

    def get_annotation(self, mo, value, date=None):
        if mo is None:
            return None
        if mo not in self.data:
            return None
        for mc in self.data[mo]:
            if value == mc.value:
                if date is None:
                    return mc
                elif mc.date == date:
                    return mc
        return None

    def get_txt(self, time_begin=-1, time_end=-1, all_values=False,empty=False):
        '''
        all_values = False -> Only last values (Default)
        all_values = True -> all annotations

        '''
        Text=""
        for o in self.data:
            if (time_begin == -1 or (time_begin >= 0 and o.t >= time_begin)) and (
                    time_end == -1 or (time_end >= time_begin and o.t <= time_end)):
                for mc in self.get_annotations(o):
                    if all_values or (not all_values and mc.active):
                        if self.property_type == "time":
                            if type(mc.value) == dict or type(mc.value) == list:
                                for ds in mc.value:
                                    Text += o.get_name() + ':' + ds.get_name()
                                    if all_values : Text += "#" + str(mc.date)
                                    Text += '\n'
                            else:
                                Text += o.get_name() + ':' + mc.value.get_name()
                                if all_values : Text += "#" + str(mc.date)
                                Text += '\n'
                        elif self.property_type == "dict":
                            if type(mc.value) == dict:
                                for dk,ds in mc.value.items():
                                    if isinstance(dk,(int,int64)):
                                        t,n = get_id_t(dk)
                                        dsname=get_name(t,n)
                                        Text += o.get_name() + ':' + str(dsname) + ':' + str(ds)
                                    else:
                                        Text += o.get_name() + ':' + str(dk) + ':' + str(ds)
                                    if all_values : Text += "#" + str(mc.date)
                                    Text += '\n'
                            else:
                                Text += o.get_name() + ':' + mc.value.get_name()
                                if all_values : Text += "#" + str(mc.date)
                                Text += '\n'
                            
                        else:
                            Text += o.get_name() + ':' + str(mc.value)
                            if all_values :  Text += "#" + str(mc.date)
                            Text += '\n'
        if not empty and Text=="": return None
        start_text = "#MorphoPlot" + '\n'
        start_text += "#"
        if all_values: start_text += 'History of annotations for '
        start_text += self.name + '\n'
        start_text += "type:" + self.property_type + "\n"
        return start_text+Text

    #INPORT EXPORT ACTIVE PROPERTY
    def read(self, filename):
        '''
        Parse a MorphoNet Property file
        '''
        if not isfile(filename):
            printv("miss " + filename, 3)
            return False
        printv("read property " + filename, 2)
        self.data = {}  # Reinitialise everything
        for d in open(filename, 'r'):
            if not d.startswith("#"):
                if d.startswith(("type")):
                    self.property_type = d.strip().replace("type:", "")
                else:
                    dos = d.split(":")
                    if len(dos) == 2:
                        mo = self.dataset.get_object(dos[0].strip())
                        self.set(mo, dos[1].strip())
        return True

    def export(self,filename=None, wait=False):
        if filename is None:
            filename = join(self.dataset.properties_path, self.name + ".txt")
        txt = self.get_txt(empty=True)
        if txt is not None:
            printv("save property in " + filename,1)
            fw=file_write_thread(filename,txt)
            fw.start()
            if wait: fw.join()

    # INPORT HISTORY OF THE PROPERTY  (Annotation)
    def export_annotations(self,filename=None):
        if filename is None:
            filename=join(self.dataset.annotations_path,self.name+".txt")
        txt = self.get_txt(all_values=True)
        if txt is not None:
            printv("save history of annotation in " + filename, 1)
            fw = file_write_thread(filename, txt)
            fw.start()

    def read_annotation(self, txt_filename):
        if isfile(txt_filename):
            printv("read history of annotation from " + txt_filename, 1)
            f = open(txt_filename, 'r')
            for line in f:
                if line.find("#") != 0 and line.find("type") == -1:
                    p = line.find(":")
                    d = line.find("#")
                    o = self.dataset.get_object(line[:p])
                    value = line[p + 1:d]
                    self.set(o, value, date=line[d + 1:].strip())
            f.close()

    # Export dictionarry FOR XML
    def get_dict(self, key_format="xml"):
        prop = {}
        for o in self.data:
            cv = o.t * 10 ** 4 + o.id
            cell_key = o.t * 10 ** 4 + o.id
            if key_format == "tuple":
                cell_key = (o.t, o.id)
            for mc in self.get_annotations(o):
                if mc.active == True:
                    if self.property_type == "time":
                        if type(mc.value) == dict or type(mc.value) == list:
                            for m in mc.value:
                                mother = m.t * 10 ** 4 + m.id
                                mother_key = m.t * 10 ** 4 + m.id
                                if key_format == "tuple":
                                    mother_key = (m.t, m.id)
                                if m.t < o.t:
                                    if mother not in prop:
                                        prop[mother_key] = []
                                    prop[mother_key].append(cv)
                                else:  # Inverse
                                    if cell_key not in prop:
                                        prop[cell_key] = []
                                    prop[cell_key].append(mother)
                        else:
                            mother = m.t * 10 ** 4 + m.id
                            mother_key = m.t * 10 ** 4 + m.id
                            if key_format == "tuple":
                                mother_key = (m.t, m.id)
                            if mc.value.t < o.t:
                                if mother not in prop:
                                    prop[mother_key] = []
                                prop[mother_key].append(cv)
                            else:  # Inverse
                                if cv not in prop:
                                    prop[cell_key] = []
                                prop[cell_key].append(mother)
                    else:
                        if cell_key in prop:
                            if type(prop[cell_key]) == list:
                                prop[cell_key].append(mc.value)
                            else:
                                prop[cell_key] = [prop[cell_key], mc.value]
                        else:
                            prop[cell_key] = mc.value
        return prop

