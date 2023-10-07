import pickle
from os import listdir
from os.path import join, dirname, basename, isfile, isdir, exists

import numpy as np
from morphonet.plot.Object import Object
from morphonet.plot.Property import Property
from morphonet.plot.ScikitProperty import ScikitProperty
from morphonet.plugins.functions import shift_bbox
from morphonet.tools import mkdir, printv, get_all_available_regionprops, _add_line_in_file, _read_last_line_in_file, \
    _load_seg, imsave, rmrf, cp, start_load_regionprops, calcul_regionprops_thread, _save_seg_thread, imread, \
    get_property_type, _set_dictionary_value, get_id_t, get_name, write_XML_properties



class Dataset():
    """Dataset class automatically created when you specify your dataset path in the seDataset function from Plot()

    Parameters
    ----------
    begin : int
        minimal time point
    end : int
        maximal time point
    raw : string
        path to raw data file where time digits are in standard format (ex: (:03d) for 3 digits  )(accept .gz)
    segment : string
        path to segmented data file  where time digits are in standard format  (accept .gz)
    log : bool
        keep the log
    background : int
        the pixel value of the background inside the segmented image
    xml_file : string
        path to the xml properties files (.xml)
    memory : int
        number of time step keep in memory durig curation (if you have memeory issue, decrease this number)
    temp_path : string
        temporary path to store all termporary data (but also curration)
    additional_properties : list of string
        additional scikit image properties to visuasile in the 3D wiever, list of available properties are here https://scikit-image.org/docs/stable/api/skimage.measure.html#skimage.measure.regionprops

    """

    def __init__(self, parent, begin=0, end=0, raw=None, segment=None, log=True, background=0, xml_file=None,memory=20,temp_path=".temp",additional_properties=None):
        assert begin<=end,'Time boundaries are not coherent ... '
        assert segment is not None or raw is not None,'Please specify either segmented or raw images'

        self.parent = parent
        self.begin = begin
        self.end = end
        self.log = log
        self.temp_path=temp_path
        self.properties_path=join(self.temp_path,"properties")
        mkdir(self.properties_path)
        self.annotations_path = join(self.temp_path, "annotations")
        mkdir(self.annotations_path)
        # List of Cells
        self.cells = {}

        # Prepare Step Folder
        self.step=self.get_last_step()
        self.step_folder = join(self.temp_path, str(self.step))
        if self.step == 0: mkdir(self.step_folder)  # Create the directory
        else:  printv(" Last step is " + str(self.step), 1)


        # raw data
        self.raw = False
        self.show_raw = None
        self.raw_path = None
        self.raw_datas = {}  # list of each rawdata time point
        if raw is not None:
            self.raw = True
            self.raw_path = dirname(raw) + "/"
            if dirname(raw) == "":
                self.raw_path = ""
            self.raw_files = basename(raw)

        # Segmentation
        self.seg_datas = {}  # list of each segmented time point
        self.voxel_size_by_t = {}
        self.segment_path = ""
        self.segment = segment
        self.segment_files = "curated_t{:03d}.inr.gz"
        self.center=None #Center of the images (we consider that center is fix throuth time and it's the same for raw and seg..)
        if segment is not None:
            self.segment_path = dirname(segment) + "/"
            if dirname(segment) == "":
                self.segment_path = ""
            self.segment_files = basename(segment)
            mkdir(self.segment_path)  #To be able to perform a first segmentation
        self.seeds = None  # To Send Centers to Unity

        # Define temporary name for segmented file in compress numpy format
        if self.segment is not None and self.segment !="":
            f = basename(self.segment)
        elif self.raw_datas is not None and self.raw_datas !="":
            f = basename(self.raw_files)
        self.temp_segname = f[:f.index('.')] + ".npz" #To save each step of the curation

        # LOG
        self.log_file = "morpho_log.txt"
        self.background = background  # Background Color

        # DATA Management
        self.memory = memory  # Memory to store dataset in Gibabytes
        self.lasT = []  # List of last time step
        self.times_updated = []  # List of modified time point

        #SCIKIT PROPERTIES (From regions scikit image)
        self.regions={} #List of Regions Properties  (from scikit image) (compute first)
        self.regions_thread={} #List of running thread to compute regions properties
        self.regionprops_name = ['area',"bbox","centroid"] #Minimum required properties
        available_regionprops=get_all_available_regionprops()
        if additional_properties is not None:
            for p in additional_properties:
                if p in available_regionprops and p not in self.regionprops_name:
                    self.regionprops_name.append(p)
        #Init Properties
        self.regionprops = {}  # List of Regions Properties (from scikit image)
        for p in self.regionprops_name:
            self.regionprops[p] = ScikitProperty(self, p, available_regionprops[p])

        # PROPERTIES
        self.xml_properties_type={} #Save All Avaiable Properties (fom XML )
        self.properties = {}  # Stored all Properties
        self.read_properties() #Read All stored Properties
        self.read_last_properties() #Read All stored version
        self.xml_file = xml_file  # Xml Properties
        if  self.xml_file is not None:
            if "cell_lineage" not in self.properties:
                self.read_xml(self.xml_file,property="cell_lineage")  #Read the lineage from the XML the fist time
            else:
                self.read_xml(self.xml_file) #Jsut Read all the details of the preoperties

        # Cell to update
        self.cells_updated = {} #[t] = None -> All Cells;  [t]=[] -> Nothing; [t]=[1] -> Cell 1


    def restart(self, plug,label=None):  # Apply and Restart a Curation
        """Restart the curation mode after execution of a specific plugin

        Parameters
        ----------
        plug : MorphoPlug
            the plugin just executed

        Examples
        --------
        >>> dataset.restart(fuse)
        """
        self.parent.restart(self.times_updated,label=label)
        self.times_updated = []
        if plug is not None:
            printv("End Of " + str(plug.name),1)

    ######### SAVE ALL STEPS OF CURATION

    def get_last_version(self,filename,step_only=False):
        '''
        Return the last file is exist in order of last steps first
        '''

        bc=self.step
        while bc>=0:
            f=join(self.temp_path,str(bc),filename)
            if isfile(f):
                if step_only:  return bc
                return f
            bc-=1
        if step_only:  return 0
        return None

    def get_last_step(self):
        '''
        Return the last step version
        '''
        bc = 0
        while isdir(join(self.temp_path, str(bc))):
           bc+=1
        if bc==0:
            return 0
        return bc-1

    def start_step(self,command,exec_time):
        '''
        Prepare the step folder and save the command to the log file system
        '''
        printv("Increase Step at "+str(self.step+1),1)
        self.step += 1  # Increase Step
        self.step_folder = join(self.temp_path, str(self.step))
        mkdir(self.step_folder)  # Create the directory

        # SAVE ACTION
        if not isfile(join(self.step_folder, "action")):
            _add_line_in_file(join(self.step_folder, "action"), str(command))

        # Add the command to the log file
            _add_line_in_file(self.log_file,str(self.step) + ":" + str(command) + str(exec_time.strftime("%Y-%m-%d-%H-%M-%S")) + "\n")

        #Initialisation times points
        self.times_updated = []

    def end_step(self):
        '''
        Save the lineage after performing an action
        '''
        printv("Finalise Step " + str(self.step),1)
        #EXPORT SOME PROPERTIES
        properties_to_save=["cell_lineage"]
        for property_name in properties_to_save:
            if property_name in self.properties:
                self.properties[property_name].export(filename=join(self.step_folder,property_name+".txt"))

    def cancel(self):
        '''
        Cancel the last action (by put the STEP back)
        '''
        if self.step<=0:
            printv("Nothing to cancel",0)
            return None
        printv("Cancel Step " + str(self.step),1)
        del_step_folder=self.step_folder #We have to delete the current step folder
        self.step-=1 #Decreate Step
        self.step_folder = join(self.temp_path, str(self.step))

        # READ COMMAND
        label = ""
        if isfile(join(del_step_folder, "action")):
            action = _read_last_line_in_file(join(del_step_folder, "action"))
            printv("Cancel " + action.replace(":"," ").replace(";"," "),0)

            # Retrieve the list of cells
            for a in action.split(";"):
                if a.strip().startswith("ID:"):
                    objts = a[a.find('[') + 1:a.find(']')].split("',")
                    for o in a[a.find('[') + 1:a.find(']')].split("',"):
                        label += o.replace("'", "") + ";"

        # RESTORE LINEAGE
        self.clear_lineage()
        for property_name in ["cell_lineage"]:
            if property_name in self.properties:
                filename=join(self.step_folder, property_name + ".txt")
                if isfile(filename):

                    self.properties[property_name].read(filename)
                else: #We have to remove completly the lienage
                    self.properties[property_name].todelete=True

        # RESTORE Images
        self.times_updated = []
        for t in range(self.begin, self.end + 1): #List images to restore
            if isfile(join(del_step_folder,self.temp_segname.format(t))):
                filename = self.get_last_version(self.temp_segname.format(t))
                if filename is  None:  printv("ERROR , we should have something somewhere .. ",2)
                self.seg_datas[t], vsize = _load_seg(filename)  # Read Image
                self.set_voxel_size(t,vsize)
                self.read_regionprops_at(t, filename)  # Read regions propertyes
                #Meshes are automatically reload from compute_meshes
                self.times_updated.append(t)

        # REMOVE STEP FOLDER
        rmrf(del_step_folder)

        self.parent.restart(self.times_updated, label=label)

    def get_actions(self):
        '''
        Return all actions in order #TODO SEND TO UNIT

        '''
        actions=[]
        for s in range(1,self.step):
            action_file=join(self.temp_path, str(s), "action")
            if not isfile(action_file):
                printv("ERROR miss action file "+action_file,0)
                actions.append("MISS ACTION FILE")
            else:
                action = _read_last_line_in_file(action_file)
                actions.append(action.replace(" ","_").replace(",",".").replace(";",":"))
        return actions

    def export(self,export_path,image_file_type="nii.gz"):
        '''
        Export all the dataset with the last version of each file
        '''
        mkdir(export_path)
        last_step=self.get_last_step()

        #EXPORT IMAGES
        for t in range(self.begin, self.end + 1):  # List images to restore
            s=last_step
            while s>0 and not isfile(join(self.temp_path, str(s), self.temp_segname.format(t))):
                s-=1
            if not isfile(join(self.temp_path, str(s), self.temp_segname.format(t))):
                printv("ERROR did not find any backup for "+self.temp_segname.format(t),1)
            else:
                data, vsize =_load_seg(join(self.temp_path, str(s), self.temp_segname.format(t)))
                self.set_voxel_size(t, vsize)
                filename=join(export_path,self.temp_segname.format(t).replace("npz",image_file_type))
                printv("export segmented image at "+str(t)+" to "+filename,1)
                imsave(filename,data,voxel_size=vsize)

        #EXPORT PROPERTIES
        property_exported=[]
        s = last_step
        while s>=0:
            for f in listdir(join(self.temp_path, str(s))):
                if isfile(join(self.temp_path, str(s),f) )and f.endswith("txt"):
                    property_name=f.replace(".txt","")
                    if property_name not in property_exported:
                        printv("export property to "+join(export_path,f),1)
                        cp(join(self.temp_path, str(s),f),export_path)
                    property_exported.append(property_name)
            s-=1


    # OBJECT ACCESS

    def get_object(self, *args):
        """Get an MorphoObject from a list of arguments (times, id, ... )

        Parameters
        ----------
        *args : list of arugemnts
            the arguments which define the object, with at least 1 argument (object id with time =0 )

        Return
        ----------
        MorphoObject class

        Examples
        --------
        >>> dataset.get_object(1,2)
        """
        t = 0
        id = None
        s = None  # label
        tab = args
        if len(args) == 1:
            tab = args[0].split(",")

        if len(tab) == 1:
            try:
                id = int(tab[0])
            except:
                id = int(float(tab[0]))
        elif len(tab) >= 2:
            try:
                t = int(tab[0])
            except:
                t = int(float(tab[0]))
            try:
                id = int(tab[1])
            except:
                id = int(float(tab[1]))
        if len(tab) >= 3:
            try:
                s = int(tab[2])
            except:
                s = int(float(tab[2]))

        if id is None:
            printv(" Wrong parsing  " + str(args[0]),1)
            return None

        if t not in self.cells:
            self.cells[t] = {}
        if id not in self.cells[t]:  # CREATION
            self.cells[t][id] = Object(t, id)

        if s is not None:
            self.cells[t][id].s = s

        return self.cells[t][id]

    def get_times(self, objects):
        '''
        Return the order list of time points corresponding to the list of objects
        '''
        times = []
        for cid in objects:  # List all time points
            o = self.get_object(cid)
            if o is not None and o.t not in times:
                times.append(o.t)
        times.sort()  # Order Times
        return times

    def get_objects(self, objects):
        '''
        Return the list of objects from string format
        '''
        all_objects=[]
        for cid in objects:
            o = self.get_object(cid)
            if o is not None:
                all_objects.append(o)
        return all_objects

    def get_objects_at(self, objects, t):
        '''
        Return the list of objects at a specific time point
        '''
        time_objects=[]
        for cid in objects:
            o = self.get_object(cid)
            if o is not None and o.t == t:
                time_objects.append(o)
        return time_objects

    def get_all_objects_at(self, t):
        '''
        Return the list of objects at a specific time point
        '''
        time_objects=[]
        if t in self.cells:
            for idc in self.cells[t]:
                time_objects.append(self.cells[t][idc])
        return time_objects

    ##### DATA ACCESS

    def _set_last(self, t):
        if t in self.lasT:  self.lasT.remove(t)
        self.lasT.append(t) #Put at the end
        if t not in self.seg_datas:
            if self._get_data_size() > self.memory * 10 ** 9:
                remove_t = self.lasT.pop(0)
                printv("Remove from memory time " + str(remove_t),2)
                if remove_t in self.regions_thread:
                    self.regions_thread[remove_t].join()
                if remove_t in self.seg_datas:
                    del self.seg_datas[remove_t]
                if remove_t in self.raw_datas:
                    del self.raw_datas[remove_t]

    def _get_data_size(self):
        sif = 0
        for t in self.seg_datas:
            if self.seg_datas[t] is not None:
                sif += self.seg_datas[t].nbytes
        return sif

    #### SCIKIT IMAGE PROPERTY (Volume, bouding box, etc ...)

    def _regionprops_filename(self,filename):
        return filename.replace(".npz", ".regions.pickle")

    def start_load_regionprops(self):#We launch the loading of all properties but sequentiallty without lociking the proce
        st=start_load_regionprops(self)
        st.start()

    def load_regionprops_at(self,t,filename=None,recompute=False):
        printv("load Regions Properties at " + str(t), 2)
        if filename is None : filename = self.get_last_version(self.temp_segname.format(t))
        if filename is None: return None
        if not self.read_regionprops_at(t, filename) or recompute:  # FIRST READ IT
            if not isfile(filename):
                printv("error : miss segmentation file name "+filename,-1)
                return None
            if t not in self.seg_datas or self.seg_datas[t] is None:
                self.seg_datas[t], vsize = _load_seg(filename)  # Read Image
            self.compute_regionprops(t,filename=filename,wait=True)  # Compute region properties

    def read_regionprops_at(self,t,filename):
        if filename is None : return False
        f=self._regionprops_filename(filename)
        if isfile(f):
            printv("read properties file "+f,1)
            with open(f, "rb") as infile:
                prop  = pickle.load(infile)
                for c in prop:
                    for p in prop[c]:
                        if p in self.regionprops:
                            self.regionprops[p].set(self.get_object(t, c), prop[c][p]) #FILL THE PROPERTY
            return True
        return False

    def compute_regionprops(self,t,filename=None,wait=False):
        if t not in self.seg_datas: return None
        if t in self.regions_thread:
            printv("region properties thread is already running at "+str(t),2)
        else:
            if filename is None: filename=join(self.step_folder, self.temp_segname.format(t))
            self.regions_thread[t] = calcul_regionprops_thread(self, t,self._regionprops_filename(filename),self.regionprops_name,background=self.background)
            self.regions_thread[t].start()
        if wait:
            self.regions_thread[t].join() #Wait the end of the calculs
            self.regions_thread[t].sr.join()

    def get_stored_regionprop(self,property,mo):
        if property not in self.regionprops:
            printv("error this propety does not exist ... " + property, -1)
            return None

        #Property is already computed and well store
        prop=self.regionprops[property].get(mo)
        if prop is not None : return prop

        #Look in the region class from scikit image (temporary used before stored in self.regionprops)
        if mo.t in self.regions:
            for r in self.regions[mo.t]:
                if r['label']==mo.id:
                    return r[property]

        return None

    def get_regionprop(self,property,mo):
        '''
        Return a given property for a specific cell at a specific time point
        '''
        #Property is already computed and well store
        prop=self.get_stored_regionprop(property,mo)
        if prop is not None : return prop

        #Sill running ?
        if mo.t in self.regions_thread:
            self.regions_thread[mo.t].join() #Wait for the end of the calcul
            prop = self.get_stored_regionprop(property, mo)
            if prop is not None: return prop

        #We look if a file exist
        if self.read_regionprops_at(mo.t, self.get_last_version(self.temp_segname.format(mo.t))):
            prop = self.get_stored_regionprop(property, mo)
            if prop is not None : return prop


        #We launch the calcul
        self.compute_regionprops(mo.t,wait=True)
        prop = self.get_stored_regionprop(property, mo)

        return prop

    def get_regionprop_at(self,property,t,ordered=False):
        '''
        Return a given property for all cells at a specific time point
        Returns a dictionnary of cell -  propertu value
        '''

        if property not in self.regionprops:
            printv("error this propety does not exist ... " +property,-1)
            return None

        #Property is already computed and well store
        properties=self.regionprops[property].get_at(t)

        #Look in the region class from scikit image (temporary used before stored in self.regionprops)
        if properties is None and t in self.regions:
            properties = {}
            for r in self.regions[t]:
                properties[Object(t,r['label'])]=r[property]

        if properties is not None:
            if ordered:  properties = dict(sorted(properties.items(), key=lambda item: item[1]))
            return properties

        #Sill running ?
        if t in self.regions_thread:
            self.regions_thread[t].join() #Wait for the end of the calcul
            return self.get_regionprop_at(property,t,ordered=ordered) #Relaunch the same function (but calcul will be finished)

        #We look if a file exist
        if self.read_regionprops_at(t, self.get_last_version(self.temp_segname.format(t))):
            return self.get_regionprop_at(property,t,ordered=ordered)  # Relaunch the same function (but reading will be finished)

        #We launch the calcul
        self.compute_regionprops(t,wait=True)
        return self.get_regionprop_at(property,t,ordered=ordered)  # Relaunch the same function (but wait for calcul will be finished)

    def get_mask_cell(self,mo,border):
        '''
        Return a given property for a specific cell at a specific time point
        '''
        bbox=self.get_regionprop("bbox",mo)
        data = self.seg_datas[mo.t]
        bbox=shift_bbox(bbox,border=border,shape=data.shape)
        return data[bbox[0]:bbox[1],bbox[2]:bbox[3],bbox[4]:bbox[5]]

    def wait_regionprops(self):
        printv("wait all regions properties ",2)
        t=0
        while len(self.regions_thread)>0 and t<self.end:
            if t in self.regions_thread:
                self.regions_thread[t].join() #Wait for all threads ended
                self.regions_thread[t].sr.join() #Wait for all saved ended
            t+=1
        printv("finish to compute all properties ",2)

    #### FAST SELECTION COMMAND
    def np_where(self,mo):
        '''
        is equal to np.where(data==mo.id)
        '''
        if mo.t not in self.seg_datas: return
        data=self.seg_datas[mo.t]
        bbox = self.get_regionprop("bbox",mo)
        if bbox is not None:
            databox=data[bbox[0]:bbox[3],bbox[1]:bbox[4],bbox[2]:bbox[5]]
            coords=np.where(databox == mo.id)
            return (coords[0]+bbox[0],coords[1]+bbox[1],coords[2]+bbox[2])
        return ([],[],[])

    def set_cell_value(self,mo,v):
        # is equal to data[np.where(data==c)]=v
        if mo.t not in self.seg_datas: return
        data = self.seg_datas[mo.t]
        bbox = self.get_regionprop("bbox",mo)
        if bbox is not None :
            databox = data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]
            databox[np.where(databox == mo.id)]=v
            data[bbox[0]:bbox[3], bbox[1]:bbox[4], bbox[2]:bbox[5]]=databox
        return data

    ###### SEGMENTATION
    def set_seg(self, t, data, cells_updated=None):
        """Define the segmented data at a specitic time point (Used in the plugins )
        Call this function when you modifiy something in the data

        Parameters
        ----------
        t : int
            the time point
        data : numpy matrix
            the segmented image
        cells_updated (optional): list
            list of cell just udpated by the plugin (in order to compute faster)

        Examples
        --------
        >>> dataset.set_seg(1,data)
        """
        self.seg_datas[t] = data
        if t not in self.times_updated: self.times_updated.append(t)
        self.cells_updated[t]=cells_updated
        self._save_seg(t,data) #Save the data
        self.compute_regionprops(t)
        #TODO WE HAVE TO DUPLICATE THE CELL VTK PATH FROM THE PREVIOUS STEP IN ORDER TO AVOIR RECOMPUTING ALL CELLS
        self.parent.compute_mesh(t,data) #We compute it here (and also in plot mesh) to start the thread


    def set_voxel_size(self,t,vsize,force=False):
        if vsize is not None:
            if force :
                self.voxel_size_by_t[t]=vsize
            elif t not in self.voxel_size_by_t or self.voxel_size_by_t[t] is None:
                self.voxel_size_by_t[t]=vsize

    def get_voxel_size(self,t,txt=False):
        vsize = None
        if self.parent.voxel_override:
            vsize = self.parent.voxel_size
        elif t in self.voxel_size_by_t:
            vsize = self.voxel_size_by_t[t]
        if vsize is None:
            vsize = (1, 1, 1)
        if txt:
            return str(vsize[0]) + "_" + str(vsize[1]) + "_" + str(vsize[2])
        else:
            return vsize

    def _save_seg(self, t, data=None):
        if data is None:
            data = self.seg_datas[t]
        else:
            self.seg_datas[t] = data
        filename=join(self.step_folder ,self.temp_segname.format(t))
        if not isfile(filename):
            sst = _save_seg_thread(filename, data, self.get_voxel_size(t))
            sst.start()

    def get_raw(self, t):
        """Get the rawdata data at a specitic time point

        Parameters
        ----------
        t : int
            the time point
        Return
        ----------
        numpy matrix
            the raw data

        Examples
        --------
        >>> dataset.get_raw(1)
        """
        if self.raw_path is None:
            printv("miss raw path",1)
            return None
        filename = join(self.raw_path, self.raw_files.format(t))
        if not isfile(filename):
            printv(" Miss raw file " + filename,1)
            return None
        if t not in self.raw_datas:
            self.raw_datas[t],vsize = imread(join(self.raw_path, self.raw_files.format(t)),voxel_size=True)
            self.set_voxel_size(t,vsize,force=True)
            self.get_center(self.raw_datas[t])
        self._set_last(t)  # Define the time step as used
        return self.raw_datas[t]

    def get_seg(self, t, reload=False):
        """Get the segmented data at a specitic time point

        Parameters
        ----------
        t : int
            the time point

        Return
        ----------
        numpy matrix
            the segmented image

        Examples
        --------
        >>> dataset.get_seg(1)
        """
        self._set_last(t)  # Define the time step as used
        if t not in self.seg_datas or reload:
            self.seg_datas[t] = None
            filename=self.get_last_version(self.temp_segname.format(t))
            self.seg_datas[t],vsize=_load_seg(filename) # Look in the previous step folder
            if self.seg_datas[t] is None:  #First time ,  we read the original data
                if self.segment_files is not None and isfile(join(self.segment_path, self.segment_files.format(t))):
                    self.seg_datas[t],vsize = imread(join(self.segment_path, self.segment_files.format(t)),voxel_size=True)
                    self.set_voxel_size(t,vsize)
                    self._save_seg(t) #Save it in npz the first time we load the data
                    
            self.set_voxel_size(t,vsize)
            if self.seg_datas[t] is not None: self.load_regionprops_at(t,filename=filename) #Launc the compute properties in // or load it if already exist
        return self.seg_datas[t]

    def get_center(self,data=None,txt=False):  # Calculate the center of a dataset
        """Get the barycnetr of an matrix passed in argument

        Parameters
        ----------
        data : numpy matrix
            the 3D image (could be segmented or rawdata)

        Return
        ----------
        list of coordinates
            the barycenter of the image

        Examples
        --------
        >>> center=dataset.get_center(seg)
        """
        center_filename=join(self.temp_path,"center.npy")
        print("center file : "+str(center_filename))
        print("Already exisitng center : "+str(self.center))
        if self.center is None:
            if isfile(center_filename):
                print("load from filename")
                self.center=np.load(center_filename)

        if self.center is None and data is not None:
            print("Load from data")
            self.center = [np.round(data.shape[0] / 2), np.round(data.shape[1] / 2), np.round(data.shape[2] / 2)]

        if self.center is None:
            for t in self.seg_datas:
                if self.center is None and self.seg_datas[t] is not None:
                    print("Center from seg at t : "+str(t))
                    self.center = [np.round(self.seg_datas[t].shape[0] / 2), np.round(self.seg_datas[t].shape[1] / 2), np.round(self.seg_datas[t].shape[2] / 2)]

        if self.center is None:
            printv("Error miss center ",-1)
            if txt: return "0_0_0"
            else: return [0,0,0]

        print("Final center : "+str(self.center))

        if self.center is not None and not isfile(center_filename):
            print("writing file")
            np.save(center_filename,self.center)

        if txt: return str(int(round(self.center[0]))) + "_" + str(int(round(self.center[1]))) + "_" + str(int(round(self.center[2])))
        return self.center


    def get_mesh(self,t):
        """
        Return the full mesh at t
        """
        return self.parent.compute_mesh(t)

    def get_mesh_object(self,mo):
        '''
        Return the specific mesh of the object
        '''
        return self.parent.get_mesh_object(mo)


    ###### SEEDS
    def add_seed(self, seed):
        """Add a seed in the seed list

        Parameters
        ----------
        seed : numpy array
            the coordinate of a seed


        Examples
        --------
        >>> dataset.add_seed(np.int32([23,34,45]),1)
        """

        if self.seeds is None:
            self.seeds = []
        center = self.get_center()
        printv("Create a seed at " + str(seed[0]) + "," + str(seed[1]) + "," + str(seed[2]),0)
        self.seeds.append(np.int32([seed[0] - center[0], seed[1] - center[1], seed[2] - center[2]]))

    def get_seeds(self):
        """Return the list of seeds as string

        Examples
        --------
        >>> seeds=mc.get_seeds()
        """

        if self.seeds is None or len(self.seeds) == 0:
            return None
        strseed = ""
        for s in self.seeds:
            strseed += str(s[0]) + "," + str(s[1]) + "," + str(s[2]) + ";"
        self.seeds = None  # Reinitializeation
        return strseed[0:-1]

    #####PROPERTIES FUNCTIONS

    def read_last_properties(self):
        """
        Read the last version of eacch property from the various step folder (FOR CELL LINEAGE)
        -------
        """
        bc = self.step
        while isdir(join(self.temp_path, str(bc))):
            for filename in listdir(join(self.temp_path, str(bc))):
                if isfile(join(self.temp_path, str(bc), filename)) and filename.endswith(
                        ".txt"):  # All files finishing with txt are property
                    property_name = filename.replace(".txt", "")
                    if property_name not in self.properties:  # Not already read before
                        inf = self.get_property(property_name)
                        inf.read(join(self.temp_path, str(bc), filename))
            bc -= 1

    def read_properties(self):
        """
        Read the properties  from the property folder
        -------
        """
        #Read All Properties
        for filename in listdir(self.properties_path):
            if isfile(join(self.properties_path,filename)) and filename.endswith(".txt"):  # All files finishing with txt are properties
                property_name = filename.replace(".txt", "")
                if property_name not in self.properties:  # Not already read before
                    inf = self.get_property(property_name)

                    #Look if there is a correspondant annotation
                    if isfile(join(self.annotations_path,filename)):
                        inf.read_annotation(join(self.annotations_path, filename))
                    else:
                        inf.read(join(self.properties_path, filename))

    def get_property(self, property_name, property_type=None, reload=False, create=True):
        """
        Return the property for the dataset
        """
        if property_type is None:
            property_type = get_property_type(property_name)
            if property_type is None:
                property_type = "string"

        if reload and property_name in self.properties:  # Clear Property
            self.properties[property_name].clear()

        if property_name not in self.properties and create:  # Create a new one
            self.properties[property_name] = Property(self, property_name, property_type)

        if property_name not in self.properties:
            return None
        return self.properties[property_name]

    ##### XML
    def read_xml(self, filename, property=None, all=True, export=True):
        if filename is None or not exists(filename) or not filename.endswith("xml"):
            printv('properties file missing ' + str(filename), 2)
            return None

        if all: self.xml_properties_type = {}
        import xml.etree.ElementTree as ElementTree
        inputxmltree = ElementTree.parse(filename)
        root = inputxmltree.getroot()
        for child in root:
            property_name = child.tag
            if property_name not in self.regionprops_name:
                property_type = get_property_type(property_name)
                if all: self.xml_properties_type[property_name] = property_type
                if property is not None and child.tag == property:
                    printv("Read " + child.tag, 0)
                    prop = _set_dictionary_value(child)
                    inf = self.get_property(property_name, property_type=property_type)
                    if type(prop) == list:  # List of Cells
                        for idl in prop:
                            t, c = get_id_t(idl)
                            mo = self.get_object(get_name(t, c))
                            inf.set(mo, 1)
                    else:  # DICT
                        for idl in prop:
                            t, c = get_id_t(idl)
                            mo = self.get_object(get_name(t, c))
                            if property_type == 'time':
                                daughters = []
                                for daughter in prop[idl]:
                                    td, d = get_id_t(daughter)
                                    do = self.get_object(get_name(td, d))
                                    do.add_mother(mo)
                                    daughters.append(do)
                                inf.set(mo, daughters)
                            else:
                                if type(prop[idl]) == list:
                                    for elt in prop[idl]:
                                        inf.set(mo, elt)
                                else:
                                    inf.set(mo, prop[idl])
                    if export:
                        if property_type == 'time':
                            inf.export(filename=join(self.step_folder, inf.name + ".txt"))  # Cell Lineage
                        else:
                            inf.export()  # We directly save it in MorphoNet Format

        if all: printv("Property found in the XML file  " + str(self.xml_properties_type.keys()), 1)

    def export_xml(self, filename):
        if filename is not None:
            properties = {}
            for property_name in self.properties:
                inf = self.properties[property_name]
                property_name_w = property_name
                if (inf.property_type == "selection" and property_name.find("selection_") == -1) or (inf.property_type == "label" and property_name.find("label_") == -1):
                    property_name_w = "label_" + property_name
                properties[property_name_w] = inf.get_dict()
            write_XML_properties(properties, filename)

    ################## TEMPORAL FUNCTIONS

    def clear_lineage(self):
        if "cell_lineage" in self.properties:
            self.properties["cell_lineage"].clear()
        for t in self.cells:
            for cid in self.cells[t]:
                self.cells[t][cid].clear_temporal_links()

    def _get_at(self, objects, t):
        cells = []
        for cid in objects:
            o = self.get_object(cid)
            if o is not None and o.t == t:
                cells.append(o)
        return cells

    def add_link(self, c1, c2):
        """Create a temporal link in the lineage between two object

        Parameters
        ----------
        c1 : MorphoObject
            the  cell
        c2: MorphoObject
            the other cell


        Examples
        --------
        >>> mc.add_link(c,m)
        """
        if c1 is None or c2 is None:   return False

        if c1.t<c2.t:   return self.add_daughter(c1, c2)
        return self.add_daughter(c2, c1)

    def add_mother(self, c, m):
        """Create a temporal PAST link in the lineage

        Parameters
        ----------
        c : MorphoObject
            the  cell
        m : MorphoObject
            the mother cell


        Examples
        --------
        >>> mc.add_mother(c,m)
        """
        if c is None or m is None:
            return False
        return self.add_daughter(m, c)

    def del_link(self, c1, c2):
        """Delete any temporal link between c1 and c2

        Parameters
        ----------
        c1 : MorphoObject
            the  cell
        c2 : MorphoObject
            the pther cell


        Examples
        --------
        >>> mc.del_link(c,d)
        """
        if c1 is None or c2 is None:
            return False
        if c1.t<c2.t : return self.del_daughter(c1,c2)
        return self.del_daughter(c2, c1)


    def del_mother(self, c, m):
        """Remove a temporal FUTUR link in the lineage

        Parameters
        ----------
        c : MorphoObject
            the  cell
        m : MorphoObject
            the mother cell


        Examples
        --------
        >>> mc.del_mother(c,m)
        """
        if c is None or m is None:
            return False
        return self.del_daughter(m,c)

    def del_cell_from_properties(self,cell):
        """ Delete a cell from properties (

        Parameters
        ----------
        cell : MorphoObject
            the  cell

        """
        updated = False
        if cell is None:
            print("Error during cell deletion from properties")
            return False

        infos_name = self.properties
        for name in infos_name:
            inf = infos_name[name]
            value = inf.get(cell)
            inf.del_annotation(cell,value)
            inf.updated = True
            updated = True
        return updated


    def del_daughter(self, c, d):
        """Create a temporal PAST link in the lineage

        Parameters
        ----------
        c : MorphoObject
            the  cell
        d : MorphoObject
            the daughter cell


        Examples
        --------
        >>> mc.del_daughter(c,d)
        """
        if c is None or d is None:
            return False
        if c.del_daughter(d):
            inf = self.get_property("cell_lineage", property_type="time")
            inf.updated = True
            inf.del_annotation(c,d)
            return True
        return False


    def add_daughter(self,c, d):
        """Create a temporal FUTUR link in the lineage

        Parameters
        ----------
        c : MorphoObject
            the  cell
        d : MorphoObject
            the daughter cell

        Examples
        --------
        >>> mc.add_daughter(c,d)
        """
        if c is None or d is None:
            return False
        if c.add_daughter(d):
            inf = self.get_property("cell_lineage", property_type="time")
            inf.set(c,d) #Add this new cell s
            inf.updated = True
            return True
        return False


    #DEPRECATED FUNCS
    def read_infos(self):
        printv("deprecated please use read_properties() ",2)
        return self.read_properties()

    def get_info(self, info_name, info_type=None, reload=False, create=True):
        printv("deprecated please use get_property() ", 2)
        return self.get_property(property_name=info_name,property_type=info_type,reload=reload,create=create)

    




