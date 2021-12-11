from socket import socket
import threading
import time
import random
import colorsys

# Settings 
# These things are the only things you need to change!
premium = "true"  # keep this set to "true" if you have Twitch Prime or Twitch Turbo. If you don't have either of them, set it to "false"
brightColoursOnly = "true" # If you set this to "true", the script will only generate bright colours. Set this to "false" if you want random colours that include more dark ones
customColours = [ ] # put custom colours here if you don't want random colours; use the following format: ['#111111', '#FF00FF', '#2F2B2A', '#B3F9FF', '#484766']; Put nothing in between the [ ] if you want random colors!; custom colors will override the brightColorsOnly setting!
colourChangeMin = 4200  # minimum time between every colour change (in milliseconds); don't set this too low!
colourChangeMax = 18700  # maximum time between every colour change (in milliseconds)
twitchName = "xheaveny_"  # your Twitch name
twitchOAuthToken = "oauth:..."  # your OAuth token; don't remove the PASS at the beginning; get one from: https://twitchapps.com/tmi/
# End of settings; if you changed the settings above, you can now run this script by double-clicking the file OR by opening the console and running "py FILENAME"

print('Starting the script...')

sockt = socket()
regularColours = "Blue", "BlueViolet", "CadetBlue", "Chocolate", "Coral", "DodgerBlue", "Firebrick", "GoldenRod", "Green", "HotPink", "OrangeRed", "Red", "SeaGreen", "SpringGreen", "YellowGreen"  # colors that are available for everyone, sorted alphabetically

def sendRequest(data):
    sockt.send(bytes(data + '\r\n', 'utf-8'))  # sends a request to Twitch's irc server using the UTF-8 standard

def changeColour():
    if premium == "true":
        if len(customColours) == 0:
            if brightColoursOnly == "true":
                while True:
                    delay = random.choice(range(colourChangeMin, colourChangeMax)) / 1000
                    print("Colour change in " + str(delay) + " seconds!")
                    time.sleep(delay)
                    randomNumber = random.randint(0, 100)
                    tuple = coloursys.hsv_to_rgb(randomNumber / 100, 1, 1)  # only generates bright colours
                    rgb = [int(i * 255) for i in tuple]
                    hexValue = '%02x%02x%02x' % (rgb[0], rgb[1], rgb[2])
                    sendRequest('PRIVMSG #xheaveny_ :/colour #' + hexValue)
                    print("Changed colour to " + hexValue + "!")
            else:
                while True:
                    delay = random.choice(range(colourChangeMin, colourChangeMax)) / 1000
                    print("Colour change in " + str(delay) + " seconds!")
                    time.sleep(delay)
                    randomNumber = random.randint(0, 16777215)  # selects a random colour; 16777215 stands for the amount of different colours that are available
                    hexValue = str(hex(randomNumber))
                    sendRequest('PRIVMSG #xheaveny_ :/colour #' + hexValue[2:])
                    print("Changed colour to #" + hexValue[2:] + "!")
        else:
            while True:
                delay = random.choice(range(colourChangeMin, colourChangeMax)) / 1000
                print("Colour change in " + str(delay) + " seconds!")
                time.sleep(delay)
                hexValue = random.choice(customColours)
                sendRequest('PRIVMSG #xheaveny_ :/colour ' + hexValue)
                print("Colour change in " + hexValue + "!")

    else:
        while True:
            delay = random.choice(range(colourChangeMin, colourChangeMax)) / 1000
            print("Colour change in " + str(delay) + " seconds!")
            time.sleep(delay)
            selectedColour = random.choice(regularColours);
            sendRequest("PRIVMSG #xheaveny_ :/colour " + selectedColour)
            print("Changed colour to " + selectedColour + "!")


def keepRunning():
    while True:
        chat = sockt.recv(1024).decode('utf -8', errors='replace')  # listens to messages from Twitch

        if "PING" in chat:
            sendRequest("pong...")  # keeps the script running


def runScript():
    print('\n')
    print('========= Settings =========')
    print("Premium = " + premium)
    print("brightColoursOnly = " + brightColoursOnly)
    print("Using custom colours? = " + ("true" if len(customColours) > 0 else "false"))
    print("Minimum delay = " + str(colourChangeMin))
    print("Maximum delay = " + str(colourChangeMax))
    print('============================')
    print('\n')
    sockt.connect(('irc.chat.twitch.tv', 6667))  # connects to Twitch.tv
    sendRequest("PASS " + twitchOAuthToken)  # your OAuth token
    sendRequest("NICK " + twitchName)  # your Twitch name
    sendRequest('CAP REQ :twitch.tv/commands')
    sendRequest('CAP REQ :twitch.tv/tags')
    keepRunning()


timerr = threading.Thread(target=changeColour)
timerr.start()

runScript()
