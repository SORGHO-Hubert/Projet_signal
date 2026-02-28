import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import os  # Pour la gestion du dossier audio/
from scipy.fft import fft, fftfreq
from scipy.signal import butter, lfilter
from scipy.io import wavfile  # Pour l'export des résultats

def enregistrer_voix(duree=5, fs=44100):
    """Enregistre le signal via le micro"""
    print("Enregistrement en cours...")
    audio = sd.rec(int(duree * fs), samplerate=fs, channels=1)
    sd.wait()
    signal = np.squeeze(audio)
    
    # --- AJOUT : Sauvegarde automatique dans le dossier audio/ ---
    if not os.path.exists("audio"):
        os.makedirs("audio")
    
    chemin_wav = os.path.join("audio", "original.wav")
    # Normalisation pour la sauvegarde WAV
    s_norm = np.int16(signal / np.max(np.abs(signal)) * 32767)
    wavfile.write(chemin_wav, fs, s_norm)
    
    return signal

def filtre_passe_bas(signal, fs, fc=3400):
    """Filtre H(f) pour la bande utile (Résultat attendu 6.10)"""
    nyq = 0.5 * fs
    low = fc / nyq
    b, a = butter(5, low, btype='low')
    return lfilter(b, a, signal)

def tracer_graphiques(signal, fs, titre="Signal"):
    """Visualisation temporelle et fréquentielle (Affichage dynamique 6.9)"""
    n = len(signal)
    xf = fftfreq(n, 1/fs)
    yf = fft(signal)
    
    plt.figure(f"Analyse {titre}", figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(np.linspace(0, n/fs, n), signal)
    plt.title(f"{titre} - Domaine Temporel")
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(xf[:n//2], np.abs(yf[:n//2]))
    plt.title("Spectre de Fréquence (FFT)")
    plt.xlim(0, 5000)
    plt.grid(True)
    
    plt.tight_layout()
    plt.show(block=False) # block=False évite de bloquer ton interface graphique