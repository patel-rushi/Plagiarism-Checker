from PyQt5 import QtCore, QtGui, QtWidgets
import ntpath
import check_plagairism
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
import traceback, sys

#==================================Multi-Threading====================================
class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress        

    @pyqtSlot()
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
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

#=========================================================================================================

#===================================QTableView========================================
class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        #self._data.columns=['File Name', '%']

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        
        if role == Qt.ForegroundRole:
            value = self._data[index.row()][index.column()]
            if ((isinstance(value, int) or isinstance(value, float)) and value >60):
                return QtGui.QColor('red')
            elif((isinstance(value, int) or isinstance(value, float)) and value <40):
                return QtGui.QColor('green')
            elif((isinstance(value, int) or isinstance(value, float)) and (value>=40 and value<=60)):
                return QtGui.QColor('orange')

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        columns_name=["File Name","%"]
        rows_name=[]
        for i in range(len(self._data)):
            rows_name.append(i+1)

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(columns_name[section])
            
            if orientation == Qt.Vertical:
                return str(rows_name[section])

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        if(len(self._data)>0):
            return len(self._data[0])
        else:
            return 0    
#======================================================================================

#====================================Widgets Initialization=================================
class Ui_MainWindow(object):
    def __init__(self):
        super().__init__()
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(836, 613)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 50, 421, 541))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        
        #Button - "Select Files" =========================================
        self.btn_selectfile = QtWidgets.QPushButton(self.frame)
        self.btn_selectfile.setGeometry(QtCore.QRect(110, 400, 200, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.btn_selectfile.setFont(font)
        self.btn_selectfile.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_selectfile.setStyleSheet("background-color: rgb(85, 170, 255);\n""color: rgb(255, 255, 255);")
        self.btn_selectfile.setFlat(False)
        self.btn_selectfile.setObjectName("btn_selectfile")
        #==================================================================

        #Button - "Check Plagiarism" ======================================
        self.btn_checkplagiarism = QtWidgets.QPushButton(self.frame)
        self.btn_checkplagiarism.setGeometry(QtCore.QRect(110, 460, 200, 41))
        self.btn_checkplagiarism.setFont(font)
        self.btn_checkplagiarism.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_checkplagiarism.setStyleSheet("background-color: rgb(85, 170, 255);\n""color: rgb(255, 255, 255);")
        self.btn_checkplagiarism.setFlat(False)
        self.btn_checkplagiarism.setObjectName("btn_checkplagiarism")
        self.btn_checkplagiarism.setEnabled(False)
        #==================================================================
        self.search_img = QtWidgets.QLabel(self.frame)
        self.search_img.setGeometry(QtCore.QRect(100, 120, 210, 210))
        self.search_img.setText("")
        self.search_img.setPixmap(QtGui.QPixmap("./images/search_img_final.jpg"))
        self.search_img.setObjectName("search_img")
        self.search_img.setVisible(True)
        self.listfile_table = QtWidgets.QTableView(self.frame)
        self.listfile_table.setGeometry(QtCore.QRect(50, 50, 321, 321))
        self.listfile_table.setObjectName("listfile_table")
        self.listfile_table.setVisible(False)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(420, 50, 411, 541))
        self.tabWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")

        #=====================Result table========================
        self.result_table = QtWidgets.QTableView(self.tab_3)
        self.result_table.setGeometry(QtCore.QRect(10, 30, 391, 461))
        self.result_table.setObjectName("result_table")
        #========================Label: No results==================
        self.lbl_noresults = QtWidgets.QLabel(self.tab_3)
        self.lbl_noresults.setGeometry(QtCore.QRect(150, 220, 100, 20))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(20)
        self.lbl_noresults.setFont(font)
        self.lbl_noresults.setObjectName("lbl_noresults")
        
        #====================Save Button==========================
        self.btn_save = QtWidgets.QPushButton(self.tab_3)
        self.btn_save.setGeometry(QtCore.QRect(345, 3, 50, 25))
        font.setPointSize(15)
        self.btn_save.setFont(font)
        self.btn_save.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_save.setStyleSheet("background-color: rgb(83, 85, 186);\n""color: rgb(255, 255, 255);")
        self.btn_save.setObjectName("btn_save")
        #===================Label: Loading=========================
        self.lbl_loading = QtWidgets.QLabel(self.centralwidget)
        self.lbl_loading.setFixedSize(271,306)
        self.lbl_loading.setGeometry(QtCore.QRect(500, 150, 271, 306))
        self.lbl_loading.setObjectName("lbl_loading")
        self.movie=QMovie('images//loading.gif')
        self.lbl_loading.setMovie(self.movie)
        #=============Label===========================
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 841, 51))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(85, 170, 255);\n"
"color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        #==================================================
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(740, 10, 75, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(85, 0, 255);\n"
"color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 836, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        self.threadpool = QThreadPool()
        
#======================Set label names=====================================================
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Plagiarism Checker"))
        self.btn_selectfile.setText(_translate("MainWindow", "Select Files"))
        self.btn_checkplagiarism.setText(_translate("MainWindow", "Check Plagiarism"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Tab 2"))
        self.label_2.setText(_translate("MainWindow", "  Plagiarism Checker"))
        self.pushButton.setText(_translate("MainWindow", "About"))
        self.lbl_noresults.setText(_translate("MainWindow", "No Results..."))
        self.btn_save.setText(_translate("MainWindow", "Save"))
        
        self.btn_selectfile.clicked.connect(self.openfiledialogbox)
        self.btn_checkplagiarism.clicked.connect(self.checkplagiarism)
        self.btn_save.clicked.connect(self.save)

#================================File Select and Table Update Section===============================
    def getbasename(*path):
            return ntpath.basename(path[1])
    data=[]
    pruned_data=[]
    
    def clearTable_results(self):
        self.lbl_noresults.setVisible(True)
        self.model = TableModel("")
        self.result_table.setModel(self.model)
        self.result_table.model().layoutChanged.emit()
    
    def fillfiletable(self,*filenames):
        global data
        global pruned_data
        data = filenames[1]
        pruned_data = []
        display_data = []
        i = 0
        for datas in data:
            #pruned_data.append([])
            display_data.append([])
            pruned_data.append(self.getbasename(datas))
            display_data[i].append(pruned_data[i])
            i = i+1

        if(len(pruned_data) > 0):
            self.listfile_table.setVisible(True)
            self.btn_checkplagiarism.setEnabled(True)

        self.model = TableModel(display_data)
        self.listfile_table.setModel(self.model)
        self.listfile_table.model().layoutChanged.emit()
        self.listfile_table.resizeColumnsToContents()
        vh = self.listfile_table.horizontalHeader()
        vh.setVisible(False)
        vh.setStretchLastSection(True)
            
            

    def openfiledialogbox(self):
        #print("Push me")
        file_name = QFileDialog()
        file_name.setFileMode(QFileDialog.ExistingFiles)
        name=[]
        names= file_name.getOpenFileNames(filter="*.txt *.pdf")
        #print(names)
        #self.listfile_table.clear()
        self.clearTable_results()
        self.fillfiletable(self,names[0])

    
#===================================Plagiarism Checking Process=========================================
    def progress_fn(self, n):
        print("%d%% done" % n)

    def print_output(self, s):
        print(s)
    
    def thread_complete(self):
        print("THREAD COMPLETE!")

    

    def checkplagiarism_threading(self,progress_callback):
        plag_result=[]
        plag_result=check_plagairism.func_check_plagiarism(data,pruned_data)
        
        self.movie.stop()
        self.lbl_loading.setVisible(False)

        self.model = TableModel(plag_result)
        self.result_table.setModel(self.model)
        self.result_table.resizeColumnsToContents()
        self.result_table.model().layoutChanged.emit()
        vh = self.result_table.horizontalHeader()
        vh.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        vh.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)

        self.btn_selectfile.setEnabled(True)
        self.btn_checkplagiarism.setEnabled(True)
        

    def checkplagiarism(self):
        self.clearTable_results()
        self.lbl_noresults.setVisible(False)
        
        self.movie.start()
        self.lbl_loading.setVisible(True)
        
        self.btn_selectfile.setEnabled(False)
        self.btn_checkplagiarism.setEnabled(False)
        
        worker = Worker(self.checkplagiarism_threading) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)
        
        # Execute
        self.threadpool.start(worker)
        
        #result=[]
        #result=check_plagairism.func_check_plagiarism(data,pruned_data)
        """
        self.btn_selectfile.setEnabled(True)
        self.btn_checkplagiarism.setEnabled(False)
        self.model = TableModel(plag_result)
        self.result_table.setModel(self.model)
        self.result_table.resizeColumnsToContents()
        self.result_table.model().layoutChanged.emit()
        vh = self.result_table.horizontalHeader()
        vh.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        vh.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
         """


    def save(self):
        print("save called")
#====================================END==============================================================
    



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
