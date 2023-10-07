# -*- coding: latin-1 -*-
import os,time
import numpy as np
import datetime
from urllib.parse import unquote
from os.path import isdir,join,dirname,basename
import json
import shutil
try:
    from vtk import vtkImageImport, vtkDiscreteMarchingCubes, vtkWindowedSincPolyDataFilter, vtkQuadricClustering, vtkDecimatePro, vtkPolyDataReader, vtkPolyDataWriter, vtkPolyData
except:
    print("VTK library is not available")
try:
    from skimage.measure import regionprops
except:
    print("ScikitImage library is not available")
from threading import Thread
import pickle
import copy

verbose=1 #Global variable for verbose
plot_instance=None #Use for print
#****************************************************************** IMAGE READER / WRITER


def load_credentials(config_json):
    """
    Load credentials from configs file path

    :Parameters:
     - `config_json` (str)

    :Returns Type:
        |numpyarray|
    """
    try :
        f = open(config_json,"r")
        json_raw = f.read()
        f.close()
    except :
        print("Error accessing config file")
        return

    json_dict = json.loads(json_raw)
    return json_dict["mn_login"],json_dict["mn_password"]

def imread(filename, verbose=True,voxel_size=False):
    """Reads an image file completely into memory

    :Parameters:
     - `filename` (str)
     - `verbose` (bool)
     - `voxel_size` (bool)

    :Returns Type:
        |numpyarray|
    """
    if verbose:
        print(" --> Read " + filename)
    if not isfile(filename):
        if verbose:
            print("Miss "+filename)
        return None
    try:

        if filename.find("mha") > 0:
            from morphonet.ImageHandling import imread as imreadINR
            data, vsize = imreadINR(filename)
            if voxel_size:
                return np.array(data), vsize
            else:
                return np.array(data)
        elif filename.find('.inr') > 0:
            from morphonet.ImageHandling import imread as imreadINR
            data,vsize = imreadINR(filename)
            if voxel_size:
                return np.array(data),vsize
            else:
                return np.array(data)
        elif filename.find('.nii') > 0:
            from nibabel import load as loadnii
            im_nifti = loadnii(filename)
            if voxel_size:
                sx, sy, sz = im_nifti.header.get_zooms()
                vsize = (sx, sy, sz)
                return np.array(im_nifti.dataobj).astype(np.dtype(str(im_nifti.get_data_dtype()))),vsize
            else :
                return np.array(im_nifti.dataobj).astype(np.dtype(str(im_nifti.get_data_dtype())))
        elif filename.find("h5") > 0:
            import h5py
            with h5py.File(filename, "r") as f:
                return np.array(f["Data"])
        else:
            from skimage.io import imread as imreadTIFF
            imtiff = imreadTIFF(filename)
            if voxel_size:
                vsize = TIFFTryParseVoxelSize(filename)
                return imtiff,(float(vsize[0]), float(vsize[1]), float(vsize[2]))
            else:
                return imtiff
    except Exception as e:
        if verbose:
            print(" Error Reading " + filename)
            print(str(e))
            if filename.endswith("gz") or filename.endswith("zip"):
                temp_path = "TEMP" + str(time.time())
                while os.path.isdir(temp_path):  # JUST IN CASE OF TWISE THE SAME
                    temp_path = "TEMP" + str(time.time())
                os.system("mkdir -p " + temp_path)
                os.system("cp " + filename + " " + temp_path)
                filename = join(temp_path, os.path.basename(filename))
                os.system("gunzip " + filename)
                filename = filename.replace('.gz', '')
                if voxel_size:
                    arrayim,vsize = imread(filename,verbose,voxel_size)
                    if temp_path is not None:
                        os.system("rm -rf " + temp_path)
                    return arrayim,vsize
                else :
                    arrayim = imread(filename,verbose,voxel_size)
                    if temp_path is not None:
                        os.system("rm -rf " + temp_path)
                    return arrayim

            return None
        # quit()
    return None

def TIFFTryParseVoxelSize(filename):
    """Tries to parse voxel size from TIFF image. default return is (1,1,1)

    :Parameters:
     - `filename` (str)

    :Returns Type:
        |tuple|
    """
    import tifffile as tf
    vsx=1
    vsy=1
    vsz=1
    with tf.TiffFile(filename) as tif:
        
        if len(tif.pages)>0:
            page = tif.pages[0]
            for tag in page.tags:
                if tag.name=="XResolution":
                    if len(tag.value)>=2:
                        vsx = round(tag.value[1]/tag.value[0],5)
                if tag.name=="YResolution":
                    if len(tag.value)>=2:
                        vsy = round(tag.value[1]/tag.value[0],5)
                if tag.name=="ImageDescription":
                    subtags = tag.value.split("\n")
                    for t in subtags:
                        if "spacing" in t:
                            if len(t.split("="))>=2:
                                vsz = t.split("=")[1]
    vsize =(vsx,vsy,vsz)
    return vsize


def imsave(filename, img, verbose=True,voxel_size=(1,1,1)):
    """Save a numpyarray as an image to filename.

    The filewriter is choosen according to the file extension.

    :Parameters:
     - `filename` (str)
     - `img` (|numpyarray|)
    """

    if verbose:
        print(" --> Save " + filename)
    if filename.find('.inr') > 0 or filename.find('.mha') > 0:
        from morphonet.ImageHandling import SpatialImage
        from morphonet.ImageHandling import imsave as imsaveINR
        return imsaveINR(filename, SpatialImage(img),voxel_size=voxel_size)
    elif filename.find('.nii') > 0:
        import nibabel as nib
        from nibabel import save as savenii
        new_img = nib.nifti1.Nifti1Image(img, None)
        new_img.header.set_zooms(voxel_size)
        im_nifti = savenii(new_img, filename)
        return im_nifti
    else:
        from skimage.io import imsave as imsaveTIFF
        if filename.endswith(".gz"):
            filename = filename.replace(".gz", "")
            im = imsaveTIFF(filename, img)
            os.system("cd " + os.path.dirname(filename) + ";gzip " + os.path.basename(filename))
            return im
    return None

class imsave_thread(Thread):
    # Just perform the saving in thread
    def __init__(self, filename, data, verbose=True):
        Thread.__init__(self)
        self.filename = filename
        self.data = data
        self.verbose = verbose

    def run(self):  # START FUNCTION
        imsave(self.filename, self.data, verbose=self.verbose)
        print(" -> Done " + self.filename)


