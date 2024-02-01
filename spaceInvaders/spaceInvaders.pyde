##############################################################################
# spaceInvaders.py - Space Invaders Game in Processing 3                     #
#                                                                            # 
##############################################################################

# if running on linux, uncomment the following line
# from java.lang import System
# System.setProperty("jogl.disable.openglcore", "false")

def gridConvert(x, y, z):
    global scaling_factor
    scaling_factor = 50.1  # Adjust the scaling factor as needed
    return [x * scaling_factor, y * scaling_factor, z * scaling_factor]

def renderBlock(x,y,z,r,g,b):
    
    global hitboxes

    #print("Rendering block at: " + str(x) + ", " + str(y) + ", " + str(z))
    # block settings
    pushMatrix()
    fill(r,g,b)
    noStroke()
    translate(x,y,z)
    box(50)
    popMatrix()

    # define the hitbox
    hitboxes.append([x,y,z,(x+50),(y+50),(z+50)])


def loadMap(key, xOffset, yOffset, zOffset):
    
    # background(0)

    # Define the maps in a array
    maps = ["test", "test2"]

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

    global hitboxes
    hitboxes = []


def player():
    # player settings
    global x,y,z, hitboxes

    step = 1
    # keyboard controls
    if keyPressed:
        if key == "w":
            z += (step)
        elif key == "s":
            z -= (step)
        elif key == "a":
            x -= (step)
        elif key == "d":
            x += (step)


    return [x,y,z]
    # camera(x, y, z, x, y, z, 0, 1, 0)  # Update camera position based on player's movement

def draw():

    background(0)

    global scaling_factor
    # Define camera math
    #####################
    xCenter = ((float(mouseX) - (float(width)/2)) / float(width) ) * (4*PI)
    yCenter = ((float(mouseY) - (float(height)/2)) / float(height) ) * (2*PI)
    print("Angle:" + str(xCenter))
    #####################
    radius = 100
    camX = xCenter/radius # arc length, arc length/radius = angle
    # print(camX)
    camY = yCenter/radius
    #####################
    # print(modelX(0,0,0))


    # localise the player position based on the camera

    x,y,z = player()

    print(z)
    print(x)

    # dot = dotProduct(1,1,(z*cos(xCenter)),(z*sin(xCenter)))

    # calculate the new x and z based on the camera angle
    tz = z
    x = tz*cos(xCenter)
    z = tz*sin(xCenter)


    camera(0 + x, yCenter, 0 + z, (50*cos(xCenter)) + x, (50*yCenter), (50*sin(xCenter)) + z, 0, 1, 0)
    
    # pushMatrix()
    # fill(255,0,0)
    # noStroke()
    # translate((50*cos(xCenter)) + x, (50*yCenter), (50*sin(xCenter)) + z)
    # box(5)
    # popMatrix()

    print(z)
    print(x)

    # x = x/cos(camX)
    # z = z/cos(camX*2*PI)
    # z = z/cos(camX)
    # z = sin(camX) * z
    # x = cos(camX) * z
    # print(z)
    # print(x)

    # Load the map
    loadMap(0, 0, 0, 0)
    # Load the map
    # player()

