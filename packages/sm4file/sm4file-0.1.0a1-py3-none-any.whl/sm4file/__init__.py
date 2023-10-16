from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List
from datetime import datetime

import numpy as np
from numpy._typing import NDArray

from .sm4_object_types import StringData

from .sm4_file import (
    Sm4FileAll,
    RhkPageType,
    RhkLineType,
    RhkImageType,
    RhkScanType,
    Sm4PageHeaderDefault,
)


@dataclass()
class Sm4Channel:
    """Class with information about a channel

    page_type: Type of page/channel
    line_type: Type of line
    datetime: Datetime of measurement
    xres: Resolution in x, e.g. number of pixels for images
    yres: Resolution in y, e.g. number of pixels for images
    image_type: Type of image
    scan_type: Type of scan
    scan_direction: Direction of scanning
    xsize: Physical size of e.g. image in x (in m)
    ysize: Physical size of e.g. image in y (in m)
    z_scale:
    x_offset:
    y_offset:
    z_offset:
    period: Acquisition time of a single data point (in s)
    bias: Bias voltage (in V)
    current: Tunneling current (in A)
    angle: Scan angle (in deg)
    data: Mesuremet data
    """

    label: str
    page_type: RhkPageType
    line_type: RhkLineType
    datetime: datetime
    xres: int
    yres: int
    image_type: RhkImageType
    scan_type: RhkScanType
    scan_direction: str
    xsize: float
    ysize: float
    z_scale: float
    x_offset: float
    y_offset: float
    z_offset: float
    period: float
    bias: float
    current: float
    angle: float
    data: NDArray[np.float32]


class Sm4:
    def __init__(self, filepath: str):
        self.filepath = filepath
        sm4file = Sm4FileAll(filepath)
        self.prm_str = sm4file.file_header.prm.prm_data
        self._channels: List[Sm4Channel] = []
        for ch in sm4file.pages:
            if isinstance(ch.header, Sm4PageHeaderDefault):
                ch_datetime = None
                for i in ch.header.page_header_objects:
                    if type(i) == StringData:
                        month_str, day_str, year_str = i.date.split("/")
                        year_str = "20" + year_str
                        month, day, year = (
                            int(month_str),
                            int(day_str),
                            int(year_str),
                        )
                        hour, min, sec = [int(x) for x in i.time.split(":")]
                        ch_datetime = datetime(
                            year, month, day, hour, min, sec
                        )

                # fallback to file stats
                if ch_datetime is None:
                    file_datetime = Path(filepath).stat().st_ctime
                    ch_datetime = datetime.fromtimestamp(file_datetime)

                self._channels.append(
                    Sm4Channel(
                        label=ch.label,
                        page_type=ch.header.page_type,
                        line_type=ch.header.line_type,
                        datetime=ch_datetime,
                        xres=ch.header.x_size,
                        yres=ch.header.y_size,
                        image_type=ch.header.image_type,
                        scan_type=ch.header.scan_type,
                        scan_direction=ch.header.scan_type.direction(),
                        xsize=abs(ch.header.x_scale * ch.header.x_size),
                        ysize=abs(ch.header.y_scale * ch.header.y_size),
                        z_scale=ch.header.z_scale,
                        x_offset=ch.header.x_offset,
                        y_offset=ch.header.y_offset,
                        z_offset=ch.header.z_offset,
                        period=ch.header.period,
                        bias=ch.header.bias,
                        current=ch.header.current,
                        angle=ch.header.angle,
                        data=ch.data.data,
                    )
                )

    def __repr__(self) -> str:
        return repr(self._channels)

    def __len__(self) -> int:
        return len(self._channels)

    def __getitem__(self, idx: int) -> Sm4Channel:
        return self._channels[idx]

    def __setitem__(self, idx: int, item: Sm4Channel) -> None:
        self._channels[idx] = item

    def __delitem__(self, idx: int) -> None:
        del self._channels[idx]

    def __iter__(self) -> Iterator[Sm4Channel]:
        return iter(self._channels)

    def save_prm(self, out_file: str) -> None:
        with open(out_file, "w") as f:
            f.write(self.prm_str)

    def topography_channels(self) -> List[Sm4Channel]:
        return [
            ch
            for ch in self
            if ch.page_type == RhkPageType.RHK_PAGE_TOPOGRAPHIC
        ]

    def current_channels(self) -> List[Sm4Channel]:
        return [
            ch for ch in self if ch.page_type == RhkPageType.RHK_PAGE_CURRENT
        ]
