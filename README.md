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

