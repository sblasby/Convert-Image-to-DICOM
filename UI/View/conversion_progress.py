import customtkinter as cTK


from UI.View.ViewABC.ViewABC import ViewABC

class ConversionProgress(ViewABC):

    def _place_widgets(self):

        self.progress_msg = cTK.CTkLabel(self, text="Conversion in Progress, Do Not Close Window")
        self.progress_msg.pack(pady=10)

        self.progress = cTK.CTkProgressBar(self, mode='determinate')
        self.progress.pack(pady=10)
        self.progress.set(0)