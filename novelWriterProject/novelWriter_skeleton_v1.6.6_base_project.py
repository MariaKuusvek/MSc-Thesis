
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt5.QtCore import QTimer, QObject
from lxml import etree
from pathlib import Path

class Config:
    def __init__(self) -> None:
        self.autoSaveProj = 5

CONFIG = Config()
    
class NWProject:
    def __init__(self) -> None:
        self._text = ""
        self.projPath = Path(os.curdir).resolve()
        self.projFile = "novelWriter_autosave_project_2"


    def saveProject(self, autoSave=False):
        """Save the project main XML file. The saving command itself
        uses a temporary filename, and the file is replaced afterwards
        to make sure if the save fails, we're not left with a truncated
        file.
        """

        xRoot = etree.Element("rootElement")
        xRoot.text = self._text

        # Root element and project details
        nwXML = etree.ElementTree(xRoot)

        # Write the xml tree to file
        tempFile = os.path.join(self.projPath, self.projFile+"~")
        saveFile = os.path.join(self.projPath, self.projFile)
        backFile = os.path.join(self.projPath, self.projFile[:-3]+"bak")
        with open(tempFile, mode="wb") as outFile:
            outFile.write(etree.tostring(
                nwXML,
                encoding="utf-8",
                xml_declaration=True
            ))

        # If we're here, the file was successfully saved,
        # so let's sort out the temps and backups
        if os.path.isfile(saveFile):
            os.replace(saveFile, backFile)
        os.replace(tempFile, saveFile)
        return True

class SharedData():

    def __init__(self) -> None:
        self._project = NWProject()

    def saveProject(self, autoSave: bool = False) -> bool:
        """Save the current project."""
        return self.project.saveProject(autoSave=autoSave)
    
    @property
    def project(self) -> NWProject:
        """Return the active NWProject instance."""
        return self._project

SHARED = SharedData()

class GuiMain():
    def __init__(self, editor) -> None:
        self.textEditor = editor

        self.mainConf = CONFIG
        self.theProject  = NWProject()

        # Set Up Auto-Save Project Timer
        self.asProjTimer = QTimer()
        self.asProjTimer.timeout.connect(self._autoSaveProject)
        self.initMain()
        self.asProjTimer.start()
    

    def initMain(self) -> None:
        """Initialise elements that depend on user settings."""
        self.asProjTimer.setInterval(int(self.mainConf.autoSaveProj*1000))
        return
    
    def _autoSaveProject(self) -> None:
        """Autosave of the project. This is a timer-activated slot."""
        self.theProject._text = self.textEditor.toPlainText()
    
        self.saveProject(autoSave=True)

        return

    def saveProject(self, autoSave: bool = False) -> bool:
        self.theProject.saveProject(autoSave=autoSave)

        return True
    
def main():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Simple PyQt Text Input")

    layout = QVBoxLayout(window)

    label = QLabel("Simple text input:")
    layout.addWidget(label)
    text_edit = QPlainTextEdit()
    layout.addWidget(text_edit)
    window.resize(400, 300)
    window.show()

    gui = GuiMain(text_edit)

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()