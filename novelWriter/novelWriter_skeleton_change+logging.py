import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit, QPlainTextDocumentLayout
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from PyQt5.QtGui import QTextDocument
import logging
logger = logging.getLogger(__name__)

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
        self._handle = "novelWriter_autosave_1"

    def writeDocument(self, text: str, forceWrite: bool = False) -> bool:
        """Write the document specified by the handle attribute. Handle
        any IO errors in the process  Returns True if successful, False
        if not.
        """

        contentPath = self._project._storage.contentPath()

        docFile = f"{self._handle}.nwd"
        logger.debug("Saving document: %s", docFile)
        docPath = contentPath / docFile
        docTemp = docPath.with_suffix(".tmp")

        try:
            with open(docTemp, mode="w", encoding="utf-8") as outFile:
                outFile.write(text)
        except Exception as exc:
            return False

        try:
            docTemp.replace(docPath)
        except OSError as exc:
            return False

        return True

class GuiTextDocument(QTextDocument):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDocumentLayout(QPlainTextDocumentLayout(self))

class GuiDocEditor(QObject):

    editedStatusChanged = pyqtSignal(bool)

    def __init__(self, text_widget: QPlainTextEdit, nw_document: NWDocument) -> None:
        super().__init__()
        self._text_widget = text_widget
        self._nwDocument = nw_document
        self._docChanged = False
        self._qDocument = GuiTextDocument(self._text_widget)
        self._text_widget.setDocument(self._qDocument)
        self._qDocument.contentsChange.connect(self._docChange)
        
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

        self._nwDocument.writeDocument(docText)

        self.setDocumentChanged(False)
        #self.docTextChanged.emit(self._docHandle, self._lastEdit)
        return True
    
    @property
    def docChanged(self) -> bool:
        """Return the changed status of the document."""
        return self._docChanged
    
    def setDocumentChanged(self, state: bool) -> None:
        """Keep track of the document changed variable, and emit the
        document change signal.
        """
        if self._docChanged != state:
            self._docChanged = state
            self.editedStatusChanged.emit(self._docChanged)
        return

    def _docChange(self, pos: int, removed: int, added: int) -> None:
        """Triggered by QTextDocument->contentsChanged. This also
        triggers the syntax highlighter.
        """
        if not self._docChanged:
            self.setDocumentChanged(removed != 0 or added != 0)

        return

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
        print("checking for save")
        """Autosave of the document. This is a timer-activated slot."""
        if self.docEditor.docChanged:
            logger.debug("Auto-saving document")
            self.saveDocument()

    def saveDocument(self, force: bool = False) -> None:
        """Save the current documents."""
        if self.docEditor.docChanged:
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