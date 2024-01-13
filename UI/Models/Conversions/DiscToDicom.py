import os
import numpy as np
from glob import glob

from UI.Models.Conversions.ABC.DicomConvertABC import Converter


class DiscToDicom(Converter):
    

    def Convert(self):
        """
        Convert the binary data stored in the disk image
        file to a DICOM for easier viewing and processing

        Requires: The disk image file have a .txt file 
                    with the header info (i.e. rows and
                    columns of the pixel array) in the 
                    same directory that the Disc image 
                    file is stored in.
        """

        try:
            self.FindHeaderInfo()

        except Exception as e:
            raise Exception(str(e))
        
        # Read in the header info
        with open(self.file_header, 'r') as fopen:
            
            lines = fopen.readlines()

        x_dim = list(filter(lambda s: "x_dim" in s, lines))

        y_dim = list(filter(lambda s: "y_dim" in s, lines))

        z_dim = list(filter(lambda s: "z_dim" in s, lines))

        if len(x_dim) != 1 or len(y_dim) != 1 or len(z_dim) != 1:
            raise Exception(f"Inappropriate header info, should contain one of each of the following: x_dim, y_dim and z_dim")

        if int(self._extract_value(z_dim[0])) != 1:
            raise Exception(f"Defines a 3D volume (z_dim > 1), converison is currently unsupported")

        x_dim, y_dim = int(self._extract_value(x_dim[0])), int(self._extract_value(y_dim[0]))

        # Open the binary file
        with open(self.filepath, 'rb') as fopen:

            # Read in to find the proper bit depth
            data_type = self.FigureOutDataType(self.filepath, x_dim * y_dim)

            file_data = np.fromfile(self.filepath, dtype=data_type, count=(x_dim * y_dim))
            
            file_data = file_data.reshape((x_dim, y_dim))
        
            file_data = np.rot90(file_data, k=-1)

        ## Pass to function to be normalized and stored
        self.WritePixelArray2Dicom(file_data)

            
    def _extract_value(self, s : str):
        """
        Extracts the numeric value from a text
        file token value pair seperated by '='
        sign

        Parameters
        ----------
        s : str
            Line from txt to be parsed

        Returns
        -------
        str
            The string after the equals sign
        """
        
        s = s.strip(' \n\t')

        s = s[s.find('=')::]
        
        return s.strip(' =;') # get rid of everything around the number


    def FindHeaderInfo(self):
        """
        Parses the directory for the txt header
        info
        """
        
        directory = os.path.dirname(self.filepath)

        header_file = glob(f'{directory}\\{self.filename}.txt')

        if header_file == []:
            raise FileNotFoundError(f"The header txt file could not be found along side the conversion file in directory {directory}")

        elif len(header_file) > 1:
            raise Exception(f'There is more than one header file along side the converison in directory {directory}')
        
        self.file_header =  header_file[0]