class _save_seg_thread(Thread):
    # Just perform the saving in thread in npz
    def __init__(self, filename , data, voxel_size=(1,1,1)):
        Thread.__init__(self)
        self.filename=filename
        self.data = data
        self.voxel_size=voxel_size

    def run(self):  # START FUNCTION
        printv("save "+self.filename,2)
        np.savez_compressed(self.filename,data=self.data,voxel_size=self.voxel_size)

def _load_seg(filename):
    if filename is None: return None,None
    printv( "load "+filename,1)
    data,voxel_size=None,None
    try:
        loaded=np.load(filename)
        voxel_size=loaded['voxel_size']
        data = loaded['data']
    except:
        printv("Error reading "+filename,2)
        if isfile(filename): rm(filename)
    return data,voxel_size

class calcul_regionprops_thread(Thread):
    def __init__(self, dataset,t,filename,regionprops_name,background=0):
        Thread.__init__(self)
        self.dataset=dataset
        self.t = t
        self.filename=filename
        self.regionprops_name=regionprops_name
        self.background=background

    def run(self):  # START Compute regions
        if self.t in self.dataset.seg_datas:
            printv("Compute regions properties at "+str(self.t),2)
            if self.background>0:
                data=np.copy(self.dataset.seg_datas[self.t])
                data[data==self.background]=0
                self.dataset.regions[self.t] = regionprops(data)
            else:
                self.dataset.regions[self.t] = regionprops(self.dataset.seg_datas[self.t])
            self.sr=save_properties_thread(self.dataset,self.t,self.filename,self.regionprops_name)
            self.sr.start()

class save_properties_thread(Thread):
    def __init__(self,dataset,t,filename,regionprops_name):
        Thread.__init__(self)
        self.t=t
        self.dataset=dataset
        self.filename=filename
        self.regionprops_name=regionprops_name

    def run(self):  # START Save properties
        regions_keep={}
        for r in self.dataset.regions[self.t]:
            c=r['label']
            regions_keep[c]={}
            for p in self.regionprops_name:
                if p in r:
                    regions_keep[c][p] = r[p]
                    self.dataset.regionprops[p].set(self.dataset.get_object(self.t,c),r[p]) #FILL DATASET PROPERTY

        if isdir(os.path.dirname(self.filename)): #In case the folder has been delete by a cancel action
            with open(self.filename, "wb") as outfile:
                pickle.dump(regions_keep, outfile)
        if self.t in self.dataset.regions:  del self.dataset.regions[self.t]
        if self.t in self.dataset.regions: self.dataset.regions.remove(self.t)
        if self.t in self.dataset.regions_thread: del self.dataset.regions_thread[self.t]
        if self.t in self.dataset.regions_thread: self.dataset.regions_thread.remove(self.t)
        printv("regions properties saved in " + self.filename, 2)



class start_load_regionprops(Thread):
    def __init__(self,dataset):
        Thread.__init__(self)
        self.dataset = dataset

    def run(self):
        for t in range(self.dataset.begin,self.dataset.end+1):
            self.dataset.load_regionprops_at(t)
        self.dataset.parent.send_regionprops_name() #After all properties calculated (or loaded), we can send them to Unity


def get_all_available_regionprops():
    available_properties={}
    available_properties['area'] = 'float'
    available_properties['area_bbox'] = 'float'
    available_properties['area_convex'] = 'float'
    available_properties['area_filled'] = 'float'
    available_properties['axis_major_length'] = 'float'
    available_properties['axis_minor_length'] = 'float'
    available_properties['bbox'] = 'dict'
    available_properties['centroid'] = 'dict'
    available_properties['centroid_local'] = 'dict'
    available_properties['centroid_weighted'] = 'dict'
    available_properties['centroid_weighted_local'] = 'dict'
    available_properties['coords_scaled'] = 'dict'
    available_properties['coords'] = 'dict'
    available_properties['eccentricity'] = 'float'
    available_properties['equivalent_diameter_area'] = 'float'
    available_properties['euler_number'] = 'float'
    available_properties['extent'] = 'float'
    available_properties['feret_diameter_max'] = 'float'
    available_properties['inertia_tensor'] = 'dict'
    available_properties['inertia_tensor_eigvals'] = 'dict'
    available_properties['intensity_max'] = 'float'
    available_properties['intensity_mean'] = 'float'
    available_properties['intensity_min'] = 'float'
    available_properties['label']='float'
    available_properties['moments'] = 'dict'
    available_properties['moments_hu'] = 'dict'
    available_properties['moments_normalized'] = 'dict'
    available_properties['moments_weighted'] = 'dict'
    available_properties['moments_weighted_central'] = 'dict'
    available_properties['moments_weighted_hu'] = 'dict'
    available_properties['moments_weighted_normalized'] = 'dict'
    available_properties['orientation'] = 'float'
    available_properties['perimeter'] = 'float'
    available_properties['perimeter_crofton'] = 'float'
    available_properties['solidity'] = 'float'
    return available_properties

def get_regionprops_type(property):
    available_properties=get_all_available_regionprops()
    if property not in available_properties:
        printv("Unknown regions property "+property,2)
        return None
    return available_properties[property]




def rescale(segment_files,begin,end,active):
    if not active:
        return segment_files
    split_name = segment_files.split('.')
    rescaled_files =split_name[0]+"_rescaled."+split_name[1]
    for i in range(begin,end+1):
        im_seg=imread(segment_files.format(i))
        im_rescaled =im_seg[::2,::2,::2]
        imsave(rescaled_files.format(i),im_rescaled)
    return rescaled_files

def _add_line_in_file(file,action):
    f = open(file, "a")
    f.write(str(action))
    f.close()
def _read_last_line_in_file(file):
    last_action=""
    for line in open(file, "r"):
        last_action=line
    return last_action

def read_file(filename):
    s=""
    for line in open(filename,"r"):
        s+=line
    return s


