##############################################################################
# spaceInvaders.py - Space Invaders Game in Processing 3                     #
#                                                                            # 
##############################################################################

# if running on linux, uncomment the following two lines
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

    # Create a 3D array with dimensions 50x50x50, or as x,z,y
    hitboxes = [[[0 for _ in range(50)] for _ in range(50)] for _ in range(50)]

    # Define the maps in a array
    maps = ["test", "test6", "de_dust2", "test3"]

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
    maps = ["test", "test6", "de_dust2", "test3"]

    # Load the map
    mapData = loadStrings("maps/" + maps[key] + ".txt")

    benchmarkStart1 = millis()
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
        
    print("This frame took " + str(millis() - benchmarkStart1) + " miliseconds to complete")

def genNavMesh(hitboxes):

    navmesh = [[1 for _ in range(50)] for _ in range(50)]

    # iterate through y level looking for blocks with a free space above them(walkable blocks)
    for i in range(0,50): #y
        # check if layer has any walkable blocks if not skip the layer
        tolerance = 0
        for item in hitboxes[i]:
            if sum(item) >= 1:
                tolerance += 1
        if tolerance == 0:
            continue
        for j in range(0,50): #x
            for k in range(0,50): #z
                if hitboxes[i][j][k] == 1 and hitboxes[i-1][j][k] == 0: # y, x, z
                    navmesh[j][k] = [[0],j,i,k] # [walkable, x, y, z]
                #else: 
                    #temp.append([[0],j,i,k]) # [not walkable?, x, y, z]
            #navmesh.append(temp)
    return navmesh

def dotProduct(x1,y1,x2,y2):
    return (float(x1)*float(x2)) + (float(y1)*float(y2))

def setup():
    size(1000, 700, P3D)
    noClip()
    # fullScreen()
    # noCursor()
    frameRate(60)

    global ui, playerModel
    ui = createGraphics(1000,700, P2D)
    playerModel = createGraphics(1000,700, P2D)

    global x,y,z
    x,y,z = 300,0,400

    global dx,dy,dz
    dx,dy,dz = 0,0,0

    global time2, time3, time, time4, time5
    time = 0
    time2 = 1000
    time3 = 0
    time4 = 0
    time5 = 0

    global hitboxes
    hitboxes = loadHitboxes(2) # hitboxes only need to be loaded once
    #print(hitboxes[2][4][0])
    # exit()

    global navMesh
    navMesh = genNavMesh(hitboxes) # navmesh only needs to be generated once

    global buffer, bx, by, bz, angle
    buffer = [0]
    bx = [0]
    by = [0,0]
    bz = [0]
    angle = [0]

    global f3State
    f3State = True

    global image1, image2
    image1 = loadImage("playerModel/AR/idle.png")
    image2 = loadImage("crosshair-1.png")

    global moveUp, moveDown, moveLeft, moveRight, jumping
    moveUp, moveDown, moveLeft, moveRight, jumping = False, False, False, False, False

    global entity
    entity = []

    global wave
    wave = 0

    global zombie
    zombie = loadShape("low_poly_zombie.obj")


# keybinds
def keyPressed():
    global moveUp, moveDown, moveLeft, moveRight, jumping
    if key == "w":
        moveUp = True
    if key == "s":
        moveDown = True
    if key == "a":
        moveLeft = True
    if key == "d":
        moveRight = True
    if key == " ":
        jumping = True

def keyReleased():
    global moveUp, moveDown, moveLeft, moveRight, jumping
    if key == "w":
        moveUp = False
    if key == "s":
        moveDown = False
    if key == "a":
        moveLeft = False
    if key == "d":
        moveRight = False
    if key == " ":
        jumping = False

def movementCalc(dir, step, rotation):
    # up=0, down=1, left=2, right=3

    # global dx,dz
    
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

