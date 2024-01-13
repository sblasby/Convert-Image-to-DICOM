import customtkinter as cTK
from abc import abstractmethod, ABCMeta


class ViewABC(cTK.CTkFrame, metaclass= ABCMeta):

    def __init__(self, master):

        super().__init__(master, fg_color=master._fg_color)

        self.parent_widget = master

        self._place_widgets()
    
    @abstractmethod
    def _place_widgets(self):
        pass