def printv(msg,v):
    '''
    General print function use in Plot mode.
    Parameters
    v : 0 ->  SEND TO UNITY +  TERMINAL IN GREEN
        1 ->  SEND TO CONSOLE  + TERMINAL IN WHITE
        2 ->  DEVELLOPEUR TO TERMINAL IN BLUE
        3 ->  HIGH DEVELLOPEUR TO TERMINAL IN RED
    '''
    if v<=verbose:
        msg=str(msg)
        if v==0:   #MESSAGE UNITY
            if msg != "DONE": printgreen("UNITY : "+msg)
            if plot_instance is not None and plot_instance.start_servers: plot_instance.send("MSG", msg) #SEND THE MESSAGE
        if v==1:  #CONSOLE
            print("-> " + msg)
            if plot_instance is not None and plot_instance.start_servers:  plot_instance.send("LOGMSG", msg)  #SEND THE MESSAGE
        if v==2:     # TERMINAL DEVELLOPEUR
            printblue("---> "+msg)
        if v == 3:  #VERY HIGH DEVELLOPEUR LEVEL
            printyellow("-----> " + msg)
        if v == -1:  #ERROR
            printred("-----> " + msg)


#******************************************************************  XML Properties
def get_txt_from_dict(property_name,data, time_begin=-1, time_end=-1,property_type="label"):
        Text= "#"+ property_name + '\n'
        Text += "type:" + property_type + "\n"
        for long_id in data.keys():
            t,id=get_id_t(long_id)
            value=data[long_id]
            if (time_begin == -1 or (time_begin >= 0 and t >= time_begin)) and (
                    time_end == -1 or (time_end >= time_begin and t <= time_end)):
                if property_type == "time":
                    if type(value) == dict or type(value) == list:
                        for longid_ds in value:
                            tds,ids=get_id_t(longid_ds)
                            Text += get_name(t,id) + ':' + get_name(tds,ids)
                            Text += '\n'
                    else:
                        tds, ids = get_id_t(value)
                        Text += get_name(t,id) + ':' + get_name(tds,ids)
                        Text += '\n'
                else:
                    Text += get_name(t, id) + ':' + str(value)
                    Text += '\n'
        return Text


def _set_dictionary_value(root):
    """

    :param root:
    :return:
    """

    if len(root) == 0:

        #
        # pas de branche, on renvoie la valeur
        #

        # return ast.literal_eval(root.text)
        if root.text is None:
            return None
        else:
            return eval(root.text)

    else:

        dictionary = {}
        for child in root:
            key = child.tag
            if child.tag == 'cell':
                key = np.int64(child.attrib['cell-id'])
            dictionary[key] = _set_dictionary_value(child)

    return dictionary

def read_XML_properties(filename,property=None):
    """
    Return a xml properties from a file 
    :param filename:
    :return as a dictionnary
    """
    properties = None
    if not os.path.exists(filename):
        printv('properties file missing '+filename,2)
    elif filename.endswith("xml") is True:
        printv('read XML properties from '+filename,1)
        import xml.etree.ElementTree as ElementTree
        inputxmltree = ElementTree.parse(filename)
        root = inputxmltree.getroot()
        if property is not None: #GET ONLY ONE PROPERTY
            for child in root:
                if child.tag==property:
                    properties={}
                    properties[property]=_set_dictionary_value(child)
        else: #GET ALL PROPERTIES
            properties= _set_dictionary_value(root)
    else:
        printv('unkown properties format for '+filename,2)
    return properties

def _indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            _indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def _set_xml_element_text(element, value):
    """

    :param element:
    :param value:
    :return:
    """
    #
    # dictionary : recursive call
    #   dictionary element may be list, int, numpy.ndarray, str
    # list : may be int, numpy.int64, numpy.float64, numpy.ndarray
    #

    if type(value) == dict:
        # print proc + ": type is dict"
        keylist = value.keys()
        sorted(keylist)
        for k in keylist:
            _dict2xml(element, k, value[k])

    elif type(value) == list:

        #
        # empty list
        #

        if len(value) == 0:
            element.text = repr(value)
        #
        # 'lineage', 'label_in_time', 'all-cells', 'principal-value'
        #

        elif type(value[0]) in (int, float, np.int64, np.float64):
            # element.text = str(value)
            element.text = repr(value)

        #
        # 'principal-vector' case
        #  liste de numpy.ndarray de numpy.float64
        #
        elif type(value[0]) == np.ndarray:
            text = "["
            for i in range(len(value)):
                # text += str(list(value[i]))
                text += repr(list(value[i]))
                if i < len(value)-1:
                    text += ", "
                    if i > 0 and i % 10 == 0:
                        text += "\n  "
            text += "]"
            element.text = text
            del text

        else:
            element.text = repr(value)
            #print( " --> error, element list type ('" + str(type(value[0]))  + "') not handled yet for "+str(value))
            #quit()
    #
    # 'barycenter', 'cell_history'
    #
    elif type(value) == np.ndarray:
        # element.text = str(list(value))
        element.text = repr(list(value))

    #
    # 'volume', 'contact'
    #
    elif type(value) in (int, float, np.int64, np.float64):
        # element.text = str(value)
        element.text = repr(value)

    #
    # 'fate', 'name'
    #
    elif type(value) == str:
        element.text = repr(value)

    else:
        print( " --> element type '" + str(type(value))  + "' not handled yet, uncomplete translation")
        quit()

def _dict2xml(parent, tag, value):
    """

    :param parent:
    :param tag:
    :param value:
    :return:
    """

    #
    # integers can not be XML tags
    #
    import xml.etree.ElementTree as ElementTree
    if type(tag) in (int, np.int64):
        child = ElementTree.Element('cell', attrib={'cell-id': str(tag)})
    else:
        child = ElementTree.Element(str(tag))

    _set_xml_element_text(child, value)
    parent.append(child)
    return parent

def dict2xml(dictionary, defaultroottag='data'):
    """

    :param dictionary:
    :param defaultroottag:
    :return:
    """
    import xml.etree.ElementTree as ElementTree
    if type(dictionary) is not dict:
        print(" --> error, input is of type '" + str(type(dictionary)) + "'")
        return None

    if len(dictionary) == 1:
        roottag = dictionary.keys()[0]
        root = ElementTree.Element(roottag)
        _set_xml_element_text(root, dictionary[roottag])

    elif len(dictionary) > 1:
        root = ElementTree.Element(defaultroottag)
        for k, v in dictionary.items():
            _dict2xml(root, k, v)

    else:
        print(" --> error, empty dictionary ?!")
        return None

    _indent(root)
    tree = ElementTree.ElementTree(root)

    return tree

