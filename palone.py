import math
import arcade
import random
import json
import os

LARGHEZZA = 800
ALTEZZA = 600
RAGGIO = 20
VELOCITA_MAX = 5

class Pallina:
    def __init__(self, x, y, vx, vy, colore):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.colore = colore 
    
    def aggiorna(self):
        self.x += self.vx
        self.y += self.vy
        
        # Rimbalzo sui bordi
        if self.x - RAGGIO < 0 or self.x + RAGGIO > LARGHEZZA:
            self.vx *= -1
            self.x = max(RAGGIO, min(self.x, LARGHEZZA - RAGGIO))
        
        if self.y - RAGGIO < 0 or self.y + RAGGIO > ALTEZZA:
            self.vy *= -1
            self.y = max(RAGGIO, min(self.y, ALTEZZA - RAGGIO))
    
    def disegna(self):
        arcade.draw_circle_filled(self.x, self.y, RAGGIO, self.colore)
    
    def controlla_collisione(self, altra):
        dx = self.x - altra.x
        dy = self.y - altra.y
        distanza = (dx**2 + dy**2)**0.5
        
        if distanza < RAGGIO * 2:
            self.vx, altra.vx = altra.vx, self.vx
            self.vy, altra.vy = altra.vy, self.vy
            
            offset = (RAGGIO * 2 - distanza) / 2 + 1
            self.x += offset * (dx / distanza)
            self.y += offset * (dy / distanza)
            altra.x -= offset * (dx / distanza)
            altra.y -= offset * (dy / distanza)
    
    def to_dict(self):
        # Converte la pallina in un dizionario (per JSON)
        return {
            'x': self.x,
            'y': self.y,
            'vx': self.vx,
            'vy': self.vy,
            'colore': list(self.colore)  # JSON vuole liste, non tuple (le tuple le vedremo, pensale come liste ma "costanti")
        }
    

def crea_pallina_da_dizionario(dati):
    """Ricrea una pallina da un dizionario"""
    return Pallina(
        dati['x'],
        dati['y'],
        dati['vx'],
        dati['vy'],
        tuple(dati['colore'])  # Riconvertiamo in tupla
    )
class GiocoPalline(arcade.Window):
    def __init__(self):
        super().__init__(LARGHEZZA, ALTEZZA, "Palline")
        self.palline = []
        arcade.set_background_color(arcade.color.BLACK)
    
    def on_draw(self):
        self.clear()
        
        for pallina in self.palline:
            pallina.disegna()
        
        # Istruzioni
        arcade.draw_text(
            "Click: Aggiungi | S: Salva JSON | L: Carica JSON",
            10, ALTEZZA - 30, arcade.color.WHITE, 14
        )
        arcade.draw_text(
            f"Palline: {len(self.palline)}",
            10, ALTEZZA - 55, arcade.color.YELLOW, 14
        )
    
    def on_update(self, delta_time):
        for pallina in self.palline:
            pallina.aggiorna()
        
        for i in range(len(self.palline)):
            for j in range(i + 1, len(self.palline)):
                self.palline[i].controlla_collisione(self.palline[j])
    
    def on_mouse_press(self, x, y, button, modifiers):
        colore = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )
        vx = random.uniform(-VELOCITA_MAX, VELOCITA_MAX) # Numero a caso tra i due estremi
        vy = random.uniform(-VELOCITA_MAX, VELOCITA_MAX)
        
        self.palline.append(Pallina(x, y, vx, vy, colore))
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.S:
            self.salva_json()
        elif key == arcade.key.L:
            self.carica_json()
    
    def salva_json(self):
        nome_file = "palline.json"
        
        try:
            # Converti ogni pallina in un dizionario
            dati = []
            
            for p in self.palline:
                dati.append(p.to_dict())
            
            with open(nome_file, 'w', encoding='utf-8') as f:
                # indent=4 rende il JSON leggibile (con indentazione)
                json.dump(dati, f, indent=4)
            
            print(f"Salvate {len(self.palline)} palline in '{nome_file}'")
        
        except Exception as e:
            print(f"Errore JSON: {e}")
    
    def carica_json(self):
        nome_file = "palline.json"
        
        if not os.path.exists(nome_file):
            print(f"File '{nome_file}' non trovato! Salva prima con S.")
            return
        
        # Questo costrutto "try"/"except" non l'abbiamo ancora visto... Per te cosa fa?
        try:
            with open(nome_file, 'r', encoding='utf-8') as f:
                dati = json.load(f)
            
            # Ricostruisci le palline dai dizionari
            self.palline = []
            
            for d in dati:
                self.palline.append(crea_pallina_da_dizionario(d))

            print(f"Caricate {len(self.palline)} palline")
        
        except json.JSONDecodeError as e:
            print(f"JSON corrotto! Errore alla linea {e.lineno}: {e.msg}")
        except Exception as e:
            print(f"Errore caricamento JSON: {e}")


def main():
    gioco = GiocoPalline()
    arcade.run()

if __name__ == "__main__":
    main()
