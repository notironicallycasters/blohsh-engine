import pygame
import random
import math
import ObjConvert
import Engine

pygame.init()

speed = 300
sens = 0.1

screen = pygame.display.set_mode((1920, 1080),pygame.FULLSCREEN) #Display the window
pygame.display.set_icon(pygame.image.load("icon.png")) #Set icon
pygame.display.set_caption("Blohsh Engine") # Set title
clock = pygame.time.Clock() #Pygame clock so time don't go brr
delta = 0.1 #Delta ?

height = screen.height/2
width = screen.width/2
print(screen.size)


running = True

velocity = [0,0,0]
jump_count = 0
jump_max = -400

#Setup
#Engine.teapot([0,0,200],100,"Assets/Jotaro.obj")

for x in range(64):
    Engine.teapot([x%8*400,0,x//8*400],200,"Assets/Plane.obj")
for x in range(8):
    #Engine.teapot([x*400,-200,7*400+200],200,"Assets/Wall.obj")
    Engine.teapot([x*400,-200,-200],200,"Assets/Wall.obj")

Engine.teapot([8*200-200,-1600,7*400+200],8*200,"Assets/Wall.obj")

def move_camera(vector):
    Engine.rotate_x(-Engine.camera_rotation[0],Engine.camera)
    Engine.rotate_y(-Engine.camera_rotation[1],Engine.camera)
    Engine.camera = [Engine.camera[i]+vector[i]*delta for i in range(3)]

    Engine.rotate_y(Engine.camera_rotation[1],Engine.camera)
    Engine.rotate_x(Engine.camera_rotation[0],Engine.camera)

def get_sign(number):
    if number > 0:
        return 1
    elif number < 0:
        return -1
    else:
        return 0

#Update loop
while running:
    velocity[1] += 9.81*7*delta
    if Engine.camera[1] >= -500:
        Engine.camera[1] = -500
        velocity[1] = 0
        jump_count = 0

    screen.fill("#ffffff") #Clear the screen
    screen.blit(pygame.image.load("Assets/sky.png"),(0,0,width,height))
    pygame.event.set_grab(True) #Grab the mouse
    pygame.mouse.set_visible(False) 
    pygame.mouse.set_pos(width/2,height/2)

    for event in pygame.event.get(): #Checks for event
        if event.type == pygame.QUIT: #If the X button on the window is pressed, terminate the program
            running = False
    
    #Key handling
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        move_camera((speed*math.sin(Engine.camera_rotation[1]),0,speed*math.cos(Engine.camera_rotation[1])))
    if pressed[pygame.K_s]:
        move_camera((-speed*math.sin(Engine.camera_rotation[1]),0,-speed*math.cos(Engine.camera_rotation[1])))
    if pressed[pygame.K_d]:
        move_camera((speed*math.sin(Engine.camera_rotation[1]+math.pi/2),0,speed*math.cos(Engine.camera_rotation[1]+math.pi/2)))
    if pressed[pygame.K_a]:
        move_camera((-speed*math.sin(Engine.camera_rotation[1]+math.pi/2),0,-speed*math.cos(Engine.camera_rotation[1]+math.pi/2)))
    if pressed[pygame.K_SPACE] and jump_count >= jump_max:
        velocity[1] -= 9.81*20*delta
        jump_count -= 9.81*20*delta
    if pressed[pygame.K_ESCAPE]:
        running = False

    #Camera rotation with mouse
    mouse_vel = pygame.mouse.get_rel()
    mouse_vel = (max(min(mouse_vel[0],10),-10),max(min(mouse_vel[1],10),-10))
    if mouse_vel[0] != 0 or mouse_vel[1] != 0:
        Engine.rotate_x(-Engine.camera_rotation[0],Engine.camera)

        Engine.rotate_y(mouse_vel[0]*delta*sens,Engine.camera)
        Engine.camera_rotation[1] += mouse_vel[0]*delta*sens

        if Engine.camera_rotation[1] > 2*math.pi:
            Engine.camera_rotation[1] = 0
        elif Engine.camera_rotation[1] < 0:
            Engine.camera_rotation[1] = 2*math.pi

        Engine.rotate_x(Engine.camera_rotation[0],Engine.camera)
        
        if abs(Engine.camera_rotation[0]+(mouse_vel[1]*delta*sens)) <= 1.2:
            Engine.rotate_x(mouse_vel[1]*delta*sens,Engine.camera)
            Engine.camera_rotation[0] += mouse_vel[1]*delta*sens

        if Engine.camera_rotation[1] > 2*math.pi:
            Engine.camera_rotation[1] = 0
        elif Engine.camera_rotation[1] < 0:
            Engine.camera_rotation[1] = 2*math.pi
            

    mouse = pygame.mouse.get_pos()
    move_camera(velocity)
    
    Engine.calculate_faces()
    Engine.render_faces()
    Engine.label("FPS: "+str(int(clock.get_fps())),50,(0,0,0),(0,0))
    Engine.label("Vertices: "+str(len(Engine.vertex_table)),50,(0,0,0),(0,30))
    Engine.label("Faces: "+str(len(Engine.face_table)),50,(0,0,0),(0,60))
    Engine.label("Culled: "+str(Engine.culled),50,(0,0,0),(0,90))
    Engine.label("Objects: "+str(Engine.objects),50,(0,0,0),(0,120))
    Engine.label("Position "+str(Engine.camera),50,(0,0,0),(0,150))
    Engine.label("Rotation: "+str(Engine.camera_rotation),50,(0,0,0),(0,180))
    Engine.culled = 0

    pygame.display.flip() # Render the screen

    delta = clock.tick(60) / 60
    delta = max(0.001,min(0.1,delta))

pygame.quit() #Terminate the program once the game is no longer running