def write_XML_properties(properties,filename,thread_mode=True):
    """
    Write a xml properties in a file 
    :param properties:
    :param filename:
    """
    if thread_mode:
        wxml = Thread(target=write_XML_properties_thread, args=[properties,filename])
        wxml.start()
    else:
        write_XML_properties_thread(properties,filename)

def write_XML_properties_thread(properties,filename):
    """
    Write a xml properties in a file in Thread Mode
    :param properties:
    :param filename:
    """
    if properties is not None:
        xmltree=dict2xml(properties)
        print(" --> write XML properties in "+filename)
        xmltree.write(filename)




def get_fate_colormap(fate_version):

    ColorFate2020 = {}
    ColorFate2020["1st Lineage, Notochord"] = 2
    ColorFate2020["Posterior Ventral Neural Plate"] = 19
    ColorFate2020["Anterior Ventral Neural Plate"] = 9
    ColorFate2020["Anterior Head Endoderm"] = 8
    ColorFate2020["Anterior Endoderm"] = 8
    ColorFate2020["Posterior Head Endoderm"] = 17
    ColorFate2020["Posterior Endoderm"] = 17
    ColorFate2020["Trunk Lateral Cell"] = 20
    ColorFate2020["Mesenchyme"] = 14
    ColorFate2020["1st Lineage, Tail Muscle"] = 3
    ColorFate2020["Trunk Ventral Cell"] = 21
    ColorFate2020["Germ Line"] = 10
    ColorFate2020["Lateral Tail Epidermis"] = 12
    ColorFate2020["Head Epidermis"] = 11
    ColorFate2020["Trunk Epidermis"] = 11
    ColorFate2020["Anterior Dorsal Neural Plate"] = 7
    ColorFate2020["Posterior Lateral Neural Plate"] = 18
    ColorFate2020["2nd Lineage, Notochord"] = 5
    ColorFate2020["Medio-Lateral Tail Epidermis"] = 13
    ColorFate2020["Midline Tail Epidermis"] = 15
    ColorFate2020["Posterior Dorsal Neural Plate"] = 16
    ColorFate2020["1st Endodermal Lineage"] = 1
    ColorFate2020["2nd Lineage, Tail Muscle"] = 6
    ColorFate2020["2nd Endodermal Lineage"] = 4

    ColorFate2009 = {}
    ColorFate2009["1st Lineage, Notochord"] = 78
    ColorFate2009["Posterior Ventral Neural Plate"] = 58
    ColorFate2009["Anterior Ventral Neural Plate"] = 123
    ColorFate2009["Anterior Head Endoderm"] = 1
    ColorFate2009["Anterior Endoderm"] = 1
    ColorFate2009["Posterior Head Endoderm"] = 27
    ColorFate2009["Posterior Endoderm"] = 27
    ColorFate2009["Trunk Lateral Cell"] = 62
    ColorFate2009["Mesenchyme"] = 63
    ColorFate2009["1st Lineage, Tail Muscle"] = 135
    ColorFate2009["Trunk Ventral Cell"] = 72
    ColorFate2009["Germ Line"] = 99
    ColorFate2009["Lateral Tail Epidermis"] = 61
    ColorFate2009["Head Epidermis"] = 76
    ColorFate2020["Trunk Epidermis"] = 76
    ColorFate2009["Anterior Dorsal Neural Plate"] = 81
    ColorFate2009["Posterior Lateral Neural Plate"] = 75
    ColorFate2009["2nd Lineage, Notochord"] = 199
    ColorFate2009["Medio-Lateral Tail Epidermis"] = 41
    ColorFate2009["Midline Tail Epidermis"] = 86
    ColorFate2009["Posterior Dorsal Neural Plate"] = 241
    ColorFate2009["1st Endodermal Lineage"] = 40
    ColorFate2009["2nd Lineage, Tail Muscle"] = 110
    ColorFate2009["2nd Endodermal Lineage"] = 44

    if fate_version=="2020":
        return ColorFate2020
    return ColorFate2009

def get_property_from_properties(prop,property_name,property_type,convert=None):
    Text="#" + property_name+"\n"
    if type(prop) == list:
        property_type="label"
    Text+= "type:" + property_type + "\n"
    Missing_Conversion=[]
    if type(prop) == list:
        for idl in prop:
            t, c = get_id_t(idl)
            Text += get_name(t, c) + ":1\n"
    else:
        if prop is not None:
            for idl in prop:
                t, c = get_id_t(idl)
                if property_type == 'time':
                    for daughter in prop[idl]:
                        td, d = get_id_t(daughter)
                        Text+=get_name(t, c) + ":" + get_name(td, d) + "\n"
                elif property_type == 'dict':  #178,724:178,1,0:602.649597
                    for elt in prop[idl]:
                        td, d = get_id_t(elt)
                        Text += get_name(t, c) + ":" + get_name(td, d)+":"+str(prop[idl][elt]) + "\n"
                else:
                    if convert is None:
                        if type(prop[idl])== list:
                            for elt in prop[idl]:
                                Text+=get_name(t, c) + ":" + str(elt) + "\n"
                        else:
                            Text+=get_name(t, c) + ":" + str(prop[idl]) + "\n"
                    else:
                        if type(prop[idl])== list:
                            for elt in prop[idl]:
                                if elt not in convert:
                                    if elt not in Missing_Conversion:
                                        Missing_Conversion.append(elt)
                                else:
                                    Text += get_name(t, c) + ":" + str(convert[elt]) + "\n"
                        else:
                            if prop[idl] not in convert:
                                if prop[idl] not in Missing_Conversion:
                                    Missing_Conversion.append(prop[idl])
                            else:
                                Text += get_name(t, c) + ":" + str(convert[prop[idl]]) + "\n"
    for elt in Missing_Conversion:
        print(" ->> Misss '" + str(elt) + "' in the conversion ")
    return Text

def write_property(filename,prop,property_name,property_type,convert=None):
    if property_type is None:
        property_type = get_property_type(property_name)
    if property_type is None:
        print(" ->> Did not find type for " + property_name)
    else:
        print(" Write "+filename)
        f = open(filename, "w")
        f.write(get_property_from_properties(prop,property_name.replace("selection_", "").replace("label_", ""),property_type,convert=convert))
        f.close()


