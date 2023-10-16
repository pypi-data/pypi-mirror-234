# Copyright (c) ARAMI Physical Asset Management Pty Ltd T/A Bladesight Inc. (2023)

from numba import njit
import numpy as np
import pandas as pd

@njit
def calculate_aoa(
    arr_opr_zero_crossing : np.ndarray, 
    arr_probe_toas : np.ndarray
):
    """
    This function calculates the angle of arrival of 
    each ToA value relative to the revolution in 
    which it occurs.

    Args:
        arr_opr_zero_crossing (np.array): An array of 
            OPR zero-crossing times. 
        arr_probe_toas (np.array): An array of 
            ToA values.

    Returns:
        np.array: A matrix of AoA values. Each row in the 
            matrix corresponds to a ToA value. The columns 
            are:
            0: The revolution number
            1: The zero crossing time at the start of the revolution
            2: The zero crossing time at the end of the revolution
            3: The angular velocity of the revolution
            4: The ToA
            5: The AoA of the ToA value
    """
    num_toas = len(arr_probe_toas)
    AoA_matrix = np.zeros( (num_toas, 6))

    AoA_matrix[:, 0] = -1

    current_zero_crossing_start = arr_opr_zero_crossing[0]
    current_zero_crossing_end = arr_opr_zero_crossing[1]
    Omega = 2 * np.pi / (
        current_zero_crossing_end 
        - current_zero_crossing_start
    )
    current_n = 0

    for i, toa in enumerate(arr_probe_toas):

        while toa > current_zero_crossing_end:
            current_n += 1
            if current_n >= (len(arr_opr_zero_crossing) - 1):
                break
            current_zero_crossing_start = arr_opr_zero_crossing[current_n]
            current_zero_crossing_end = arr_opr_zero_crossing[current_n + 1]
            Omega = 2 * np.pi / (
                current_zero_crossing_end 
                - current_zero_crossing_start
            )
        if current_n >= (len(arr_opr_zero_crossing) - 1):
            break

        if toa > current_zero_crossing_start:
            AoA_matrix[i, 0] = current_n
            AoA_matrix[i, 1] = current_zero_crossing_start
            AoA_matrix[i, 2] = current_zero_crossing_end
            AoA_matrix[i, 3] = Omega
            AoA_matrix[i, 4] = toa
            AoA_matrix[i, 5] = Omega * (
                toa 
                - current_zero_crossing_start
            )

    return AoA_matrix

def transform_ToAs_to_AoAs(
    df_opr_zero_crossings : pd.DataFrame,
    df_probe_toas : pd.DataFrame,
) -> pd.DataFrame:
    """ This function transforms the ToA values to AoA values for a 
    single probe, given the OPR zero-crossing times and the proximity
    probe's ToA values. It receives Pandas DataFrames, and also
    cleans up the ToAs that could not be converted.

    The timestamps are assumed to reside in the first column of
    each DataFrame.

    Args:
        df_opr_zero_crossings (pd.DataFrame): A DataFrame with the 
            OPR zero-crossing times.
        df_probe_toas (pd.DataFrame): A DataFrame with the probe's 
            ToA values.

    Returns:
        pd.DataFrame: A DataFrame with the AoA values.
    """
    AoA_matrix = calculate_aoa(
        df_opr_zero_crossings.iloc[:, 0].to_numpy(),
        df_probe_toas.iloc[:, 0].to_numpy()
    )
    df_AoA = pd.DataFrame(
        AoA_matrix, 
        columns=[
            "n",
            "n_start_time",
            "n_end_time",
            "Omega",
            "ToA",
            "AoA"
        ]
    )
    df_AoA = df_AoA[df_AoA["n"] != -1]
    df_AoA.reset_index(inplace=True, drop=True)
    return df_AoA

