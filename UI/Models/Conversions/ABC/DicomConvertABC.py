from abc import ABC, abstractmethod
import random
import datetime as dt
import re
import numpy as np

from DicomModules.DICOM_Objects.Base_Class.dicom_processing import DicomProcessing

class Converter(ABC):

    def __init__(self, filepath, savepath, fname):
        """
        Provides useful variables for the DICOM construction
         
         Parameters
         ----------
         filepath : str
         	Path to the file where the file to be converted is stored
         savepath : str
         	Path that resulting file is to be saved to
         fname : __type__
         	Name of the file that is to be converted (without extension)
         
        """
        
        self.filepath = filepath

        self.savepath = savepath

        self.filename = fname

        ## Dicom Parameters
        secondaryImage = "1.2.840.10008.5.1.4.1.1.7"

        uid_base = '1.3.6.1.4.1.9590.100.1.2.'

        mediaStorageSOPInstance = secondaryImage + '.' + str(random.randint(10000000, 99999999))

        self.fileMetaData = {
            "MediaStorageSOPClassUID": secondaryImage,
            "MediaStorageSOPInstanceUID": mediaStorageSOPInstance, 
            "TransferSyntaxUID": "1.2.840.10008.1.2", 
        }

        self.dataDict = {
                        "PatientName" : '',
                        "PatientID" : '',
                        "PatientBirthDate" : '',
                        "PatientSex" : '',

                        "StudyDate" : '',
                        "StudyTime" : '',
                        "AccessionNumber" : '',
                        "ReferringPhysicianName" : '',
                        "StudyInstanceUID" : uid_base + str(random.randint(int(1E9), int(1E12)-1)),
                        "StudyID" : '',

                        "Modality":"OT",
                        "SeriesInstanceUID" : uid_base + str(random.randint(int(1E9), int(1E12)-1)),
                        "SeriesNumber" : '',

                        "ConversionType" : "WSD",

                        "InstanceNumber" : '',

                        "SOPClassUID" : secondaryImage,
                        "SOPInstanceUID" : uid_base + str(random.randint(int(1E9), int(1E12)-1)),

                        "ContentDate" : dt.datetime.now().strftime('%Y%m%d'),
                        }

    @abstractmethod
    def Convert(self):
        """
        Converts the data. Subclasses should override this method to do the conversion. 
        If this method returns None the conversion is aborted
        """
        pass

    
    def WritePixelArray2Dicom(self, pixel_array, already_image_data = False, bit_depth = 16):

        """
        Accepts a 2D NumPy array and writes it to a DICOM file. 
        If 'already_image_data' is set to False, the pixel array 
        will be linearly scaled such that the minimum value in the 
        array becomes zero, and the maximum value becomes the maximum 
        allowed value for the 'pixel_array.dtype'.

        Parameters:
        ----------
        pixel_array : numpy.ndarray
            A 2D NumPy array representing image pixel data.

        already_image_data : bool, optional
            If True, the provided array is assumed to be properly scaled pixel data. Argument bit_depth is ignored
            If False, the array will be linearly scaled. Argument bit_depth is used to scale the array

        already_image_data : int, optional
            Specifies how many bits to use per pixel

        Raises:
        ------
        Exception
            - If the provided 'array' is not considered a valid pixel array.
            - If the DICOM file cannot be created.
        """

        ## Normalize the pixel data
        maximum, minimum = np.max(pixel_array), np.min(pixel_array)

        # data_type = pixel_array.dtype

        # If it is not an image already then normalize it
        if not already_image_data:

            value_range = maximum - minimum

            pixel_array = ((pixel_array - minimum) / value_range) * (2 ** bit_depth - 1)

            pixel_array = pixel_array.astype(eval(f"np.uint{bit_depth}"))

        shape = pixel_array.shape

        rows, cols = shape[0], shape[1]

        # Check that the dimension of the array is 2D arrays.
        if pixel_array.ndim != 2:
            raise Exception(f'The dimension of the array is {len(shape)}, only 2D arrays are supported')

        elif rows == 1:
            raise Exception(f'Only 1 row, likely not a pixel array')

        # bit_depth = int(re.search(r'\d+$', str(pixel_array.dtype)).group())

        smallest = np.min(pixel_array)
        
        largest = np.max(pixel_array)

        pixel_array = pixel_array.tobytes()

        bits_stored = bit_depth

        data_dict = {
                    "SamplesPerPixel" : 1,
                    "PhotometricInterpretation" : 'MONOCHROME2',
                    "Rows": rows,
                    "Columns":cols,
                    "BitsAllocated" : bit_depth,
                    "BitsStored":bits_stored,
                    "HighBit" : bits_stored - 1,
                    "PixelRepresentation" : 0,
                    "SmallestImagePixelValue" : int(smallest).to_bytes(bit_depth // 8, 'big'),
                    "LargestImagePixelValue" : int(largest).to_bytes(bit_depth // 8, 'big'),
                    "PixelData" : pixel_array,                         
                    }

        self.dataDict |= data_dict

        try:

            DicomProcessing.CreateNewDicom(self.savepath, self.fileMetaData, self.dataDict)
        
        except Exception as e:

            raise Exception(f'Skipped "{self.filename}": Error in creating dicom - {str(e)}')
    

    def FigureOutDataType(self, filepath, expected_size):
        """
        Attempts to figure out the data type of the
        binary file on filepath

        Parameters
        ----------
        filepath : str
            Path to the binary file containing image binary data.
        expected_size : int
            Expected number of pixels in the image.

        Returns
        -------
        numpy.dtype
            A NumPy data type (e.g., numpy.uint8, numpy.uint16, etc.) 
            representing the determined data type based on the array size.
        """

        array = np.fromfile(filepath, count=expected_size)
        
        bit_depth = int(array.nbytes / expected_size * 8)

        bit_depth = max(8, min(64, bit_depth))

        return eval(f"np.uint{bit_depth}")


             