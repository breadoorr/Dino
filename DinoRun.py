# DinoRun.py
# Author: Daria Chystiakova (G21065197)
# Email: DChystiakova@uclan.ac.uk
# Description: The DinoRun.py is the grogram that provides a simple game, which allows the user to manipulate the main character of game - dino.
# The point of the game is to score the most numbers of points possible going through multiple obstacles at the same time.
# the new rule implemented in this version of the game is: when dino touches the bird, 10 points are incremented


# importing tkinter library in order to create a window and then proceed with a game in this window
from tkinter import *
# importing random library
import random 
# declaring variables that contain maesures of the game window
WIDTH = 800
HEIGHT = 600
# creating a window
win = Tk()
win.title('Dino Run')
win.geometry(str(WIDTH) + 'x' + str(HEIGHT))
# decring an array with colors that will be used for the background
colors = ['#9F9C9D', '#F3D582', '#BEA382', '#9F7D74', '#6A2D23', '#242025', '#9F9C9D']
# creating a canvas in the window
canvas = Canvas(win, width=WIDTH, height=HEIGHT, bg=colors[0])
canvas.pack()

# importing images that will be used for the game objects
# Reference: CO1417, week07-parallax, step0704, adding_obstacles.py
# All images were taken from the 'resources' folder provided in CO1417, week08-capstone-dino
dino_frames = [PhotoImage(file='./resources/dino%i.png' % i) for i in range(5)]
ground_img = PhotoImage(file='./resources/ground.png')
cloud_img = PhotoImage(file='./resources/cloud.png')
cactus_img = PhotoImage(file='./resources/cactus-small.png')
big_cactus_img = PhotoImage(file='./resources/cactus-big.png')
# Source for the image of the bird: https://www.google.com/url?sa=i&url=https%3A%2F%2Ftenor.com%2Fview%2Ftero-gif-25926692&psig=AOvVaw33qTsk7KjVBcURMZGFGd45&ust=1678716274023000&source=images&cd=vfe&ved=0CBAQjhxqFwoTCMDN65PI1v0CFQAAAAAdAAAAABAE
tero_frames = [PhotoImage(file = f'./resources/sprite_{i:02d}.png') for i in range(16)]

# declaring variables for distance between the obstacles, game state, jump state, indexes for animations, pause state and all of the objects that will be created in the window
# Reference for the distance: CO1417, lecture slides, week 7-8, slide 34
distance1 = random.randrange(int(0.75 * WIDTH), int(1.25 * WIDTH), 10)
distance2 = distance1 + random.randrange(int(0.75 * WIDTH), int(WIDTH), 10)
game_over = False
in_a_jump = False
# declaring variables for the score and delay between the update of the canvas
points = 0
DELAY = 100
# Reference for the jump offsets and indexes: CO1417, week06-animations, step0604, interactive_flappy_wings.py
jump_offsets = [-60, -45, -30, -20, -10, 0, 0, 0, 10, 20, 30, 45, 60]
color_index = 0
jump_index = 0
animation_index = 0
index = 0
tero_index = 0
in_pause = False
# Reference for the objects: CO1417, week07-parallax, step0704, adding_obstacles.py
score = ''
dino_obj = ''
ground_obj = ''
cloud_obj = ''
cloud_obj1 = ''
tero_obj = ''
cactus_obj = ''
big_cactus_obj = ''
string = ''
text1 = ''
high = 0
high_t = ''
text = ''


