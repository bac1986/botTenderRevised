import tkinter as tk
import tkinter.font as tkFont
#import tkinter.messagebox as tkmb
from PIL import Image, ImageTk  # pip install pillow
import time
import serial  # pip install serial
import subprocess
#from LED_Control import *
#import gpiozero as GPIO

# GPIO.setmode(GPIO.BOARD)
#GPIO.setup(27, GPIO.OUT)

# arduino1 = serial.Serial('/dev/TTY/ACM0', baudrate=9600, timeout=0.1)
# arduino1 = serial.Serial(port='COM6',baudrate=115200,timeout=1)
arduino = serial.Serial('COM3', 9600, timeout=0.1)
arduino.setRTS(False)
arduino.close()

# globals
global ingredientsArray
ingredientsArray = [["Vodka", "Rum", "Triple sec", "Coke", "Cranberry Juice", "Lime Juice", "Whiskey"],
                    ["1000000", "0100000", "0010000", "0001000", "0000100", "0000010", "0000001"]]
global recipeArray
recipeArray = [["Cuba Libre", "Harpoon", "Cape Codder", "Kamikaze", "Vodka Gimlet", "Cranberry Vodka"],
               ["0101010", "1010110", "1000110", "1010010", "1000010", "1000100"],
               ["0\n", "60\n", "38\n", "34\n", "50\n", "47\n"],  # vodka
               ["47\n", "0\n", "0\n", "0\n", "0\n", "0\n"],  # rum
               ["0\n", "20\n", "0\n", "33\n", "0\n", "0\n"],  # triple sec
               ["47\n", "0\n", "0\n", "0\n", "0\n", "0\n"],  # coke
               ["0\n", "10\n", "57\n", "0\n", "0\n", "57\n"],  # cran juice
               ["6\n", "10\n", "5\n", "33\n", "50\n", "0\n"],  # lime juice
               ]

global primeArray
primeArray = ["10\n", "10\n", "10\n", "10\n", "10\n", "10\n"]

# RF Inventory Scan
global fillAmount
fillAmount = [100] * 6
try:
    inventory = open('botInventory.txt')
except IOError:
    inventory = open('botInventory.txt', 'w')
    for i in range(6):
        # inventory.write(valueatRFID)
        inventory.write('\n')
        inventory.write(ingredientsArray[0][i])
        inventory.write('\n')
        inventory.write('fill: \n')
        inventory.write(str(fillAmount[i]))
    inventory.close()
finally:
    inventory = open('botInventory.txt', 'a')
    inventory.close()


class Page(tk.Frame):
    def __init__(self, *args, **kwargs) -> object:
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


global userID
userID = ['']
global filename
filename = ''


class Page0(Page):  # login page
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs, bg='gray24')
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        fatFingerFont2 = tkFont.Font(family='Bell Gothic Std Light', size=34)
        entryFont = tkFont.Font(family='Bell Gothic Std Light', size=16)
        welcomeFont = tkFont.Font(family='Letter Gothic Std', size=42, weight='bold')
        label = tk.Label(self, text="Welcome to BotTender!", font=welcomeFont, bg='gray24', fg='gray99')
        label.pack(side="top", fill="both")

        # def pinKeyboard(event):
        # alreadyOpen=False
        # if alreadyOpen == False:
        # subprocess.call("matchbox-keyboard", shell=True)
        # alreadyOpen=True

        pinEntry = tk.Label(self, text='Enter PIN:', font=fatFingerFont, bg='gray24', fg='ghost white')
        pinEntry.place(relx=0.315, rely=175 / 600)
        pinLogin = tk.Entry(self, bd=5, font=entryFont)
        pinLogin.place(relx=490 / 1024, rely=175 / 600, height=40, width=200)

        # pinLogin.focus_force()
        # pinLogin.bind("<Button-1>", pinKeyboard)

        def RFloginpoll():
            start = time.time()
            data = ''
            arduino.open()
            arduino.flush()
            arduino.write("readRFID\n".encode())
            time.sleep(0.1)
            arduino.flush()
            while time.time() < start + 3:
                if arduino.in_waiting > 0:
                    data = arduino.readline().decode('utf-8').rstrip()
                    print('data = ' + str(data))
                    if data == 'Reader DC AC 02 5C':
                        args[1].lift()
                        userID[0] = 'jborum'
                        # return userID[0]
                    elif data == 'Reader 1A3AF084':
                        args[1].lift()
                        userID[0] = 'bcarrier'
                        # return userID[0]
            if time.time() > start + 4:
                scanError = tk.Label(self, text="This login attempt failed",
                                     font=tkFont.Font(family='Bell Gothic Std Light', size=14))
                scanError.place(relx=495 / 1024, rely=230 / 600)
            if userID[0] != '':
                userIDLabel = "Welcome, " + userID[0] + '!'
                welcomeLabel = tk.Label(args[1], text=userIDLabel, font=welcomeFont, bg='gray24', fg='gray99').pack(
                    side="top")
            filename = userID[0] + 'Favorites.txt'
            try:
                open(filename)
            except IOError:
                f = open(filename, "w")
                f.write(userID[0])
                f.close()
            finally:
                userData = open(filename, "a+")
                userData.close()

            filename1 = userID[0] + 'Recents.txt'
            try:
                open(filename1)
            except IOError:
                f = open(filename1, "w")
                f.write(userID[0])
                f.close()
            finally:
                userData = open(filename1, "a+")
                userData.close()

        RFlogin = tk.Button(self, text='Scan Card', font=fatFingerFont, bg='gray35', fg='gray99',
                            command=lambda: RFloginpoll())
        RFlogin.pack(side='bottom')

        chosenPin = tk.StringVar()

        def pinVerify():
            # need check on serial for RFID card scan and automatically lift page1
            chosenPin = pinLogin.get()
            user1Pin = ""
            user2Pin = "jack"
            user3Pin = "bcarrier"
            if chosenPin == user1Pin:
                args[1].lift()
                userID[0] = 'User'
                print(userID[0])
            elif chosenPin == user2Pin:
                args[1].lift()
                userID[0] = 'jborum'
                print(userID[0])
            elif chosenPin == user3Pin:
                args[1].lift()
                userID[0] = 'bcarrier'
                print(userID[0])
            else:
                pinError = tk.Label(self, text="This login attempt failed",
                                    font=tkFont.Font(family='Bell Gothic Std Light', size=14))
                pinError.place(relx=495 / 1024, rely=230 / 600)
            if userID[0] != '':
                userIDLabel = "Welcome, " + userID[0] + '!'
                welcomeLabel = tk.Label(args[1], text=userIDLabel, font=welcomeFont, bg='gray24', fg='gray99').pack(
                    side="top")
            filename = userID[0] + 'Favorites.txt'
            try:
                open(filename)
            except IOError:
                f = open(filename, "w")
                f.write(userID[0])
                f.close()
            finally:
                userData = open(filename, "a+")
                userData.close()

            filename1 = userID[0] + 'Recents.txt'
            try:
                open(filename1)
            except IOError:
                f = open(filename1, "w")
                f.write(userID[0])
                f.close()
            finally:
                userData = open(filename1, "a+")
                userData.close()

        login = tk.Button(self, text="Login", command=pinVerify, font=fatFingerFont, fg='gray99', bg='royal blue')
        login.place(height=175, width=325, relx=0.5, rely=0.75, anchor='s')


