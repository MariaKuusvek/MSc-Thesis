import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt5.QtCore import QTimer
import os
import tempfile
import xml.etree.ElementTree as ElementTree

class Commands:
    def __init__(self, fileName: str, text_edit: QPlainTextEdit) -> None:
        self.fileName = fileName 
        self.fileCommands = FileCommands()
        self.fileCommands.text_edit = text_edit
        self.mFileName: str = fileName or ''

class FileCommands:
    def __init__(self) -> None:
        self.leo_file_encoding = 'utf-8'
        self.mFileName = '' 
        self.mFileName = ""

    def writeOutline(self, fileName: str) -> bool:
        #c = self.c
        #errors = c.checkOutline()
        #if errors:
        #    g.error('Structure errors in outline! outline not written')
        #    return False
        # Other file types and readonly file logic removed
    
        return self.write_xml_file(fileName)

    def createBackupFile(self, fileName: str) -> str:
        """
            Create a closed backup file and copy the file to it,
            but only if the original file exists.
        """
        if fileName:
            fd, backupName = tempfile.mkstemp(text=False)
            f = open(fileName, 'rb')  # rb is essential.
            s = f.read()
            f.close()
            try:
                os.write(fd, s)
            finally:
                os.close(fd)
        return backupName
    
    def deleteBackupFile(self, fileName: str) -> None:
        os.remove(fileName)
    
    def outline_to_xml_string(self) -> str:
        """Write the outline in .leo (XML) format to a string."""
        return self.text_edit.toPlainText()

    def write_xml_file(self, fileName: str) -> bool:
        """Write the outline in .leo (XML) format."""
        #c = self.c
        backupName = self.createBackupFile(fileName)
        #if not ok:
        #    return False
        #try:
        f = open(fileName, 'wb')  # Must write bytes.
        self.mFileName = fileName
        #except Exception:
        #    g.es(f"can not open {fileName}")
        #    return False
        s = self.outline_to_xml_string()
        # Write bytes.
        f.write(bytes(s, self.leo_file_encoding, 'replace'))
        f.close()
        #c.setFileTimeStamp(fileName)
        if backupName:
            self.deleteBackupFile(backupName)
        return True
        
def onIdle(commands):
    """
    Save the outline to a .bak file every "interval" seconds if it has changed.
    Make *no* changes to the UI and do *not* update c.changed.
    """
    #global gDict
    #if g.app.killed or g.unitTesting:
    #    return
    #c = keywords.get('c')
    #d = gDict.get(c.hash())
    #if not d or not c or not c.exists or not c.changed or not c.mFileName:
    #    return
    # Time interval section has been edited out to ensure tests are happening at the same interval
    #save(c, d.get('verbose'))
    save(commands)

def save(c: Commands) -> None:
    """Save c's outlines to a .bak file without changing any part of the UI."""

    fc = c.fileCommands
    #old_log = g.app.log
    # Make sure nothing goes to the log.
    #try:
    #    # Disable the log so that g.es will append to g.app.logWaiting.
    #    g.app.log = None
    #    # The following methods call g.es.
    #    fc.writeAllAtFileNodes()  # Ignore any errors.
    fc.writeOutline(f"{c.mFileName}.bak")
    #    if verbose:
    #        print(f"Autosave: {time.ctime()} {c.shortFileName()}.bak")
    #finally:
    #    # Printing queued messages quickly becomes annoying.
    #    if 0:
    #        for msg in g.app.logWaiting:
    #            s, color, newline = msg[:3]  # May have 4 elements.
    #            print(s.rstrip())
    #    # Restore the log.
    #    g.app.logWaiting = []
    #    g.app.log = old_log


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

    commands = Commands("leo_autosave_1", text_edit)

    timer = QTimer()
    timer.setInterval(10000)
    timer.timeout.connect(lambda: onIdle(commands))
    timer.start()

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()