import sys, time, os, keyboard, ctypes
from colorama import init, Fore

init(autoreset=True)

MB_ICONERROR = 0x10
MB_ICONWARNING = 0x30

def show_msg(title, text, style=0x0):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)

class Scene:
    def __init__(self, raw_map):
        lines = raw_map.strip('\n').split('\n')
        self.width = max(len(line) for line in lines)
        self.height = len(lines)
        self.tilemap = [list(line.ljust(self.width)) for line in lines]

    def update(self, engine, dt): pass
    def render_ui(self, engine): pass

class GameObject:
    def __init__(self, x, y, char, color=Fore.WHITE, gravity=False, draggable=False):
        self.x, self.y = float(x), float(y)
        self.char = char
        self.color = color
        self.vx, self.vy = 0.0, 0.0
        self.has_gravity = gravity
        self.is_draggable = draggable

class Fog2D:
    def __init__(self):
        self.current_scene = None
        self.running = False
        self.objects = []
        self.gravity_val = 100.0
        self.friction = 0.85
        self.selected_idx = 0

    def switch_scene(self, scene_instance):
        self.current_scene = scene_instance
        self.objects = getattr(scene_instance, 'start_objects', [])
        os.system('cls' if os.name == 'nt' else 'clear')
        sys.stdout.write("\033[5;1H") 
        for row in self.current_scene.tilemap:
            sys.stdout.write("".join(row) + "\n")

    def _draw(self, x, y, char):
        tx, ty = int(x), int(y)
        if 0 <= tx < 120 and 0 <= ty < 50:
            sys.stdout.write(f"\033[{ty+5};{tx+1}H{char}")

    def get_tile(self, x, y):
        tx, ty = int(x), int(y)
        if ty < 0 or ty >= self.current_scene.height or tx < 0 or tx >= self.current_scene.width:
            return "#"
        return self.current_scene.tilemap[ty][tx]

    def run(self, fps=60):
        self.running = True
        sys.stdout.write("\033[?25l")
        last_t = time.time()
        
        try:
            while self.running and not keyboard.is_pressed('esc'):
                now = time.time()
                dt = now - last_t
                last_t = now
                
                try:
                    self.current_scene.update(self, dt)

                    for obj in self.objects:
                        self._draw(obj.x, obj.y, self.get_tile(obj.x, obj.y))

                    for obj in self.objects:
                        if obj.has_gravity:
                            obj.vy += self.gravity_val * dt
                        
                        obj.vx *= self.friction

                        new_x = obj.x + obj.vx * dt
                        if self.get_tile(new_x, obj.y) not in ["#", "█"]:
                            obj.x = new_x
                        else:
                            obj.x = round(obj.x)
                            obj.vx = 0

                        new_y = obj.y + obj.vy * dt
                        if self.get_tile(obj.x, new_y) not in ["#", "█"]:
                            obj.y = new_y
                        else:
                            if obj.vy > 0:
                                obj.y = int(obj.y)
                            obj.vy = 0

                    for i, obj in enumerate(self.objects):
                        color = Fore.YELLOW if i == self.selected_idx else obj.color
                        self._draw(obj.x, obj.y, f"{color}{obj.char}")

                    sys.stdout.write("\033[1;1H")
                    self.current_scene.render_ui(self)
                    sys.stdout.flush()
                    
                except Exception as e:
                    show_msg("Logic Error", f"Error in Scene.update:\n{e}", MB_ICONWARNING)
                    self.running = False

                time.sleep(1/fps)
        except Exception as e:
            show_msg("Critical Error", f"Fog2d Error:\n{e}", MB_ICONERROR)
        finally:
            sys.stdout.write("\033[?25h\033[50;1H")