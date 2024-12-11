import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfile
from PIL import ImageTk, Image
import random
import os

# Window setup
window = tk.Tk()
window.title("Map Maker")
canvas = tk.Canvas(window, width=660, height=420, bg="cyan")
canvas.pack()

# Block size and grid dimensions
block_size = 11
grid_width = 21
grid_height = 33
offset = 20

#Gamemodes list
GAMEMODES = ["NONE",
    "Gem Grab",
    "Bounty",
]

gamemode_value = tk.StringVar(window)
gamemode_value.set(GAMEMODES[0]) # default value

#Gamemodes list
MIRROR = ["OFF",
    "Horizontal",
    "Vertical",
    "Diagonal"
]

mirror_value = tk.StringVar(window)
mirror_value.set(MIRROR[0]) # default value

#Tile Codes list
TILE_CODES = [".","M","Y","C","R","W","1","2"]

bSpawnNum = 3
rSpawnNum = 3

# Dropdown menu options
OPTIONS = ["DELETE",
    "Block_1",
    "Box",
    "Barrel",
    "Bush",
    "Water",
    "Blue Spawn("+ str(bSpawnNum) +")",
    "Red Spawn("+ str(rSpawnNum) +")"
]

menu_value = tk.StringVar(window)
menu_value.set(OPTIONS[1]) # default value

# Load images
empty= ImageTk.PhotoImage(Image.open("Map Blocks/Empty.png").resize((block_size, int(block_size + (block_size/2)) )))
box = ImageTk.PhotoImage(Image.open("Map Blocks/Box.png").resize((block_size, int(block_size + (block_size/2)) )))  
block_1 = ImageTk.PhotoImage(Image.open("Map Blocks/Block_1.gif").resize((block_size, int(block_size + (block_size/2)) ))) 
bush = ImageTk.PhotoImage(Image.open("Map Blocks/Bush.gif").resize((block_size, int(block_size + (block_size/2)) )))
barrel = ImageTk.PhotoImage(Image.open("Map Blocks/Barrel.gif").resize((block_size, int(block_size + (block_size/1.4)) )))
bSpawn = ImageTk.PhotoImage(Image.open("Map Blocks/Spawn_Blue.gif").resize((int(block_size + (block_size/1.25)), int(block_size + (block_size/1.25)) )))
rSpawn = ImageTk.PhotoImage(Image.open("Map Blocks/Spawn_Red.gif").resize((int(block_size + (block_size/1.25)), int(block_size + (block_size/1.25)) )))
water = ImageTk.PhotoImage(Image.open("Map Blocks/water.gif").resize((int(block_size), int(block_size) )))

# Create a list of images
images = [empty, block_1, box, barrel, bush, water, bSpawn, rSpawn]

start_image = images[0]
current_image_index = images.index(start_image) + 1

secret = 0

# Create a list for the map grid 
grid = []
count = 0
for i in range(grid_height):
    for j in range(grid_width):
        x = j * block_size + offset
        y = i * block_size + offset
        # set the correct color of the squares based on the count
        if (count % 2 == 0):
            color = '#ec9e6e'
        else:
            color = '#f9a576'
        grid.append({"x": x, "y": y, "color": color})
        count += 1

# Function to draw the map grid
def draw_grid(grid):
    canvas.create_rectangle(
        grid["x"],
        grid["y"],
        grid["x"] + block_size,
        grid["y"] + block_size,
        fill=grid["color"],
        outline=grid["color"],
    )

# Create a list of blocks 
blocks = []
for i in range(grid_height):
    for j in range(grid_width):
        x = (j * block_size + offset) + 0.1
        y = (i * block_size + offset) + 0.1
        # Use the first image (index 0) for all blocks
        image_index = 0 
        image = start_image
        edit = True
        blocks.append({"x": x, "y": y, "image": image, "image_index": image_index, "edit": edit})

# Function to draw a block
def draw_block(block):
    block["image_id"] = canvas.create_image(
        block["x"] + block_size // 2, 
        block["y"] + block_size // 2,
        anchor=tk.CENTER,
        image=block["image"]
    )

# Function to place a block when clicked on
def place_block(event):
    for block in blocks:
        if (block["x"] <= event.x <= block["x"] + block_size and
            block["y"] <= event.y <= block["y"] + block_size and block["edit"] == True):
                block["image_index"] = current_image_index % len(images)
                block["image"] = images[block["image_index"]]
                canvas.itemconfig(block["image_id"], image=block["image"])
    
    if (mirror_value.get() != "Off"):
        if (mirror_value.get() == "Horizontal"):
            x = 272 - event.x + 0.1
            y = event.y
        elif (mirror_value.get() == "Vertical"):
            x = event.x
            y = 404 - event.y + 0.1
        elif (mirror_value.get() == "Diagonal"):
            x = 272 - event.x + 0.1
            y = 404 - event.y + 0.1
        for block in blocks:
            if (block["x"] <= x <= block["x"] + block_size and
                block["y"] <= y <= block["y"] + block_size and block["edit"] == True):
                    block["image_index"] = current_image_index % len(images)
                    block["image"] = images[block["image_index"]]
                    canvas.itemconfig(block["image_id"], image=block["image"])


