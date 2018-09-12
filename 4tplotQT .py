import sys
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

import random

class Window(QtGui.QDialog):
    
    def __init__(self, parent=None):
        
        super(Window, self).__init__(parent)

        #self.setGeometry(300, 100, 800, 600)
        # distance from sx, from top, length, heigth

        self.showMaximized()
        
        self.figure, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2)


        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QtGui.QPushButton('Browse')
        self.button.clicked.connect(self.browse)

        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)
        #self.ax = self.figure.add_subplot(111)

        self.span1 =SpanSelector(self.ax1, self.extremes1, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor= 'green'))

        self.span2 =SpanSelector(self.ax2, self.extremes2, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor= 'green'))
        
        self.span3 =SpanSelector(self.ax3, self.extremes3, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor= 'green'))
        
        self.span4 =SpanSelector(self.ax4, self.extremes4, 'horizontal', useblit=True,
                    rectprops=dict(alpha=0.5, facecolor= 'green'))

    
    def extremes1(self, xmin, xmax):

        return xmin,xmax

    def extremes2(self, xmin, xmax):

        return xmin,xmax

    def extremes3(self, xmin, xmax):

        return xmin,xmax

    def extremes4(self, xmin, xmax):

        return xmin,xmax


    def browse(self):


        fName = QtGui.QFileDialog.getOpenFileName(self, 'Browse file' , "Open new file", self.tr("All Files (*);;Text Files (*txt)"))

        if fName.isEmpty() == False:
            self.fileLocation = fName
            
            self.ax1.clear()
            self.ax2.clear()
            self.ax3.clear()
            self.ax4.clear()
            
            self.printSig()

    def printSig(self):

        import Signals as ss
        import PreAllinea
        
        segnali = ss.Signals(str(self.fileLocation))
        lista_segnali=[]
        shift = PreAllinea.getShift()

        for i in range(24):

            if i<8:

                segnale = segnali.SigData(i)
                lista_segnali.append(segnale)
                lista_segnali[i].SigShift(shift[i])
                self.ax1.plot(segnale.x, segnale.SigFir(10))
                self.ax1.set_xlim(1000,2300)
                self.ax1.set_ylim(1e-1,100000)

            elif (i>7 and i<16):
        
                segnale = segnali.SigData(i)
                lista_segnali.append(segnale)
                lista_segnali[i].SigShift(shift[i])
                self.ax2.plot(segnale.x, segnale.SigFir(10))
                self.ax2.set_xlim(1000,2300)
                self.ax2.set_ylim(1e-1,100000)
                

            elif (i>15 and i<24):

                segnale = segnali.SigData(i)
                lista_segnali.append(segnale)
                lista_segnali[i].SigShift(shift[i])
                self.ax3.plot(segnale.x, segnale.SigFir(10))
                self.ax3.set_xlim(1000,2300)
                self.ax3.set_ylim(1e-1,100000)

            else:

                segnale = segnali.SigData(i)
                lista_segnali.append(segnale)
                lista_segnali[i].SigShift(shift[i])
                self.ax4.plot(segnale.x, segnale.SigFir(10))
                self.ax4.set_xlim(1000,2300)
                self.ax4.set_ylim(1e-1,100000)

        self.ax1.semilogy()
        self.ax2.semilogy()
        self.ax3.semilogy()
        self.ax4.semilogy()

        self.canvas.show()
       
        

if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
