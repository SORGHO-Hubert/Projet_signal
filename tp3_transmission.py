import numpy as np
import matplotlib.pyplot as plt

def modulation_bpsk(bits):
    """Transforme les bits 0/1 en symboles -1/1"""
    return 2 * bits - 1

def canal_awgn(signal_tx, snr_db):
    """Ajoute du bruit blanc gaussien au signal"""
    snr_lin = 10**(snr_db / 10)
    # Calcul de l'écart-type du bruit
    sigma = np.sqrt(1 / (2 * snr_lin))
    bruit = sigma * np.random.standard_normal(len(signal_tx))
    return signal_tx + bruit

def demoder_bpsk(signal_rx):
    """Décision par seuillage à 0"""
    return (signal_rx > 0).astype(int)

def lancer_tp3(signal_audio):
    """
    FONCTION PRINCIPALE : Appelée par le bouton 'EXÉCUTER LA CHAÎNE' 
    du fichier main.py.
    """
    print("Début de la simulation de transmission...")
    
    # 1. Conversion du signal en bits (0/1) pour la transmission
    # On normalise et on seuille pour simuler des données binaires
    bits_source = (signal_audio > 0).astype(int)
    
    # 2. Modulation BPSK
    signal_tx = modulation_bpsk(bits_source)
    
    # 3. Passage dans le canal bruité (SNR de 10 dB par défaut)
    snr_test = 10
    signal_rx = canal_awgn(signal_tx, snr_test)
    
    # 4. Démodulation à la réception
    bits_recus = demoder_bpsk(signal_rx)
    
    # 5. Calcul du Taux d'Erreur Binaire (BER)
    erreurs = np.sum(bits_source != bits_recus)
    ber = erreurs / len(bits_source)
    
    # 6. Affichage des graphiques pour le Dr KONANE
    plt.figure("Résultats TP3 - Transmission BPSK", figsize=(12, 6))
    
    # Constellation bruitée
    plt.subplot(1, 2, 1)
    plt.plot(signal_rx[:500], np.zeros(500), 'r.', alpha=0.5)
    plt.axvline(0, color='blue', linestyle='--')
    plt.title(f"Constellation reçue (SNR = {snr_test}dB)")
    plt.xlabel("Amplitude")
    plt.grid(True)
    
    # Comparaison bits source / bits reçus
    plt.subplot(1, 2, 2)
    plt.step(range(50), bits_source[:50], label="Source", where='post', color='green')
    plt.step(range(50), bits_recus[:50], label="Reçu", where='post', color='red', linestyle='--')
    plt.title(f"Comparaison des Bits (BER = {ber:.4f})")
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    print(f"Transmission terminée. BER : {ber:.4f}")
    return bits_recus