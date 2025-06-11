import pygame
import random
import math
import ObjConvert
import Engine

pygame.init()

speed = 600
sens = 0.5

screen = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN) #Display the window
pygame.display.set_icon(pygame.image.load("icon.png")) #Set icon
pygame.display.set_caption("Blohsh Engine") # Set title
clock = pygame.time.Clock() #Pygame clock so time don't go brr
delta = 0.1 #Delta ?

height = screen.height/2
width = screen.width/2
print(screen.size)

running = True


#Setup
Engine.teapot([0,0,200],100,"Assets/Jotaro.obj")

for x in range(-8,8):
    for y in range(-8,8):
        Engine.teapot([x*200,random.randint(-8,8)*200,y*200],100,"Assets/CubeQuad.obj")


#Update loop
while running:
    screen.fill("#ffffff") #Clear the screen
    pygame.event.set_grab(True) #Grab the mouse
    pygame.mouse.set_visible(False) 
    pygame.mouse.set_pos(width/2,height/2)

    for event in pygame.event.get(): #Checks for event
        if event.type == pygame.QUIT: #If the X button on the window is pressed, terminate the program
            running = False
    
    #Key handling
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        Engine.camera[2] += speed*delta
    if pressed[pygame.K_s]:
        Engine.camera[2] += -speed*delta
    if pressed[pygame.K_d]:
        Engine.camera[0] += speed*delta
    if pressed[pygame.K_a]:
        Engine.camera[0] += -speed*delta
    if pressed[pygame.K_e]:
        Engine.camera[1] += speed*delta
    if pressed[pygame.K_q]:
        Engine.camera[1] += -speed*delta
    if pressed[pygame.K_ESCAPE]:
        running = False

    #Camera rotation with mouse
    mouse_vel = pygame.mouse.get_rel()
    if mouse_vel[0] != 0 or mouse_vel[1] != 0:
        Engine.rotate_x(-Engine.camera_rotation[0],Engine.camera)

        Engine.rotate_y(mouse_vel[0]*delta*sens,Engine.camera)
        Engine.camera_rotation[1] += mouse_vel[0]*delta*sens

        Engine.rotate_x(Engine.camera_rotation[0],Engine.camera)
        
        if abs(Engine.camera_rotation[0]+(mouse_vel[1]*delta*sens)) <= 0.8:
            Engine.rotate_x(mouse_vel[1]*delta*sens,Engine.camera)
            Engine.camera_rotation[0] += mouse_vel[1]*delta*sens

    mouse = pygame.mouse.get_pos()

    
    Engine.calculate_faces()
    Engine.render_faces()
    Engine.label("FPS: "+str(int(clock.get_fps())),50,(0,0,0),(0,0))
    Engine.label("Vertices: "+str(len(Engine.vertex_table)),50,(0,0,0),(0,30))
    Engine.label("Faces: "+str(len(Engine.face_table)),50,(0,0,0),(0,60))
    Engine.label("Culled: "+str(Engine.culled),50,(0,0,0),(0,90))
    Engine.label("Objects: "+str(Engine.objects),50,(0,0,0),(0,120))
    Engine.culled = 0

    pygame.display.flip() # Render the screen

    delta = clock.tick(1000) / 1000
    delta = max(0.001,min(0.1,delta))

pygame.quit() #Terminate the program once the game is no longer running