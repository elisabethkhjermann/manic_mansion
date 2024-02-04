# Importere de nødvendige bibliotekene
import pygame as pg
import sys
import random
import math

# Konstanter
BREDDE = 800 # Bredden til vinduet
HØYDE = 800 # Høyden til vinduet
b = 30
h = 30
SIZE = (BREDDE, HØYDE) # Størrelsen til vinduet
# Frames Per Second (bilder per sekund)
FPS = 60
# Farger (RGB)
HVIT = (255, 255, 255) # Fargen på sauene
SVART = (0, 0, 0) # Fargen på hindringene
RØD = (255, 0, 0) # Fargen på mennesket
GRØNN = (0, 255, 0) # Fargen på bakgrunnen
BLÅ = (0, 0, 255) # Fargen på spøkelsene
MØRKEGRØNN = (0, 255, 100) # Fargen på frisonene
GRÅ = (172, 172, 172) # Fargen på poengsummen

# Initiere pygame
pg.init()
# Lager en overflate (surface) vi kan tegne på
bakgrunn = pg.display.set_mode(SIZE)
# Lager en klokke
klokke = pg.time.Clock()
# Variabel som styrer om spillet skal kjøres
font = pg.font.SysFont("Arial", 26)
run = True

class SpillObjekt:
    def __init__(self, x, y): 
        self.x = x
        self.y = y

        
class Spillbrett(SpillObjekt):
    def __init__(self):
        super().__init__(0, 0)
        
    def tegnBakgrunn(self, bakgrunn):
        bakgrunn.fill(GRØNN)
        pg.draw.rect(bakgrunn, MØRKEGRØNN, pg.Rect(0, 0, 100, 800))
        pg.draw.rect(bakgrunn, MØRKEGRØNN, pg.Rect(700, 0, 100, 800))
        
    def tegnObjekter(self, bakgrunn, x, y, b, h, farge):
        pg.draw.rect(bakgrunn, farge, pg.Rect(x, y, b, h))
    
    
class Menneske(SpillObjekt):
    def __init__(self, b, h, fart, poeng):
        # Arver x- og y-koordinater fra superklassen
        super().__init__(20, 300)
        self.b = b
        self.h = h
        self.fart = fart
        self.poeng = 0
        
    def plassering(self):
        # Sjekker kollisjon med høyre side av skjermen
        if x+b >= BREDDE:
            x = BREDDE - b # Sørger for at den ikke stikker av
        # Sjekker kollisjon med venstre side
        if x <= 0:
            x = 0

    def beveg(self, keys):
        vx, vy = 0, 0
        if keys[pg.K_LEFT]:
            vx = -self.speed
        if keys[pg.K_RIGHT]:
            vx = self.speed
        if keys[pg.K_UP]:
            vy = -self.speed
        if keys[pg.K_DOWN]:
            vy = self.speed
        self.rect.move_ip(vx, vy)
        
    def reduserFart(self):
        if bærerSau is True:
            self.fart = 2.5
        else:
            self.speed = 4
    
    def økPoeng(self):
        self.poeng += 1
        
    def sjekkKollisjon(self, annet):
        return (
            self.x < annet.x + annet.b
            and self.x + self.b > annet.x
            and self.y < annet.y + annet.h
            and self.y + self.h > annet.y)

class Hindring(SpillObjekt):
    def __init__(self, x, y, b, h):
        super().__init__(x, y)
        self.b = b
        self.h = h
        
class Spøkelse(SpillObjekt):
    def __init__(self, b, h, fart):
        super().__init__(random.randint(110, 660), random.randint(10, 760))
        self.b = b
        self.h = h
        self.fart = fart
        self.vinkel = random.randint(0, 360)
        
    def endreRetning(self):
        vinkel_rad = math.radians(self.vinkel)
        delta_x, delta_y = self.fart * math.cos(vinkel_rad), self.fart * math.sin(vinkel_rad)
        self.x += delta_x
        self.y += delta_y
        
        if self.x + self.b >= 700 or self.x <= 700:
            self.vinkel = 180 - self.vinkel
            
        if self.y + self.h >= 800 or self.y <= 0:
            self.vinkel = 360 - self.vinkel
            
class Sau(SpillObjekt):
    def __init__(self, x, y, b, h):
        super().__init__(x, y)
        self.b = b
        self.h = h
        
def lagObjekter(antallObjekter, xRange, yRange, b, h, obj_class, minAvstand = 50):
    objekter = []
    for i in range (antallObjekter):
        x = random.randint(*xRange)
        y = random.randint(*yRange)
        # Sjekker oom det valgte stedet overlapper med eksisterende objekter
        while any(
            (obj.x - minAvstand <= x <= obj.x + obj.b + minAvstand and
             obj.y - minAvstand <= y <= obj.x + obj.b + minAvstand)
            for obj in objekter
        ):
            x = random.randint(*xRange)
            y = random.randint(*yRange)
        
        obj = obj_class(x, y, b, h)
        objekter.append(obj)
        
        return objekter


# Starter spillet med å lage 3 hindringer og 3 sauer
hindringer = lagObjekter(3, (110, 660), (10, 760), b, h, Hindring)
saueListe = lagObjekter(3, (700, 770), (20, 750), b, h, Sau)

# Skriver inn poensummen på spillbrettet
def visPoeng(poeng):
    tekst_img = font.render(f"Poengsum: {poeng}", True, GRÅ)
    bakgrunn.blit(text_img, (10, 20))

# Definerer spillbrettet
spillbrett = Spillbrett()

# Definerer spilleren og spøkelse. antallSpøkelser bruker jeg for å senere
menneske = Menneske(b, h, 4, 0)
antallSpøkelser = menneske.poeng + 1
spøkelser = [Spøkelse(b, h, 4) for i in range(antallSpøkelser)]


# Spill-løkken
while run:
    # Går gjennom hendelser (events)
    for event in pg.event.get():
        # Sjekker om vi ønsker å lukke vinduet
        if event.type == pg.QUIT:
            run = False # Spillet skal avsluttes

    # Tegner bakgrunnen
    spillbrett.tegnBakgrunn(bakgrunn)
    # Går gjennom alle spøkelsene i listen og sjekker om den kolliderer.
    # Da avsluttes spillet
    for spøkelse in spøkelser:
        if menneske.sjekkKollisjon(spøkelse):
            run = False
        spøkelse.endreRetning()
        spillbrett.tegnObjekter(bakgrunn, spøkelse.x, spøkelse.y, b, h, BLÅ)
        
    for hindring in hindringer:
        spillbrett.tegnObjekter(bakgrunn, hindring.x, hindring.y, b, h, SVART)
        
    for sau in saueListe:
        spillbrett.tegnObjekter(bakgrunn, sau.x, sau.y, b, h, HVIT)
        if menneske.sjekkKollisjon(sau):
            saueListe.remove(sau)
            bærerSau = True
            menneske.reduserFart()
            
    spillbrett.tegnObjekter(bakgrunn, spøkelse.x, spøkelse.y, b, h, BLÅ)
    
    if bærerSau is True:
        menneske.reduserFart()
        spillbrett.tegnObjekter(bakgrunn, menneske.x, menneske.y, b, h, HVIT)
    else:
        spillbrett.tegnObjekter(bakgrunn, menneske.x, menneske.y, b, h, RØD)
    

    # "Flipper" displayet for å vise hva vi har tegnet
    pg.display.flip()


# Avslutter pygame
pg.quit()
sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()