def Astar(ySlice, start, end):

    # written with reference to https://youtu.be/-L-WgKMFuhE?si=UlBWzKz5x3yjQHLc&t=455
    # ySlice is the slice of the 3D array
    # start [x,y,z]
    # end [x,y,z]

    openList = [] # [x,y,z,f,g,h,parent]
    closedList = []
    blank = 0,0,0
    path = []

    ySlice = navMesh 
    print(ySlice)
    temp = ySlice[0][20]
    print(temp[0])
    #exit()
    # debug
    # start = 1,0,1
    # end = 3,0,9 
    # ySlice = [[0,0,0,0,0,0,0,0,0,0,0]
    #          ,[0,0,0,0,0,0,0,1,1,0,0]
    #          ,[0,0,1,1,1,1,1,1,1,0,0]
    #          ,[0,0,1,0,0,0,1,1,1,0,0]
    #          ,[0,0,0,0,0,0,0,0,0,0,0]
    #          ,[0,0,0,0,0,0,0,0,0,0,0]]
    
    # add the start node to the open list
    openList.append([int(start[0]),int(start[1]),int(start[2]),0,0,0,blank])


    while openList:
        
        # sort list by lowest f value 
        openList.sort(key=lambda x: x[3])


        # set current node from the open list
        current = openList[0]
        # remove the current node from the open list
        openList.remove(current)
        # add the current node to the closed list
        closedList.append(current)

        # check if the current node is the end node
        if current[0] == end[0] and current[1] == end[1] and current[2] == end[2]:
            print("path found")
            # generate the path
            if current[0] == end[0] and current[1] == end[1] and current[2] == end[2]:
                temp = navMesh[current[0]][current[2]]
                path.append([temp[1],temp[2],temp[3]])
                #path.append([current[0],current[1],current[2]])
                
                # search for the coordinates in closedList and then set the closed list item as the current node
                for item in closedList:
                    if item[0] == current[6][0] and item[1] == current[6][1] and item[2] == current[6][2]:
                        temp = navMesh[current[0]][current[2]]
                        path.append([temp[1],temp[2],temp[3]])
                        #path.append([item[0],item[1],item[2]])
                        current = item

            while closedList:
                for item in closedList:
                    if item[0] == current[6][0] and item[1] == current[6][1] and item[2] == current[6][2]:
                        temp = navMesh[current[0]][current[2]]
                        path.append([temp[1],temp[2],temp[3]])
                        #path.append([item[0],item[1],item[2]])
                        current = item
                
                if current[0] == start[0] and current[2] == start[2]:
                    #print(closedList)    
                    return path
        
        # generate the children of the current node
        for i in range(-1,2):
            for j in range(-1,2):
                # check if the child is the current node
                try:
                    if i == 0 and j == 0:
                        continue
                    # ensure coordinates are not negative
                    if int(current[0])+i < 0 or int(current[2]+j) < 0:
                        continue

                    # check if the child is collidable
                    temp = ySlice[int(current[0])+i][int(current[2]+j)]
                    #print(temp)
                    if len(str(temp)) == 1:
                        if temp == 1:                
                            continue

                    # check if the child is within the bounds of the grid
                    # if ySlice[int(current[0])+i][int(current[2]+j)][0] != 0:
                    #     continue

                    # check if y level differenence is no greater than 1 block, else its not viable
                    try:
                        temp = navMesh[int(current[0])+i][int(current[2]+j)]
                        temp1 = navMesh[int(current[0])][int(current[2])]
                        #print(str(temp) + " " + str(temp1))
                        if len(str(temp)) >= 4 and len(str(temp1)) >= 4:
                            if int(abs(int(temp[2]) - int(temp1[2]))) > 1:
                                continue
                    except TypeError:
                        continue

                    # check if the child is in the closed list
                    tolerance = 0
                    for block in closedList:
                        if block[0] == int(current[0])+i and block[2] == int(current[2]+j):
                            tolerance += 1
                            continue
                    if tolerance >= 1:
                        continue

                    # check if the child is in the open list
                    tolerance = 0
                    for block in openList:
                        if block[0] == int(current[0])+i and block[2] == int(current[2]+j):
                            tolerance += 1
                            continue
                    if tolerance >= 1:
                        continue
                    
                except IndexError:
                    continue

                # calculate the f,g,h values
                g = current[4] + sqrt(i**2 + j**2)
                h = sqrt((current[0]+i-end[0])**2 + (current[2]+j-end[2])**2)
                f = (g*10) + (h*10)
                parent = current[0],current[1],current[2]

                # add the child to the open list
                #print("child: " + str([int(current[0])+i,current[1],int(current[2]+j),f,g,h,parent]))
                openList.append([int(current[0])+i,current[1],int(current[2]+j),f,g,h,parent])
        
def AABB(player, box):
    # player = [x-20,y-40,z-20, x+20,y+40,z+20]
    # box = [x1,y1,z1,x2,y2,z2]
    # check if the player collides with the box
    if player[0] <= box[3] and player[3] >= box[0] and player[1] <= box[4] and player[4] >= box[1] and player[2] <= box[5] and player[5] >= box[2]:
        return True
    else:
        return False

