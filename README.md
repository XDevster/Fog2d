FOG2D ENGINE - README.TXT

1. OVERVIEW
Fog2D is a lightweight, terminal-based 2D game engine written in Python. 
It enables coordinate-based rendering and real-time physics within a 
standard console window using ANSI escape sequences.

2. TECHNICAL REQUIREMENTS
The engine utilizes two core libraries to bypass console limitations:
- Colorama: Provides ANSI escape support for cursor positioning and 
  character coloring. This allows redrawing specific coordinates 
  rather than scrolling the screen.
- Keyboard: Facilitates non-blocking input, detecting key presses 
  instantly without interrupting the game execution loop.

3. CORE COMPONENTS

3.1 GameObject
The base class for all entities (Player, NPCs, Items).
- x, y: Floating-point coordinates for sub-pixel precision.
- vx, vy: Velocity vectors. vx (horizontal), vy (vertical).
- gravity: Boolean. When true, downward acceleration is applied.
- char: The ASCII character representing the object.
- color: The color constant assigned to the character.

3.2 Scene
A container for level layout and unique logic.
- __init__: Processes the map string and ensures a uniform 
  rectangular grid to prevent IndexErrors.
- update(engine, dt): Executed 60 times per second for input 
  handling and game rules.
- render_ui(engine): Reserved for printing HUD elements in the 
  top 4 lines of the console.

3.3 Fog2D (The Engine)
The central manager of the game loop.
- get_tile(x, y): Returns the character from the map at specific 
  coordinates. Used for collision detection.
- switch_scene(scene): Clears terminal and initializes a new Scene.
- run(fps): The main loop (Logic -> Physics -> Collision -> Render).

4. PHYSICS LOGIC
To prevent collision tunneling, the engine calculates X and Y 
collisions independently. If a predicted movement intersects 
with a solid tile (# or █), velocity on that axis is zeroed 
out before the position update. This allows for smooth sliding 
along walls and stable landing on platforms.
