from __future__ import annotations
from typing import List
from enum import Enum
from dataclasses import dataclass
import zlib

import numpy as np
from numpy._typing import NDArray

from .cursor import Cursor


class RhkDriftOptionType(Enum):
    RHK_DRIFT_DISABLED = 0
    RHK_DRIFT_EACH_SPECTRA = 1
    RHK_DRIFT_EACH_LOCATION = 2


@dataclass
class PageData:
    data: NDArray[np.float32]

    @classmethod
    def from_buffer(
        cls, cursor: Cursor, size: int, z_scale: float, z_offset: float
    ) -> PageData:
        # cursor.set_position(offset)

        raw_data = np.frombuffer(cursor.read(size), dtype=np.int32)
        data: NDArray[np.float32] = raw_data * z_scale + z_offset
        return cls(data)


@dataclass
class ImageDriftHeader:
    imagedrift_filetime: int
    imagedrift_drift_option_type: RhkDriftOptionType

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> ImageDriftHeader:
        imagedrift_filetime = cursor.read_u64_le()
        imagedrift_drift_option_type = RhkDriftOptionType(cursor.read_u32_le())

        return cls(imagedrift_filetime, imagedrift_drift_option_type)


@dataclass
class ImageDriftData:
    imagedrift_time: int
    imagedrift_dx: int
    imagedrift_dy: int
    imagedrift_cumulative_x: int
    imagedrift_cumulative_y: int
    imagedrift_vector_x: int
    imagedrift_vector_y: int

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> ImageDriftData:
        imagedrift_time = cursor.read_u32_le()
        imagedrift_dx = cursor.read_u32_le()
        imagedrift_dy = cursor.read_u32_le()
        imagedrift_cumulative_x = cursor.read_u32_le()
        imagedrift_cumulative_y = cursor.read_u32_le()
        imagedrift_vector_x = cursor.read_u32_le()
        imagedrift_vector_y = cursor.read_u32_le()

        return cls(
            imagedrift_time,
            imagedrift_dx,
            imagedrift_dy,
            imagedrift_cumulative_x,
            imagedrift_cumulative_y,
            imagedrift_vector_x,
            imagedrift_vector_y,
        )


@dataclass
class SpecDriftHeader:
    specdrift_filetime: int
    specdrift_drift_option_type: int
    specdrift_drift_option_type_name: str
    specdrift_channel: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> SpecDriftHeader:
        # unix epoch
        specdrift_filetime = cursor.read_u64_le()
        specdrift_drift_option_type = cursor.read_u32_le()
        if specdrift_drift_option_type == 0:
            specdrift_drift_option_type_name = "RHK_DRIFT_DISABLED"
        elif specdrift_drift_option_type == 1:
            specdrift_drift_option_type_name = "RHK_DRIFT_EACH_SPECTRA"
        elif specdrift_drift_option_type == 1:
            specdrift_drift_option_type_name = "RHK_DRIFT_EACH_LOCATION"
        else:
            specdrift_drift_option_type_name = "RHK_DRIFT_UNKNOWN"

        _ = cursor.read_u32_le()
        specdrift_channel = cursor.read_sm4_string()

        return cls(
            specdrift_filetime,
            specdrift_drift_option_type,
            specdrift_drift_option_type_name,
            specdrift_channel,
        )


@dataclass
class SpecDriftData:
    specdrift_time: List[float]
    specdrift_x_coord: List[float]
    specdrift_y_coord: List[float]
    specdrift_dx: List[float]
    specdrift_dy: List[float]
    specdrift_cumulative_x: List[float]
    specdrift_cumulative_y: List[float]

    @classmethod
    def from_buffer(cls, cursor: Cursor, y_size: int) -> SpecDriftData:
        specdrift_time: List[float] = []
        specdrift_x_coord: List[float] = []
        specdrift_y_coord: List[float] = []
        specdrift_dx: List[float] = []
        specdrift_dy: List[float] = []
        specdrift_cumulative_x: List[float] = []
        specdrift_cumulative_y: List[float] = []

        for _ in range(y_size):
            specdrift_time.append(cursor.read_f32_le())
            specdrift_x_coord.append(cursor.read_f32_le())
            specdrift_y_coord.append(cursor.read_f32_le())
            specdrift_dx.append(cursor.read_f32_le())
            specdrift_dy.append(cursor.read_f32_le())
            specdrift_cumulative_x.append(cursor.read_f32_le())
            specdrift_cumulative_y.append(cursor.read_f32_le())

        return cls(
            specdrift_time,
            specdrift_x_coord,
            specdrift_y_coord,
            specdrift_dx,
            specdrift_dy,
            specdrift_cumulative_x,
            specdrift_cumulative_y,
        )


