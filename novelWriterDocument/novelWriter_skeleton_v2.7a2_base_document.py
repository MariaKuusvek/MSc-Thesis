
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt5.QtCore import QTimer, QObject

class Config:
    def __init__(self) -> None:
        self.autoSaveDoc = 5     # Interval for auto-saving document, in seconds

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

        self._nwDocument.writeDocument(docText)

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