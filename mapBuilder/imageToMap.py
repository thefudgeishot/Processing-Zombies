from PIL import Image

# Open the image file
# for each file in directory
for i in range(10, 16):

    image = Image.open(f"C:/Users/hoeth/OneDrive/Desktop/3D-SpaceInvaders/mapBuilder/dust2/{i}.png")

    ylevel = i
    width, height = image.size

    dataIndex = {}

    # Iterate over each pixel
    for z in range(height):
        for x in range(width):
            # Get the RGB values of the pixel at (x, z)

            r, g, b, a = image.getpixel((x, z))

            if a >= 200:
                print(f"Pixel at ({x}, {z}): R={r}, G={g}, B={b}")
                dataIndex.update({(x,ylevel,z): (r,g,b)})

    # save the data to a file
    with open("C:/Users/hoeth/OneDrive/Desktop/3D-SpaceInvaders/SpaceInvaders/data/maps/test7.txt", "a") as file:
        for key, value in dataIndex.items():
            file.write("[" + str(key[0]) + "," + str(key[1]) + "," + str(key[2]) + "," + str(value[0]) + "," + str(value[1]) + "," + str(value[2]) + "]\n")
            # print("[" + str(key[0]) + "," + str(key[1]) + "," + str(key[2]) + "," + str(value[0]) + "," + str(value[1]) + "," + str(value[2]) + "]\n")
