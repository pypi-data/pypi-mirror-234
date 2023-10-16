import os
from os.path import join, isfile, isdir, dirname
import json
import numpy as np

def cast_to_json_compat(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def cast_dict(mp):
    for k, v in mp.items():
        mp[k] = cast_to_json_compat(v)
        if type(v) is dict:
            cast_dict(v)
    return mp
    
    
def sort_dict(mut_profiles):
    sorting_key = lambda item: 1000*{int:0, str:0, float:0, list:1, dict:2}[type(item[1])] + ord(item[0][0])
    mut_profiles = {k:mut_profiles[k] for k in sorted(mut_profiles)}
    mut_profiles = dict(sorted(mut_profiles.items(), key=sorting_key))
    for k, v in mut_profiles.items():
        if type(v) is not dict:
            continue
        mut_profiles[k] = sort_dict(v)
    return mut_profiles


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def dump_json(data, path, beautify=True):
    """Beautifies and 
    
    """
    import json
    assert isdir(dirname(path)), f"output directory does not exist: {dirname(path)}"
    
    # Write the output
    out = cast_dict(data)
    out = sort_dict(out)
    
    # Make lists in one line
    out = json.dumps(out, cls=NpEncoder, indent=2)

    if beautify:
        out = list(out)
        out = ''.join(['[' if i == ']' else i for i in out])
        out = out.split('[')
        out = [o.replace('\n        ','') if i%2 else o for i, o in enumerate(out)]
        out = out[0] + ''.join([('[',']')[i%2] + o for i, o in enumerate(out[1:])])
        
    # Write the output
    with open(os.path.join(path), 'w') as f:
        f.write(out)
        