class Page1(Page):  # main menu
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs, bg='gray24')
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)
        welcomeFont = tkFont.Font(family='Bell Gothic Std Light', size=42, weight='bold')

        self.logoIMG = ImageTk.PhotoImage(Image.open('botTender_logo.png').resize((225, 225), Image.ANTIALIAS))
        self.botTenderLogo = tk.Label(self, image=self.logoIMG, bg='gray24').place(relx=412 / 1024, rely=100 / 600)


class Page2(Page):  # Custom/Shots
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=18)
        fatFingerFont2 = tkFont.Font(family='Bell Gothic Std Light', size=15)

        userFile = 'userRecents' + '.txt'
        userData = open(userFile, 'a+')

        label = tk.Label(self, text="Shots/Custom Pour Menu", font=headerFont, bg='gray24', fg='gray99')
        label.place(relx=0.33, y=0)
        backtoMenu = tk.Button(self, text="← Back to Main Menu", font=fatFingerFont2, bg='gray35', fg='gray99',
                               command=args[1].lift)
        backtoMenu.place(x=0, y=0, height=60, width=225)

        global customCount
        customCount = [0] * 6

        def addShot(shotCounterLabel):
            index = int(shotCounterLabel["wraplength"]) - 10
            currentShotCount = int(shotCounterLabel["text"])
            if currentShotCount < 4:
                currentShotCount = currentShotCount + 1
            shotCounterLabel["text"] = currentShotCount
            customCount[index] = currentShotCount

        def lessShot(shotCounterLabel):
            index = int(shotCounterLabel["wraplength"]) - 10
            currentShotCount = int(shotCounterLabel["text"])
            if currentShotCount > 0:
                currentShotCount = currentShotCount - 1
            shotCounterLabel["text"] = currentShotCount
            customCount[index] = currentShotCount

        def resetCount(shotCounterLabel):
            print("reset")

        resetCounterButton = tk.Button(self, text="Reset Count")

        shotOption1 = tk.Label(self, text="Vodka", font=fatFingerFont, bg='gray24', fg='gray99').place(relx=175 / 1024,
                                                                                                       rely=0.20)
        shotCounter1 = tk.Label(self, text="0", font=fatFingerFont, bg='gray24', fg='gray99', wraplength=10)
        shotCounter1.place(height=50, width=50, relx=175 / 1024, rely=0.26)
        ounceLabel = tk.Label(self, text="(oz)", font=fatFingerFont, bg='gray24', fg='gray99').place(height=50,
                                                                                                     width=50, x=215,
                                                                                                     rely=0.26)
        optAdd1 = tk.Button(self, text="+", font=fatFingerFont2, bg='gray35', fg='gray99',
                            command=lambda: addShot(shotCounter1)).place(height=40, width=40, relx=350 / 1024,
                                                                         rely=0.26)
        optSub1 = tk.Button(self, text="-", font=fatFingerFont2, bg='gray35', fg='gray99',
                            command=lambda: lessShot(shotCounter1)).place(height=40, width=40, relx=400 / 1024,
                                                                          rely=0.26)

        shotOption2 = tk.Label(self, text="Rum", font=fatFingerFont, bg='gray24', fg='gray99').place(relx=175 / 1024,
                                                                                                     rely=0.45)
        shotCounter2 = tk.Label(self, text=0, font=fatFingerFont, bg='gray24', fg='gray99', wraplength=11)
        shotCounter2.place(height=50, width=50, relx=175 / 1024, rely=0.51)
        ounceLabel2 = tk.Label(self, text="(oz)", font=fatFingerFont, bg='gray24', fg='gray99').place(height=50,
                                                                                                      width=50,
                                                                                                      relx=215 / 1024,
                                                                                                      rely=0.51)
        optAdd2 = tk.Button(self, text="+", font=fatFingerFont2, bg='gray35', fg='gray99',
                            command=lambda: addShot(shotCounter2)).place(height=40, width=40, relx=350 / 1024,
                                                                         rely=0.51)
        optSub2 = tk.Button(self, text="-", bg='gray35', fg='gray99', command=lambda: lessShot(shotCounter2)).place(
            height=40, width=40, relx=400 / 1024, rely=0.51)

        shotOption3 = tk.Label(self, text="Triple Sec", font=fatFingerFont, bg='gray24', fg='gray99').place(
            relx=175 / 1024, rely=0.7)
        shotCounter3 = tk.Label(self, text=0, font=fatFingerFont, bg='gray24', fg='gray99', wraplength=12)
        shotCounter3.place(height=50, width=50, relx=175 / 1024, rely=0.76)
        ounceLabel3 = tk.Label(self, text="(oz)", font=fatFingerFont, bg='gray24', fg='gray99').place(height=50,
                                                                                                      width=50,
                                                                                                      relx=215 / 1024,
                                                                                                      rely=0.76)
        optAdd3 = tk.Button(self, text="+", font=fatFingerFont2, bg='gray35', fg='gray99',
                            command=lambda: addShot(shotCounter3)).place(height=40, width=40, relx=350 / 1024,
                                                                         rely=0.76)
        optSub3 = tk.Button(self, text="-", font=fatFingerFont2, bg='gray35', fg='gray99',
                            command=lambda: lessShot(shotCounter3)).place(height=40, width=40, relx=400 / 1024,
                                                                          rely=0.76)

        shotOption4 = tk.Label(self, text="Coke", font=fatFingerFont, bg='gray24', fg='gray99').place(relx=575 / 1024,
                                                                                                      rely=0.20)
        shotCounter4 = tk.Label(self, text=0, font=fatFingerFont, bg='gray24', fg='gray99', wraplength=13)
        shotCounter4.place(height=50, width=50, relx=575 / 1024, rely=0.26)
        ounceLabel4 = tk.Label(self, text="(oz)", font=fatFingerFont, bg='gray24', fg='gray99').place(height=50,
                                                                                                      width=50,
                                                                                                      relx=615 / 1024,
                                                                                                      rely=0.26)
        optAdd4 = tk.Button(self, text="+", font=fatFingerFont2, bg='gray35', fg='gray99',
                            command=lambda: addShot(shotCounter4)).place(height=40, width=40, relx=750 / 1024,
                                                                         rely=0.26)
        optSub4 = tk.Button(self, text="-", font=fatFingerFont2, bg='gray35', fg='gray99',
                            command=lambda: lessShot(shotCounter4)).place(height=40, width=40, relx=800 / 1024,
                                                                          rely=0.26)

        shotOption5 = tk.Label(self, text="Cranberry Juice", font=fatFingerFont, bg='gray24', fg='gray99').place(
            relx=575 / 1024, rely=0.45)
        shotCounter5 = tk.Label(self, text=0, font=fatFingerFont, bg='gray24', fg='gray99', wraplength=14)
        shotCounter5.place(height=50, width=50, relx=575 / 1024, rely=0.51)
        ounceLabel = tk.Label(self, text="(oz)", font=fatFingerFont, bg='gray24', fg='gray99').place(height=50,
                                                                                                     width=50,
                                                                                                     relx=615 / 1024,
                                                                                                     rely=0.51)
        optAdd5 = tk.Button(self, text="+", font=fatFingerFont2, bg='gray35', fg='gray99',
                            command=lambda: addShot(shotCounter5)).place(height=40, width=40, relx=750 / 1024,
                                                                         rely=0.51)
        optSub5 = tk.Button(self, text="-", font=fatFingerFont2, bg='gray35', fg='gray99',
                            command=lambda: lessShot(shotCounter5)).place(height=40, width=40, relx=800 / 1024,
                                                                          rely=0.51)

        shotOption6 = tk.Label(self, text="Lime Juice", font=fatFingerFont, bg='gray24', fg='gray99').place(
            relx=575 / 1024, rely=0.7)
        shotCounter6 = tk.Label(self, text=0, font=fatFingerFont, bg='gray24', fg='gray99', wraplength=15)
        shotCounter6.place(height=50, width=50, relx=575 / 1024, rely=0.76)
        ounceLabel = tk.Label(self, text="(oz)", font=fatFingerFont, bg='gray24', fg='gray99').place(height=50,
                                                                                                     width=50,
                                                                                                     relx=615 / 1024,
                                                                                                     rely=0.76)
        optAdd6 = tk.Button(self, text="+", font=fatFingerFont2, bg='gray35', fg='gray99',
                            command=lambda: addShot(shotCounter6)).place(height=40, width=40, relx=750 / 1024,
                                                                         rely=0.76)
        optSub6 = tk.Button(self, text="-", font=fatFingerFont2, bg='gray35', fg='gray99',
                            command=lambda: lessShot(shotCounter6)).place(height=40, width=40, relx=800 / 1024,
                                                                          rely=0.76)

        global customPourFunc

        def customPourFunc(event):
            # gui stuff
            global customIngredients
            currentOrder = ["", "", "", "", "", ""]
            customAmount = 0
            newline = "\n"
            for i in range(6):
                currentOrder[i] = str(customCount[i] * 100)
                currentOrder[i] = currentOrder[i] + newline
                print("Current Order:")
                print(currentOrder[i])

            arduino.flush()
            arduino.write("custom\n".encode())
            arduino.flush()
            data = arduino.readline().decode('utf-8').rstrip()
            print(data)
            while data != 'Vodka':
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)

            if data == 'Vodka':
                arduino.write(currentOrder[0].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                # time.sleep(0.05)
            if data == 'WhiteRum':
                arduino.write(currentOrder[1].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'TripleSec':
                arduino.write(currentOrder[2].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'Coke':
                arduino.write(currentOrder[3].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'CranberryJuice':
                arduino.write(currentOrder[4].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'LimeJuice':
                arduino.write(currentOrder[5].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            while data != 'Done':
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)

            userData.write(str(currentOrder))
            userData.close
            inventory = open('botInventory.txt', "r")
            totalStatus = inventory.readlines()
            inventory.close()
            inventory = open('botInventory.txt', "w")
            for i in range(6):
                index = (i + 1) * 3
                totalStatus[index] = str(int(round(float(totalStatus[index]) - (customCount[i] / 18) * 100))) + "\n"
            inventory.writelines(totalStatus)
            inventory.close()

            # controls stuff


class Page3(Page):  # Mixed drink menu
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        mainHeaderFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=20)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)

        userFile = 'userRecents' + '.txt'
        userData = open(userFile, 'a+')

        backtoMenu = tk.Button(self, text="← Back to Main Menu", font=fatFingerFont, bg='gray35', fg='gray99',
                               command=args[1].lift)
        backtoMenu.place(relx=0, rely=0, height=60, width=225)

        label = tk.Label(self, text="Mixed Drink Menu", font=mainHeaderFont, bg='gray24', fg='gray99')
        label.place(relx=400 / 1024, rely=0)

        def searchSort():
            searchEntry = searchInput.get()
            if searchEntry != "":
                for i in reversed(range(15)):
                    if searchEntry != recipeList.get(i):
                        recipeList.delete(i)
            elif searchEntry == "":
                for i in range(6):
                    recipeList.delete(i)
                    recipeList.insert(i, (recipeArray[0][i]))

        def pinKeyboard(event):
            alreadyOpen = False
            if alreadyOpen == False:
                pop = subprocess.Popen("osk", stdout=subprocess.PIPE, shell=True)
                alreadyOpen = True

        recipeSearch = tk.Label(self, text='Search:', font=headerFont, bg='gray24', fg='gray99')
        recipeSearch.place(relx=360 / 1024, rely=60 / 600)
        searchInput = tk.Entry(self, bd=5, font=fatFingerFont)
        searchInput.place(relx=465 / 1024, rely=65 / 600, height=30, width=150)
        searchInput.bind("<Button-1>", pinKeyboard)
        searchButton = tk.Button(self, text="►", font=fatFingerFont, command=searchSort)
        searchButton.place(height=30, width=30, relx=625 / 1024, rely=65 / 600)
        self.after(10000, searchSort)

        recipeScroll = tk.Scrollbar(self)
        recipeScroll.place(height=383, width=25, relx=550 / 1024, rely=115 / 600)
        recipeList = tk.Listbox(self, yscrollcommand=recipeScroll.set, font=headerFont)
        for i in range(6):
            recipeList.insert(i, (recipeArray[0][i]))
        recipeList.place(height=383, width=250, relx=300 / 1024, rely=115 / 600)
        recipeScroll.config(command=recipeList.yview)

        ingredientsDet = ["", "", "", "", "", "", ""]

        def onSelect(evt):
            w = evt.widget
            global index1
            index1 = int(w.curselection()[0])
            global drinkName
            drinkName = w.get(index1)
            for i in range(6):
                if drinkName == recipeArray[0][i]:
                    drinkDesc.delete('1.0', tk.END)
                    drinkDesc.insert(tk.END, drinkName + "\n\nIngredients:\n")
                    ingredientCalc = list(recipeArray[1][i])
                    for j in range(7):
                        if int(ingredientCalc[j]) == 1:
                            ingredientsDet[j] = ingredientsArray[0][j]
                            drinkDesc.insert(tk.END, str(ingredientsDet[j]) + "\n")

        drinkDesc = tk.Text(self, height=13.4, font=headerFont)
        drinkDesc.place(relx=600 / 1024, rely=115 / 600, height=383)
        recipeList.bind('<<ListboxSelect>>', onSelect)

        checkSortSum = 000000
        CheckVar1 = tk.IntVar()
        CheckVar2 = tk.IntVar()
        CheckVar3 = tk.IntVar()
        CheckVar4 = tk.IntVar()
        CheckVar5 = tk.IntVar()
        CheckVar6 = tk.IntVar()
        checkVarsList = [CheckVar1, CheckVar2, CheckVar3, CheckVar4, CheckVar5, CheckVar6]

        def checkSort():
            for k in range(6):
                recipeList.delete(k)
                recipeList.insert(k, (recipeArray[0][k]))
            for i in range(6):
                if checkVarsList[i].get() == 1:
                    for j in reversed(range(6)):
                        if list(ingredientsArray[1][i])[i] != list(recipeArray[1][j])[i]:
                            recipeList.delete(j)

        C1 = tk.Checkbutton(self, text=ingredientsArray[0][0], variable=CheckVar1, onvalue=1, offvalue=0, height=1,
                            width=20, font=fatFingerFont, bg='gray35', fg='LightBlue3', command=lambda: checkSort())
        C2 = tk.Checkbutton(self, text=ingredientsArray[0][1], variable=CheckVar2, onvalue=1, offvalue=0, height=1,
                            width=20, font=fatFingerFont, bg='gray35', fg='LightBlue3', command=lambda: checkSort())
        C3 = tk.Checkbutton(self, text=ingredientsArray[0][2], variable=CheckVar3, onvalue=1, offvalue=0, height=1,
                            width=20, font=fatFingerFont, bg='gray35', fg='LightBlue3', command=lambda: checkSort())
        C4 = tk.Checkbutton(self, text=ingredientsArray[0][3], variable=CheckVar4, onvalue=1, offvalue=0, height=1,
                            width=20, font=fatFingerFont, bg='gray35', fg='LightBlue3', command=lambda: checkSort())
        C5 = tk.Checkbutton(self, text=ingredientsArray[0][4], variable=CheckVar5, onvalue=1, offvalue=0, height=1,
                            width=20, font=fatFingerFont, bg='gray35', fg='LightBlue3', command=lambda: checkSort())
        C6 = tk.Checkbutton(self, text=ingredientsArray[0][5], variable=CheckVar6, onvalue=1, offvalue=0, height=1,
                            width=20, font=fatFingerFont, bg='gray35', fg='LightBlue3', command=lambda: checkSort())

        recipeSort = tk.Label(self, text='Sort by Ingredient:', font=headerFont, bg='gray24', fg='gray99')
        sortHeight = 15
        recipeSort.place(relx=25 / 1024, rely=(sortHeight + 45) / 600)

        C1.place(width=265, height=40, relx=0, rely=(sortHeight + 105) / 600)
        C2.place(width=265, height=40, relx=0, rely=(sortHeight + 180) / 600)
        C3.place(width=265, height=40, relx=0, rely=(sortHeight + 255) / 600)
        C4.place(width=265, height=40, relx=0, rely=(sortHeight + 330) / 600)
        C5.place(width=265, height=40, relx=0, rely=(sortHeight + 405) / 600)
        C6.place(width=265, height=40, relx=0, rely=(sortHeight + 480) / 600)

        global pourFunc

        def pourFunc(event):
            # python side
            global drinkIngredients
            drinkIngredients = ''
            for i in range(6):
                if drinkName == recipeArray[0][i]:
                    drinkIngredients = recipeArray[1][i]
            currentOrder = '\n' + str(drinkName) + ',' + str(drinkIngredients)
            userData.write(currentOrder)
            userData.close()
            print('Drink ingredients:' + str(drinkIngredients))

            # arduino1 side
            arduino.flush()
            arduino.write("selected\n".encode())
            arduino.flush()
            time.sleep(0.05)
            data = arduino.readline().decode('utf-8').rstrip()
            print(data)
            while data != 'Vodka':
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                arduino.write("selected\n".encode())

            if data == 'Vodka':
                arduino.write(recipeArray[2][index1].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'WhiteRum':
                arduino.write(recipeArray[3][index1].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'TripleSec':
                arduino.write(recipeArray[4][index1].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'Coke':
                arduino.write(recipeArray[5][index1].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'CranberryJuice':
                arduino.write(recipeArray[6][index1].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'LimeJuice':
                arduino.write(recipeArray[7][index1].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)

            while data != 'Done':
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)

            if data == 'Done':
                arduino.close()
                arduino.open()


class Page4(Page):  # Settings
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        mainHeaderFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=15)
        backtoMenu = tk.Button(self, text="← Back to Main Menu", font=fatFingerFont, bg='gray35', fg='gray99',
                               command=args[1].lift)
        backtoMenu.place(x=0, y=0, height=60, width=225)
        label = tk.Label(self, text="Settings", font=headerFont, bg='gray24', fg='gray99')
        label.pack(side="top", anchor="n")

        # fillStatus = tk.Frame(self, bg='WHITE')
        # fillStatus.place(relx=0.25, rely=0.25, height = 300 , width = 512)
        fillStatus = tk.Label(self, text="Bottle Fill Status", font=headerFont, bg='gray24', fg='gray99').place(x=325,
                                                                                                                rely=0.2,
                                                                                                                width=374)
        self.emptyBottleIMG = ImageTk.PhotoImage(Image.open('bottle_empty.png'))
        self.lowBottleIMG = ImageTk.PhotoImage(Image.open('bottle_low.png'))
        self.halfBottleIMG = ImageTk.PhotoImage(Image.open('bottle_half.png'))
        self.highBottleIMG = ImageTk.PhotoImage(Image.open('bottle_high.png'))
        self.fullBottleIMG = ImageTk.PhotoImage(Image.open('bottle_full.png'))
        bottlePlacerX = 158

        global settingsUpdate

        def settingsUpdate(event):
            inventory = open('botInventory.txt', "r")
            totalStatus = inventory.readlines()
            self.fillStatusImages = [self.emptyBottleIMG, self.lowBottleIMG, self.halfBottleIMG, self.highBottleIMG,
                                     self.fullBottleIMG]
            self.fillImagePlacer = [None] * 6
            for i in range(6):
                if float(totalStatus[(i + 1) * 3]) >= 80:
                    self.fillImagePlacer[i] = self.fillStatusImages[4]
                elif float(totalStatus[(i + 1) * 3]) < 80 and float(totalStatus[(i + 1) * 3]) >= 60:
                    self.fillImagePlacer[i] = self.fillStatusImages[3]
                elif float(totalStatus[(i + 1) * 3]) < 60 and float(totalStatus[(i + 1) * 3]) >= 40:
                    self.fillImagePlacer[i] = self.fillStatusImages[2]
                elif float(totalStatus[(i + 1) * 3]) < 40 and float(totalStatus[(i + 1) * 3]) >= 20:
                    self.fillImagePlacer[i] = self.fillStatusImages[1]
                elif float(totalStatus[(i + 1) * 3]) < 20:
                    self.fillImagePlacer[i] = self.fillStatusImages[0]
            inventory.close()

            #GPIO.output(27, GPIO.LOW)
            #time.sleep(0.1)
            #GPIO.output(27, GPIO.HIGH)
            #time.sleep(0.1)
            #start = time.time()
            #data = ''
            arduino.flush()
            arduino.write("readRFID\n".encode())
            time.sleep(0.1)
            arduino.flush()

            inventory = open('botInventory.txt', "w")
            str1 = ''
            str1.join(totalStatus)
            print(str1)
            inventory.write(str1.join(totalStatus))
            inventory.close()

            self.bottle1Fill = tk.Label(self, image=self.fillImagePlacer[0], bg='gray24').place(x=bottlePlacerX,
                                                                                                rely=0.3)
            self.bottle2Fill = tk.Label(self, image=self.fillImagePlacer[1], bg='gray24').place(x=bottlePlacerX + 118,
                                                                                                rely=0.3)
            self.bottle3Fill = tk.Label(self, image=self.fillImagePlacer[2], bg='gray24').place(
                x=bottlePlacerX + (118 * 2), rely=0.3)
            self.bottle4Fill = tk.Label(self, image=self.fillImagePlacer[3], bg='gray24').place(
                x=bottlePlacerX + (118 * 3), rely=0.3)
            self.bottle5Fill = tk.Label(self, image=self.fillImagePlacer[4], bg='gray24').place(
                x=bottlePlacerX + (118 * 4), rely=0.3)
            self.bottle6Fill = tk.Label(self, image=self.fillImagePlacer[5], bg='gray24').place(
                x=bottlePlacerX + (118 * 5), rely=0.3)
            bottle1desc = tk.Label(self, text="Content:\n" + totalStatus[1] + "\nFill Status: " + totalStatus[3] + "%",
                                   bg='gray24', fg='gray99').place(x=bottlePlacerX + 25, rely=0.65)
            bottle2desc = tk.Label(self, text="Content:\n" + totalStatus[4] + "\nFill Status: " + totalStatus[6] + "%",
                                   bg='gray24', fg='gray99').place(x=bottlePlacerX + 25 + 118, rely=0.65)
            bottle3desc = tk.Label(self, text="Content:\n" + totalStatus[7] + "\nFill Status: " + totalStatus[9] + "%",
                                   bg='gray24', fg='gray99').place(x=bottlePlacerX + 25 + (118 * 2), rely=0.65)
            bottle4desc = tk.Label(self,
                                   text="Content:\n" + totalStatus[10] + "\nFill Status: " + totalStatus[12] + "%",
                                   bg='gray24', fg='gray99').place(x=bottlePlacerX + 25 + (118 * 3), rely=0.65)
            bottle5desc = tk.Label(self,
                                   text="Content:\n" + totalStatus[13] + "\nFill Status: " + totalStatus[15] + "%",
                                   bg='gray24', fg='gray99').place(x=bottlePlacerX + 25 + (118 * 4), rely=0.65)
            bottle6desc = tk.Label(self,
                                   text="Content:\n" + totalStatus[16] + "\nFill Status: " + totalStatus[18] + "%",
                                   bg='gray24', fg='gray99').place(x=bottlePlacerX + 25 + (118 * 5), rely=0.65)

        refresh = tk.Button(self, text="Refresh", font=fatFingerFont, bg='gray35', fg='gray99')
        refresh.bind("<ButtonRelease>", settingsUpdate)
        refresh.pack(anchor="ne")


class Page5(Page):  # priming menu
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=15)
        backSettings = tk.Button(self, text="← Back to Settings", font=fatFingerFont, bg='gray35', fg='gray99',
                                 command=args[1].lift).place(x=0, y=0, height=60, width=225)

        primemenuheader1 = tk.Label(self, text="What is Pump Priming?", font=headerFont, bg='gray24',
                                    fg='gray99').place(relx=(512 - 200) / 1024, rely=0.025, width=400)
        primemenuheader2 = tk.Label(self, text="Priming Instructions:", font=headerFont, bg='gray24',
                                    fg='gray99').place(relx=(512 - 175) / 1024, rely=0.475, width=350)

        primeInstructText1 = "Our pumps use the principle of a vaccuum to move your ingredients without contamination.\n\n" \
                             "The process of priming clears any remaining liquid from the pump lines and preps them\n\nwith your new ingredient selection. " \
                             "This process should be repeated every time a bottle\n\nis replaced to ensure we can deliver your favorite drinks " \
                             "with optimal speed and quality!"

        primeInstructText2 = "Before priming the pumps, please place a container below the BotTender nozzle to\n\ncatch excess liquid. " \
                             "With the new bottle installed press 'PRIME and select the bottle\n\nlocation. An LED indicator will light up " \
                             "to confirm your selection. This process will\n\ntake approximately xx seconds and the LED indicator will turn off when it is done."

        primeInstruct = tk.Label(self, text=primeInstructText1, font=fatFingerFont, bg='gray24', fg='gray99',
                                 justify=tk.LEFT).place(relx=0.075, rely=0.15)
        primeInstruct2 = tk.Label(self, text=primeInstructText2, font=fatFingerFont, bg='gray24', fg='gray99',
                                  justify=tk.LEFT).place(relx=0.075, rely=0.6)


class Page6(Page):  # pour page
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=20)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)

        backtoMenu = tk.Button(self, text="← Back to Main Menu", bg='gray35', fg='gray99', font=fatFingerFont,
                               command=args[1].lift).place(x=0, y=0, height=60, width=225)

        def Fav():
            filename = userID[0] + 'Recents.txt'
            getValue = open(filename, 'r')
            info = getValue.readlines()
            index = len(info) - 1
            currentVal = info[index]
            filename.close()
            filename = userID[0] + 'Favorites.txt'
            saveFaves = open(filename, 'a')
            saveFaves.write(currentVal)
            saveFaves.close()

        label1 = tk.Label(self, text="Your chosen drink:", font=headerFont, bg='gray24', fg='gray99').place(x=325,
                                                                                                            rely=0.05,
                                                                                                            width=374)
        label1 = tk.Label(self, text="Custom Drink", font=headerFont, bg='gray24',fg='gray99').place(relx=0.41, rely=0.15)

        label2 = tk.Label(self, text="Would you like to add this to favorites?", font=headerFont, bg='gray24',
                          fg='gray99').place(x=312, rely=0.35)
        b1 = tk.Button(self, text="Yes", font=fatFingerFont, bg='gray35', fg='gray99', command=lambda: Fav()).place(
            x=362, rely=0.45, height=60, width=100)
        b2 = tk.Button(self, text="No", font=fatFingerFont, bg='gray35', fg='gray99').place(x=562, rely=0.45, height=60,
                                                                                            width=100)

        label3 = tk.Label(self, text="Confirm action:", font=headerFont, bg='gray24', fg='gray99').place(x=312,
                                                                                                         rely=0.65,
                                                                                                         width=400)

        b4 = tk.Button(self, text="No", font=fatFingerFont, bg='gray35', fg='gray99', command=args[1].lift)
        b4.place(x=562, rely=0.75, height=60, width=100)


class Page7(Page):  # UserProfile Menu
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        bigheaderFont = tkFont.Font(family='Bell Gothic Std Light', size=34)
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=18)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)

        userFileRecents = 'userRecents' + '.txt'
        userDataRecents = open(userFileRecents, 'r+')
        userFileFavorites = 'userFavorites' + '.txt'
        userDataFavorites = open(userFileFavorites, 'r+')

        backtoMenu = tk.Button(self, text="← Back to Main Menu", font=fatFingerFont, bg='gray35', fg='gray99',
                               command=args[1].lift).place(x=0, y=0, height=60, width=225)
        upTitleLabel = tk.Label(self, text="User Profile", font=bigheaderFont, bg='gray24', fg='gray99').place(relx=.45,
                                                                                                               rely=0)
        favLabel = tk.Label(self, text="Your\nFavorites", font=headerFont, bg='gray24', fg='gray99').place(
            relx=40 / 1024, rely=0.225)

        favoriteScroll = tk.Scrollbar(self)
        favoriteScroll.place(height=200, width=30, x=390, rely=100 / 600)
        favoriteList = tk.Listbox(self, yscrollcommand=favoriteScroll.set, font=headerFont)
        favoriteList.place(height=200, width=215, x=175, rely=100 / 600)
        favoriteDrinkDesc = tk.Text(self, font=headerFont)
        favoriteDrinkDesc.place(height=200, width=235, x=435, rely=100 / 600)

        favContent = userDataFavorites.readlines()[1:]
        favCount = len(favContent)
        print('content: ')
        print(favContent)
        favLIFOcontent = favContent[favCount::-1]
        for i in range(favCount):
            wholeLine1 = list(favLIFOcontent[i])
            nameOnly = ''
            for j in range(len(wholeLine1)):
                if wholeLine1[j] != ',':
                    nameOnly += wholeLine1[j]
                else:
                    break
            favoriteList.insert(i, nameOnly)

        favoriteScroll.config(command=favoriteList.yview)

        ingredientsDet = ["", "", "", "", "", "", ""]

        def onSelect(evt):
            w = evt.widget
            index2 = int(w.curselection()[0])
            drinkName = w.get(index2)
            for i in range(6):
                if drinkName == recipeArray[0][i]:
                    favoriteDrinkDesc.delete('1.0', tk.END)
                    favoriteDrinkDesc.insert(tk.END, drinkName + "\n\nIngredients:\n")
                    ingredientCalc = list(recipeArray[1][i])
                    for j in range(7):
                        if int(ingredientCalc[j]) == 1:
                            ingredientsDet[j] = ingredientsArray[0][j]
                            favoriteDrinkDesc.insert(tk.END, str(ingredientsDet[j]) + "\n")
                elif drinkName == 'Custom Beverage':
                    favoriteDrinkDesc.delete('1.0', tk.END)
                    favoriteDrinkDesc.insert(tk.END, drinkName + "\n\nIngredients:\n")
                    temp = list(LIFOcontent[index2])
                    # print(temp)
                    if len(temp) == 24:
                        temp.remove('\n')
                    customNumStr = temp[len(temp):len(temp) - 8:-1]
                    # print(customNumStr)
                    for j in range(7):
                        if int(customNumStr[j]) == 1:
                            ingredientsDet[j] = ingredientsArray[0][j]
                            favoriteDrinkDesc.insert(tk.END, str(ingredientsDet[j]) + "\n")

        favoriteList.bind('<<ListboxSelect>>', onSelect)
        #####################################################################################################################
        recentLabel = tk.Label(self, text="Your\nRecents", font=headerFont, bg='gray24', fg='gray99').place(
            relx=40 / 1024, rely=400 / 600)

        recentScroll = tk.Scrollbar(self)
        recentScroll.place(height=200, width=30, x=390, y=365)
        recentList = tk.Listbox(self, yscrollcommand=recentScroll.set, font=headerFont)
        recentList.place(height=200, width=215, x=175, y=365)
        recentDrinkDesc = tk.Text(self, font=headerFont)
        recentDrinkDesc.place(height=200, width=235, x=435, y=365)

        content = userDataRecents.readlines()[1:]
        count = len(content)
        print('content: ')
        print(content)
        LIFOcontent = content[count::-1]
        for i in range(count):
            wholeLine = list(LIFOcontent[i])
            nameOnly = ''
            for j in range(len(wholeLine)):
                if wholeLine[j] != ',':
                    nameOnly += wholeLine[j]
                else:
                    break
            recentList.insert(i, nameOnly)

        recentScroll.config(command=recentList.yview)

        ingredientsDet = ["", "", "", "", "", "", ""]

        def onSelect(evt):
            w = evt.widget
            index2 = int(w.curselection()[0])
            drinkName = w.get(index2)
            for i in range(6):
                if drinkName == recipeArray[0][i]:
                    recentDrinkDesc.delete('1.0', tk.END)
                    recentDrinkDesc.insert(tk.END, drinkName + "\n\nIngredients:\n")
                    ingredientCalc = list(recipeArray[1][i])
                    for j in range(7):
                        if int(ingredientCalc[j]) == 1:
                            ingredientsDet[j] = ingredientsArray[0][j]
                            recentDrinkDesc.insert(tk.END, str(ingredientsDet[j]) + "\n")
                elif drinkName == 'Custom Beverage':
                    recentDrinkDesc.delete('1.0', tk.END)
                    recentDrinkDesc.insert(tk.END, drinkName + "\n\nIngredients:\n")
                    temp = list(LIFOcontent[index2])
                    # print(temp)
                    if len(temp) == 24:
                        temp.remove('\n')
                    customNumStr = temp[len(temp):len(temp) - 8:-1]
                    # print(customNumStr)
                    for j in range(7):
                        if int(customNumStr[j]) == 1:
                            ingredientsDet[j] = ingredientsArray[0][j]
                            recentDrinkDesc.insert(tk.END, str(ingredientsDet[j]) + "\n")

        recentList.bind('<<ListboxSelect>>', onSelect)

        userDataFavorites.close()
        userDataRecents.close()

class Page8(Page):  # pour page 2
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs, bg='gray24')
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=20)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)

        backtoMenu = tk.Button(self, text="← Back to Main Menu", bg='gray35', fg='gray99', font=fatFingerFont,
                               command=args[1].lift).place(x=0, y=0, height=60, width=225)

        def Fav():
            filename = userID[0] + 'Recents.txt'
            getValue = open(filename, 'r')
            info = getValue.readlines()
            index = len(info) - 1
            currentVal = info[index]
            filename.close()
            filename = userID[0] + 'Favorites.txt'
            saveFaves = open(filename, 'a')
            saveFaves.write(currentVal)
            saveFaves.close()

        label1 = tk.Label(self, text="Your chosen drink:", font=headerFont, bg='gray24', fg='gray99').place(x=325,
                                                                                                            rely=0.05,
                                                                                                            width=374)
        label1 = tk.Label(self, text="Kamikaze", font=headerFont, bg='gray24',fg='gray99').place(relx=0.425, rely=0.15)

        label2 = tk.Label(self, text="Would you like to add this to favorites?", font=headerFont, bg='gray24',
                          fg='gray99').place(x=312, rely=0.35)
        b1 = tk.Button(self, text="Yes", font=fatFingerFont, bg='gray35', fg='gray99', command=lambda: Fav()).place(
            x=362, rely=0.45, height=60, width=100)
        b2 = tk.Button(self, text="No", font=fatFingerFont, bg='gray35', fg='gray99').place(x=562, rely=0.45, height=60,
                                                                                            width=100)

        label3 = tk.Label(self, text="Confirm action:", font=headerFont, bg='gray24', fg='gray99').place(x=312,
                                                                                                         rely=0.65,
                                                                                                         width=400)
        b4 = tk.Button(self, text="No", font=fatFingerFont, bg='gray35', fg='gray99', command=args[1].lift).place(x=562,
                                                                                                                  rely=0.75,
                                                                                                                  height=60,
                                                                                                                  width=100)