def get_property_type(property_name):
    '''
    Return the MorphoNet type according the name of the property name
    '''
    if property_name.lower().startswith("selection"):
        return "label"
    if property_name.lower().startswith("label"):
        return "label"
    if property_name.lower().startswith("float"):
        return "float"
    if property_name.lower().find("lineage") >= 0:
        return "time"
    if property_name.lower().find("cell_contact_surface") >= 0:
        return "dict"
    if property_name.lower().find("surface") >= 0:
        return "float"
    if property_name.lower().find("compactness") >= 0:
        return "float"
    if property_name.lower().find("volume") >= 0:
        return "float"
    if property_name.lower().find("area") >= 0:
        return "float"
    if property_name.lower().find("fate") >= 0:
        return "string"
    if property_name.lower().find("name") >= 0:
        return "string"
    if property_name.lower().find("ktr") >= 0:
        return "float"
    if property_name.lower().find("erk") >= 0:
        return "float"
    if property_name.lower().find("h2b") >= 0:
        return "float"
    if property_name.lower().find("choice_certainty") >= 0:
        return "float"
    if property_name.lower().find("choice_difference") >= 0:
        return "float"
    if property_name.lower().find("tissuefate_guignard_2020") >= 0:
        return "label"
    if property_name.lower().find("tissuefate_lemaire_2009") >= 0:
        return "label"
    if property_name.lower().find("asymmetric_division_errors") >= 0:
        return "label"
    return None


def get_XML_properties(filename,property=None):
    properties = read_XML_properties(filename,property=property)
    infos={}
    if properties is not None:
        for property_name in properties:
            if property_name != "all_cells":
                prop = properties[property_name]
                if prop is None:
                    prop =  []
                if prop is not None:
                    property_type = get_property_type(property_name)
                    if property_name.find("morphonet_") >= 0: property_name = property_name.replace("morphonet_", "")
                    for possible_type in ["float", "label", "selection", "string"]:
                        if property_name.find(possible_type + "_") >= 0:
                            property_name = property_name.replace(possible_type + "_", "")
                            property_type = possible_type
                    if property_type is None:
                        property_type = "string"
                    if type(prop) == list:
                        property_type = "label"
                    if property_type=="selection":
                        property_type = "label"
                    infos[(property_name,property_type)]=prop
    return infos

#Return t, cell_id from long name : t*10**4+id (to have an unique identifier of cells)
def get_id_t(idl):
    t=int(int(idl)/(10**4))
    cell_id=int(idl)-int(t)*10**4
    return t,cell_id
def get_longid(t,idc):
    return t*10**4+idc
 

#Return Cell name as string
def get_name(t,id):
    return str(t)+","+str(id)

def _get_object(o):
    """ Construct an object (as a tuple) from a string
        
    """
    to=0
    ido=0
    cho=0
    oss=o.split(',')
    if len(oss)==1:
        ido=int(o)
    if len(oss)>1:
        to=int(oss[0])
        ido=int(oss[1])
    if len(oss)>2:
        cho=int(oss[2])
    if cho==0:
        return (to, ido) #We do not put channel 0 for most of the case
    return (to,ido,cho)

def _get_objects(property):
        """ Get the list of object from an properties data
        
        Parameters
        ----------
        property : string
            The property data

        Returns
        -------
        objects : list
            List of key/value corresponding to a split of the data

        """
        if type(property)==bytes or type(property)==bytearray:
            property=property.decode('utf-8')
        property=property.split("\n")
        objects={}
        for line in property:
            if len(line)>0 and line[0]!="#":
                if line.find("type")==0:
                    dtype=line.replace("type:","")
                else:
                    tab=line.split(":")
                    ob=_get_object(tab[0])
                    if ob in objects: #Multiple times the same value (we put in list)
                        val1=objects[ob]
                        if type(val1)!=list :
                            objects[ob]=[]
                            objects[ob].append(val1)
                        if dtype =="time" or dtype =="space" :
                            objects[ob].append(_get_object(tab[1]))
                        elif dtype == "dict":
                            objects[ob].append((_get_object(tab[1]), tab[2]))
                        else:
                            objects[ob].append(tab[1])
                    else:
                        if dtype =="time" or dtype =="space" :
                            objects[ob]=_get_object(tab[1])
                        elif dtype=="dict": #178,724:178,1,0:602.649597
                            objects[ob]=[]
                            objects[ob].append((_get_object(tab[1]),tab[2]))
                        else:
                            objects[ob] = tab[1]

        return objects

def _get_type(property):
        """ Get the type from an property data
        
        Parameters
        ----------
        property : string
            The property data

        Returns
        -------
        type : string
            the type (float, string, ...)

        """
        property=property.split('\n')
        for line in property:
            if len(line)>0 and line[0]!="#":
                if line.find("type")==0:
                    return line.split(":")[1]
        return None

def _get_string(ob):
    ret=""
    for i in range(len(ob)):
        ret+=str(ob[i])
        if not i==len(ob)-1:
            ret+=","
    return ret

def _get_last_annotation(l):
    if type(l)==list:
        lastD=datetime.datetime.strptime('1018-06-29 08:15:27','%Y-%m-%d %H:%M:%S')
        value=""
        for o in l:
            d=o.split(";")[2] #1 Value, 2 Guy, 3 Date
            d2 = datetime.datetime.strptime(d,'%Y-%m-%d-%H-%M-%S')
            if d2>lastD:
                lastD=d2
                value=o
        return value
    return l

def _get_param(command,p): #Return the value of a specific parameter in http query
    params=unquote(str(command.decode('utf-8'))).split("&")
    for par in params:
        k=par.split("=")[0]
        if k==p:
            return par.split("=")[1].replace('%20',' ')
    return ""

def isfile(filename):
    if os.path.isfile(filename):
        return True
    elif os.path.isfile(filename+".gz"):
        return True
    elif os.path.isfile(filename+".zip"):
        return True
    return False

