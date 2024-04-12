##############################################################################
# spaceInvaders.py - Space Invaders Game in Processing 3                     #
#                                                                            # 
##############################################################################

# if running on linux, uncomment the following two lines
from java.lang import System
System.setProperty("jogl.disable.openglcore", "false")

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
    #noStroke()
    offset = 20
    rO,gO,bO = offset,offset,offset
    if r-offset <= 0:
        rO = 0 
    if g-offset <= 0:
        gO = 0
    if b-offset <= 0:
        bO = 0

    stroke(r-rO,g-gO,b-bO)

    strokeWeight(2) # DONT GO OVER 2 (causes clipping)
    translate(x,y,z)
    box(100)
    popMatrix()

def loadHitboxes(key):

    # Create a 3D array with dimensions 50x50x50, or as x,z,y
    hitboxes = [[[0 for _ in range(50)] for _ in range(50)] for _ in range(50)]

    # Define the maps in a array
    maps = ["de_dust2", "crater"]

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
    maps = ["de_dust2", "crater"]

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

    global ui, playerModel, dmgOverlay, mainMenu, gameOver
    ui = createGraphics(width,height, P2D)
    playerModel = createGraphics(width,height, P2D)
    dmgOverlay = createGraphics(width,height, P2D)
    mainMenu = createGraphics(width,height, P2D)
    gameOver = createGraphics(width,height, P2D)

    global x,y,z
    x,y,z = 300,200,400

    global dx,dy,dz
    dx,dy,dz = 0,0,0

    global sceneIndex
    sceneIndex = 0 # [0 = main menu, 1 = game, 2 = game over]

    global time2, time3, time, time4, time5, time6, time7
    time = 0
    time2 = 1000
    time3 = 0
    time4 = 0
    time5 = 0
    time6 = 0
    time7 = 0

    global hitboxes
    hitboxes = []
    #print(hitboxes[2][4][0])
    # exit()

    global navMesh
    navMesh = []

    global buffer, bx, by, bz, angle
    buffer = [0]
    bx = [0]
    by = [0,0]
    bz = [0]
    angle = [0]

    global f3State
    f3State = False

    global image1, image2, image3
    image1 = loadImage("playerModel/AR/idle.png")
    image2 = loadImage("crosshair-1.png")
    image3 = loadImage("playerModel/damageOverlay.png")

    global mainMenuBG, keybinds, title
    mainMenuBG = loadImage("mainMenuBackground.png")
    keybinds = loadImage("keybinds.png")
    title = loadImage("title.png")

    global cursorIMG
    cursorIMG = loadImage("cursor.png")

    global gameOverText
    gameOverText = loadImage("gameOver.png")

    global mapSequence, mapIndex
    mapSequence = []

    mapSequence.append(loadImage("maps/thumbnails/de_dust2.png"))
    mapSequence.append(loadImage("maps/thumbnails/crater.png"))

    mapIndex = 0

    global arSequence, arIndex

    arSequence = []

    arSequence.append(loadImage("playerModel/AR/shoot/frame-0099.png"))
    arSequence.append(loadImage("playerModel/AR/shoot/frame-0100.png"))
    arSequence.append(loadImage("playerModel/AR/shoot/frame-0101.png"))
    arSequence.append(loadImage("playerModel/AR/shoot/frame-0102.png"))
    arSequence.append(loadImage("playerModel/AR/shoot/frame-0103.png"))
    arSequence.append(loadImage("playerModel/AR/shoot/frame-0104.png"))
    arSequence.append(loadImage("playerModel/AR/shoot/frame-0105.png"))

    arIndex = 0

    global arRSequence, arRIndex

    arRSequence = []

    arRSequence.append(loadImage("playerModel/AR/reload/frame-0110.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0111.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0112.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0113.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0114.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0115.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0116.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0117.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0118.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0119.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0120.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0121.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0122.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0123.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0124.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0125.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0126.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0127.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0128.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0129.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0130.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0131.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0132.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0133.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0134.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0135.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0136.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0137.png"))
    arRSequence.append(loadImage("playerModel/AR/reload/frame-0138.png"))

    arRIndex = 0

    global numberSequence, bannerBase
    bannerBase = loadImage("banner/base.png")
    numberSequence = []

    numberSequence.append(loadImage("banner/0.png"))
    numberSequence.append(loadImage("banner/1.png"))
    numberSequence.append(loadImage("banner/2.png"))
    numberSequence.append(loadImage("banner/3.png"))
    numberSequence.append(loadImage("banner/4.png"))
    numberSequence.append(loadImage("banner/5.png"))
    numberSequence.append(loadImage("banner/6.png"))
    numberSequence.append(loadImage("banner/7.png"))
    numberSequence.append(loadImage("banner/8.png"))
    numberSequence.append(loadImage("banner/9.png"))


    global cAmmo, tAmmo, health
    cAmmo = 30
    tAmmo = 60
    health = 100

    global moveUp, moveDown, moveLeft, moveRight, jumping, shooting, reloading
    moveUp, moveDown, moveLeft, moveRight, jumping, shooting, reloading = False, False, False, False, False, False, False

    global entity
    entity = []

    global emitters
    emitters = []

    global ammoBoxes
    ammoBoxes = []

    global textOverlays
    textOverlays = []

    global wave, totalZombies, maxZombies
    wave = 1
    totalZombies = 0
    maxZombies = 10

    global zombie, ammoBox
    zombie = loadShape("low_poly_zombie.obj")
    ammoBox = loadShape("ammoPickup.obj")

    global path_cache
    path_cache = {}

    size(1000, 700, P3D)
    noClip()
    fullScreen()
    #noCursor()
    frameRate(60)


