
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QMovie, QPixmap ,QImage # اضافه کردن QMovie
from pathlib import Path
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem, QTableWidget
from PyQt6.QtCore import Qt

import csv

from ultralytics import YOLO
from datetime import datetime
import os
# image_path = r"frame1358_png.rf.429138c912315c9a29eb058b408f7d14.jpg"
# path_model = r'runs_archive\runs\detect\train\weights\best.pt'


def calculate_dimensions(coords):
    x1, y1, x2, y2 = coords

    # محاسبه طول و عرض مستطیل
    length = abs(x2 - x1)
    width = abs(y2 - y1)

    return length, width

def PredictModels(image_path, path_model):
    current_datetime = datetime.now()
    model = YOLO(path_model)
    results = model.predict(source=image_path)
    stopMotion = True if len(results) == 1 else False
    result = results[0]

    data = {
        'confidence': results[0].boxes.conf.tolist(),
        'class': results[0].boxes.cls.tolist(),
        'position': results[0].boxes.xyxy.tolist()
    }
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    formatted_datetime2 = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    predPath = "temp/pred_" +  formatted_datetime2 + '.jpg'
    result.save(predPath)
    return data, formatted_datetime , predPath, stopMotion
# فراخوانی تابع
# data, formatted_datetime , predPath, stopMotion = PredictModels(image_path, path_model)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.modelPath = r'model/best.pt'
        self.ClassDetection =  {0: 'Clips', 1: 'Damage', 2: 'Loops', 3: 'Repair', 4: 'Splice', 5: 'Splice Number'}


        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(839, 471)
        MainWindow.setMinimumSize(QtCore.QSize(839, 471))
        MainWindow.setMaximumSize(QtCore.QSize(839, 471))
        MainWindow.setStyleSheet("QMainWindow {\n"
"    background-color: #rgb(254, 255, 237); /* رنگ پس‌زمینه پنجره */\n"
"    border: 1px solid #rgb(204, 202, 202); /* مرز اطراف پنجره */\n"
"    border-radius: 8px; /* گوشه‌های گرد پنجره */\n"
"}\n"
"\n"
"QMenuBar {\n"
"    background-color: rgb(255, 253, 233); /* رنگ پس‌زمینه نوار منو */\n"
"    color: #fff; /* رنگ متن نوار منو */\n"
"    border: none; /* حذف مرز */\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"    padding: 10px; /* فاصله داخلی آیتم‌های نوار منو */\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"    background-color: #555; /* رنگ پس‌زمینه آیتم‌های انتخاب شده */\n"
"}\n"
"\n"
"QToolBar {\n"
"    background-color: #f1f1f1; /* رنگ پس‌زمینه نوار ابزار */\n"
"    border: 1px solid #ddd; /* مرز نوار ابزار */\n"
"    border-radius: 4px; /* گوشه‌های گرد نوار ابزار */\n"
"}\n"
"\n"
"QToolButton {\n"
"    background-color: #fff; /* رنگ پس‌زمینه دکمه‌های نوار ابزار */\n"
"    border: 1px solid #ddd; /* مرز دکمه‌های نوار ابزار */\n"
"    border-radius: 4px; /* گوشه‌های گرد دکمه‌های نوار ابزار */\n"
"    padding: 5px; /* فاصله داخلی دکمه‌های نوار ابزار */\n"
"}\n"
"\n"
"QToolButton:hover {\n"
"    background-color: #e0e0e0; /* رنگ پس‌زمینه دکمه‌های نوار ابزار هنگام هاور */\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 811, 431))
        self.tabWidget.setStyleSheet("QTabWidget::pane {\n"
"      background-color: rgb(194, 223, 255) ;\n"
"    border: 1px solid #ccc; /* مرز اطراف پنل */\n"
"    border-radius: 14px; /* گوشه‌های گرد */\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background-color: #f1f1f1; /* رنگ پس‌زمینه تب */\n"
"    border: 1px solid #ccc; /* مرز تب */\n"
"    border-bottom: none; /* حذف مرز پایین تب */\n"
"    padding: 10px; /* فاصله داخلی تب */\n"
"    margin-right: -1px; /* فاصله بین تب‌ها */\n"
"    border-radius: 4px 4px 0 0; /* گوشه‌های گرد در بالا */\n"
"    font-size: 14px; /* اندازه فونت */\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: #fff; /* رنگ پس‌زمینه تب انتخاب شده */\n"
"    border-bottom: 1px solid #fff; /* مرز پایین تب انتخاب شده */\n"
"    font-weight: bold; /* ضخیم کردن متن تب انتخاب شده */\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background-color: #e0e0e0; /* رنگ پس‌زمینه تب هنگام هاور */\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    alignment: left; /* تراز کردن تب‌ها در وسط */\n"
"}\n"
"")
        self.tabWidget.setIconSize(QtCore.QSize(25, 25))
        self.tabWidget.setObjectName("tabWidget")
        self.lsTab = QtWidgets.QWidget()
        self.lsTab.setObjectName("lsTab")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/lsTab.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.tabWidget.addTab(self.lsTab, icon, "")
        self.AnalyseTab = QtWidgets.QWidget()
        self.AnalyseTab.setObjectName("AnalyseTab")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/anlyse.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.tabWidget.addTab(self.AnalyseTab, icon1, "")
        self.CalibrateTab = QtWidgets.QWidget()
        self.CalibrateTab.setAccessibleName("")
        self.CalibrateTab.setObjectName("CalibrateTab")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/cal.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.tabWidget.addTab(self.CalibrateTab, icon2, "")
        self.ReportTab = QtWidgets.QWidget()
        self.ReportTab.setObjectName("ReportTab")
        self.rsGroup = QtWidgets.QGroupBox(parent=self.ReportTab)
        self.rsGroup.setGeometry(QtCore.QRect(390, 40, 411, 281))
        self.rsGroup.setObjectName("rsGroup")
        self.dbTable = QtWidgets.QTableWidget(parent=self.rsGroup)
        self.dbTable.setGeometry(QtCore.QRect(10, 20, 391, 251))
        self.dbTable.setStyleSheet("QTableWidget {\n"
"    border: 1px solid #ccc; /* مرز اطراف جدول */\n"
"    border-radius: 4px; /* گوشه‌های گرد */\n"
"    gridline-color: #ddd; /* رنگ خطوط شبکه */\n"
"}\n"
"\n"
"QTableWidget::item {\n"
"    padding: 8px; /* فاصله داخلی سلول‌ها */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #f5f5f5; /* رنگ پس‌زمینه هدر */\n"
"    border: 1px solid #ddd; /* مرز هدر */\n"
"    padding: 10px; /* فاصله داخلی هدر */\n"
"    font-weight: bold; /* ضخیم کردن متن هدر */\n"
"    color: #333; /* رنگ متن هدر */\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #b3d9ff; /* رنگ پس‌زمینه سلول‌های انتخاب شده */\n"
"}\n"
"\n"
"QTableWidget::item:hover {\n"
"    background-color: #e6f7ff; /* رنگ پس‌زمینه سلول‌های هاور شده */\n"
"}\n"
"\n"
"QTableWidget::item:alternate {\n"
"    background-color: #f9f9f9; /* رنگ پس‌زمینه ردیف‌های متناوب */\n"
"}\n"
"")
        self.dbTable.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
        self.dbTable.setShowGrid(True)
        self.dbTable.setGridStyle(QtCore.Qt.PenStyle.DotLine)
        self.dbTable.setRowCount(1)
        self.dbTable.setColumnCount(5)
        self.dbTable.setObjectName("dbTable")
        self.dbTable.horizontalHeader().setVisible(True)
        self.dbTable.horizontalHeader().setCascadingSectionResizes(True)
        self.dbTable.horizontalHeader().setDefaultSectionSize(66)
        self.dbTable.horizontalHeader().setHighlightSections(True)
        self.dbTable.horizontalHeader().setMinimumSectionSize(37)
        self.dbTable.horizontalHeader().setSortIndicatorShown(False)
        self.dbTable.horizontalHeader().setStretchLastSection(True)
        self.dbTable.verticalHeader().setVisible(False)
        self.dbTable.verticalHeader().setCascadingSectionResizes(False)
        self.dbTable.verticalHeader().setMinimumSectionSize(34)
        self.dbTable.verticalHeader().setSortIndicatorShown(False)
        self.dbTable.verticalHeader().setStretchLastSection(True)

        # اضافه کردن این خط برای تنظیم اندازه ستون‌ها
        self.dbTable.resizeColumnsToContents()
        
        


        self.runBtn = QtWidgets.QPushButton(parent=self.ReportTab)
        self.runBtn.setGeometry(QtCore.QRect(630, 330, 161, 51))
        self.runBtn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.runBtn.setStyleSheet("QPushButton {\n"
"    background-color: rgb(9, 202, 80); /* رنگ پس‌زمینه */\n"
"    border: none; /* حذف مرز */\n"
"    color: white; /* رنگ متن */\n"
"    padding: 10px 20px; /* فاصله داخلی */\n"
"    text-align: center; /* تراز کردن متن */\n"
"    text-decoration: none; /* حذف تزئینات متن */\n"
"    display: inline-block; /* نمایش به صورت بلوکی درون خط */\n"
"    font-size: 18px; /* اندازه فونت */\n"
"    margin: 4px 2px; /* فاصله خارجی */\n"
"    cursor: pointer; /* نشانگر موس */\n"
"    border-radius: 12px; /* گوشه‌های گرد */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #45a049; /* رنگ پس‌زمینه هنگام هاور */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #3e8e41; /* رنگ پس‌زمینه هنگام فشار */\n"
"}\n"
"")
        
        
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icon/run.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.runBtn.setIcon(icon4)
        self.runBtn.setIconSize(QtCore.QSize(30, 30))
        self.runBtn.setObjectName("runBtn")
        self.runBtn.clicked.connect(self.onRunBtnClick)

        
        
        
        
        
        self.add_to_db = QtWidgets.QPushButton(parent=self.ReportTab)
        self.add_to_db.setGeometry(QtCore.QRect(410, 300, 141, 41))
        self.add_to_db.setStyleSheet("QPushButton {\n"
"    background-color: rgb(0, 85, 255); /* رنگ پس‌زمینه */\n"
"    border: none; /* حذف مرز */\n"
"    color: white; /* رنگ متن */\n"
"    padding: 10px 20px; /* فاصله داخلی */\n"
"    text-align: center; /* تراز کردن متن */\n"
"    text-decoration: none; /* حذف تزئینات متن */\n"
"    display: inline-block; /* نمایش به صورت بلوکی درون خط */\n"
"    font-size: 10px; /* اندازه فونت */\n"
"    margin: 4px 2px; /* فاصله خارجی */\n"
"    cursor: pointer; /* نشانگر موس */\n"
"    border-radius: 12px; /* گوشه‌های گرد */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(105, 253, 255); /* رنگ پس‌زمینه هنگام هاور */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(82, 63, 157); /* رنگ پس‌زمینه هنگام فشار */\n"
"}\n"
"")
        self.add_to_db.setObjectName("add_to_db")
        self.loadImgBtn = QtWidgets.QPushButton(parent=self.ReportTab)
        self.loadImgBtn.setGeometry(QtCore.QRect(660, 0, 131, 41))
        self.loadImgBtn.setStyleSheet("QPushButton {\n"
"    background-color: rgb(0, 85, 255); /* رنگ پس‌زمینه */\n"
"    border: none; /* حذف مرز */\n"
"    color: white; /* رنگ متن */\n"
"    padding: 10px 20px; /* فاصله داخلی */\n"
"    text-align: center; /* تراز کردن متن */\n"
"    text-decoration: none; /* حذف تزئینات متن */\n"
"    display: inline-block; /* نمایش به صورت بلوکی درون خط */\n"
"    font-size: 12px; /* اندازه فونت */\n"
"    margin: 4px 2px; /* فاصله خارجی */\n"
"    cursor: pointer; /* نشانگر موس */\n"
"    border-radius: 12px; /* گوشه‌های گرد */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(105, 253, 255); /* رنگ پس‌زمینه هنگام هاور */\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(82, 63, 157); /* رنگ پس‌زمینه هنگام فشار */\n"
"}\n"
"")

        icon40 = QtGui.QIcon()
        icon40.addPixmap(QtGui.QPixmap("icon/load.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.loadImgBtn.setIcon(icon40)
        self.loadImgBtn.setObjectName("loadImgBtn")
        self.imageTab = QtWidgets.QTabWidget(parent=self.ReportTab)
        self.imageTab.setEnabled(False)
        self.imageTab.setGeometry(QtCore.QRect(10, 10, 381, 361))
        self.imageTab.setStyleSheet("QTabWidget::pane {\n"
"    background-color: #fff; /* رنگ پس‌زمینه تب */\n"
"    border: 1px solid #ccc; /* مرز اطراف پنل */\n"
"    border-radius: 14px; /* گوشه‌های گرد */\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background-color: #f1f1f1; /* رنگ پس‌زمینه تب */\n"
"    border: 1px solid #ccc; /* مرز تب */\n"
"    border-bottom: none; /* حذف مرز پایین تب */\n"
"    padding: 0px; /* فاصله داخلی تب */\n"
"    margin-right: -1px; /* فاصله بین تب‌ها */\n"
"    border-radius: 4px 4px 0 0; /* گوشه‌های گرد در بالا */\n"
"    font-size: 14px; /* اندازه فونت */\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background-color: #fff; /* رنگ پس‌زمینه تب انتخاب شده */\n"
"    border-bottom: 1px solid #fff; /* مرز پایین تب انتخاب شده */\n"
"    font-weight: bold; /* ضخیم کردن متن تب انتخاب شده */\n"
"}\n"
"\n"
"QTabBar::tab:hover {\n"
"    background-color: #e0e0e0; /* رنگ پس‌زمینه تب هنگام هاور */\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    alignment: left; /* تراز کردن تب‌ها در وسط */\n"
"}\n"
"")
        self.imageTab.setIconSize(QtCore.QSize(15, 15))
        self.imageTab.setObjectName("imageTab")
        self.real = QtWidgets.QWidget()
        self.real.setObjectName("real")
        self.image_real = QtWidgets.QLabel(parent=self.real)
        self.image_real.setGeometry(QtCore.QRect(0, 0, 381, 341))
        # self.image_real.setStyleSheet("  background-color:rgb(255, 255, 255) ")
        self.image_real.setText("")
        self.image_real.setObjectName("image_real")
        
        
        
        # self.loading = QtWidgets.QLabel(parent=self.real)
        # self.loading.setGeometry(QtCore.QRect(80, 30, 251, 261))
        # self.loading.setStyleSheet("  background-color:rgb(255, 255, 255) ")
        # self.loading.setText("")
        # self.loading.setObjectName("loading")
        # self.movie = QMovie("loading.gif")  # مسیر فایل GIF خود را وارد کنید
        # self.loading.setMovie(self.movie)
        # self.movie.start()

        # self.loading = QtWidgets.QLabel(parent=self.real)
        # self.loading.setGeometry(QtCore.QRect(80, 30, 251, 261))
        # self.loading.setStyleSheet("background-color:rgb(255, 255, 255)")
        # self.loading.setText("")
        # self.loading.setObjectName("loading")
        # self.loading.setVisible(False)  # ابتدا لیبل را مخفی کنیم
        #
        # # بارگذاری فایل GIF
        # self.movie = QMovie("loading.gif")  # مسیر فایل GIF خود را وارد کنید
        # self.loading.setMovie(self.movie)
        #



        
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icon/i-2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.imageTab.addTab(self.real, icon5, "")
        self.pred = QtWidgets.QWidget()
        self.pred.setObjectName("pred")
        self.image_pred = QtWidgets.QLabel(parent=self.pred)
        self.image_pred.setGeometry(QtCore.QRect(0, 0, 381, 341))
        # self.image_pred.setStyleSheet("  background-color:rgb(255, 255, 255) ")
        self.image_pred.setText("")
        self.image_pred.setObjectName("image_pred")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icon/i-1.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.imageTab.addTab(self.pred, icon6, "")
        self.imageLoadCh = QtWidgets.QCheckBox(parent=self.ReportTab)
        self.imageLoadCh.setEnabled(False)
        self.imageLoadCh.setGeometry(QtCore.QRect(643, 11, 16, 20))
        self.imageLoadCh.setText("")
        self.imageLoadCh.setObjectName("imageLoadCh")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icon/report.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.tabWidget.addTab(self.ReportTab, icon7, "")
        self.SettingTab = QtWidgets.QWidget()
        self.SettingTab.setObjectName("SettingTab")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icon/setting.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.On)
        self.tabWidget.addTab(self.SettingTab, icon8, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.ErrorModel = QtWidgets.QLabel(parent=self.ReportTab)
        self.ErrorModel.setGeometry(QtCore.QRect(400, 360, 231, 21))
        self.ErrorModel.setStyleSheet("color: red;")
        self.ErrorModel.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhNone)
        self.ErrorModel.setObjectName("ErrorModel")
        self.ErrorModel.setVisible(False)

        self.add_to_db.setVisible(False)



        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(3)
        self.imageTab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.loadImgBtn.clicked.connect(self.onloadImgBtnClick)
        self.add_to_db.clicked.connect(self.onadd_to_dbClick)




    def save_to_csv(self, table_widget: QTableWidget, file_path: str, formatted_datetime: str,iamgePath: str, pred_path: str):
        # تعداد ردیف‌ها و ستون‌های جدول را دریافت می‌کنیم
        row_count = table_widget.rowCount()
        column_count = table_widget.columnCount()

        # هدرهای جدول را دریافت می‌کنیم
        headers = ['id', 'Date', 'iamgePath', 'predictionPath']
        for column in range(column_count):
            header_item = table_widget.horizontalHeaderItem(column)
            if header_item is not None:
                headers.append(header_item.text())
            else:
                headers.append(f"Column {column}")

        # بررسی می‌کنیم آیا فایل از قبل وجود دارد
        file_exists = os.path.isfile(file_path)

        # آخرین ID را پیدا می‌کنیم (اگر فایل وجود دارد)
        last_id = 0
        if file_exists:
            with open(file_path, 'r', newline='', encoding='utf-8') as csv_file:
                reader = csv.reader(csv_file)
                next(reader)  # هدر را رد می‌کنیم
                for row in reader:
                    if row:  # اگر ردیف خالی نباشد
                        last_id = int(row[0])

        with open(file_path, 'a', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            if not file_exists:
                writer.writerow(headers)

            # داده‌های هر ردیف را می‌نویسیم
            for row in range(row_count):
                last_id += 1
                row_data = [last_id, formatted_datetime,iamgePath, pred_path]
                for column in range(column_count):
                    item = table_widget.item(row, column)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                writer.writerow(row_data)



    def onadd_to_dbClick(self):
        self.save_to_csv(self.dbTable,file_path='temp/db.csv', formatted_datetime=self.formatted_datetime , pred_path=self.predPath, iamgePath=self.imagePath)
        self.add_to_db.setVisible(False)

    def onloadImgBtnClick(self):
        self.imagePath, _ = QFileDialog.getOpenFileName(self.centralwidget, "Select Image File", "", "Image Files (*.jpg *.jpeg *.png *.bmp)")
        if self.imagePath:
            print(f"Selected model file: {self.imagePath}")
            self.imageLoadCh.setChecked(True)
            image = QImage(self.imagePath)
            pixmap = QPixmap.fromImage(image)
            label_size = self.image_real.size()
            scaled_pixmap = pixmap.scaled(label_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
            self.image_real.setPixmap(scaled_pixmap)
            self.image_real.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.imageTab.setCurrentIndex(0)

    def onRunBtnClick(self):

        self.ErrorModel.setVisible(False)

        if self.imageLoadCh.isChecked():

            self.data, self.formatted_datetime , self.predPath, stopMotion = PredictModels(self.imagePath, self.modelPath)

            if stopMotion:

                self.imageTab.setCurrentIndex(1)
                self.imageTab.setEnabled(True)

                image = QImage(self.predPath)
                pixmap = QPixmap.fromImage(image)
                label_size = self.image_pred.size()
                scaled_pixmap = pixmap.scaled(label_size, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
                self.image_pred.setPixmap(scaled_pixmap)
                self.image_pred.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                num_rows = len(self.data[list(self.data.keys())[0]])
                self.dbTable.setRowCount(num_rows)  # +1 برای سطر هدر

                # پر کردن جدول
                for row in range(1, num_rows + 1):
                    self.dbTable.setItem(row-1, 0, QTableWidgetItem(str(row)))
                    self.dbTable.setItem(row-1, 1, QTableWidgetItem(self.ClassDetection[self.data['class'][row - 1]]))
                    self.dbTable.setItem(row-1, 2, QTableWidgetItem((str(round(self.data['confidence'][row - 1], 4)))))
                    cordinate = self.data['position'][row - 1]
                    Width, Length = calculate_dimensions(cordinate)
                    self.dbTable.setItem(row-1, 3, QTableWidgetItem((str(round(Width, 4)))))
                    self.dbTable.setItem(row-1, 4, QTableWidgetItem((str(round(Length, 4)))))

                self.add_to_db.setVisible(True)

            self.add_to_db.setVisible(True)
            self.dbTable.resizeColumnsToContents()

        else:
            self.ErrorModel.setVisible(True)





    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Coveyor Belt Monitoring"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.lsTab), _translate("MainWindow", "Last Refect"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.AnalyseTab), _translate("MainWindow", "Analyse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CalibrateTab), _translate("MainWindow", "Calibration"))
        self.rsGroup.setTitle(_translate("MainWindow", "Result"))
        # __sortingEnabled = self.dbTable.isSortingEnabled()
        # self.dbTable.setSortingEnabled(False)
        # item = self.dbTable.item(0, 0)
        # item.setText(_translate("MainWindow", "IN"))
        # item = self.dbTable.item(0, 1)
        # item.setText(_translate("MainWindow", "Damage Type"))
        # item = self.dbTable.item(0, 2)
        # item.setText(_translate("MainWindow", "Confidence"))
        # item = self.dbTable.item(0, 3)
        # item.setText(_translate("MainWindow", "Width"))
        # item = self.dbTable.item(0, 4)
        # item.setText(_translate("MainWindow", "Length"))
        # self.dbTable.setSortingEnabled(__sortingEnabled)
        self.dbTable.setHorizontalHeaderLabels(['IN', 'Damage Type', 'Confidence', 'Width', 'Length'])
        self.dbTable.horizontalHeader().setVisible(True)


        self.ErrorModel.setText(_translate("MainWindow", "Error! You Must Be Image!"))

        
        
        
        self.runBtn.setText(_translate("MainWindow", "Run"))
        self.add_to_db.setText(_translate("MainWindow", "Add to database"))
        self.loadImgBtn.setText(_translate("MainWindow", "Load Image"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ReportTab), _translate("MainWindow", "Report"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SettingTab), _translate("MainWindow", "Setting"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
