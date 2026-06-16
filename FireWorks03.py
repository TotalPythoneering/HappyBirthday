# MISSION: Chat together a firework display.
# STATUS: Research
# VERSION: 0.0.0
# NOTES: A.I. Generated
# DATE: 2026-05-19 04:51:20
# FILE: FireWorks03.py
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
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.life = random.randint(3, 8)
        self.color = random.choice(['#ffffff', '#ffebad'])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  
        self.life -= 1

class Firework:
    def __init__(self, canvas, x, y, global_crackle_list, shell_type=None):
        self.canvas = canvas
        self.x, self.y = x, y
        self.global_crackle_list = global_crackle_list
        self.color = random.choice(['#ff2a2a', '#2aff2a', '#2a2aff', '#ffff2a', '#ff2aff', '#2affff', '#ffffff'])
        self.particles = []
        self.exploded = False
        
        # Assign a random shell type if none is provided
        self.shell_type = shell_type if shell_type else random.choice(['classic', 'willow', 'ring'])

        # Rocket trail setup
        self.trail = []
        self.trail_len = 8

        # Launch physics
        self.vx = random.uniform(-1.2, 1.2)
        self.vy = random.uniform(-15, -11)

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
                
                # Gravity adjustment based on shell type
                if self.shell_type == 'willow':
                    p['vy'] += 0.15  # Heavy gravity for drooping effect
                    p['vx'] *= 0.98  # Air resistance pulls them tight
                else:
                    p['vy'] += 0.06  # Normal drifting gravity
                
                p['life'] -= 1

                # Dynamic trail logic for Willow type
                if self.shell_type == 'willow' and p['life'] % 2 == 0 and p['life'] > 0:
                    self.global_crackle_list.append(CrackleSpark(p['x'], p['y']))

                # Crackle explosion at the death of classic/ring particles
                if self.shell_type != 'willow' and p['life'] == 1 and random.random() < 0.6:
                    for _ in range(random.randint(1, 3)):
                        self.global_crackle_list.append(CrackleSpark(p['x'], p['y']))

    def draw(self):
        if not self.exploded:
            for tx, ty in self.trail:
                self.canvas.create_oval(tx-2, ty-2, tx+2, ty+2, fill=self.color, outline="")
        else:
            for p in self.particles:
                if p['life'] > 0:
                    # Visual flare right before bursting/fading
                    color = '#ffffff' if p['life'] <= 3 and self.shell_type != 'willow' else self.color
                    size = 1 if p['life'] <= 3 else (3 if self.shell_type == 'willow' else 2)
                    self.canvas.create_oval(p['x']-size, p['y']-size, p['x']+size, p['y']+size, fill=color, outline="")

    def explode(self):
        if self.shell_type == 'classic':
            # Dense, standard spherical burst
            for _ in range(65):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 8)
                self.particles.append({'x': self.x, 'y': self.y, 'vx': math.cos(angle) * speed, 'vy': math.sin(angle) * speed, 'life': random.randint(15, 35)})
                
        elif self.shell_type == 'willow':
            # Shoots upward slightly, then rains down long golden-tinted weeping paths
            self.color = random.choice(['#ffca3a', '#ff9f1c', '#ffffff']) # Willow looks best gold/warm
            for _ in range(45):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 4)
                self.particles.append({'x': self.x, 'y': self.y, 'vx': math.cos(angle) * speed, 'vy': math.sin(angle) * speed - 2, 'life': random.randint(35, 55)})
                
        elif self.shell_type == 'ring':
            # Perfect expanding circle shell
            num_particles = 40
            speed = random.uniform(4, 6)
            for i in range(num_particles):
                angle = (i / num_particles) * 2 * math.pi
                v_var = random.uniform(0.9, 1.1)
                self.particles.append({'x': self.x, 'y': self.y, 'vx': math.cos(angle) * speed * v_var, 'vy': math.sin(angle) * speed * v_var, 'life': random.randint(25, 40)})

def trigger_finale():
    """Launches a barrage of 12 multi-type fireworks rapidly across the screen."""
    for _ in range(12):
        delay = random.randint(0, 400)
        root.after(delay, lambda: fireworks.append(
            Firework(canvas, random.randint(80, 720), 600, crackles)
        ))

def run_show(canvas, fireworks, crackles):
    canvas.delete("all")
    
    # Update and render fireworks
    for fw in fireworks[:]:
        fw.update()
        fw.draw()
        if fw.exploded and all(p['life'] <= 0 for p in fw.particles):
            fireworks.remove(fw)

    # Update and render crackles
    for cs in crackles[:]:
        cs.update()
        if cs.life > 0:
            canvas.create_oval(cs.x-1, cs.y-1, cs.x+1, cs.y+1, fill=cs.color, outline="")
        else:
            crackles.remove(cs)

    # Normal background sequence ambient launches
    if random.random() < 0.05:
        x = random.randint(120, 680)
        fireworks.append(Firework(canvas, x, 600, crackles))

    canvas.after(20, run_show, canvas, fireworks, crackles)

# GUI Layout
root = tk.Tk()
root.title("4th of July Fireworks Simulator")
root.geometry("800x650") 
root.configure(bg='#111')

# Interactive Showroom Canvas
canvas = tk.Canvas(root, bg='#040410', width=800, height=580, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Control Panel Frame (Fixed: Using standard padding arguments)
ui_frame = tk.Frame(root, bg='#111', padx=5, pady=5)
ui_frame.pack(fill=tk.X, side=tk.BOTTOM)

# Grand Finale Button
finale_btn = tk.Button(
    ui_frame, 
    text="💥 TRIGGER GRAND FINALE 💥", 
    font=("Arial", 11, "bold"),
    bg="#d90429", 
    fg="white", 
    activebackground="#ef233c",
    activeforeground="white",
    command=trigger_finale,
    pady=5
)
finale_btn.pack(expand=True)

fireworks = []
crackles = []

# Initialize loop
run_show(canvas, fireworks, crackles)
root.mainloop()