# keybinds
def keyPressed():
    global moveUp, moveDown, moveLeft, moveRight, jumping, reloading
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
    if key == "r":
        reloading = True

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

def mousePressed():

    global shooting, cAmmo

    if cAmmo > 0:
        shooting = True

def mouseReleased():
    global shooting
    shooting = False

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

def Astar(start, end):

    # written with reference to https://youtu.be/-L-WgKMFuhE?si=UlBWzKz5x3yjQHLc&t=455
    # ySlice is the slice of the 3D array
    # start [x,y,z]
    # end [x,y,z]

    openList = [] # [x,y,z,f,g,h,parent]
    closedList = set() # using a set for faster lookups
    blank = 0,0,0
    path = []

    global navMesh

    print(navMesh)
    temp = navMesh[0][20]
    #print(temp[0])
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
        
        # check if finding the path is taking too long
        if len(openList) >= 50:
            print("path not found")
            return []

        # sort list by lowest f value 
        openList.sort(key=lambda x: x[3])

        # set current node from the open list
        current = openList[0]
        # remove the current node from the open list
        openList.remove(current)
        # add the current node to the closed list
        closedList.update({(current[0],current[1],current[2],str((current[6])))})

        # check if the current node is the end node       
        if (current[0], current[1], current[2]) == end:
            print("path found")
            # initialise current node from open list is in the format [x,y,z,f,g,h,parent]
            if len(current) >= 6:
                # if that current node is in [x,y,z,f,g,h,parent] format, then find the parent node in closedList
                x,y,z,_,_,_,parent = current
                path.append([x,y,z])
                for item in closedList:
                    if item[0] == parent[0] and item[1] == parent[1] and item[2] == parent[2]:
                        current = item
                        print(current)
            
            # closedList is in the format [x,y,z,parent], so find the parent node in closedList
            while closedList:
                x,y,z,parent = current
                parent = eval(parent)
                path.append([x,y,z])
                if x == start[0] and z == start[2]:
                    # convert the path coordinates to navMesh coordinates
                    tempA = []
                    for item in path:
                        temp = navMesh[item[0]][item[2]]
                        tempA.append([temp[1],temp[2],temp[3]])
                    
                    path = tempA
                    return path

                for item in closedList:
                    px,py,pz = parent
                    if item[0] == px and item[2] == pz:
                        current = item
                        print(current)
               
            return []  # reverse the path because it was built from end to start
        
        
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
                    temp = navMesh[int(current[0])+i][int(current[2]+j)]
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
                    #tolerance = 0
                    #for block in closedList:
                    #    if block[0] == int(current[0])+i and block[2] == int(current[2]+j):
                    #        tolerance += 1
                    #        continue
                    #if tolerance >= 1:
                    #    continue

                    if (int(current[0])+i, int(current[1]), int(current[2]+j)) in [tuple(item[:3]) for item in closedList]:
                        # print the node that is in the closed list
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
        
def cache_path(start, end, path):
    global path_cache

    cache_key = (start, end)
    path_cache[cache_key] = path

