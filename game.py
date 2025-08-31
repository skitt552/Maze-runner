
# ==============================
#  MAZE FPS GAME - WEB VERSION
#  Pygbag compatible for iOS/Browser
# ==============================
import pygame, random, os, json

pygame.init()

WIDTH, HEIGHT = 1280, 720
FPS = 60
WHITE=(255,255,255); BLACK=(0,0,0); RED=(255,0,0); GREEN=(0,255,0); BLUE=(0,0,255); YELLOW=(255,255,0)

SAVE_FILE="savegame.json"; ACH_FILE="achievements.json"
default_save={"level":1,"xp":0,"cash":0,"megabucks":0,"guns":["Pistol_Common","Rifle_Common"],"grenades":3,
"settings":{"master_volume":0.8,"music_volume":0.3,"sfx_volume":0.8,"fov":70}}
default_achievements={"first_boss":False,"level10":False,"legendary_gun":False,"millionaire":False}

def load_json(file,default):
    if os.path.exists(file):
        try:
            with open(file,"r") as f: return json.load(f)
        except: pass
    return default.copy()
def save_json(file,data):
    with open(file,"w") as f: json.dump(data,f,indent=2)

save_data=load_json(SAVE_FILE,default_save)
achievements=load_json(ACH_FILE,default_achievements)

def load_sound(path):
    try:
        if os.path.exists(path): return pygame.mixer.Sound(path)
    except: pass
    return None
sounds={
 "gunshot":load_sound("sounds/gunshot.wav"),
 "reload":load_sound("sounds/reload.wav"),
 "grenade":load_sound("sounds/grenade.wav"),
 "explosion":load_sound("sounds/explosion.wav"),
 "shop":load_sound("sounds/shop.wav"),
 "boss":load_sound("sounds/boss.wav"),
 "levelup":load_sound("sounds/levelup.wav"),
}
if os.path.exists("sounds/music.wav"):
    pygame.mixer.music.load("sounds/music.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

class Player:
    def __init__(self):
        self.level=save_data["level"]; self.xp=save_data["xp"]
        self.cash=save_data["cash"]; self.megabucks=save_data["megabucks"]
        self.guns=save_data["guns"]; self.grenades=save_data["grenades"]
        self.health=100; self.max_health=100
        self.fov=save_data["settings"]["fov"]
        self.master_volume=save_data["settings"]["master_volume"]
        self.music_volume=save_data["settings"]["music_volume"]
        self.sfx_volume=save_data["settings"]["sfx_volume"]
        self.recoil=True; self.luck=1.0; self.aimbot=False; self.wallhack=False; self.neon_mode=False
    def add_xp(self,amt):
        self.xp+=amt
        while self.xp>=self.level*100:
            self.xp-=self.level*100; self.level+=1; self.megabucks+=5
            if sounds["levelup"]: sounds["levelup"].play()
    def take_damage(self,amt):
        self.health-=amt
        if self.health<=0: self.health=0; print("You died!")

class Enemy:
    def __init__(self,boss=False,round_num=1):
        self.boss=boss
        self.health=50+round_num*10; self.damage=10+round_num*2
        if boss: self.health=500+round_num*100; self.damage=50+round_num*10
    def drop_cash(self):
        if self.boss: return 100000
        return int(random.randint(100,5000)*player.luck)

player=Player()

round_num=1; enemies=[]; cheats_enabled=False
cheat_unlocked=False; cheat_code="skitzcraz0211"; cheat_input=""

screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Maze FPS Web")
clock=pygame.time.Clock()
font=pygame.font.SysFont("Arial",24)

def draw_cheat_menu():
    menu=["CHEAT MENU","1) Toggle Aimbot","2) Toggle Wallhack","3) Toggle No Recoil","4) Boost Luck","5) Neon Mode","6) FOV+10"]
    for i,t in enumerate(menu): screen.blit(font.render(t,True,RED if i==0 else WHITE),(50,50+i*30))

def draw_hud():
    hp_txt=font.render(f"HP: {player.health}/{player.max_health}",True,WHITE)
    cash_txt=font.render(f"Cash: ${player.cash}",True,YELLOW)
    xp_txt=font.render(f"XP: {player.xp}/{player.level*100}",True,GREEN)
    lvl_txt=font.render(f"Lvl: {player.level}  MBucks:{player.megabucks}",True,BLUE)
    screen.blit(hp_txt,(20,20)); screen.blit(cash_txt,(20,50))
    screen.blit(xp_txt,(20,80)); screen.blit(lvl_txt,(20,110))

running=True; cheat_menu_open=False
while running:
    screen.fill(BLACK if not player.neon_mode else (0,255,200))
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE: pass
            if event.key==pygame.K_p:
                cheat_input=""; cheat_unlocked=False; print("Type cheat code now...")
            if event.key==pygame.K_INSERT and cheat_unlocked: cheat_menu_open=not cheat_menu_open
            if event.key==pygame.K_RETURN and cheat_input==cheat_code:
                cheat_unlocked=True; print("Cheats Unlocked!")
            if event.unicode.isprintable(): cheat_input+=event.unicode
            if cheat_menu_open:
                if event.key==pygame.K_1: player.aimbot=not player.aimbot
                if event.key==pygame.K_2: player.wallhack=not player.wallhack
                if event.key==pygame.K_3: player.recoil=not player.recoil
                if event.key==pygame.K_4: player.luck*=1.5
                if event.key==pygame.K_5: player.neon_mode=not player.neon_mode
                if event.key==pygame.K_6: player.fov=min(100,player.fov+10)
    draw_hud()
    if cheat_menu_open: draw_cheat_menu()
    pygame.display.flip(); clock.tick(FPS)
