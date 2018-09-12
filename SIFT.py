from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

def inter (segn, rag, a, b):

    arr = segn[a:b+1]
    f = interp1d(np.arange(a,b+1), arr)

    newx = np.arange(a,b, rag)
    
    return np.concatenate((segn[:a],f(newx),segn[b:]))

def Fir(sig, deg):

    box = np.ones(deg)/deg
    SigSmooth = np.convolve(sig, box, mode='same')
        
    return SigSmooth

def allinea(segn1, segn2):

    a = np.argmax(segn1)
    b = np.argmax(segn2)
    diff = a-b
    return np.roll(segn2, diff)


def alla (sig, pref, p1, p2):

    ratio =float(pref-p1)/(pref-p2)
    sig = inter(sig, ratio, p1, pref)
    
    return np.roll(sig, p2-p1)

def gauss(mean, sigma, values):

    gaussian = 1/(sigma*np.sqrt(2*np.pi)) * np.exp(-((np.arange(-values/2,values/2)-mean)**2)/(2*(sigma**2)))
    return gaussian


ref = Fir(np.load('ref.npy'),20)
sec = Fir(np.load('sec.npy'),20)
ter = Fir(np.load('ter.npy'),20)
qua = Fir(np.load('qua.npy'), 10)
cin = Fir(np.load('cin.npy'), 10)

sec = allinea(ref, sec)
ter = allinea(ref, ter)
qua = allinea(ref, qua)
cin = allinea(ref, cin)

gauss1 = gauss(0, 1.5, 2000)

l1 = np.convolve(cin, gauss1)
l2 = np.convolve(l1, gauss1)
l3 = np.convolve(l2, gauss1)
l4 = np.convolve(l3, gauss1)
l5 = np.convolve(l4, gauss1)

l1 = l1[1500:4000]
l2 = np.roll(l2, -1000)[1500:4000]
l3 = np.roll(l3, -2000)[1500:4000]
l4 = np.roll(l4, -3000)[1500:4000]
l5 = np.roll(l5, -4000)[1500:4000]

d1 = l2-l1
d2 = l3-l2
d3 = l4-l3
d4 = l5-l4

plt.plot(np.arange(d1.size), d1)
plt.plot(np.arange(d2.size), d2)
plt.plot(np.arange(d3.size), d3)
plt.plot(np.arange(d4.size), d4)


#plt.ylim(1e0,1e7)
#plt.semilogy()
plt.show()



