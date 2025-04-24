import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt5.QtCore import QTimer
import os
import tempfile

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
        backupName = self.createBackupFile(fileName)
        f = open(fileName, 'wb')  # Must write bytes.
        self.mFileName = fileName
        s = self.outline_to_xml_string()
        # Write bytes.
        f.write(bytes(s, self.leo_file_encoding, 'replace'))
        f.close()
        if backupName:
            self.deleteBackupFile(backupName)
        return True
        
def onIdle(commands):
    """
    Save the outline to a .bak file every "interval" seconds if it has changed.
    Make *no* changes to the UI and do *not* update c.changed.
    """
    save(commands)

def save(c: Commands) -> None:
    """Save c's outlines to a .bak file without changing any part of the UI."""
    fc = c.fileCommands
    fc.writeOutline(f"{c.mFileName}.bak")


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