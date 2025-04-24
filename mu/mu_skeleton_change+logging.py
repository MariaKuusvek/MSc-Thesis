# Test this
import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt5.QtCore import QTimer
import logging
logger = logging.getLogger(__name__)
from logging.handlers import TimedRotatingFileHandler
LOG_DIR = Path(os.curdir).resolve() 
LOG_FILE = os.path.join(LOG_DIR, "mu.log")
ENCODING = "utf-8"

class Window():
    def __init__(self, widget):
        self._widget = widget

    def set_timer(self, duration, callback):
        """
        Set a repeating timer to call "callback" every "duration" seconds.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(callback)
        self.timer.start(duration * 1000)

    @property
    def widgets(self):
        """
        Returns a list of references to the widgets representing tabs in the
        editor.
        """
        return [self._widget]

    @property
    def modified(self):
        """
        Returns a boolean indication if there are any modified tabs in the
        editor.
        """
        for widget in self.widgets:
            if widget.document().isModified():
                return True
        return False


def write_and_flush(fileobj, content):
    """
    Write content to the fileobj then flush and fsync to ensure the data is,
    in fact, written.

    This is especially necessary for USB-attached devices
    """
    fileobj.write(content)
    fileobj.flush()
    os.fsync(fileobj)

def save_and_encode(text, filepath, newline=os.linesep):
    """
    Detect the presence of an encoding cookie and use that encoding; if
    none is present, do not add one and use the Mu default encoding.
    If the codec is invalid, log a warning and fall back to the default.
    """

    with open(filepath, "w", newline="") as f:
        text_to_write = (
            newline.join(line.rstrip(" ") for line in text.splitlines())
            + newline
        )
        write_and_flush(f, text_to_write)

def setup_logging():
    """
    Configure logging.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    # set logging format
    log_fmt = (
        "%(asctime)s - %(name)s:%(lineno)d(%(funcName)s) "
        "%(levelname)s: %(message)s"
    )
    formatter = logging.Formatter(log_fmt)

    # define log handlers such as for rotating log files
    handler = TimedRotatingFileHandler(
        LOG_FILE, when="midnight", backupCount=5, delay=0, encoding=ENCODING
    )
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    # set up primary log
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)


class Editor():
    def __init__(self, view, _text_widget):
        self._view = view
        self._view.set_timer(10, self.autosave)
        self._text_widget = _text_widget

    def autosave(self):
        """
        Cycles through each tab and, if changed, saves it to the filesystem.
        """
        if self._view.modified:
            self.save_tab_to_file(self._text_widget, show_error_messages=False)
            logger.info(
                "Autosave detected and saved "
                "changes in {}.".format("mu_autosave_1.py")
            )


    def save_tab_to_file(self, tab, show_error_messages=True):
        """
        Given a tab, will attempt to save the script in the tab to the path
        associated with the tab. If there's a problem this will be logged and
        reported and the tab status will continue to show as Modified.
        """
        logger.info("Saving script to: {}".format("mu_autosave_1.py"))
        logger.debug(tab.toPlainText())
        save_and_encode(tab.toPlainText(), Path(os.curdir).resolve()  / "mu_autosave_1.py")
        tab.document().setModified(False)

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

    setup_logging()
    newWindow = Window(text_edit)
    editor = Editor(newWindow, text_edit)

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()