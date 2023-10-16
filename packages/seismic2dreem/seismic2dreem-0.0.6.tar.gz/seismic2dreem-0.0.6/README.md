# seismic2dreem
A python module to turn seismic output into dreem output

## Installation

```bash
pip install seismic2dreem
```

## Usage

You need a seismic file structure such as:

```
dreem_output_dir/
    sample1/
        table/
            reference1/
                section1/
                    relate-per-read.csv.gz
                    mask-per-pos.csv
```

### Python

```python
import seismic2dreem
seismic2dreem.run(
    seismic_dir = 'seismic_main_folder',  # path to the folder containing the seismic output. Can be a list of folders.
    output = 'dreem_output_dir',        # path to the folder where the dreem output will be written
    ow = False,                             # if True, existing files will be overwritten.
    mask = True,                           # if True, use the mask-per-pos.csv file instead of the relate-per-read.csv.gz file (default: True)
    beautify = True,                         # if True, the json files will be beautified. 10x slower and can generate bugs
    verbose = True)                              # if True, print the progress of the conversion
```

### Command line

```bash
seismic2dreem --help
seismic2dreem path/to/this/seismic_main_folder path/to/this/other/seismic_main_folder -o path/to/dreem_output_dir --ow --beautify --verbose
```

## License

[MIT](https://choosealicense.com/licenses/mit/)


## Author

Yves Martin des Taillades

