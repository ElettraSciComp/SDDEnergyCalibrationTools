from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema
import Signals as ss


class allineatore():

    def __init__(self):
        
        self.segnali = []
        self.Shift= []
        self.trasl = []


    def apriHDF(self, location):

        siglist = []
        sigs = ss.Signals('SCAN_084.h5')    

        for i in range(len(sigs.data)):

            siglist.append(sigs.data[i].Sig)

        return siglist

    def inter (self, segn, rag, a, b):

        arr = segn[a:b+1]
        
        f = interp1d(np.arange(a,b+1), arr)

        newx = np.arange(a,b-1, rag)

        self.Shift.append(rag)
        
        return np.concatenate((segn[:a],f(newx),segn[b:]))


    def Fir(self, sig, deg):

        box = np.ones(deg)/deg
        SigSmooth = np.convolve(sig, box, mode='same')
            
        return SigSmooth


    def allinea(self, segn1, segn2):

        a = np.argmax(segn1)
        b = np.argmax(segn2)
        diff = a-b
        self.trasl.append(diff)
        return np.roll(segn2, diff)


    def zonaMassimo(self, segnali, xmin, xmax):

        listmassimi = []

        for i in range( len(segnali)):

            temp = np.argmax(self.Fir(segnali[i][xmin:xmax],10))

            listmassimi.append(temp + xmin)

        return listmassimi


    def zonaPicchi (self, segnali):

        listmassimi = []

        for i in range(len(segnali)):

            temp = argrelextrema(self.Fir(segnali[i],10), np.greater, order = 20)
                
            listmassimi.append(temp[0][0])

        return listmassimi
        

    def stampa (self, segnali):

        for i in range(len(segnali)):

            plt.plot(np.arange(segnali[i].size), self.Fir(segnali[i], 10))

        plt.semilogy()
        plt.show()
        

    def superallinea(self, segnali, picchi):
        
        pref = 2085

        for j in range(8):

            p1 = picchi[j]
            p2 = picchi[0]

            ratio =float(pref-p1)/(pref-p2)
        
            segnali[j] = self.inter(segnali[j], ratio, p1, pref)
        
            segnali[j] = np.roll(segnali[j], p2-p1)

            x = 4095 - segnali[j].size

            if x>0:

                segnali[j] = np.concatenate((segnali[j], np.zeros(x)))

            else:

                segnali[j] = segnali[j][:4095]

        return segnali
    

    def limite_picchi(self, segnali):

        limite = 0

        for i in range(len(segnali)):

            temp = argrelextrema(self.Fir(segnali[i],15), np.greater, order = 50)

            if(temp[0].size!=0):

                if (limite < temp[0][0]):
                    
                    limite = temp [0][0]

        return limite+10


    def separa(self, segnali):

        #Prende i segnali in ingresso e li separa secondo il trapezio di provenienza

        for i in range(len(segnali)/8):

            segnalit= []
            picchit=[]

            for j in range(8):

                #segnalit sono i Segnali di un singolo trapezio
                
                segnalit.append(segnali[8*i+j])

            picchit = self.zonaMassimo(segnalit, 0, self.limite_picchi(segnalit))

            segnalit = self.superallinea(segnalit, picchit)

            for j in range(8):

                self.segnali.append(segnalit[j])

        #self.stampa(self.segnali)



def main():

    al1 = allineatore()

    segnali = al1.apriHDF('SCAN_084.h5')

    for i in range(len(segnali)):

        segnali[i] = al1.Fir(segnali[i], 10)
 
        segnali[i] = al1.allinea(segnali[0], segnali[i])

    al1.separa(segnali)

    segnali = al1.segnali

    for i in range(len(segnali)):

        if i<8:

            segnali[i] = al1.inter(segnali[i], 1, 100, 4000)

        elif i<16:
            segnali[i] = al1.inter(segnali[i], 1.018, 100, 4000)

        elif i<24:
            segnali[i] = al1.inter(segnali[i], 1.0047, 100, 4000)

        else:
            segnali[i] = al1.inter(segnali[i], 1.03, 100, 4000)

        x = 4095 - segnali[i].size

        if x>0:

            segnali[i] = np.concatenate((segnali[i], np.zeros(x)))

        else:

            segnali[i] = segnali[i][:4095]
        
        segnali[i] = al1.allinea(segnali[0], segnali[i])

    np.save('Sig_algn.npy', al1.segnali)  



if __name__ == '__main__':

    main()


