# MISSION: Chat together a firework display.
# STATUS: Research
# VERSION: 0.0.0
# NOTES: A.I. Generated
# DATE: 2026-05-19 04:43:49
# FILE: FireWorks01.py
# AUTHOR: https://github.com/TotalPythoneering
#
import tkinter as tk
import random
import math

class Firework:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x, self.y = x, y
        # Standard 6-character hex colors
        self.color = random.choice(['#ff2a2a', '#2aff2a', '#2a2aff', '#ffff2a', '#ff2aff', '#2affff', '#ffffff'])
        self.particles = []
        self.exploded = False

        # Rocket trail
        self.trail = []
        self.trail_len = 8

        # Launch physics
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-13, -9)

    def update(self):
        if not self.exploded:
            self.trail.append((self.x, self.y))
            if len(self.trail) > self.trail_len:
                self.trail.pop(0)

            self.x += self.vx
            self.y += self.vy
            self.vy += 0.25  # Gravity pulling rocket down

            # Explode at apex
            if self.vy >= 0:
                self.exploded = True
                self.explode()
        else:
            # Update explosion particles
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] += 0.08  # Gravity on particles
                p['life'] -= 1   # Countdown instead of alpha fade

    def draw(self):
        if not self.exploded:
            # Draw rocket trail
            for tx, ty in self.trail:
                self.canvas.create_oval(tx-2, ty-2, tx+2, ty+2, fill=self.color, outline="")
        else:
            # Draw particles that are still alive
            for p in self.particles:
                if p['life'] > 0:
                    self.canvas.create_oval(p['x']-2, p['y']-2, p['x']+2, p['y']+2, fill=self.color, outline="")

    def explode(self):
        for _ in range(60):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 7)
            self.particles.append({
                'x': self.x,
                'y': self.y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'life': random.randint(20, 45)  # Particle lifespan in frames
            })

def run_show(canvas, fireworks):
    # Clear canvas to redraw everything and prevent memory lag
    canvas.delete("all")
    
    # Update and draw fireworks
    for fw in fireworks[:]:
        fw.update()
        fw.draw()
        
        # Remove dead fireworks
        if fw.exploded and all(p['life'] <= 0 for p in fw.particles):
            fireworks.remove(fw)

    # Launch new fireworks occasionally
    if random.random() < 0.05:
        x = random.randint(100, 700)
        fireworks.append(Firework(canvas, x, 600))

    canvas.after(20, run_show, canvas, fireworks)

# Set up main window
root = tk.Tk()
root.title("4th of July Fireworks")
root.geometry("800x600")

# Night sky background
canvas = tk.Canvas(root, bg='#050515', width=800, height=600)
canvas.pack(fill=tk.BOTH, expand=True)

fireworks = []

# Start simulation
run_show(canvas, fireworks)
root.mainloop()
