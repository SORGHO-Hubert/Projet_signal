import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.signal import butter, lfilter

def enregistrer_voix(duree=5, fs=44100):
    """Enregistre le signal via le micro"""
    print("Enregistrement en cours...")
    audio = sd.rec(int(duree * fs), samplerate=fs, channels=1)
    sd.wait()
    return np.squeeze(audio)

def filtre_passe_bas(signal, fs, fc=3400):
    """Filtre H(f) pour la bande utile"""
    nyq = 0.5 * fs
    low = fc / nyq
    b, a = butter(5, low, btype='low')
    return lfilter(b, a, signal)

def tracer_graphiques(signal, fs, titre="Signal"):
    """Visualisation temporelle et fréquentielle"""
    n = len(signal)
    xf = fftfreq(n, 1/fs)
    yf = fft(signal)
    
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(np.linspace(0, n/fs, n), signal)
    plt.title(f"{titre} - Domaine Temporel")
    plt.subplot(2, 1, 2)
    plt.plot(xf[:n//2], np.abs(yf[:n//2]))
    plt.title("Spectre de Fréquence (FFT)")
    plt.xlim(0, 5000)
    plt.tight_layout()
    plt.show()