import numpy as np
import pandas as pd
import os
import gzip
import shutil
import os

translation_arrays = {
    "Called": 'cov',
    "Covered" : 'cov',
    "Informed": 'info',
    "Subbed": 'sub_N',
    "Subbed-A": 'sub_A',
    "Subbed-C": 'sub_C',
    "Subbed-G": 'sub_G',
    "Subbed-T": 'sub_T',
    "Deleted": 'del',
    "Inserted": 'ins',
}

def seismic_csv_to_dreem_json(csv_path:str, csv_gz_path:str, mask:bool=True):
    # load csv
    i = pd.read_csv(csv_path)
    sequence = ''.join(i['Base'].tolist())
    
    # convert to json
    d = {}
    for k, v in translation_arrays.items():
        if k in i.columns:
            d[v] = np.array(i[k], dtype=float)

    d['min_cov'] = np.min(d['cov'][~np.isnan(d['cov'])]) if 'cov' in d.keys() and len(d['cov'][~np.isnan(d['cov'])]) else 0
    if 'info' not in d.keys():
        d['info'] = (i['Mutated'] + i['Matched'])
    d['sub_rate'] = d['sub_N']/d['info'] 
    #, out=0*np.ones_like(np.array(d['sub_N']).astype(float)), where= np.array(d['sub_N']).astype(float) != 0)

    if mask:
        for k, v in translation_arrays.items():
            d[v] = np.nan_to_num(d[v], nan=-1000).tolist()
        d['sub_rate'] = np.nan_to_num(d['sub_rate'], nan=-1000).tolist()
    
    # add sub_hist from relate-per-read.csv.gz
    d['sub_hist'] = read_num_of_mutations(csv_gz_path)
    
    return {'sequence': sequence, 'pop_avg': d}


def read_num_of_mutations(csv_gz_path:str):
    csv_path = untar_csv_gz(csv_gz_path)
    mut_per_read = pd.read_csv(csv_path)['Mutated']
    out = np.histogram(mut_per_read, bins=range(0, max(mut_per_read)+1))[0].tolist()
    os.remove(csv_path)
    return out

def untar_csv_gz(csv_gz_path):
    with gzip.open(csv_gz_path, 'rb') as f_in:
        with open(os.path.splitext(csv_gz_path)[0], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return f_out.name
