import customtkinter as cTK
from customtkinter import filedialog

from UI.View.ViewABC.ViewABC import ViewABC

class MainPage(ViewABC):

    def _place_widgets(self):
        
        self.columnconfigure([0,1,2], weight=1, pad=75, uniform="fred")

        Header = cTK.CTkLabel(self, text="Convert To DICOM")
        Header._font["size"] = 25
        Header.grid(row = 0, column = 0, columnspan = 3, pady = 50,)

        self.ModeSwitchBtns = cTK.CTkSegmentedButton(self, values=["File Mode", "Directory Mode"])
        self.ModeSwitchBtns.grid(row = 1, column = 1, pady = 40)

        self.SelctFileBtn = cTK.CTkButton(self, text="Select Files", state='disabled')
        self.SelctFileBtn.grid(row = 2, column = 1, pady = 40)

        self.SaveLocationBtn = cTK.CTkButton(self, text = "Save Location",state='disabled')
        self.SaveLocationBtn.grid(row= 3, column = 1, pady = 40)

        self.ConvertBtn = cTK.CTkButton(self, text="Convert", state='disabled')
        self.ConvertBtn.grid(row = 4, column = 1,  pady = 40)

        

        



    


