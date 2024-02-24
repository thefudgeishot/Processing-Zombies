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
    hitboxes = [[[0 for _ in range(20)] for _ in range(20)] for _ in range(20)]

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
    
    global ui, playerModel
    ui = createGraphics(1000,700, P2D)
    playerModel = createGraphics(1000,700, P2D)

    global x,y,z
    x,y,z = 50,0,50

    global dx,dy,dz
    dx,dy,dz = 0,0,0

    global time2, time3
    time2 = 1000
    time3 = 0

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

    global image1, image2
    image1 = loadImage("playerModel/AR/idle.png")
    image2 = loadImage("crosshair-1.png")

def movementCalc(dir, step, rotation):
    # up=0, down=1, left=2, right=3

    global dx,dz
    
    dx,dz = 0,0

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

    
    return [dx,dz]

def AABB(player, box):
    # player = [x-20,y-40,z-20, x+20,y+40,z+20]
    # box = [x1,y1,z1,x2,y2,z2]
    # check if the player collides with the box
    if player[0] <= box[3] and player[3] >= box[0] and player[1] <= box[4] and player[4] >= box[1] and player[2] <= box[5] and player[5] >= box[2]:
        return True
    else:
        return False

def hitboxCalc(x, y, z, setting=0, option=0):

    # Test if the player has collideable objects around them
    # [-1,1] [0,1] [1,1]
    # [-1,0] player [1,0]
    # [-1,-1] [0,-1] [1,-1]
    

    playerArray = [[-1,1], [0,1], [1,1], [-1,0], [1,0], [-1,-1], [0,-1], [1,-1]]
    tempArray = []
    # test if objects around player are collidable and add them to an array
    if setting == 0:
        # check around the player
        w = 0
        while w != 300:
            for item in playerArray:
                if hitboxes[int(floor((y+w)/100))][int(int(floor((x/100)+item[1])))][int(floor((z/100)+item[0]))] == 1: # y, x, z
                    tempArray.append([int(int(floor((x/100)+item[1]))),int(floor((y+w)/100)),int(floor((z/100)+item[0]))])
            w += 100

    elif setting == 1:
        # check below the player
        for item in playerArray:
            if hitboxes[int(floor((y+300)/100))][int(int(floor((x/100)+item[1])))][int(floor((z/100)+item[0]))] == 1: # y, x, z
                tempArray.append([int(int(floor((x/100)+item[1]))),int(floor((y+300)/100)),int(floor((z/100)+item[0]))])
        if hitboxes[int(floor((y+300)/100))][int(floor((x/100)))][int(floor((z/100)))] == 1:
            tempArray.append([int(floor((x/100))),int(floor((y+300)/100)),int(floor((z/100)))])
    
    elif setting == 2:
        # check above the player
        for item in playerArray:
            if hitboxes[int(floor((y-100)/100))][int(int(floor((x/100)+item[1])))][int(floor((z/100)+item[0]))] == 1: # y, x, z
                tempArray.append([int(floor((x/100)+item[1])),int(floor((y-100)/100)),int(floor((z/100)+item[0]))])
        if hitboxes[int(abs(floor((y-100)/100)))][int(floor((x/100)))][int(floor((z/100)))] == 1:
            tempArray.append([int(floor((x/100))),int(abs(floor((y-100)/100))),int(floor((z/100)))])

    # process output
    if option == 0:
        return tempArray
    elif option == 1:
        return len(tempArray)

