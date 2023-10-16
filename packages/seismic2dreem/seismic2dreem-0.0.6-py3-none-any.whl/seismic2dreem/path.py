import os
from os.path import join, isfile, isdir, dirname


class SeismicPath:
    
    def __init__(self, root:str, mask:bool) -> None:
        assert isdir(root), f"seismic_folder_path is not a directory: {root}"
        self.root = root
      #  assert isdir(self.root), f"seismic_folder_path does not contain a 'out/table' directory: {root}"
        self.mask = mask
        
    # def find_table(self, root):
    #     paths = os.walk(root)
    #     for path in paths:
    #         path = path[0]
    #         if path.split('/')[-1] == 'table':
    #             return path
    #     raise FileNotFoundError("No table directory found")
    
    def list_csvs(self):
        for sample in self.list_samples():
            for construct in self.list_constructs(sample):
                for section in self.list_sections(sample, construct):
                    yield self.get_csv(sample, construct, section)
                    
    def get_sample_path(self, sample:str):
        return join(self.root, sample)
    
    def get_construct_path(self, sample:str, construct:str):
        return join(self.get_sample_path(sample), 'table', construct)
    
    def get_section_path(self, sample:str, construct:str, section:str):
        return join(self.get_construct_path(sample, construct), section)
    
    def get_csv_path(self, sample:str, construct:str, section:str):
        return join(self.get_section_path(sample, construct, section), "mask-per-pos.csv" if self.mask else "relate-per-pos.csv")
    
    def get_csv_gz_path(self, sample:str, construct:str, section:str):
        return join(self.get_section_path(sample, construct, section), "relate-per-read.csv.gz")
    
    def list_samples(self):
        l = os.listdir(self.root)
        # remove non-directories
        l = [x for x in l if isdir(self.get_sample_path(x))]
        assert len(l), f"no samples found in {self.root}"
        return l

    def list_constructs(self, sample:str):
        l = os.listdir(join(self.get_sample_path(sample), 'table'))
        # remove non-directories
        l = [x for x in l if isdir(self.get_construct_path(sample, x))]
        if not len(l): print(f"no constructs found in {self.get_sample_path(sample)}")
        return l
    
    def list_sections(self, sample:str, construct:str):
        l = os.listdir(self.get_construct_path(sample, construct))
        # remove non-directories
        l = [x for x in l if isdir(self.get_section_path(sample, construct, x))]
        if not len(l): print(f"no sections found in {self.get_construct_path(sample, construct)}")
        return l
    
    def _only_dir(self, list):
        return [x for x in list if isdir(x)]