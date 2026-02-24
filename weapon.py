import pygame
import math
import settings

# --- DATABASE 5 SENJATA ---
# Heavy Bomb diperbaiki: Speed dinaikkan ke 0.50, Gravitasi dikurangi ke 0.5 biar bisa dilempar
WEAPONS = [
    {"name": "BAZOOKA",     "color": (50, 50, 50),  "radius": 6,  "speed": 0.40, "blast": 45, "dmg": 40, "grav": 0.5, "wind": 0.01,  "count": 1, "spread": 0},
    {"name": "SNIPER",      "color": (10, 10, 10),  "radius": 3,  "speed": 0.85, "blast": 15, "dmg": 60, "grav": 0.1, "wind": 0.00,  "count": 1, "spread": 0},
    {"name": "HEAVY BOMB",  "color": (150, 0, 0),   "radius": 12, "speed": 0.50, "blast": 90, "dmg": 80, "grav": 0.5, "wind": 0.005, "count": 1, "spread": 0}, 
    {"name": "TRIPLE SHOT", "color": (200, 100, 0), "radius": 4,  "speed": 0.35, "blast": 25, "dmg": 20, "grav": 0.5, "wind": 0.01,  "count": 3, "spread": 12},
    {"name": "WIND RIDER",  "color": (255, 255, 255),"radius": 5, "speed": 0.30, "blast": 35, "dmg": 30, "grav": 0.2, "wind": 0.06,  "count": 1, "spread": 0}
]

class Projectile:
    def __init__(self, x, y, angle, power, wind, weapon_data):
        self.x = x
        self.y = y
        self.weapon = weapon_data
        self.radius = weapon_data["radius"]
        
        rad = math.radians(angle)
        self.vx = math.cos(rad) * (power * weapon_data["speed"])
        self.vy = -math.sin(rad) * (power * weapon_data["speed"])
        
        self.wind = wind 
        self.active = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        self.vy += self.weapon["grav"] 
        self.vx += self.wind * self.weapon["wind"] 

        if self.y > settings.HEIGHT + 50 or self.x < -100 or self.x > settings.MAP_WIDTH + 100:
            self.active = False
            return "MISS"
        return "FLYING"

    def check_collision(self, terrain, players):
        ground_y = terrain.get_y(self.x)
        if self.y >= ground_y:
            self.active = False
            return "HIT_TERRAIN"

        for p in players:
            dist = math.hypot(self.x - p.x, self.y - (p.y - 15))
            if dist < 20: 
                self.active = False
                return "HIT_PLAYER"
        return None

    def draw(self, screen, camera_x):
        if self.active:
            screen_x = int(self.x - camera_x)
            pygame.draw.circle(screen, self.weapon["color"], (screen_x, int(self.y)), self.radius)
            if self.weapon["name"] == "WIND RIDER": 
                pygame.draw.circle(screen, (0,0,0), (screen_x, int(self.y)), self.radius, 1)