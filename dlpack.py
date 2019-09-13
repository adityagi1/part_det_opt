#!/usr/bin/env python
# coding: utf-8

# In[4]:


#import statements 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import queue
import operator
from collections import OrderedDict
import math
import utils
import config
from classes import Partition, Detector

# In[5]:





#ENCAPSULATE PHASE 0 (SETUP) INTO MODULAR FUNCTION

#PRECONDITION:
#dets has columns 'DetectorID', 'ProfileSupport', 'DetectorType', 'TotalProfileSize'
#parts has columns 'PartitionID', 'PartitionType', 'ProfileSupport'
#map_dict will contain the det-part mapping. keys = part_id, values = set containing det_ids
#POSTCONDITION:
#returns a dict with v2_dets, v2_parts, v3_dets, v3_parts, shared_parts, dedicated_parts, dim_dets, dar_dets, xs_dets, reg_dets, xl_dets 
def phase_0(det_list, part_list):
    #*SEPARATE DETECTORS, PARTITIONS
    v2_dets = list(filter(lambda det: det.version == "V2", det_list))
    v3_dets = list(filter(lambda det: det.version == "V3", det_list))
    v2_parts = list(filter(lambda part: part.version == "V2", part_list))
    v3_parts = list(filter(lambda part: part.version == "V3", part_list))
    shared_parts = list(filter(lambda part: part.part_type == "SHARED", part_list))
    dedicated_parts = list(filter(lambda part: part.part_type == "DEDICATED", part_list))
    dim_dets = list(filter(lambda det: det.det_type == "DIM", det_list))
    dar_dets = list(filter(lambda det: det.det_type == "DAR", det_list))
    xs_dets = list(filter(lambda det: det.size_label == "XS", det_list))
    reg_dets = list(filter(lambda det: det.size_label == "REG", det_list))
    xl_dets = list(filter(lambda det: det.size_label == "XL", det_list))
    #*ADD TO DICTIONARY
    ret_dict = {}
    ret_dict['v2_dets'] = v2_dets
    ret_dict['v3_dets'] = v3_dets
    ret_dict['v2_parts'] = v2_parts
    ret_dict['v3_parts'] = v3_parts
    ret_dict['shared_parts'] = shared_parts
    ret_dict['dedicated_parts'] = dedicated_parts
    ret_dict['dim_dets'] = dim_dets
    ret_dict['dar_dets'] = dar_dets
    ret_dict['xs_dets'] = xs_dets
    ret_dict['reg_dets'] = reg_dets
    ret_dict['xl_dets'] = xl_dets
    return ret_dict


# In[8]:


#ENCAPSULATE PHASE 1 (XL MAPPING) INTO MODULAR FUNCTION

#PRECONDITION:
#*** map_dict needs to be defined in the global environment
#dets contains XL dets
#parts contains dedicated parts
#POSTCONDITION:
#modifies map_dict with XL mapping (already defined in env.)
def phase_1(det_list, part_list, map_dict):
    for version in ["V2", "V3"]:
        my_dets = list(filter(lambda det: det.version == version, det_list))
        my_parts = list(filter(lambda part: part.version == version, part_list))
        for index in range(0, min(len(my_dets), len(my_parts))):
            map_dict[my_parts[index].part_id].append(my_dets[index])
            if config.LOG_PROG:
                print("Adding detID = " + str(my_dets[index].det_id) + " [size = " + str(my_dets[index].prof_size) + "]" \
                      + " to partitionID = " + str(my_parts[index].part_id) + " with rem. space = " + \
                      str(config.PARTITION_MEMORY_CAPACITY - utils.calc_part_mem_usage(my_parts[index], map_dict)))

        if len(my_dets) > len(my_parts):
            for index in range(min(len(my_dets), len(my_parts)), len(my_dets)):
                part_id = version + " DED. PARTITION " + str(index - len(my_parts) + 1)
                part = Partition(part_id, version, "DEDICATED")
                config.part_list.append(part)
                map_dict[part_id] = list()
                map_dict[part_id].append(my_dets[index])
                if config.LOG_PROG:
                    print("Adding detID = " + str(my_dets[index].det_id) + " [size = " + str(my_dets[index].prof_size) + "]" +
                            " to partitionID = " + str(part_id) + " with rem. space = " +
                            str(config.PARTITION_MEMORY_CAPACITY - my_dets[index].prof_size))

    return map_dict


# In[9]:


#ENCAPSULATE PHASE 2: REGULAR MAPPING
     
# PRECONDITIONS:
# dets must contain only regular detectors
# parts must only contain shared partitions
# POSTCONDITIONS:
# modifies map_dict with the new regular mapping to shared partitions
def phase_2(dets, parts, map_dict):
        for version in ["V2", "V3"]:
            my_dets = list(filter(lambda det: det.version == version, dets))
            my_parts = list(filter(lambda part: part.version == version, parts))
            #sort my_dets according in descending order of profile size
            sorted(my_dets, key=lambda det: det.prof_size, reverse=True)
            # for loop over all R detectors
            for det in my_dets:
                for part in my_parts:
                    rem_mem_cap = config.PARTITION_MEMORY_CAPACITY - utils.calc_part_mem_usage(part, map_dict)
                    #if curr partition can hold detector, then put in, and update partition state
                    if rem_mem_cap >= det.prof_size:
                        map_dict[part.part_id].append(det)
                        if config.LOG_PROG:
                            print("Adding detID = " + str(det.det_id) + " [size = " + str(utils.get_det_mem_size(det)) + "]"                               + " to partitionID = " + str(part_id) + " with rem. space = "                               + str(rem_mem_cap))
                        break

                #det_id could not be assigned amongst existing partitions
                if utils.get_det_assignment(det, map_dict) is None:
                    #a new partition needs to be created, and put detector in it
                    part_id = "New Shared Partition" + str(len(map_dict))
                    print("Creating a new shared partition (V2) with partition ID = " + part_id)
                    #update map_dict with new partition
                    map_dict[part_id] = list()
                    map_dict[part_id].append(det)
                    config.part_list.append(Partition(part_id, version, "SHARED"))
        return map_dict


