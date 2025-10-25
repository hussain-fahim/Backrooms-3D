# 🌀 Backrooms 3D - BETA
*A Retro Raycasting Game Built with Python & Pygame*

---

## 🧩 Overview

**Backrooms 3D - BETA** is an experimental **first-person 3D-style game** built entirely with **raycasting** in **Pygame**.  
Inspired by early classics like *Wolfenstein 3D*, it uses **mathematical ray projection** to simulate a 3D environment from a 2D grid — no external 3D engines required.

The goal of this project is to explore **low-level rendering**, **collision systems**, and **classic game mechanics** while building an immersive "Backrooms"-themed experience.

---

## 🎮 Current Features

✅ Fully functional **raycasting engine**  
✅ Player movement and rotation controls  
✅ Wall collisions and environment boundaries  
✅ Dynamic lighting based on distance  
✅ HUD with ammo, health, and crosshair  
✅ Shooting and projectile animation  
✅ Checkpoints and respawn system  
✅ Moving walls / traps  
✅ Debug mode for 2D top-down visualization  
✅ “YOU DIED” screen and restart logic  

---

## 🕹️ Controls

| Key | Action |
|-----|--------|
| **W / A / S / D** | Move forward, left, backward, right |
| **← / →** | Rotate view left / right |
| **Space** | Shoot |
| **F** | Interact / open |
| **Esc** | Quit game |

---

## 🧱 Technical Details

- **Engine:** Pygame 2D rendering  
- **Rendering technique:** Raycasting  
- **Field of View (FOV):** 90°  
- **Lighting:** Distance-based shading  
- **Projection mode:** 1 = 3D View, 0 = 2D Debug  
- **Map:** Grid-based level using tile IDs for walls and entities  
- **Resolution:** Adjustable (default 960×640)  

---

## 🖼️ Game Assets

| Type | Files |
|------|-------|
| Character sprites | `char1.png` → `char5.png` |
| Wall texture | `bricksx64.png` |
| Weapon textures | `water_gun_green_fps_transparent-2.png`, `gun_shot.png` |
| Interface / HUD | `HUD-2.png`, `green_crosshair_30x30.png` |
| Background | `space.png` |
| Font | `Jersey25-Regular.ttf` |

> 💡 Place all assets in the same directory as `raycaster.py`, or in an `assets/` folder and update the paths in your code.

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/backrooms-3d.git
cd backrooms-3d
```

### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
Or simply:
```bash
pip install pygame
```

### 3️⃣ Run the game
```bash
python raycaster.py
```

---

## 📦 Requirements

```
pygame==2.6.1
```

*(You can also add optional packages like `numpy` or `pillow` later for performance or graphics enhancements.)*

---

## 🧠 Code Structure

```
backrooms-3d/
│
├── raycaster.py             # Main game file
├── requirements.txt         # Dependencies
├── README.md                # Project documentation
│
├── assets/
│   ├── bricksx64.png
│   ├── space.png
│   ├── water_gun_green_fps_transparent-2.png
│   ├── gun_shot.png
│   ├── green_crosshair_30x30.png
│   ├── HUD-2.png
│   ├── Jersey25-Regular.ttf
│   └── char1.png ... char5.png
```

---

## 🔬 How It Works (Simplified)

1. **Raycasting:**  
   The engine casts one ray per column on the screen to detect wall collisions in the grid map.  
   The closer the wall, the taller it appears on-screen — simulating a 3D perspective.

2. **Projection:**  
   Each wall slice’s height is computed using inverse distance scaling and rendered as vertical strips.

3. **Lighting:**  
   Distant walls are darkened using linear or quadratic falloff.

4. **Collision Detection:**  
   Player position updates only if the next move doesn’t intersect with a wall cell.

5. **HUD Rendering:**  
   Health, ammo, and crosshair are drawn every frame on top of the game scene.

---

## 💀 Death & Respawn

When the player’s health drops to **0**, a **“YOU DIED”** overlay appears.  
After a short delay, the player is respawned at the **last checkpoint** position.

---

## 🧩 Debug Mode

To enable a **2D top-down debug map**, set:
```python
debug_mode = 1
```
This mode shows:
- Player position
- Raycasting lines
- Wall collision boundaries  
Useful for developing and optimizing ray logic.

---

## 🧱 Map System

The environment is defined using a **2D list**:
```python
game_map = [
  [1,1,1,1,1,1],
  [1,0,0,0,0,1],
  [1,0,2,0,0,1],
  [1,1,1,1,1,1]
]
```
Each number represents:
- `1` → Wall  
- `0` → Empty space  
- `2+` → Doors, triggers, or hazards  

---

## 🚧 Future Improvements

- [ ] Texture projection on walls  
- [ ] Better lighting and shading  
- [ ] Enemy AI and pathfinding  
- [ ] Interactive objects and pickups  
- [ ] Sound effects and ambient audio  
- [ ] Multiple maps / level loading  
- [ ] Game menus (Start / Pause / Death)  
- [ ] Save & load feature  

---

## 🛠️ Known Issues

⚠️ Texture alignment may vary by angle  
⚠️ Lighting sometimes flickers near corners  
⚠️ Occasional frame dips on older systems  
⚠️ Wall collision edge cases still being refined  

---

## 📈 Performance

The engine runs around **60 FPS** at 960×640 on midrange hardware.  
You can tweak performance by reducing ray count:
```python
rays = 480  # Half resolution for faster rendering
```

---

## 🧠 Developer Notes

- Set `projection_mode = 1` for 3D or `projection_mode = 0` for debug view.  
- Keep the aspect ratio locked to avoid wall distortion.  
- If new assets are added, ensure they are PNG or BMP with transparency.  
- Use consistent pixel sizes (preferably 64×64) for wall textures.

---

> *“The walls may move, but the Backrooms never end.”*

---
