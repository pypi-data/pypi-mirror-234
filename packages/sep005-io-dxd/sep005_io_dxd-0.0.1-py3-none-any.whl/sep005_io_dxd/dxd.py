import os
from pathlib import Path
from typing import Union
import dwdatareader
import numpy as np


class DxdFileReader:

    """
    DXD file, reads the the file and can access trough properties

    """

    def __init__(self, filename: str, filerootfolder: str = "", qa=True, verbose=False):
        """

        :param filename:
        :param filerootfolder:
        :param qa: Run quality assurance tests,
        """
        self.filename = filename
        self.file_rootfolder = filerootfolder
        self.fullpath = filename
        self.verbose = verbose
        if filerootfolder:
            self.fullpath = os.path.join(filerootfolder, filename)

        if not os.path.isfile(self.fullpath):
            raise FileNotFoundError(f"File not Found {self.fullpath}")

        with dwdatareader.open(self.fullpath) as file:
            info = file.info
            self.dt = info.start_store_time
            self.fs = info.sample_rate  # This the global sampling rate
            self.duration = info.duration
            self.df = file.dataframe()
            self.time = self.df.index.to_list()
            self.channels = file.channels
            self.info = info

        if verbose:
            print(f'Loaded {len(self.channels)} channels starting at {str(self.dt)} at {self.fs}Hz')

        if qa:
            self.missing_samples
            self.nan_samples

    @property
    def nan_samples(self):
        """
        Check if there are samples as NaN
        :return:
        """
        if len(self.df) != len(self.df.dropna()):
            raise ValueError('Channels contain NaN samples')
        if self.verbose:
            print('QA (NaN samples) : Imported signals contain no NaNs')


    @property
    def missing_samples(self):
        """
        Check if the sampling frequency is maintained properly
        :return:
        """
        # check the index matches the sampling frequency
        differences = np.diff(self.time)  # Calculate the differences between consecutive elements
        is_equidistant = np.allclose(differences, differences[0]*np.ones(len(differences)))  # Check if all differences are the same, up to precision
        if not is_equidistant:
            raise ValueError('Samples missing from channels')
        if self.verbose and is_equidistant:
            print('QA (missing samples) : Imported signals are equidistant spaced on index')


    def to_sep005(self) -> list[dict]:
        """_summary_

        Args:

        Returns:
            list: signals
        """
        signals = []
        for chan in self.channels:
            data = self.df[chan.name].to_numpy()
            fs_signal = len(data) / self.duration

            signal = {
                'name': chan.name,
                'data': data,
                'start_timestamp': str(self.dt),
                'fs': fs_signal,
                'unit_str': chan.unit
            }
            signals.append(signal)

        return signals




def read_dxd(path: Union[str, Path], verbose=False, qa=True) -> list[dict]:
    """
    Primary function to read dxd files based on file_path

    :param

    """
    dxd_reader = DxdFileReader(path, verbose=verbose, qa=qa)

    return dxd_reader.to_sep005()