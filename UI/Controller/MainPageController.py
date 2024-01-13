import os
import datetime as dt
from customtkinter import filedialog
from glob import glob


from UI.Controller.ControllerABC.ControllerABC import ControllerABC

class MainPageController(ControllerABC):


    @property
    def PreviousSavePath(self):
        if hasattr(self, '_previous_save_path'):
            return self._previous_save_path
        
        else:
            return None

    @property
    def PreviousSelectionPath(self):
        
        if hasattr(self, '_previous_selection_path'):
            return self._previous_selection_path
        
        else:
            return None

    def SaveAsDicoms(self):

        #open the pop up window
        self.Root.ShowAsTopLevel("TopLevelConversionProgress")

        topLevel = self.Root.OpenedTopLevels["TopLevelConversionProgress"]

        self.topWindow = topLevel.Window

        self.topView = topLevel.View

        self.topWindow.grab_set()

        self.mode()

        self.topWindow.grab_release()

        self.Root.CloseTopLevel("TopLevelConversionProgress")

        self.ChangeBtnState("ConvertBtn", 'disabled')

        self.ChangeBtnState("SaveLocationBtn", 'disabled')

        self.saveLocation = ''


    def SaveLocation(self):

        location = filedialog.askdirectory(initialdir=self.PreviousSavePath)

        # if location == "":
        #     self.ChangeBtnState("ConvertBtn", 'disabled')

        if location != "":
            self.saveLocation = location
            self._previous_save_path = location
            self.ChangeBtnState("ConvertBtn", 'normal')


    def ModeSwitch(self, value):

        self.ChangeBtnState("SelctFileBtn", 'normal')

        self.ChangeBtnState("SaveLocationBtn", 'disabled')

        if value == "File Mode":
            self.View.SelctFileBtn.configure(text = 'Select File(s)')
            self.View.SelctFileBtn.configure(command = self._set_files)
            self.mode = self._file_mode

        elif value == "Directory Mode":
            self.View.SelctFileBtn.configure(text = 'Select Directory')
            self.View.SelctFileBtn.configure(command = self._set_dir)
            self.mode = self._dir_mode

        

    ## Private Functions 
    ##------------------

    def _bind(self) -> None:
        
        self.View.ConvertBtn.configure(command = self.SaveAsDicoms)
        self.View.SaveLocationBtn.configure(command = self.SaveLocation)
        self.View.ModeSwitchBtns.configure(command = self.ModeSwitch)

    def _set_files(self):
        
        files = filedialog.askopenfiles(filetypes=[("Convertable Files", '*' + ';*'.join(self.Model.converterObjDict.keys()))], initialdir=self.PreviousSelectionPath)
        
        # if files == "":
        #     self.ChangeBtnState("SaveLocationBtn", 'disabled')
        
        if files != "":
            self.to_convert = files
            self._previous_selection_path = os.path.dirname(files[0].name)
            self.ChangeBtnState("SaveLocationBtn", 'normal')


    def _set_dir(self):
        
        directory = filedialog.askdirectory(initialdir=self.PreviousSelectionPath)
        
        # if directory == "":
        #     self.ChangeBtnState("SaveLocationBtn", 'disabled')
        
        if directory != "":
            self.to_convert = directory
            self._previous_selection_path = directory
            self.ChangeBtnState("SaveLocationBtn", 'normal')

    def _dir_mode(self):

        base_save_dir = self.saveLocation

        base_dir = self.to_convert

        results = os.walk(base_dir)

        for dir_path, _, _ in results:
            
            files2convert = []

            for extension in self.Model.converterObjDict.keys():

                    files2add = glob(f'{dir_path}\*{str(extension)}')

                    files2convert.extend(files2add)
            
            save_dir = base_save_dir + '\\' + dir_path.lstrip(base_dir)

            if files2convert != []:

                base = save_dir

                count = 1

                while os.path.isdir(save_dir):
                    
                    save_dir = base + f' Copy{count}'

                os.makedirs(save_dir)

                self.topView.progress_msg.configure(text = f'Converting files on path {dir_path}')

                progressStep = 100 / len(files2convert)

                currentProgress = 0

                self.topView.progress.configure(determinate_speed = progressStep)

                self.CreateLogFile(save_dir)


            for file in files2convert:
                
                self._convert(file, save_dir)

                currentProgress += progressStep

                self.topView.progress.set(currentProgress / 100)

                self.topWindow.update()


    def _file_mode(self):

        fileList = list(map(lambda f: f.name, self.to_convert))

        progressStep = 100 / len(fileList)

        currentProgress = 0

        self.topView.progress.configure(determinate_speed = progressStep)

        saveDir = self.saveLocation

        self.CreateLogFile(saveDir)

        for file2convert in fileList:
            
            self._convert(file2convert, saveDir)

            currentProgress += progressStep

            self.topView.progress.set(currentProgress / 100)

            self.topWindow.update()
        

    def _convert(self, file2convert, saveDir):

        base = os.path.basename(file2convert)

        fileName, suffix = os.path.splitext(base)

        savePath = saveDir + os.sep + str(fileName) + '.dcm'

        try:
            self.Model.PreformConversion(file2convert, savePath, fileName, suffix)

        except Exception as e:

            self.WriteLog(f'Skipped "{fileName}": {str(e)}')

            # If the dicom was saved before the exception then delete the file
            if os.path.isfile(savePath):

                os.remove(savePath)