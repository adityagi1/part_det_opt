#import statements 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import queue
import operator
from collections import OrderedDict
import math
import dlpack
import mmh
import utils
import config
import classes



def ryg(current_mapping, optimal_mapping):
    red_parts = [config.create_part_obj(part_id, config.part_list) \
                 for part_id in utils.Intersect(list(config.current_mapping.keys()), list(optimal_mapping.keys()))]
    green_parts = list()
    #holding_zone = list()
    total_dets_reshuffled = 0
    move_list = []
    #if utils.check_ryg_termination(config.current_mapping, optimal_mapping):
    #    print("CURRENT MAPPING ALREADY CONFORMS TO OPTIMAL MAPPING.")
    #    return
    for yellow_part in red_parts:
        red_parts.remove(yellow_part)
        add_dets = utils.identify_add_dets(yellow_part, config.current_mapping, optimal_mapping)
        total_dets_reshuffled = total_dets_reshuffled + len(add_dets)
        stay_dets = utils.identify_stay_dets(yellow_part, config.current_mapping, optimal_mapping)
        remove_dets = utils.identify_remove_dets(yellow_part, config.current_mapping, optimal_mapping)
        for det in remove_dets:
            move_list.append("REMOVE "+ str(det) + "FROM" + str(yellow_part) + "TO HOLDING ZONE")
            #config.current_mapping[yellow_part.part_id].remove(det)
            #config.holding_zone.append(det)
        for det in add_dets:
            orig_part_id = utils.search_det_location(det, red_parts, config.holding_zone, config.current_mapping)
            if orig_part_id == 0:
                #config.holding_zone.remove(det)
                move_list.append("MOVE " + str(det) + " FROM HOLDING ZONE TO " + str(yellow_part))
                if config.LOG_PROG:
                    print("MOVING", det.det_id, "from HOLDING ZONE TO", yellow_part.part_id)
                #config.current_mapping[yellow_part.part_id].append(det.det_id)
            elif orig_part_id == -1:
                print("ERROR: SEARCH DET_ID NOT FOUND IN CURRENT_MAPPING OR HOLDING ZONE")
            else:
                #config.current_mapping[orig_part_id].remove(det)
                #config.current_mapping[yellow_part.part_id].append(det)
                move_list.append("MOVE " + str(det) + " FROM" + orig_part_id + "TO" + str(yellow_part))
                if config.LOG_PROG:
                    print("MOVING", det.det_id, "from", orig_part_id, "to", yellow_part.part_id)

        green_parts.append(yellow_part)
    #print(holding_zone)
    #if utils.check_ryg_termination(config.current_mapping, optimal_mapping):
    #    if config.LOG_OVERALL_PROG:
    #        print("RYG Algorithm terminated successfully! All detectors have been reassigned.")
    #        print("TOTAL # OF DETS RESHUFFLED: ", total_dets_reshuffled)
    #    return config.current_mapping
    #else:
    #    print("RYG Algorithm has not terminated successfully!")
    #    return config.current_mapping
    print("RYG Algorithm terminated successfully! All detectors have been reassigned.")
    print("TOTAL # OF DETS RESHUFFLED: ", total_dets_reshuffled)

    return move_list




