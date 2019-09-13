#DEFINE UTILITY FUNCTIONS TO BE USED LATER


#import statements 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import queue
import operator
from collections import OrderedDict
import math
import config





#PRECONDITIONS:
#map_dict needs to be defined in the calling frame/environment
#detID needs to be valid
#POSTCONDITIONS:
#returns the partititonID associated with detID
#if detID has not been assigned, returns None
def get_det_assignment(target_det, map_dict):
    for part_id in map_dict.keys():
        for det in map_dict[part_id]:
            if det.det_id == target_det.det_id:
                return part_id
    return None

#PRECONDITIONS:
#detID should be valid
#all_dets has been defined in the global environment
#POSTCONDITIONS:
#returns the size of a particular detID
def get_det_mem_size(det):
    return det.prof_size

#PRECONDITIONS: 
#map_dict needs to be defined in the calling frame/environment
#partID must be valid
#POSTCONDITIONS:
#will return remaining mem_space on that partition
def calc_part_mem_usage(part, map_dict):
    total_mem_usage = 0.0
    for det in map_dict[part.part_id]:
        total_mem_usage = total_mem_usage + det.prof_size
    return total_mem_usage   


#calculate the number of detectors on partition partID
def calc_part_det_usage(part, map_dict):
    return len(map_dict[part.part_id])


#calculate packing_ratio for partID
def calculate_part_packing_ratio(part, map_dict):
    #create v2's packing ratio dict
    rem_part_det_cap = config.PARTITION_DETECTOR_CAPACITY - calc_part_det_usage(part, map_dict)
    rem_part_mem_cap = config.PARTITION_MEMORY_CAPACITY - calc_part_mem_usage(part, map_dict)
    if rem_part_mem_cap == 0.0:
        #if both rem_mem_cap and rem_det_cap are 0,
        if rem_part_det_cap == 0.0:
            #then part is of no value (so zero packing ratio)
            ratio_value = 0.0
        else:
            ratio_value = math.inf
    else:
        ratio_value = rem_part_det_cap/rem_part_mem_cap
    
    return ratio_value


#check if all detectors have been assigned to a partition (dlpack has terminated)
#PRECONDITIONS:
#map_dict needs to be defined in the calling frame/environment
#POSTCONDITIONS:
#returns True if all dets have been assigned, False if not.
def check_termination(map_dict):
    for det in config.det_list:
        if get_det_assignment(det, map_dict) is None:
            print("Missing DetID = ", det.det_id)
            return False
    return True


#searches map_dict and returns all partitions containing a particular type of detector
#PRECONDITIONS:
#target_criteria is either "DIM", "DAR", "XS", "REG", "L"
#POSTCONDITIONS:
#returns a list of part_ids containing the target_criteria
def search_parts(target_criteria, map_dict):
    ret_list = []
    if target_criteria in ["DIM", "DAR"]:
        for part in config.part_list:
            det_list = map_dict[part.part_id]
            for det in det_list:
                if det.det_type == target_criteria:
                    ret_list.append(part)
                    break
    elif target_criteria in ["XS", "REG", "XS"]:
        for part in config.part_list:
            det_list = map_dict[part.part_id]
            for det in det_list:
                if det.size_label == target_criteria:
                    ret_list.append(part)
                    break
            
    elif target_criteria in ["V2", "V3"]:
        for part in config.part_list:
            det_list = map_dict[part.part_id]
            for det in det_list:
                if det.version == target_criteria:
                    ret_list.append(part)
                    break
    return ret_list
    
#returns a dict containing the 'det_id', version', 'detector type', 'sizelabel', 'profile size' of detector with det_id 
def get_det_info(target_det_id):
    target_det_obj = list(filter(lambda det: det.det_id == target_det_id, config.det_list))
    det_id = target_det_obj.det_id
    det_type = target_det_obj.det_type
    prof_size = target_det_obj.prof_size
    size_label = target_det_id.size_label
    version = target_det_obj.version

    ret_dict = {}
    ret_dict['det_id'] = det_id
    ret_dict['version'] = version
    ret_dict['detector type'] = det_type
    ret_dict['profile size'] = prof_size
    ret_dict['size label'] = size_label
    
    return ret_dict
#returns a dict containing the 'part_id', 'version', 'partition type' of partitio with ID  = part_id
def get_part_info(target_part_id):
    target_part = list(filter(lambda part: part.part_id == target_part_id, config.part_list))[0]
    part_id = target_part.part_id
    version = target_part.version
    part_type = target_part.part_type
    
    ret_dict = {}
    ret_dict['part_id'] = part_id
    ret_dict['version'] = version
    ret_dict['part_type'] = part_type
    
    return ret_dict 



def compute_number_of_partitions_used(mapping):
    num_partitions_used = 0 
    for part_id in mapping.keys():
        num_dets_on_partition = len(mapping[part_id])
        if num_dets_on_partition > 0:
            num_partitions_used = num_partitions_used + 1
    return num_partitions_used



def identify_xs_dets(part, mapping):
    ret_list = []
    for det in mapping[part.part_id]:
        if det.size_label == "XS":
            ret_list.append(det)
    return ret_list


def identify_eq_xs_dets(part, vers, pref_det_type, mapping):
    ret_list = []
    
    for det in mapping[part.part_id]:
        if det.size_label == "XS" and det.version == vers and det.det_type == pref_det_type:
            ret_list.append(det)
    return ret_list

def search_det_location(search_det, red_parts, holding_zone, current_mapping):
    #first search holding zone, if search_det_id in holding_zone, return -1
    if search_det.det_id in [det.det_id for det in holding_zone]:
        return 0
    else:
        for red_part in red_parts:
            if search_det.det_id in [det.det_id for det in current_mapping[red_part.part_id]]:
                return red_part.part_id
        
        return -1







def identify_add_dets(part, current_mapping, optimal_mapping):
    curr_det_list = current_mapping[part.part_id]
    optimal_det_list = optimal_mapping[part.part_id]
    return Diff(optimal_det_list, curr_det_list)

def identify_remove_dets(part, current_mapping, optimal_mapping):
    curr_det_list = current_mapping[part.part_id]
    optimal_det_list = optimal_mapping[part.part_id]
    
    return Diff(curr_det_list, optimal_det_list)
def identify_stay_dets(part, current_mapping, optimal_mapping):
    curr_det_list = current_mapping[part.part_id]
    optimal_det_list = optimal_mapping[part.part_id]
    
    return Intersect(curr_det_list, optimal_det_list)

def search_det_location(search_det, red_parts, holding_zone, current_mapping):
    #first search holding zone, if search_det_id in holding_zone, return -1
    if search_det in holding_zone:
        return 0
    else:
        for part in config.part_list:
            if search_det in config.current_mapping[part.part_id]:
                return part.part_id
        return -1

#CHECK TERMINATION OF RYG ALGORITHM
def check_ryg_termination(current_mapping, optimal_mapping):
    for part in config.part_list:
        if Diff(optimal_mapping[part.part_id], current_mapping[part.part_id]) == []:
            if config.LOG_PROG: print("Detector Sets do not match for " + part.part_id)
            return False
    return True       


#implements SET DIFFERENCE li1 - li2
def Diff(li1, li2):
    diff_list = li1
    for elem in li2:
        if elem in diff_list:
            diff_list.remove(elem)
    return diff_list
    #li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    #return li_dif

def Intersect(li1, li2):
    int_list = []
    combined_list = li1 + li2
    for elem in combined_list:
        if elem in li1 and elem in li2:
            if elem not in int_list:
                int_list.append(elem)
    return int_list