def raycast(x,y,z, angleX, angleY):
    # angleX and angleY are in radians (yaw and pitch)
    # x,y,z are the players coordinates
    raycastDistance = 0

    global entity

    ## crosshair offsets
    angleX -= 0.06
    angleY -= 0.06
    # calculate the direction of the ray
    dx = cos(angleX) * cos(angleY)
    dy = sin(angleY)
    dz = sin(angleX) * cos(angleY)

    while raycastDistance < 3000:
        # calculate the position of the ray
        rx = x + (dx * raycastDistance)
        ry = (y) + (dy * raycastDistance)
        rz = z + (dz * raycastDistance)

        # check if the ray is colliding with a block or entity
        e = 0
        for item in entity:
            ex,ey,ez,rotation,type,id,path,timer1,timer2 = item
            # ex,ey,ez = gridConvert(int(ex),int(ey),int(ez))
            rotation,type,id = float(rotation),int(type),int(id)
            # pushMatrix()
            # fill(0,255,0)
            # translate(ex-60,ey-50,ez-60)
            # box(20)
            # popMatrix()
            # pushMatrix()
            # fill(0,255,0)
            # translate(ex+50,ey+140,ez+50)
            # box(20)
            # popMatrix()
# 
            # pushMatrix()
            # fill(0,0,255)
            # translate(rx,ry,rz)
            # box(20)
            # popMatrix()

            if AABB([(rx-10),(ry-10),(rz-10), (rx+10),(ry+10),(rz+10)], [(ex-60),(ey-50),(ez-60), (ex+50),(ey+140),(ez+50)]) == True:
                e += 1

        try:
            if hitboxes[int(floor(ry/100))][int(floor(rx/100))][int(floor(rz/100))] == 1 or e != 0:
                if e != 0:
                    print("entity collision")
                if hitboxes[int(floor(ry/100))][int(floor(rx/100))][int(floor(rz/100))] == 1:
                    print("block collision")
                return [rx,ry,rz]
            else:
                raycastDistance += 100
        except IndexError: 
                raycastDistance = 3000
                pass

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
                try:
                    if hitboxes[int(floor((y+w)/100))][int(int(floor((x/100)+item[1])))][int(floor((z/100)+item[0]))] == 1: # y, x, z
                        tempArray.append([int(int(floor((x/100)+item[1]))),int(floor((y+w)/100)),int(floor((z/100)+item[0]))])
                except IndexError: 
                    pass
            w += 100

    elif setting == 1:
        # check below the player
        for item in playerArray:
            try:
                if hitboxes[int(floor((y+300)/100))][int(int(floor((x/100)+item[1])))][int(floor((z/100)+item[0]))] == 1: # y, x, z
                    tempArray.append([int(int(floor((x/100)+item[1]))),int(floor((y+300)/100)),int(floor((z/100)+item[0]))])
            except IndexError: 
                pass
        try:
            if hitboxes[int(floor((y+300)/100))][int(floor((x/100)))][int(floor((z/100)))] == 1:
                tempArray.append([int(floor((x/100))),int(floor((y+300)/100)),int(floor((z/100)))])
        except IndexError: 
                pass
    
    elif setting == 2:
        # check above the player
        for item in playerArray:
            try:
                if hitboxes[int(floor((y-100)/100))][int(int(floor((x/100)+item[1])))][int(floor((z/100)+item[0]))] == 1: # y, x, z
                    tempArray.append([int(floor((x/100)+item[1])),int(floor((y-100)/100)),int(floor((z/100)+item[0]))])
            except IndexError: 
                pass
        try:
            if hitboxes[int(abs(floor((y-100)/100)))][int(floor((x/100)))][int(floor((z/100)))] == 1:
                tempArray.append([int(floor((x/100))),int(abs(floor((y-100)/100))),int(floor((z/100)))])
        except IndexError: 
                pass

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
        ui.text("fps: " + str(round(frameRate)), 220, 110)
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

def playerUi(timer=0,wave=0):
    # player model
    global playerModel, image1, image2

    playerModel.beginDraw()
    playerModel.clear()
    playerModel.image(image1, 0, 0, width, height)
    playerModel.image(image2, (width/2)-50, (height/2)-50, 30, 30)
    playerModel.endDraw()

    if timer != 0:
        playerModel.beginDraw()
        playerModel.fill(0,0,0)
        playerModel.textSize(30)
        playerModel.textAlign(CENTER)
        playerModel.text(timer, (width/2), 50)
        playerModel.endDraw()
    
    if wave != 1:
        playerModel.beginDraw()
        playerModel.fill(0,0,0)
        playerModel.textSize(30)
        playerModel.textAlign(CENTER)
        playerModel.text("wave: " + str(wave), (width/2), 100)
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

    global time2, moveUp, moveDown, moveLeft, moveRight, jumping

    dx,dy,dz = 0,0,0
    step = 7.5
    # keyboard controls
    if moveUp == True:
        dz += step
    if moveDown == True:
        dz -= step
    if moveLeft == True:
        dx -= step
    if moveRight == True:
        dx += step

    
    # jump
    if (jumping == True) or (millis() - time2) < 500:
        if (jumping == True and (millis() - time2) > 500):
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

