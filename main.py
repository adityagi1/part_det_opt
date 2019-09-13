#import statements 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import queue
import operator
from collections import OrderedDict
import math
import ryg
import dlpack
import mmh
import utils
import config


def main():
    optimal_mapping = dlpack.dlpack(config.det_list, config.part_list)
    reshaped_mapping = mmh.mmh(config.current_mapping, optimal_mapping)
    final_move_list = ryg.ryg(config.current_mapping, reshaped_mapping)

    print(final_move_list)

main()

