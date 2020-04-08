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
#Variables globales:
puerto = 800                                    #Puerto para conexiones del servidor [socket]

#Clase de reproductor, contiene la ventana y las funciones de reproducir, pausar, detener,...,siguiente.
class VideoWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoWindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget 2 Screens")
                
        self.playlist = QMediaPlaylist()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setPlaylist(self.playlist)
        self.nombreVideoActual = ''

        videoWidget = QVideoWidget()

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

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        
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


    def setControles(self,controles):
        self.controles = controles

    def FullScreen(self):
        self.showFullScreen()

    def openFile(self, item=''):
        #fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",QDir.homePath())
        #QMessageBox.question(self, 'ITEM', item, QMessageBox.Ok)
        if item != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(item)))

    def setIndex(self, index=-1):
        print('setIndex(' + str(index) + ') in ' + str(self.mediaPlayer.playlist().mediaCount()))
        if index < 0:
            index = 0
        elif index >= self.count():
            index = self.count()-1
        if self.count()!=0:
            self.mediaPlayer.playlist().setCurrentIndex(index)
        for x in range(0,self.mediaPlayer.playlist().mediaCount()):
            print(self.mediaPlayer.playlist().media(x).canonicalUrl().fileName())

    def addFile(self, filename=''):
        try:
            if filename != '':
                if "\n" in filename:
                    filename = filename.replace("\n", "")
                self.mediaPlayer.playlist().addMedia(QMediaContent(QUrl.fromLocalFile(filename)))
                self.controles.reload()
        except Exception as err:
            QMessageBox.question(self, 'Error', "Formato no compatible.", QMessageBox.Ok)
            raise

    def addURL(self, urlname=''):
        try:
            if urlname != '':
                self.mediaPlayer.playlist().addMedia(QMediaContent(QUrl(urlname)))
        except Exception as err:
            QMessageBox.question(self, 'Error', "No se pudo agregar el video "+urlname, QMessageBox.Ok)
            raise

    def removeFile(self, index=-1):
        if index==-1:
            QMessageBox.question(self, 'Error', "No se eligio un elemento para borrar.", QMessageBox.Ok)
        else:
            try:
                self.mediaPlayer.playlist().removeMedia(index)
            except Exception as err:
                print('Error al remover el archivo "'+str(index)+'", total de elementos: '+str(self.mediaPlayer.playlist().mediaCount()))

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
        
    def pause(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
    
    def stop(self):
        self.mediaPlayer.stop()

    def next(self):
        self.setIndex(self.mediaPlayer.playlist().currentIndex()+1)

    def prev(self):
        self.setIndex(self.mediaPlayer.playlist().currentIndex()-1)

    def getListNames(self):
        list = ""
        cont = self.count()
        for x in range(0,self.count()):      
            try:                
                media = self.mediaPlayer.playlist().media(x)
                name = os.path.splitext(os.path.basename(media.canonicalUrl().fileName()))[0]
                #list.append(name)   
                list += name+"||"     
            except Exception as err:
                print(err)
        return list

    def getMediaName(self):
        try:                
            media = self.mediaPlayer.playlist().currentMedia()
            name = os.path.splitext(os.path.basename(media.canonicalUrl().fileName()))[0]
            return str(name)
        except Exception as err:
            print(err)
        return ""

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

    def count(self):
        return self.mediaPlayer.playlist().mediaCount()
#Clase principal que muestra los controles en pantalla, para controlar lo que hace el reproductor e inicia las otras clases. 
class Controles(QMainWindow):

    def __init__(self, parent=None):
        super(Controles, self).__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Controles") 
        self.indexScreen = 0
        self.Reproduciendo = False
        self.strButtonShow = "  Ver   Reproductor"
        self.strButtonHide  = "Ocultar Reproductor"

        self.videoVentana = VideoWindow()
        self.videoVentana.setControles(self)
        self.videoVentana.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)
        self.videoVentana.resize(640, 480)

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
        self.showPlayerButton.setText(self.strButtonShow)
        self.showPlayerButton.clicked.connect(self.showPlayer)

        self.maxButton = QPushButton()
        self.maxButton.setEnabled(True)
        self.maxButton.setText("Maximizar")
        self.maxButton.clicked.connect(self.maximizePlayer)

        self.minButton = QPushButton()
        self.minButton.setEnabled(True)
        self.minButton.setText("Normal")
        self.minButton.clicked.connect(self.minimizePlayer)
        
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

        #Server, receives commands to player
        self.server =  Server(self.videoVentana)
        self.startServer()

    def startServer(self):
        import threading
        try:
            threading.Thread(target=self.server.start_server, args=(puerto,)).start()
            print("Server on port "+str(puerto))
            #QMessageBox.question(self, 'Info', "Opening server on port "+str(800), QMessageBox.Ok)
            
        except  Exception as err:
            print(str(err))

    def reload(self):
        self.listwidget.clear()
        for x in range(0,self.videoVentana.count()):
            try:
                newUrl = str(self.videoVentana.mediaPlayer.playlist().media(x).canonicalUrl().toLocalFile())
                self.listwidget.insertItem(self.listwidget.count(), os.path.splitext(os.path.basename(newUrl))[0])
            except Exception as err:
                print(str(err))
    #List functions
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
    #Media functions
    def play(self):
        item = self.listwidget.currentRow()
        self.videoVentana.play(item)#play/pause
    def stop(self):
        self.videoVentana.stop()#play/pause
    #Window functions
    def elegirPantalla(self):
        self.seleccionarP = SeleccionPantalla()
        self.seleccionarP.AsignarVideoWidget(self.videoVentana)
        self.seleccionarP.resize(400,300)
        self.seleccionarP.show()
    def sigPantalla(self):
        if self.indexScreen == QDesktopWidget().screenCount() - 1:
            self.indexScreen = 0
        else:
            self.indexScreen = self.indexScreen + 1
        monitor = QDesktopWidget().screenGeometry(self.indexScreen)
        self.videoVentana.setGeometry(monitor)
        self.videoVentana.FullScreen()
        self.showPlayerButton.setText(self.strButtonHide)
    def antPantalla(self):
        if self.indexScreen == 0:
            self.indexScreen = QDesktopWidget().screenCount() - 1
        else:
            self.indexScreen = self.indexScreen - 1
        monitor = QDesktopWidget().screenGeometry(self.indexScreen)
        self.videoVentana.setGeometry(monitor)
        self.videoVentana.FullScreen()
        self.showPlayerButton.setText(self.strButtonHide)
    def showPlayer(self):
        if self.showPlayerButton.text() == self.strButtonShow:
            self.videoVentana.show()
            self.showPlayerButton.setText(self.strButtonHide)
        else:
            self.videoVentana.hide()
            self.showPlayerButton.setText(self.strButtonShow)
    def maximizePlayer(self):
        self.videoVentana.showFullScreen()
        self.showPlayerButton.setText(self.strButtonHide)
    def minimizePlayer(self):
        self.videoVentana.showNormalS()
        self.showPlayerButton.setText(self.strButtonHide)
    #Events
    def closeEvent(self, event):
        buttonReply = QMessageBox.question(self, 'Question', "¿Close? Will close video window too.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            try:
                self.server.stop()
            except Exception as err:
                print("Error at closing Thread: "+str(err))
            self.videoVentana.close()
            self.close()
        else:
            print('No clicked.')
            event.ignore()
            return
    def currentMediaChanged(self,actualMedia):
        titulo = str(actualMedia.canonicalUrl().fileName())
        self.videoVentana.setWindowTitle(titulo)
        self.lblMediaActual.setText("Media actual: \n" + titulo)
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
#Clase para elegir en que pantalla se va a mostrar el reproductor.
class SeleccionPantalla(QMainWindow):

    def __init__(self, parent = None):
        super(SeleccionPantalla, self).__init__(parent)
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Chose screen") 
        self.videoVentana = VideoWindow()
        
        self.listwidget = QListWidget()
        for x in range(0,QDesktopWidget().screenCount()):
            self.listwidget.insertItem(x, "Screen " + str(x+1))
        
        self.seleccionarButton = QPushButton()
        self.seleccionarButton.setEnabled(True)
        self.seleccionarButton.setText("Ok")
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
#Clase que permite controlar el reproductor desde otro equipo a traves del socket/puerto especificado          
class Server:  #Clase que se usa para controlar desde app externa
    def __init__(self,videoWin):
        self.videoVentana = videoWin
        self._continue = True

    def stop(self):
        self._continue = False

    def do_some_stuffs_with_input(self,input_string,vw):  
        do = input_string[0:4]
        value = ""
        returnValue = ""
        if len(input_string) >= 5:
            value = input_string[4:]
        if do == "play":
            print('Playing..')
            vw.play()
        elif do == "stop":
            print("Stop")
            vw.stop()
        elif do == "next":
            print('Nexting')
            vw.next()
        elif do == "prev":
            print("Previus")
            vw.prev()
        elif do == "setx":
            print("Set index to "+value)
            try:
                vw.setIndex(int(value))
                returnValue = "true"
            except Exception as err:
                print("Error at set index: "+value)
                returnValue = "false"
        elif do == "insr":
            print("Insert:")
            vw.addFile(value)
        elif do == "remv":
            print("Remove index:")
            vw.removeFile(index)
        elif do == "scnx":
            print("Change to Next Screen")
        elif do == "scpv":
            print("Change to Previus Screen")
        elif do == "gtls":
            list = vw.getListNames()
            print("Getting list "+str(list))
            returnValue = str(list)
        elif do == "gtmd":
            media = vw.getMediaName()
            print("Getting media "+str(media))
            returnValue = str(media)
        #elif do == "exit":
            #raise Exception("SALIR")
        #print("Processing that nasty input!")#input_string[::-1]
        return do+str(returnValue)

    def client_thread(self,conn, ip, port,vw, MAX_BUFFER_SIZE = 4096):
        no_wait = True
        while no_wait:    
            # the input is in bytes, so decode it
            input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

            # MAX_BUFFER_SIZE is how big the message can be
            # this is test if it's sufficiently big
            import sys
            siz = sys.getsizeof(input_from_client_bytes)
            if  siz >= MAX_BUFFER_SIZE:
                print("The length of input is probably too long: {}".format(siz))

            # decode input and strip the end of line
            input_from_client = input_from_client_bytes.decode("utf8").rstrip()

            res = self.do_some_stuffs_with_input(input_from_client,vw)
            #print("Result of processing {} is: {}".format(input_from_client, res))
            
            vysl = res.encode("utf8")  # encode the result string
            conn.sendall(vysl)  # send it to client
            conn.close()  # close connection
            print('Connection ' + ip + ':' + port + " ended")
            no_wait=False

    def start_server(self,_port):

        import socket
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # this is for easy starting/killing the app
        soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Socket created')

        try:
            soc.bind(("127.0.0.1", _port))
            print('Socket bind complete')
        except socket.error as msg:
            import sys
            print('Bind failed. Error : ' + str(sys.exc_info()))
            sys.exit()

        #Start listening on socket
        soc.listen(10)
        print('Socket now listening')

        # for handling task in separate jobs we need threading
        from threading import Thread

        # this will make an infinite loop needed for 
        # not reseting server for every client
        try:
            while self._continue:
                conn, addr = soc.accept()
                ip, port = str(addr[0]), str(addr[1])
                print('Accepting connection from ' + ip + ':' + port)
                try:
                    Thread(target=self.client_thread, args=(conn, ip, port,self.videoVentana)).start()
                except:
                    print("Terible error!")
                    import traceback
                    traceback.print_exc()
        except Exception as err:
            print(err)
        soc.close()
        print("Terminated")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        controles = Controles()
        controles.resize(700,400)
        controles.show()
        
    except Exception as err:
        print("Error: " + str(err))
    sys.exit(app.exec_())