def spawnZombies(entity):
    
    # zombie settings
    for item in entity:
        x,y,z,rotation,type,id,path,timer1,timer2 = item
        # x,y,z = gridConvert(int(x),int(y),int(z))
        rotation,type,id = float(rotation),int(type),int(id)
        if type == 0:
            # regular zombie

            # render the zombie
            print("zombie at " + str(x) + "," + str(y) + "," + str(z) + " rotation: " + str(rotation))
            pushMatrix()
            translate(x,y+160,z)
            rotateY(rotation)
            rotateX(PI)
            scale(60)
            shape(zombie)
            popMatrix()

            #renderBlock(x,y,z,255,0,0)

def zombieMove(player): # TODO: potentially needs a refactor to organise some variables, y axis does not reset and stacks on top of each other

    global entity, hitboxes
    # move zombies
    for item in entity:
        print("item length: " + str(len(item[6])))
        print(item[6])
        print(entity)
        id = item[5]
        if item[6] == [] or len(item[6]) == 1:
            # calculate the path
            Zx,Zy,Zz,rotation,type,id,path,timer1,timer2 = item
            player = (int(floor((player[0])/100)),int(int(floor(Zy/100))+1),int(floor((player[2])/100)))
            zombie = (int(floor((Zx/100))),int(int(floor(Zy/100))+1),int(floor((Zz/100))))
            print("player: " + str(player))
            print("zombie: " + str(zombie))
            print("hitboxes: " + str(hitboxes[int(floor(Zy/100))+1]))
            path = Astar(hitboxes[int(floor(Zy/100))+1], zombie, player)
            if path == None:
                print("path not found")
                continue
            print("zombie path is: " + str(path))
            for index in entity:
                if index[5] == id:
                    index[6] = path[::-1]
                    print("path set")
                    print(entity)
        
        elif item[6] != []:

            # process the path
            Zx,Zy,Zz,rotation,type,id,path,timer1,timer2 = item
            Zx,Zy,Zz = int(Zx),int(Zy)+200,int(Zz)
            # print(path)
            Tx,Ty,Tz = path[0]
            Tx,Ty,Tz = gridConvert(int(Tx),int(Ty),int(Tz))
            #Tx,Ty,Tz = int(Tx)-69.9,int(Ty)+0.1,int(Tz)-69.9
            print("zombie at " + str(Zx) + "," + str(Zy) + "," + str(Zz) + " rotation: " + str(rotation), "target: " + str(Tx) + "," + str(Ty) + "," + str(Tz))

            # check if the zombie is at the target
            feather = 20
            if (Tx-feather <= Zx <= Tx+feather) and (Ty-feather <= Zy <= Ty+feather) and (Tz-feather <= Zz <= Tz+feather):
                print("zombie at target")
                # remove the target from the path
                path.pop(0)
                continue

            # set speed of the zombie
            #dx = (Tx - Zx)
            #dz = (Tz - Zz)
            #dy = (Ty - Zy)
            dx,dy,dz = 0,0,0

            # look at player
            print(str(Zx-player[0]) + " " + str(Zz-player[2]))
            offset = PI/2
            rot = atan2(Zx - Tx,Zz - Tz) + offset
            
            print("Zombie rotation: " + str(rot))

            # TODO: add y movement

            # make the zombie jump
            if ((Ty - Zy) < -20) or (millis() - timer1) < 500:
                print("step one")
                if (((Ty - Zy) < -20) and (millis() - timer1) > 500):
                    print("step two")
                    # print(hitboxCalc(floor(Zx)/100,floor(Zy+2)/ 100,floor(Zz)/100,1,1))
                    # if hitboxCalc(floor(Zx)/100,floor(Zy)/100,floor(Zz)/100,1,1) != 0:
                    print("timer reset")
                    timer1 = millis()
                    item[7] = timer1

                if (millis() - timer1) < 500:
                    # https://www.desmos.com/calculator/jlcyciwaaq
                    dt = -5 + (millis() - timer1)/58
                    height = 15
                    width = 1
                    steepness = 1
                    dy -= float(height / (1 + exp((steepness*(dt-10))/width)) - float(height / (1 + exp((steepness*dt)/width))))

            print("Zx: " + str(Zx) + " Zy: " + str(Zy) + " Zz: " + str(Zz) + " id: " + str(id) + " path: " + str(path))

            # TODO: add a seperate timer from the jump timer
            # run gravity calculations
            print(Zx)
            if hitboxes[floor(Zy)/100][floor(Zx)/100][floor(Zz)/100] == 1: # y, x, z
                print("set time")
                timer2 = millis()
                item[8] = timer2

        
            #renderBlock(Zx,Zy-250,Zz,255,0,0)
            if ((Ty - Zy) > 20) and hitboxes[floor(Zy)/100][floor(Zx)/100][floor(Zz)/100] == 0: 
                dt = ((millis() - timer2)/500)+2
                gravity = 9.8
                print(str(gravity * dt))
                dy += gravity * dt
            
            #item[1] = Zy

            # move the zombie
            step = 4.5
            if (Tx - Zx) > 0:
                dx += step
            elif (Tx - Zx) < 0:
                dx -= step

            if (Tz - Zz) > 0:
                dz += step
            elif (Tz - Zz) < 0:
                dz -= step

            # prevent jittering
            #tolerance = 5
            #if -tolerance <= dx <= tolerance:
            #    dx = 0
            #if -tolerance <= dy <= tolerance:
            #    dy = 0
            #if -tolerance <= dz <= tolerance:
            #    dz = 0

            # update all movements to entity data
            print("dx: " + str(dx) + " dz: " + str(dz) + " dy: " + str(dy))
            for index in entity:
                if index[5] == id:
                    entity[int(index[5])][0] = int(entity[int(index[5])][0]) + dx
                    entity[int(index[5])][1] = int(entity[int(index[5])][1]) + dy
                    entity[int(index[5])][2] = int(entity[int(index[5])][2]) + dz
                    entity[int(index[5])][3] = float(rot)


            
