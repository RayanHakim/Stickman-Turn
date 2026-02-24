import pygame
import sys
import os  # Ditambahkan untuk membaca file audio
import random
import math
import settings
from terrain import Terrain
from player import Player
from weapon import Projectile, WEAPONS

pygame.init()
pygame.mixer.init() # Inisialisasi Mesin Audio

# --- PENGATURAN AUDIO (BGM LOOP) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
bg_music_path = os.path.join(BASE_DIR, "bg_music.mp3") 

if os.path.exists(bg_music_path):
    try:
        pygame.mixer.music.load(bg_music_path)
        pygame.mixer.music.set_volume(0.4) # Volume 40% agar tidak menutupi efek ledakan
        pygame.mixer.music.play(-1) # Angka -1 agar lagu mengulang terus (loop sampai kiamat)
    except Exception as e:
        print(f"Gagal memutar musik: {e}")

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Stickman Turn")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsansms", 20)
big_font = pygame.font.SysFont("comicsansms", 50)

def draw_button(rect, text, mouse_pos, base_color, hover_color):
    color = hover_color if rect.collidepoint(mouse_pos) else base_color
    pygame.draw.rect(screen, color, rect, border_radius=10)
    txt_surf = font.render(text, True, (255,255,255))
    screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))

def main_menu():
    while True:
        screen.fill((10, 10, 30))
        title = big_font.render("STICKMAN TURN", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(settings.WIDTH/2, 120)))

        mx, my = pygame.mouse.get_pos()
        btn_play = pygame.Rect(settings.WIDTH/2 - 100, 220, 200, 50)
        btn_info = pygame.Rect(settings.WIDTH/2 - 100, 290, 200, 50)
        btn_help = pygame.Rect(settings.WIDTH/2 - 100, 360, 200, 50)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: click = True

        draw_button(btn_play, "PLAY", (mx, my), (30, 150, 30), (50, 200, 50))
        draw_button(btn_info, "INFO SENJATA", (mx, my), (30, 100, 180), (50, 150, 220))
        draw_button(btn_help, "HOW TO PLAY", (mx, my), (120, 30, 150), (180, 50, 200))

        if click:
            if btn_play.collidepoint((mx, my)): return "PLAY"
            if btn_info.collidepoint((mx, my)): return "INFO"
            if btn_help.collidepoint((mx, my)): return "HELP"
        pygame.display.update()

def info_menu():
    while True:
        screen.fill((20, 30, 40))
        title = big_font.render("WEAPON STATS", True, (255, 215, 0))
        screen.blit(title, title.get_rect(center=(settings.WIDTH/2, 50)))

        mx, my = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: click = True

        btn_back = pygame.Rect(20, 20, 100, 40)
        draw_button(btn_back, "BACK", (mx, my), (150, 30, 30), (200, 50, 50))

        y_offset = 120
        for w in WEAPONS:
            name_txt = font.render(f"[{w['name']}]", True, (0, 255, 255))
            stats_txt = font.render(f"Damage: {w['dmg']} | Blast Area: {w['blast']} | Speed: {w['speed']} | Peluru: {w['count']}", True, (200, 200, 200))
            desc = ""
            if w["name"] == "SNIPER": desc = "-> Cepat, Akurat, Mengabaikan Angin, Area Ledakan Kecil"
            elif w["name"] == "HEAVY BOMB": desc = "-> Sangat Berat, Bikin Kawah Raksasa, Butuh Power Tinggi"
            elif w["name"] == "TRIPLE SHOT": desc = "-> Menembakkan 3 Peluru menyebar"
            elif w["name"] == "WIND RIDER": desc = "-> Ringan, Sangat dipengaruhi arah angin"
            else: desc = "-> Senjata standar dan seimbang"
            desc_txt = font.render(desc, True, (150, 150, 150))
            
            screen.blit(name_txt, (100, y_offset))
            screen.blit(stats_txt, (100, y_offset + 25))
            screen.blit(desc_txt, (100, y_offset + 50))
            y_offset += 90

        if click and btn_back.collidepoint((mx, my)): return
        pygame.display.update()

