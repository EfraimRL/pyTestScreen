# PyQt5 Video player
#!/usr/bin/env python
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QGridLayout,QDesktopWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction, QListWidget, QMessageBox
from PyQt5.QtGui import QIcon
import sys
#https://doc-snapshots.qt.io/qtforpython/PySide2/QtMultimedia/QMediaPlayer.html


class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget 2 Screens")

        self.playlist = QMediaPlaylist()

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.mediaPlayer.setPlaylist(self.playlist)

        self.nombreVideoActual = ''

        videoWidget = QVideoWidget()
        
        # Create new action
        #openAction = QAction(QIcon('open.png'), '&Open', self)
        #openAction.setShortcut('Ctrl+O')
        #openAction.setStatusTip('Open movie')
        #openAction.triggered.connect(self.openFile)

        # Create exit action
        #exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        #exitAction.setShortcut('Ctrl+Q')
        #exitAction.setStatusTip('Exit application')
        #exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        #menuBar = self.menuBar()
        #fileMenu = menuBar.addMenu('&File')
        #fileMenu.addAction(newAction)
        #fileMenu.addAction(openAction)
        #fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        #controlLayout.addWidget(self.playButton)
        #controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        #layout.addLayout(controlLayout)
        #layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        #self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        #self.mediaPlayer.positionChanged.connect(self.positionChanged)
        #self.mediaPlayer.durationChanged.connect(self.durationChanged)
        #self.mediaPlayer.error.connect(self.handleError)

    def FullScreen(self):
        self.showFullScreen()

    def openFile(self, item=''):

        #fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
        #        QDir.homePath())
        #QMessageBox.question(self, 'ITEM', item, QMessageBox.Ok)

        if item != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(item)))

    def setIndex(self, index=-1):
        print('setIndex(' + str(index) + ') in ' + str(self.mediaPlayer.playlist().mediaCount()))
        if index != -1:
            self.mediaPlayer.playlist().setCurrentIndex(index)

        for x in range(0,self.mediaPlayer.playlist().mediaCount()):
            print(self.mediaPlayer.playlist().media(x).canonicalUrl().fileName())

    def addFile(self, filename=''):
        try:
            if filename!='':
                self.mediaPlayer.playlist().addMedia(QMediaContent(QUrl.fromLocalFile(filename)))
        except Exception as err:
            QMessageBox.question(self, 'Error', "Formato no compatible.", QMessageBox.Ok)
            raise


    def exitCall(self):
        sys.exit(app.exec_())

    def play(self,index=-1):
        if index != -1:
            self.mediaPlayer.playlist().setCurrentIndex(index)

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play() 
        

    def pause(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

    
class Controles(QMainWindow):

    def __init__(self, parent = None):
        super(Controles, self).__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Controles") 
        
        self.Reproduciendo = False

        self.videoVentana = VideoWindow()

        self.videoVentana.resize(640, 480)
        #self.monitor = QDesktopWidget().screenGeometry(0)
        #self.videoVentana.setGeometry(self.monitor)
        #self.videoVentana.move(monitor.left(), monitor.top())

        #self.setLayout(layout)
        self.listwidget = QListWidget()
        #self.listwidget.insertItem(0, "Red")
        self.listwidget.clicked.connect(self.listclicked)

        self.playButton = QPushButton()
        self.playButton.setEnabled(True)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        
        self.stopButton = QPushButton()
        self.stopButton.setEnabled(True)
        self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopButton.clicked.connect(self.stop)

        self.anadirButton = QPushButton()
        self.anadirButton.setEnabled(True)
        self.anadirButton.setText("+")
        self.anadirButton.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        self.anadirButton.clicked.connect(self.addFile)
        
        self.removeButton = QPushButton()
        self.removeButton.setEnabled(True)
        self.removeButton.setText("-")
        self.removeButton.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
        self.removeButton.clicked.connect(self.removeFile)
        
        self.abrirListaButton = QPushButton()
        self.abrirListaButton.setEnabled(True)
        self.abrirListaButton.setText(" ")
        self.abrirListaButton.setIcon(self.style().standardIcon(QStyle.SP_FileDialogNewFolder))
        self.abrirListaButton.clicked.connect(self.addFile)

        self.guardarListaButton = QPushButton()
        self.guardarListaButton.setEnabled(True)
        self.guardarListaButton.setText(" ")
        self.guardarListaButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.guardarListaButton.clicked.connect(self.addFile)

        self.quitarButton = QPushButton()
        self.quitarButton.setEnabled(True)
        self.quitarButton.setText("Quitar -")
        self.quitarButton.clicked.connect(self.removeFile)

        self.showPlayerButton = QPushButton()
        self.showPlayerButton.setEnabled(True)
        self.showPlayerButton.setText("  Ver   Reproductor")
        self.showPlayerButton.clicked.connect(self.showPlayer)

        self.maxButton = QPushButton()
        self.maxButton.setEnabled(True)
        self.maxButton.setText("Maximizar")
        self.maxButton.clicked.connect(self.videoVentana.showFullScreen)

        self.minButton = QPushButton()
        self.minButton.setEnabled(True)
        self.minButton.setText("Minimizar")
        self.minButton.clicked.connect(self.videoVentana.showNormal)
        
        self.screensButton = QPushButton()
        self.screensButton.setEnabled(True)
        self.screensButton.setText("Cambiar pantalla")
        self.screensButton.clicked.connect(self.elegirPantalla)

        self.lblMediaActual = QLabel()
        self.lblMediaActual.setText("Label")
        
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        #controlLayout = QHBoxLayout()
        controlLayout = QGridLayout()
        #controlLayout.setContentsMargins(0, 0, 0, 0)
                                    # row, col, rowspan, colspan#
        controlLayout.addWidget(self.maxButton,0,0,1,2)
        controlLayout.addWidget(self.minButton,0,2,1,2)
        controlLayout.addWidget(self.showPlayerButton,0,4,1,2)
        controlLayout.addWidget(self.screensButton,0,6,1,2)
        controlLayout.addWidget(self.positionSlider,1,0,1,8)
        controlLayout.addWidget(self.listwidget,2,0,6,4)
        controlLayout.addWidget(self.playButton,2,4,1,1)
        controlLayout.addWidget(self.stopButton,3,4,1,1)
        controlLayout.addWidget(self.anadirButton,4,4,1,1)
        controlLayout.addWidget(self.abrirListaButton,2,5,1,1)
        controlLayout.addWidget(self.guardarListaButton,3,5,1,1)
        controlLayout.addWidget(self.errorLabel,8,0,1,8)
        #controlLayout.addWidget(self.lblMediaActual)

        layout = QVBoxLayout()
        layout.addLayout(controlLayout)

        
        self.videoVentana.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.videoVentana.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.videoVentana.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.videoVentana.mediaPlayer.error.connect(self.handleError)

        # Set widget to contain window contents
        wid.setLayout(layout)

    def elegirPantalla(self):
        self.seleccionarP = SeleccionPantalla()
        self.seleccionarP.SeleccionarWidget(self.videoVentana)
        self.seleccionarP.resize(400,300)
        self.seleccionarP.show()
        
    def listclicked(self, qmodelindex):
        #item = self.listwidget.currentItem()
        item = self.listwidget.currentIndex()
        #print(item.text())
        print(item.row())
        #self.videoVentana.openFile(item.text())
        #self.videoVentana.setIndex(item.row())

    
    def addFile(self):
        try:
            fileName, _ = QFileDialog.getOpenFileName(self, "Seleccionar video",QDir.homePath()+"\\Videos")
        except:
            fileName, _ = QFileDialog.getOpenFileName(self, "Seleccionar video",QDir.homePath())

        self.listwidget.insertItem(self.listwidget.count(), fileName)
        try:
            self.videoVentana.addFile(fileName)
        except Exception as err:
            self.listwidget.removeItemWidget(self.listwidget.itemAt(self.listwidget.count()-1))
            self.Reproduciendo = False
            self.videoVentana = VideoWindow()
            self.videoVentana.resize(640, 480)
            for x in range(0,self.listwidget.count()):
                self.videoVentana.addFile(self.listwidget.itemAt(x).text())

            print(err)

    def removeFile(self):        
        index = self.listwidget.currentRow()
        self.listwidget.removeItemWidget(self.listwidget.itemAt(index))

        try:
            self.videoVentana.addFile(fileName)
        except Exception as err:
            self.listwidget.removeItemWidget(self.listwidget.itemAt(self.listwidget.count()-1))
            self.Reproduciendo = False
            self.videoVentana = VideoWindow()
            self.videoVentana.resize(640, 480)
            for x in range(0,self.listwidget.count()):
                self.videoVentana.addFile(self.listwidget.itemAt(x).text())

            print(err)


    def removeFile(self):
        QMessageBox.question(self, 'Alerta', "Función no implementada aún.", QMessageBox.Ok)
        #self.listwidget.removeItemWidget(self.listwidget.currentRow())

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        item = self.listwidget.currentRow()
        self.videoVentana.play(item)#play/pause

    def stop(self):
        self.videoVentana.mediaPlayer.stop()#play/pause


    def pause(self):#No se usa
        self.videoVentana.pause

    def showPlayer(self):
        if self.showPlayerButton.text() == "  Ver   Reproductor":
            self.videoVentana.show()
            self.showPlayerButton.setText("Ocultar Reproductor")
        else:
            self.videoVentana.hide()
            self.showPlayerButton.setText("  Ver   Reproductor")
        
    def mediaStateChanged(self, state):
        if self.videoVentana.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.Reproduciendo = True
        else:
            self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.Reproduciendo = False

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.videoVentana.mediaPlayer.setPosition(position)

    def handleError(self):
        #self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.videoVentana.mediaPlayer.errorString())

class SeleccionPantalla(QMainWindow):

    def __init__(self, parent = None):
        super(SeleccionPantalla, self).__init__(parent)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Selección de pantalla") 
        self.videoVentana = VideoWindow()
        
        #self.setLayout(layout)
        self.listwidget = QListWidget()
        for x in range(0,QDesktopWidget().screenCount()):
            self.listwidget.insertItem(0, "Pantalla "+str(x))
        #self.listwidget.clicked.connect(self.listclicked)
        
        self.seleccionarButton = QPushButton()
        self.seleccionarButton.setEnabled(True)
        self.seleccionarButton.setText("Elegir")
        self.seleccionarButton.clicked.connect(self.SeleccionarPantalla1)
        
        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        #controlLayout = QHBoxLayout()
        controlLayout = QGridLayout()
        #controlLayout.setContentsMargins(0, 0, 0, 0)
                                    # row, col, rowspan, colspan#
        controlLayout.addWidget(self.listwidget,0,0,6,4)
        controlLayout.addWidget(self.seleccionarButton,0,4,1,1)

        layout = QVBoxLayout()
        layout.addLayout(controlLayout)

        # Set widget to contain window contents
        wid.setLayout(layout)


    def SeleccionarWidget(self,widget):
        self.videoVentana = widget

    def SeleccionarPantalla1(self):
        try:
            index = self.listwidget.currentRow()
            self.monitor = QDesktopWidget().screenGeometry(index)
            self.videoVentana.setGeometry(self.monitor)
            #self.videoVentana.move(monitor.left(), monitor.top())
        except Exception as err:
            print(err)
            
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controles = Controles()
    controles.resize(700,400)
    controles.show()
    sys.exit(app.exec_())
