import config
import
def extract_det_ids(part_id):
    dim_ids_text = overall_mapping[overall_mapping['PartitionID'] == part_id]['DetectorID (DIM)'].values[0]
    dar_ids_text = overall_mapping[overall_mapping['PartitionID'] == part_id]['DetectorID (DAR)'].values[0]
    dim_ids_set = set([str.strip(det_id) for det_id in dim_ids_text.split(",")]) if dim_ids_text == dim_ids_text else set()
    dim_set = set()
    dar_set = set()
    for dim_id in dim_ids_set:
        dict_results = utils.get_det_info(dim_id)
        dim_set.add(Detector(dict_results['det_id'], \
                             dict_results['version'], dict_results['det_type'], dict_results['profile_size'], \
                             dict_results['size_label']))

    dar_set = set([str.strip(det_id) for det_id in dar_ids_text.split(",")]) if dar_ids_text == dar_ids_text else set()
    return dim_set.union(dar_set)

def read_dets(df):
    det_set = set()
    for row in df.iterrows():
        det_id  = row[1]['DetectorID']
        det_type = row[1]['DetectorType']
        prof_size = row[1]['TotalProfileSize']
        version = "V2" if row[1]['ProfileSupport'] == "EDM_V2" else "V3"
        size_label = row[1]['SizeLabel']
        det_set.add(Detector(det_id, version,det_type, prof_size, size_label))
    return det_set


def read_parts(df):
    part_set = set()
    for row in df.iterrows():
        part_id = row[1]['PartitionID']
        part_type = row[1]['PartitionType']
        version = "V2" if row[1]['ProfileSupport'] == "EDM_V2" else "V3"

        part_set.add(Partition(part_id, version, part_type))
    return part_set