@dataclass
class StringData:
    label: str
    system_text: str
    session_text: str
    user_text: str
    filename: str
    date: str
    time: str
    x_units: str
    y_units: str
    z_units: str
    x_label: str
    y_label: str
    status_channel_text: str
    completed_line_count: str
    oversampling_count: str
    sliced_voltage: str
    pll_pro_status: str
    setpoint_unit: str
    channel_list: str

    @classmethod
    def from_buffer(cls, cursor: Cursor, count: int) -> StringData:
        strings = [cursor.read_sm4_string() for _ in range(count)]

        label = strings[0]
        system_text = strings[1]
        session_text = strings[2]
        user_text = strings[3]
        filename = strings[4]
        date = strings[5]
        time = strings[6]
        x_units = strings[7]
        y_units = strings[8]
        z_units = strings[9]
        x_label = strings[10]
        y_label = strings[11]
        status_channel_text = strings[12]
        completed_line_count = strings[13]
        try:
            oversampling_count = strings[14]
            sliced_voltage = strings[15]
            pll_pro_status = strings[16]
            setpoint_unit = strings[17]
            channel_list = strings[18]
        except IndexError:
            oversampling_count = ""
            sliced_voltage = ""
            pll_pro_status = ""
            setpoint_unit = ""
            channel_list = ""

        return cls(
            label,
            system_text,
            session_text,
            user_text,
            filename,
            date,
            time,
            x_units,
            y_units,
            z_units,
            x_label,
            y_label,
            status_channel_text,
            completed_line_count,
            oversampling_count,
            sliced_voltage,
            pll_pro_status,
            setpoint_unit,
            channel_list,
        )


@dataclass
class TipTrackHeader:
    tiptrack_filetime: int
    tiptrack_feature_height: float
    tiptrack_feature_width: float
    tiptrack_time_constant: float
    tiptrack_cycle_rate: float
    tiptrack_phase_lag: float
    tiptrack_tiptrack_info_count: int
    tiptrack_channel: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> TipTrackHeader:
        # unix epoch
        tiptrack_filetime = cursor.read_u64_le()
        tiptrack_feature_height = cursor.read_f32_le()
        tiptrack_feature_width = cursor.read_f32_le()
        tiptrack_time_constant = cursor.read_f32_le()
        tiptrack_cycle_rate = cursor.read_f32_le()
        tiptrack_phase_lag = cursor.read_f32_le()
        _ = cursor.read_u32_le()
        tiptrack_tiptrack_info_count = cursor.read_u32_le()
        tiptrack_channel = cursor.read_sm4_string()

        return cls(
            tiptrack_filetime,
            tiptrack_feature_height,
            tiptrack_feature_width,
            tiptrack_time_constant,
            tiptrack_cycle_rate,
            tiptrack_phase_lag,
            tiptrack_tiptrack_info_count,
            tiptrack_channel,
        )


@dataclass
class TipTrackData:
    tiptrack_cumulative_time: List[float]
    tiptrack_time: List[float]
    tiptrack_dx: List[float]
    tiptrack_dy: List[float]

    @classmethod
    def from_buffer(
        cls, cursor: Cursor, tiptrack_tiptrack_info_count: int
    ) -> TipTrackData:
        tiptrack_cumulative_time: List[float] = []
        tiptrack_time: List[float] = []
        tiptrack_dx: List[float] = []
        tiptrack_dy: List[float] = []

        for _ in range(tiptrack_tiptrack_info_count):
            tiptrack_cumulative_time.append(cursor.read_f32_le())
            tiptrack_time.append(cursor.read_f32_le())
            tiptrack_dx.append(cursor.read_f32_le())
            tiptrack_dy.append(cursor.read_f32_le())

        return cls(
            tiptrack_cumulative_time,
            tiptrack_time,
            tiptrack_dx,
            tiptrack_dy,
        )