def retrieve_path(start, end):
    global path_cache

    cache_key = (start, end)
    return path_cache.get(cache_key)

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
            # translate(ex-60,ey-90,ez-60)
            # box(20)
            # popMatrix()
            # pushMatrix()
            # fill(0,255,0)
            # translate(ex+50,ey+120,ez+50)
            # box(20)
            # popMatrix()

            #pushMatrix()
            #fill(0,0,255)
            #translate(rx,ry,rz)
            #box(20)
            #popMatrix()

            if AABB([(rx-5),(ry-5),(rz-5), (rx+5),(ry+5),(rz+5)], [(ex-60),(ey-120),(ez-60), (ex+60),(ey+120),(ez+60)]) == True:
                e += 1
                return id


        raycastDistance += 50
        #try:
        #    setting = 0
        #    if hitboxes[int(floor(ry/100))][int(floor(rx/100))][int(floor(rz/100))] == 1 or e != 0:
        #        if e != 0:
        #            print("entity collision")
        #            setting = 1
        #        if hitboxes[int(floor(ry/100))][int(floor(rx/100))][int(floor(rz/100))] == 1:
        #            print("block collision")
        #        if setting == 0:
        #            return [rx,ry,rz]
        #        elif setting == 1:
        #            return id
#
        #    else:
        #        raycastDistance += 100
        #except IndexError: 
        #        raycastDistance = 3000
        #        pass

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

def ammoBoxSpawn(location, rotation):
    
    x,y,z = location

    global ammoBox

    pushMatrix()
    translate(x,y+120,z)
    rotateY(rotation)
    rotateX(PI)
    scale(50)
    shape(ammoBox)
    popMatrix()

def runAmmoBoxes():

    global ammoBoxes

    for item in ammoBoxes:
        x,y,z,rotation = item
        rotation += (PI/34)
        item[3] = rotation
        ammoBoxSpawn([x,y,z], rotation)


def explode(emitter, lifetime):

    ox,oy,oz = emitter

    # spawn particles
    # https://www.desmos.com/3d/8db868c05d
    for i in range(0,10): # x,z sectors of particles
        for j in range(-1,2): # y sectors of particles

            # calculate the position of the particle
            a = i * ((2*PI)/10)
            b = j * 0.7
            lifetime = millis() - lifetime

            x = (sin(i)+ox) - lifetime*((sin(i)+ox)-ox) 
            y = (b+oy) - lifetime*((b+oy)-oy)
            z = (cos(i)+oz) - lifetime*((cos(i)+oz)-oz)

            # render the particle
            pushMatrix()
            fill(255,0,0)
            translate(x,y,z)
            noStroke()
            box(10)
            popMatrix()

def runEmitters():
    global emitters

    for item in emitters:
        ox,oy,oz = item[0]
        lifetime = item[1]

        if millis() - lifetime > 200:
            emitters.remove(item)
        else:
            explode([ox,oy,oz], lifetime)

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
        ui.textAlign(LEFT)
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

def waveBanner(waveN, lifetime):

    

    global ui
    #print(str(textm) + " " + str(coord) + " " + str(colour) + " " + str(lifetime))
    if (millis() - lifetime) <= 2000:
        #ui.beginDraw()
        #ui.fill(r,g,b)
        #ui.textAlign(CENTER)
        #ui.textSize(30)
        #ui.text(textm, x-50, z)
        #ui.endDraw()

        xO = +15
        yO = -120
        global numberSequence, bannerBase
        if len(str(waveN)) == 1:
            ui.beginDraw()
            ui.clear()
            ui.image(bannerBase, floor(width/3)+xO, floor((width/8))+yO, (width/3), (height/8))
            ui.image(numberSequence[int(0)], floor(width/3)+xO, floor((width/8))+yO, (width/3), (height/8))
            ui.image(numberSequence[int(waveN)], floor(width/3)+60+xO, floor((width/8))+yO, (width/3), (height/8))
            ui.endDraw()



    elif (millis() - lifetime) > 2000:
        global textOverlays
        try:
            textOverlays.remove([waveN, lifetime])
        except ValueError:
            pass
    
    pushMatrix()
    camera()
    hint(DISABLE_DEPTH_TEST)
    noLights()
    image(ui,0,0)
    hint(ENABLE_DEPTH_TEST)
    popMatrix()

def runTextOverlay():
    global textOverlays

    for item in textOverlays:
        waveBanner(item[0], item[1])


def damageOverlay(reset=False):
    global dmgOverlay, image3, time7

    if reset == True:
        time7 = millis()
    else:
        if millis() - time7 < 3000:
            dmgOverlay.beginDraw()
            dmgOverlay.clear()
            dmgOverlay.image(image3, 0, 0, width, height)
            dmgOverlay.endDraw()
        else:
            dmgOverlay.beginDraw()
            dmgOverlay.clear()
            dmgOverlay.endDraw()

    pushMatrix()
    camera()
    hint(DISABLE_DEPTH_TEST)
    noLights()
    image(dmgOverlay,0,0)
    hint(ENABLE_DEPTH_TEST)
    popMatrix()

