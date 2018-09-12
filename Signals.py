import numpy as np
import h5py
from scipy.signal import argrelextrema
from scipy.interpolate import interp1d

class Signal():

    def __init__(self, data):
        
        self.data =  data
        self.width ,self.heigth, self.length = self.data.shape
        self.x=np.arange(self.length)
        self.Sig = np.sum(self.data, axis=(0,1))
        self.Pic = np.sum(self.data,axis=2)


    def XShift(self, shift):

        self.x = self.x + shift       


    def Fir(self, deg):

        box = np.ones(deg)/deg
        SigSmooth = np.convolve(self.Sig, box, mode='same')
        
        return SigSmooth

    def findLocalMax(self,loco=(0,4096)):

        a,b = loco
        a=int(a)
        b=int(b)
        x_max = a + argrelextrema(self.Fir(10)[a:b], np.greater, order=2000)[0][0]
        
        if (x_max.size==0):
            x_max=np.array([0])

        max = self.Sig[x_max]

        return x_max, max

    def findMax(self):

        x_max = np.argmax(self.Fir(10))
        max = self.Sig[x_max]

        return x_max, max


    def SigSub(self, inarr, a=0, b=4096):

        head = self.Sig[:a]
        tail = self.Sig[b:]
        newarr = np.concatenate((head, inarr, tail))

        self.Sig = newarr
        
        return newarr

    def XSub(self, inarr, a=0, b=4096):

        head = self.x[:a]
        tail = self.x[b:]
        newarr = np.concatenate((head, inarr, tail))

        self.x = newarr
        return newarr

    def SigInterpole(self, ratio, xmin = 0, xmax = 4095):

        arr = self.Sig[xmin:xmax+1]
        f = interp1d(np.arange(xmin, xmax+1), arr)
        newx =np.arange(xmin, xmax-1, ratio)
        newy = f(newx)

        self.Sig = np.concatenate(( self.Sig[:xmin], newy, self.Sig[xmax:]))
        self.x = np.arange(self.Sig.size)       


class Signals():

    def __init__(self, testo):

        self.file = h5py.File(testo,'r')
        self.dset = self.file[self.file.items()[0][0]]
        self.data = []
        self.sig = []
        
        for i in range(len(self.dset.keys())):

            segnale = (Signal(self.dset[self.dset.keys()[i]]))
            self.data.append(segnale)

    def SigNum(self):

        return len(self.sig)



    
        