@dataclass
class Prm:
    prm_data: str

    @classmethod
    def from_buffer(
        cls,
        cursor: Cursor,
        prm_compression_flag: int,
        prm_data_size: int,
        prm_compression_size: int,
    ) -> Prm:
        if prm_compression_flag == 0:
            prm_data_raw = cursor.read(prm_data_size)
        else:
            prm_data_raw = zlib.decompress(
                cursor.read(prm_compression_size),
                wbits=0,
                bufsize=prm_data_size,
            )

        prm_data = prm_data_raw.decode("CP437")
        return cls(prm_data)


@dataclass
class PrmHeader:
    prm_compression_flag: int
    prm_data_size: int
    prm_compression_size: int

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> PrmHeader:
        prm_compression_flag = cursor.read_u32_le()
        prm_data_size = cursor.read_u32_le()
        prm_compression_size = cursor.read_u32_le()

        # read the actual PRM data

        return cls(
            prm_compression_flag,
            prm_data_size,
            prm_compression_size,
        )


@dataclass
class ApiInfo:
    voltage_high: float
    voltage_low: float
    gain: float
    api_offset: float
    ramp_mode: int
    ramp_type: int
    step: int
    image_count: int
    dac: int
    mux: int
    bias: int
    units: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> ApiInfo:
        voltage_high = cursor.read_f32_le()
        voltage_low = cursor.read_f32_le()
        gain = cursor.read_f32_le()
        api_offset = cursor.read_f32_le()

        ramp_mode = cursor.read_u32_le()
        ramp_type = cursor.read_u32_le()
        step = cursor.read_u32_le()
        image_count = cursor.read_u32_le()
        dac = cursor.read_u32_le()
        mux = cursor.read_u32_le()
        bias = cursor.read_u32_le()

        _ = cursor.read_u32_le()
        units = cursor.read_sm4_string()

        return cls(
            voltage_high,
            voltage_low,
            gain,
            api_offset,
            ramp_mode,
            ramp_type,
            step,
            image_count,
            dac,
            mux,
            bias,
            units,
        )


@dataclass
class PiezoSensitivity:
    tube_x: float
    tube_y: float
    tube_z: float
    tube_z_offset: float
    scan_x: float
    scan_y: float
    scan_z: float
    actuator: float
    tube_x_unit: str
    tube_y_unit: str
    tube_z_unit: str
    tube_z_unit_offset: str
    scan_x_unit: str
    scan_y_unit: str
    scan_z_unit: str
    actuator_unit: str
    tube_calibration: str
    scan_calibration: str
    actuator_calibration: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> PiezoSensitivity:
        tube_x = cursor.read_f64_le()
        tube_y = cursor.read_f64_le()
        tube_z = cursor.read_f64_le()
        tube_z_offset = cursor.read_f64_le()
        scan_x = cursor.read_f64_le()
        scan_y = cursor.read_f64_le()
        scan_z = cursor.read_f64_le()
        actuator = cursor.read_f64_le()

        _ = cursor.read_u32_le()

        tube_x_unit = cursor.read_sm4_string()
        tube_y_unit = cursor.read_sm4_string()
        tube_z_unit = cursor.read_sm4_string()
        tube_z_unit_offset = cursor.read_sm4_string()
        scan_x_unit = cursor.read_sm4_string()
        scan_y_unit = cursor.read_sm4_string()
        scan_z_unit = cursor.read_sm4_string()
        actuator_unit = cursor.read_sm4_string()
        tube_calibration = cursor.read_sm4_string()
        scan_calibration = cursor.read_sm4_string()
        actuator_calibration = cursor.read_sm4_string()

        return cls(
            tube_x,
            tube_y,
            tube_z,
            tube_z_offset,
            scan_x,
            scan_y,
            scan_z,
            actuator,
            tube_x_unit,
            tube_y_unit,
            tube_z_unit,
            tube_z_unit_offset,
            scan_x_unit,
            scan_y_unit,
            scan_z_unit,
            actuator_unit,
            tube_calibration,
            scan_calibration,
            actuator_calibration,
        )


