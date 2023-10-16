from os.path import join, exists
import json
from .dump import dump_json
from .path import SeismicPath
from .translation import seismic_csv_to_dreem_json
import os

def run(seismic_dir:str, output:str, ow=False, mask=True, beautify:bool=True, verbose:bool=True):
    """A function to convert a seismic folder to a dreem json output.
    
    Arguments:
        seismic_dir {str} -- The path to the seismic folder
        output {str} -- The path to the output directory
        ow {bool} -- Whether to overwrite an existing file
        mask {bool} -- Use the mask-per-pos.csv file instead of the relate-per-read.csv.gz file (default: True)
        beautify {bool} -- Whether to beautify the json output (default: True). Deactivate for faster processing and less possible errors.
        verbose {bool} -- Whether to print warnings (default: True)

    Returns:
        None
    """
    
    if type(seismic_dir) == str:
        seismic_dir = [seismic_dir]
        
    os.makedirs(output, exist_ok=True)
            
    for p in seismic_dir:
        seismic_path = SeismicPath(p, mask=mask)
            
        for sample in seismic_path.list_samples():
            
            path = join(output, sample + ".json")
            if exists(path) and not ow and verbose:
                print(f"WARNING: {path} already exists")
                continue
            
            out = {'sample': sample}
            for construct in seismic_path.list_constructs(sample):
                out[construct] = {}
                for section in seismic_path.list_sections(sample, construct):
                    out[construct][section] = {}
                    try:
                        out[construct][section] = seismic_csv_to_dreem_json(
                            seismic_path.get_csv_path(sample, construct, section), 
                            seismic_path.get_csv_gz_path(sample, construct, section), 
                            mask=mask)
                    except FileNotFoundError:
                        if verbose:
                            print(f"WARNING: no csv found for {sample}/{construct}/{section}")
                    except ValueError as e:
                        if verbose:
                            print(f"WARNING value error: {e} for {sample}/{construct}/{section}")
                    except Exception as e:
                        if verbose:
                            print(f"WARNING: exception {e} for {sample}/{construct}/{section}")
                
            # clean up empty constructs
            for construct in seismic_path.list_constructs(sample):
                if len(out[construct]) == 1:
                    if len(out[construct][list(out[construct].keys())[0]]) == 0:
                        del out[construct]
                        
            # Save to file
            dump_json(out, path, beautify=beautify)
            if verbose:
                print(f"saved {sample}.json to {seismic_path.get_sample_path(sample)}")