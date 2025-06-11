
![alt text](https://github.com/notironicallycasters/blohsh-engine/blob/main/icon.png)

> Is that a JoJo reference ??? -Reddit

# Blohsh Engine or Battle Verticy ? ‍
3D engine I made with Python/Pygame to learn Computer Graphics and 3D rendering.
Made 100% in python. 100% human generated code. No AI used for this project.
Uses `pygame-ce` for the graphics so if you wanna test the code, install it along with `pyperclip`

## Features ?
- Render 3D(No way)
- Render faces with colors !!!
- Rotation along point
- Camera with:
  - Perspective projection
  - Position
  - Rotation
- Freecam movement
- Homemade depth buffer:
  - Sorts faces from nearest to closest so the far ones renders first
- Culling:
  - Culls faces off screen
  - Culls faces behind camera(Kind of stupid since the screen culling is already enough(I think))
- OBJ format importation:
  - Vertices 
  - Triangular faces 
  - Quad faces 
  - Materials 
  - UVs 
  - Normals
 
  ## Documentation
  The `main.py` contains a default freecam with randomly placed cube and J-J-J-Jotaro ???

  ###
  Use the Engine class to use the different functions:

  - `teapot(position - tuple or list, scale - float, path - str)` Add a 3d model in an obj format(musn't have normals or uv's) with a uniform size
  - `calculates_faces()` Sort the faces by depth
  - `render_faces()` Render faces
  - `rotate_x/y/z(degrees - float, origin - tuple or list)` Rotate all vertices along a point
