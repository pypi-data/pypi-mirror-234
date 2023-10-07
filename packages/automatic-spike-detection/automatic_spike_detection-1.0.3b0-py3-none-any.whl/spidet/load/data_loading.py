from typing import List, Tuple

import h5py
import mne.io
import numpy as np
from h5py import Dataset, File
from loguru import logger
from mne.io import RawArray

from spidet.domain.SpikeDetectionFunction import SpikeDetectionFunction
from spidet.domain.Trace import Trace
from spidet.utils.times_utils import compute_rescaled_timeline

# Supported file formats
HDF5 = "h5"
EDF = "edf"
FIF = "fif"

# Other variables
LABEL_STD_LL = "Std_LL"
H_KEYWORD = "H_best"


class DataLoader:
    @staticmethod
    def extract_channel_names(channel_paths: List[str]) -> List[str]:
        return [
            channel_path[channel_path.rfind("/") + 1 :]
            for channel_path in channel_paths
        ]

    @staticmethod
    def extract_start_timestamp(dataset_path: str, file: File) -> float:
        sub_path = dataset_path[dataset_path.find("traces/") + 7 :]
        subgroup = sub_path[: sub_path.find("/")]
        subgroup_attributes = file.get(f"traces/{subgroup}").attrs
        return subgroup_attributes["start_timestamp"]

    @staticmethod
    def get_anodes_and_cathodes(
        leads: List[str], channel_names: List[str]
    ) -> Tuple[List[str], List[str]]:
        anodes, cathodes = [], []
        for prefix in leads:
            channels = list(
                filter(
                    lambda channel_name: channel_name.startswith(prefix), channel_names
                )
            )
            for idx in range(len(channels) - 1):
                anodes.append(channels[idx])
                cathodes.append(channels[idx + 1])

        return anodes, cathodes

    def generate_bipolar_references(self, raw: RawArray, leads: List[str]) -> RawArray:
        if leads is None:
            raise Exception(
                "bipolar_reference is true but no leads were passed for whose channels to perform the referencing"
            )
        anodes, cathodes = self.get_anodes_and_cathodes(leads, raw.ch_names)
        raw = mne.set_bipolar_reference(
            raw,
            anode=anodes,
            cathode=cathodes,
            drop_refs=True,
            copy=False,
            verbose=False,
        )
        return raw

    @staticmethod
    def create_trace(
        label: str, dataset: np.array, sfreq: int, start_timestamp: float
    ) -> Trace:
        """
        Create a Trace object from a recording of a particular electrode with a corresponding label.

        Parameters
        ----------
        label : str
            The label of the trace.

        dataset : array_like
            Numerical representation of the recording.

        sfreq : int
            Sampling frequency of the recording.

        start_timestamp: float
            Start timestamp of the recording (UNIX timestamp).

        Returns
        -------
        Trace
            A Trace object representing a recording from an electrode with the corresponding label.
        """
        return Trace(
            label,
            sfreq,
            start_timestamp,
            dataset[:].astype(np.float64),
        )

    def read_file(
        self,
        path: str,
        channel_paths: List[str] = None,
        bipolar_reference: bool = False,
        leads: List[str] = None,
    ) -> List[Trace]:
        """
        Read EEG data from a file and return a list of Trace objects,
        containing the EEG data of each channel.

        Reads EEG data from a file specified by 'path'.
        The supported file formats include '.h5', '.fif', and '.edf'.

        Parameters
        ----------
        path : str
            The file path of the EEG data file.

        channel_paths : List[str]
            Paths to the channels to include within the file
            (for edf and fif defaults to include all channels)

        bipolar_reference: bool (default False)
            A boolean indicating whether bipolar references between respective
            channels should be calculated and subsequently considered as traces

        leads: List[str] (default None)
            The leads for whose channels to perform bipolar referencing.
            NOTE: 'leads' cannot be None if 'bipolar_reference' is True

        Returns
        -------
        List[Trace]
            A list of Trace objects containing EEG data.

        Raises
        ------
        Exception
            If the file format is not supported.
        """
        filename = path[path.rfind("/") + 1 :]
        logger.debug(f"Loading file {filename}")
        file_format = path[path.rfind(".") + 1 :].lower()

        if file_format == HDF5:
            return self.read_h5_file(path, channel_paths, bipolar_reference, leads)
        elif file_format in [EDF, FIF]:
            return self.read_edf_or_fif_file(
                path, file_format, channel_paths, bipolar_reference, leads
            )
        else:
            raise Exception(
                f"The file format {file_format} ist not supported by this application"
            )

    def read_h5_file(
        self,
        file_path: str,
        channel_paths: List[str],
        bipolar_reference: bool = False,
        leads: List[str] = None,
    ) -> List[Trace]:
        """
        Loads a file in HDF5 format and transforms its content to a list of Trace objects.
        Provides the option to perform bipolar referencing for channels within a lead,
        if the leads are provided as argument.

        Parameters
        ----------
        file_path : str
            The path to the HDF5 file.

        channel_paths : List[str]
            Paths to the channels to include within the file

        bipolar_reference: bool (default False)
            A boolean indicating whether bipolar references between respective channels
            should be calculated and subsequently considered as traces

        leads: List[str] (default None)
            The leads for whose channels to perform bipolar referencing.
            NOTE: 'leads' cannot be None if 'bipolar_reference' is True

        Returns
        -------
        List[Trace]
            A list of Trace objects representing the content of the HDF5 file.

        Raises
        ------
        Exception
            If the channel paths are None.
        """
        if channel_paths is None:
            raise Exception(
                "Paths to the channels within the file can not be None for h5"
            )

        h5_file = h5py.File(file_path, "r")

        # Extract the raw datasets from the hdf5 file
        raw_traces: List[Dataset] = [h5_file.get(path) for path in channel_paths]

        # Extract start timestamps for datasets
        start_timestamps: List[float] = [
            self.extract_start_timestamp(path, h5_file) for path in channel_paths
        ]

        # Extract channel names from the dataset paths
        channel_names = self.extract_channel_names(channel_paths)

        # Extract frequencies from datasets
        frequencies: List[float] = [
            raw_trace.attrs.get("sfreq") for raw_trace in raw_traces
        ]

        if bipolar_reference:
            # Generate an instance of mne.io.RawArray from the h5 Datasets
            # in order to generate bipolar references
            raw: RawArray = RawArray(
                np.array(raw_traces),
                info=mne.create_info(
                    ch_names=channel_names,
                    ch_types="eeg",
                    sfreq=frequencies[0],
                    verbose=False,
                ),
                verbose=False,
            )
            raw = self.generate_bipolar_references(raw, leads)
            raw_traces = raw.get_data()

        return [
            self.create_trace(label, data, freq, ts)
            for label, data, freq, ts in zip(
                channel_names, raw_traces, frequencies, start_timestamps
            )
        ]

    def read_edf_or_fif_file(
        self,
        file_path: str,
        file_format: str,
        channel_paths: List[str],
        bipolar_reference: bool = False,
        leads: List[str] = None,
    ):
        """
        Loads a file in either FIF or EDF format and transforms its content to a list of Trace objects.
        Provides the option to perform bipolar referencing for channels within a lead,
        if the leads are provided as argument.

        Parameters
        ----------
        file_path : str
            The path to the file.

        file_format : str
            format indicating whether the file is of type FIF or EDF

        channel_paths : List[str]
            Paths to the channels to include within the file
            (defaults to all if non are present)

        bipolar_reference: bool (default False)
            A boolean indicating whether bipolar references between respective channels
            should be calculated and subsequently considered as traces

        leads: List[str] (default None)
            The leads for whose channels to perform bipolar referencing.
            NOTE: 'leads' cannot be None if 'bipolar_reference' is True

        Returns
        -------
        List[Trace]
            A list of Trace objects representing the content of the file.
        """
        raw: RawArray = (
            mne.io.read_raw_fif(file_path, preload=True, verbose=False)
            if file_format == FIF
            else mne.io.read_raw_edf(file_path, preload=True, verbose=False)
        )

        if channel_paths is not None:
            channel_names = self.extract_channel_names(channel_paths)
            raw = raw.pick(channel_names)

        if bipolar_reference:
            raw = self.generate_bipolar_references(raw, leads)

        return [
            self.create_trace(
                label, times, raw.info["sfreq"], raw.info["meas_date"].timestamp()
            )
            for label, times in zip(raw.ch_names, raw.get_data())
        ]

    @staticmethod
    def load_spike_detection_functions(
        file_path: str, start_timestamp: float, sfreq: int = 50
    ) -> List[SpikeDetectionFunction]:
        logger.debug(f"Loading spike detection functions {file_path}")
        data_matrix = np.genfromtxt(file_path, delimiter=",")

        # Compute times for x-axis
        times = compute_rescaled_timeline(
            start_timestamp=start_timestamp,
            length=data_matrix.shape[1],
            sfreq=sfreq,
        )

        # Create unique id prefix
        rank = file_path[file_path.find("/k=") + 1]
        dir_path = file_path[: file_path.find("/k=")]
        unique_id_prefix = f"{dir_path[dir_path.rfind('/') + 1:]}_rank_{rank}"

        # Create return objects
        spike_detection_functions: List[SpikeDetectionFunction] = []

        for idx, sdf in enumerate(data_matrix):
            # Create SpikeDetectionFunction
            label_sdf = f"H{idx}" if H_KEYWORD in file_path else LABEL_STD_LL
            unique_id_sdf = f"{unique_id_prefix}_{label_sdf}"
            spike_detection_fct = SpikeDetectionFunction(
                label=label_sdf, unique_id=unique_id_sdf, times=times, data_array=sdf
            )

            spike_detection_functions.append(spike_detection_fct)

        return spike_detection_functions