# In[10]:


#PHASE 3: XS MAPPING



#PRECONDITIONS:
#*** map_dict needs to be defined in the calling frame/environment
#dets contains only xs detectors
#parts contains only shared partitions
#POSTCONDITIONS:
#returns map_dict with xs mapping
def phase_3(dets, parts, map_dict):
        for version in ["V2", "V3"]:
            my_dets = list(filter(lambda det: det.version == version, dets))
            my_parts = list(filter(lambda part: part.version == version, parts))
            pr_dict = {}
            #populate pr_dict with packing ratios keyed by part_id
            for part in my_parts:
                pr_dict[part.part_id] = utils.calculate_part_packing_ratio(part, map_dict)
            #now sort parts in order of decreasing packing_ratio
            sorted_pr_dict = OrderedDict(sorted(pr_dict.items(), key = lambda x : x[1], reverse = True))
            #start filling partitions with detectors
            start = 0
            cutoff = 0
            for part_id in sorted_pr_dict.keys():
                start = cutoff
                num_free = config.PARTITION_DETECTOR_CAPACITY - utils.calc_part_det_usage(part, map_dict)
                cutoff = cutoff + num_free
                add_list = my_dets[start:cutoff]
                for det in add_list:
                    map_dict[part_id].append(det)
                    if config.LOG_PROG:
                        print("Adding detID = " + str(det.det_id)+ " [size = " + str(utils.get_det_mem_size(det.det_id)) + "]" \
                              + " to partitionID = " + str(part_id) + " with rem. space = " + \
                              str(config.PARTITION_MEMORY_CAPACITY - utils.calc_part_mem_usage(part_id, map_dict)))

        return map_dict


# In[11]:


#FINAL: TIE UP ABOVE FUNCTIONS INTO MASTER DLPACK FUNCTION

#PRECONDITIONS:
#* dets must contain all the detectors to be allocated.
#* parts must contain all the partitions to receive detectors.
#POSTCONDITIONS:
#*returns map_dict which contains final mapping of all dets to parts
def dlpack(dets, parts):
    map_dict = {}
    #setup map_dict with keys = part_ids of partitons in parts
    for part in config.part_list:
        map_dict[part.part_id] = list()
    
    #PHASE 0 - SETUP
    d = phase_0(dets, parts)
    
    #PHASE 1
    xl_dets = d['xl_dets']
    dedicated_parts = d['dedicated_parts']
    map_dict = phase_1(xl_dets, dedicated_parts, map_dict)
    
    #PHASE 2
    reg_dets = d['reg_dets']
    shared_parts = d['shared_parts']
    #only call phase_2 with reg_dim detectors, 
    reg_dim_dets = list(filter(lambda det: det.det_type == "DIM", reg_dets))
    map_dict = phase_2(reg_dim_dets, shared_parts, map_dict)
    #identify which partitions contain dim_detectors
    dim_parts = utils.search_parts("DIM", map_dict)
    
    #call phase_2 with reg_dar_detectors only, with parts_arg excluding the parts used up by dim_detectors before
    reg_dar_dets = list(filter(lambda det: det.det_type == "DAR", reg_dets))
    map_dict = phase_2(reg_dar_dets, list(filter(lambda part: part not in dim_parts, shared_parts)), map_dict)
    
    #PHASE 3
    xs_dets = d['xs_dets']
    xs_dim_dets = list(filter(lambda det: det.det_type == "DIM", xs_dets))
    xs_dar_dets = list(filter(lambda det: det.det_type == "DAR", xs_dets))
    #identify which partitions contain dar_detectors
    dar_parts = utils.search_parts("DAR", map_dict)
    #call phase_3 with xs dim_detectors, with parts_arg excluding parts used up by dar_detectors earlier
    map_dict = phase_3(xs_dim_dets, list(filter(lambda part: part not in dar_parts, shared_parts)), map_dict)
    
    
    
    #identify which parts contain dim_detectors
    dim_parts = utils.search_parts("DIM",  map_dict)
    #call phase_3 with xs_dar_detectors, with parts_arg excluding parts used up by dim_detectors earlier
    map_dict = phase_3(xs_dar_dets, list(filter(lambda part: part not in dim_parts, shared_parts)), map_dict)
    
    if config.LOG_OVERALL_PROG:
        if utils.check_termination(map_dict):
            print("DLPack algorithm terminated successfully! All detectors have been mapped to partitions. ")
        else:
            print("Not all detectors have been mapped to partitions! ")
    return map_dict