def playerUi(timer=0,wave=0):
    # player model
    global playerModel, image1, image2

    global shooting, reloading, health
    
    global arSequence, arIndex, cAmmo, tAmmo
    if shooting == False and reloading == False:
        playerModel.beginDraw()
        playerModel.clear()
        playerModel.image(image1, 0, 0, width, height)
        playerModel.image(image2, (width/2)-50, (height/2)-50, 30, 30)
        playerModel.endDraw()
    if (shooting == True or arIndex != 0) and reloading == False and cAmmo > 0:
        playerModel.beginDraw()
        playerModel.clear()
        
        # animate the player shooting
        playerModel.image(arSequence[arIndex], 0, 0, width, height)
        arIndex += 1
        if arIndex == 7:
            cAmmo -= 1
            arIndex = 0

        playerModel.image(image2, (width/2)-50, (height/2)-50, 30, 30)
        playerModel.endDraw()

    global arRSequence, arRIndex
    if (reloading == True or arRIndex != 0) and shooting == False:
        playerModel.beginDraw()
        playerModel.clear()
        
        # animate the player reloading
        playerModel.image(arRSequence[arRIndex], 0, 0, width, height)
        arRIndex += 1
        if arRIndex == 28:
            arRIndex = 0

            if tAmmo >= 30:
                if cAmmo == 0:
                    cAmmo = 30
                    tAmmo -= 30 
                elif cAmmo != 30:
                    tAmmo -= 30 - cAmmo
                    cAmmo = 30
            elif tAmmo < 30:
                if cAmmo == 0:
                    cAmmo = tAmmo
                    tAmmo = 0
                elif cAmmo + tAmmo > 30:
                    tAmmo -= 30 - cAmmo
                    cAmmo = 30
                elif cAmmo + tAmmo <= 30:
                    cAmmo += tAmmo
                    tAmmo = 0

            reloading = False

        playerModel.image(image2, (width/2)-50, (height/2)-50, 30, 30)
        playerModel.endDraw()


    if timer != 0:
        playerModel.beginDraw()
        playerModel.fill(0,0,0)
        playerModel.textSize(30)
        playerModel.textAlign(CENTER)
        playerModel.text(timer, (width/2), 50)
        playerModel.endDraw()

    # Display the ammo
    playerModel.beginDraw()
    playerModel.fill(0,0,0)
    playerModel.textSize(30)
    playerModel.textAlign(BOTTOM)
    playerModel.text("ammo: " + str(cAmmo) + "/" + str(tAmmo), 30, 150)
    playerModel.endDraw()

    # Display the health
    playerModel.beginDraw()
    playerModel.fill(0,0,0)
    playerModel.rectMode(CORNER)
    playerModel.rect(19,19,202,32)
    playerModel.fill(255,0,0)
    playerModel.rectMode(CORNER)
    playerModel.rect(20,20,(health*2),30)
    playerModel.noStroke()
    playerModel.endDraw()

    # display the wave duration
    global totalZombies, maxZombies, entity
    playerModel.beginDraw()
    playerModel.fill(0,0,0)
    playerModel.rectMode(CENTER)
    playerModel.rect(((width/6)*3)-2,38,304,64)
    playerModel.fill(0,255,0)
    
    count = 0
    for item in entity:
        count += 1

    #print("total zombies: " + str(totalZombies+float(count)) + " max zombies: " + str(maxZombies) + " ratio: " + str(float(totalZombies)/float(maxZombies)))
    playerModel.rectMode(CENTER)
    playerModel.rect(((width/6)*3)-1,38,((float(totalZombies+float(count))/float(maxZombies))*float(300-1)),58)
    playerModel.noStroke()
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
            height = 15
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

            # check if zombie is within a certain distance of the player
            global time6, health
            if sqrt((Zx-player[0])**2 + (Zz-player[2])**2) < 250:
                print("zombie is close to player")
                offset = PI/2
                rot = atan2(Zx - player[0],Zz - player[2]) + offset

                if time6 == 0:
                    time6 = millis()
                else:
                    if millis() - time6 >= 400:
                        time6 = millis()
                        print("player hit")
                        health -= 10
                        damageOverlay(reset=True)

                for index in entity:
                    if index[5] == id:
                        index[3] = float(rot)

                continue
            else:
                time6 = 0


            player = (int(floor((player[0])/100)),int(int(floor(Zy/100))+1),int(floor((player[2])/100)))
            zombie = (int(floor((Zx/100))),int(int(floor(Zy/100))+1),int(floor((Zz/100))))
            print("player: " + str(player))
            print("zombie: " + str(zombie))
            #print("hitboxes: " + str(hitboxes[int(floor(Zy/100))+1]))

            # find the middle point of the zombie and player, reduce the path length if the path is too long to prevent lag
            Zx,Zy,Zz = zombie
            Px,Py,Pz = player

            maxPathLength = 5

            #try: # prevent division by zero
            #    hDistance = sqrt((Zx-Px)**2 + (Zz-Pz)**2) # heuristic distance
            #    slope = float(Zy-Py)/float(Zx-Px)
            #    b = Zy - (slope*Zx)
            #    if hDistance > maxPathLength:
            #        halfwayX = hDistance/2
            #        halfwayY = slope*halfwayX + b
