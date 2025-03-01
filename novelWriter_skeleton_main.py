
import sys
import hashlib
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QTimer, pyqtSlot

class Config:
    def __init__(self) -> None:
        self.autoSaveDoc     = 30     # Interval for auto-saving document, in seconds

CONFIG = Config()

class NWProject:
    def __init__(self) -> None:
        self._valid    = True  # The project was successfully loaded

    @property
    def isValid(self) -> bool:
        """Return True if a project is loaded."""
        return self._valid
    
class SharedData:

    def __init__(self, project: NWProject):
        self.project = project

    @property
    def hasProject(self) -> bool:
        """Return True if the project instance is populated."""
        return self.project.isValid
    
SHARED = SharedData(NWProject(valid=True))

class NWItem:
    def __init__(self, project: NWProject, handle: str) -> None:
        self._handle   = handle

    @property
    def itemHandle(self) -> str:
        return self._handle

class NWStorage:
    def __init__(self, project: NWProject) -> None:
        self._project = project
        self._storagePath = None
        return

    @property
    def storagePath(self) -> Path | None:
        """Return the path where the project is stored."""
        return self._storagePath


class NWDocument:

    def __init__(self, project: NWProject, tHandle: str | None) -> None:
        self._project = project
        self._handle = "file"

    def writeDocument(self, text: str, forceWrite: bool = False) -> bool:
        """Write the document specified by the handle attribute. Handle
        any IO errors in the process  Returns True if successful, False
        if not.
        """

        if not isinstance(self._handle, str):
            return False

        contentPath = self._project.storage.contentPath
        if not isinstance(contentPath, Path):
            return False

        docFile = f"{self._handle}.nwd"

        docPath = contentPath / docFile
        docTemp = docPath.with_suffix(".tmp")

        try:
            with open(docTemp, mode="w", encoding="utf-8") as outFile:
                outFile.write(text)
        except Exception as exc:
            return False

        # If we're here, the file was successfully saved, so we can
        # replace the temp file with the actual file
        try:
            docTemp.replace(docPath)
        except OSError as exc:
            return False

        return True

class GuiDocEditor:

    def __init__(self,) -> None:
        self._docChanged = True  # Flag for changed status of document
        self.text = "Text to be saved"

    @property
    def docChanged(self) -> bool:
        """Return the changed status of the document."""
        return self._docChanged
    
    def getText(self) -> str:
        return self.text
    
    def saveText(self) -> bool:
        """Save the text currently in the editor to the NWDocument
        object, and update the NWItem meta data.
        """
        if self._nwItem is None or self._nwDocument is None:
            return False

        docText = self.getText()

        if not self._nwDocument.writeDocument(docText):
            saveOk = False
            if self._nwDocument.hashError:
                msgYes = SHARED.question(self.tr(
                    "This document has been changed outside of novelWriter "
                    "while it was open. Overwrite the file on disk?"
                ))
                if msgYes:
                    saveOk = self._nwDocument.writeDocument(docText, forceWrite=True)

            if not saveOk:
                SHARED.error(
                    self.tr("Could not save document."),
                    info=self._nwDocument.getError()
                )

            return False
        return True


class GuiMain:
    def __init__(self) -> None:
	  # Set Up Auto-Save Document Timer
        self.asDocTimer = QTimer(self)
        self.asDocTimer.timeout.connect(self._autoSaveDocument)
        self.initMain()
        self.asDocTimer.start()


    def initMain(self) -> None:
        """Initialise elements that depend on user settings."""
        self.asDocTimer.setInterval(int(CONFIG.autoSaveDoc*1000))
        return


    @pyqtSlot()
    def _autoSaveDocument(self) -> None:
        """Autosave of the document. This is a timer-activated slot."""
        if SHARED.hasProject and self.docEditor.docChanged:
            self.saveDocument()
        return

    def saveDocument(self, force: bool = False) -> None:
        """Save the current documents."""
        if SHARED.hasProject:
            if force or self.docEditor.docChanged:
                self.docEditor.saveText()
        return

# Create main function and skeleton application to carry out above

def main():
    pass
    # somekind of empty window (or maybe a window just displaying the saveable text)