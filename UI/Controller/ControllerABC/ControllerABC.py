from abc import abstractmethod, ABCMeta
import os


class ControllerABC(metaclass= ABCMeta):

    Root = None # Set in the main file (UI.py), allows for the controller to be able to switch windows, etc

    def __init__(self, view, model):
        """
        Initalize a controller object

        Args:
            view: A subclass of ViewABC that contains the
                    widgets that are to me displayed
            model: A class that defines the "main work" 
                    that is to be done 
        """

        self.View = view

        self.Model = model

        self._bind()

    @abstractmethod
    def _bind(self) -> None:
        """
        Where the binding of events will be placed.
        If there are no bindings required for view
        then def this method but have the body be
        the keyword "pass".

        exmaple: if we want button binded
            self.View.(name of button).configure(command = (method you want to run))
        """
        pass

    def ChangeBtnState(self, btn_str, new_state):

        btn = getattr(self.View, btn_str)

        btn.configure(state = new_state)


    def CreateLogFile(self, dirForFile):
        
        self.logPath = dirForFile + os.sep + 'logs.txt'

        # Attempt to create the file, continue if it already exists
        try:
            fopen = open(self.logPath, 'x')

            fopen.close()

        except FileExistsError:
            pass


    def WriteLog(self, msg):
        
        with open(self.logPath, 'a') as fopen:
            fopen.write(msg + '\n')
        