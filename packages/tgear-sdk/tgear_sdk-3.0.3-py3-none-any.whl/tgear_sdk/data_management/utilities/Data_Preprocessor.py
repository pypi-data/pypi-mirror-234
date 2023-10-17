import numpy as np
from scipy import signal, interpolate


class Data_Preprocessor:
    # Do NOT CHANGE
    DATA_MAT_COL = 7
    F_SAMP = 50
    NEW_DATA_INT_SEC = 1 / F_SAMP

    # GENERAL PARAMS
    DATA_DIM = 100  # DIM OF THE DATA MATRIX

    # FILT PARAMS [ORDER, LP_CUTOFF]
    FILT_ACC = [5, 4]
    FILT_VEL = [5, 5]
    FILT_VELTOT = [1, 1.3]

    # SEGMENTATION PARAMS
    MAX_TH = 0.4  # VELTOT Maximum TH
    MAX_TIME_TH = 1  # minimum time between maximum
    LEFT_MAX_WIN = 50  # LEFT MAX WINDOW
    RIGHT_MAX_WIN = 5  # RIGHT MAX WINDOW
    MIN_TH = 3  # VELTOT Minimum TH
    LFT_MIN_WIN = 0  # LEFT MIN WINDOW (starting from INDEX = 0)

    # DISPLACEMENT PARAMS
    DISP_DELAY = 8

    def __init__(self):
        self.data_counter = 0
        self.last_max_time = 0

        #### FILTER SETUP ######
        F_NYQ = Data_Preprocessor.F_SAMP / 2

        # ACC FILTER
        self.b_acc, self.a_acc = signal.butter(
            Data_Preprocessor.FILT_ACC[0],
            Data_Preprocessor.FILT_ACC[1] / F_NYQ,
            "lowpass",
        )

        # VEL FILTER
        self.b_vel, self.a_vel = signal.butter(
            Data_Preprocessor.FILT_VEL[0],
            Data_Preprocessor.FILT_VEL[1] / F_NYQ,
            "lowpass",
        )

        # VEL TOT FILTER
        self.b_veltot, self.a_veltot = signal.butter(
            Data_Preprocessor.FILT_VELTOT[0],
            Data_Preprocessor.FILT_VELTOT[1] / F_NYQ,
            "lowpass",
        )
        #### FILTER SETUP ######

        #### DATA STRUCT #####
        self.data_m = np.zeros(
            shape=(Data_Preprocessor.DATA_DIM, Data_Preprocessor.DATA_MAT_COL),
            dtype=float,
        )
        self.acc_filt_m = np.zeros(shape=(Data_Preprocessor.DATA_DIM, 3), dtype=float)
        self.vel_filt_m = np.zeros(shape=(Data_Preprocessor.DATA_DIM, 3), dtype=float)
        self.veltot_filt_a = np.zeros(Data_Preprocessor.DATA_DIM, dtype=float)
        self.time_a = np.zeros(Data_Preprocessor.DATA_DIM, dtype=float)
        #### DATA STRUCT #####
        self.left = 0
        self.right = 98

    def push_data(self, data):
        """push new data into data matrix, push new data from the bottom"""

        self.data_counter = self.data_counter + 1
        data = np.append(data, self.data_counter * Data_Preprocessor.NEW_DATA_INT_SEC)
        self.data_m[:-1] = self.data_m[1:]
        self.data_m[-1] = data

    def data_filter(self):

        # ACC Filtering
        self.acc_filt_m = signal.lfilter(
            self.b_acc, self.a_acc, self.data_m[:, 0:3], axis=0
        )

        # VEL Filtering
        self.vel_filt_m = signal.lfilter(
            self.b_vel, self.a_vel, self.data_m[:, 3:6], axis=0
        )

        # VEL TOT Filtering
        veltot = np.sqrt(np.power(self.data_m[:, 3:6], 2).sum(axis=1)) # type: ignore
        self.veltot_filt_a = signal.lfilter(self.b_veltot, self.a_veltot, veltot)

        # TIME array
        self.time_a = self.data_m[:, 6]

    def data_segmentation(self):
        """segment veltot"""

        MAX_SEG_WINDOW = [
            Data_Preprocessor.DATA_DIM - Data_Preprocessor.LEFT_MAX_WIN,
            Data_Preprocessor.DATA_DIM - Data_Preprocessor.RIGHT_MAX_WIN,
        ]

        # search for a MAX into the MAX SEG WINDOW
        max = np.amax(self.veltot_filt_a[MAX_SEG_WINDOW[0] : MAX_SEG_WINDOW[1]])
        max_ind = (
            np.where(self.veltot_filt_a[MAX_SEG_WINDOW[0] : MAX_SEG_WINDOW[1]] == max)[
                0
            ][0]
            + MAX_SEG_WINDOW[0]
        )
        max_time = self.time_a[max_ind]
        if not (
            (max > Data_Preprocessor.MAX_TH)
            and ((max_time - self.last_max_time) > Data_Preprocessor.MAX_TIME_TH)
        ):
            return False

        # search for right MIN
        for i in range(max_ind, Data_Preprocessor.DATA_DIM):
            if self.veltot_filt_a[i] < (max / Data_Preprocessor.MIN_TH):
                right_min_time = self.time_a[i]
                right_min_ind = i
                break
        else:
            return False

        # search for left MIN
        for i in range(max_ind, Data_Preprocessor.LFT_MIN_WIN, -1):
            if self.veltot_filt_a[i] < (max / Data_Preprocessor.MIN_TH):
                left_min_time = self.time_a[i]
                left_min_ind = i
                break
        else:
            return False

        # register min limits and max last time
        self.last_max_time = max_time
        self.min_time_a = [left_min_time, right_min_time]
        self.min_index_a = [left_min_ind, right_min_ind]

        self.seg_time_a = self.time_a[left_min_ind : (right_min_ind + 1)].transpose()
        self.seg_acc_m = self.acc_filt_m[left_min_ind : (right_min_ind + 1), :] # type: ignore
        self.seg_vel_m = self.vel_filt_m[left_min_ind : (right_min_ind + 1), :] # type: ignore
        self.left = left_min_ind
        self.right = right_min_ind

        return True

    def data_interpolation(self):
        """data interpolation"""

        INT_SAM = 50

        temp_norm = np.linspace(self.min_time_a[0], self.min_time_a[1], INT_SAM)

        f_int_acc = interpolate.interp1d(self.seg_time_a, self.seg_acc_m, axis=0)
        self.acc_int = f_int_acc(temp_norm)

        f_int_vel = interpolate.interp1d(self.seg_time_a, self.seg_vel_m, axis=0)
        self.vel_int = f_int_vel(temp_norm)

        acc_int_x = self.acc_int[:, 0].transpose()
        acc_int_y = self.acc_int[:, 1].transpose()
        acc_int_z = self.acc_int[:, 2].transpose()
        vel_int_x = self.vel_int[:, 0].transpose()
        vel_int_y = self.vel_int[:, 1].transpose()
        vel_int_z = self.vel_int[:, 2].transpose()

        return np.concatenate(
            ([1.0], acc_int_x, acc_int_y, acc_int_z, vel_int_x, vel_int_y, vel_int_z)
        )

    def run(self):
        """run neural netwrok"""

        # Filtering (ACC, VEL, VEL TOT)
        self.data_filter()

        # Segmentation
        result = self.data_segmentation()

        # ACC and VEl time interpolation
        if result:
            data_set = self.data_interpolation()
            return data_set
        else:
            return False
