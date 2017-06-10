import numpy as np
from scipy import interpolate
from netCDF4 import Dataset

xs = np.linspace(, ,)
ys = np.linspace(, ,)

x_axis, y_axis = np.meshgrid(xs, ys)
f = interpolate.interp2d(x_axis, y_axis,)


class InterpolationArea:
    # wanted area
    # (135.4, 34.8), (135.4, 35.0), (135.4, 35.2), (135.4, 35.4)
    # (135.6, 34.8), (135.6, 35.0), (135.6, 35.2), (135.6, 35.4)
    # (135.8, 34.8), (135.8, 35.0), (135.8, 35.2), (135.8, 35.4)
    # (136.0, 34.8), (136.0, 35.0), (136.0, 35.2), (136.0, 35.4)

    def __init__(self, src_area_info, target_area_info, ncfile_list):
        self.srcObject = src_area_info
        self.targetObject = target_area_info
        self.ncFilelist = ncfile_list

    def interpolateArea(self):
        xs_o = np.linspace(0, self.srcObject[0] - 1, self.srcObject[0])
        ys_o = np.linspace(0, self.srcObject[1] - 1, self.srcObject[1])
        x_axis, y_axis = no.meshgrid(xs_o, ys_o)
        values = np.array(self.srcObject[2])
        func = interpolate.interp2d(x_axis, y_axis, values, kind='cubic')
        xs_t = np.linspace()
