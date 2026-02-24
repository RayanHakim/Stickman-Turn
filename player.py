import pygame
import math
import settings
from weapon import WEAPONS

class Player:
    def __init__(self, x, color, name, is_bot=False): 
        self.x = x
        self.y = 0 
        self.color = color
        self.name = name
        self.hp = settings.MAX_HP
        self.fuel = settings.MAX_FUEL
        
        self.angle = 45 
        self.power = 50
        self.facing_right = True
        
        self.weapon_idx = 0 
        self.is_bot = is_bot       
        self.bot_timer = 0         

    def switch_weapon(self):
        self.weapon_idx = (self.weapon_idx + 1) % len(WEAPONS)
        
    def get_current_weapon(self):
        return WEAPONS[self.weapon_idx]

    def move(self, dx, terrain):
        if self.fuel > 0:
            self.x += dx
            self.fuel -= abs(dx)
            # Batasnya sekarang adalah MAP_WIDTH, bukan WIDTH layar
            self.x = max(20, min(settings.MAP_WIDTH - 20, self.x))
            if dx > 0: self.facing_right = True
            elif dx < 0: self.facing_right = False

    def update(self, terrain):
        ground_y = terrain.get_y(self.x)
        self.y = ground_y - 25 

    def draw(self, screen, camera_x):
        screen_x = self.x - camera_x
        
        # Stickman Body
        pygame.draw.circle(screen, self.color, (int(screen_x), int(self.y - 20)), 10)
        pygame.draw.line(screen, self.color, (screen_x, self.y - 10), (screen_x, self.y + 10), 2)
        pygame.draw.line(screen, self.color, (screen_x, self.y + 10), (screen_x - 10, self.y + 25), 2)
        pygame.draw.line(screen, self.color, (screen_x, self.y + 10), (screen_x + 10, self.y + 25), 2)

        rad_angle = math.radians(self.angle)
        if not self.facing_right: rad_angle = math.pi - rad_angle
        
        gun_len = 30
        end_x = screen_x + math.cos(rad_angle) * gun_len
        end_y = self.y - math.sin(rad_angle) * gun_len
        
        # Menggambar Senjata
        wpn_name = self.get_current_weapon()["name"]
        if wpn_name == "BAZOOKA":
            pygame.draw.line(screen, (50, 100, 50), (screen_x, self.y), (end_x, end_y), 8)
        elif wpn_name == "SNIPER":
            pygame.draw.line(screen, (20, 20, 20), (screen_x, self.y), (screen_x + math.cos(rad_angle)*45, self.y - math.sin(rad_angle)*45), 3)
            scope_x = screen_x + math.cos(rad_angle)*15 - math.sin(rad_angle)*8
            scope_y = self.y - math.sin(rad_angle)*15 - math.cos(rad_angle)*8
            pygame.draw.circle(screen, (100, 100, 100), (int(scope_x), int(scope_y)), 4)
        elif wpn_name == "HEAVY BOMB":
            pygame.draw.circle(screen, (150, 0, 0), (int(end_x), int(end_y)), 8)
            pygame.draw.line(screen, self.color, (screen_x, self.y), (end_x, end_y), 2)
        elif wpn_name == "TRIPLE SHOT":
            pygame.draw.line(screen, (200, 100, 0), (screen_x, self.y), (end_x, end_y), 5)
            pygame.draw.line(screen, (200, 100, 0), (screen_x, self.y), (screen_x + math.cos(rad_angle+0.2)*20, self.y - math.sin(rad_angle+0.2)*20), 3)
            pygame.draw.line(screen, (200, 100, 0), (screen_x, self.y), (screen_x + math.cos(rad_angle-0.2)*20, self.y - math.sin(rad_angle-0.2)*20), 3)
        elif wpn_name == "WIND RIDER":
            pygame.draw.line(screen, (200, 255, 255), (screen_x, self.y), (end_x, end_y), 5)

        # HP Bar
        pygame.draw.rect(screen, (255,0,0), (screen_x - 20, self.y - 45, 40, 5))
        hp_width = (self.hp / settings.MAX_HP) * 40
        pygame.draw.rect(screen, (0,255,0), (screen_x - 20, self.y - 45, hp_width, 5))
        
        if self.is_bot:
            font = pygame.font.SysFont("arial", 12, bold=True)
            txt = font.render("BOT", True, (200,200,200))
            screen.blit(txt, (screen_x - 12, self.y - 60))