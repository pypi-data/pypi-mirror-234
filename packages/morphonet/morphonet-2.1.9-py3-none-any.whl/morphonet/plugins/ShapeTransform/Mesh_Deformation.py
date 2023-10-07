# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from morphonet.tools import printv

import numpy as np
from .Deformation.DeformationAPI import initializeData, InvalidMeshDeformationException

class MeshDeformation(MorphoPlugin):
    """This plugin deforms the segmented image from the mesh data using a deformation made in unity

    Parameters
    ----------
    Objects:
        It can be apply on one selected object
    """
    def __init__(self): #PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_name("Manual mesh deformation")
        self.set_parent("Deformation")
        self.mesh_inputs = {}
        self._set_meshinput("mesh_morphing","mesh_morphing")
        self.set_description("This plugin allows you to manually deform your data using mesh deformation. It is to be "
                             "used with the mesh morphing menu and its various tools. First, the mesh morphing tool "
                             "allows you to manually deform a selected element of your dataset by applying various "
                             "transformations (move vertices, extrude, hollow, ...) with the mouse pointer. Once you "
                             "are satisfied with the deformation you applied to an element, This plugin propagates "
                             "the transformation(s) applied to the mesh to the segmented image in your dataset, "
                             "and regenerates the element using this segmented data.")
        


    def _get_btn(self):
        c=self._cmd()+";"+self.parent
        for tf in self.inputfields:
            c+=";IF_"+str(tf)
            if self.inputfields[tf] is not None:
                c+=";DF_"+str(self.inputfields[tf])
        for dd in self.dropdowns:
            c+=";DD_"+str(dd)+"_"
            for v in self.dropdowns[dd]:
                c+=str(v)+"_"
        for cd in self.coordinates:
            c+=";CD_"+str(cd)
        for mi in self.mesh_inputs:
            c+=";MI_"+str(mi)
        return c

    def _set_meshinput(self,text_name,value):
        self.mesh_inputs[text_name]=value

    def process(self, t, dataset, objects, mesh_deform): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects):
            return None

        if len(objects)!=1:
            printv("error : please select only one cell", 0)
        else:
            cells_updated=[]
            for cid in objects:
                o=dataset.get_object(cid)
                if o is not None:
                    data = dataset.get_seg(o.t)
                    
                    mesh = dataset.get_mesh_object(o)

                    """
                    scaledBorder = np.asarray([VoxelSize[2], VoxelSize[1], VoxelSize[0]]) * Border * factor
                    scaledCenter = np.asarray(center) * np.asarray([VoxelSize[2], VoxelSize[1], VoxelSize[0]])

                    point = np.asarray([v[2], v[1], v[0]]) * factor - scaledBorder - scaledCenter

                    -> pointScaling = factor
                    -> pointTranslation =  - scaledBorder - scaledCenter
                    """

                    border = 0
                    voxelSize = dataset.get_voxel_size(o.t)
                    voxelSize = np.array([voxelSize[2], voxelSize[1], voxelSize[0]])
                    factor = dataset.parent.factor
                    center = np.asarray(dataset.center)
                    scaledBorder = voxelSize * border * factor
                    #scaledCenter = center * voxelSize
                    scaledCenter = center
                    mesh_translation = scaledBorder + scaledCenter
                    mesh_scaling = 1.0 / voxelSize

                    try:
                        data = self.computeDeformation(data, mesh, mesh_deform[0], mesh_translation, mesh_scaling, dataset.background, o.id, o.t)
                    except InvalidMeshDeformationException as ex:
                        printv(f"Mesh error : {ex}", 0)
                    except Exception as ex:
                        printv(f"Generic error in deformation : {ex}", 2)
                    else:
                        cells_updated.append(o.id)
                        printv(f"Deformation succesfull on cell {o.t} {o.id}, processing results...", 0)

            if len(cells_updated) > 0:
                dataset.set_seg(o.t, data, cells_updated=cells_updated)
                printv(f"Computing new mesh{'es' if len(cells_updated) > 1 else ''} ...", 0)
            self.restart()

    def computeDeformation(self, data : np.array, mesh : str, mesh_deform : str, mesh_translation, mesh_scaling, background, cell=None, time=None, ):
        printv("Initializing deformation", 0)
        originalData, originalMesh, deformedData, deformedMesh, volume = initializeData(data, mesh, mesh_deform, mesh_translation, mesh_scaling, background, cell, time)

        volume.construct(originalMesh)

        volume.applyTransformation(originalData, originalMesh, deformedData, deformedMesh)

        return deformedData
