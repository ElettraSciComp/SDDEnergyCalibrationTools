import numpy as np
import matplotlib.pyplot as plt

segnali = np.load('Sig_algn.npy')

def norm():


    for i in range(segnali.shape[0]):

        norm = segnali[i][2085]

        if norm !=0:

            segnali[i]= segnali[i]/norm

### ora i segnali sono normalizzati
norm()

def stampa():

    for i in range(8):
        
        plt.plot (np.arange(4095), segnali[16+i])
        
    plt.semilogy()

    plt.show()

def main():
        
    ### semplice distanza euclidea

    from scipy.spatial.distance import euclidean

    print "primo trapezio"

    for i in range(8):

        print euclidean(segnali[0], segnali[i])

    print "\n secondo trapezio"

    for i in range(8):

        print euclidean(segnali[8], segnali[8+i])

    print "\n terzo trapezio"

    for i in range(8):

        print euclidean(segnali[16], segnali[16+i])

    print "\n tutti"

    for i in range(24):

        print euclidean(segnali[0], segnali[i])

    print "\n\n\n"



    ### correlazione di pearson

    from scipy.stats import pearsonr

    print "primo trapezio"

    for i in range(8):

        print pearsonr(segnali[0], segnali[i])

    print "\n secondo trapezio"

    for i in range(8):

        print pearsonr(segnali[8], segnali[8+i])

    print "\n terzo trapezio"

    for i in range(8):

        print pearsonr(segnali[16], segnali[16+i])

    print "\n tutti"

    for i in range(24):

        print i, pearsonr(segnali[0], segnali[i])

    print "\n\n\n"

    
    ### cross correlation


    from scipy.signal import correlate

    print "primo trapezio"

    for i in range(8):

        print correlate(segnali[0], segnali[i])

    print "\n secondo trapezio"

    for i in range(8):

        print correlate(segnali[8], segnali[8+i])

    print "\n terzo trapezio"

    for i in range(8):

        print correlate(segnali[16], segnali[16+i])

    print "\n tutti"

    for i in range(24):

        print i, correlate(segnali[0], segnali[i])

    print "\n\n\n"

    

if __name__=='__main__':

    main()
