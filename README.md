# 🏹 Stickman Turn: Turn-Based Artillery Game

**Stickman Turn** adalah game tembak-tembakan strategis berbasis giliran (*turn-based artillery*) yang dibangun menggunakan Python dan Pygame. Pemain harus mengandalkan perhitungan sudut, kekuatan tembakan, dan pengaruh angin untuk menghancurkan lawan di medan tempur yang dinamis.

---

## 🎮 Fitur Utama

* **🔄 Turn-Based Combat:** Sistem pertarungan bergilir yang membutuhkan strategi matang.
* **🤖 Artificial Intelligence:** Bermain melawan teman secara lokal (1vs1) atau melawan BOT dengan logika kalkulasi tembakan otomatis.
* **🌬️ Dynamic Wind System:** Arah dan kekuatan angin berubah setiap giliran, mempengaruhi lintasan peluru secara real-time.
* **🔫 Weapon Classes:** Tersedia berbagai jenis senjata (Sniper, Heavy Bomb, Triple Shot, dll) dengan statistik kerusakan dan area ledakan yang berbeda.
* **🗺️ Diverse Maps:** Lima pilihan peta unik (Hill, Snow, Moon, Desert, Volcano) dengan karakteristik gravitasi dan latar belakang yang berbeda.
* **🎥 Cinematic Camera:** Kamera dinamis yang secara otomatis mengikuti pergerakan peluru dan efek ledakan.
* **🎵 Audio System:** Dilengkapi dengan *Background Music* (BGM) dan efek suara untuk pengalaman bermain yang lebih imersif.

---

## 🛠️ Tech Stack
* **Language:** [Python 3.x](https://www.python.org/)
* **Library:** [Pygame](https://www.pygame.org/) (Graphics, Input, & Audio)
* **Logic:** Physics Engine (Gravity & Projectile Motion), AI Calculation, State Machine.

---

## 📂 Struktur Proyek
```text
/Stickman-Turn
  ├── main.py          <-- Entry point & Game Loop
  ├── settings.py      <-- Konfigurasi konstanta (Width, Height, FPS)
  ├── terrain.py       <-- Logika pembentukan peta & deformasi tanah
  ├── player.py        <-- Logika pergerakan & status pemain
  ├── weapon.py        <-- Data stat senjata & logika proyektil
  ├── bg_music.mp3     <-- Aset Audio
  └── README.md
