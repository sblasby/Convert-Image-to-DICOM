from scipy.io import loadmat
import datetime as dt
import re
import numpy as np

from DicomModules.DICOM_Objects.Base_Class.dicom_processing import DicomProcessing
from UI.Models.Conversions.ABC.DicomConvertABC import Converter

class MatToDicom(Converter):

    def Convert(self):
        # Load in the data
        mat_data = loadmat(self.filepath)

        variable = list(filter(lambda k: not "__" in k, mat_data.keys()))

        # Check if there is more than one variable stored within the variable.
        if len(variable) > 1:
            raise Exception(f'More than one variable stored within')

        pixel_data = mat_data[variable[0]]

        # Check that pixel_data is a numpy. ndarray
        if type(pixel_data) != np.ndarray:
            raise Exception(f'Does not contain a pixel array')

        pixel_data = pixel_data.copy(order='C')

        pixel_data = np.nan_to_num(pixel_data)

        self.WritePixelArray2Dicom(pixel_data)



