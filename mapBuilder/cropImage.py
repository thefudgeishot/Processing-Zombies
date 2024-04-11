from PIL import Image


i = 1
while i <= 13:
    image = Image.open("C:/Users/hoeth/OneDrive/Desktop/3D-SpaceInvaders/crater_thing_lol.png")
    image = image.crop((0, (-50+(i*50)), 50, (i*50)))
    print(str(-50+(i*50))+ " " + str(-50+(i*50))+ " " + str(i*50)+ " " + str(i*50))
    image.save(f"C:/Users/hoeth/OneDrive/Desktop/3D-SpaceInvaders/mapBuilder/crater/{i}.png")
    i += 1