def copy(filename1,filename2):
    if not (os.path.exists(filename1)) or os.path.exists(filename2):
        print("ERROR, copy function : incorrect argument(s)")
        return
    if os.path.isfile(filename1):
        shutil.copy2(filename1,filename2)
    elif os.path.isfile(filename1+".gz"):
        shutil.copy2(filename1+".gz",filename2+".gz")
    elif os.path.isfile(filename1+".zip"):
        shutil.copy2(filename1+".zip",filename2+".zip")
    else:
        print("ERROR : didn't find file "+filename1+" for copy")

def cp_dir(dir,target_dir):
    if not os.path.exists(dir) or not os.path.isdir(dir):
        print("ERROR, copy function : incorrect argument(s)")
        return
    shutil.copytree(dir, target_dir)

def cp(file, target_dir):
    if not os.path.exists(file) or not os.path.exists(target_dir) or not os.path.isdir(target_dir):
        print("ERROR, copy function : incorrect argument(s)")
        return
    shutil.copy2(file,target_dir)
    
def rmrf(path):
    import glob
    folders = glob.glob(path)
    for fold in folders:
        if os.path.exists(fold):
            if os.path.isfile(fold) or os.path.islink(fold):
                os.unlink(fold)
            else:
                res = shutil.rmtree(fold)

def rm(file):
    if os.path.exists(file):  
        if os.path.isfile(file):
            os.unlink(file)

def load_mesh(filename,voxel_size=None,center=None):
    f=open(filename,'r')
    obj=''
    for line in f:
        if len(line)>4 and line.find("v")==0 and line[1]==" ": #VERTEX
            if voxel_size is not None or center is not None:
                tab=line.replace('\t',' ').replace('   ',' ').replace('  ',' ').split(" ")
                v=[float(tab[1]),float(tab[2]),float(tab[3])]
                if voxel_size is not None:
                    if type(voxel_size)==str:
                        vs=voxel_size.split(",")
                        if len(vs)==3:
                            v[0]= v[0]*float(vs[0])
                            v[1]= v[1]*float(vs[1])
                            v[2]= v[2]*float(vs[2])
                    else:
                        v=v*voxel_size
                if center is not None:
                    v=v-center
                obj+="v "+str(v[0])+" "+str(v[1])+" "+str(v[2])+"\n"
            else:
                obj += line
        else:
            obj+=line
    f.close()
    return obj

def save_mesh(filename,obj):
    f = open(filename, "w")
    f.write(obj)
    f.close()

def get_objects_by_time(dataset,objects):
    times=[]
    for cid in objects: #List all time points
        o=dataset.get_object(cid)
        if o is not None and o.t not in times:
            times.append(o.t)
    times.sort() #Order Times
    return times


_dataToConvert=None
class convert_one_to_OBJ(Thread):
    def __init__(self, t,elt, path_write,recompute,Smooth=True, smooth_passband=0.01,smooth_iterations=25,Decimate=True,QC_divisions=1,Reduction=True,
                 TargetReduction=0.8, voxel_size=[1,1,1], DecimationThreshold=30):
        Thread.__init__(self)
        self.t=t
        self.elt = elt
        self.Smooth = Smooth
        self.smooth_passband = smooth_passband
        self.smooth_iterations = smooth_iterations
        self.Decimate = Decimate
        self.QC_divisions = QC_divisions
        self.Reduction = Reduction
        self.TargetReduction=TargetReduction
        self.Voxel_size = voxel_size
        self.DecimationThreshold = DecimationThreshold
        self.polydata=None
        self.recompute=True
        self.filename=None
        if path_write is not None:
            self.recompute=recompute
            self.filename=join(path_write,str(t),str(t)+'-'+str(elt)+'.vtk')
    def run(self):
        global _dataToConvert
        if not self.recompute:
            self.recompute=self.read()
        if self.recompute:
            coord=np.where(_dataToConvert==self.elt)

            min_bounds = [np.amin(coord[0]), np.amin(coord[1]), np.amin(coord[2])]
            max_bounds = [np.amax(coord[0]) + 1, np.amax(coord[1]) + 1, np.amax(coord[2]) + 1]

            for i in range(3):
                if min_bounds[i] > 0:   min_bounds[i] -= 1
                if max_bounds[i] < _dataToConvert.shape[i]:  max_bounds[i] += 1

            eltsd = np.array(
                _dataToConvert[min_bounds[0]:max_bounds[0], min_bounds[1]:max_bounds[1], min_bounds[2]:max_bounds[2]],
                copy=True, dtype=np.uint16)

            eltsd[eltsd!=self.elt]=0
            eltsd[eltsd==self.elt]=255

            eltsd = np.swapaxes(eltsd,0,2)
            eltsd = eltsd.astype(np.uint8)

            data_string = eltsd.tobytes('F')
            reader = vtkImageImport()
            reader.CopyImportVoidPointer(data_string, len(data_string))
            reader.SetDataScalarTypeToUnsignedChar()
            reader.SetDataSpacing(float(self.Voxel_size[0]),float(self.Voxel_size[1]),float(self.Voxel_size[2])) #invert X and Z ?

            reader.SetNumberOfScalarComponents(1)
            reader.SetDataExtent(min_bounds[2],max_bounds[2]-1, min_bounds[1],max_bounds[1]-1, min_bounds[0],max_bounds[0]-1)
            reader.SetWholeExtent(min_bounds[2],max_bounds[2]-1, min_bounds[1],max_bounds[1]-1, min_bounds[0],max_bounds[0]-1)

            reader.Update()

            #MARCHING CUBES
            contour = vtkDiscreteMarchingCubes()
            contour.SetInputData(reader.GetOutput())
            contour.ComputeNormalsOn()
            contour.ComputeGradientsOn()
            contour.SetValue(0,255)
            contour.Update()
            self.polydata= contour.GetOutput()

            if self.Smooth and self.polydata.GetPoints() is not None:
                smooth_angle=120.0
                smoth_passband=self.smooth_passband
                smooth_itertations=self.smooth_iterations
                smoother = vtkWindowedSincPolyDataFilter()
                smoother.SetInputData(self.polydata)
                smoother.SetFeatureAngle(smooth_angle)
                smoother.SetPassBand(smoth_passband)
                smoother.SetNumberOfIterations(smooth_itertations)
                smoother.NonManifoldSmoothingOn()
                smoother.NormalizeCoordinatesOn()
                smoother.Update()
                if smoother.GetOutput() is not None:
                    if smoother.GetOutput().GetPoints() is not None:
                        if smoother.GetOutput().GetPoints().GetNumberOfPoints() > 0:
                            self.polydata = smoother.GetOutput()

            if self.Decimate and self.polydata is not None:
                mesh_fineness=self.QC_divisions
                decimater = vtkQuadricClustering()
                decimater.SetInputData(self.polydata)
                decimater.SetNumberOfDivisions(*np.uint16(tuple(mesh_fineness*np.array(np.array(_dataToConvert.shape)/2))))
                decimater.SetFeaturePointsAngle(30.0)
                decimater.CopyCellDataOn()
                decimater.Update()
                if decimater.GetOutput() is not None:
                    if decimater.GetOutput().GetPoints() is not None:
                        if decimater.GetOutput().GetPoints().GetNumberOfPoints() > 0:
                                self.polydata = decimater.GetOutput()

            pdatacp = vtkPolyData()
            nbPoints=0            
            if self.Reduction and self.polydata is not None:
                while pdatacp is not None and nbPoints < self.DecimationThreshold and self.TargetReduction > 0:
                    decimatePro  = vtkDecimatePro()
                    decimatePro.SetInputData(self.polydata)
                    decimatePro.SetTargetReduction(self.TargetReduction)
                    decimatePro.Update()
                    if decimatePro.GetOutput() is not None:
                        if decimatePro.GetOutput().GetPoints() is not None:
                            if decimatePro.GetOutput().GetPoints().GetNumberOfPoints() > 0:
                                pdatacp = decimatePro.GetOutput()
                                nbPoints = pdatacp.GetPoints().GetNumberOfPoints()
                    self.TargetReduction-=0.05
            if pdatacp is not None and pdatacp.GetPoints() is not None and pdatacp.GetPoints().GetNumberOfPoints()>0:
                self.polydata = pdatacp
    
    def read(self):
        if os.path.isfile(self.filename):
            #print("Read "+self.filename)
            reader = vtkPolyDataReader()
            reader.SetFileName(self.filename)
            reader.Update()
            self.polydata=reader.GetOutput()
            return False
        return True


    def write(self,write_vtk):
        if write_vtk and self.recompute and self.filename is not None:
            writer = vtk_thread_writer(self.filename,self.polydata)
            writer.start()


