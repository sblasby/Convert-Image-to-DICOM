from UI.Models.Conversions.MatToDicom import MatToDicom
from UI.Models.Conversions.DiscToDicom import DiscToDicom

class ConversionModel:

    # Keys are the file extensions that are supported
    # Values are lambda functions that initailize the converters
    converterObjDict = \
        {
            ".mat" : lambda path, save, fname : MatToDicom(path, save, fname),
            ".img" : lambda path, save, fname : DiscToDicom(path, save, fname)
        }


    def PreformConversion(self, path, save, fname, filext):
        """
        Preform conversion of file. This is called before saving the file. 
        The converter is looked up in self.converterObjDict and the conversion 
        is called.
        
        Parameters
        ----------
        path : str
            Path to the file to be converted. 
        save : str
            Path for the file to be saved on
        fname : str
            Name of the file that is being converted.
        filext : str
            File extension of the file
        
        Returns
        -------
        """

        converter =  self.converterObjDict[filext](path, save, fname)

        converter.Convert()


    