def f3(x,y,z,rotation):
    # information screen
    global f3State,ui,time3

    # keybind toggle
    if keyPressed and key == "p":
        print("f3 toggled")
        # add interval to prevent multiple keypresses
        if millis() - time3 > 100:
            time3 = millis()
            if f3State == False:
                f3State = True
            elif f3State == True:
                f3State = False

    # display information
    if f3State == True:
        # setup the ui
        ui.beginDraw()
        ui.clear()
        ui.textSize(30)
        ui.textAlign(RIGHT)
        ui.fill(255,0,0)
        ui.text("coordinates: " + str(floor((x+50)/100)) + "," + str(-1*floor(y/100)) + "," + str(floor((z+50)/100)), 300, 30)
        ui.text("rotation: " + str(round(rotation*(180/PI))), 220, 70)
        ui.endDraw()
    elif f3State == False:
        # setup the ui
        ui.beginDraw()
        ui.clear()
        ui.endDraw()

    # display the ui
    pushMatrix()
    camera()
    hint(DISABLE_DEPTH_TEST)
    noLights()
    image(ui,0,0)
    hint(ENABLE_DEPTH_TEST)
    popMatrix()

def playerUi():
    # player model
    global playerModel, image1, image2

    playerModel.beginDraw()
    playerModel.clear()
    playerModel.image(image1, 0, 0, width, height)
    playerModel.image(image2, (width/2)-50, (height/2)-50, 30, 30)
    playerModel.endDraw()

    # display the player model
    pushMatrix()
    camera()
    hint(DISABLE_DEPTH_TEST)
    noLights()
    image(playerModel,0,0) 
    hint(ENABLE_DEPTH_TEST)
    popMatrix()

def player():
    # player settings

    global time2

    dx,dy,dz = 0,0,0
    step = 7.5
    # keyboard controls
    if keyPressed:
        if key == "w":
            # dx,dy,dz = movementCalc(0,step)
            dz += step
        if key == "s":
            # dx,dy,dz = movementCalc(1,step) 
            dz -= step
        if key == "a":
            # dx,dy,dz = movement(2,step)
            dx -= step
        if key == "d":
            # dx,dy,dz = movement(3,step)
            dx += step
    
    # jump
    if (keyPressed == True and key == " ") or (millis() - time2) < 500:
        if (keyPressed == True and key == " " and (millis() - time2) > 500):
            if hitboxCalc(x,y,z,1,1) != 0:
                print("timer reset")
                time2 = millis()

        if (millis() - time2) < 500:
            # https://www.desmos.com/calculator/jlcyciwaaq
            dt = -5 + (millis() - time2)/58
            height = 10
            width = 1
            steepness = 1
            dy -= float(height / (1 + exp((steepness*(dt-10))/width)) - float(height / (1 + exp((steepness*dt)/width))))
        #dy += -60

    ## print("delta coordinates: " + str(dx) + "," + str(dy) + "," + str(dz))
    return [dx,dy,dz]
    # camera(x, y, z, x, y, z, 0, 1, 0)  # Update camera position based on player's movement


