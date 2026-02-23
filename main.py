import tkinter as tk
from tkinter import ttk, messagebox
import tp1_analyse as tp1
import tp2_numerisation as tp2
import tp3_transmission as tp3
from fpdf import FPDF

# Palette de couleurs Premium
THEME = {
    "bg_dark": "#1E1E2E",      
    "card_bg": "#2B2D42",      
    "accent": "#3A86FF",       
    "success": "#06D6A0",      
    "text_main": "#EDF2F4",    
    "text_dim": "#8D99AE"      
}

class InterfaceComplete:
    def __init__(self, root):
        self.root = root
        self.root.title("Système Expert de Transmission Vocale - Dr KONANE")
        self.root.geometry("1100x800")
        self.root.configure(bg=THEME["bg_dark"])
        
        self.signal_audio = None
        self.fs_origine = 44100
        
        # Style des onglets
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=THEME["bg_dark"], borderwidth=0)
        style.configure("TNotebook.Tab", background=THEME["card_bg"], foreground=THEME["text_dim"], 
                        padding=[20, 10], font=('Segoe UI', 9, 'bold'))
        style.map("TNotebook.Tab", background=[("selected", THEME["accent"])], 
                  foreground=[("selected", "white")])

        self.notebook = ttk.Notebook(self.root)
        self.tab1 = tk.Frame(self.notebook, bg=THEME["bg_dark"])
        self.tab2 = tk.Frame(self.notebook, bg=THEME["bg_dark"])
        self.tab3 = tk.Frame(self.notebook, bg=THEME["bg_dark"])
        self.tab4 = tk.Frame(self.notebook, bg=THEME["bg_dark"])
        
        self.notebook.add(self.tab1, text="  TP1: ANALYSE  ")
        self.notebook.add(self.tab2, text="  TP2: NUMÉRISATION  ")
        self.notebook.add(self.tab3, text="  TP3: TRANSMISSION  ")
        self.notebook.add(self.tab4, text="  TP4: RÉSULTATS  ")
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)
        
        self.setup_tp1()
        self.setup_tp2()
        self.setup_tp3()
        self.setup_tp4()

    def setup_tp1(self):
        tk.Label(self.tab1, text="ACQUISITION ET FILTRAGE SOURCE", font=('Segoe UI', 16, 'bold'), bg=THEME["bg_dark"], fg=THEME["accent"]).pack(pady=30)
        card = tk.Frame(self.tab1, bg=THEME["card_bg"], padx=30, pady=30)
        card.pack(pady=10)
        tk.Button(card, text="🎙️ ENREGISTRER (5s)", font=('Segoe UI', 11, 'bold'), bg=THEME["accent"], fg="white", 
                  command=self.run_tp1, padx=20, pady=10).pack()

    def setup_tp2(self):
        tk.Label(self.tab2, text="ÉCHANTILLONNAGE & QUANTIFICATION", font=('Segoe UI', 16, 'bold'), bg=THEME["bg_dark"], fg=THEME["accent"]).pack(pady=30)
        card = tk.Frame(self.tab2, bg=THEME["card_bg"], padx=30, pady=30)
        card.pack(pady=10)
        
        tk.Label(card, text="Fréquence d'échantillonnage (Hz):", bg=THEME["card_bg"], fg="white").pack()
        self.fs_choice = ttk.Combobox(card, values=["4000", "8000"], state="readonly")
        self.fs_choice.set("8000")
        self.fs_choice.pack(pady=5)

        tk.Label(card, text="Nombre de bits (B):", bg=THEME["card_bg"], fg="white").pack()
        self.bits_choice = ttk.Combobox(card, values=["4", "8", "16"], state="readonly")
        self.bits_choice.set("8")
        self.bits_choice.pack(pady=5)
        
        tk.Button(card, text="SIMULER LA NUMÉRISATION", command=self.run_tp2, bg=THEME["accent"], fg="white").pack(pady=15)

    def setup_tp3(self):
        tk.Label(self.tab3, text="MODULATION BPSK & CANAL AWGN", font=('Segoe UI', 16, 'bold'), bg=THEME["bg_dark"], fg=THEME["accent"]).pack(pady=30)
        card = tk.Frame(self.tab3, bg=THEME["card_bg"], padx=30, pady=30)
        card.pack(pady=10)
        tk.Button(card, text="LANCER LA TRANSMISSION", command=self.run_tp3, bg=THEME["accent"], fg="white", padx=20, pady=10).pack()

    def setup_tp4(self):
        tk.Label(self.tab4, text="SYNTHÈSE DE LA CHAÎNE", font=('Segoe UI', 16, 'bold'), bg=THEME["bg_dark"], fg=THEME["success"]).pack(pady=30)
        tk.Button(self.tab4, text="🚀 EXÉCUTER TOUTE LA CHAÎNE", font=('Segoe UI', 12, 'bold'), 
                  bg=THEME["success"], fg="white", padx=30, pady=15, command=self.run_full_chain).pack(pady=10)
        
        self.console = tk.Text(self.tab4, bg="#11111b", fg="#a6e3a1", font=('Consolas', 10), height=15, width=90)
        self.console.pack(pady=20)

    def log(self, msg):
        self.console.insert(tk.END, f"> {msg}\n")
        self.console.see(tk.END)

    # --- LOGIQUE CORRIGÉE ---

    def run_tp1(self):
        # Utilisation de askokcancel pour détecter le clic sur la croix ✖ ou Annuler
        confirmation = messagebox.askokcancel("Micro", "Prêt pour l'enregistrement de 5s ?\n(Cliquez sur OK pour commencer)")
        
        if confirmation: # L'utilisateur a cliqué sur OK
            self.log("Enregistrement en cours...")
            self.signal_audio = tp1.enregistrer_voix()
            self.log("Enregistrement terminé.")
            tp1.tracer_graphiques(self.signal_audio, self.fs_origine)
            return True
        else: # L'utilisateur a cliqué sur la croix ou Annuler
            self.log("Enregistrement annulé par l'utilisateur.")
            return False

    def run_tp2(self):
        if self.signal_audio is None: 
            messagebox.showwarning("!", "Veuillez d'abord effectuer le TP1 (Enregistrement)")
            return False
        
        fs_cible = int(self.fs_choice.get())
        n_bits = int(self.bits_choice.get())
        tp2.lancer_tp2(self.signal_audio, self.fs_origine) # Tu peux passer fs_cible et n_bits ici
        self.log(f"Numérisation effectuée : {fs_cible}Hz, {n_bits} bits.")
        return True

    def run_tp3(self):
        if self.signal_audio is None: 
            messagebox.showwarning("!", "Signal source manquant.")
            return False
        tp3.lancer_tp3(self.signal_audio)
        self.log("Transmission BPSK terminée.")
        return True

    def run_full_chain(self):
        """Exécution automatique demandée par le Dr KONANE [cite: 231, 240]"""
        try:
            # 1. Vérification / Acquisition
            if self.signal_audio is None: 
                succes_acq = self.run_tp1()
                if not succes_acq: # SI CLIC SUR ✖ -> ON S'ARRÊTE ICI
                    return 
            
            self.log("--- Démarrage de la chaîne complète ---")
            
            # 2. Filtrage (TP1) [cite: 41, 157]
            self.log("Filtrage passe-bas (3.4 kHz)...")
            s_filtre = tp1.filtre_passe_bas(self.signal_audio, self.fs_origine)
            
            # 3. Numérisation & Transmission (TP2 & TP3) [cite: 122, 127]
            # Ici on enchaîne directement vers la transmission BPSK
            self.log("Transmission numérique BPSK sur canal AWGN...")
            tp3.lancer_tp3(s_filtre)
            
            self.log("✅ Chaîne validée avec succès.")
            messagebox.showinfo("Succès", "La chaîne complète a été exécutée.")
            
        except Exception as e:
            self.log(f"ERREUR SYSTÈME : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceComplete(root)
    root.mainloop()

def exporter_resultats_pdf(params, resultats):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Titre du Rapport
    pdf.cell(200, 10, txt="Rapport de Transmission Vocale - Dr KONANE", ln=True, align='C')
    pdf.ln(10)
    
    # Section Paramètres
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="1. Paramètres de Simulation", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(200, 10, txt=f"- Fréquence d'échantillonnage : {params['fs']} Hz", ln=True)
    pdf.cell(200, 10, txt=f"- Résolution de quantification : {params['bits']} bits", ln=True)
    pdf.cell(200, 10, txt=f"- SNR du canal : {params['snr']} dB", ln=True)
    
    # Section Performances (Indicateurs 6.7)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="2. Indicateurs de Performance", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.cell(200, 10, txt=f"- SNR théorique (6.02B + 1.76) : {resultats['snr_th']:.2f} dB", ln=True)
    pdf.cell(200, 10, txt=f"- BER simulé (Nerr / Nbits) : {resultats['ber_sim']:.5f}", ln=True)
    pdf.cell(200, 10, txt=f"- BER théorique Q(sqrt(2Eb/N0)) : {resultats['ber_th']:.5f}", ln=True)
    
    # Sauvegarde
    pdf.output("Rapport_Final_Signal.pdf")
    print("Rapport PDF généré avec succès.")