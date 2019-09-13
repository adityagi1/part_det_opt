import pandas as pd
import utils
from classes import Detector, Partition

XL_CUTOFF = 1200
PARTITION_MEMORY_CAPACITY = 15000
PARTITION_DETECTOR_CAPACITY = 80
LOG_PROG = False
LOG_OVERALL_PROG = True
PRINT_DLPACK_RESULTS = False
PRINT_MMH_RESULTS = False
PRINT_RYG_RESULTS = False

holding_zone = []

def read_dets(df):
    det_list = list()
    for row in df.iterrows():
        det_id  = row[1]['DetectorID']
        det_type = row[1]['DetectorType']
        prof_size = row[1]['TotalProfileSize']
        version = "V2" if row[1]['ProfileSupport'] == "EDM_V2" else "V3"
        size_label = row[1]['SizeLabel']
        det_list.append(Detector(det_id, version,det_type, prof_size, size_label))
    return det_list


def read_parts(df):
    part_list = list()
    for row in df.iterrows():
        part_id = row[1]['PartitionID']
        part_type = row[1]['PartitionType']
        version = "V2" if row[1]['ProfileSupport'] == "EDM_V2" else "V3"

        part_list.append(Partition(part_id, version, part_type))
    return part_list





def extract_det_ids(part_id, det_list):
    dim_ids_text = overall_mapping[overall_mapping['PartitionID'] == part_id]['DetectorID (DIM)'].values[0]
    dar_ids_text = overall_mapping[overall_mapping['PartitionID'] == part_id]['DetectorID (DAR)'].values[0]
    dim_ids_list = list([str.strip(det_id) for det_id in dim_ids_text.split(",")]) if dim_ids_text == dim_ids_text else list()
    dar_ids_list = list([str.strip(det_id) for det_id in dar_ids_text.split(",")]) if dar_ids_text == dar_ids_text else list()
    dim_list = [create_det_obj(det_id, det_list) for det_id in dim_ids_list]
    dar_list = [create_det_obj(det_id, det_list) for det_id in dar_ids_list]
    return dim_list + dar_list


def create_det_obj(det_id, det_list):
    return list(filter(lambda det: det.det_id == det_id, det_list))[0]

def create_part_obj(part_id, part_list):
    return list(filter(lambda part: part.part_id == part_id, part_list))[0]


def search_det_location(search_det, red_parts, holding_zone, current_mapping):
    # first search holding zone, if search_det_id in holding_zone, return -1
    if search_det.det_id in [det.det_id for det in holding_zone]:
        return 0
    else:
        for red_part in red_parts:
            if search_det.det_id in [det.det_id for det in current_mapping[red_part.part_id]]:
                return red_part.part_id

        return -1


#load the data
overall_mapping = pd.read_csv("cleaned data/overall_mapping.csv")
all_dets = pd.read_csv("cleaned data/all_detectors.csv")
all_parts = pd.read_csv("cleaned data/partition_data.csv")

new_dets = pd.read_csv("grafana_data_export (68).csv")
new_dets.columns = ["DetectorID", "TotalProfileSize"]
updated_all_dets = all_dets.copy()
for index in range(len(updated_all_dets)):
    det_id = updated_all_dets.at[index,"DetectorID"]
    if det_id in new_dets['DetectorID'].tolist():
        new_prof_value = new_dets[new_dets['DetectorID'] == det_id]['TotalProfileSize'].iloc[0]
        updated_all_dets.iat[index,3] = new_prof_value
all_dets = updated_all_dets
all_dets['SizeLabel'] = all_dets['TotalProfileSize'].apply(lambda size: "XS" if size == 0.0 else ("XL" if size > XL_CUTOFF else "REG" ))



part_list = read_parts(all_parts)
det_list = read_dets(all_dets)

current_mapping = dict()
for p_id in overall_mapping['PartitionID'].tolist():
    current_mapping[p_id] = list()

for p_id in current_mapping.keys():
    current_mapping[p_id] = extract_det_ids(p_id, det_list)

for part in part_list:
    assert(part.part_id in list(current_mapping.keys()))
for det in det_list:
    assert(search_det_location(det,part_list,[],current_mapping) != -1)

#'83a59117-8109-4c28-ae79-80b04bb4d4c8'

"b33e0af4-51aa-11e9-b60e-0242ac110002 AND   d0d7fde9-a5b4-441b-99e0-c866261c19ca not in current_mapping"