# Function to place a spawn
#def place_spawn(event):
#    global bSpawnNum
#    global rSpawnNum
#    if (block["x"] <= event.x <= block["x"] + block_size and
#            block["y"] <= event.y <= block["y"] + block_size):
#        if bSpawnNum != 0 and current_image_index == 5:
#            block["image_index"] = current_image_index % len(images)
#            block["image"] = images[block["image_index"]]
#            canvas.itemconfig(block["image_id"], image=block["image"])
#        elif rSpawnNum != 0 and current_image_index == 6:
#            block["image_index"] = current_image_index % len(images)
#            block["image"] = images[block["image_index"]]
#            canvas.itemconfig(block["image_id"], image=block["image"])
#            rSpawnNum -= 1
#        else:
#            return
# Function to change the current image to what is selected in dropdown menu
def change_current_image(event):
    global current_image_index
    current_image_index = OPTIONS.index(menu_value.get())

# Function to print the map code in the console
def export_map_code(event):
    count = 1
    code = ""
    for block in blocks:
        index = block["image_index"]
        code += TILE_CODES[index]
        
        if count % 21 == 0 and count != 0:
            code += "\n"
        count+=1
    
    export_file = asksaveasfile(mode='w', defaultextension=".txt")
    if export_file is None: return
    export_file.write(code)
    
# Function to import a map from a .txt file
def import_map_code(event):
    global secret
    file_name = askopenfilename(filetypes=[("Text files", "*.txt")])
    try:
        open(file_name, 'r')
    except TypeError:
        secret += 1
        return
    except FileNotFoundError:
        secret += 1
        if secret % 5 == 0: print("this is super cool easter egg. so cool")
        return
    txt = []
    with open(file_name, 'r') as file:
        for line in file:
            for tile in line.strip():
                txt += [tile]
    count = 0
    for block in blocks:
        if (block["edit"] == True):
            block["image_index"] = TILE_CODES.index(txt[count])
            block["image"] = images[TILE_CODES.index(txt[count])]
            canvas.itemconfig(block["image_id"], image=block["image"])
        count += 1
    secret = 0
    
# Function to clear the map
def clear_map(event):
    for block in blocks:
        if (block["edit"] == True):
            block["image_index"] = TILE_CODES[0]
            block["image"] = images[0]
            canvas.itemconfig(block["image_id"], image=block["image"])

#Function to change the current gamemode
def change_current_gamemode(event):
    global gamemode_value
    print (gamemode_value.get())
    for block in blocks:
        if (block["x"] <= 135.1 <= block["x"] + block_size and
            block["y"] <= 201.1 <= block["y"] + block_size):
                block["image_index"] = 0 % len(images)
                if (gamemode_value.get() == "NONE"):
                    block["image_index"] = 0 % len(images)
                    block["edit"] = True
                    block["image"] = ImageTk.PhotoImage(Image.open("Map Blocks/Empty.png").resize((int(block_size + (block_size/1)), int(block_size + (block_size/1)) )))
                elif (gamemode_value.get() == "Gem Grab"):
                    block["image_index"] = 0 % len(images)
                    block["edit"] = False
                    block["image"] = ImageTk.PhotoImage(Image.open("Map Blocks/mine.gif").resize((int(block_size + (block_size/1)), int(block_size + (block_size/1)) )))
                elif (gamemode_value.get() == "Bounty"):
                    block["image_index"] = 0 % len(images)
                    block["edit"] = False
                    block["image"] = ImageTk.PhotoImage(Image.open("Map Blocks/bounty_star.gif").resize((int(block_size + (block_size/1)), int(block_size + (block_size/1)) )))
                    canvas.itemconfig(block["image_id"], image=block["image"])



# Draw grid
for squares in grid:
    draw_grid(squares)
    
# Draw initial blocks
for block in blocks:
    draw_block(block)


# Block Dropdown menu
dropdown_label = tk.Label(canvas, text="Selected Block:", bg="cyan")
dropdown = tk.OptionMenu(window, menu_value, *OPTIONS, command=change_current_image)
dropdown_label.place(x=280, y=grid_height)
dropdown.place(x=(int(dropdown_label.place_info()['x']) + 170), y=int(dropdown_label.place_info()['y'])-5)

# Gamemode Dropdown menu
gamemode_label = tk.Label(canvas, text="Selected Gamemode:", bg="cyan")
gamemode_menu = tk.OptionMenu(window, gamemode_value, *GAMEMODES, command=change_current_gamemode)
gamemode_label.place(x=280, y=grid_height+50)
gamemode_menu.place(x=(int(gamemode_label.place_info()['x']) + 170), y=int(gamemode_label.place_info()['y'])-5)

# Mirror Dropdown menu
mirror_label = tk.Label(canvas, text="Mirror Mode:", bg="cyan")
mirror_menu = tk.OptionMenu(window, mirror_value, *MIRROR)
mirror_label.place(x=280, y=grid_height+100)
mirror_menu.place(x=(int(mirror_label.place_info()['x']) + 170), y=int(mirror_label.place_info()['y'])-5)

# Import map code button
import_mc = tk.Button(canvas, text = "Import")
import_mc.place(x=280, y=grid_height+150)
import_mc.bind("<Button-1>", import_map_code)

# Export map code button
export_mc = tk.Button(canvas, text = "Export")
export_mc.place(x=int(import_mc.place_info()['x'])+120, y=int(import_mc.place_info()['y']))
export_mc.bind("<Button-1>", export_map_code)

# Clear Map
clear = tk.Button(window, text = "Clear Map", bg = "lightcoral")
clear.pack(side="bottom")
clear.bind("<Button-1>", clear_map)

# Bind place block 
canvas.bind("<B1-Motion>", place_block)
canvas.bind("<Button-1>", place_block)
#canvas.bind("<Button-1>", place_spawn)


window.mainloop()






























































































































































#print("this is super cool easter egg. so cool")