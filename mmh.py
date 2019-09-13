#import statements 
import dlpack
import utils
import config
from classes import Detector, Partition

def mmh(current_mapping, optimal_mapping):
    holding_zone = []
    for part_id in current_mapping.keys():
        part_type = utils.get_part_info(part_id)['part_type']
        part_version = utils.get_part_info(part_id)['version']
        part_obj = Partition(part_id, part_type, part_version)
        if part_type == "SHARED" and len(optimal_mapping[part_id]) != 0:
            typical_det = list(optimal_mapping[part_id])[0]
            pref_det_type = typical_det.det_type
            xs_list = utils.identify_xs_dets(part_obj, optimal_mapping)
            eq_xs_list = utils.identify_eq_xs_dets(part_obj, part_version, pref_det_type, current_mapping)
            for det in xs_list:
                optimal_mapping[part_id].remove(det)
                holding_zone.append(det)
            for det in eq_xs_list:
                orig_part_id = utils.search_det_location(det, config.part_list,holding_zone, \
                                                         optimal_mapping)
                if orig_part_id == 0:
                    holding_zone.remove(det)
                    optimal_mapping[part_id].append(det)
                elif orig_part_id == -1:
                    print("ERROR: SEARCH DET_ID NOT FOUND IN CURRENT_MAPPING")
                else:
                    optimal_mapping[orig_part_id].remove(det)
                    optimal_mapping[part_id].append(det)
    if config.LOG_OVERALL_PROG:
        print("MMH algorithm terminated successfully! Optimal allocation from DLPACK has been reshaped.")
    #return the modified optimal mapping
    return optimal_mapping



