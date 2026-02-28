import numpy as np
import matplotlib.pyplot as plt

def modulation_bpsk(bits):
    """Transforme les bits 0/1 en symboles -1/1"""
    return 2 * bits - 1

def canal_awgn(signal_tx, snr_db):
    """Ajoute du bruit blanc gaussien au signal"""
    snr_lin = 10**(snr_db / 10)
    # Calcul de l'écart-type du bruit selon le SNR choisi
    sigma = np.sqrt(1 / (2 * snr_lin))
    bruit = sigma * np.random.standard_normal(len(signal_tx))
    return signal_tx + bruit

def demoder_bpsk(signal_rx):
    """Décision par seuillage à 0"""
    return (signal_rx > 0).astype(int)

def simuler_courbe_ber():
    """Génère la Courbe BER vs SNR (Résultat attendu 6.10)"""
    snr_db_range = np.arange(0, 11)
    ber_list = []
    
    # Test sur un petit échantillon pour la rapidité du tracé
    bits_test = np.random.randint(0, 2, 10000)
    s_tx = modulation_bpsk(bits_test)
    
    for snr in snr_db_range:
        s_rx = canal_awgn(s_tx, snr)
        bits_rx = demoder_bpsk(s_rx)
        erreurs = np.sum(bits_test != bits_rx)
        ber_list.append(erreurs / len(bits_test))
    
    plt.figure("Performances - Courbe BER", figsize=(8, 5))
    plt.semilogy(snr_db_range, ber_list, 'r-o', label='BER mesuré')
    plt.title("Taux d'erreur binaire (BER) en fonction du SNR")
    plt.xlabel("SNR (dB)")
    plt.ylabel("BER")
    plt.grid(True, which="both")
    plt.legend()
    plt.show(block=False)

def lancer_tp3(signal_audio):
    """
    FONCTION PRINCIPALE : Appelée par le bouton 'EXÉCUTER LA CHAÎNE'
    Affiche les résultats attendus 6.10
    """
    print("Début de la simulation de transmission...")
    
    # 1. Conversion du signal en bits (0/1)
    # Normalisation pour simuler des données binaires
    bits_source = (signal_audio > np.mean(signal_audio)).astype(int)
    
    # 2. Modulation BPSK
    signal_tx = modulation_bpsk(bits_source)
    
    # 3. Canal bruité (SNR par défaut de 10 dB)
    snr_test = 10
    signal_rx = canal_awgn(signal_tx, snr_test)
    
    # 4. Démodulation
    bits_recus = demoder_bpsk(signal_rx)
    
    # 5. Calcul du BER
    erreurs = np.sum(bits_source != bits_recus)
    ber = erreurs / len(bits_source)
    
    # 6. Affichage dynamique des graphiques (6.9)
    plt.figure("Résultats TP3 - Transmission BPSK", figsize=(12, 6))
    
    # Constellation bruitée (Signal transmis/reçu)
    plt.subplot(1, 2, 1)
    plt.plot(signal_rx[:500], np.zeros(500), 'r.', alpha=0.5)
    plt.axvline(0, color='blue', linestyle='--')
    plt.title(f"Signal Transmis avec Bruit (SNR = {snr_test}dB)")
    plt.xlabel("Amplitude")
    plt.grid(True)
    
    # Comparaison des bits
    plt.subplot(1, 2, 2)
    plt.step(range(50), bits_source[:50], label="Source", where='post', color='green')
    plt.step(range(50), bits_recus[:50], label="Reçu", where='post', color='red', linestyle='--')
    plt.title(f"Comparaison des Bits (BER = {ber:.4f})")
    plt.legend()
    
    plt.tight_layout()
    plt.show(block=False) # block=False pour ne pas geler l'interface
    
    return bits_recus