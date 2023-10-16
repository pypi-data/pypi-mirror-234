from typing import List, Tuple
import glob
import os

class BandDataPackage:
    BAND_NAME: str = None
    BAND_PATH: str = None
    path_pairs: List[Tuple[str, str]] = None

    def __init__(self, band_name, band_path):
        self.BAND_NAME = band_name
        self.BAND_PATH = band_path
        self.check_band_path()

    """
    Check if for every RAS file there is a corresponding RHD file and 
    create a list of paths pairs
    """
    def check_band_path(self):
        self.path_pairs = []
        ras_paths = glob.glob(os.path.join(self.BAND_PATH, "**", '**.RAS'),
                                  recursive=True)
        ras_bases = [os.path.basename(path).replace('.RAS', '') for path in ras_paths]

        if len(ras_paths) == 0:
            raise ValueError(f"No RAS files found in {self.BAND_PATH}")

        rhd_paths = glob.glob(os.path.join(self.BAND_PATH, "**", '**.RHD'),
                                  recursive=True)
        rhd_bases = [os.path.basename(path).replace('.RHD', '') for path in rhd_paths]
        
        for ras_id, ras_base in enumerate(ras_bases):
            rhd_base = ras_base.replace('.RAS', '.RHD')
            try:
                rhd_id = rhd_bases.index(rhd_base)
                self.path_pairs.append((ras_paths[ras_id], rhd_paths[rhd_id]))
            except ValueError:
                raise ValueError(f"RHD file for {ras_base} not found")

class BandsDataPackage:
    B2_package: BandDataPackage = None
    B3_package: BandDataPackage = None
    B4_package: BandDataPackage = None
    B8_package: BandDataPackage = None

    def __init__(self, b2_path, b3_path, b4_path, b8_path):
        self.B2_package = BandDataPackage("B2", b2_path)
        self.B3_package = BandDataPackage("B3", b3_path)
        self.B4_package = BandDataPackage("B4", b4_path)
        self.B8_package = BandDataPackage("B8A", b8_path)

    def tolist(self):
        return [self.B2_package, self.B3_package, self.B4_package, self.B8_package]