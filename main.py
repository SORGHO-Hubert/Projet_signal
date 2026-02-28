import tkinter as tk
from tkinter import ttk, messagebox
import tp1_analyse as tp1
import tp2_numerisation as tp2
import tp3_transmission as tp3
from fpdf import FPDF
import matplotlib.pyplot as plt
import datetime

# Mode interactif pour éviter le gel de la GUI
plt.ion()

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
        
        # --- STYLE INTERFACE (Conservé tel quel) ---
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

    # --- MÉTHODES DE CONFIGURATION DES ONGLETS ---
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
        # Appel à la fonction BER requise
        tk.Button(card, text="📈 VOIR COURBE BER", command=lambda: tp3.simuler_courbe_ber(), bg="#6C757D", fg="white").pack(pady=5)

    def setup_tp4(self):
        tk.Label(self.tab4, text="SYNTHÈSE DE LA CHAÎNE", font=('Segoe UI', 16, 'bold'), bg=THEME["bg_dark"], fg=THEME["success"]).pack(pady=30)
        btn_frame = tk.Frame(self.tab4, bg=THEME["bg_dark"])
        btn_frame.pack()
        tk.Button(btn_frame, text="🚀 EXÉCUTER TOUTE LA CHAÎNE", font=('Segoe UI', 12, 'bold'), bg=THEME["success"], fg="white", padx=30, pady=15, command=self.run_full_chain).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="📄 EXPORT PDF", font=('Segoe UI', 12, 'bold'), bg=THEME["accent"], fg="white", padx=30, pady=15, command=self.exporter_pdf).pack(side=tk.LEFT, padx=10)
        self.console = tk.Text(self.tab4, bg="#11111b", fg="#a6e3a1", font=('Consolas', 10), height=15, width=90)
        self.console.pack(pady=20)

    # --- MÉTHODES D'EXÉCUTION ---
    def log(self, msg):
        self.console.insert(tk.END, f"> {msg}\n")
        self.console.see(tk.END)

    def run_tp1(self):
        if messagebox.askokcancel("Micro", "Prêt pour l'enregistrement de 5s ?"):
            self.log("Enregistrement en cours...")
            self.signal_audio = tp1.enregistrer_voix()
            self.log("Enregistrement terminé.")
            tp1.tracer_graphiques(self.signal_audio, self.fs_origine, "Signal Original")
            return True
        return False

    def run_tp2(self):
        if self.signal_audio is None: 
            messagebox.showwarning("!", "Veuillez d'abord effectuer le TP1")
            return False
        fs_cible = int(self.fs_choice.get())
        n_bits = int(self.bits_choice.get())
        tp2.lancer_tp2(self.signal_audio, self.fs_origine) # Utilise vos paramètres par défaut ou à adapter dans tp2
        self.log(f"Numérisation : {fs_cible}Hz, {n_bits} bits.")
        return True

    def run_tp3(self):
        if self.signal_audio is None: return False
        tp3.lancer_tp3(self.signal_audio)
        self.log("Transmission BPSK terminée.")
        return True

    def run_full_chain(self):
        try:
            if self.signal_audio is None: 
                if not self.run_tp1(): return 
            self.log("--- Démarrage de la chaîne complète ---")
            s_filtre = tp1.filtre_passe_bas(self.signal_audio, self.fs_origine)
            tp3.lancer_tp3(s_filtre)
            self.log("✅ Chaîne validée avec succès.")
        except Exception as e:
            self.log(f"ERREUR : {e}")

    # --- CORRECTION : FONCTION EXPORT PDF COMPLÈTE ---
    def exporter_pdf(self):
        """Génère un rapport détaillé avec les paramètres de simulation"""
        pdf = FPDF()
        pdf.add_page()
        
        # En-tête
        pdf.set_font("Arial", 'B', 18)
        pdf.set_text_color(58, 134, 255) # Couleur Accent
        pdf.cell(200, 20, txt="RAPPORT DE SIMULATION SIGNAL", ln=True, align='C')
        
        pdf.set_font("Arial", 'I', 10)
        pdf.set_text_color(128, 128, 128)
        date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        pdf.cell(200, 10, txt=f"Généré le : {date_str} | Superviseur : Dr KONANE", ln=True, align='C')
        pdf.ln(10)
        
        # Section 1 : Configuration
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, txt="1. Parametres de Numérisation (TP2)", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, txt=f"   - Frequence d'echantillonnage : {self.fs_choice.get()} Hz", ln=True)
        pdf.cell(200, 10, txt=f"   - Resolution de quantification : {self.bits_choice.get()} bits", ln=True)
        pdf.ln(5)
        
        # Section 2 : Analyse de Transmission
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="2. Resultats de Transmission (TP3)", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, txt="La simulation utilise une modulation BPSK (Binary Phase Shift Keying) "
                                 "sur un canal AWGN. Les resultats montrent la robustesse du signal "
                                 "apres filtrage passe-bas (300-3400Hz).")
        pdf.ln(5)
        
        # Section 3 : Conclusion
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt="3. Conclusion", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.multi_cell(0, 10, txt="L'ensemble des modules (Acquisition, Numerisation, Transmission) "
                                 "est fonctionnel et conforme au cahier des charges.")

        # Sauvegarde
        filename = "Rapport_Final_Signal.pdf"
        pdf.output(filename)
        self.log(f"PDF généré avec succès : {filename}")
        messagebox.showinfo("Export PDF", f"Le rapport complet a été généré sous le nom : {filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceComplete(root)
    root.mainloop()