#
            #        # check if the halfway point is collidable
            #        while hitboxes[int(floor(Zy))][int(floor(halfwayX))][int(floor(halfwayY))] == 1:
            #            halfwayX = halfwayX/2
            #            halfwayY = slope*halfwayX + b
#
            #        zombie = (int(floor(halfwayX)),int(floor(Zy)),int(floor(halfwayY)))
            #except ZeroDivisionError:
            #    pass





            # check if the path is cached
            cached_path = retrieve_path(zombie, player)
            if cached_path is None:
                if player[0] != 0 and player[2] != 0: # for some reason the player will falsely get reported as being at 0,0, causing the pathfinding to fail, by checking if the player is at 0,0, we can prevent the pathfinding from running and prevent lag
                    path = Astar(zombie, player)

                    # cache the path
                    cache_path(zombie, player, path)
            else:
                path = cached_path

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
            global time6, health
            if sqrt((Zx-player[0])**2 + (Zz-player[2])**2) < 250:
                # zombie is close to the player so look at the player
                rot = atan2(Zx - player[0],Zz - player[2]) + offset
 
                if time6 == 0:
                    time6 = millis()
                else:
                    if millis() - time6 >= 400:
                        time6 = millis()
                        print("player hit")
                        health -= 10
                        damageOverlay(reset=True)
            else:
                # zombie is too far from the player so look where its walking
                rot = atan2(Zx - Tx,Zz - Tz) + offset
                time6 = 0
            
            print("Zombie rotation: " + str(rot))

            # make the zombie jump
            if ((Ty - Zy) < -20) or (millis() - timer1) < 500:
                print("step one")
                if (((Ty - Zy) < -20) and (millis() - timer1) > 500):
                    print("step two")
                    # print(hitboxCalc(floor(Zx)/100,floor(Zy+2)/ 100,floor(Zz)/100,1,1))
                    # if hitboxCalc(floor(Zx)/100,floor(Zy)/100,floor(Zz)/100,1,1) != 0:
                    print("timer reset")
                    timer1 = millis()
                    #item[7] = timer1

                if (millis() - timer1) < 500:
                    # https://www.desmos.com/calculator/jlcyciwaaq
                    dt = -5 + (millis() - timer1)/58
                    height = 15
                    width = 1
                    steepness = 1
                    dy -= float(height / (1 + exp((steepness*(dt-10))/width)) - float(height / (1 + exp((steepness*dt)/width))))

            print("Zx: " + str(Zx) + " Zy: " + str(Zy) + " Zz: " + str(Zz) + " id: " + str(id) + " path: " + str(path))

            # run gravity calculations
            print(Zx)
            if hitboxes[floor(Zy)/100][floor(Zx)/100][floor(Zz)/100] == 1: # y, x, z
                print("set time")
                timer2 = millis()
                #item[8] = timer2

        
            #renderBlock(Zx,Zy-250,Zz,255,0,0)
            if ((Ty - Zy) > 20) and hitboxes[floor(Zy)/100][floor(Zx)/100][floor(Zz)/100] == 0: 
                dt = ((millis() - timer2)/500)+2
                gravity = 9.8
                print(str(gravity * dt))
                dy += gravity * dt
            
            #item[1] = Zy

            # move the zombie
            step = 4.5
            tolerance = 5 # prevent jittering
            if -tolerance <= (Tx - Zx) <= tolerance:
                dx = 0
            else:
                if (Tx - Zx) > 0:
                    dx += step
                elif (Tx - Zx) < 0:
                    dx -= step

            if -tolerance <= (Tz - Zz) <= tolerance:
                dz = 0
            else:
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

            for item in entity:
                if item[5] == id:
                    continue

                feather = 20
                
                #print("zombie")
                #print(str(Zx+dx) + " " + str(Zy-200) + " " + str(Zz+dz))
                #pushMatrix()
                #fill(255,0,0)
                #translate(Zx+dx,Zy-200,Zz+dz)
                #noStroke()
                #box(50)
                #popMatrix()

                #print("other Zombie")
                #print(str(item[0]) + " " + str(item[1]) + " " + str(item[2]))
                #pushMatrix()
                #fill(0,255,0)
                #translate(item[0],item[1],item[2])
                #noStroke()
                #box(50)
                #popMatrix()

                if AABB([((Zx+dx)-feather),((Zy-200)-10),((Zz+dz)-feather), ((Zx+dx)+feather), ((Zy-200)+100), ((Zz+dz)+feather)], [(item[0]-feather), (item[1]), (item[2]-feather),  (item[0]+feather), (item[1]+100), (item[2]+feather)]) == True:

                    # push the zombie away from the other zombie
                    direction = -dotProduct(Zx,Zz,item[0]-Zx,item[2]-Zz)
                    force = 50
                    dx += force*cos(direction)
                    dz += force*sin(direction)
                    print("collision")

            # update all movements to entity data
            print("dx: " + str(dx) + " dz: " + str(dz) + " dy: " + str(dy))
            for index in entity:
                if index[5] == id:
                    index[0] = int(index[0]) + dx
                    index[1] = int(index[1]) + dy
                    index[2] = int(index[2]) + dz
                    index[3] = float(rot)
                    index[7] = timer1
                    index[8] = timer2
                      
