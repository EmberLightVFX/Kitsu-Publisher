# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'ui.ui'
##
# Created by: Qt User Interface Compiler version 5.15.1
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

***REMOVED***
***REMOVED***
***REMOVED***


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(500, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gb_p1 = QGroupBox(self.centralwidget)
        self.gb_p1.setObjectName(u"gb_p1")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.gb_p1.sizePolicy().hasHeightForWidth())
        self.gb_p1.setSizePolicy(sizePolicy1)
        self.gb_p1.setFlat(False)
        self.gb_p1.setCheckable(False)
        self.verticalLayout_2 = QVBoxLayout(self.gb_p1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.l_kitsuURL = QLabel(self.gb_p1)
        self.l_kitsuURL.setObjectName(u"l_kitsuURL")

        self.horizontalLayout_2.addWidget(self.l_kitsuURL)

        self.le_kitsuURL = QLineEdit(self.gb_p1)
        self.le_kitsuURL.setObjectName(u"le_kitsuURL")

        self.horizontalLayout_2.addWidget(self.le_kitsuURL)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.l_username = QLabel(self.gb_p1)
        self.l_username.setObjectName(u"l_username")

        self.horizontalLayout_3.addWidget(self.l_username)

        self.le_username = QLineEdit(self.gb_p1)
        self.le_username.setObjectName(u"le_username")

        self.horizontalLayout_3.addWidget(self.le_username)

        self.l_password = QLabel(self.gb_p1)
        self.l_password.setObjectName(u"l_password")

        self.horizontalLayout_3.addWidget(self.l_password)

        self.le_password = QLineEdit(self.gb_p1)
        self.le_password.setObjectName(u"le_password")
        self.le_password.setEchoMode(QLineEdit.Password)

        self.horizontalLayout_3.addWidget(self.le_password)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.pb_login = QPushButton(self.gb_p1)
        self.pb_login.setObjectName(u"pb_login")

        self.verticalLayout_2.addWidget(self.pb_login)

        self.project_layout = QHBoxLayout()
        self.project_layout.setObjectName(u"project_layout")
        self.l_project = QLabel(self.gb_p1)
        self.l_project.setObjectName(u"l_project")
        self.l_project.setEnabled(False)
        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.l_project.sizePolicy().hasHeightForWidth())
        self.l_project.setSizePolicy(sizePolicy2)

        self.project_layout.addWidget(self.l_project)

        self.cb_project = QComboBox(self.gb_p1)
        self.cb_project.setObjectName(u"cb_project")
        self.cb_project.setEnabled(False)

        self.project_layout.addWidget(self.cb_project)

        self.verticalLayout_2.addLayout(self.project_layout)

        self.verticalLayout.addWidget(self.gb_p1)

        self.gb_p2 = QGroupBox(self.centralwidget)
        self.gb_p2.setObjectName(u"gb_p2")
        sizePolicy1.setHeightForWidth(
            self.gb_p2.sizePolicy().hasHeightForWidth())
        self.gb_p2.setSizePolicy(sizePolicy1)
        self.verticalLayout_3 = QVBoxLayout(self.gb_p2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.rb_doXML = QRadioButton(self.gb_p2)
        self.rb_doXML.setObjectName(u"rb_doXML")
        self.rb_doXML.setChecked(True)

        self.horizontalLayout_5.addWidget(self.rb_doXML)

        self.rb_doFolder = QRadioButton(self.gb_p2)
        self.rb_doFolder.setObjectName(u"rb_doFolder")

        self.horizontalLayout_5.addWidget(self.rb_doFolder)

        self.cb_subfolders = QCheckBox(self.gb_p2)
        self.cb_subfolders.setObjectName(u"cb_subfolders")
        self.cb_subfolders.setEnabled(False)
        self.cb_subfolders.setChecked(True)

        self.horizontalLayout_5.addWidget(self.cb_subfolders)

        self.le_infopath = QLineEdit(self.gb_p2)
        self.le_infopath.setObjectName(u"le_infopath")

        self.horizontalLayout_5.addWidget(self.le_infopath)

        self.pb_pick = QPushButton(self.gb_p2)
        self.pb_pick.setObjectName(u"pb_pick")

        self.horizontalLayout_5.addWidget(self.pb_pick)

        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.pb_fetch = QPushButton(self.gb_p2)
        self.pb_fetch.setObjectName(u"pb_fetch")

        self.verticalLayout_3.addWidget(self.pb_fetch)

        self.verticalLayout.addWidget(self.gb_p2)

        self.gb_p3 = QGroupBox(self.centralwidget)
        self.gb_p3.setObjectName(u"gb_p3")
        self.verticalLayout_5 = QVBoxLayout(self.gb_p3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tv_information = QTableWidget(self.gb_p3)
        if (self.tv_information.columnCount() < 7):
            self.tv_information.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.tv_information.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tv_information.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tv_information.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tv_information.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tv_information.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tv_information.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignJustify | Qt.AlignVCenter)
        self.tv_information.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tv_information.setObjectName(u"tv_information")
        self.tv_information.setAlternatingRowColors(True)
        self.tv_information.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tv_information.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tv_information.setHorizontalScrollMode(
            QAbstractItemView.ScrollPerPixel)
        self.tv_information.setWordWrap(False)

        self.verticalLayout_5.addWidget(self.tv_information)

        self.tasklayout = QFormLayout()
        self.tasklayout.setObjectName(u"tasklayout")
        self.l_task = QLabel(self.gb_p3)
        self.l_task.setObjectName(u"l_task")
        self.l_task.setEnabled(False)
        sizePolicy2.setHeightForWidth(
            self.l_task.sizePolicy().hasHeightForWidth())
        self.l_task.setSizePolicy(sizePolicy2)

        self.tasklayout.setWidget(0, QFormLayout.LabelRole, self.l_task)

        self.l_status = QLabel(self.gb_p3)
        self.l_status.setObjectName(u"l_status")
        self.l_status.setEnabled(False)

        self.tasklayout.setWidget(1, QFormLayout.LabelRole, self.l_status)

        self.cb_status = QComboBox(self.gb_p3)
        self.cb_status.setObjectName(u"cb_status")
        self.cb_status.setEnabled(False)

        self.tasklayout.setWidget(1, QFormLayout.FieldRole, self.cb_status)

        self.cb_task = QComboBox(self.gb_p3)
        self.cb_task.setObjectName(u"cb_task")
        self.cb_task.setEnabled(False)

        self.tasklayout.setWidget(0, QFormLayout.FieldRole, self.cb_task)

        self.verticalLayout_5.addLayout(self.tasklayout)

        self.verticalLayout.addWidget(self.gb_p3)

        self.gb_p4 = QGroupBox(self.centralwidget)
        self.gb_p4.setObjectName(u"gb_p4")
        self.verticalLayout_4 = QVBoxLayout(self.gb_p4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cb_reupload = QCheckBox(self.gb_p4)
        self.cb_reupload.setObjectName(u"cb_reupload")

        self.horizontalLayout.addWidget(self.cb_reupload)

        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.pb_publish = QPushButton(self.gb_p4)
        self.pb_publish.setObjectName(u"pb_publish")

        self.verticalLayout_4.addWidget(self.pb_publish)

        self.progressBar = QProgressBar(self.gb_p4)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout_4.addWidget(self.progressBar)

        self.l_info = QLabel(self.gb_p4)
        self.l_info.setObjectName(u"l_info")

        self.verticalLayout_4.addWidget(self.l_info)

        self.verticalLayout.addWidget(self.gb_p4)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.l_createdby = QLabel(self.centralwidget)
        self.l_createdby.setObjectName(u"l_createdby")

        self.horizontalLayout_7.addWidget(self.l_createdby)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.l_appinfo = QLabel(self.centralwidget)
        self.l_appinfo.setObjectName(u"l_appinfo")

        self.horizontalLayout_9.addWidget(self.l_appinfo)

        self.l_appversion = QLabel(self.centralwidget)
        self.l_appversion.setObjectName(u"l_appversion")

        self.horizontalLayout_9.addWidget(self.l_appversion)

        self.horizontalLayout_7.addLayout(self.horizontalLayout_9)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_7.addWidget(self.line)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.l_gazuinfo = QLabel(self.centralwidget)
        self.l_gazuinfo.setObjectName(u"l_gazuinfo")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.l_gazuinfo.sizePolicy().hasHeightForWidth())
        self.l_gazuinfo.setSizePolicy(sizePolicy3)
        self.l_gazuinfo.setLayoutDirection(Qt.LeftToRight)

        self.horizontalLayout_8.addWidget(self.l_gazuinfo)

        self.l_gazuversion = QLabel(self.centralwidget)
        self.l_gazuversion.setObjectName(u"l_gazuversion")

        self.horizontalLayout_8.addWidget(self.l_gazuversion)

        self.horizontalLayout_7.addLayout(self.horizontalLayout_8)

        self.verticalLayout.addLayout(self.horizontalLayout_7)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate(
            "MainWindow", u"Kitsu Publisher", None))
        self.gb_p1.setTitle(QCoreApplication.translate(
            "MainWindow", u"1. Login", None))
        self.l_kitsuURL.setText(QCoreApplication.translate(
            "MainWindow", u"Kitsu URL:", None))
        self.l_username.setText(QCoreApplication.translate(
            "MainWindow", u"Username:", None))
        self.l_password.setText(QCoreApplication.translate(
            "MainWindow", u"Password:", None))
        self.pb_login.setText(QCoreApplication.translate(
            "MainWindow", u"Log in", None))
        self.l_project.setText(QCoreApplication.translate(
            "MainWindow", u"Project:", None))
        self.gb_p2.setTitle(QCoreApplication.translate(
            "MainWindow", u"2. Where to fetch information from", None))
        self.rb_doXML.setText(QCoreApplication.translate(
            "MainWindow", u"Resolve XML", None))
        self.rb_doFolder.setText(
            QCoreApplication.translate("MainWindow", u"Folder", None))
        self.cb_subfolders.setText(QCoreApplication.translate(
            "MainWindow", u"Subfolders", None))
        self.pb_pick.setText(QCoreApplication.translate(
            "MainWindow", u"Pick", None))
        self.pb_fetch.setText(QCoreApplication.translate(
            "MainWindow", u"Fetch!", None))
        self.gb_p3.setTitle(QCoreApplication.translate(
            "MainWindow", u"3. Analyze your information", None))
        ___qtablewidgetitem = self.tv_information.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("MainWindow", u"Status", None))
        ___qtablewidgetitem1 = self.tv_information.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate(
            "MainWindow", u"Shot Exists", None))
        ___qtablewidgetitem2 = self.tv_information.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate("MainWindow", u"Sequence", None))
        ___qtablewidgetitem3 = self.tv_information.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate("MainWindow", u"Shot", None))
        ___qtablewidgetitem4 = self.tv_information.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate("MainWindow", u"Framerange", None))
        ___qtablewidgetitem5 = self.tv_information.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate(
            "MainWindow", u"Preview Path", None))
        ___qtablewidgetitem6 = self.tv_information.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(
            QCoreApplication.translate("MainWindow", u"Filesize", None))
        self.l_task.setText(QCoreApplication.translate(
            "MainWindow", u"Post previews under:", None))
        self.l_status.setText(QCoreApplication.translate(
            "MainWindow", u"With status:", None))
        self.gb_p4.setTitle(QCoreApplication.translate(
            "MainWindow", u"4. Publish", None))
        self.cb_reupload.setText(QCoreApplication.translate(
            "MainWindow", u"Upload previews to shots that already exists", None))
        self.pb_publish.setText(QCoreApplication.translate(
            "MainWindow", u"Publish", None))
        self.l_info.setText(QCoreApplication.translate(
            "MainWindow", u"Information bar", None))
        self.l_createdby.setText(QCoreApplication.translate(
            "MainWindow", u"Created by Jacob Danell, Ember Light", None))
        self.l_appinfo.setText(QCoreApplication.translate(
            "MainWindow", u"Kitsu Publisher v", None))
        self.l_appversion.setText(
            QCoreApplication.translate("MainWindow", u"1234", None))
        self.l_gazuinfo.setText(QCoreApplication.translate(
            "MainWindow", u"Gazu v", None))
        self.l_gazuversion.setText(
            QCoreApplication.translate("MainWindow", u"1234", None))
    # retranslateUi
