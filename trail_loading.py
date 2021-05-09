import sys
from PyQt5.QtWidgets import * #QApplication, QWidget, QLabel
from PyQt5.QtGui import * #QMovie
from PyQt5.QtCore import * #Qt, QTimer


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(271,306)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.label_animation=QLabel(self)
        self.movie=QMovie('images//loading.gif')
        self.label_animation.setMovie(self.movie)
        self.startAnimation()
        self.show()
    
    def startAnimation(self):
        self.movie.start()
    
    def stopAnimation(self):
        self.movie.stop()
        self.close()

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        label=QLabel('asjdnalsjdn',self)
        label.setGeometry(150,150,300,50)

        self.loading_screen=LoadingScreen()
        self.show()

app=QApplication(sys.argv)
demo=AppDemo()
app.exit(app.exec_())
    


