
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt5.QtCore import QTimer

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

        #self._docError = ""
        #if not isinstance(self._handle, str):
        #    logger.error("No document handle set")
        #    return False

        contentPath = self._project._storage.contentPath()

        #if not isinstance(contentPath, Path):
        #    logger.error("No content path set")
        #    return False

        docFile = f"{self._handle}.nwd"
        #logger.debug("Saving document: %s", docFile)

        docPath = contentPath / docFile
        docTemp = docPath.with_suffix(".tmp")

        #prevHash = self._lastHash
        #self.readDocument()
        #if prevHash and self._lastHash != prevHash and not forceWrite:
        #    logger.error("File has been altered on disk since opened")
        #    self._hashError = True
        #    return False

        #currTime = formatTimeStamp(time())
        #writeHash = hashlib.sha1(text.encode()).hexdigest()
        #createdDate = self._docMeta.get("created", "Unknown")
        #updatedDate = self._docMeta.get("updated", "Unknown")
        #if writeHash != self._lastHash:
        #    updatedDate = currTime
        #if not docPath.is_file():
        #    createdDate = currTime
        #    updatedDate = currTime

        ## DocMeta Line
        #docMeta = ""
        #if self._item:
        #    docMeta = (
        #        f"%%~name: {self._item.itemName}\n"
        #        f"%%~path: {self._item.itemParent}/{self._item.itemHandle}\n"
        #        f"%%~kind: {self._item.itemClass.name}/{self._item.itemLayout.name}\n"
        #        f"%%~hash: {writeHash}\n"
        #        f"%%~date: {createdDate}/{updatedDate}\n"
        #    )

        try:
            with open(docTemp, mode="w", encoding="utf-8") as outFile:
                #outFile.write(docMeta)
                outFile.write(text)
        except Exception as exc:
            #self._docError = formatException(exc)
            return False

        # If we're here, the file was successfully saved, so we can
        # replace the temp file with the actual file
        try:
            docTemp.replace(docPath)
        except OSError as exc:
            #self._docError = formatException(exc)
            return False
        
        #self._lastHash = writeHash
        #self._hashError = False

        return True


class GuiDocEditor():

    def __init__(self, text_widget: QPlainTextEdit, nw_document: NWDocument) -> None:
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

        #if self._nwItem is None or self._nwDocument is None:
        #    logger.error("Cannot save text as no document is open")
        #    return False

        #tHandle = self._nwItem.itemHandle
        #if self._docHandle != tHandle:
        #    logger.error(
        #        "Editor handle '%s' and item handle '%s' do not match", self._docHandle, tHandle
        #    )
        #    return False

        docText = self.getText()

        #cC, wC, pC = standardCounter(docText)
        #self._updateDocCounts(cC, wC, pC)

        #if not >
        self._nwDocument.writeDocument(docText)

        #    saveOk = False
        #    if self._nwDocument.hashError:
        #        msgYes = SHARED.question(self.tr(
        #            "This document has been changed outside of novelWriter "
        #            "while it was open. Overwrite the file on disk?"
        #        ))
        #        if msgYes:
        #            saveOk = self._nwDocument.writeDocument(docText, forceWrite=True)

        #    if not saveOk:
        #        SHARED.error(
        #            self.tr("Could not save document."),
        #            info=self._nwDocument.getError()
        #        )
        #    return False


        #self.setDocumentChanged(False)
        #self.docTextChanged.emit(self._docHandle, self._lastEdit)

        #oldHeader = self._nwItem.mainHeading
        #oldCount = SHARED.project.index.getHandleHeaderCount(tHandle)
        #SHARED.project.index.scanText(tHandle, docText)
        #newHeader = self._nwItem.mainHeading
        #newCount = SHARED.project.index.getHandleHeaderCount(tHandle)

        #if self._nwItem.itemClass == nwItemClass.NOVEL:
        #    if oldCount == newCount:
        #        self.novelItemMetaChanged.emit(tHandle)
        #    else:
        #        self.novelStructureChanged.emit()

        #if oldHeader != newHeader:
        #    self.docFooter.updateInfo()

        ## Update the status bar
        #self.updateStatusMessage.emit(self.tr("Saved Document: {0}").format(self._nwItem.itemName))

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
        # if SHARED.hasProject and self.docEditor.docChanged:
        # logger.debug("Auto-saving document")
        self.saveDocument()

    def saveDocument(self, force: bool = False) -> None:
        """Save the current documents."""
        #if SHARED.hasProject:
        #    self.docEditor.saveCursorPosition()
        #    if force or self.docEditor.docChanged:
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