@dataclass
class FrequencySweepData:
    psd_total_signal: float
    peak_frequency: float
    peak_amplitude: float
    drive_aplitude: float
    signal_to_drive_ratio: float
    q_factor: float
    total_signal_unit: str
    peak_frequency_unit: str
    peak_amplitude_unit: str
    drive_amplitude_unit: str
    signal_to_drive_ratio_unit: str
    q_factor_unit: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> FrequencySweepData:
        psd_total_signal = cursor.read_f64_le()
        peak_frequency = cursor.read_f64_le()
        peak_amplitude = cursor.read_f64_le()
        drive_aplitude = cursor.read_f64_le()
        signal_to_drive_ratio = cursor.read_f64_le()
        q_factor = cursor.read_f64_le()

        _ = cursor.read_u32_le()

        total_signal_unit = cursor.read_sm4_string()
        peak_frequency_unit = cursor.read_sm4_string()
        peak_amplitude_unit = cursor.read_sm4_string()
        drive_amplitude_unit = cursor.read_sm4_string()
        signal_to_drive_ratio_unit = cursor.read_sm4_string()
        q_factor_unit = cursor.read_sm4_string()

        return cls(
            psd_total_signal,
            peak_frequency,
            peak_amplitude,
            drive_aplitude,
            signal_to_drive_ratio,
            q_factor,
            total_signal_unit,
            peak_frequency_unit,
            peak_amplitude_unit,
            drive_amplitude_unit,
            signal_to_drive_ratio_unit,
            q_factor_unit,
        )


@dataclass
class ScanProcessorInfo:
    x_slope_compensation: float
    y_slope_compensation: float
    x_slope_compensation_unit: str
    y_slope_compensation_unit: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> ScanProcessorInfo:
        x_slope_compensation = cursor.read_f64_le()
        y_slope_compensation = cursor.read_f64_le()
        _ = cursor.read_u32_le()
        x_slope_compensation_unit = cursor.read_sm4_string()
        y_slope_compensation_unit = cursor.read_sm4_string()

        return cls(
            x_slope_compensation,
            y_slope_compensation,
            x_slope_compensation_unit,
            y_slope_compensation_unit,
        )


@dataclass
class PllInfo:
    amplitude_control: int
    drive_amplitude: float
    drive_ref_frequency: float
    lockin_freq_offset: float
    lockin_harmonic_factor: float
    lockin_phase_offset: float
    pi_gain: float
    pi_int_cutoff_frequency: float
    pi_lower_bound: float
    pi_upper_bound: float
    diss_pi_gain: float
    diss_pi_int_cutoff_frequency: float
    diss_pi_lower_bound: float
    diss_pi_upper_bound: float
    lockin_filter_cutoff_frequency: str
    drive_amplitude_unit: str
    drive_ref_frequency_unit: str
    lockin_freq_offset_unit: str
    lockin_harmonic_factor_unit: str
    lockin_phase_offset_unit: str
    pi_gain_unit: str
    pi_int_cutoff_frequency_unit: str
    pi_lower_bound_unit: str
    pi_upper_bound_unit: str
    diss_pi_gain_unit: str
    diss_pi_int_cutoff_frequency_unit: str
    diss_pi_lower_bound_unit: str
    diss_pi_upper_bound_unit: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> PllInfo:
        amplitude_control = cursor.read_u32_le()
        drive_amplitude = cursor.read_f64_le()
        drive_ref_frequency = cursor.read_f64_le()
        lockin_freq_offset = cursor.read_f64_le()
        lockin_harmonic_factor = cursor.read_f64_le()
        lockin_phase_offset = cursor.read_f64_le()
        pi_gain = cursor.read_f64_le()
        pi_int_cutoff_frequency = cursor.read_f64_le()
        pi_lower_bound = cursor.read_f64_le()
        pi_upper_bound = cursor.read_f64_le()
        diss_pi_gain = cursor.read_f64_le()
        diss_pi_int_cutoff_frequency = cursor.read_f64_le()
        diss_pi_lower_bound = cursor.read_f64_le()
        diss_pi_upper_bound = cursor.read_f64_le()

        lockin_filter_cutoff_frequency = cursor.read_sm4_string()

        drive_amplitude_unit = cursor.read_sm4_string()
        drive_ref_frequency_unit = cursor.read_sm4_string()
        lockin_freq_offset_unit = cursor.read_sm4_string()
        lockin_harmonic_factor_unit = cursor.read_sm4_string()
        lockin_phase_offset_unit = cursor.read_sm4_string()
        pi_gain_unit = cursor.read_sm4_string()
        pi_int_cutoff_frequency_unit = cursor.read_sm4_string()
        pi_lower_bound_unit = cursor.read_sm4_string()
        pi_upper_bound_unit = cursor.read_sm4_string()
        diss_pi_gain_unit = cursor.read_sm4_string()
        diss_pi_int_cutoff_frequency_unit = cursor.read_sm4_string()
        diss_pi_lower_bound_unit = cursor.read_sm4_string()
        diss_pi_upper_bound_unit = cursor.read_sm4_string()

        return cls(
            amplitude_control,
            drive_amplitude,
            drive_ref_frequency,
            lockin_freq_offset,
            lockin_harmonic_factor,
            lockin_phase_offset,
            pi_gain,
            pi_int_cutoff_frequency,
            pi_lower_bound,
            pi_upper_bound,
            diss_pi_gain,
            diss_pi_int_cutoff_frequency,
            diss_pi_lower_bound,
            diss_pi_upper_bound,
            lockin_filter_cutoff_frequency,
            drive_amplitude_unit,
            drive_ref_frequency_unit,
            lockin_freq_offset_unit,
            lockin_harmonic_factor_unit,
            lockin_phase_offset_unit,
            pi_gain_unit,
            pi_int_cutoff_frequency_unit,
            pi_lower_bound_unit,
            pi_upper_bound_unit,
            diss_pi_gain_unit,
            diss_pi_int_cutoff_frequency_unit,
            diss_pi_lower_bound_unit,
            diss_pi_upper_bound_unit,
        )


