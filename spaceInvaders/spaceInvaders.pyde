##############################################################################
# spaceInvaders.py - Space Invaders Game in Processing 3                     #
#                                                                            # 
##############################################################################

# if running on linux, uncomment the following line
# from java.lang import System
# System.setProperty("jogl.disable.openglcore", "false")

def gridConvert(x, y, z):
    global scaling_factor
    scaling_factor = 100.1  # Adjust the scaling factor as needed
    return [x * scaling_factor, y * scaling_factor, z * scaling_factor]

def renderBlock(x,y,z,r,g,b):
    
    global hitboxes

    #print("Rendering block at: " + str(x) + ", " + str(y) + ", " + str(z))
    # block settings
    pushMatrix()
    fill(r,g,b)
    noStroke()
    translate(x,y,z)
    box(100)
    popMatrix()

    # define the hitbox
    hitboxes.append([x,y,z,(x+50),(y+50),(z+50)])

def loadHitboxes(key):

    # Create a 3D array with dimensions 50x50x10, or as x,z,y
    hitboxes = [[[0 for _ in range(20)] for _ in range(20)] for _ in range(10)]

    # Define the maps in a array
    maps = ["test", "test2", "flight"]

    # Load the map
    mapData = loadStrings("maps/" + maps[key] + ".txt")

    for line in mapData:
        # split and convert the data
        data = str(line).strip("[]").split(",")
        x,y,z = int(data[0]), int(data[1]), int(data[2])
        hitboxes[y][x][z] = 1

    return hitboxes

def loadMap(key, xOffset, yOffset, zOffset):
    
    # background(0)

    # Define the maps in a array
    maps = ["test", "test2", "flight"]

    # Load the map
    mapData = loadStrings("maps/" + maps[key] + ".txt")

    for line in mapData:
        # split and convert the data
        data = str(line).strip("[]").split(",")
        x,y,z = gridConvert(int(data[0]), int(data[1]), int(data[2]))
        r,g,b = int(data[3]), int(data[4]), int(data[5])

        # Render the block
        x += xOffset
        y += yOffset
        z += zOffset
        renderBlock(x,y,z,r,g,b)

# def collision(hitboxes, playerX, playerY, playerZ):
#     for hitbox in hitboxes:
#         if playerX >= hitbox[0] and playerX hitbox[3]:
#             return x
#         if playerY >= hitbox[1] and playerY <= hitbox[4]:
#             return y
#         if playerZ >= hitbox[2] and playerZ <= hitbox[5]:
#             return z

def dotProduct(x1,y1,x2,y2):
    return (float(x1)*float(x2)) + (float(y1)*float(y2))

def setup():
    size(1000, 700, P3D)
    # fullScreen()
    # noCursor()

    global x,y,z
    x,y,z = 0,0,0

    global dx,dy,dz
    dx,dy,dz = 0,0,0

    global hitboxes
    hitboxes = loadHitboxes(0) # hitboxes only need to be loaded once
    print(hitboxes[2][4][0])
    # exit()

    global buffer, bx, by, bz, angle
    buffer = [0]
    bx = [0]
    by = [0,0]
    bz = [0]
    angle = [0]

def movementCalc(dir,step, rotation):
    # up=0, down=1, left=2, right=3

    global dx,dy,dz
    
    dx,dy,dz = 0,0,0

    if dir == 0:
        dx += step*cos(rotation)
        dz += step*sin(rotation)
    elif dir == 1:
        dx += step*cos(rotation)
        dz += step*sin(rotation)
    elif dir == 2:
        dx += step*cos(rotation+(PI/2))
        dz += step*sin(rotation+(PI/2))
    elif dir == 3:
        dx += step*cos(rotation+(PI/2))
        dz += step*sin(rotation+(PI/2))

    
    return [dx,dy,dz]

def gravityCalc():
    global dx,dy,dz
    dy -= 0.1
    return [dx,dy,dz]

def player():
    # player settings

    dx,dy,dz = 0,0,0
    step = 7.5
    # keyboard controls
    if keyPressed:
        if key == "w":
            # dx,dy,dz = movementCalc(0,step)
            dz += step
        elif key == "s":
            # dx,dy,dz = movementCalc(1,step)
            dz -= step
        elif key == "a":
            # dx,dy,dz = movement(2,step)
            dx -= step
        elif key == "d":
            # dx,dy,dz = movement(3,step)
            dx += step

    print("delta coordinates: " + str(dx) + "," + str(dy) + "," + str(dz))
    return [dx,dy,dz]
    # camera(x, y, z, x, y, z, 0, 1, 0)  # Update camera position based on player's movement

def draw():

    background(0)

    global scaling_factor, buffer, bx, by, bz, angle, rotation, x, y, z, hitboxes
    # Define camera math
    #####################
    xCenter = ((float(mouseX) - (float(width)/2)) / float(width) ) * (4*PI)
    yCenter = ((float(mouseY) - (float(height)/2)) / float(height) ) * (2*PI)
    print("Angle:" + str(360*(xCenter)/2*PI))
    rotation = xCenter
    #####################

    # get hitboxes
    # localise the player position based on the camera
    dx,dy,dz = player()

    # translate rigid x,y,z to camera x,y,z
    if dz > 0:
        print("forward")
        # check if there is a block in the way
        print("x: " + str(int(x/100)+int(cos(rotation))) + " y: " + str(2) + " z: " + str(int((z/100)+int(sin(rotation)))))
        if int(hitboxes[int(2)][int(x/100)+int(1.1*cos(rotation))][int((z/100)+int(1.2*sin(rotation)))]) == 0: # y, x, z
            dx,dy,dz = movementCalc(0,dz, rotation)
        else:
            print("collision")
            dx,dy,dz = 0,0,0
    elif dz < 0:
        print("backward")
        dx,dy,dz = movementCalc(1,dz, rotation)
    elif dx > 0:
        print("right")
        dx,dy,dz = movementCalc(2,dx, rotation)
    elif dx < 0:
        print("left")
        # check if there is a block in the way
        print("x: " + str(x) + " y: " + str(y) + " z: " + str(z))
        if int(hitboxes[int(2)][int((x/100)+1)][int(z/100)]) == 0:
            dx,dy,dz = movementCalc(3,dx, rotation)
        else:
            print("collision")
            dx,dy,dz = 0,0,0

    x += dx
    z += dz

    # run gravity calculations
    

    beginCamera()
    camera(x, yCenter, z, (50*cos(xCenter)) + x, (50*yCenter), (50*sin(xCenter)) + z, 0, 1, 0)
    print(yCenter)
    perspective()
    endCamera()

    print(z)
    print(x)
    # Load the map
    loadMap(0, 0, 0, 0)


