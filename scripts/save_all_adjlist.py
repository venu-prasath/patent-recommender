import os
from glob import glob
import numpy as np
import shutil
from patent_graph import make_graph
from tqdm import tqdm

base_dir = 'patent-recommender/dataset'
file_list=glob(os.path.join(base_dir,'*/*.json'))
for file in tqdm(file_list):
    filename = os.path.splitext(os.path.split(file)[1])[0]
    G=make_graph(file, file_loc=f"patent-recommender/dataset/{filename}/{filename}.adjlist")