class Page10(Page):  # help menu
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs, bg='gray24')
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)
        welcomeFont = tkFont.Font(family='Bell Gothic Std Light', size=42, weight='bold')

        backtoMenu = tk.Button(self, text="← Back to Main Menu", font=fatFingerFont, bg='gray35', fg='gray99',
                               command=args[1].lift).place(x=0, y=0, height=70, width=240)

        instructionList = "Welcome to BotTender!\n\nTo get started with your drink, click one of the " + \
                          "buttons below:\nThe Shots button will allow you " + \
                          "to dispense individual shots\nThe Mixed Drinks " + \
                          "button will allow you to choose from one of our " + \
                          "pre-set recipes\nbased on the options you have " + \
                          "loaded your BotTender with.\nThere are options to " + \
                          "sort by ingredient or search for your favorite recipe\n" + \
                          "The settings menu will show you the fill status of " + \
                          'your containers and\nallow you to prime the pumps ' + \
                          "when replacing your containers."

        helpInstructions = tk.Label(self, text=instructionList, font=headerFont, bg='gray24', fg='gray99')
        helpInstructions.place(relx=0.075, rely=0.25)


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):

        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self, p1)
        p3 = Page3(self, p1)
        p4 = Page4(self, p1)
        p5 = Page5(self, p4)
        p6 = Page6(self, p1)
        p7 = Page7(self, p1)
        p8 = Page8(self, p1)
