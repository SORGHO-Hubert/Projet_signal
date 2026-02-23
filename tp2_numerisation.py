import numpy as np
import matplotlib.pyplot as plt

def echantillonner(signal, fs_in, fs_out):
    """Réduction de la fréquence (Shannon)"""
    pas = int(fs_in / fs_out)
    return signal[::pas]

def quantifier(signal, bits):
    """Quantification uniforme sur B bits"""
    n_niveaux = 2**bits
    v_min, v_max = -1.0, 1.0
    sig_norm = (signal - v_min) / (v_max - v_min) * (n_niveaux - 1)
    sig_q = np.round(sig_norm)
    return (sig_q / (n_niveaux - 1)) * (v_max - v_min) + v_min

def calculer_snr(orig, quant):
    """Calcul du Rapport Signal sur Bruit réel"""
    p_signal = np.mean(orig**2)
    p_bruit = np.mean((orig - quant)**2)
    return 10 * np.log10(p_signal / p_bruit)

def lancer_tp2(signal, fs_origine):
    """Fonction appelée par la GUI pour le TP2"""
    sig_ech = echantillonner(signal, fs_origine, 8000)
    sig_quant = quantifier(sig_ech, 8)
    
    plt.figure(figsize=(10, 4))
    plt.plot(sig_ech[:200], label="Original (8kHz)")
    plt.step(range(200), sig_quant[:200], label="Quantifié (8 bits)", where='post')
    plt.legend()
    plt.title("Effet de la numérisation")
    plt.show()