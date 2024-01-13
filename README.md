# Convert-Image-to-DICOM
UI built in python for the purpose of converting pixel arrays and image files into a DICOM format for viewing and editing in a DICOM software.

NOTE: The DICOM files that this code generates do not have proper UID tags. They are filled in as random numbers since these fields are required.
      The code could be edited to do this! Although currently the main purpose for the converter is to be able to open strange image files in a
      DICOM viewer/editor.

MODES IN THE UI:
The UI has 2 modes that can be selected, one mode allows the user to select the file(s) that they wish to convert and the location to save them.
The other mode prompts the user to select a directory and a save location. The selected directory will be crawled. An attempt at conversion will
happen for every file found within the directory and any sub directories. Furthermore, it will mimic the hierarchy of the folder selected to the save location.

The UI follows the MVVM OOP pattern and is designed with extensibility in mind. Adding new file types to be converted is straightforward.

To Add a New Model (or file conversion type):
•	Create a new Python file in the "Model" folder and define a class.
      -	In this class, you should implement the core functionality and processing required for the desired feature.
•	Note: If your goal is to add a new type of conversion and not a completely new model, you can do so without creating a brand-new model. Follow these steps instead:
      -	Create a new file within the "UI\Conversions" path.
      -	In this new file, create a class that inherits from the existing Converter class located in "UI\Conversions\ABC."
      -	Define a method named "Convert(self)" in your new class, which should contain the logic for generating a pixel array as a 2D numpy array.
      -	Use the "WritePixelArray2Dicom" method from the Converter class to write the pixel array to a DICOM file.
      -	In the Conversion Model file, add the file extension of the new conversion type to the "convertableFiles" class variable.
      -	Also, add the file extension and a lambda function that instantiates the object as a key-value pair in the "converterObjDict" dictionary, respectively.