def gameManager(setup=False):
    global time4, time5, wave, entity
    global totalZombies, maxZombies
    # if being called for the first time
    if setup == True:
        # start timer
        time4 = millis()
        wave = 0

    # spawnable locations
    global mapIndex
    if mapIndex == 0:
        locations = [[3,13,29],[4,13,29],[5,13,29],[23,13,17],[23,13,18],[23,13,19],[23,11,10],[23,11,11],[23,11,12]]
    elif mapIndex == 1:
        locations = [[33,-4,16],[16,-4,16],[33,-4,33],[16,-4,33]]
    if millis() - time4 < 10000:
        playerUi(timer=(10 - ((millis() - time4)/1000))) # display the player a countdown timer
    else:
        # start the game loop
        if entity == [] and time5 == 0:
            time5 = millis()
        
        # display wave number for 2 seconds
        if millis() - time5 < 2000:
            #playerUi(wave=wave) # display the player the wave number
            global textOverlays
            if textOverlays != []:
                for item in textOverlays:
                    if item[0] == ("wave " + str(wave)):
                        pass
            else:
                if wave != 0:
                    textOverlays.append([int(wave), millis()])
                    print(textOverlays)
                #exit()
        # then spawn zombies
        elif ((millis() - time5 > 2000) and entity == []) or totalZombies != 0:
            # spawn zombies
            if totalZombies == 0:
                scaleFactor = 1.2
                maxZombies = ceil(random(10+(wave*scaleFactor),30+(wave*scaleFactor)))
                totalZombies = maxZombies
                wave += 1
                time5 = millis()
    
            spawnLimit = 4

            if len(entity) <= spawnLimit and totalZombies != 0:
                totalZombies -= 1
                print(locations[int(random(0,len(locations)))][1])
                randomId = int(random(0,len(locations)))
                Tx,Ty,Tz = gridConvert(locations[randomId][0],locations[randomId][1],locations[randomId][2])
                entity.append([Tx,Ty,Tz,str(float(random((-2*PI),(2*PI)))),str(0),str(maxZombies-totalZombies),[],int(0),int(0)]) # [x,y,z,rotation,type,id,path,timer1,timer2]

def drawMainMenu():

    global mainMenu, mainMenuBG, title, keybinds

    mainMenu.beginDraw()
    mainMenu.clear()
    mainMenu.imageMode(CORNER)
    mainMenu.image(mainMenuBG, 0, 0, width, height)
    mainMenu.image(keybinds, 10, height-(height/6)-10, (width/6)*2, (height/6))
    mainMenu.image(title, (width/2)-(width/4), 10, (width/2), (height/5))

    mainMenu.endDraw()

    pushMatrix()
    camera()
    hint(DISABLE_DEPTH_TEST)
    noLights()
    image(mainMenu,0,0)
    hint(ENABLE_DEPTH_TEST)
    popMatrix()

