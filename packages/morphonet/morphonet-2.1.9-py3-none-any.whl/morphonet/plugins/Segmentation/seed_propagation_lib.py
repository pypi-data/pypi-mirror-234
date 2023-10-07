from ...tools import printv
from ..functions import  get_borders, force_apply_new_label,watershed,get_barycenter,gaussian

def remove_background(value,background):
    if value == background:
          return False

    return True

#Get the coordinates of all ids in the image
def get_coords_indexes_in_image(image,list_ids):
    import numpy as np
    result = np.where(image==list_ids[0])
    i = 0
    for cell in list_ids:
        if i > 0:
            result = np.concatenate((result,np.where(image==cell)),axis=1)
        i += 1
    return result

def get_list_of_selections(dataset,objects):
    selections = {}
    for cid in objects:
        o = dataset.get_object(cid)
        if o is not None:
            if o.s not in selections:
                selections[o.s] = []
            selections[o.s].append(o)
    if len(selections) > 1:
        printv(" --> Found  " + str(len(selections)) + " selections ", 0)
    return selections


def process_at(t, input_cells, dataset, next_t, min_vol, forward=True, use_raw_images=False, s_sigma=0):
    import numpy as np
    printv("Processing propagation of seeds from time " + str(t) + " towards " + str(next_t), 1)
    # Load current time point segmentation
    data_t = dataset.get_seg(t)
    # Load next time point segmentation
    data_next_t = dataset.get_seg(next_t)
    # COMPUTE BARYUCENTERS
    barycenter_for_id = {}
    ids_next_for_id = {}
    # For each cell
    for o in input_cells:
        # Get its barycenter
        barycoord = get_barycenter(data_t, o)
        # Store it in the memory for computation
        barycenter_for_id[o] = barycoord
        # Store id of the cells at next t to remove informations if cell is updated
        ids_next_for_id[o] = data_next_t[barycoord[0], barycoord[1], barycoord[2]]
    idnextcells = []
    is_mask_missing = False

    # Among the cells to split, detect if at least one is background in next t, to determine in which case we're going to computer
    for o in ids_next_for_id:
        if ids_next_for_id[o] == dataset.background:
            is_mask_missing = True
        else:
            idnextcells.append(ids_next_for_id[o])

    # Data of the time that will be modified
    printv("Compute the mask of the working cell at time " + str(t), 1)

    mask = None
    # Compute the mask depending of the situation we're in
    ###### CASE 1 : 1 or multiple masks missing
    if is_mask_missing:
        printv("Mask missing case", 1)
        # Get all cells to propagate bounding box
        cellCoords = get_coords_indexes_in_image(data_t, list(barycenter_for_id.keys()))
        xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data_t, cellCoords)
        # Increase bouding box to be sure we work in the complete cells
        xmin -= 10
        xmax += 10
        ymin -= 10
        ymax += 10
        zmin -= 10
        zmax += 10
        cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
        mask = np.zeros(cellShape, dtype=bool)
        mask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True
        # Remove from mask the voxels of next that are not a cell
        unmask_cells_coords = np.where(
            data_next_t[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2]] != dataset.background)
        mask[unmask_cells_coords] = False


    ####### CASE 2 : no mask missing
    ####mask=mask_celluls_nextt
    else:
        printv("No mask missing case", 1)
        # Get all cells to propagate bounding box
        cellCoords = get_coords_indexes_in_image(data_next_t, idnextcells)
        xmin, xmax, ymin, ymax, zmin, zmax = get_borders(data_next_t, cellCoords)
        # Increase bouding box to be sure we work in the complete cell
        xmin -= 10
        xmax += 10
        ymin -= 10
        ymax += 10
        zmin -= 10
        zmax += 10
        cellShape = [1 + xmax - xmin, 1 + ymax - ymin, 1 + zmax - zmin]
        mask = np.zeros(cellShape, dtype=bool)
        mask[cellCoords[0] - xmin, cellCoords[1] - ymin, cellCoords[2] - zmin] = True

    # CREATE MARKERS
    markers = np.zeros(mask.shape, dtype=np.uint16)
    # Find the next unsused id in segmentation for the cells created
    newId = np.max(data_next_t) + 1
    printv("Marking cell in image masked of time " + str(next_t), 1)
    # For each id in cells
    for o in barycenter_for_id:  # For Each Barycenters  ...
        # Seedd coordinates are cell barycenter
        seed = barycenter_for_id[o]
        # If barycenter was computed correctly
        if not seed[0] == 0 and not seed[1] == 0 and not seed[2] == 0:
            printv("Adding marker : " + str((seed[0], seed[1], seed[2])) + " with id : " + str(newId), 1)
            # Adding seed for watershed
            markers[seed[0] - xmin, seed[1] - ymin, seed[2] - zmin] = newId
            newId += 1
        else:
            printv("Errors during computation of one barycenter", 1)
    source = 255-mask
    if use_raw_images:
        # Load raw data
        rawdata = dataset.get_raw(next_t)
        if rawdata is None:
            printv("ERROR : Missing Raw Images at time : " + str(next_t), 0)
            return [], None
        # Get the mask computed before in the raw data
        seed_preimage = rawdata[xmin:xmax + 1, ymin:ymax + 1, zmin:zmax + 1]
        # If user chosen to smooth the raw data, smooth it with a gaussian soothing
        if s_sigma > 0.0:
            printv("Perform gaussian with sigma=" + str(s_sigma) + " at " + str(t), 0)
            source = gaussian(seed_preimage, sigma=s_sigma, preserve_range=True)

    printv(" --> Process watershed ", 0)
    # Compute new segmentation in the mask using seeds
    labelw = watershed(source, markers=markers, mask=mask)
    # apply the new labels got by the watershed
    printv("Apply new label " + str(labelw[labelw != 0]), 1)
    # apply new segmentation to the image
    data_next_t, c_newIds = force_apply_new_label(data_next_t, xmin, ymin, zmin, labelw, minVol=min_vol,
                                                  minimal_count=1)
    # If cells have been created in the process (could be empty if volume count fail)
    cells_updated_at_t = []
    if len(c_newIds) > 0:
        # Delete the lineage informations for cells that have been updated
        for idc in idnextcells:
            cell = dataset.get_object(str(next_t) + "," + str(idc))
            for m in cell.mothers:
                dataset.del_mother(cell, m)
            for d in cell.daughters:
                dataset.del_daughter(cell, d)
        # send the new labels as source for the next step barycenters
        for idc in c_newIds:
            if not idc in cells_updated_at_t:
                cells_updated_at_t.append(idc)
        # set the new segmentation
        dataset.set_seg(next_t, data_next_t, cells_updated=cells_updated_at_t)
        # Compute the time point to link new cells created
        next_next_t = t + 2 if forward else t - 2
        # Load the time point segmentation
        data_next_next_t = dataset.get_seg(next_next_t)
        # For each cell created
        for o in barycenter_for_id:
            seed = barycenter_for_id[o]
            # Get the mother id
            mother = dataset.get_object(str(t) + "," + str(o))
            # Get the daughter id
            daugther = data_next_t[seed[0], seed[1], seed[2]]
            mndaugther = None
            # If we found a daughter
            if daugther != dataset.background:
                # Link daughter in the corresponding direction
                mndaugther = dataset.get_object(str(next_t) + "," + str(daugther))
                if forward and mndaugther is not None:
                    dataset.add_mother(mndaugther, mother)
                elif mndaugther is not None:
                    dataset.add_mother(mother, mndaugther)
            # If there is a time point after the time point we segmented
            if data_next_next_t is not None and dataset.begin <= next_next_t <= dataset.end:
                secondaughter = data_next_next_t[seed[0], seed[1], seed[2]]
                secondaughtermn = dataset.get_object(str(next_next_t) + "," + str(secondaughter))
                # Link daughter and daughter of daughter depending on the direction
                if forward:
                    if mndaugther is not None:
                        dataset.add_mother(mndaugther, mother)
                    if mndaugther is not None and secondaughtermn is not None:
                        dataset.add_mother(secondaughtermn, mndaugther)
                else:
                    if mndaugther is not None:
                        dataset.add_mother(mother, mndaugther)
                    if mndaugther is not None and secondaughtermn is not None:
                        dataset.add_mother(mndaugther, secondaughtermn)

    printv("Cells used for next step of propagation : " + str(cells_updated_at_t), 1)
    # Return the list of cells updated, and the new segmentation
    return cells_updated_at_t, data_next_t

