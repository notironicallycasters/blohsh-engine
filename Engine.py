import pygame
import random
import math
import ObjConvert
import time
import numpy as np


pygame.init()

#List of all vertices,edges,faces,their color, the amount of faces culled and the amount of objects
vertex_table=[]
edge_table=[]
face_table=[]
depth_table=[]
faces_color = []
projected_vertices = []
culled = 0
objects = 0

#Wireframe colors and width(Deprecated)
vertex_color = (255,0,0)
edge_color = (0,255,0)
edge_width = 1

#Camera informations
camera = [0,0,0] #Camera position
camera_rotation = [0,0,0] #Camera rotation
focal_length = 600 #Focal length of the camera

#Screen info
screen = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN) #Display the window
height = screen.height/2
width = screen.width/2

#Render text
def label(str,size,color,pos):
    font = pygame.font.Font(None,size)
    text = font.render(str,True,color)
    screen.blit(text,pos) 

#Render all faces
def render_faces():
    global culled
    for f in range(len(face_table)): #For all faces
        if len(face_table[f]) == 3: #Checks if it's a triangle
            a,b,c = face_table[f]
        else:
            a,b,c,d = face_table[f]

        if camera[2] > vertex_table[a][2] or camera[2] > vertex_table[b][2] or camera[2] > vertex_table[c][2]: #If face is behind the camera. Cull it
            culled += 1
            continue

        #First vertex
        x,y,z = vertex_table[a]
        z1 = z-camera[2]
        
        x_p = ((x-camera[0])*focal_length) / ((z-camera[2]))
        y_p = ((y-camera[1])*focal_length) / ((z-camera[2]))
        if abs(x_p) > screen.width and abs(y_p) > screen.height :
            culled += 1
            continue
        x_p += width
        y_p += height
        a_p = (x_p,y_p)

        #Second vertex
        x,y,z = vertex_table[b]
        z2 = z-camera[2]
        x_p = ((x-camera[0])*focal_length) / ((z-camera[2]))
        y_p = ((y-camera[1])*focal_length) / ((z-camera[2]))
        if abs(x_p) > screen.width and abs(y_p) > screen.height :
            culled += 1
            continue
        x_p += width
        y_p += height
        b_p = (x_p,y_p)

        #Third vertex
        x,y,z = vertex_table[c]
        z3 = z-camera[2]
        x_p = ((x-camera[0])*focal_length) / ((z-camera[2]))
        y_p = ((y-camera[1])*focal_length) / ((z-camera[2]))
        if abs(x_p) > screen.width and abs(y_p) > screen.height :
            culled += 1
            continue
        x_p += width
        y_p += height
        
        c_p = (x_p,y_p)

        #Fourth vertex if face is quad
        if len(face_table[f]) == 4:
            x,y,z = vertex_table[d]
            x_p = ((x-camera[0])*focal_length) / ((z-camera[2]))
            y_p = ((y-camera[1])*focal_length) / ((z-camera[2]))
            if abs(x_p) > screen.width and abs(y_p) > screen.height :
                culled += 1
                continue
            x_p += width
            y_p += height
            d_p = (x_p,y_p)

            pygame.draw.polygon(screen,faces_color[f],[a_p,b_p,c_p,d_p]) #Draw quad face
            continue

        # z4 = min(min(z1,z2),z3)
        # color = max(min(int(z4/-5),255),0)
        # r,g,b = face_table[f]
        # r = min(r//20,255)/255
        # g = min(g//20,255)/255
        # b = min(b//20,255)/255
        # depth_rgb = [r,g,b]
        #triangle(a_p,b_p,c_p,faces_color[f])
        pygame.draw.polygon(screen,faces_color[f],[a_p,b_p,c_p]) #Draw triangle face

#Calculate the faces depths
def calculate_faces():
    depth_table.clear()
    for pf in range(len(face_table)): #For all faces
        if len(face_table[pf]) == 3: #Triangle faces
            a,b,c = face_table[pf]
            z = (vertex_table[a][2]+vertex_table[b][2]+vertex_table[c][2])/3.0 #Depth by average
            #z = min(min(vertex_table[a][2],vertex_table[b][2]),vertex_table[c][2]) #Depth by furtherest
        elif len(face_table[pf]) == 4: #Quad faces
            a,b,c,d = face_table[pf]
            z = (vertex_table[a][2]+vertex_table[b][2]+vertex_table[c][2]+vertex_table[d][2])/4.0 #Depth by average

        depth_table.append(z)

    #Sort all lists from nearest to closest    
    l1,l2,l3 = zip(*sorted(zip(depth_table, face_table, faces_color)))
    sorted_stuff = [l2,l3]
    face_table.clear()
    face_table.extend(sorted_stuff[0])
    faces_color.clear()
    faces_color.extend(sorted_stuff[1])
    faces_color.reverse()
    face_table.reverse()
    depth_table.reverse()

#Render OBJ file(Musn't have normals and UVs)
def teapot(pos,scale,path):
    global objects
    objects += 1
    vertices,edges,faces,colors = ObjConvert.get_obj(path,scale,len(vertex_table))
    for v in range(len(vertices)):
        for c in range(3):
            vertices[v][c] = vertices[v][c]+pos[c]
    vertex_table.extend(vertices)
    edge_table.extend(edges)
    face_table.extend(faces)
    faces_color.extend(colors)

#Rotate all vertices along the Y axis based on an point
def rotate_y(degrees, origin):
    for v in range(len(vertex_table)):
        t_x,t_y,t_z = vertex_table[v]
        x,y,z = vertex_table[v]
        t_x -= origin[0]
        t_z -= origin[2]
        x = (t_x*math.cos(degrees)) + (t_z*-math.sin(degrees))
        z = (t_x*math.sin(degrees)) + (t_z*math.cos(degrees))
        x += origin[0]
        z += origin[2]
        vertex_table[v] = (x,y,z)

#Rotate all vertices along the X axis based on an point
def rotate_x(degrees, origin):
    for v in range(len(vertex_table)):
        t_x,t_y,t_z = vertex_table[v]
        x,y,z = vertex_table[v]
        t_y -= origin[1]
        t_z -= origin[2]
        y = (t_y*math.cos(degrees)) + (t_z*-math.sin(degrees))
        z = (t_y*math.sin(degrees)) + (t_z*math.cos(degrees))
        y += origin[1]
        z += origin[2]
        vertex_table[v] = (x,y,z)

#Rotate all vertices along the Z axis based on an point
def rotate_z(degrees, origin):
    for v in range(len(vertex_table)):
        t_x,t_y,t_z = vertex_table[v]
        x,y,z = vertex_table[v]
        t_x -= origin[0]
        t_y -= origin[1]
        x = (t_x*math.cos(degrees)) + (t_y*-math.sin(degrees))
        y = (t_x*math.sin(degrees)) + (t_y*math.cos(degrees))
        x += origin[0]
        y += origin[1]
        vertex_table[v] = (x,y,z)