def sceneSwitcher():

    global mainMenu

    mainMenu.beginDraw()

    # select button
    mainMenu.rectMode(CENTER)
    mainMenu.fill(255,0,0)
    mainMenu.stroke(0)
    mainMenu.strokeWeight(2)
    mainMenu.rect((width/5)*2.5, (height/2)+(height/4), 200, 50)
    mainMenu.fill(0)
    mainMenu.textSize(30)
    mainMenu.textAlign(CENTER)
    mainMenu.text("Start", (width/5)*2.5, (height/2)+(height/4)+10)

    # left button
    mainMenu.rectMode(CENTER)
    mainMenu.fill(255,0,0)
    mainMenu.stroke(0)
    mainMenu.strokeWeight(2)
    mainMenu.rect((width/5)*1.5, height/2, 50, 200)
    mainMenu.fill(0)
    mainMenu.textSize(30)
    mainMenu.textAlign(CENTER)
    mainMenu.text("<", (width/5)*1.5, height/2+10)

    # right button
    mainMenu.rectMode(CENTER)
    mainMenu.fill(255,0,0)
    mainMenu.stroke(0)
    mainMenu.strokeWeight(2)
    mainMenu.rect((width/5)*3.5, height/2, 50, 200)
    mainMenu.fill(0)
    mainMenu.textSize(30)
    mainMenu.textAlign(CENTER)
    mainMenu.text(">", (width/5)*3.5, height/2+10)

    # map image
    global mapSequence, mapIndex
    mainMenu.imageMode(CENTER)
    mainMenu.image(mapSequence[mapIndex], (width/5)*2.5, (height/2), 280, 180)

    # mouse cursor
    global cursorIMG
    mainMenu.image(cursorIMG, mouseX, mouseY, 50, 50)

    mainMenu.endDraw()

    pushMatrix()
    camera()
    hint(DISABLE_DEPTH_TEST)
    noLights()
    image(mainMenu,0,0)
    hint(ENABLE_DEPTH_TEST)
    popMatrix()

def drawGameOver():
    
        global gameOver, gameOverText, wave

        # general ui elements
        gameOver.beginDraw()
        gameOver.clear()
        gameOver.imageMode(CORNER)
        gameOver.background(0,0,0,200)
        gameOver.image(gameOverText, (width/2)-(width/4), (height/2)-(height/3), (width/2), (height/2))

        # display wave number
        gameOver.textSize(30)
        gameOver.textAlign(CENTER)
        gameOver.fill(255,0,0)
        gameOver.text("wave: " + str(wave), (width/2), (height/2)+50)

        # retry button
        gameOver.rectMode(CENTER)
        gameOver.fill(255,0,0)
        gameOver.stroke(0)
        gameOver.strokeWeight(2)
        gameOver.rect((width/5)*2.5, (height/2)+(height/4), 200, 50)
        gameOver.fill(0)
        gameOver.textSize(30)
        gameOver.textAlign(CENTER)
        gameOver.text("Retry", (width/5)*2.5, (height/2)+(height/4)+10)

        # main menu button
        gameOver.rectMode(CENTER)
        gameOver.fill(255,0,0)
        gameOver.stroke(0)
        gameOver.strokeWeight(2)
        gameOver.rect((width/5)*2.5, (height/2)+(height/4)+75, 200, 50)
        gameOver.fill(0)
        gameOver.textSize(30)
        gameOver.textAlign(CENTER)
        gameOver.text("Main Menu", (width/5)*2.5, (height/2)+(height/4)+85)

        # mouse cursor
        global cursorIMG
        gameOver.image(cursorIMG, mouseX, mouseY, 50, 50)

        gameOver.endDraw()
    
        pushMatrix()
        camera()
        hint(DISABLE_DEPTH_TEST)
        noLights()
        image(gameOver,0,0)
        hint(ENABLE_DEPTH_TEST)
        popMatrix()
    