def gameManager(setup=False):
    global time4, time5, wave, entity
    # if being called for the first time
    if setup == True:
        # start timer
        time4 = millis()
        wave = 1

    # spawnable locations
    locations = [[3,13,29],[4,13,29],[5,13,29],[23,13,17],[23,13,18],[23,13,19]]#,[24,11,10],[24,11,11],[24,11,12]]
    if millis() - time4 < 10000:
        playerUi(timer=(10 - ((millis() - time4)/1000))) # display the player a countdown timer
    else:
        # start the game loop
        if entity == [] and time5 == 0:
            time5 = millis()
        
        # display wave number for 2 seconds
        if millis() - time5 < 2000:
            playerUi(wave=wave) # display the player the wave number
        # then spawn zombies
        elif (millis() - time5 > 2000) and entity == []:
            # spawn zombies
            wave += 1
            for i in range(1):
                print(locations[int(random(0,len(locations)))][1])
                randomId = int(random(0,len(locations)))
                Tx,Ty,Tz = gridConvert(locations[randomId][0],locations[randomId][1],locations[randomId][2])
                entity.append([Tx,Ty,Tz,str(float(random((-2*PI),(2*PI)))),str(0),str(i),[],int(0),int(0)]) # [x,y,z,rotation,type,id,path,timer1,timer2]


def draw():

    benchmarkStart = millis()

    # lights()
    background(58, 57, 63)
    
    global scaling_factor, buffer, bx, by, bz, angle, rotation, x, y, z, hitboxes, time
    # Define camera mathww
    xCenter = ((float(mouseX) - (float(width)/2)) / float(width) ) * (4*PI)
    yCenter = ((float(mouseY) - (float(height)/2)) / float(height) ) * (2*PI)
    ## print("Angle:" + str(360*(xCenter)/2*PI))
    rotation = xCenter
    #####################

    print(raycast(x,y,z,xCenter,yCenter))

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
    loadMap(2, 0, 0, 0)
    #print(genNavMesh(hitboxes))
    #print(navMesh)
    #exit()

    # run game manager function
    gameManager()

    # load zombies
    playerCord = x,y,z
    zombieMove(playerCord)
    spawnZombies(entity)

    # start = 18,14,24
    # end = 4,14,26 
    # benchmarkStartAstar = millis()
    # print(Astar(hitboxes[14],start,end))
    # print("This frame took " + str(millis() - benchmarkStartAstar) + " miliseconds to complete")
    #exit()

    # run ui commands
    f3(x,y,z,rotation)
    playerUi()


    print("This frame took " + str(millis() - benchmarkStart) + " miliseconds to complete")