def how_to_play_menu():
    while True:
        screen.fill((20, 30, 40))
        title = big_font.render("HOW TO PLAY", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(settings.WIDTH/2, 80)))

        mx, my = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: click = True

        btn_back = pygame.Rect(20, 20, 100, 40)
        draw_button(btn_back, "BACK", (mx, my), (150, 30, 30), (200, 50, 50))

        instructions = [
            "Ini adalah game Tembak-tembakan Bergiliran (Turn-Based).",
            "  - [KIRI] / [KANAN] : Berjalan (Butuh Bensin/Fuel)",
            "  - [ATAS] / [BAWAH]: Mengatur Sudut Tembakan",
            "  - [W] / [S]        : Mengatur Kekuatan (Power)",
            "  - [TAB]            : Mengganti Senjata (Cek Info!)",
            "  - [SPASI]          : TEMBAK!",
            "  - [P] / [ESC]      : Membuka Menu Pause",
            "",
            "Perhatikan arah ANGIN di pojok kanan atas!",
            "Semakin berat senjatamu, semakin sulit tertiup angin."
        ]
        for i, line in enumerate(instructions):
            col = (255, 215, 0) if "Tembak" in line else (200, 200, 200)
            screen.blit(font.render(line, True, col), (100, 180 + (i * 30)))

        if click and btn_back.collidepoint((mx, my)): return
        pygame.display.update()

def mode_select_menu():
    while True:
        screen.fill((10, 20, 40))
        title = big_font.render("SELECT MODE", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(settings.WIDTH/2, 150)))

        mx, my = pygame.mouse.get_pos()
        btn_1v1 = pygame.Rect(settings.WIDTH/2 - 100, 250, 200, 50)
        btn_bot = pygame.Rect(settings.WIDTH/2 - 100, 320, 200, 50)
        btn_back = pygame.Rect(20, 20, 100, 40)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: click = True

        draw_button(btn_1v1, "1 VS 1 (LOKAL)", (mx, my), (30, 150, 30), (50, 200, 50))
        draw_button(btn_bot, "1 VS BOT (AI)", (mx, my), (150, 80, 20), (200, 120, 40))
        draw_button(btn_back, "BACK", (mx, my), (150, 30, 30), (200, 50, 50))

        if click:
            if btn_back.collidepoint((mx, my)): return None
            if btn_1v1.collidepoint((mx, my)): return "1v1"
            if btn_bot.collidepoint((mx, my)): return "bot"
        pygame.display.update()

def map_select_menu():
    maps = ["HILL", "SNOW", "MOON", "DESERT", "VOLCANO"]
    while True:
        screen.fill((20, 40, 30))
        title = big_font.render("SELECT MAP", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(settings.WIDTH/2, 60)))

        mx, my = pygame.mouse.get_pos()
        btn_back = pygame.Rect(20, 20, 100, 40)
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: click = True

        draw_button(btn_back, "BACK", (mx, my), (150, 30, 30), (200, 50, 50))
        if click and btn_back.collidepoint((mx, my)): return None

        for i, name in enumerate(maps):
            btn_rect = pygame.Rect(settings.WIDTH/2 - 150, 140 + i * 75, 300, 50)
            draw_button(btn_rect, name, (mx, my), (50, 80, 100), (80, 120, 150))
            if click and btn_rect.collidepoint((mx, my)): return i + 1
            
        pygame.display.update()

def draw_in_game_ui(screen, player, wind):
    overlay = pygame.Surface((settings.WIDTH, 90))
    overlay.fill((255, 255, 255))
    overlay.set_alpha(180)
    screen.blit(overlay, (0, 0))

    txt_turn = font.render(f"GILIRAN: {player.name} {'(BOT)' if player.is_bot else ''}", True, player.color)
    txt_wpn = font.render(f"WEAPON: {player.get_current_weapon()['name']}", True, (200, 0, 0))
    screen.blit(txt_turn, (20, 10))
    screen.blit(txt_wpn, (20, 40))

    info1 = font.render(f"POWER: {int(player.power)}   ANGLE: {int(player.angle)}", True, settings.TEXT_COLOR)
    info2 = font.render(f"FUEL: {int(player.fuel)}", True, (200, 100, 0))
    screen.blit(info1, (350, 10))
    screen.blit(info2, (350, 40))

    wind_dir = ">>" if wind > 0 else "<<"
    txt_wind = font.render(f"ANGIN: {abs(wind)} {wind_dir}", True, (100, 100, 255))
    screen.blit(txt_wind, (settings.WIDTH - 250, 25))

