import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPlainTextEdit
from PyQt5.QtCore import QTimer

class Window():
    def __init__(self, parent=None):
        pass

    def set_timer(self, duration, callback):
        """
        Set a repeating timer to call "callback" every "duration" seconds.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(callback)
        self.timer.start(duration * 1000)


def write_and_flush(fileobj, content):
    """
    Write content to the fileobj then flush and fsync to ensure the data is,
    in fact, written.

    This is especially necessary for USB-attached devices
    """
    fileobj.write(content)
    fileobj.flush()
    #
    # Theoretically this shouldn't work; fsync takes a file descriptor,
    # not a file object. However, there's obviously some under-the-cover
    # mechanism which converts one to the other (at least on Windows)
    #
    os.fsync(fileobj)

def save_and_encode(text, filepath, newline=os.linesep):
    """
    Detect the presence of an encoding cookie and use that encoding; if
    none is present, do not add one and use the Mu default encoding.
    If the codec is invalid, log a warning and fall back to the default.
    """

    #match = ENCODING_COOKIE_RE.match(text)
    #if match:
    #    encoding = match.group(1)
    #    try:
    #        codecs.lookup(encoding)
    #    except LookupError:
    #        logger.warning("Invalid codec in encoding cookie: %s", encoding)
    #        encoding = ENCODING
    #else:
    #    encoding = ENCODING

    with open(filepath, "w", newline="") as f:
        text_to_write = (
            newline.join(line.rstrip(" ") for line in text.splitlines())
            + newline
        )
        write_and_flush(f, text_to_write)

class Editor():
    def __init__(self, view, _text_widget):
        self._view = view
        self._view.set_timer(10, self.autosave)
        self._text_widget = _text_widget

    def autosave(self):
        """
        Cycles through each tab and, if changed, saves it to the filesystem.
        """
        #if self._view.modified:
            # Something has changed, so save it!
        #    for tab in self._view.widgets:
        #        if tab.path and tab.isModified():
        self.save_tab_to_file(self._text_widget, show_error_messages=False)
        #            logger.info(
        #                "Autosave detected and saved "
        #                "changes in {}.".format(tab.path)
        #            )


    def save_tab_to_file(self, tab, show_error_messages=True):
        """
        Given a tab, will attempt to save the script in the tab to the path
        associated with the tab. If there's a problem this will be logged and
        reported and the tab status will continue to show as Modified.
        """
        #logger.info("Saving script to: {}".format(tab.path))
        #logger.debug(tab.text())
        #try:
        save_and_encode(tab.toPlainText(), Path(os.curdir).resolve()  / "mu_autosave_1.py")

        #except OSError as e:
        #    logger.error(e)
        #    error_message = _("Could not save file (disk problem)")
        #    information = _(
        #        "Error saving file to disk. Ensure you have "
        #        "permission to write the file and "
        #        "sufficient disk space."
        #    )
        #except UnicodeEncodeError:
        #    error_message = _("Could not save file (encoding problem)")
        #    logger.exception(error_message)
        #    information = _(
        #        "Unable to convert all the characters. If you "
        #        "have an encoding line at the top of the file, "
        #        "remove it and try again."
        #    )
        #else:
        #    error_message = information = None
        #if error_message and show_error_messages:
        #    self._view.show_message(error_message, information)
        #else:
        #    tab.setModified(False)
        #    self.show_status_message(_("Saved file: {}").format(tab.path))


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

    newWindow = Window()
    editor = Editor(newWindow, text_edit)

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()