class vtk_thread_writer(Thread): #A writer in Thread
    def __init__(self,filename,polydata):
        Thread.__init__(self)
        self.filename=filename
        self.polydata=polydata
    def run(self):
        mkdir(os.path.dirname(self.filename))
        # print("Write "+self.filename)
        writer = vtkPolyDataWriter()
        writer.SetFileName(self.filename)
        writer.SetInputData(self.polydata)
        writer.Update()


def convert_to_OBJ(dataFull,t=0,background=0,factor=1,channel=None,z_factor=None,Smooth=True,smooth_passband=0.01,smooth_iterations=25,
                   Decimate=True,QC_divisions=1,Reduction=True,TargetReduction=0.8,DecimationThreshold=30,Border=2,center=[0,0,0],
                   VoxelSize=[1,1,1],maxNumberOfThreads=None,cells_updated=None,path_write=None,write_vtk=False,force_recompute=False): ####  CONVERT SEGMENTATION IN MESH
        factor_z = z_factor if z_factor is not None else factor
        if factor_z == 0:
            factor_z = factor
        if factor != z_factor and z_factor is not None and z_factor != 0:
            VoxelSize = [VoxelSize[0],VoxelSize[1],VoxelSize[2]]
            VoxelSize[2] = VoxelSize[2] / (factor/z_factor)
        if path_write is None:  path_write="morphonet_tmp"
        if not isdir(path_write) and write_vtk:os.mkdir(path_write)
        time_filename=join(path_write,str(t)+".obj")
        if cells_updated is not None and len(cells_updated)==0 and isfile(time_filename) and not force_recompute:
            print(" --> read temporary mesh file at "+str(t))
            return file_read(time_filename)
        if dataFull is None:
            return None
        print(" --> Compute mesh at " + str(t))
        global _dataToConvert
        if maxNumberOfThreads is None:
            maxNumberOfThreads=os.cpu_count()*2
        _dataToConvert=dataFull[::factor_z,::factor,::factor]
        if Border>0: #We add border to close the cell
            _dataToConvert=np.zeros(np.array(_dataToConvert.shape) + Border * 2).astype(dataFull.dtype)
            _dataToConvert[:,:,:]=background
            _dataToConvert[Border:-Border,Border:-Border,Border:-Border]=dataFull[::factor_z,::factor,::factor]
        elts=np.unique(_dataToConvert) #This take times ....
        elts=elts[elts!=background] #Remove Background
        threads=[]
        all_threads=[]
        for elt in elts:
            if len(threads)>=maxNumberOfThreads:
                tc = threads.pop(0)
                tc.join()
                tc.write(write_vtk)

            #print(" Compute cell "+str(elt))
            recompute_cell=True if cells_updated is None else elt in cells_updated
            tc = convert_one_to_OBJ(t, elt,path_write, recompute_cell, Smooth=Smooth,smooth_passband=smooth_passband,
                                    smooth_iterations=smooth_iterations ,Decimate=Decimate,QC_divisions=QC_divisions, 
                                    Reduction=Reduction, TargetReduction=TargetReduction,DecimationThreshold=DecimationThreshold,
                                    voxel_size=VoxelSize)
            tc.start()
            all_threads.append(tc)
            threads.append(tc)

        #Finish all threads left
        while len(threads)>0:
            tc = threads.pop(0)
            tc.join()
            tc.write(write_vtk)

        #Merge all polydata in one
        obj=""
        shiftFace=1
        
        ch=str(channel) if channel is not None else '0'

        scaledBorder = np.asarray([VoxelSize[2], VoxelSize[1], VoxelSize[0]]) * Border * factor
        scaledCenter = np.asarray(center) * np.asarray([VoxelSize[2], VoxelSize[1], VoxelSize[0]])
        for tc in all_threads:
            polydata=tc.polydata
            elt=tc.elt
            if polydata is not None:
                if polydata.GetPoints() is not None:
                    obj+="g "+str(t)+","+str(elt)+","+ch+"\n"
                    for p in range(polydata.GetPoints().GetNumberOfPoints()):
                        v=polydata.GetPoints().GetPoint(p)
                        point = np.asarray([v[2], v[1], v[0]]) * factor - scaledBorder - scaledCenter
                        obj+='v ' + str(point[0]) +' '+str(point[1]) +' '+str(point[2])+'\n'
                    for f in range(polydata.GetNumberOfCells()):
                        obj+='f ' + str(shiftFace+polydata.GetCell(f).GetPointIds().GetId(2)) +' '+str(shiftFace+polydata.GetCell(f).GetPointIds().GetId(1)) +' '+str(shiftFace+polydata.GetCell(f).GetPointIds().GetId(0))+'\n'
                    shiftFace+=polydata.GetPoints().GetNumberOfPoints()
        #Write The finale file
        if write_vtk:
            file_write(time_filename,obj,in_thread=True)
        return obj


