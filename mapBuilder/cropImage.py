from PIL import Image


i = 1
while i <= 35:
    image = Image.open("C:/Users/hoeth/OneDrive/Desktop/3D-SpaceInvaders/city_meteor_statue.png")
    image = image.crop((0, (-50+(i*50)), 50, (i*50)))
    print(str(-50+(i*50))+ " " + str(-50+(i*50))+ " " + str(i*50)+ " " + str(i*50))
    image.save(f"C:/Users/hoeth/OneDrive/Desktop/3D-SpaceInvaders/mapBuilder/city/{i}.png")
    i += 1


def setup():
    # set environment settings
    # set background
    # set title
    # show keybinds hints

def draw():
    
    # load sky color

    # get player rotation in radians based on the mouse position
    # playerRot = (mouseX - (width/2)) / width * 4*PI
    # get vertical rotation of the players head based on the mouse position
    # playerHeadRot = (mouseY - (height/2)) / height * 2*PI

    # call function to get the players delta position

    # run gravity calculations
    # call function to check if there is a block under the player and if so, start a timer 

    # call function to check if there is no block under the player and if so run gravity calculations
    # calculate delta time / time since player was last on a block
    # multiply gravity by delta time to get the players delta y position

    # call function to check if there is a block in front of the player and if so, stop the players positive delta x position
    # additionally check if there are blocks around the player and if the player will collide with the block, stop the players positive delta x position

    # repeat the above process for the negative delta x position, and the positive and negative delta z position

    # begin translation of the camera to the players position   
    # camera(x, y, z, (50*cos(playerRot)) + x, (50*playerHeadRot)+y, (50*sin(playerRot)) + z, 0, 1, 0) 

    # load map

    # load random coordinates into array for each zombie to spawn at
    # each frame run an A* pathfinding algorithm per random coordinate to find the shortest path to the player for each zombie
    # move each zombie along the path to the player
    # if a zombie is within a certain distance of the player, damage the player

    # if the player left clicks call function to fire a bullet in the direction the player is facing
    # if the bullet collides with a zombie, remove the zombies coordinate from the array