# --- GAME LOOP UTAMA ---
def run_game(mode, map_idx):
    terrain = Terrain(map_idx)
    
    # Spawn Pemain berjauhan (Di ujung kiri dan ujung kanan Peta)
    p1 = Player(150, settings.P1_COLOR, "PLAYER 1", is_bot=False)
    p2 = Player(settings.MAP_WIDTH - 150, settings.P2_COLOR, "PLAYER 2", is_bot=(mode == "bot"))
    p2.facing_right = False
    p2.angle = 135 
    
    players = [p1, p2]
    turn_idx = 0
    
    active_projectiles = []
    explosion_points = []   
    explosion_timer = 0
    wind = random.randint(-5, 5) 
    
    game_state = "AIMING" 
    is_paused = False 
    
    btn_pause = pygame.Rect(settings.WIDTH - 60, 25, 40, 40)
    camera_x = 0 # Variabel inti untuk sistem kamera

    while True:
        clock.tick(settings.FPS)
        current_player = players[turn_idx]
        opponent = players[1 - turn_idx]
        fire_triggered = False
        
        mx, my = pygame.mouse.get_pos()
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: click = True
            
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_p):
                    is_paused = not is_paused
                
                if not is_paused and game_state == "AIMING" and not current_player.is_bot:
                    if event.key == pygame.K_TAB: current_player.switch_weapon()
                    elif event.key == pygame.K_SPACE: fire_triggered = True

        if not is_paused and click and btn_pause.collidepoint((mx, my)):
            is_paused = True

        # --- LOGIKA BERJALAN JIKA TIDAK PAUSE ---
        if not is_paused:
            # 1. LOGIKA SCROLLING KAMERA (SINEMATIK)
            target_x = current_player.x
            # Kalau ada peluru terbang, kamera fokus mengejar peluru!
            if game_state == "FIRING" and len(active_projectiles) > 0:
                target_x = active_projectiles[0].x
            # Kalau meledak, kamera fokus ke ledakan!
            elif game_state == "EXPLODING" and len(explosion_points) > 0:
                target_x = explosion_points[0][0]

            ideal_camera_x = target_x - (settings.WIDTH / 2)
            ideal_camera_x = max(0, min(settings.MAP_WIDTH - settings.WIDTH, ideal_camera_x))
            camera_x += (ideal_camera_x - camera_x) * 0.1 # Pergerakan kamera mulus

            # 2. STATE AIMING
            if game_state == "AIMING":
                if current_player.is_bot:
                    current_player.bot_timer += 1
                    if current_player.bot_timer > 90:
                        current_player.bot_timer = 0
                        dx = opponent.x - current_player.x
                        current_player.facing_right = (dx > 0)
                        if random.random() < 0.3: current_player.weapon_idx = random.randint(0, 4)
                        
                        dist = abs(dx)
                        current_player.angle = random.randint(35, 55)
                        wind_effect = wind if current_player.facing_right else -wind
                        
                        wpn_grav = current_player.get_current_weapon()["grav"]
                        calc_power = (dist / 8.5) * (wpn_grav/0.5) - (wind_effect * 1.5)
                        current_player.power = max(10, min(100, int(calc_power)))
                        fire_triggered = True
                else:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_LEFT]: current_player.move(-settings.MOVE_SPEED, terrain)
                    if keys[pygame.K_RIGHT]: current_player.move(settings.MOVE_SPEED, terrain)
                    if keys[pygame.K_UP]: current_player.angle = min(90, current_player.angle + 1)
                    if keys[pygame.K_DOWN]: current_player.angle = max(0, current_player.angle - 1)
                    if keys[pygame.K_w]: current_player.power = min(100, current_player.power + 1)
                    if keys[pygame.K_s]: current_player.power = max(10, current_player.power - 1)
                
                current_player.update(terrain) 
                opponent.update(terrain)

                if fire_triggered:
                    game_state = "FIRING"
                    wpn_data = current_player.get_current_weapon()
                    shot_angle = current_player.angle
                    if not current_player.facing_right: shot_angle = 180 - current_player.angle
                    
                    for i in range(wpn_data["count"]):
                        spread_offset = 0
                        if wpn_data["count"] > 1:
                            spread_offset = (i - (wpn_data["count"]//2)) * wpn_data["spread"]
                        
                        proj = Projectile(current_player.x, current_player.y - 20, shot_angle + spread_offset, current_player.power, wind, wpn_data)
                        active_projectiles.append(proj)

            # 3. STATE FIRING
            elif game_state == "FIRING":
                for proj in active_projectiles[:]: 
                    status = proj.update()
                    coll = proj.check_collision(terrain, players)
                    
                    if status == "MISS":
                        active_projectiles.remove(proj)
                    elif coll:
                        explosion_points.append((int(proj.x), int(proj.y), proj.weapon["blast"]))
                        explosion_timer = 20 
                        terrain.explode(proj.x, proj.weapon["blast"])
                        
                        for p in players:
                            dist = math.hypot(proj.x - p.x, proj.y - p.y)
                            if dist < proj.weapon["blast"] + 20:
                                dmg = int((1 - (dist / (proj.weapon["blast"]+20))) * proj.weapon["dmg"])
                                p.hp -= max(0, dmg)
                                
                        active_projectiles.remove(proj)
                
                if len(active_projectiles) == 0:
                    if explosion_timer > 0: game_state = "EXPLODING"
                    else: game_state = "NEXT_TURN"

            elif game_state == "EXPLODING":
                explosion_timer -= 1
                if explosion_timer <= 0:
                    explosion_points.clear()
                    game_state = "NEXT_TURN"

            elif game_state == "NEXT_TURN":
                if p1.hp <= 0 or p2.hp <= 0: game_state = "GAMEOVER"
                else:
                    turn_idx = 1 - turn_idx
                    players[turn_idx].fuel = settings.MAX_FUEL 
                    wind = random.randint(-8, 8) 
                    game_state = "AIMING"

        # --- MENGGAMBAR LAYAR (Termasuk offset Kamera) ---
        screen.fill(terrain.bg_color)
        terrain.draw(screen, camera_x)
        for p in players: p.draw(screen, camera_x)
        for proj in active_projectiles: proj.draw(screen, camera_x)
        
        if game_state == "EXPLODING":
            for ex, ey, rad in explosion_points:
                screen_ex = int(ex - camera_x)
                pygame.draw.circle(screen, (255, 200, 50), (screen_ex, ey), rad)
                pygame.draw.circle(screen, (255, 100, 0), (screen_ex, ey), rad - 10)

        draw_in_game_ui(screen, players[turn_idx], wind)

        pygame.draw.rect(screen, (80, 80, 80), btn_pause, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), (settings.WIDTH - 48, 32, 6, 26)) 
        pygame.draw.rect(screen, (255, 255, 255), (settings.WIDTH - 36, 32, 6, 26)) 

        if is_paused:
            overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0,0,0, 180)) 
            screen.blit(overlay, (0,0))
            
            title = big_font.render("GAME PAUSED", True, (255, 255, 255))
            screen.blit(title, title.get_rect(center=(settings.WIDTH/2, 150)))
            
            btn_resume = pygame.Rect(settings.WIDTH/2 - 100, 250, 200, 50)
            btn_restart = pygame.Rect(settings.WIDTH/2 - 100, 320, 200, 50)
            btn_menu = pygame.Rect(settings.WIDTH/2 - 100, 390, 200, 50)
            
            draw_button(btn_resume, "RESUME", (mx, my), (30, 150, 30), (50, 200, 50))
            draw_button(btn_restart, "RESTART", (mx, my), (150, 100, 30), (200, 150, 50))
            draw_button(btn_menu, "MAIN MENU", (mx, my), (150, 30, 30), (200, 50, 50))
            
            if click:
                if btn_resume.collidepoint((mx, my)): is_paused = False
                elif btn_restart.collidepoint((mx, my)): return "RESTART"
                elif btn_menu.collidepoint((mx, my)): return "MENU"

        if game_state == "GAMEOVER":
            winner = "PLAYER 1" if p2.hp <= 0 else ("BOT" if mode=="bot" else "PLAYER 2")
            win_color = settings.P1_COLOR if p2.hp <= 0 else settings.P2_COLOR
            
            overlay = pygame.Surface((settings.WIDTH, settings.HEIGHT))
            overlay.fill((0,0,0)); overlay.set_alpha(150); screen.blit(overlay, (0,0))
            
            txt = big_font.render(f"{winner} WINS!", True, win_color)
            screen.blit(txt, txt.get_rect(center=(settings.WIDTH/2, settings.HEIGHT/2 - 30)))
            
            sub1 = font.render("Press [R] to Restart", True, (255,255,255))
            sub2 = font.render("Press [M] to Main Menu", True, (255,255,255))
            screen.blit(sub1, sub1.get_rect(center=(settings.WIDTH/2, settings.HEIGHT/2 + 40)))
            screen.blit(sub2, sub2.get_rect(center=(settings.WIDTH/2, settings.HEIGHT/2 + 70)))
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_m]: return "MENU"
            if keys[pygame.K_r]: return "RESTART"

        pygame.display.update()

if __name__ == "__main__":
    while True:
        action = main_menu()
        if action == "PLAY":
            mode = mode_select_menu()
            if mode:
                map_idx = map_select_menu()
                if map_idx:
                    while True:
                        result = run_game(mode, map_idx)
                        if result != "RESTART": 
                            break 
        elif action == "INFO":
            info_menu()
        elif action == "HELP":
            how_to_play_menu()