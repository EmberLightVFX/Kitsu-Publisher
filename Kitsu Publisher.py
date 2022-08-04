import sys
import os
import urllib.parse
import platform
import cv2
import gazu
from xml.etree import ElementTree

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from ui import Ui_MainWindow

version = "0.1"


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    '''
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int, object)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @Slot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()  # Done


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.connectEvents()
        self.threadpool = QThreadPool()
        # Set thread count to 1 so only one shot is synced
        self.threadpool.setMaxThreadCount(1)

        self.cb_subfolders.setEnabled(True)
        self.rb_doXML.setEnabled(False)
        self.rb_doFolder.setChecked(True)

        self.l_info.setText("")
        self.l_gazuversion.setText(gazu.__version__)
        self.l_appversion.setText(version)
        self.gazuToken = None
        self.isTransfering = False
        self.cancelTransfer = False
        self.numberOfShots = 0
        appIcon = QIcon("kitsu.png")
        self.setWindowIcon(appIcon)
        self.show()

    def __keyPressEvent(self, event):
        if event.matches(QKeySequence.Delete):
            self.__removeServer()
        else:
            QTableWidget.keyPressEvent(self.setup.serverTable, event)

    def __removeServer(self):
        self.tv_information.removeRow(
            self.tv_information.currentRow()
        )

    def connectEvents(self):
        self.pb_login.clicked.connect(
            lambda: self.login(refresh=True)
        )
        self.rb_doXML.toggled.connect(
            lambda: self.radioSwitch(self.rb_doXML)
        )
        self.rb_doFolder.toggled.connect(
            lambda: self.radioSwitch(self.rb_doFolder)
        )
        self.pb_pick.clicked.connect(self.pick)
        self.pb_fetch.clicked.connect(self.fetch)
        self.pb_publish.clicked.connect(self.publish)
        self.tv_information.keyPressEvent = self.__keyPressEvent

    def login(self, refresh=False):
        self.pb_login.setText("...Logging in...")
        worker = Worker(self.login_kitsu, refresh)
        worker.signals.result.connect(self.login_result)

        # Execute
        self.threadpool.start(worker)

    def login_result(self, success):
        self.pb_login.setText("Log in")
        if success is True:
            self.l_info.setText("Logged in")
        elif success is False:
            return  # Already logged in
        else:
            self.l_info.setText("Failed to login")
            printMessage(success)
        self.cb_project.setCurrentIndex(0)
        self.cb_task.setCurrentIndex(0)
        self.cb_status.setCurrentIndex(0)

    def login_kitsu(self, refresh, progress_callback):
        self.l_info.setText("Logging in")
        # Connect to server
        if self.gazuToken is None or refresh is True:
            try:
                host = self.le_kitsuURL.text()
                host = removeLastSlash(host)
                host = host + "/api"
                gazu.set_host(host)
                if not gazu.client.host_is_up():
                    raise ConnectionError(
                        "Could not connect to the server. Is the host URL correct?"
                    )
            except Exception as exc:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(exc).__name__, exc.args)
                return message

            # Login
            try:
                self.gazuToken = gazu.log_in(self.le_username.text(),
                                             self.le_password.text())

            except Exception as exc:
                message = (
                    "Login verification failed. "
                    "Please ensure your username and "
                    "password for Kitsu are correct. "
                )
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(exc).__name__, message)
                return message

            # Logged in. Let's fetch the projects!
            try:
                self.cb_project.setEnabled(True)
                self.l_project.setEnabled(True)
                self.cb_project.clear()
                projects = gazu.project.all_projects()
                for index, project in enumerate(projects):
                    self.cb_project.insertItem(
                        index,
                        project["name"],
                        userData=project
                    )
            except Exception as exc:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(exc).__name__, exc.args)
                return message

            # and let's fetch the shot task types
            try:
                self.cb_task.setEnabled(True)
                self.l_task.setEnabled(True)
                self.cb_task.clear()
                task_types = gazu.task.all_task_types()
                for index, task_type in enumerate(task_types):
                    if task_type["for_shots"] is True:
                        self.cb_task.insertItem(
                            index,
                            task_type["name"],
                            userData=task_type
                        )
            except Exception as exc:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(exc).__name__, exc.args)
                return message

            # and let's fetch the statuses
            try:
                self.cb_status.setEnabled(True)
                self.l_status.setEnabled(True)
                self.cb_status.clear()
                all_task_statuses = gazu.task.all_task_statuses()
                for index, all_task_status in enumerate(all_task_statuses):
                    self.cb_status.insertItem(
                        index,
                        all_task_status["name"],
                        userData=all_task_status
                    )
            except Exception as exc:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(exc).__name__, exc.args)
                return message

            return True
        return False

    def radioSwitch(self, switch):
        if switch == self.rb_doXML:
            self.cb_subfolders.setEnabled(False)
        else:
            self.cb_subfolders.setEnabled(True)
        self.le_infopath.setText("")

    def pick(self):
        if self.rb_doXML.isChecked() is True:  # If pick XML file
            fname = QFileDialog.getOpenFileName(self,
                                                'Pick XML File',
                                                self.le_infopath.text(),
                                                filter="XML files (*.xml)")
            fname = fname[0]
        else:  # If pick folder
            fname = QFileDialog.getExistingDirectory(self,
                                                     'Select a folder',
                                                     self.le_infopath.text(),
                                                     options=QFileDialog.ShowDirsOnly)
        if fname != "":
            self.le_infopath.setText(os.path.abspath(fname))

    def fetch(self):
        self.pb_fetch.setText("...Fetching...")
        self.login()

        worker = Worker(self.fetch_data)
        worker.signals.result.connect(self.fetch_result)

        # Execute
        self.threadpool.start(worker)

    def fetch_result(self, nr_shots):
        self.pb_fetch.setText("Fetch")
        if not isinstance(nr_shots, (int, float, complex)):
            self.l_info.setText(
                "Some error happend. Could not fetch information")
            printMessage(nr_shots)  # An error happened. Print it
        else:
            self.l_info.setText("Fetched " + str(nr_shots) + " shots")

    def fetch_data(self, progress_callback):
        self.l_info.setText("Fetching information")
        try:
            shots = gazu.shot.all_shots_for_project(
                self.cb_project.currentData())
            path = os.path.abspath(self.le_infopath.text())
            files = []
            if self.rb_doXML.isChecked() is True:  # If pick XML file
                printMessage("XML isn't supported yet.")
            else:
                if os.path.exists(path) is False:
                    printMessage(
                        title="Error",
                        msg="Path does not seem to exists.\nPlease check!"
                    )
                    return 0

                self.tv_information.setRowCount(0)
                acceptedExtensions = [
                    ".mov", ".mp4", ".jpg", ".png", ".tiff"]

                if self.cb_subfolders.isChecked() is True:
                    subfolders, files = run_fast_scandir(
                        path, acceptedExtensions)
                else:
                    for entry in os.scandir(path):
                        if entry.is_file():
                            files.append(entry.path)

                # To speed up the preview-check,
                # save old sequence if same mutlieple times
                old_sequence_name = None
                old_sequence_dict = None
                for file in files:
                    extension = os.path.splitext(file)[1]
                    if extension in acceptedExtensions:
                        namesplit = os.path.splitext(
                            os.path.basename(file)
                        )[0].split("_")

                        exists = "No"
                        if old_sequence_name != namesplit[0]:
                            sequence_dict = gazu.shot.get_sequence_by_name(self.cb_project.currentData(),
                                                                           namesplit[0])
                            old_sequence_name = namesplit[0]
                            old_sequence_dict = sequence_dict
                        else:
                            sequence_dict = old_sequence_dict
                        if sequence_dict is not None:
                            shot_dict = gazu.shot.get_shot_by_name(
                                sequence_dict, namesplit[1])

                            if shot_dict is not None:
                                exists = "Yes"

                        sequence = QTableWidgetItem(namesplit[0])
                        shot = QTableWidgetItem(namesplit[1])
                        vidReader = cv2.VideoCapture(file)
                        if not vidReader.isOpened():
                            printMessage(
                                "Could not read video file")
                        framerange = QTableWidgetItem(
                            str(int(vidReader.get(cv2.CAP_PROP_FRAME_COUNT))))
                        preview = QTableWidgetItem(file)
                        filesize = QTableWidgetItem(
                            pretty_size(os.stat(file).st_size)
                        )

                        row = self.tv_information.rowCount()
                        self.tv_information.setRowCount(row + 1)

                        self.tv_information.setItem(
                            row, 0, QTableWidgetItem("Ready"))
                        self.tv_information.setItem(
                            row, 1, QTableWidgetItem(exists))
                        self.tv_information.setItem(row, 2, sequence)
                        self.tv_information.setItem(row, 3, shot)
                        self.tv_information.setItem(row, 4, framerange)
                        self.tv_information.setItem(row, 5, preview)
                        self.tv_information.setItem(row, 6, filesize)
                        self.tv_information.item(row, 6).setTextAlignment(2)

            self.tv_information.resizeColumnsToContents()
            return len(files)
        except Exception as exc:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exc).__name__, exc.args)
            return message

    def publish(self):
        if self.isTransfering is False:
            try:
                self.login()

                self.progressBar.setValue(0)
                rows = self.tv_information.rowCount()

                self.numberOfShots = rows
                for i in range(rows):
                    # Pass the function to execute
                    # Any other args, kwargs are passed to the run function
                    worker = Worker(self.uploadToKitsu, i)
                    worker.signals.progress.connect(self.upload_progress)
                    worker.signals.result.connect(self.thread_result)
                    worker.signals.finished.connect(self.thread_complete)

                    # Execute
                    self.threadpool.start(worker)

            except Exception as exc:
                printMessage("Error", exc)
        else:
            self.pb_publish.setText("...Canceling at next upload...")
            self.cancelTransfer = True

    def upload_progress(self, calltype, data):
        if calltype == 0:  # Write upload filesize
            self.l_info.setText(
                "Uploading... This can take a while. Current file: "
                + str(data.text())
            )
        elif calltype == 1:  # Process done. Update progressbar
            self.progressBar.setValue(
                int(((data + 1) / self.numberOfShots) * 100))

    def thread_result(self, msg):
        if msg is not None:
            # Error
            self.l_info.setText("Failed to upload to Kitsu")
            printMessage(msg)

    def thread_complete(self):
        self.l_info.setText("Done uploading")
        self.pb_publish.setText("Publish")
        self.isTransfering = False
        pass

    def uploadToKitsu(self, i, progress_callback):
        if self.cancelTransfer is True:
            return

        self.isTransfering = True
        self.pb_publish.setText("Cancel")
        try:
            status = self.tv_information.item(i, 0)
            # exists = self.tv_information.item(i, 1)
            sequence = self.tv_information.item(i, 2)
            shot = self.tv_information.item(i, 3)
            framerange = self.tv_information.item(i, 4)
            preview = self.tv_information.item(i, 5)

            # Update some info
            status.setText("Uploading")
            progress_callback.emit(0, self.tv_information.item(i, 6))

            # Fix Sequence
            sequence_dict = gazu.shot.get_sequence_by_name(self.cb_project.currentData(),
                                                           sequence.text())
            if sequence_dict is None:
                sequence_dict = gazu.shot.new_sequence(self.cb_project.currentData(),
                                                       sequence.text())

            # Fix Shot
            already_uploaded = True
            shot_dict = gazu.shot.get_shot_by_name(
                sequence_dict, shot.text())
            if shot_dict is None:
                shot_dict = gazu.shot.new_shot(self.cb_project.currentData(),
                                               sequence_dict,
                                               shot.text(),
                                               nb_frames=framerange.text())
                already_uploaded = False
            # Add preview
            if already_uploaded is False or self.cb_reupload.isChecked() is True:
                task_dict = gazu.task.get_task_by_name(
                    shot_dict, self.cb_task.currentData())
                if task_dict is None:
                    task_dict = gazu.task.new_task(
                        shot_dict, self.cb_task.currentData()
                    )
                previews = gazu.files.get_all_preview_files_for_task(
                    task_dict)
                person = gazu.person.get_person_by_email(
                    self.le_username.text())
                comment_dict = gazu.task.add_comment(
                    task_dict,
                    self.cb_status.currentData(),
                    "",
                    person
                )
                preview_dict = gazu.task.add_preview(
                    task_dict,
                    comment_dict,
                    preview.text()
                )
                gazu.task.set_main_preview(preview_dict)
            status.setText("Done")
            progress_callback.emit(1, i)
        except Exception as exc:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exc).__name__, exc.args)
            return message

    def closeEvent(self, event):
        if self.isTransfering is True:
            msg = QMessageBox(
                QMessageBox.Question,
                "Kitsu Publishing",
                "Are you sure you want to cancel the transfer?"
            )
            msg.addButton("Yes", QMessageBox.YesRole)
            msg.addButton("No", QMessageBox.NoRole)
            action = msg.exec_()

            if action == 0:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def printMessage(msg, title=""):
    if title == "":
        title = "Kitsu Publisher"
    else:
        title = "Kitsu Publisher - " + title
    QMessageBox.warning(QWidget(), title, str(msg))


def pretty_size(bytes):
    """Get human-readable file sizes.
    simplified version of https://pypi.python.org/pypi/hurry.filesize/
    """
    units = [
        (1 << 50, ' PB'),
        (1 << 40, ' TB'),
        (1 << 30, ' GB'),
        (1 << 20, ' MB'),
        (1 << 10, ' KB'),
        (1, (' byte', ' bytes')),
    ]
    for factor, suffix in units:
        if bytes >= factor:
            break
    amount = round(bytes / factor, 2)

    if isinstance(suffix, tuple):
        singular, multiple = suffix
        if amount == 1:
            suffix = singular
        else:
            suffix = multiple
    return str(amount) + suffix


def run_fast_scandir(dir, ext):    # dir: str, ext: list
    subfolders, files = [], []

    for f in os.scandir(dir):
        if f.is_dir():
            subfolders.append(f.path)
        if f.is_file():
            if os.path.splitext(f.name)[1].lower() in ext:
                files.append(f.path)

    for dir in list(subfolders):
        sf, f = run_fast_scandir(dir, ext)
        subfolders.extend(sf)
        files.extend(f)
    return subfolders, files


def removeLastSlash(adress):
    if adress[-1:] == "/":
        adress = adress[:-1]

    return adress


if (__name__ == '__main__'):
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
