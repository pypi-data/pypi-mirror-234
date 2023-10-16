# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

from __future__ import annotations

import dataclasses as dtcl
from pathlib import Path as path_t
from typing import Any, Callable, Dict, Iterator, List, Optional, Sequence, Union

import numpy as nmpy
from logger_36 import LOGGER
from skimage.transform import resize as Resize

from cell_tracking_BC.standard.number import MAX_INT
from cell_tracking_BC.standard.uid import Identity
from cell_tracking_BC.type.acquisition.frame import (
    AsUncompressedArray,
    NewFromArray,
    frame_t,
)

array_t = nmpy.ndarray
channel_computation_h = Callable[[Dict[str, array_t], Dict[str, Any]], array_t]
# ...=[array_t, **kwargs]
transform_h = Callable[..., array_t]


class frames_t(List[frame_t]):
    """"""

    def append(self, uncompressed: array_t, /) -> None:
        """"""
        list.append(self, NewFromArray(uncompressed))

    def extend(self, frames: Sequence[array_t], /) -> None:
        """"""
        for uncompressed in frames:
            list.append(self, NewFromArray(uncompressed))

    def __setitem__(self, index: int, uncompressed: array_t, /) -> None:
        """"""
        list.__setitem__(self, index, NewFromArray(uncompressed))

    def __getitem__(self, index: int, /) -> array_t:
        """"""
        return AsUncompressedArray(list.__getitem__(self, index))

    def __iter__(self) -> Iterator[array_t]:
        """"""
        for frame in list.__iter__(self):
            yield AsUncompressedArray(frame)


