import time
import board
import adafruit_dotstar as dotstar

# number of LEDs, baudrate = clock rate
dots = dotstar.DotStar(board.SCK, board.MOSI, 12, brightness=0.2, auto_write = True)#, baudrate = 4000000)

# EXAMPLE CODE:
# https://docs.circuitpython.org/projects/dotstar/en/latest/api.html#adafruit_dotstar.DotStar.fill
# (R,G,B,brightness)
# dots.fill((255, 255, 255, 0.1))
# dots[#] = (255, 255, 255)

# # FOR TESTING
# L = ["370\n", "1, 5, 1.5, 1.34\n", "2, 3, 2.2, 1.4\n", "3, 4, 1, 1.5\n"]

# # writing to file
# file1 = open('song.txt', 'w')
# file1.writelines(L)
# file1.close()
# # END TESTING

# takes string number and returns rgb tuple value
def getColor(string):
    if(string == 1):
        return (255, 0, 0)      # red
    elif(string == 2):
        return (255, 255, 0)    # yellow
    elif(string == 3):
        return (0, 0, 255)      # blue
    elif (string == 4):
        return (255, 128, 0)    # orange
    else:
        return (0,0,0)

# read the song txt file
song = open('song.txt', 'r')
Lines = song.readlines()
# the queue of notes
queue = []

# takes the first line as total song time in seconds
songLength = Lines.pop(0)

# for every line in the file
for line in Lines:
    # split the line by the commas
    note = line.split(',')
    # strip spaces/breaks from each part
    for i in range(len(note)):
        note[i] = note[i].strip()
    
    # process its relevant values
    rgb = getColor(int(note[0]))
    #fret = note[1]
    fret = 4*(note[1]-1) + (note[0]-1)
    length = note[2]
    # and add them as a tuple to the queue
    queue.append((rgb, fret, length))

# note counter
nc = 0
stillPlaying = True

# main loop to turn on the LEDs
while(stillPlaying):
    # if we are out of notes, exit while loop
    if(nc == len(queue)):
        stillPlaying = False
        break
    
    curNote = queue[nc]
    print(curNote)
    # turn off all LEDs
    dots.fill((0, 0, 0, 0.1))

    # light up the correct LED with the correct color
    dots[int(curNote[1])] = curNote[0]

    # wait amount of time note lasts for (in seconds)
    time.sleep(float(curNote[2]))

    # increment note count
    nc += 1
