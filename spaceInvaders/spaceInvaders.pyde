##############################################################################
# spaceInvaders.py - Space Invaders Game in Processing 3                     #
#                                                                            # 
##############################################################################

# if running on linux, uncomment the following line
# from java.lang import System
# System.setProperty("jogl.disable.openglcore", "false")

def gridConvert(x, y, z):
    global scaling_factor
    scaling_factor = 100  # Adjust the scaling factor as needed
    return [(x * scaling_factor)+70.1, (y * scaling_factor)+0.1, (z * scaling_factor)+70.1]

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

def dotProduct(x1,y1,x2,y2):
    return (float(x1)*float(x2)) + (float(y1)*float(y2))

def setup():
    size(1000, 700, P3D)
    noClip()
    # fullScreen()
    # noCursor()
    global ui
    ui = createGraphics(1000,700, P2D)

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

    global f3State
    f3State = False

def movementCalc(dir, step, rotation):
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

def AABB(player, box):
    # player = [x-20,y-40,z-20, x+20,y+40,z+20]
    # box = [x1,y1,z1,x2,y2,z2]
    # check if the player collides with the box
    if player[0] <= box[3] and player[3] >= box[0] and player[1] <= box[4] and player[4] >= box[1] and player[2] <= box[5] and player[5] >= box[2]:
        return True
    else:
        return False

def hitboxCalc(x, y, z, option=0):

    # Test if the player has collideable objects around them
    # [-1,1] [0,1] [1,1]
    # [-1,0] player [1,0]
    # [-1,-1] [0,-1] [1,-1]

    playerArray = [[-1,1], [0,1], [1,1], [-1,0], [1,0], [-1,-1], [0,-1], [1,-1]]
    tempArray = []
    # test if objects around player are collidable and add them to an array
    for item in playerArray:
        print(str(floor((x/100))) + "," + str(2) + "," + str(floor((z/100))))
        hx, hy, hz = gridConvert(int(floor((x/100)+item[1])), int(2), int(floor((z/100)+item[0])))
        if hitboxes[int(2)][int(int(floor((x/100)+item[1])))][int(floor((z/100)+item[0]))] == 1: # y, x, z
            tempArray.append([int(int(floor((x/100)+item[1]))),int(2),int(floor((z/100)+item[0]))])

    if option == 0:
        return tempArray
    elif option == 1:
        return len(tempArray)

def gravityCalc():
    global dx,dy,dz
    dy -= 0.1
    return [dx,dy,dz]

def f3(x,y,z,rotation):
    # information screen
    global f3State,ui

    # keybind toggle
    if keyPressed and key == "p":
        print("f3 toggled")
        if f3State == False:
            f3State = True
        elif f3State == True:
            f3State = False

    # display information
    if f3State == True:
        ui.beginDraw()
        ui.background(255)
        ui.textSize(20)
        ui.textAlign(CENTER,CENTER)
        ui.fill(255,0,0)
        ui.text("coordinates: " + str(floor((x+50)/100)) + "," + str(floor(y)) + "," + str(floor((z+50)/100)), 100, 100)
        ui.endDraw()

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

    ## print("delta coordinates: " + str(dx) + "," + str(dy) + "," + str(dz))
    return [dx,dy,dz]
    # camera(x, y, z, x, y, z, 0, 1, 0)  # Update camera position based on player's movement

