import numpy as np
import matplotlib.pyplot as plt

def echantillonner(signal, fs_in, fs_out):
    """Réduction de la fréquence (Critère de Shannon)"""
    pas = int(fs_in / fs_out)
    return signal[::pas]

def quantifier(signal, bits):
    """Quantification uniforme sur B bits (4 vs 16 bits)"""
    n_niveaux = 2**bits
    v_min, v_max = np.min(signal), np.max(signal) # Dynamique réelle du signal
    
    if v_max == v_min: return signal
    
    # Normalisation et mise sur niveaux
    sig_norm = (signal - v_min) / (v_max - v_min) * (n_niveaux - 1)
    sig_q = np.round(sig_norm)
    
    # Reconstruction du signal quantifié
    return (sig_q / (n_niveaux - 1)) * (v_max - v_min) + v_min

def calculer_snr(orig, quant):
    """Calcul du Rapport Signal sur Bruit (Performance SNR)"""
    # On s'assure que les signaux ont la même longueur
    min_len = min(len(orig), len(quant))
    p_signal = np.mean(orig[:min_len]**2)
    p_bruit = np.mean((orig[:min_len] - quant[:min_len])**2)
    
    if p_bruit == 0: return float('inf')
    return 10 * np.log10(p_signal / p_bruit)

def lancer_tp2(signal, fs_origine, bits=8, fs_cible=8000):
    """
    Fonction appelée par le TP4 pour la chaîne globale.
    Permet de visualiser le 'Signal quantifié' attendu.
    """
    if signal is None: return None
    
    # 1. Échantillonnage selon le choix (4kHz ou 8kHz)
    sig_ech = echantillonner(signal, fs_origine, fs_cible)
    
    # 2. Quantification selon le choix (4 ou 16 bits)
    sig_quant = quantifier(sig_ech, bits)
    
    # 3. Affichage dynamique requis (6.9)
    plt.figure(f"Numérisation : {bits} bits / {fs_cible} Hz", figsize=(10, 5))
    plt.plot(sig_ech[:400], label="Signal Échantillonné", alpha=0.6)
    plt.step(range(400), sig_quant[:400], label=f"Signal Quantifié ({bits} bits)", where='post')
    
    snr = calculer_snr(sig_ech, sig_quant)
    plt.title(f"Visualisation TP2 - SNR : {snr:.2f} dB")
    plt.legend()
    plt.grid(True)
    plt.show(block=False) # Important pour ne pas bloquer la GUI
    
    return sig_quant