@dtcl.dataclass(repr=False, eq=False)
class sequence_t(Dict[str, frames_t]):
    """"""

    path: path_t = None
    shape: tuple[int, int] = None
    original_length: int = None
    first_frame: int = None
    length: int = None
    base_channels: Sequence[
        str
    ] = None  # Those present in the sequence file and retained for use
    plot_channel: str = None  # Channel used as default for plotting

    @classmethod
    def NewFromFrames(
        cls,
        frames: array_t,
        in_channel_names: Sequence[Optional[str]],
        plot_channel: str,
        path: path_t,
        /,
        *,
        first_frame: int = 0,
        last_frame: int = MAX_INT,
        expected_shape: Sequence[int] = None,
    ) -> sequence_t:
        """
        in_channel_names: names equal to None or "___" or "---" indicate channels that should be discarded
        """
        # TODO: make this function accept various input shapes thanks to an additional arrangement parameter of the
        #     form THRC, T=time, H=channel, RC= row column. This requires that SequenceFromPath deals with TH combined
        #     dimension.
        if (n_dims := frames.ndim) not in (3, 4):
            raise ValueError(
                f"{n_dims}: Invalid number of dimensions of sequence with shape {frames.shape}. "
                f"Expected=3 or 4=(TIME POINTS*CHANNELS)xROWSxCOLUMNS or "
                f"TIME POINTSxCHANNELSxROWSxCOLUMNS."
            )
        n_in_channels = in_channel_names.__len__()

        if n_dims == 3:
            original_length = frames.shape[0] // n_in_channels
            frames = frames[
                (first_frame * n_in_channels) : ((last_frame + 1) * n_in_channels), ...
            ]
        else:
            original_length = frames.shape[0]
            frames = frames[first_frame : (last_frame + 1), ...]
        first_frame = 0
        last_frame = MAX_INT

        if expected_shape is not None:
            if n_dims == 3:
                order_in = (0, 1, 2)
                order_out = (2, 0, 1)
                fixed_size = frames.shape[:1]
                to_be_resized = frames.shape[1:]
            else:
                order_in = (0, 1, 2, 3)
                order_out = (2, 3, 0, 1)
                fixed_size = frames.shape[:2]
                to_be_resized = frames.shape[2:]
            if to_be_resized != expected_shape:
                LOGGER.warning(
                    f"Resizing sequence from actual size {to_be_resized} (full shape={frames.shape}) "
                    f"to expected size {expected_shape}"
                )
                frames = nmpy.moveaxis(frames, order_in, order_out)
                frames = Resize(
                    frames, (*expected_shape, *fixed_size), preserve_range=True
                )
                frames = nmpy.moveaxis(frames, order_out, order_in)
                LOGGER.info(f"Resizing done. New sequence shape={frames.shape}")

        frames_of_channel = {}
        for name in in_channel_names:
            if (name is not None) and (name != "___") and (name != "---"):
                frames_of_channel[name] = frames_t()
        base_channel_names = tuple(frames_of_channel.keys())

        if n_dims == 3:
            c_idx = n_in_channels - 1
            time_point = -1
            for frame in frames:
                c_idx += 1
                if c_idx == n_in_channels:
                    c_idx = 0
                    time_point += 1

                if time_point < first_frame:
                    continue
                elif time_point > last_frame:
                    break

                name = in_channel_names[c_idx]
                if name in base_channel_names:
                    frames_of_channel[name].append(frame)
        else:
            for time_point, frame in enumerate(frames):
                if time_point < first_frame:
                    continue
                elif time_point > last_frame:
                    break

                for c_idx, channel in enumerate(frame):
                    name = in_channel_names[c_idx]
                    if name in base_channel_names:
                        frames_of_channel[name].append(channel)

        frames_of_base_channel = frames_of_channel[base_channel_names[0]]
        shape = frames_of_base_channel[0].shape
        length = frames_of_base_channel.__len__()
        instance = cls(
            path=path,
            shape=shape,
            original_length=original_length,
            first_frame=first_frame,
            length=length,
            base_channels=base_channel_names,
            plot_channel=plot_channel,
        )
        instance.update(frames_of_channel)

        return instance

    def AddChannel(
        self, name: str, ChannelComputation: channel_computation_h, /, **kwargs
    ) -> None:
        """"""
        if name in self:
            raise ValueError(f"{name}: Existing channel cannot be overridden")

        computed = frames_t()
        for frames in self.FramesIterator():
            frames_as_dict = dict(zip(self.channels, frames))
            frame = ChannelComputation(frames_as_dict, **kwargs)
            computed.append(frame)

        self[name] = computed

    @property
    def channels(self) -> tuple[str, ...]:
        """
        Names of channels read from file (base channels) and computed channels
        """
        return tuple(self.keys())

    def ChannelExtrema(self, channel: str, /) -> tuple[float, float]:
        """"""
        min_intensity = nmpy.Inf
        max_intensity = -nmpy.Inf

        for frame in self[channel]:
            min_intensity = min(min_intensity, nmpy.amin(frame))
            max_intensity = max(max_intensity, nmpy.amax(frame))

        # Apparently, the intensities might not be Numpy object in certain situations (Numpy version?). Although
        # currently unexplained, an easy workaround is to return the intensities as is.
        try:
            output = min_intensity.item(), max_intensity.item()
        except AttributeError:
            output = min_intensity, max_intensity

        return output

    def FramesIterator(
        self,
        /,
        *,
        channels: Union[str, Sequence[str]] = None,
    ) -> Iterator[Sequence[array_t]]:
        """
        channel: None=all (!) channels
        """
        if channels is None:
            channels = self.channels
        elif isinstance(channels, str):
            channels = (channels,)

        for f_idx in range(self.length):
            output = tuple(self[_chl][f_idx] for _chl in channels)
            yield output

    def ApplyTransform(
        self,
        Transform: transform_h,
        /,
        *,
        channel: Union[str, Sequence[str]] = None,
        **kwargs,
    ) -> None:
        """
        channel: None=all (!) base channels
        """
        if channel is None:
            channels = self.base_channels
        elif isinstance(channel, str):
            channels = (channel,)
        else:
            channels = channel

        for channel in channels:
            targets = self[channel]
            references_sets = self.FramesIterator()
            for target, references in zip(targets, references_sets):
                refs_as_dict = dict(zip(self.channels, references))
                transformed = Transform(target, channels=refs_as_dict, **kwargs)
                target[...] = transformed[...]

    def AsArray(
        self,
        /,
        *,
        channel: Union[str, Sequence[str]] = None,
    ) -> array_t:
        """"""
        if channel is None:
            channels = self.channels
            multi_channel = channels.__len__() > 1
        elif isinstance(channel, str):
            channels = (channel,)
            multi_channel = False
        else:
            channels = channel
            multi_channel = channels.__len__() > 1

        if multi_channel:
            frames = (
                nmpy.dstack(_chl) for _chl in self.FramesIterator(channels=channels)
            )
            extra_axis = 3
        else:
            frames = (_chl[0] for _chl in self.FramesIterator(channels=channels))
            extra_axis = 2

        return nmpy.stack(tuple(frames), axis=extra_axis)

    def __hash__(self) -> int:
        """
        Note that (from Python documentation:
            if it defines __eq__() but not __hash__(), its instances will not be usable as items in hashable collections
        """
        return hash((self.path, self.shape, self.first_frame, self.length))

    __repr__ = Identity

    def __str__(self) -> str:
        """"""
        all_extrema = []
        for channel in self.channels:
            dtype = self[channel][0].dtype
            minimum, maximum = self.ChannelExtrema(channel)
            if nmpy.issubdtype(dtype, nmpy.integer):
                extrema = f"{minimum},{maximum}"
            else:
                extrema = f"{minimum:.3},{maximum:.3}"
            all_extrema.append(f"{channel}:{dtype.name}=[{extrema}]")
        all_extrema = ", ".join(all_extrema)

        return (
            f"{repr(self)}\n"
            f"    Path: {self.path}\n"
            f"    Acquired channels: {self.base_channels}\n"
            f"    Computed channels: {tuple(set(self.channels).difference(self.base_channels))}\n"
            f"    Extrema: {all_extrema}\n"
            f"    Shape: {self.shape}\n"
            f"    Length: {self.original_length}\n"
            f"    Processed length: {self.length} from frame idx {self.first_frame}\n"
        )
