import pygame
import settings
import math
import random

class Terrain:
    def __init__(self, map_type):
        self.heights = []
        self.map_type = map_type
        
        # Penentuan Warna Lapis Atas dan Tanah Bawah
        if map_type == 1: # HILL
            self.top_color = (34, 139, 34)   # Hijau Rumput
            self.bot_color = (139, 69, 19)   # Coklat Tanah
            self.bg_color = (135, 206, 235)  # Biru Langit
            for x in range(settings.MAP_WIDTH):
                y = 400 + math.sin(x * 0.005) * 100 + math.sin(x * 0.02) * 30
                self.heights.append(int(y))
                
        elif map_type == 2: # SNOW
            self.top_color = (255, 255, 255) # Putih Salju
            self.bot_color = (176, 224, 230) # Biru Es Batu
            self.bg_color = (119, 136, 153)  # Langit Kelabu
            for x in range(settings.MAP_WIDTH):
                y = 450 + math.sin(x * 0.02) * 80 + math.cos(x * 0.05) * 50 + random.randint(-3, 3)
                self.heights.append(int(y))
                
        elif map_type == 3: # MOON
            self.top_color = (200, 200, 200) # Abu Terang
            self.bot_color = (105, 105, 105) # Abu Gelap
            self.bg_color = (10, 10, 25)     # Angkasa Hitam
            for x in range(settings.MAP_WIDTH):
                y = 400 - abs(math.sin(x * 0.005) * 150) + math.cos(x * 0.03) * 20
                self.heights.append(int(y))
                
        elif map_type == 4: # DESERT
            self.top_color = (244, 164, 96)  # Pasir Terang
            self.bot_color = (210, 105, 30)  # Pasir Gelap
            self.bg_color = (255, 140, 0)    # Senja Oranye
            for x in range(settings.MAP_WIDTH):
                y = 500 + math.sin(x * 0.003) * 150 # Gundukan sangat halus dan panjang
                self.heights.append(int(y))
                
        else: # VOLCANO
            self.top_color = (139, 0, 0)     # Merah Lahar
            self.bot_color = (50, 50, 50)    # Batu Obsidian
            self.bg_color = (80, 0, 0)       # Langit Kiamat Merah
            for x in range(settings.MAP_WIDTH):
                nx = x - settings.MAP_WIDTH/2
                y = 550 - 400 * math.exp(-(nx**2)/80000) + math.sin(x*0.1)*10
                self.heights.append(int(y))

    def get_y(self, x):
        x = max(0, min(x, settings.MAP_WIDTH - 1))
        return self.heights[int(x)]

    def explode(self, center_x, radius):
        for x in range(int(center_x - radius), int(center_x + radius)):
            if 0 <= x < settings.MAP_WIDTH:
                dx = x - center_x
                dy = math.sqrt(max(0, radius**2 - dx**2))
                self.heights[x] += dy
                if self.heights[x] > settings.HEIGHT - 10:
                    self.heights[x] = settings.HEIGHT - 10

    def draw(self, screen, camera_x):
        # Hanya menggambar tanah yang terlihat di layar untuk menghemat memori!
        start_x = max(0, int(camera_x))
        end_x = min(settings.MAP_WIDTH, start_x + settings.WIDTH + 5)
        
        for x in range(start_x, end_x):
            screen_x = x - camera_x
            y = self.heights[x]
            # Lapisan Tanah Bawah
            pygame.draw.line(screen, self.bot_color, (screen_x, settings.HEIGHT), (screen_x, y))
            # Lapisan Kerak Atas (Ketebalan 15 piksel)
            pygame.draw.line(screen, self.top_color, (screen_x, y), (screen_x, y - 15))
            
            if self.map_type == 2: # Tambah titik outline hitam untuk map Snow
                pygame.draw.circle(screen, (0,0,0), (int(screen_x), y-15), 1)