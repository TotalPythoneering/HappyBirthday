# MISSION: Chat together a firework display.
# STATUS: Research
# VERSION: 0.0.0
# NOTES: A.I. Generated
# DATE: 2026-05-19 05:34:37
# FILE: FireWorks13.py
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
    def __init__(self, canvas, x, y, global_crackle_list, flash_callback, instant_detonate=False):
        self.canvas = canvas
        self.x = x
        self.shell_type = random.choice(['classic', 'willow', 'ring', 'fountain'])
        
        canvas_height = canvas.winfo_height()
        self.y = (canvas_height - 30) if (self.shell_type == 'fountain' and not instant_detonate) else y
        
        self.global_crackle_list = global_crackle_list
        self.flash_callback = flash_callback
        self.color = random.choice(['#ff2a2a', '#2aff2a', '#2a2aff', '#ffff2a', '#ff2aff', '#2affff', '#ffffff'])
        self.particles = []
        self.trail = []
        self.trail_len = 8
        
        if instant_detonate or self.shell_type == 'fountain':
            self.exploded = True
            self.explode()
        else:
            self.exploded = False
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
                
                if self.shell_type == 'willow':
                    p['vy'] += 0.15  
                    p['vx'] *= 0.98  
                elif self.shell_type == 'fountain':
                    p['vy'] += 0.22  
                    p['vx'] *= 0.97  
                else:
                    p['vy'] += 0.06  
                
                p['life'] -= 1

                if self.shell_type in ['willow', 'fountain'] and p['life'] % 2 == 0 and p['life'] > 0:
                    self.global_crackle_list.append(CrackleSpark(p['x'], p['y']))

                if self.shell_type not in ['willow', 'fountain'] and p['life'] == 1 and random.random() < 0.6:
                    for _ in range(random.randint(1, 3)):
                        self.global_crackle_list.append(CrackleSpark(p['x'], p['y']))

    def draw(self):
        if not self.exploded:
            for tx, ty in self.trail:
                self.canvas.create_oval(tx-2, ty-2, tx+2, ty+2, fill=self.color, outline="")
        else:
            for p in self.particles:
                if p['life'] > 0:
                    color = '#ffffff' if p['life'] <= 3 and self.shell_type not in ['willow', 'fountain'] else self.color
                    size = 1 if p['life'] <= 3 else (3 if self.shell_type == 'willow' else 2)
                    self.canvas.create_oval(p['x']-size, p['y']-size, p['x']+size, p['y']+size, fill=color, outline="")

    def explode(self):
        self.flash_callback(self.x, self.y, self.color)
        
        if self.shell_type == 'classic':
            for _ in range(65):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(2, 8)
                self.particles.append({'x': self.x, 'y': self.y, 'vx': math.cos(angle) * speed, 'vy': math.sin(angle) * speed, 'life': random.randint(15, 35)})
                
        elif self.shell_type == 'willow':
            self.color = random.choice(['#ffca3a', '#ff9f1c', '#ffffff']) 
            for _ in range(45):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 4)
                self.particles.append({'x': self.x, 'y': self.y, 'vx': math.cos(angle) * speed, 'vy': math.sin(angle) * speed - 2, 'life': random.randint(35, 55)})
                
        elif self.shell_type == 'ring':
            num_particles = 40
            speed = random.uniform(4, 6)
            for i in range(num_particles):
                angle = (i / num_particles) * 2 * math.pi
                v_var = random.uniform(0.9, 1.1)
                self.particles.append({'x': self.x, 'y': self.y, 'vx': math.cos(angle) * speed * v_var, 'vy': math.sin(angle) * speed * v_var, 'life': random.randint(25, 40)})

        elif self.shell_type == 'fountain':
            self.color = random.choice(['#ffffff', '#2affff', '#ffca3a'])
            for _ in range(80):
                angle = random.uniform(-1.9, -1.2)  
                speed = random.uniform(6, 14)       
                self.particles.append({'x': self.x, 'y': self.y, 'vx': math.cos(angle) * speed, 'vy': math.sin(angle) * speed, 'life': random.randint(40, 65)})

class Skyline:
    def __init__(self, width, height):
        self.buildings = []
        self.windows = []
        self.resize(width, height)

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.buildings.clear()
        self.windows.clear()
        
        x = 0
        while x < self.width:
            b_width = random.randint(40, 90)
            b_height = random.randint(60, 160)
            self.buildings.append((x, self.height - b_height, x + b_width, self.height))
            
            for wx in range(x + 5, x + b_width - 10, 12):
                for wy in range(self.height - b_height + 10, self.height - 15, 18):
                    if random.random() < 0.35:  
                        self.windows.append((wx, wy, wx + 6, wy + 10))
            x += b_width - 5

    def draw(self, canvas):
        canvas.create_oval(self.width - 100, 40, self.width - 40, 100, fill="#fffebb", outline="")
        for b in self.buildings:
            canvas.create_rectangle(*b, fill="#0b0b18", outline="#111122")
        for w in self.windows:
            canvas.create_rectangle(*w, fill="#ffe066", outline="")

