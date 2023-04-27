import time
import board
import adafruit_dotstar as dotstar

# number of LEDs, baudrate = clock rate
dots = dotstar.DotStar(board.SCK, board.MOSI, 52, brightness=0.2, auto_write = True)#, baudrate = 4000000)

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

# Reverses fret #
def getFret(x):
    if(x == 1):
        return 12
    elif(x == 2):
        return 11
    elif(x == 3):
        return 10
    elif(x == 4):
        return 9
    elif(x == 5):
        return 8
    elif(x == 6):
        return 7
    elif(x == 7):
        return 6
    elif(x == 8):
        return 5
    elif(x == 9):
        return 4
    elif(x == 10):
        return 3
    elif(x == 11):
        return 2
    else:
        return 1

# Checks if the user paused the song
def isPaused():
    #MINA <---------------------------------------------------------------------------
    return False

# Checks which speed is selected
def checkSpeed():
    pingSpeed = 1   # MINA <---------------------------------------------------------------------------
    return pingSpeed

# Checks if the song is on loop
def isLooped():
    # MINA <---------------------------------------------------------------------------
    return False

# read the song txt file
song = open('song.txt', 'r')
Lines = song.readlines()
# the queue of notes
queue = []

# takes the first line as total song time in seconds
#songLength = Lines.pop(0)

# for every line in the file
for line in Lines:
    # split the line by the commas
    note = line.split(',')
    # strip spaces/breaks from each part
    for i in range(len(note)):
        note[i] = note[i].strip()
    
    # process its relevant values: String, Fret, Length
    rgb = getColor(int(note[0]))
    #fret = note[1]
    fret = 4*(getFret(int(note[1]))-1) + (int(note[0])-1)
    length = note[2]
    # and add them as a tuple to the queue
    queue.append((rgb, fret, length))

# note counter
nc = 0
notFinished = True

# main loop to turn on the LEDs
while(notFinished):
    # Ping web server to see if paused
    paused = isPaused()
    # while the song is not paused, play a note
    while not paused:
        # Checks user's selected speed
        speed = checkSpeed()

        # if we are out of notes, exit while loop
        if(nc == len(queue)):
            # if looping, go back to beginning
            if (isLooped()):
                nc = 0
            # otherwise exit loop
            else:
                notFinished = False
                paused = True
                break

        #grab the current note
        curNote = queue[nc]
        print(curNote)
        # turn off all LEDs
        dots.fill((0, 0, 0, 0.1))

        # light up the correct LED with the correct color, [1] = fret # with +4 offset, [0] is rgb value
        dots[int(curNote[1])+4] = curNote[0]

        # wait amount of time note lasts for (in seconds) times the chosen speed
        time.sleep(float(curNote[2])*speed)

        #turn off all LEDs
        dots.fill((0, 0, 0, 0.1))

        # increment note count
        nc += 1

        #Ping web server to see if paused
        paused = isPaused()