def convert_vtk_file_in_obj(filename,mo,ch=0,factor=None,Border=2,center=[0,0,0],VoxelSize=[1,1,1]):
    if isfile(filename):
        reader = vtkPolyDataReader()
        reader.SetFileName(filename)
        reader.Update()
        polydata = reader.GetOutput()

        scaledBorder = np.asarray([VoxelSize[2], VoxelSize[1], VoxelSize[0]]) * Border * factor
        scaledCenter = np.asarray(center) * np.asarray([VoxelSize[2], VoxelSize[1], VoxelSize[0]])

        if polydata is not None:
            if polydata.GetPoints() is not None:
                obj = ""
                obj += "g " + str(mo.t) + "," + str(mo.id) + "," + str(ch) + "\n"
                for p in range(polydata.GetPoints().GetNumberOfPoints()):
                    v = polydata.GetPoints().GetPoint(p)
                    #obj += 'v ' + str((v[2] + (-Border * VoxelSize[2])) * factor - center[0]) + ' ' + str(
                    #    (v[1] + (-Border * VoxelSize[1])) * factor - center[1]) + ' ' + str(
                    #    (v[0] + (-Border * VoxelSize[0])) * factor - center[2]) + '\n'
                    point = np.asarray([v[2], v[1], v[0]]) * factor - scaledBorder - scaledCenter
                    obj+='v ' + str(point[0]) +' '+str(point[1]) +' '+str(point[2])+'\n'
                for f in range(polydata.GetNumberOfCells()):
                    obj += 'f ' + str(polydata.GetCell(f).GetPointIds().GetId(2)) + ' ' + str(
                        polydata.GetCell(f).GetPointIds().GetId(1)) + ' ' + str(
                        polydata.GetCell(f).GetPointIds().GetId(0)) + '\n'
                return obj
    return None

def mkdir(path):
    if path is not None and path!="" and not isdir(path):
        try:
            os.mkdir(path)
            return True
        except:
            return False
            #path is already created ...
    return True
    
class file_write_thread(Thread):  # A file writer in Thread
    def __init__(self,filename,stri):
        Thread.__init__(self)
        self.filename = filename
        self.stri = stri
    def run(self):
        f = open(self.filename, 'w')
        f.write(str(self.stri))
        f.close()

def file_write(filename, stri,in_thread=False):
    '''
    Write in a file
    '''
    if in_thread:
        fw=file_write_thread(filename,stri)
        fw.start()
    else:
        f = open(filename, 'w')
        f.write(str(stri))
        f.close()

def file_read(filename):
    '''
    Read in a file
    '''
    line=""
    for f in open(filename, 'r'):
        line +=f
    return line


def add_slashes(s):
    d = {'"':'\\"', "'":"\\'", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s)


def try_parse_int(value):
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None
    return None

ss="-->"
class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def strblue(strs):
    return bcolors.BLUE+strs+bcolors.ENDC
def strred(strs):
    return bcolors.RED+strs+bcolors.ENDC
def strgreen(strs):
    return bcolors.GREEN+strs+bcolors.ENDC

def printblue(strs):
    print(bcolors.BLUE+strs+bcolors.ENDC)
def printred(strs):
    print(bcolors.RED+strs+bcolors.ENDC)
def printgreen(strs):
    print(bcolors.GREEN+strs+bcolors.ENDC)
def printyellow(strs):
    print(bcolors.YELLOW+strs+bcolors.ENDC)


def nodata(data,other_test=None):
    if data=="" or data==[] or data==None or len(data)==0:
        return True
    if type(data)==str:
        if data.lower().find("done")>=0 or data.lower().find("status")>=0:
            return True
    if type(data)==dict:
        if "status" in data and data['status'].lower()=="error":
            return True
    if other_test is not None:
        if other_test not in data:
            return True
    return False

def error_request(data,msg):
    if "error_message" in data:
        print(strred(" --> Error "+msg+" : "+data["error_message"]))
    else:
        print(strred(" --> Error "+msg +" : with no error message"))
    return False

def _get_pip_version(projet="morphonet"):
    '''
    Find the last available version of MorphoNet API
    '''
    import urllib.request
    fp = urllib.request.urlopen("https://pypi.org/project/"+projet)
    release__version=False
    for lines in fp.readlines():
        if release__version:
            return lines.decode("utf8").strip()
        if lines.decode("utf8").find("release__version")>0:
            release__version=True
    return "unknown"

def _check_version():
    '''
    Chekc if the API installed is the last version
    '''
    import pkg_resources
    current_version=None
    try :
        current_version = pkg_resources.get_distribution('morphonet').version
    except:
        print(' --> did not find current version of MorphoNet API ')

    online_version=None
    try:
        online_version = _get_pip_version()
    except:
        print(' --> did not last version of MorphoNet API ')

    if current_version is not None and online_version is not None and current_version != online_version:
        print(strblue("WARNING : please update your MorphoNet version : pip install -U morphonet "))
        return False
    return True

def RemoveLastTokensFromPath(path, nb):
    if nb>0:
        tokens = path.split(os.sep)
        if nb <= len(tokens):
            if tokens[len(tokens)-1] == "" or tokens[len(tokens)-1] is None:
                tokens = tokens[:-1]
            #print(tokens)
            tokens = tokens[:-nb]
            return os.sep.join(tokens)+os.sep
    if path[len(path)-1]!=os.sep:
        return path+os.sep
    return path