#        p9 = Page9(self, p1) #commented out for simplicty
        p10 = Page10(self, p1)
        p0 = Page0(self, p1)

        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=18)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p0.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p7.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p8.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
#        p9.place(in_=container, x=0, y=0, relwidth=1, relheight=1) #commented out for simplicty of the system
        p10.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        self.cocktailsMenu = ImageTk.PhotoImage(Image.open('Cocktailmenu.png'))
        self.shotsMenu = ImageTk.PhotoImage(Image.open('shotsMenu.png'))
        self.settingButton = ImageTk.PhotoImage(Image.open('settingButton.png').resize((36, 34), Image.ANTIALIAS))
        b2 = tk.Button(p1, text="Custom Pour", font=fatFingerFont, image=self.shotsMenu, compound=tk.TOP,
                       bg='royal blue', fg='gray99', command=p2.lift).place(height=150, width=250, relx=250 / 1024,
                                                                            rely=375 / 600)
        b3 = tk.Button(p1, text='Mixed Drink Menu', font=fatFingerFont, image=self.cocktailsMenu, compound=tk.TOP,
                       bg='royal blue', fg='gray99', command=p3.lift).place(height=150, width=250, relx=524 / 1024,
                                                                            rely=375 / 600)
        b4 = tk.Button(p1, text="Settings", font=fatFingerFont, image=self.settingButton, compound=tk.LEFT, bg='gray35',
                       fg='gray99')
        b4.place(relx=822 / 1024, rely=528 / 600, height=70, width=200)

        def pageLift(event):
            p4.lift()
            settingsUpdate(event)

        b4.bind("<ButtonRelease>", pageLift, add='+')

        pourButton2 = tk.Button(p2, text="    Pour    ", font=fatFingerFont, bg='gray35', fg='gray99', command=p6.lift)
        pourButton2.place(relx=0.427, rely=.875, height=75, width=150)

        def confirmPour1(event, drink_name=None):
            p6.lift()
            filename = userID[0] + 'Recents.txt'
            getValue = open(filename, 'r')
            info = getValue.readlines()
            index = len(info) - 1
            currentVal = info[index]
            i = 0
            while list(currentVal)[i] != ',':
                drink_name += currentVal[i]
                i += 1
            DNlabel = tk.Label(p6, text=drink_name, font=headerFont, bg='gray24', fg='gray99').place(relx=0.45,
                                                                                                     rely=0.15)

        pourButton2.bind("<ButtonRelease>", confirmPour1, add='+')

        pourButton3 = tk.Button(p3, text="    Pour    ", font=fatFingerFont, bg='gray35', fg='gray99', command=p8.lift)
        pourButton3.place(relx=0.427, rely=0.875, height=75, width=150)

        def confirmPour2(event, drink_name=None):
            p8.lift()
            filename = userID[0] + 'Recents.txt'
            getValue = open(filename, 'r')
            info = getValue.readlines()
            index = len(info) - 1
            currentVal = info[index]
            print(currentVal)
            i = 0
            while list(currentVal)[i] != ',':
                drink_name += currentVal[i]
                i += 1
            DNlabel = tk.Label(p8, text=drink_name, font=headerFont, bg='gray24', fg='gray99').place(relx=0.45,
                                                                                                     rely=0.15)

        pourButton2.bind("<Button-1>", confirmPour2, add='+')

        userProfileButton = tk.Button(p1, text="User\nProfile", font=fatFingerFont, fg='gray99', bg='gray35',
                                      command=p7.lift).place(y=0, x=822, height=70, width=200)

        bprime = tk.Button(p4, text="Replace Bottle", font=fatFingerFont, bg='gray35', fg='gray99', command=p5.lift)
        bprime.place(relx=0.427, rely=0.875, height=75, width=200)

        p0.show()

        self.helpIcon = ImageTk.PhotoImage(Image.open('helpButton.png').resize((25, 25), Image.ANTIALIAS))
        getHelp = tk.Button(p1, text="  Help", image=self.helpIcon, compound=tk.LEFT, command=p10.lift, bg='gray35',
                            fg='gray99', font=fatFingerFont).place(relx=0, rely=0, height=70, width=200)

        #activatePrimingButton = tk.Button(p5, text="Initiate Priming", font=fatFingerFont, bg='gray35', fg='gray99',
        #                                  command=p9.lift)
        #activatePrimingButton.place(relx=0.4, rely=0.90, height=70, width=200)

        confPour1But = tk.Button(p6, text="Yes", font=fatFingerFont, bg='gray35', fg='gray99')
        confPour1But.place(x=362, rely=0.75, height=60, width=100)

        def confirmLift1(event):
            p1.lift()
            customPourFunc(event)

        confPour1But.bind("<ButtonRelease>", confirmLift1, add='+')

        confPourBut2 = tk.Button(p8, text="Yes", font=fatFingerFont, bg='gray35', fg='gray99')
        confPourBut2.place(x=362, rely=0.75, height=60, width=100)

        def confirmLift2(event):
            p1.lift()
            pourFunc(event)

        confPourBut2.bind("<ButtonRelease>", confirmLift2, add='+')


if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    # root.overrideredirect(True)
    # root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    # root.resizable(0, 0)
    root.wm_geometry("1024x600")

    root.mainloop()