##########################################################################
#                             MPR ENCODER                                #
##########################################################################
def calculate_aoa_from_mpr(
    arr_mpr_zero_crossing : np.ndarray,
    arr_probe_toas : np.ndarray,
    mpr_sections : int = 1,
) -> np.ndarray:
    """ This function calculates the angle of arrival of
    each ToA value relative to the section and revolution in
    which it occurs when using an MPR encoder.

    Args:
        arr_mpr_zero_crossing (np.ndarray): An array of MPR
            zero-crossing times.
        arr_probe_toas (np.ndarray): An array of ToA values.
        mpr_sections (int, optional): The number of sections
            in the MPR encoder. Defaults to 1, in this case,
            this function will be treated as an OPR encoder.

    Returns:
        np.ndarray: A matrix of AoA values. Each row in the
            matrix corresponds to a ToA value. The columns
            are:
            0: The revolution number
            1: The section number
            2: The zero crossing time at the start of the revolution
            3: The zero crossing time at the end of the revolution
            4: The angular velocity of the revolution
            5: The ToA
            6: The AoA of the ToA value
    """
    num_toas = len(arr_probe_toas)
    AoA_matrix = np.zeros((num_toas, 7))
    rad_per_section = 2 * np.pi / mpr_sections
    AoA_matrix[:, 0] = -1

    current_zero_crossing_start = arr_mpr_zero_crossing[0]
    current_zero_crossing_end = arr_mpr_zero_crossing[1]
    Omega = rad_per_section / (
        current_zero_crossing_end 
        - current_zero_crossing_start
    )
    current_n = 0
    current_revo = 0
    current_section = 0

    for i, toa in enumerate(arr_probe_toas):

        while toa > current_zero_crossing_end:
            current_n += 1
            if current_n >= (len(arr_mpr_zero_crossing) - 1):
                break
            current_zero_crossing_start = arr_mpr_zero_crossing[current_n]
            current_zero_crossing_end = arr_mpr_zero_crossing[current_n + 1]
            Omega = rad_per_section / (
                current_zero_crossing_end 
                - current_zero_crossing_start
            )
            current_section += 1
            if current_section == mpr_sections:
                current_section = 0
                current_revo += 1

        if current_n >= (len(arr_mpr_zero_crossing) - 1):
            break

        if toa > current_zero_crossing_start:
            AoA_matrix[i, 0] = current_revo
            AoA_matrix[i, 1] = current_section
            AoA_matrix[i, 2] = current_zero_crossing_start
            AoA_matrix[i, 3] = current_zero_crossing_end
            AoA_matrix[i, 4] = Omega
            AoA_matrix[i, 5] = toa
            AoA_matrix[i, 6] = Omega * (
                toa
                - current_zero_crossing_start
            ) + current_section * rad_per_section

    return AoA_matrix
    
def transform_ToAs_to_AoAs_mpr(
    df_mpr_zero_crossings : pd.DataFrame,
    df_probe_toas : pd.DataFrame,
    mpr_sections : int = 1,
) -> pd.DataFrame:
    """ This function transforms the ToA values to AoA values for a 
    single probe, given the MPR zero-crossing times and the proximity
    probe's ToA values.

    The timestamps are assumed to reside in the first column of
    each DataFrame.

    Args:
        df_opr_zero_crossings (pd.DataFrame): A DataFrame with the 
            OPR zero-crossing times.
        df_probe_toas (pd.DataFrame): A DataFrame with the probe's 
            ToA values.
        mpr_sections (int, optional): The number of sections
            in the MPR encoder. Defaults to 1, in this case,
            this function will be treated as an OPR encoder.

    Returns:
        pd.DataFrame: A DataFrame with the AoA values.
    """
    AoA_matrix = calculate_aoa_from_mpr(
        df_mpr_zero_crossings.iloc[:, 0].to_numpy(),
        df_probe_toas.iloc[:, 0].to_numpy(),
        mpr_sections
    )
    df_AoA = pd.DataFrame(
        AoA_matrix, 
        columns=[
            "n",
            "mpr_section",
            "section_start_time",
            "section_end_time",
            "Omega",
            "ToA",
            "AoA"
        ]
    )
    df_AoA = df_AoA[df_AoA["n"] != -1]
    df_AoA.reset_index(inplace=True, drop=True)
    return df_AoA