@dataclass
class ChannelDriveInfo:
    master_osciallator: int
    amplitude: float
    frequency: float
    phase_offset: float
    harmonic_factor: float
    amplitude_unit: str
    frequency_unit: str
    phase_offset_unit: str
    harmonic_factor_unit: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> ChannelDriveInfo:
        _ = cursor.read_u32_le()
        master_osciallator = cursor.read_u32_le()
        amplitude = cursor.read_f64_le()
        frequency = cursor.read_f64_le()
        phase_offset = cursor.read_f64_le()
        harmonic_factor = cursor.read_f64_le()
        amplitude_unit = cursor.read_sm4_string()
        frequency_unit = cursor.read_sm4_string()
        phase_offset_unit = cursor.read_sm4_string()
        harmonic_factor_unit = cursor.read_sm4_string()

        return cls(
            master_osciallator,
            amplitude,
            frequency,
            phase_offset,
            harmonic_factor,
            amplitude_unit,
            frequency_unit,
            phase_offset_unit,
            harmonic_factor_unit,
        )


@dataclass
class LockinInfo:
    num_strings: int
    non_master_oscillator: int
    frequency: float
    harmonic_factor: float
    phase_offset: float
    # these might be not included
    filter_cutoff_frequency: str
    frequency_unit: str
    phase_unit: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> LockinInfo:
        num_strings = cursor.read_u32_le()

        non_master_oscillator = cursor.read_u32_le()
        frequency = cursor.read_f64_le()
        harmonic_factor = cursor.read_f64_le()
        phase_offset = cursor.read_f64_le()
        # these might be not included
        filter_cutoff_frequency = cursor.read_sm4_string()
        frequency_unit = cursor.read_sm4_string()
        phase_unit = cursor.read_sm4_string()

        return cls(
            num_strings,
            non_master_oscillator,
            frequency,
            harmonic_factor,
            phase_offset,
            filter_cutoff_frequency,
            frequency_unit,
            phase_unit,
        )


@dataclass
class PiControllerInfo:
    setpoint: float
    proportional_gain: float
    integral_gain: float
    lower_bound: float
    upper_bound: float
    feedback_unit: str
    setpoint_unit: str
    proportional_gain_unit: str
    integral_gain_unit: str
    output_unit: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> PiControllerInfo:
        setpoint = cursor.read_f64_le()
        proportional_gain = cursor.read_f64_le()
        integral_gain = cursor.read_f64_le()
        lower_bound = cursor.read_f64_le()
        upper_bound = cursor.read_f64_le()
        _ = cursor.read_u32_le()
        feedback_unit = cursor.read_sm4_string()
        setpoint_unit = cursor.read_sm4_string()
        proportional_gain_unit = cursor.read_sm4_string()
        integral_gain_unit = cursor.read_sm4_string()
        output_unit = cursor.read_sm4_string()

        return cls(
            setpoint,
            proportional_gain,
            integral_gain,
            lower_bound,
            upper_bound,
            feedback_unit,
            setpoint_unit,
            proportional_gain_unit,
            integral_gain_unit,
            output_unit,
        )


@dataclass
class LowpassFilterInfo:
    info: str

    @classmethod
    def from_buffer(cls, cursor: Cursor) -> LowpassFilterInfo:
        _ = cursor.read_u32_le()
        lowpass_filter_info = cursor.read_sm4_string()

        return cls(lowpass_filter_info)