def process_propagation_for_selection(selections,s,dataset,forward,min_vol,use_raw_images=False,sigma=0):
    # Find the min, max and list of times
    mint = 100000
    maxt = -10000
    times = {}  # List all times

    # Work on selections
    for o in selections[s]:
        mint = min(mint, o.t)
        maxt = max(maxt, o.t)
        if o.t not in times:
            times[o.t] = []
        times[o.t].append(o.id)
    # fill time gaps to be able to create multiples cells if needed
    for i in range(mint, maxt + 1):
        if not i in times:
            times[i] = []
    # Sort the timepoints sequence depending in the direction
    times = dict(sorted(times.items()))
    if not forward:
        times = dict(reversed(sorted(times.items())))
    # For each time point of this Selection
    new_label = ""
    for t in times:
        # Detect the time point to modify using direction chosen
        next_t = t + 1 if forward else t - 1
        # If the user labeled a cell at the time point to propagate
        if next_t in times:
            # Propagate the seeds and get the new cells created as source for the next propagation
            times[next_t], data = process_at(t, times[t], dataset, next_t,min_vol,forward,use_raw_images,s_sigma=sigma)
            # Add the updated cells to the list of cells to update
            for cell in times[next_t]:
                new_label += str(next_t) + "," + str(cell) + "," + str(s) + ";"
    return new_label
