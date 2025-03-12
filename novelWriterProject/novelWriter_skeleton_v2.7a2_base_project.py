
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt5.QtCore import QTimer, QObject
import xml.etree.ElementTree as ET
from pathlib import Path
from time import time

class Config:
    def __init__(self) -> None:
        self.autoSaveProj = 5

CONFIG = Config()

class ProjectXMLWriter:
    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)


    def write(self) -> bool:
        """Write the project data and content to the XML files."""

        xRoot = ET.Element("rootElement")
        xRoot.text = self._project._text

        # Write the XML tree to file
        tmp = self._path.with_suffix(".tmp")
        xml = ET.ElementTree(xRoot)
        xml.write(tmp, encoding="utf-8", xml_declaration=True)
        tmp.replace(self._path)

        return True

class NWStorage:
    def __init__(self, project: "NWProject") -> None:
        self._project = project
        self._runtimePath = Path(os.curdir).resolve()

    def getXmlWriter(self) -> ProjectXMLWriter | None:
        """Return a properly configured ProjectXMLWriter instance."""
        writer = ProjectXMLWriter(self._runtimePath / "novelWriter_autosave_project_1.xml")
        writer._project = self._project 
        return writer
    
class NWProject:
    def __init__(self) -> None:
        self._storage = NWStorage(self)  
        self._text = ""

    def saveProject(self, autoSave: bool = False) -> bool:
        """Save the project main XML file. The saving command itself
        uses a temporary filename, and the file is replaced afterwards
        to make sure if the save fails, we're not left with a truncated
        file.
        """

        xmlWriter = self._storage.getXmlWriter()

        xmlWriter.write()

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

        # Set Up Auto-Save Project Timer
        self.asProjTimer = QTimer()
        self.asProjTimer.timeout.connect(self._autoSaveProject)
        self.initMain()
        self.asProjTimer.start()

    def initMain(self) -> None:
        """Initialise elements that depend on user settings."""
        self.asProjTimer.setInterval(int(CONFIG.autoSaveProj*1000))
        return
    
    def _autoSaveProject(self) -> None:
        """Autosave of the project. This is a timer-activated slot."""
        SHARED.project._text = self.textEditor.toPlainText()
        self.saveProject(autoSave=True)

    def saveProject(self, autoSave: bool = False) -> bool:
        return SHARED.saveProject(autoSave=autoSave)
    
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