def draw():

    global sceneIndex

    if sceneIndex == 0:
        # run main menu
        print("main menu")

        cursor()
        drawMainMenu()

        sceneSwitcher()

        global mapIndex 
        if mousePressed:
            # select button
            if (width/5)*2.5-100 <= mouseX <= (width/5)*2.5+100 and (height/2)+(height/4)-25 <= mouseY <= (height/2)+(height/4)+25:
                global time 
                time = millis()

                # wait to load map before switching scenes
                i = 0
                while i != 1:
                    global hitboxes
                    hitboxes = loadHitboxes(mapIndex) # hitboxes only need to be loaded once
                    #print(hitboxes[2][4][0])
                    # exit()

                    global navMesh
                    navMesh = genNavMesh(hitboxes) # navmesh only needs to be generated once

                    if hitboxes != None and navMesh != None:
                        i = 1
                        print("loaded")

                if mapIndex == 1:
                    global x,y,z
                    x,y,z = 2500,200,2500
                
                sceneIndex = 1

            
            # left button
            if (width/5)*1.5-25 <= mouseX <= (width/5)*1.5+25 and (height/2)-100 <= mouseY <= (height/2)+100:
                if mapIndex != 0:
                    mapIndex -= 1
            
            # right button
            if (width/5)*3.5-25 <= mouseX <= (width/5)*3.5+25 and (height/2)-100 <= mouseY <= (height/2)+100:
                if mapIndex != 1:
                    mapIndex += 1




    elif sceneIndex == 1:
        # run game loop
        benchmarkStart = millis()

        # lights()
        background(58, 57, 63)
        noCursor()
        
        global scaling_factor, buffer, bx, by, bz, angle, rotation, x, y, z, hitboxes, time
        # Define camera mathww
        xCenter = ((float(mouseX) - (float(width)/2)) / float(width) ) * (4*PI)
        yCenter = ((float(mouseY) - (float(height)/2)) / float(height) ) * (2*PI)
        ## print("Angle:" + str(360*(xCenter)/2*PI))
        rotation = xCenter
        #####################

        # shooting
        global shooting, reloading
        if shooting == True and reloading == False:
            print("shooting")
            raycastOut = raycast(x,y,z,xCenter,yCenter)
            print(raycastOut)
            try:
                if raycastOut == None:
                    pass
                if len(raycastOut) == 3:
                    pass
            except TypeError:
                if raycastOut != None:
                    for item in entity:
                        if int(item[5]) == int(raycastOut):
                            print("hit")

                            global emitters, ammoBoxes
                            pos = item[0],item[1],item[2]
                            print(entity)
                            emitters.append([pos,millis()])

                            # drop ammo box
                            global wave
                            scaleFactor = 1.2
                            maxZ = floor(10 + (wave*scaleFactor))
                            if random(0,maxZ) >= maxZ-1:
                                ammoBoxes.append([item[0],item[1],item[2],int(0)])

                            entity.remove(item)
                            print(entity)
                            break



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
                    #renderBlock(hx,hy,hz,255,0,0)

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
                    
                    #renderBlock(hx,hy,hz,255,0,0)

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
                    
                    #renderBlock(hx,hy,hz,255,0,0)

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
                    
                    #renderBlock(hx,hy,hz,255,0,0)

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
                    
                    #renderBlock(hx,hy,hz,255,0,0)

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
        global mapIndex
        loadMap(int(mapIndex), 0, 0, 0)
        #print(genNavMesh(hitboxes))
        #print(navMesh)
        #exit()

        # run game manager function
        gameManager()

        # load zombies
        playerCord = x,y,z
        zombieMove(playerCord)
        spawnZombies(entity)

        runEmitters()
        runAmmoBoxes()

        # detect if player intersected with an ammo box
        global ammoBoxes, tAmmo
        for item in ammoBoxes:
            feather = 30
            if AABB([(x-20),(y),(z-20), (x+20),(y+200),(z+20)], [(item[0]-feather),(item[1]-feather),(item[2]-feather), (item[0]+feather),(item[1]+feather),(item[2]+feather)]) == True:
                ammoBoxes.remove(item)
                tAmmo += 10


        # start = 18,14,24
        # end = 4,14,26 
        # benchmarkStartAstar = millis()
        # print(Astar(hitboxes[14],start,end))
        # print("This frame took " + str(millis() - benchmarkStartAstar) + " miliseconds to complete")
        #exit()

        # run ui commands
        f3(x,y,z,rotation)
        playerUi()
        damageOverlay()
        runTextOverlay()


        print("This frame took " + str(millis() - benchmarkStart) + " miliseconds to complete")

    elif sceneIndex == 2:
        # run game over screen
        print("game over")

        cursor()
        drawGameOver()

        if mousePressed:
            # retry button
            if (width/5)*2.5-100 <= mouseX <= (width/5)*2.5+100 and (height/2)+(height/4)-25 <= mouseY <= (height/2)+(height/4)+25:
                sceneIndex = 1
                global time 
                time = millis()
            
            # main menu button
            if (width/5)*2.5-100 <= mouseX <= (width/5)*2.5+100 and (height/2)+(height/4)+50 <= mouseY <= (height/2)+(height/4)+100:
                sceneIndex = 0