# function that creates and displays objects on the canvas, such as pictures of the dino or obstacles and text 
# Reference for the objects: CO1417, week07-parallax, step0704, adding_obstacles.py
def create():
    global dino_obj, ground_obj, cloud_obj, cloud_obj1, cactus_obj, big_cactus_obj, string, text1, score, high_t, tero_obj
    ground_obj = canvas.create_image(WIDTH / 2, HEIGHT - ground_img.height() / 2, image=ground_img)
    cloud_obj = canvas.create_image(WIDTH/2, HEIGHT/2 - cloud_img.height(), image=cloud_img)
    cloud_obj1 = canvas.create_image(WIDTH/2+200, HEIGHT/2 - cloud_img.height()+30, image=cloud_img)
    tero_obj = canvas.create_image(WIDTH-20, HEIGHT//2, image = tero_frames[0])
    cactus_obj = canvas.create_image(distance1, HEIGHT - ground_img.height() - cactus_img.height()/2+10, image=cactus_img)
    big_cactus_obj = canvas.create_image(distance2, HEIGHT - ground_img.height() - big_cactus_img.height()/4-10, image=big_cactus_img)
    dino_obj = canvas.create_image(50, HEIGHT - ground_img.height() - dino_frames[0].height()/4-10, image=dino_frames[0])
    string = canvas.create_rectangle(0, HEIGHT-45, WIDTH, HEIGHT, fill='#918f8d', outline='#918f8d')
    text1 = canvas.create_text(255, HEIGHT-45 + 20, text="CO1417  Dino Run  |  Q: Quit  R: Restart  P: Pause", font=('Fixedsys', 14), fill='white')
    score = canvas.create_text(WIDTH-90, HEIGHT-45+20, text="Score:" + f"{points:09d}", font=('Fixedsys', 14), fill='white')
    high_t = canvas.create_text(WIDTH - 220, HEIGHT-45+20, text="High:" + f"{high}", font=('Fixedsys', 14), fill='white')
   


# function that moves objects on the screen and updates their state on the canvas
# Reference: CO1417, week07-parallax, step0704, adding_obstacles.py
def update():
    global animation_index, index, in_a_jump, jump_offsets, jump_index, points, score, high_t, distance1, distance2, DELAY, text, color_index, tero_index, bird
    # update is taking place only if the game is not over
    if not game_over:
        # randomosing distances every time
        distance1 = random.randrange(int(0.75 * WIDTH), int(1.25 * WIDTH), 10)
        distance2 = distance1 + random.randrange(int(0.75 * WIDTH), int(1.25 * WIDTH), 10)
        # moving canvas objects
        (x, y) = canvas.coords(cloud_obj)
        if x >= 0:            
            canvas.move(cloud_obj, -3, 0)
        else:            
            canvas.move(cloud_obj, WIDTH, 0)

        (x, y) = canvas.coords(cloud_obj1)
        if x >= 0: 
            canvas.move(cloud_obj1, -2, 0)
        else:
            canvas.move(cloud_obj1, WIDTH, 0)

        (x, y) = canvas.coords(ground_obj)
        if x >= 0:            
            canvas.move(ground_obj, -15, 0)
        else:            
            canvas.move(ground_obj, WIDTH, 0)

        (x, y) = canvas.coords(cactus_obj)
        if x >= 0:            
            canvas.move(cactus_obj, -15, 0)
        else:            
            canvas.move(cactus_obj, distance1, 0)

        (x, y) = canvas.coords(big_cactus_obj)
        if x >= 0:            
            canvas.move(big_cactus_obj, -15, 0)
        else:            
            canvas.move(big_cactus_obj, distance2, 0)

        (x, y) = canvas.coords(tero_obj)
        if x >= 0:
            canvas.move(tero_obj, -7, 0)
        else:
            canvas.move(tero_obj, WIDTH, -(random.randint(1, 50)))

        canvas.itemconfig(tero_obj, image = tero_frames[tero_index])
        tero_index += 1
        if tero_index>= len(tero_frames):
            tero_index = 0

        # imitating animation of the dino
        canvas.itemconfig(dino_obj, image = dino_frames[index])
        index += 1
        if index >= 3:            
            index = 0
        # moving dino depending on the user input
        if in_a_jump:            
            jump_offset = jump_offsets[jump_index]
            canvas.move(dino_obj, 0, jump_offset)
            jump_index = jump_index + 1
            if jump_index > len(jump_offsets)-1:                
                jump_index = 0
                in_a_jump = False
        # calling the function that detects collision between dino and obstacle
        collision()
        # incrementing the score on 1 every 100 ms
        points += 1
        # in order to make the game harder depending on time the user plays decrementing delay on 2 every 100 points and also changing the background color
        if points %100 == 0:            
            DELAY -= 2
            color_index += 1
            if color_index >= len(colors):                
                color_index = 0
        # updating background color, score and highest score
        canvas.config(bg=colors[color_index])
        canvas.itemconfig(score, text="Score:" + f"{points:09d}")
        canvas.itemconfig(high_t, text="High:" + f"{high}")
        # calling an update function only if the game is not paused
        # else, showing Pause label
        if not in_pause:            
            win.after(DELAY, update)
        else:            
            text = canvas.create_text(WIDTH//2, HEIGHT//2, text= 'Paused', font = ('Fixedsys', 50), fill='white')
            

# function that changes the state of the dino(in a jump or not)
# Reference: CO1417, week06-animations, step0604, interactive_flappy_wings.py
def jump(__self__):
    global in_a_jump
    if not in_a_jump:
        
        in_a_jump = True


# function that detects the user's input and pauses or unpauses the game 
def pause(event):
   global in_pause, text 
   if event and not in_pause:
        
        in_pause = True
   elif event and in_pause:
        
        in_pause = False
        canvas.delete(text)
        win.after(DELAY, update)


# function that detects collision between dino and cactuses
def collision():
    global points, high, game_over, bird, luck
    (x, y) = canvas.coords(dino_obj)
    (x1, y1) = canvas.coords(cactus_obj)
    (x2, y2) = canvas.coords(big_cactus_obj)
    (x3, y3) = canvas.coords(tero_obj)
    # if coordinates of the dino and a cactus are overlapping, the game is over, the label of it is displayed, points are reseted 
    # and highest score is updated in case it is lower than the number of points
    if x + dino_frames[0].width()/2-5 >= x1 - cactus_img.width()/2+10 and x - dino_frames[0].width()/2+5 <= x1 + cactus_img.width()/2-10 and y + dino_frames[0].height()/4-5 >= y1-cactus_img.height()/2:
        canvas.itemconfig(dino_obj, image = dino_frames[4])
        game_over = True
        canvas.create_text(WIDTH//2, HEIGHT//2, text="GAME OVER!", fill='white', font=('Fixedsys', 50))
        if points > high:
            high = points
        points = 0
    elif x + dino_frames[0].width()/2-5 >= x2 - big_cactus_img.width()/2+10 and x - dino_frames[0].width()/2+5 <= x2 + big_cactus_img.width()/2-10 and y + dino_frames[0].height()/4-5 >= y2-big_cactus_img.height()/2:
        canvas.itemconfig(dino_obj, image = dino_frames[4])
        game_over = True
        canvas.create_text(WIDTH//2, HEIGHT//2, text="GAME OVER!", fill='white', font=('Fixedsys', 50))
        if points > high:
            high = points
        points = 0
    if x + dino_frames[0].width()/2-5 >= x3 - tero_frames[0].width()//2 and x - dino_frames[0].width()/2+5 <= x3 + tero_frames[0].width()//2 and y - dino_frames[0].height()/4-5 >= y3+tero_frames[0].height()//2:
        points += 10
       
        

# function that allows user to restart the game
def restart(event):
    global canvas, points, high, game_over, jump_index, in_a_jump, DELAY, color_index, in_pause, bird
    # fully destroying the canvas and all the objects on it and creating a new one
    canvas.destroy()
    canvas = Canvas(win, width=WIDTH, height=HEIGHT, bg = colors[0])
    canvas.pack()
    if points > high:
        high = points
    points = 0
    # calling a create function in order to return all of the objects on the new canvas
    create()
    # reseting all of the values to their initial state
    jump_index = 0
    in_a_jump = False
    if in_pause:
        in_pause = False
        update()
    color_index = 0
    DELAY = 100
    # if the game was over calling an update function again
    if game_over:
        game_over = False
        update()
   

# function that allows user to quit the game, uses built-in functins to quit canvas and the window
def quit(event):
   canvas.quit()
   win.quit()


# calling a create function
create()
# binding functions with the keys in order for the user to operate
win.bind("<Key-q>", quit)
win.bind("<Key-Q>", quit)
win.bind("<Key-r>", restart)
win.bind("<Key-R>", restart)
win.bind("<space>", jump)
win.bind("<Key-P>", pause)
win.bind("<Key-p>", pause)
# calling an update function
win.after(0, update)
# creating a mainloop that listens for the key-preses the user provides
win.mainloop()
