import sys
import os
import urllib.parse
import platform
import cv2
import gazu
import configparser
import re
import subprocess
from xml.etree import ElementTree
from cryptography.fernet import Fernet
from datetime import datetime

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
        self.general_path()
        # The initial job queue status of the host is true
        self.RQ = 1
        self.threadpool = QThreadPool()
        self.max_threads_count = os.cpu_count() - 1
        self.max_threads_value.setText(str(self.max_threads_count))
        # Set thread count to 1 so only one shot is synced
        self.threadpool.setMaxThreadCount(1)
        self.le_threads.setText("1")
        self.le_threads.setValidator(QIntValidator(1, self.max_threads_count, self))
        self.completed_tasks = 0
        self.total_tasks = 0
        self.l_ep.setVisible(True)
        self.le_ep.setVisible(True)
        self.le_delimiter.setText("_")
        self.le_ep.setText("1")
        self.le_sq.setText("2")
        self.le_sh.setText("3")
        self.le_ta.setText("4")
        self.tv_information.setColumnHidden(2, False)
        self.nb_frame = 0
        self.newTaskItem_index = 0
        self.pb_refresh.clicked.connect(lambda: self.refresh_project_list())
        self.pb_tips.clicked.connect(lambda: self.open_file("Tips for rule definition.txt", path_chosen=0))
        self.pb_logs.clicked.connect(lambda: self.open_file("Publish_log.txt", path_chosen=1))
        self.cb_project.currentIndexChanged.connect(self.on_project_changed)
        self.le_threads.textChanged.connect(self.update_thread_count)
        
        if not os.path.exists(self.key_file_path):
            self.generate_key()

        # Auto login
        self.load_config()

        self.cb_subfolders.setEnabled(True)
        self.rb_doXML.setEnabled(False)
        self.rb_doFolder.setChecked(True)
        self.cb_reupload.setChecked(True)

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

    def update_thread_count(self):
        user_input = self.le_threads.text()
        thread_count = 1
        if user_input:
            thread_count = int(user_input)
            if thread_count <= 0:
                thread_count = 1
            elif thread_count > self.max_threads_count:
                thread_count = self.max_threads_count
        else:
            thread_count = 1
        self.threadpool.setMaxThreadCount(thread_count)
        self.le_threads.setText(str(thread_count))

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
            self.save_config()
        elif success is False:
            return  # Already logged in
        else:
            self.l_info.setText("Failed to login")
            printMessage(success)
        self.cb_project.setCurrentIndex(0)
        self.cb_task.setEnabled(False)
        self.cb_task.setCurrentIndex(self.newTaskItem_index)
        self.cb_status.setCurrentIndex(0)

        if self.RQ == 0:
            self.le_threads.setText("1")
            self.le_threads.setEnabled(False)
            self.l_max_threads.setText("# Enabling job queue is needed | <span style='font-size: 8.8pt;'>需要启用 job queue</ span>")
            self.max_threads_value.setVisible(False)
        else:
            self.le_threads.setEnabled(True)
            self.l_max_threads.setText("# Max input value | <span style='font-size: 8.8pt;'>最大允许输入</ span>")
            self.max_threads_value.setVisible(True)

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

            # Logged in. Let's fetch the job-queue-up status first!
            host_status = gazu.client.get("status")
            if host_status["job-queue-up"] is False:
                self.RQ = 0
            else:
                self.RQ = 1
                
            # Logged in. Let's fetch the projects!
            self.refresh_project_list()

            # and let's fetch the shot task types
            try:
                self.cb_task.setEnabled(True)
                self.l_task.setEnabled(True)
                self.cb_task.clear()
                task_types = gazu.task.all_task_types()
                for index, task_type in enumerate(task_types):
                    if task_type["for_entity"] == "Shot":   # Fixed to align with API changes.
                        self.cb_task.insertItem(
                            index,
                            task_type["name"],
                            userData=task_type
                        )
                self.cb_task.insertItem(
                    0,
                    "Don't post | 不上传",
                    self.cb_task.itemData(1)
                )
                self.newTaskItem_index = self.cb_task.count()
                self.cb_task.insertItem(
                    self.newTaskItem_index,
                    "There's no preview with a null task name | 没有空任务字段的预览",
                    self.cb_task.itemData(1)
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

    def refresh_project_list(self):
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
            self.l_info.setText("Project list refreshed | 项目列表已更新")
        except Exception as exc:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exc).__name__, exc.args)
            return message
            
    def on_project_changed(self):
        current_project_name = self.cb_project.currentText()

        if current_project_name:
            current_project_dict = gazu.project.get_project_by_name(current_project_name)
            if current_project_dict["production_type"] != "tvshow":
                self.l_ep.setVisible(False)
                self.le_ep.setText("1")
                self.le_ep.setVisible(False)
                self.tv_information.setColumnHidden(2, True)
                self.has_episode = 0
            else:
                self.l_ep.setVisible(True)
                self.le_ep.setVisible(True)
                self.tv_information.setColumnHidden(2, False)
                self.has_episode = 1

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

    def parse_rule_indices(self, input_str):
        try:
            return [int(i) - 1 for i in input_str.split('+') if i]

        except ValueError:
            return [0]

    def process_rule_part(self, rule_input, namesplit):
        parts = rule_input.split(",")
        base_rule = parts[0].strip()
        adv_rules = parts[1:]

        parts = []
        for idx in [int(i) - 1 for i in base_rule.split('+')]:
            if 0 <= idx < len(namesplit):
                parts.append(namesplit[idx])
            else:
                parts.append("❗out of range")
        result = "_".join(parts)

        for adv_rule in adv_rules:
            adv_rule = adv_rule.strip()
            if adv_rule.startswith('+'):
                result += adv_rule[1:]
            elif adv_rule.endswith('+'):
                result = adv_rule[:-1] + result
            elif adv_rule.startswith('-'):
                remove_str = adv_rule[1:]
                if remove_str:
                    result = re.sub(r'{}$'.format(re.escape(remove_str)), "", result)
            elif adv_rule.endswith('-'):
                remove_str = adv_rule[:-1]
                if remove_str:
                    if result.startswith(remove_str):
                        result = result[len(remove_str):]
            elif ":" in adv_rule:
                find, replace = adv_rule.split(":")
                result = result.replace(find, replace)

        return result

    def process_rule(self, rule_input, namesplit, indices):
        if "," not in rule_input:
            rule_input = rule_input + ", : "
            
        if "&" in rule_input:
            rule_parts = rule_input.split("&")
            results = []
            
            for part in rule_parts:
                result = self.process_rule_part(part.strip(), namesplit)
                results.append(result)

            return "_".join(results)
    
        else:
            return self.process_rule_part(rule_input, namesplit)

    def fetch(self):
        self.pb_fetch.setText("...Fetching...")
        self.progressBar.setValue(0)
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
        self.delimiter_input = self.le_delimiter.text() or "_"
        self.ep_input = self.le_ep.text() or "1"
        self.sq_input = self.le_sq.text() or "2"
        self.sh_input = self.le_sh.text() or "3"
        self.ta_input = self.le_ta.text() or "4"
        self.clear_log()
        self.task_rule_list = []
        self.task_type_dict_list = []
        all_task_type_names = []
        shot_dict = {}
        
        ep_indices = self.parse_rule_indices(self.ep_input)
        sq_indices = self.parse_rule_indices(self.sq_input)
        sh_indices = self.parse_rule_indices(self.sh_input)
        ta_indices = self.parse_rule_indices(self.ta_input)
        
        try:
            shots = gazu.shot.all_shots_for_project(
                self.cb_project.currentData())
            path = os.path.abspath(self.le_infopath.text())
            files = []
            task_types = gazu.task.all_task_types()
            for task_type in task_types:
                if task_type["for_entity"] == "Shot":
                    all_task_type_names.append(task_type["name"].lower())

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
                # save old episode & sequence if same mutlieple times
                old_episode_name = None
                old_episode_dict = None
                old_sequence_name = None
                old_sequence_dict = None
                for i, file in enumerate(files):
                    extension = os.path.splitext(file)[1]
                    if extension in acceptedExtensions:
                        if self.cb_use_folder.isChecked():
                            normpath = os.path.normpath(file)
                            path_parts = normpath.split(os.sep)
                            filename = os.path.splitext(path_parts[-1])[0]
                            name_parts = filename.split(self.delimiter_input)
                            namesplit = path_parts[: -1] + name_parts
                        else:
                            namesplit = os.path.splitext(
                                os.path.basename(file)
                            )[0].split(self.delimiter_input)

                        episode_rule = self.process_rule(self.ep_input, namesplit, ep_indices)
                        sequence_rule = self.process_rule(self.sq_input, namesplit, sq_indices)
                        shot_rule = self.process_rule(self.sh_input, namesplit, sh_indices)

                        preview_task_name = self.process_rule(self.ta_input, namesplit, ta_indices).lower()
                        if preview_task_name in all_task_type_names:
                            for task_type in task_types:
                                task_name_match = task_type["name"].lower() == preview_task_name
                                if task_type["for_entity"] == "Shot" and task_name_match:
                                    task_rule = task_type["name"]
                                    task_type_dict = task_type
                        else:
                            task_rule = "null"
                            task_type_dict = "{'name': 'null'}"
                        self.task_rule_list.append((i, task_rule))
                        self.task_type_dict_list.append((i, task_type_dict))
                        
                        exists = "No"
                        if self.has_episode == 1:
                            if old_episode_name != episode_rule:
                                episode_dict = gazu.shot.get_episode_by_name(self.cb_project.currentData(),
                                                                             episode_rule)
                                old_episode_name = episode_rule
                                old_episode_dict = episode_dict
                            else:
                                episode_dict = old_episode_dict
                            if episode_dict is not None:
                                if old_sequence_name != sequence_rule:
                                    sequence_dict = gazu.shot.get_sequence_by_name(self.cb_project.currentData(),
                                                                                   sequence_rule, episode_dict)
                                    old_sequence_name = sequence_rule
                                    old_sequence_dict = sequence_dict
                                else:
                                    sequence_dict = old_sequence_dict
                                if sequence_dict is not None:
                                    shot_dict = gazu.shot.get_shot_by_name(
                                        sequence_dict, shot_rule)
                                    if shot_dict is not None:
                                        exists = "Yes"
                        else:
                            if old_sequence_name != sequence_rule:
                                sequence_dict = gazu.shot.get_sequence_by_name(self.cb_project.currentData(),
                                                                               sequence_rule)
                                old_sequence_name = sequence_rule
                                old_sequence_dict = sequence_dict
                            else:
                                sequence_dict = old_sequence_dict
                            if sequence_dict is not None:
                                shot_dict = gazu.shot.get_shot_by_name(
                                    sequence_dict, shot_rule)

                                if shot_dict is not None:
                                    exists = "Yes"

                        episode = QTableWidgetItem(episode_rule)
                        sequence = QTableWidgetItem(sequence_rule)
                        shot = QTableWidgetItem(shot_rule)
                        task = QTableWidgetItem(task_rule)
                        vidReader = cv2.VideoCapture(file)
                        if not vidReader.isOpened():
                            # printMessage() here may cause the program to freeze, use self.log_message() instead
                            #printMessage(
                            #    "Could not read video file")
                            self.log_message(
                                f"\nCould not read video file |"
                                f"\n无法读取视频文件："
                                f"\n{file}")
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
                        self.tv_information.setItem(row, 2, episode)
                        self.tv_information.setItem(row, 3, sequence)
                        self.tv_information.setItem(row, 4, shot)
                        self.tv_information.setItem(row, 5, task)
                        self.tv_information.setItem(row, 6, framerange)
                        self.tv_information.setItem(row, 7, preview)
                        self.tv_information.setItem(row, 8, filesize)
                        self.tv_information.item(row, 8).setTextAlignment(2)

            if all('null' not in task_rule for _, task_rule in self.task_rule_list):
                self.cb_task.setEnabled(False)
                if self.cb_task.count() == self.newTaskItem_index:
                    self.cb_task.insertItem(
                        self.newTaskItem_index,
                        "There's no preview with a null task name | 没有空任务字段的预览",
                        self.cb_task.itemData(1)
                        )
                self.cb_task.setCurrentText("There's no preview with a null task name | 没有空任务字段的预览")
            else:
                self.cb_task.setEnabled(True)
                self.cb_task.removeItem(self.newTaskItem_index)
                self.cb_task.setCurrentText("Don't post | 不上传")
            self.cb_task.update()
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

                confirm_msg = QMessageBox(QMessageBox.Question,
                                          "Confirm | 确认上传",
                                          "Project | 项目:  <b>{}</b><br><br>"
                                          "Post “NULL TASK” under | 空任务字段预览上传到:<br><b>{}</b>"
                                          "<br><br>Status | 上传状态:  <b>{}</b>".format(
                                              self.cb_project.currentText(),
                                              self.cb_task.currentText(),
                                              self.cb_status.currentText()),
                                          QMessageBox.Yes | QMessageBox.No)
                confirm_msg.setWindowIcon(QIcon("kitsu.png"))
                icon_pixmap = QPixmap("kitsu.png").scaled(64, 64, aspectRatioMode=Qt.KeepAspectRatio)
                confirm_msg.setIconPixmap(QPixmap(icon_pixmap))

                if confirm_msg.exec_() == QMessageBox.Yes:
                    self.cancelTransfer = False
                    self.start_upload()

            except Exception as exc:
                printMessage("Error", exc)

        else:
            self.pb_publish.setText("...Canceling at next upload...")
            self.cancelTransfer = True

    def start_upload(self):
        self.progressBar.setValue(0)
        rows = self.tv_information.rowCount()
        self.numberOfShots = rows
        self.completed_tasks = 0
        self.total_tasks = len(self.task_type_dict_list)
        for i, task_type_dict in self.task_type_dict_list:
            # Pass the function to execute
            # Any other args, kwargs are passed to the run function
            worker = Worker(self.uploadToKitsu, i, task_type_dict)
            worker.signals.progress.connect(self.upload_progress)
            worker.signals.result.connect(self.thread_result)
            worker.signals.finished.connect(self.thread_complete)

            # Execute
            self.threadpool.start(worker)

    def upload_progress(self, calltype, data):
        if calltype == 0:  # Write upload filesize
            if hasattr(data, "text"):
                data_text = data.text()
            else:
                data_text = str(data)

            self.l_info.setText(
                "Uploading... This can take a while. Current file: "
                + data_text
            )   # str(data.text()) may cause error in some cases.
        elif calltype == 1:  # Process done. Update progressbar
            self.completed_tasks += 1
            progress_percentage = int((self.completed_tasks / self.total_tasks) * 100)
            self.progressBar.setValue(progress_percentage)

    def thread_result(self, msg):
        if msg is not None:
            # Error
            self.l_info.setText("Failed to upload to Kitsu")
            printMessage(msg)

    def thread_complete(self):
        if self.completed_tasks == self.total_tasks:
            self.l_info.setText("Done uploading")
            self.pb_publish.setText("Publish")
            self.isTransfering = False

    def uploadToKitsu(self, i, task_type_dict, progress_callback):
        if self.cancelTransfer is True:
            self.isTransfering = False
            self.pb_publish.setText("Publish")
            self.l_info.setText("Canceled! Press the Fetch button to reset the progress bar | "
                                "已取消，点击 Fetch 按钮重置进度条")
            return

        self.isTransfering = True
        self.pb_publish.setText("Cancel")
        try:
            status = self.tv_information.item(i, 0)
            # exists = self.tv_information.item(i, 1)
            episode = self.tv_information.item(i, 2)
            sequence = self.tv_information.item(i, 3)
            shot = self.tv_information.item(i, 4)
            task = self.tv_information.item(i, 5)
            framerange = self.tv_information.item(i, 6)
            preview = self.tv_information.item(i, 7)

            # Update some info
            status.setText("Uploading")
            progress_callback.emit(0, self.tv_information.item(i, 8))

            # About creating new entries:
            # We use Kitsu to handle this process.
            # To avoid confusion, the statements for creating new entries have been disabled.
            # However, this is a very cool feature—
            # if you'd like to use it, simply uncomment "{entry}_dict = gazu.shot.new_{entry}()" statement.
            if self.has_episode == 1:
                episode_msg_str = episode.text() + "/"
                # Fix Episode
                episode_dict = gazu.shot.get_episode_by_name(self.cb_project.currentData(),
                                                             episode.text())
                if episode_dict is None:
                    #episode_dict = gazu.shot.new_episode(self.cb_project.currentData(),
                    #                                       episode.text())
                    progress_callback.emit(1, i)
                    status.setText("Done")
                    self.log_message(f"\nThere is no data for this episode on Kitsu |\nKitsu上没有这一集的数据："
                                     f"\n{episode.text()}")
                    return

                # Fix Sequence
                sequence_dict = gazu.shot.get_sequence_by_name(self.cb_project.currentData(),
                                                               sequence.text(),
                                                               episode_dict)
                if sequence_dict is None:
                    #sequence_dict = gazu.shot.new_sequence(self.cb_project.currentData(),
                    #                                       sequence.text(),
                    #                                       episode_dict)
                    progress_callback.emit(1, i)
                    status.setText("Done")
                    self.log_message(f"\nThere is no data for this sequence on Kitsu |\nKitsu上没有这一场的数据："
                                     f"\n{episode_msg_str}{sequence.text()}")
                    return
            else:
                episode.setText("")
                episode_msg_str = ""
                # Fix Sequence
                sequence_dict = gazu.shot.get_sequence_by_name(self.cb_project.currentData(),
                                                               sequence.text())
                if sequence_dict is None:
                    #sequence_dict = gazu.shot.new_sequence(self.cb_project.currentData(),
                    #                                       sequence.text())
                    progress_callback.emit(1, i)
                    status.setText("Done")
                    self.log_message(f"\nThere is no data for this sequence on Kitsu |\nKitsu上没有这一场的数据："
                                     f"\n{sequence.text()}")
                    return

            # Fix Shot
            already_uploaded = True
            shot_dict = gazu.shot.get_shot_by_name(
                sequence_dict, shot.text())
            if shot_dict is None:
                #shot_dict = gazu.shot.new_shot(self.cb_project.currentData(),
                #                               sequence_dict,
                #                               shot.text(),
                #                               nb_frames=framerange.text())
                progress_callback.emit(1, i)
                status.setText("Done")
                self.log_message(f"\nThere is no data for this shot on Kitsu |\nKitsu上没有这个镜头的数据："
                                 f"\n{episode_msg_str}{sequence.text()}/{shot.text()}")
                return
                already_uploaded = False
            # Add preview
            if already_uploaded is False or self.cb_reupload.isChecked() is True:
                if "null" in task.text():
                    if self.cb_task.currentText() == "Don't post | 不上传":
                            progress_callback.emit(1, i)
                            status.setText("Done")
                            return
                    else:
                        task_dict = gazu.task.get_task_by_name(shot_dict, self.cb_task.currentData())
                        if task_dict is None:
                            #task_dict = gazu.task.new_task(shot_dict, self.cb_task.currentData())
                            self.log_message(f"\nThere is no data for this task on Kitsu |\nKitsu上没有这个环节的数据："
                                             f"\n{episode_msg_str}{sequence.text()}/{shot.text()}/{self.cb_task.currentText()}")
                            progress_callback.emit(1, i)
                            status.setText("Done")
                            return

                else:
                    task_dict = gazu.task.get_task_by_name(shot_dict, task_type_dict)
                    if task_dict is None:
                        #task_dict = gazu.task.new_task(shot_dict, task_type_dict)
                        self.log_message(f"\nThere is no data for this task on Kitsu |\nKitsu上没有这个环节的数据："
                                         f"\n{episode_msg_str}{sequence.text()}/{shot.text()}/{task.text()}")
                        progress_callback.emit(1, i)
                        status.setText("Done")
                        return

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
            msg.setWindowIcon(QIcon("kitsu.png"))
            action = msg.exec_()

            if action == 0:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def general_path(self):
        self.app_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(os.path.expanduser("~"), "KitsuPublisher")
        os.makedirs(self.config_path, exist_ok=True)
        
        self.config_file_path = os.path.join(self.config_path, ".config.ini")
        self.key_file_path = os.path.join(self.config_path, ".secret.key")
        self.log_file_path = os.path.join(self.config_path, "Publish_log.txt")

    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_file_path):
            config.read(self.config_file_path)
            self.le_kitsuURL.setText(config.get("Login", "url", fallback=""))
            self.le_username.setText(config.get("Login", "username", fallback=""))
            encrypted_password = config.get("Login", "password", fallback="")
            if encrypted_password:
                self.le_password.setText(self.decrypt_password(encrypted_password.encode()))
                self.login(refresh=True)

    def save_config(self):
        config = configparser.ConfigParser()
        config["Login"] = {
            "url": self.le_kitsuURL.text(),
            "username": self.le_username.text(),
            "password": self.encrypt_password(self.le_password.text()).decode(),
            }
        with open(self.config_file_path, "w") as configfile:
            config.write(configfile)

    def generate_key(self):
        key = Fernet.generate_key()    
        with open(self.key_file_path, "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        return open(self.key_file_path, "rb").read()

    def encrypt_password(self, password):
        key = self.load_key()
        f = Fernet(key)
        encrypted_password = f.encrypt(password.encode())
        return encrypted_password

    def decrypt_password(self, encrypted_password):
        key = self.load_key()
        f = Fernet(key)
        decrypted_password = f.decrypt(encrypted_password).decode()
        return decrypted_password

    def log_message(self, message):
        with open(self.log_file_path, "a") as log_file:
            log_file.write(message + "\n")
        print(message)

    def clear_log(self):
        with open(self.log_file_path, "w") as log_file:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write("===The following preview files have not been uploaded\n"
                           "===以下视频文件没有被上传\n"
                           f"\n{current_time}\n")

    def open_file(self, file_name, path_chosen=0):
        if path_chosen == 0:
            file_path = os.path.join(self.app_path, file_name)
        elif path_chosen == 1:
            file_path = os.path.join(self.config_path, file_name)
        else:
            print("Invalid path chosen")
            return

        if os.path.exists(file_path):
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", file_path])
            else:
                subprocess.Popen(["xdg-open", file_path])
        else:
            print(f"{file_path} does not exist")

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