def draw():

    background(0)

    global scaling_factor, buffer, bx, by, bz, angle, rotation, x, y, z, hitboxes, time
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

    # run gravity calculations

    # renderBlock(x,((y+300)),z,255,0,0)
    if hitboxCalc(x,y,z,1,1) >= 1: # y, x, z
        time = millis() # set time since last on ground
        print("set time")

    if hitboxCalc(x,y,z,1,1) == 0: # y, x, z
        if dy == 0:
            dt = ((millis() - time)/500)+2
            gravity = 9.8
            dy += gravity * dt
    else:
        if dy == 0:
            tempArray = hitboxCalc(x,y,z,1,0)
            e = 0
            for item in tempArray:
                hx, hy, hz = gridConvert(item[0], item[1], item[2])
                hx, hy, hz = floor(hx), floor(hy), floor(hz)
                renderBlock(hx,hy,hz,255,0,0)

                feather = 60

                if AABB([(x-10),(y-10),(z-10), ((x+10)),(y+210),((z+10))], [hx-feather,hy-feather,hz-feather, hx+feather,hy+feather,hz+feather]) == False:
                    e += 1
                
            if e == len(tempArray):
                dt = ((millis() - time)/500)+2
                gravity = 9.8
                dy += gravity * dt



    # Run player movement
    if dz > 0:
        print("forward")
        
        if hitboxCalc(x,y,z,0,1) == 0: # y, x, z
            # calculate the movement      
            dx,dz = movementCalc(0,dz, rotation)
        else:
            # test if objects around player are collidable and add them to an array
            tempArray = hitboxCalc(x,y,z)

            # test if the player will collide with any of the objects
            tx,tz = movementCalc(0,dz, rotation) # temporary x y z
            e = 0
            for item in tempArray:
                hx, hy, hz = gridConvert(item[0], item[1], item[2])
                hx, hy, hz = floor(hx), floor(hy), floor(hz)
                
                renderBlock(hx,hy,hz,255,0,0)

                # print("x: " + str(x) + " y: " + str(y) + " z: " + str(z) + " dx: " + str(dx) + " dz: " + str(dz) + " hx: " + str(hx) + " hy: " + str(hy) + " hz: " + str(hz))
                feather = 60 # how far out the collision check is https://www.desmos.com/calculator/t4tosexwdn distance value is "o"
                # print("tx: " + str(tx) + " tz: " + str(tz))
                # print(AABB([((x+(2*tx))),((250)),((z+(tz*2))), ((x+(tx*2))),(250),((z+(tz*2))),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]))
                if AABB([((x+(4*tx)-10)),((y)),((z+(tz*4)-10)), ((x+(tx*4)+10)),(y+200),((z+(tz*4)+10)),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]) == True:
                    print("collision")
                    dx,dz = 0,0
                else:
                    print("no")
                    e += 1
                    # dx,dy,dz = 0,0,0
            
            # only execute the movement if there are no collisions
            if e == len(tempArray):
                dx,dz = movementCalc(0,dz, rotation)

    elif dz < 0:
        print("backward")

        if hitboxCalc(x,y,z,1) == 0: # y, x, z
            # calculate the movement      
            dx,dz = movementCalc(1,dz, rotation)
        else:
            # test if objects around player are collidable and add them to an array
            tempArray = hitboxCalc(x,y,z)

            # test if the player will collide with any of the objects
            tx,tz = movementCalc(1,dz, rotation) # temporary x y z
            e = 0
            for item in tempArray:
                hx, hy, hz = gridConvert(item[0], item[1], item[2])
                hx, hy, hz = floor(hx), floor(hy), floor(hz)
                
                renderBlock(hx,hy,hz,255,0,0)

                # print("x: " + str(x) + " y: " + str(y) + " z: " + str(z) + " dx: " + str(dx) + " dz: " + str(dz) + " hx: " + str(hx) + " hy: " + str(hy) + " hz: " + str(hz))
                feather = 60 # how far out the collision check is https://www.desmos.com/calculator/t4tosexwdn distance value is "o"
                # print("tx: " + str(tx) + " tz: " + str(tz))
                # print(AABB([((x+(2*tx))),((250)),((z+(tz*2))), ((x+(tx*2))),(250),((z+(tz*2))),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]))
                if AABB([((x+(4*tx)-10)),((y)),((z+(tz*4)-10)), ((x+(tx*4)+10)),(y+200),((z+(tz*4)+10)),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]) == True:
                    print("collision")
                    dx,dz = 0,0
                else:
                    print("no")
                    e += 1
                    # dx,dy,dz = 0,0,0
            
            # only execute the movement if there are no collisions
            if e == len(tempArray):
                dx,dz = movementCalc(1,dz, rotation)

    elif dx > 0:
        print("right")

        if hitboxCalc(x,y,z,1) == 0: # y, x, z
            # calculate the movement      
            dx,dz = movementCalc(2,dx, rotation)
        else:
            # test if objects around player are collidable and add them to an array
            tempArray = hitboxCalc(x,y,z)

            # test if the player will collide with any of the objects
            tx,tz = movementCalc(2,dx, rotation) # temporary x y z
            e = 0
            for item in tempArray:
                hx, hy, hz = gridConvert(item[0], item[1], item[2])
                hx, hy, hz = floor(hx), floor(hy), floor(hz)
                
                renderBlock(hx,hy,hz,255,0,0)

                # print("x: " + str(x) + " y: " + str(y) + " z: " + str(z) + " dx: " + str(dx) + " dz: " + str(dz) + " hx: " + str(hx) + " hy: " + str(hy) + " hz: " + str(hz))
                feather = 60 # how far out the collision check is https://www.desmos.com/calculator/t4tosexwdn distance value is "o"
                # print("tx: " + str(tx) + " tz: " + str(tz))
                # print(AABB([((x+(2*tx))),((250)),((z+(tz*2))), ((x+(tx*2))),(250),((z+(tz*2))),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]))
                if AABB([((x+(4*tx)-10)),((y)),((z+(tz*4)-10)), ((x+(tx*4)+10)),(y+200),((z+(tz*4)+10)),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]) == True:
                    print("collision")
                    dx,dz = 0,0
                else:
                    print("no")
                    e += 1
                    # dx,dy,dz = 0,0,0
            
            # only execute the movement if there are no collisions
            if e == len(tempArray):
                dx,dz = movementCalc(2,dx, rotation)

    elif dx < 0:
        print("left")
        
        if hitboxCalc(x,y,z,1) == 0: # y, x, z
            # calculate the movement      
            dx,dz = movementCalc(3,dx, rotation)
        else:
            # test if objects around player are collidable and add them to an array
            tempArray = hitboxCalc(x,y,z)

            # test if the player will collide with any of the objects
            tx, tz = movementCalc(3,dx, rotation) # temporary x y z
            e = 0
            for item in tempArray:
                hx, hy, hz = gridConvert(item[0], item[1], item[2])
                hx, hy, hz = floor(hx), floor(hy), floor(hz)
                
                renderBlock(hx,hy,hz,255,0,0)

                # print("x: " + str(x) + " y: " + str(y) + " z: " + str(z) + " dx: " + str(dx) + " dz: " + str(dz) + " hx: " + str(hx) + " hy: " + str(hy) + " hz: " + str(hz))
                feather = 60 # how far out the collision check is https://www.desmos.com/calculator/t4tosexwdn distance value is "o"
                # print("tx: " + str(tx) + " tz: " + str(tz))
                # print(AABB([((x+(2*tx))),((250)),((z+(tz*2))), ((x+(tx*2))),(250),((z+(tz*2))),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]))
                if AABB([((x+(4*tx)-10)),((y)),((z+(tz*4)-10)), ((x+(tx*4)+10)),(y+200),((z+(tz*4)+10)),], [hx-feather,hy-feather,hz-feather,hx+feather,hy+feather,hz+feather]) == True:
                    print("collision")
                    dx,dz = 0,0
                else:
                    print("no")
                    e += 1
                    # dx,dy,dz = 0,0,0
            
            # only execute the movement if there are no collisions
            if e == len(tempArray):
                dx,dz = movementCalc(3,dx, rotation)


    x += dx
    z += dz
    y += dy

    
    # execute camera movement
    beginCamera()
    # camera(x-60, yCenter, z-60, (50*cos(xCenter)) + x-60, (50*yCenter), (50*sin(xCenter)) + z-60, 0, 1, 0) # WHY THE FUCK DO YOU NEED -60?!?!?!
    camera(x, y, z, (50*cos(xCenter)) + x, (50*yCenter)+y, (50*sin(xCenter)) + z, 0, 1, 0) 
    ## print(yCenter)
    perspective()
    endCamera()

    # apply player hitbox movement
    # x - x+50, y - y+50, z - z+50

    print("rotation:" + str(rotation))
    print("x: " + str(x) + " y: " + str(y) + " z: " + str(z))
    # Load the map
    loadMap(0, 0, 0, 0)

    # run ui commands
    f3(x,y,z,rotation)
    playerUi()



