import Signals as Sig
import sys
from PyQt4 import QtGui, QtCore
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

class Window(QtGui.QMainWindow):
    
    def __init__(self):
          
        QtGui.QMainWindow.__init__(self)
        self.title = ["Browse file"]
        slots = [self.browseFile]

        self.resize(200, 150)
        self.setWindowTitle('Align')
        self.segnali = []
        self.picchi = []
        self.ref=0
        self.fig, self.ax1 = plt.subplots(1, 1)
        self.shift=[]
 
        widget = QtGui.QWidget(self)
  
        grid = QtGui.QGridLayout(widget)
        grid.setVerticalSpacing(2)
        grid.setHorizontalSpacing(1)
          
        Browse_button = QtGui.QPushButton('Browse file', widget)
        self.connect(Browse_button, QtCore.SIGNAL('clicked()'), self.browseFile)


        self.span = SpanSelector(self.ax1, self.stp, 'horizontal', useblit=True,
            rectprops=dict(alpha=0.5, facecolor='green'))
        

    def browseFile(self):

        fName = QtGui.QFileDialog.getOpenFileName(self, 'Browse file' , "Open new file", self.tr("All Files (*);;Text Files (*txt)"))

        if fName.isEmpty() == False:

            self.segnali = Sig.Signals(str(fName))
            self.allinea()
            self.stampa()


    def allinea (self):
        
        x_massimi = []
        
        for i in range(len(self.segnali.data)):

            a, b = self.segnali.data[i].findMax()
            x_massimi.append(a)
            c = x_massimi[0] - x_massimi[i]
            self.shift.append(c)
            self.segnali.data[i].XShift(c)

        

        
    def cestina(self):
        return

    def stp (self, xmin, xmax):

        if (self.picchi != []):
            self.ref = self.picchi[0]
            
        self.picchi = []

        for i in range(len(self.segnali.data)):

            try:

                a, b = self.segnali.data[i].findLocalMax((xmin-self.shift[i],xmax-self.shift[i]))
                a = a+self.shift[i]
                self.picchi.append(a)

            except:
                
                self.cestina()

        if (self.ref != 0):

            self.ax1.clear()

            for i in range(len(self.picchi)):

                self.ratio = float(self.ref-self.picchi[i])/(self.ref - self.picchi[0])

                self.segnali.data[i].SigInterpole(self.ratio, self.picchi[i]+self.shift[i], self.ref+self.shift[i])

                self.allinea()
                
                self.ax1.plot(self.segnali.data[i].x, self.segnali.data[i].Fir(10))


            self.ax1.set_xlim(1000,2300)
            self.ax1.set_ylim(1e-1,100000)
            self.ax1.semilogy()
            self.fig.show()


    def stampa (self):

        for i in range(len(self.segnali.data)):

            self.ax1.plot(self.segnali.data[i].x,self.segnali.data[i].Fir(10))

        self.ax1.set_xlim(1000,2300)
        self.ax1.set_ylim(1e-1,100000)
        self.ax1.semilogy()
        self.fig.show()


if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
