
# Currently unfinished implementation
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt5.QtCore import QTimer, QObject
import hashlib

class Config:
    def __init__(self) -> None:
        self.autoSaveDoc = 10     # Interval for auto-saving document, in seconds

CONFIG = Config()

class NWProject:
    def __init__(self) -> None:
        pass

class NWStorage:
    def __init__(self, project: NWProject) -> None:
        self._project = project
        self._runtimePath = Path(os.curdir).resolve()

    def contentPath(self) -> Path | None:
        """Return the path used for project content. The folder must
        already exist, otherwise this property is None.
        """
        return self._runtimePath

class NWProject:
    def __init__(self) -> None:
        self._storage = NWStorage(self)

class NWDocument:
    def __init__(self, project: NWProject, tHandle: str | None) -> None:
        self._project = project
        self._handle = "novelWriter_autosave_hash"
        self._lastHash = None
        self._hashError = False

    def readDocument(self, isOrphan: bool = False) -> str | None:
        """Read the document specified by the handle set in the
        constructor, capturing potential file system errors and parse
        meta data. If the document doesn't exist on disk, return an
        empty string. If something went wrong, return None.
        """

        contentPath = self._project.storage.contentPath
        docFile = f"{self._handle}.nwd"
        docPath = contentPath / docFile
        self._fileLoc = docPath

        text = ""
        self._docMeta = {}
        self._lastHash = ""

        with open(docPath, mode="r", encoding="utf-8") as inFile:
            # Check the first <= 10 lines for metadata
            for _ in range(10):
                line = inFile.readline()
                if line.startswith(r"%%~"):
                    self._parseMeta(line)
                else:
                    text = line
                    break
            # Load the rest of the file
            text += inFile.read()


        self._lastHash = hashlib.sha1(text.encode()).hexdigest()

        return text

    def writeDocument(self, text: str, forceWrite: bool = False) -> bool:
        """Write the document specified by the handle attribute. Handle
        any IO errors in the process  Returns True if successful, False
        if not.
        """

        contentPath = self._project._storage.contentPath()
        docFile = f"{self._handle}.nwd"
        docPath = contentPath / docFile
        docTemp = docPath.with_suffix(".tmp")

        prevHash = self._lastHash
        self.readDocument()
        if prevHash and self._lastHash != prevHash and not forceWrite:
            self._hashError = True
            return False

        writeHash = hashlib.sha1(text.encode()).hexdigest()
        #createdDate = self._docMeta.get("created", "Unknown")
        #updatedDate = self._docMeta.get("updated", "Unknown")
        #if writeHash != self._lastHash:
        #    updatedDate = currTime
        #if not docPath.is_file():
        #    createdDate = currTime
        #    updatedDate = currTime

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
        
        self._lastHash = writeHash
        self._hashError = False

        return True


class GuiDocEditor(QObject):

    def __init__(self, text_widget: QPlainTextEdit, nw_document: NWDocument) -> None:
        super().__init__()
        self._text_widget = text_widget
        self._nwDocument = nw_document

    def getText(self) -> str:
        """
        Get text from the QPlainTextEdit.
        """
        return self._text_widget.toPlainText()
    
    def saveText(self) -> bool:
        """Save the text currently in the editor to the NWDocument
        object, and update the NWItem meta data.
        """
        docText = self.getText()

        #if not >
        self._nwDocument.writeDocument(docText)

        if self._nwDocument.hashError:
            msgYes = SHARED.question(self.tr(
                "This document has been changed outside of novelWriter "
                "while it was open. Overwrite the file on disk?"
            ))
            if msgYes:
                saveOk = self._nwDocument.writeDocument(docText, forceWrite=True)


        return True

class GuiMain:
    
    def __init__(self, editor: GuiDocEditor) -> None:
        self.docEditor = editor

        # Set Up Auto-Save Document Timer
        self.asDocTimer = QTimer()
        self.asDocTimer.timeout.connect(self._autoSaveDocument)
        self.initMain()
        self.asDocTimer.start()

    def initMain(self) -> None:
        """Initialise elements that depend on user settings."""
        self.asDocTimer.setInterval(int(CONFIG.autoSaveDoc*1000))
        return
    
    def _autoSaveDocument(self) -> None:
        """Autosave of the document. This is a timer-activated slot."""
        self.saveDocument()

    def saveDocument(self, force: bool = False) -> None:
        """Save the current documents."""
        self.docEditor.saveText()
    
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

    project = NWProject()
    nw_document = NWDocument(project, "MyHandle")
    editor = GuiDocEditor(text_edit, nw_document)
    guiMain = GuiMain(editor)

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()