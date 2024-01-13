import customtkinter as cTK
from collections import namedtuple

## View Imports
from UI.View.mainpage import MainPage
from UI.View.conversion_progress import ConversionProgress

## Controller Imports
from UI.Controller.ControllerABC.ControllerABC import ControllerABC
from UI.Controller.MainPageController import MainPageController

## Model Imports
from UI.Models.ConversionModel import ConversionModel



class UI(cTK.CTk):

    MVC = namedtuple("MVC", ["View", "Controller", "Model"], defaults=[None, None, None])
    
    # Where the different views are to be stored
    Views = \
    {
        "MainPage" : MVC(MainPage, MainPageController, ConversionModel),
        "TopLevelConversionProgress" : MVC(ConversionProgress) #Leaving the other 2 blank will make the TopLevel be controlled by the current controller and model                                                  
    }


    def __init__(self):
        
        super().__init__()

        cTK.set_appearance_mode("dark")

        self._setGeo()

        self.title("Convert2DICOM")

        try:
            self.iconbitmap("Python Code\Comp_Brain.ico")
        except:
            pass

        self.OpenedTopLevels = {}

        ControllerABC.Root = self # Allow controllers to call methods from this class

        self.SwitchView("MainPage")


    def _setGeo(self):

        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()

        gui_width = width // 2
        gui_height = height // 2

        self.geometry(f'{gui_width}x{gui_height}')

        self.CenterWindow(self)

        


    def CenterWindow(self, window2center):
        
        w, h  = window2center._current_width, window2center._current_height

        x_pos = (window2center.winfo_screenwidth() - w) // 2
        y_pos = (window2center.winfo_screenheight() - h) // 2

        window2center.geometry(f'+{x_pos}+{y_pos}')

        return x_pos, y_pos

    

    def SwitchView(self, new_view_name : str):
        """
        _summary_

        Parameters
        ----------
        new_view_name : str
            Name of the view that is being switched to
            (must be a valid key in the Views dictionary)
        """
        if hasattr(self, 'CurrView'):
            self.CurrView.destroy()

        # Instantiate the new view
        self.CurrView = self.Views[new_view_name].View(self)
        self.CurrView.pack(fill="both")
        self.CenterWindow(self)

        self.CurrViewName = new_view_name

        # Instantiate the new model
        self.Model = self.Views[new_view_name].Model()

        # Instatiate the controller
        self.Controller = self.Views[new_view_name].Controller(self.CurrView, self.Model)


    def ShowAsTopLevel(self, view_to_show : str):

        TopLevel = namedtuple("TopLevel", ["Window", "View", "Controller", "Model"])
        
        TopLevelWindow = cTK.CTkToplevel(master = self)

        TopLevelView = self.Views[view_to_show].View(TopLevelWindow)

        TopLevelView.pack()

        self.CenterWindow(TopLevelWindow)

        TopLevelModel = self.Views[view_to_show].Model

        TopLevelController = self.Views[view_to_show].Controller

        if TopLevelModel != None:
            TopLevelModel = TopLevelModel()
        
        else:
            TopLevelModel = self.Model

        if TopLevelController != None:
            TopLevelController = TopLevelController(TopLevelView, TopLevelModel)
        
        else:
            TopLevelController = self.Controller

        self.OpenedTopLevels[view_to_show] = TopLevel(TopLevelWindow, TopLevelView, TopLevelController, TopLevelModel)


    def CloseTopLevel(self, toplevel_name : str):
        """
        To be called to close the top level. If extra
        closing functionality is desired, then create
        a method in the respective controller for the
        desired closing functionality and call this at
        the end.

        Args:
            toplevel_name (str): key to the toplevel info
                                    stored in self.OpenedTopLevels
        """

        self.OpenedTopLevels[toplevel_name].Window.destroy()

        self.OpenedTopLevels.pop(toplevel_name)

UI().mainloop()