class AmericanFlag:
    def __init__(self, canvas, x, y, width, height):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        stripe_height = self.height / 13
        canton_width = self.width * 0.4
        canton_height = stripe_height * 7

        dark_red = "#8b0000"
        pale_white = "#e0e0e0"
        dark_blue = "#000040"

        for i in range(13):
            top_y = self.y + (i * stripe_height)
            bot_y = top_y + stripe_height
            color = dark_red if i % 2 == 0 else pale_white
            self.canvas.create_rectangle(self.x, top_y, self.x + self.width, bot_y, fill=color, outline="")

        self.canvas.create_rectangle(self.x, self.y, self.x + canton_width, self.y + canton_height, fill=dark_blue, outline="")

        col_spacing = canton_width / 12
        row_spacing = canton_height / 10
        for row in range(1, 10):
            for col in range(1, 12):
                if (row % 2 == 1 and col % 2 == 1) or (row % 2 == 0 and col % 2 == 0):
                    sx = self.x + (col * col_spacing)
                    sy = self.y + (row * row_spacing)
                    self.canvas.create_rectangle(sx-1, sy-1, sx+1, sy+1, fill="#ffffff", outline="")

class TextOverlay:
    def __init__(self, text):
        self.text = text
        self.colors = ["#ff3333", "#ffffff", "#3333ff", "#ffff33", "#ff33ff", "#33ffff"]
        self.color_index = 0
        self.tick = 0

    def update(self):
        self.tick += 1
        if self.tick % 25 == 0:  
            self.color_index = (self.color_index + 1) % len(self.colors)

    def draw(self, canvas):
        mid_x = canvas.winfo_width() // 2
        mid_y = canvas.winfo_height() // 2 - 40
        current_color = self.colors[self.color_index]
        
        canvas.create_text(mid_x + 3, mid_y + 3, text=self.text, fill="#040410", font=("Impact", 44, "bold"), justify=tk.CENTER)
        canvas.create_text(mid_x, mid_y, text=self.text, fill=current_color, font=("Impact", 44, "bold"), justify=tk.CENTER)

def trigger_flash(x, y, color):
    flashes.append({'x': x, 'y': y, 'radius': 5, 'max_radius': random.randint(40, 70), 'color': color})

def trigger_finale():
    global display_elements
    # FIXED: Reverses the state from True -> False or False -> True every click
    display_elements = not display_elements 
    
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    for _ in range(16):
        delay = random.randint(0, 450)
        root.after(delay, lambda: fireworks.append(
            Firework(canvas, random.randint(60, w - 60), h - 50, crackles, trigger_flash)
        ))

def on_canvas_click(event):
    fireworks.append(
        Firework(canvas, event.x, event.y, crackles, trigger_flash, instant_detonate=True)
    )

def on_window_resize(event):
    if event.widget == canvas:
        skyline.resize(event.width, event.height)

def run_show(canvas, fireworks, crackles, skyline, flashes, flag, overlay):
    canvas.delete("all")
    
    # 1. Background conditional layers
    if display_elements:
        flag.draw()
        
    skyline.draw(canvas)
    
    if display_elements:
        overlay.update()
        overlay.draw(canvas)
    
    # 2. Particle Processing Engine
    for f in flashes[:]:
        f['radius'] += 6
        if f['radius'] < f['max_radius']:
            canvas.create_oval(f['x']-f['radius'], f['y']-f['radius'], f['x']+f['radius'], f['y']+f['radius'], outline=f['color'], width=2)
        else:
            flashes.remove(f)

    for fw in fireworks[:]:
        fw.update()
        fw.draw()
        if fw.exploded and all(p['life'] <= 0 for p in fw.particles):
            fireworks.remove(fw)

    for cs in crackles[:]:
        cs.update()
        if cs.life > 0:
            canvas.create_oval(cs.x-1, cs.y-1, cs.x+1, cs.y+1, fill=cs.color, outline="")
        else:
            crackles.remove(cs)

    # 3. Ambient Generation Loops
    if random.random() < 0.05:
        w = canvas.winfo_width()
        h = canvas.winfo_height()
        span_w = w if w > 200 else 800
        base_h = h if h > 200 else 580
        
        x = random.randint(60, span_w - 60)
        fireworks.append(Firework(canvas, x, base_h - 50, crackles, trigger_flash))

    canvas.after(20, run_show, canvas, fireworks, crackles, skyline, flashes, flag, overlay)

# Global tracker state variable initialization
display_elements = False

root = tk.Tk()
root.title("4th of July Fireworks Simulator")
root.geometry("800x650") 
root.configure(bg='#111')

canvas = tk.Canvas(root, bg='#03030d', width=800, height=580, highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<Configure>", on_window_resize)

ui_frame = tk.Frame(root, bg='#111', padx=5, pady=5)
ui_frame.pack(fill=tk.X, side=tk.BOTTOM)

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
flashes = []
skyline = Skyline(800, 580)
flag = AmericanFlag(canvas, x=30, y=30, width=300, height=160)
overlay = TextOverlay("Happy 4th of July!")

run_show(canvas, fireworks, crackles, skyline, flashes, flag, overlay)
root.mainloop()
