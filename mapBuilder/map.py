import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser

def open_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        print("Selected file:", file_path)
        load_map(file_path)
        newFile = True

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            for key, value in dataIndex.items(): # Write the map to text file
                file.write("[" + str(key[0]) + "," + str(key[1]) + "," + str(key[2]) + "," + str(value[0]) + "," + str(value[1]) + "," + str(value[2]) + "]\n")
                print("[" + str(key[0]) + "," + str(key[1]) + "," + str(key[2]) + "," + str(value[0]) + "," + str(value[1]) + "," + str(value[2]) + "]\n")
        print("Saved file:", file_path)

def on_box_click(event):
    box = event.widget
    box.configure(bg=color1)  # Change the color of the clicked box

    # Get the row, column and colour of the clicked box
    row = int(box.grid_info()["row"]) - 2
    column = int(box.grid_info()["column"]) - 2
    color = box.cget("bg")
    print(color)

    dictData = dataIndex.get((row,ylevel,column))
    if dictData != None:
        dataIndex.pop((row,3,column), None)
    
    # convert the color to rgb
    r,g,b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
    dataIndex.update({(row,ylevel,column): (r,g,b)})
    print(dataIndex[(row,ylevel,column)])

def on_slider_move(event):
    value = slider.get()
    global ylevel
    ylevel = value
    loadBoxes()

def pick_color():
    color = colorchooser.askcolor(title="Pick a Color")
    if color[1]:
        print("Selected color:", color[1])
        global color1
        color1 = color[1]
        # root.configure(bg=color[1])  # Set the background color of the root window
        loadButton()

def load_map(filePath):

    mapData = open(filePath, "r").readlines()
    print(mapData)

    dataIndex = {}

    for line in mapData:
        # split and convert the data
        data = str(line).strip("[]").strip("]\n").split(",")
        print(data)
        x,y,z = int(data[0]), int(data[1]), int(data[2])
        r,g,b = int(data[3]), int(data[4]), int(data[5])
        dataIndex.update({(x,y,z): (r,g,b)})
    
    return dataIndex

dataIndex = load_map(f"C:/Users/hoeth/OneDrive/Desktop/3D-SpaceInvaders/SpaceInvaders/data/maps/test.txt")
newFile = False
ylevel = 3
color1 = "#ff0000"

root = tk.Tk()

# DARK MODE 
root.configure(bg='white')

if newFile == True:
    root.update()

# Set fixed size for grid cells
for i in range(20):
    root.columnconfigure(i+2, minsize=25)
    root.rowconfigure(i+2, minsize=25)

def loadBoxes():
# Create 20x20 grid of boxes
    for i in range(20):
        for j in range(20):
            if dataIndex != None:
                if (i,ylevel,j) in dataIndex:
                    r,g,b = dataIndex[(i,ylevel,j)]
                    box = tk.Label(root, width=2, height=1, relief='solid', bg='#%02x%02x%02x' % (r,g,b))
                else:
                    box = tk.Label(root, width=2, height=1, relief='solid', bg='white')
                box.grid(row=(i+2), column=(j+2), sticky="nsew")  # Use sticky="nsew" to prevent scaling
                box.bind('<Button-1>', on_box_click)  # Bind left-click event to the box
            else:
                box = tk.Label(root, width=2, height=1, relief='solid', bg='white')
                box.grid(row=(i+2), column=(j+2), sticky="nsew")  # Use sticky="nsew" to prevent scaling
                box.bind('<Button-1>', on_box_click)  # Bind left-click event to the box

# Create "Open File" button
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.grid(row=0, column=0, padx=10, pady=10)

# Create "Save File" button
save_button = tk.Button(root, text="Save File", command=save_file)
save_button.grid(row=0, column=1, padx=10, pady=10)

# Create vertical slider
slider = tk.Scale(root, from_=0, to=20, orient='vertical', command=on_slider_move, length=450)
slider.set(ylevel)
slider.grid(row=1, column=1, padx=10, pady=10, rowspan=20)  # Use rowspan to occupy multiple rows

# Create color picker button
def loadButton():
    color_button = tk.Button(root, text="Pick Color", command=pick_color, bg=color1)
    color_button.grid(row=1, column=0, padx=10, pady=10, rowspan=20)  # Use rowspan to occupy multiple rows

loadButton()

# Create reload button
reload_button = tk.Button(root, text="Reload", command=loadBoxes)
reload_button.grid(row=2, column=0, padx=10, pady=10, rowspan=15) # Use rowspan to occupy multiple rows

root.mainloop()