def draw():

    background(0)

    global scaling_factor, buffer, bx, by, bz, angle, rotation, x, y, z, hitboxes
    # Define camera math
    #####################
    xCenter = ((float(mouseX) - (float(width)/2)) / float(width) ) * (4*PI)
    yCenter = ((float(mouseY) - (float(height)/2)) / float(height) ) * (2*PI)
    ## print("Angle:" + str(360*(xCenter)/2*PI))
    rotation = xCenter
    #####################

    # get hitboxes
    # localise the player position based on the camera
    dx,dy,dz = player()

    ## print("x:" + str((x+50)/100))
    ## print("z:" + str((z+50)/100))
    # translate rigid x,y,z to camera x,y,z
    if dz > 0:
        print("forward")
        
        if hitboxCalc(x,y,z,1) == 0: # y, x, z
            # calculate the movement      
            dx,dy,dz = movementCalc(0,dz, rotation)
        else:
            # test if objects around player are collidable and add them to an array
            tempArray = hitboxCalc(x,y,z)

            # test if the player will collide with any of the objects
            tx, ty, tz = movementCalc(0,dz, rotation) # temporary x y z
            e = 0
            for item in tempArray:
                hx, hy, hz = gridConvert(item[0], item[1], item[2])
                hx, hy, hz = floor(hx), floor(hy), floor(hz)
                
                renderBlock(hx,hy,hz,255,0,0)

                # print("x: " + str(x) + " y: " + str(y) + " z: " + str(z) + " dx: " + str(dx) + " dz: " + str(dz) + " hx: " + str(hx) + " hy: " + str(hy) + " hz: " + str(hz))
                feather = 60 # how far out the collision check is https://www.desmos.com/calculator/t4tosexwdn distance value is "o"
                # print("tx: " + str(tx) + " tz: " + str(tz))
                # print(AABB([((x+(2*tx))),((250)),((z+(tz*2))), ((x+(tx*2))),(250),((z+(tz*2))),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]))
                if AABB([((x+(4*tx)-10)),((200)),((z+(tz*4)-10)), ((x+(tx*4)+10)),(300),((z+(tz*4)+10)),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]) == True:
                    print("collision")
                    dx,dy,dz = 0,0,0
                else:
                    print("no")
                    e += 1
                    # dx,dy,dz = 0,0,0
            
            # only execute the movement if there are no collisions
            if e == len(tempArray):
                dx,dy,dz = movementCalc(0,dz, rotation)

    elif dz < 0:
        print("backward")

        if hitboxCalc(x,y,z,1) == 0: # y, x, z
            # calculate the movement      
            dx,dy,dz = movementCalc(1,dz, rotation)
        else:
            # test if objects around player are collidable and add them to an array
            tempArray = hitboxCalc(x,y,z)

            # test if the player will collide with any of the objects
            tx, ty, tz = movementCalc(1,dz, rotation) # temporary x y z
            e = 0
            for item in tempArray:
                hx, hy, hz = gridConvert(item[0], item[1], item[2])
                hx, hy, hz = floor(hx), floor(hy), floor(hz)
                
                renderBlock(hx,hy,hz,255,0,0)

                # print("x: " + str(x) + " y: " + str(y) + " z: " + str(z) + " dx: " + str(dx) + " dz: " + str(dz) + " hx: " + str(hx) + " hy: " + str(hy) + " hz: " + str(hz))
                feather = 60 # how far out the collision check is https://www.desmos.com/calculator/t4tosexwdn distance value is "o"
                # print("tx: " + str(tx) + " tz: " + str(tz))
                # print(AABB([((x+(2*tx))),((250)),((z+(tz*2))), ((x+(tx*2))),(250),((z+(tz*2))),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]))
                if AABB([((x+(4*tx)-10)),((200)),((z+(tz*4)-10)), ((x+(tx*4)+10)),(300),((z+(tz*4)+10)),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]) == True:
                    print("collision")
                    dx,dy,dz = 0,0,0
                else:
                    print("no")
                    e += 1
                    # dx,dy,dz = 0,0,0
            
            # only execute the movement if there are no collisions
            if e == len(tempArray):
                dx,dy,dz = movementCalc(1,dz, rotation)

    elif dx > 0:
        print("right")

        if hitboxCalc(x,y,z,1) == 0: # y, x, z
            # calculate the movement      
            dx,dy,dz = movementCalc(2,dx, rotation)
        else:
            # test if objects around player are collidable and add them to an array
            tempArray = hitboxCalc(x,y,z)

            # test if the player will collide with any of the objects
            tx, ty, tz = movementCalc(2,dx, rotation) # temporary x y z
            e = 0
            for item in tempArray:
                hx, hy, hz = gridConvert(item[0], item[1], item[2])
                hx, hy, hz = floor(hx), floor(hy), floor(hz)
                
                renderBlock(hx,hy,hz,255,0,0)

                # print("x: " + str(x) + " y: " + str(y) + " z: " + str(z) + " dx: " + str(dx) + " dz: " + str(dz) + " hx: " + str(hx) + " hy: " + str(hy) + " hz: " + str(hz))
                feather = 60 # how far out the collision check is https://www.desmos.com/calculator/t4tosexwdn distance value is "o"
                # print("tx: " + str(tx) + " tz: " + str(tz))
                # print(AABB([((x+(2*tx))),((250)),((z+(tz*2))), ((x+(tx*2))),(250),((z+(tz*2))),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]))
                if AABB([((x+(4*tx)-10)),((200)),((z+(tz*4)-10)), ((x+(tx*4)+10)),(300),((z+(tz*4)+10)),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]) == True:
                    print("collision")
                    dx,dy,dz = 0,0,0
                else:
                    print("no")
                    e += 1
                    # dx,dy,dz = 0,0,0
            
            # only execute the movement if there are no collisions
            if e == len(tempArray):
                dx,dy,dz = movementCalc(2,dx, rotation)

    elif dx < 0:
        print("left")
        
        if hitboxCalc(x,y,z,1) == 0: # y, x, z
            # calculate the movement      
            dx,dy,dz = movementCalc(3,dx, rotation)
        else:
            # test if objects around player are collidable and add them to an array
            tempArray = hitboxCalc(x,y,z)

            # test if the player will collide with any of the objects
            tx, ty, tz = movementCalc(3,dx, rotation) # temporary x y z
            e = 0
            for item in tempArray:
                hx, hy, hz = gridConvert(item[0], item[1], item[2])
                hx, hy, hz = floor(hx), floor(hy), floor(hz)
                
                renderBlock(hx,hy,hz,255,0,0)

                # print("x: " + str(x) + " y: " + str(y) + " z: " + str(z) + " dx: " + str(dx) + " dz: " + str(dz) + " hx: " + str(hx) + " hy: " + str(hy) + " hz: " + str(hz))
                feather = 60 # how far out the collision check is https://www.desmos.com/calculator/t4tosexwdn distance value is "o"
                # print("tx: " + str(tx) + " tz: " + str(tz))
                # print(AABB([((x+(2*tx))),((250)),((z+(tz*2))), ((x+(tx*2))),(250),((z+(tz*2))),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]))
                if AABB([((x+(4*tx)-10)),((200)),((z+(tz*4)-10)), ((x+(tx*4)+10)),(300),((z+(tz*4)+10)),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]) == True:
                    print("collision")
                    dx,dy,dz = 0,0,0
                else:
                    print("no")
                    e += 1
                    # dx,dy,dz = 0,0,0
            
            # only execute the movement if there are no collisions
            if e == len(tempArray):
                dx,dy,dz = movementCalc(3,dx, rotation)


    x += dx
    z += dz

    # run gravity calculations
    
    # execute camera movement
    beginCamera()
    # camera(x-60, yCenter, z-60, (50*cos(xCenter)) + x-60, (50*yCenter), (50*sin(xCenter)) + z-60, 0, 1, 0) # WHY THE FUCK DO YOU NEED -60?!?!?!
    camera(x, yCenter, z, (50*cos(xCenter)) + x, (50*yCenter), (50*sin(xCenter)) + z, 0, 1, 0) 
    ## print(yCenter)
    perspective()
    endCamera()

    # apply player hitbox movement
    # x - x+50, y - y+50, z - z+50

    print(rotation)
    print(z)
    print(x)
    # Load the map
    loadMap(0, 0, 0, 0)

    # run ui commands
    # f3(x,y,z,rotation)
    # pushMatrix()
    # image(ui,0,0)
    # translate(x,z,0)
    # rotateZ((2*PI) - rotation)
    # popMatrix()

