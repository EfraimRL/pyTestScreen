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
import os
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
        #fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",QDir.homePath())
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
            if filename != '':
                if "\n" in filename:
                    filename = filename.replace("\n", "")
                self.mediaPlayer.playlist().addMedia(QMediaContent(QUrl.fromLocalFile(filename)))
        except Exception as err:
            QMessageBox.question(self, 'Error', "Formato no compatible.", QMessageBox.Ok)
            raise
    
    def removeFile(self, index=-1):
        if index==-1:
            QMessageBox.question(self, 'Error', "No se eligio un elemento para borrar.", QMessageBox.Ok)
        else:
            try:
                self.mediaPlayer.playlist().removeMedia(index)
            except Exception as err:
                print('Error al remover el archivo "'+str(index)+'", total de elementos: '+str(self.mediaPlayer.playlist().mediaCount()))

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self,index=-1):
        contador = self.count()
        if index != -1:
            self.mediaPlayer.playlist().setCurrentIndex(index)
        if self.mediaPlayer.playlist().currentIndex()==-1 or self.mediaPlayer.playlist().currentIndex()>=self.count():
            print("index del elemento a reproducir fuera del rango "+str(index)+", "+str(contador))
            return
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play() 
        
    def showNormalS(self):
        try:
            #self.monitor = QDesktopWidget().screenGeometry()
            #self.move(monitor.left(), monitor.top())
            self.showNormal()
            self.resize(700,400)
            self.center()
        except Esception as err:
            print(err)

    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()
        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()
        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)
        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft()) 

    def pause(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

    def count(self):
        return self.mediaPlayer.playlist().mediaCount()
    
class Controles(QMainWindow):

    def __init__(self, parent=None):
        super(Controles, self).__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Controles") 
        self.indexPantalla = 0
        
        self.Reproduciendo = False

        self.videoVentana = VideoWindow()
        self.videoVentana.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.videoVentana.resize(640, 480)
        #self.monitor = QDesktopWidget().screenGeometry(0)
        #self.videoVentana.setGeometry(self.monitor)
        #self.videoVentana.move(monitor.left(), monitor.top())

        self.listwidget = QListWidget()
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
        self.abrirListaButton.clicked.connect(self.openList)

        self.guardarListaButton = QPushButton()
        self.guardarListaButton.setEnabled(True)
        self.guardarListaButton.setText(" ")
        self.guardarListaButton.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        self.guardarListaButton.clicked.connect(self.saveList)

        self.quitarButton = QPushButton()
        self.quitarButton.setEnabled(True)
        self.quitarButton.setText("-")
        self.quitarButton.setIcon(self.style().standardIcon(QStyle.SP_FileIcon))
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
        self.minButton.setText("Normal")
        self.minButton.clicked.connect(self.videoVentana.showNormalS)
        
        self.screensButton = QPushButton()
        self.screensButton.setEnabled(True)
        self.screensButton.setText("Cambiar pantalla")
        self.screensButton.clicked.connect(self.elegirPantalla)

        self.sigScreenButton = QPushButton()
        self.sigScreenButton.setEnabled(True)
        self.sigScreenButton.setText(">")
        self.sigScreenButton.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.sigScreenButton.clicked.connect(self.sigPantalla)
        
        self.antScreenButton = QPushButton()
        self.antScreenButton.setEnabled(True)
        self.antScreenButton.setText("<")
        self.antScreenButton.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        self.antScreenButton.clicked.connect(self.antPantalla)

        self.lblMediaActual = QLabel()
        self.lblMediaActual.setText("Media actual: No seleccionado.")
        
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,  QSizePolicy.Maximum)

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
        controlLayout.addWidget(self.quitarButton,4,5,1,1)
        controlLayout.addWidget(self.lblMediaActual,5,4,1,4)
        controlLayout.addWidget(self.abrirListaButton,2,5,1,1)
        controlLayout.addWidget(self.sigScreenButton,2,7,1,1)
        controlLayout.addWidget(self.antScreenButton,3,7,1,1)
        controlLayout.addWidget(self.guardarListaButton,3,5,1,1)
        controlLayout.addWidget(self.errorLabel,8,0,1,8)
        layout = QVBoxLayout()
        layout.addLayout(controlLayout)
        #Eventos del reproductor
        self.videoVentana.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.videoVentana.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.videoVentana.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.videoVentana.mediaPlayer.error.connect(self.handleError)
        self.videoVentana.mediaPlayer.currentMediaChanged.connect(self.currentMediaChanged)

        # Set widget to contain window contents
        wid.setLayout(layout)

    def closeEvent(self, event):
        buttonReply = QMessageBox.question(self, 'Question', "¿Close? Will close video window too.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.videoVentana.close()
            self.close()
        else:
            print('No clicked.')
            event.ignore()
            return
        

    def sigPantalla(self):
        if self.indexPantalla == QDesktopWidget().screenCount() - 1:
            self.indexPantalla = 0
        else:
            self.indexPantalla = self.indexPantalla + 1
        monitor = QDesktopWidget().screenGeometry(self.indexPantalla)
        self.videoVentana.setGeometry(monitor)
        self.videoVentana.FullScreen()
    def antPantalla(self):
        if self.indexPantalla == 0:
            self.indexPantalla = QDesktopWidget().screenCount() - 1
        else:
            self.indexPantalla = self.indexPantalla - 1
        monitor = QDesktopWidget().screenGeometry(self.indexPantalla)
        self.videoVentana.setGeometry(monitor)
        self.videoVentana.FullScreen()
    
    def currentMediaChanged(self,actualMedia):
        titulo = str(actualMedia.canonicalUrl().fileName())
        self.videoVentana.setWindowTitle(titulo)
        self.lblMediaActual.setText("Media actual: \n" + titulo)

    def elegirPantalla(self):
        self.seleccionarP = SeleccionPantalla()
        self.seleccionarP.AsignarVideoWidget(self.videoVentana)
        self.seleccionarP.resize(400,300)
        self.seleccionarP.show()
        
    def listclicked(self, qmodelindex):
        #item = self.listwidget.currentItem()
        #print(item.text())
        #print(item.row())
        item = self.listwidget.currentIndex()

    def openList(self):
        try:
            fileName, _ = QFileDialog.getOpenFileName(self, "Seleccionar lista",QDir.homePath())
            #f = open(fileName,"r")
            self.listwidget.clear()
            for line in open(fileName, 'r'):
                self.addFile(line)
        except  Exception as err:
            QMessageBox.question(self, 'Alerta', "Error" + str(err), QMessageBox.Ok)
    def saveList(self):
        try:
            fileName, _ = QFileDialog.getOpenFileName(self, "Seleccionar lista",QDir.homePath())
            f = open(fileName,"w+")
            for i in range(0,self.listwidget.count()):
                newUrl = str(self.videoVentana.mediaPlayer.playlist().media(i).canonicalUrl().toLocalFile())
                f.write(newUrl + "\n")
            f.close()
        except  Exception as err:
            QMessageBox.question(self, 'Alerta', "Error" + str(err), QMessageBox.Ok)
        

    def addFile(self,fileName=''):        
        try:
            if fileName=='' or fileName==False:
                fileName, _ = QFileDialog.getOpenFileName(self, "Seleccionar video",QDir.homePath() + "\\Videos")
        except:
            fileName, _ = QFileDialog.getOpenFileName(self, "Seleccionar video",QDir.homePath())

        if fileName == '' or fileName==False:
            return
        for x in range(0,self.listwidget.count()):      #Valida que no exista el archivo a agregar
            try:
                if self.listwidget.itemAt(x,0).text() == os.path.splitext(os.path.basename(fileName))[0]:
                    QMessageBox.question(self, 'Alerta', "Video ya en la lista", QMessageBox.Ok)
                    return
            except Exception as err:
                print(err)
                return
        self.listwidget.insertItem(self.listwidget.count(), os.path.splitext(os.path.basename(fileName))[0])
        try:
            self.videoVentana.addFile(fileName)
        except Exception as err:                        #Si hay un error, vuelve a abrir la ventana de video y carga la lista
            self.listwidget.removeItemWidget(self.listwidget.itemAt(self.listwidget.count() - 1))
            self.Reproduciendo = False
            self.videoVentana = VideoWindow()
            self.videoVentana.resize(640, 480)
            for x in range(0,self.listwidget.count()):
                self.videoVentana.addFile(self.listwidget.itemAt(x).text())
            print(err)

    def removeFile(self):
        index = self.listwidget.currentRow()
        if index!=-1:
            try:
                cantPlayList = self.videoVentana.count()
                self.videoVentana.removeFile(index)                             #Elimina del playlist
                #self.videoVentana.mediaPlayer.playlist().removeMedia(index)
                if cantPlayList != self.videoVentana.count():                   #Si se borro de la playlist
                    self.listwidget.takeItem(index)                             #Elimina del comboBox
                print(str(self.listwidget.count()) + "<-listWidget playlist->" + str(self.videoVentana.count()))
            except Exception as err:
                print(str(err))

    def exitCall(self):
        sys.exit(app.exec_())

    def play(self):
        item = self.listwidget.currentRow()
        self.videoVentana.play(item)#play/pause

    def stop(self):
        self.videoVentana.mediaPlayer.stop()#play/pause

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
            self.listwidget.insertItem(x, "Pantalla " + str(x))
        
        self.seleccionarButton = QPushButton()
        self.seleccionarButton.setEnabled(True)
        self.seleccionarButton.setText("Elegir")
        self.seleccionarButton.clicked.connect(self.SeleccionarPantallaPorIndice)
        
        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QGridLayout()
        controlLayout.addWidget(self.listwidget,0,0,6,4)
        controlLayout.addWidget(self.seleccionarButton,0,4,1,1)

        layout = QVBoxLayout()
        layout.addLayout(controlLayout)

        # Set widget to contain window contents
        wid.setLayout(layout)


    def AsignarVideoWidget(self,widget):
        self.videoVentana = widget

    def SeleccionarPantallaPorIndice(self):
        try:
            index = self.listwidget.currentRow()
            self.monitor = QDesktopWidget().screenGeometry(index)
            self.videoVentana.setGeometry(self.monitor)
            self.videoVentana.FullScreen()
            self.close()
        except Exception as err:
            print(err)
            
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        controles = Controles()
        controles.resize(700,400)
        controles.show()
        
    except Exception as err:
        print("Error: " + str(err))
    sys.exit(app.exec_())
