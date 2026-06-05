# MISSION: Chat together a firework display.
# STATUS: Research
# VERSION: 0.0.0
# NOTES: A.I. Generated
# DATE: 2026-05-19 04:48:48
# FILE: FireWorks02.py
# AUTHOR: https://github.com/TotalPythoneering
#
import tkinter as tk
import random
import math

class CrackleSpark:
    """Tiny, fast-fading white/gold sparks that pop at the end of a particle's life."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-1.5, 1.5)
        self.life = random.randint(3, 8)
        self.color = random.choice(['#ffffff', '#ffebad'])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Slight gravity
        self.life -= 1

class Firework:
    def __init__(self, canvas, x, y, global_crackle_list):
        self.canvas = canvas
        self.x, self.y = x, y
        self.global_crackle_list = global_crackle_list
        self.color = random.choice(['#ff2a2a', '#2aff2a', '#2a2aff', '#ffff2a', '#ff2aff', '#2affff', '#ffffff'])
        self.particles = []
        self.exploded = False

        # Rocket trail
        self.trail = []
        self.trail_len = 8

        # Launch physics
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-14, -10)

    def update(self):
        if not self.exploded:
            self.trail.append((self.x, self.y))
            if len(self.trail) > self.trail_len:
                self.trail.pop(0)

            self.x += self.vx
            self.y += self.vy
            self.vy += 0.25

            if self.vy >= 0:
                self.exploded = True
                self.explode()
        else:
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] += 0.06
                p['life'] -= 1

                # Crackle effect: trigger sparks right before the particle dies
                if p['life'] == 1 and random.random() < 0.7:
                    # Spawn 2-3 crackle sparks per dying particle
                    for _ in range(random.randint(2, 3)):
                        self.global_crackle_list.append(CrackleSpark(p['x'], p['y']))

    def draw(self):
        if not self.exploded:
            for tx, ty in self.trail:
                self.canvas.create_oval(tx-2, ty-2, tx+2, ty+2, fill=self.color, outline="")
        else:
            for p in self.particles:
                if p['life'] > 0:
                    # Visual Polish: Make particles flash white/bright right before crackling
                    color = '#ffffff' if p['life'] <= 3 else self.color
                    size = 1 if p['life'] <= 3 else 2
                    self.canvas.create_oval(p['x']-size, p['y']-size, p['x']+size, p['y']+size, fill=color, outline="")

    def explode(self):
        for _ in range(60):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.randint(15, 35)
            })

def run_show(canvas, fireworks, crackles):
    canvas.delete("all")
    
    # Update and draw main fireworks
    for fw in fireworks[:]:
        fw.update()
        fw.draw()
        if fw.exploded and all(p['life'] <= 0 for p in fw.particles):
            fireworks.remove(fw)

    # Update and draw crackle sparks
    for cs in crackles[:]:
        cs.update()
        if cs.life > 0:
            canvas.create_oval(cs.x-1, cs.y-1, cs.x+1, cs.y+1, fill=cs.color, outline="")
        else:
            crackles.remove(cs)

    # Launch new fireworks randomly
    if random.random() < 0.05:
        x = random.randint(100, 700)
        fireworks.append(Firework(canvas, x, 600, crackles))

    canvas.after(20, run_show, canvas, fireworks, crackles)

# Main window setup
root = tk.Tk()
root.title("4th of July Crackling Fireworks")
root.geometry("800x600")

canvas = tk.Canvas(root, bg='#050515', width=800, height=600)
canvas.pack(fill=tk.BOTH, expand=True)

fireworks = []
crackles = []

run_show(canvas, fireworks, crackles)
root.mainloop()
