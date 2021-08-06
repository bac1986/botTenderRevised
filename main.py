import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import Image, ImageTk  # pip install pillow
import serial
import time
import subprocess

global ingredientsArray
ingredientsArray = [["Vodka", "Rum", "Triple sec", "Coke", "Cranberry", "Lime", "Whiskey"],
                    ["1000000", "0100000", "0010000", "0001000", "0000100", "0000010", "0000001"]]

global recipeArray
recipeArray = [["Cuba Libre", "Harpoon", "Cape Codder", "Kamikaze", "Vodka Gimlet", "Cranberry Vodka"],
               ["0101010", "1010110", "1000110", "1010010", "1000010", "1000100"],
               ["0\n", "60\n", "38\n", "34\n", "50\n", "47\n"],  # vodka
               ["47\n", "0\n", "0\n", "0\n", "0\n", "0\n"],  # rum
               ["0\n", "20\n", "0\n", "33\n", "0\n", "0\n"],  # triple sec
               ["47\n", "0\n", "0\n", "0\n", "0\n", "0\n"],  # coke
               ["0\n", "10\n", "57\n", "0\n", "0\n", "57\n"],  # cran juice
               ["6\n", "10\n", "5\n", "33\n", "50\n", "0\n"]]  # lime juice

arduino = serial.Serial()
arduino.port = 'COM4'
arduino.baudrate = 9600
arduino.timeout = 0.1
arduino.setRTS(False)
arduino.open()


class MainView(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #button_frame = tk.Frame(self)
        #button_frame.pack(side="top", fill="x", expand=False)
        # fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=18)

        container = tk.Frame(self, width=1024, height=600)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in (p1, p2, p3, p4, p5, p10):
            frame = F(container, self)

            self.frames[F] = frame
            frame.place(relheight=1, relwidth=1)

        self.show_frame(p1)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class p1(tk.Frame):  # main menu
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray24')
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)
        welcomeFont = tkFont.Font(family="Gill Sans", size=50)

        self.logoIMG = ImageTk.PhotoImage(Image.open('cocktail.png').resize((340, 340), Image.ANTIALIAS))
        self.botTenderLogo = tk.Label(self, image=self.logoIMG).place(relx=120 / 1024, rely=180 / 600)
        self.cocktailsMenu = ImageTk.PhotoImage(Image.open('Cocktailmenu.png'))
        self.shotsMenu = ImageTk.PhotoImage(Image.open('shotsMenu.png'))
        self.settingButton = ImageTk.PhotoImage(Image.open('settingButton.png').resize((36, 34), Image.ANTIALIAS))
        self.helpIcon = ImageTk.PhotoImage(Image.open('helpButton.png').resize((25, 25), Image.ANTIALIAS))

        bottender = tk.Label(self, text="BotTender", font=welcomeFont, background='gray24', foreground='gray99')
        bottender.place(relx=350 / 1024, rely=50 / 600)

        b2 = tk.Button(self, text="Custom Pour Menu", font=fatFingerFont, bg='gray50', image=self.shotsMenu, compound=tk.TOP, command=lambda: controller.show_frame(p2))
        b2.place(height=150, width=250, relx=590 / 1024, rely=175 / 600)

        b3 = tk.Button(self, text='Mixed Drink Menu', font=fatFingerFont, bg='gray50', image=self.cocktailsMenu, compound=tk.TOP, command=lambda: controller.show_frame(p3))
        b3.place(height=150, width=250, relx=590 / 1024, rely=375 / 600)

        b4 = ttk.Button(self, text="Settings", image=self.settingButton, compound=tk.LEFT, command=lambda: controller.show_frame(p4))
        b4.place(relx=822 / 1024, rely=0, height=70, width=200)

        getHelp = ttk.Button(self, text="  Help", image=self.helpIcon, compound=tk.LEFT, command=lambda: controller.show_frame(p10))
        getHelp.place(relx=0, rely=0, height=70, width=200)


class p2(tk.Frame):  # Custom/Shots
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray24')

        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=26)

        label = ttk.Label(self, text="Shots/Custom Pour Menu", font=fatFingerFont, background='gray24', foreground='gray99')
        label.place(relx=0.33, rely=.05, height=60)

        backtoMenu = ttk.Button(self, text="← Back to Main Menu", command=lambda: controller.show_frame(p1))
        backtoMenu.place(x=0, y=0, height=60, width=225)

        global customCount
        customCount = [0] * 6

        def resetCount():
            print("reset")
            i = 0
            for i in range(6):
                if customCount[i] > 0:
                    customCount[i] -= customCount[i]
                    if i == 0:
                        shotCounter1["text"] = customCount[i]
                    elif i == 1:
                        shotCounter2["text"] = customCount[i]
                    elif i == 2:
                        shotCounter3["text"] = customCount[i]
                    elif i == 3:
                        shotCounter4["text"] = customCount[i]
                    elif i == 4:
                        shotCounter5["text"] = customCount[i]
                    elif i == 5:
                        shotCounter6["text"] = customCount[i]
                    print(customCount[i])

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

        def confirm_pour():
            if messagebox.askquestion("Confirm", "Do you want to dispense this custom order?") == "yes":
                customPourFunc(event=custom_pour)

            else:
                tk.messagebox.showinfo("Reset", "Resetting Selection")
                resetCount()

        def customPourFunc(event):
            # gui stuff
            global customIngredients
            currentOrder = ["", "", "", "", "", ""]
            customAmount = 0
            i = 0
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
                controller.show_frame(p1)

        custom_pour = tk.Button(self, text="Pour Custom Selection", font=fatFingerFont, command=lambda: confirm_pour())
        custom_pour.place(relx=.18, rely=.85, height=70, width=380)

        resetCounterButton = tk.Button(self, text="Reset Count", font=fatFingerFont, command=lambda: resetCount())
        resetCounterButton.place(relx=.63, rely=.85, height=70, width=220)

        shotOption1 = ttk.Label(self, text="Vodka", font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption1.place(relx=125 / 1024, rely=0.17)
        shotCounter1 = ttk.Label(self, text="0", font=fatFingerFont, background='gray24', foreground='gray99', wraplength=10)
        shotCounter1.place(height=50, width=50, relx=125 / 1024, rely=0.24)
        ounceLabel = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel.place(height=50, width=70, relx=175 / 1024, rely=0.24)
        optAdd1 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter1))
        optAdd1.place(height=80, width=80, relx=320 / 1024, rely=0.19)
        optSub1 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter1))
        optSub1.place(height=80, width=80, relx=420 / 1024, rely=0.19)

        shotOption2 = ttk.Label(self, text="Rum", font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption2.place(relx=125 / 1024,  rely=0.4)
        shotCounter2 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=11)
        shotCounter2.place(height=50, width=50, relx=125 / 1024, rely=0.47)
        ounceLabel2 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel2.place(height=50, width=70, relx=175 / 1024, rely=0.47)
        optAdd2 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter2))
        optAdd2.place(height=80, width=80, relx=320 / 1024, rely=0.415)
        optSub2 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter2))
        optSub2.place(height=80, width=80, relx=420 / 1024, rely=0.415)

        shotOption3 = ttk.Label(self, text="Triple Sec", font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption3.place(relx=125 / 1024, rely=0.63)
        shotCounter3 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=12)
        shotCounter3.place(height=50, width=50, relx=125 / 1024, rely=0.7)
        ounceLabel3 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel3.place(height=50, width=70, relx=175 / 1024, rely=0.7)
        optAdd3 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter3))
        optAdd3.place(height=80, width=80, relx=320 / 1024, rely=0.65)
        optSub3 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter3))
        optSub3.place(height=80, width=80, relx=420 / 1024, rely=0.65)

        shotOption4 = ttk.Label(self, text="Coke", font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption4.place(relx=575 / 1024, rely=0.17)
        shotCounter4 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=13)
        shotCounter4.place(height=50, width=50, relx=575 / 1024, rely=0.24)
        ounceLabel4 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel4.place(height=50, width=70, relx=615 / 1024, rely=0.24)
        optAdd4 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter4))
        optAdd4.place(height=80, width=80, relx=750 / 1024, rely=0.19)
        optSub4 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter4))
        optSub4.place(height=80, width=80, relx=850 / 1024, rely=0.19)

        shotOption5 = ttk.Label(self, text="Cranberry", font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption5.place(relx=575 / 1024, rely=0.4)
        shotCounter5 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=14)
        shotCounter5.place(height=50, width=50, relx=575 / 1024, rely=0.47)
        ounceLabel5 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel5.place(height=50, width=70, relx=615 / 1024, rely=0.47)
        optAdd5 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter5))
        optAdd5.place(height=80, width=80, relx=750 / 1024, rely=0.415)
        optSub5 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter5))
        optSub5.place(height=80, width=80, relx=850 / 1024, rely=0.415)

        shotOption6 = ttk.Label(self, text="Lime", font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption6.place(relx=575 / 1024, rely=0.63)
        shotCounter6 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=15)
        shotCounter6.place(height=50, width=50, relx=575 / 1024, rely=0.7)
        ounceLabel6 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel6.place(height=50, width=70, relx=615 / 1024, rely=0.7)
        optAdd6 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter6))
        optAdd6.place(height=80, width=80, relx=750 / 1024, rely=0.65)
        optSub6 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter6))
        optSub6.place(height=80, width=80, relx=850 / 1024, rely=0.65)


class p3(tk.Frame):  # Mixed drink menu
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray24')

        mainHeaderFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=20)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=26)

        userFile = 'userRecents' + '.txt'
        userData = open(userFile, 'a+')

        backtoMenu = ttk.Button(self, text="← Back to Main Menu", command=lambda: controller.show_frame(p1))
        backtoMenu.place(relx=0, rely=0, height=60, width=225)

        label = ttk.Label(self, text="Mixed Drink Menu", font=mainHeaderFont, background='gray24', foreground='gray99')
        label.place(relx=400 / 1024, rely=.06)

        recipeScroll = ttk.Scrollbar(self)
        recipeScroll.place(height=420, width=25, relx=600 / 1024, rely=130 / 600)
        recipeList = tk.Listbox(self, yscrollcommand=recipeScroll.set, font=headerFont)
        for i in range(6):
            recipeList.insert(i, (recipeArray[0][i]))
        recipeList.place(height=420, width=250, relx=350 / 1024, rely=130 / 600)
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
        drinkDesc.place(relx=680 / 1024, rely=130 / 600, height=300, width=300)
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

        sortHeight = 15

        C1 = tk.Checkbutton(self, text=ingredientsArray[0][0], font=fatFingerFont, background='gray24', foreground='gray99', indicatoron=0, variable=CheckVar1, onvalue=1, offvalue=0, command=lambda: checkSort())
        C2 = tk.Checkbutton(self, text=ingredientsArray[0][1], font=fatFingerFont, background='gray24', foreground='gray99', indicatoron=0, variable=CheckVar2, onvalue=1, offvalue=0, command=lambda: checkSort())
        C3 = tk.Checkbutton(self, text=ingredientsArray[0][2], font=fatFingerFont, background='gray24', foreground='gray99', indicatoron=0, variable=CheckVar3, onvalue=1, offvalue=0, command=lambda: checkSort())
        C4 = tk.Checkbutton(self, text=ingredientsArray[0][3], font=fatFingerFont, background='gray24', foreground='gray99', indicatoron=0, variable=CheckVar4, onvalue=1, offvalue=0, command=lambda: checkSort())
        C5 = tk.Checkbutton(self, text=ingredientsArray[0][4], font=fatFingerFont, background='gray24', foreground='gray99', indicatoron=0, variable=CheckVar5, onvalue=1, offvalue=0, command=lambda: checkSort())
        C6 = tk.Checkbutton(self, text=ingredientsArray[0][5], font=fatFingerFont, background='gray24', foreground='gray99', indicatoron=0, variable=CheckVar6, onvalue=1, offvalue=0, command=lambda: checkSort())
        C1.place(width=265, height=40, relx=.045, rely=(sortHeight + 170) / 600)
        C2.place(width=265, height=40, relx=.045, rely=(sortHeight + 230) / 600)
        C3.place(width=265, height=40, relx=.045, rely=(sortHeight + 290) / 600)
        C4.place(width=265, height=40, relx=.045, rely=(sortHeight + 350) / 600)
        C5.place(width=265, height=40, relx=.045, rely=(sortHeight + 410) / 600)
        C6.place(width=265, height=40, relx=.045, rely=(sortHeight + 470) / 600)

        recipeSort = ttk.Label(self, text='Sort by Ingredient:', font=fatFingerFont, background='gray24', foreground='gray99')
        recipeSort.place(relx=25 / 1024, rely=(sortHeight + 110) / 600)

        pour = tk.Button(self, text="Pour Selection", font=fatFingerFont, command=lambda: confirm_pour_func())
        pour.place(relx=680/1024, rely=470/600, height=80, width=300)


        def confirm_pour_func():
            if messagebox.askquestion("Confirm", "Do you want to dispense this selection?") == "yes":
                pourFunc(event=confirm_pour_func)
            else:
                tk.messagebox.showinfo("Selection", "Make a Selection")

        def pourFunc(event):
            # python side
            global drinkIngredients
            drinkIngredients = ''
            for i in range(6):
                if drinkName == recipeArray[0][i]:
                    drinkIngredients = recipeArray[1][i]
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
                controller.show_frame(p1)

            if data == 'Done':
                arduino.close()
                arduino.open()


class p4(tk.Frame):  # Settings
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray24')
        mainHeaderFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=15)

        backtoMenu = ttk.Button(self, text="← Back to Main Menu", command=lambda: controller.show_frame(p1))
        backtoMenu.place(x=0, y=0, height=60, width=225)
        label = ttk.Label(self, text="Settings", font=headerFont, background='gray24', foreground='gray99')
        label.pack(side="top", anchor="n")

        fillStatus = ttk.Label(self, text="Bottle Fill Status", font=headerFont, background='gray24', foreground='gray99')
        fillStatus.place(x=325, rely=0.2, width=374)

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

            inventory = open('botInventory.txt', "w")
            str1 = ''
            str1.join(totalStatus)
            print(str1)
            inventory.write(str1.join(totalStatus))
            inventory.close()

            self.bottle1Fill = ttk.Label(self, image=self.fillImagePlacer[0], background='gray24')
            self.bottle1Fill.place(x=bottlePlacerX, rely=0.3)
            self.bottle2Fill = ttk.Label(self, image=self.fillImagePlacer[1], background='gray24')
            self.bottle2Fill.place(x=bottlePlacerX + 118, rely=0.3)
            self.bottle3Fill = ttk.Label(self, image=self.fillImagePlacer[2], background='gray24')
            self.bottle3Fill.place(x=bottlePlacerX + (118 * 2), rely=0.3)
            self.bottle4Fill = ttk.Label(self, image=self.fillImagePlacer[3], background='gray24')
            self.bottle4Fill.place(x=bottlePlacerX + (118 * 3), rely=0.3)
            self.bottle5Fill = ttk.Label(self, image=self.fillImagePlacer[4], background='gray24')
            self.bottle5Fill.place(x=bottlePlacerX + (118 * 4), rely=0.3)
            self.bottle6Fill = ttk.Label(self, image=self.fillImagePlacer[5], background='gray24')
            self.bottle6Fill.place(x=bottlePlacerX + (118 * 5), rely=0.3)

            bottle1desc = ttk.Label(self, text="Content:\n" + totalStatus[1] + "\nFill Status: " + totalStatus[3] + "%", background='gray24', foreground='gray99')
            bottle1desc.place(x=bottlePlacerX + 25, rely=0.65)
            bottle2desc = ttk.Label(self, text="Content:\n" + totalStatus[4] + "\nFill Status: " + totalStatus[6] + "%", background='gray24', foreground='gray99')
            bottle2desc.place(x=bottlePlacerX + 25 + 118, rely=0.65)
            bottle3desc = ttk.Label(self, text="Content:\n" + totalStatus[7] + "\nFill Status: " + totalStatus[9] + "%", background='gray24', foreground='gray99')
            bottle3desc.place(x=bottlePlacerX + 25 + (118 * 2), rely=0.65)
            bottle4desc = ttk.Label(self, text="Content:\n" + totalStatus[10] + "\nFill Status: " + totalStatus[12] + "%", background='gray24', foreground='gray99')
            bottle4desc.place(x=bottlePlacerX + 25 + (118 * 3), rely=0.65)
            bottle5desc = ttk.Label(self, text="Content:\n" + totalStatus[13] + "\nFill Status: " + totalStatus[15] + "%", background='gray24', foreground='gray99')
            bottle5desc.place(x=bottlePlacerX + 25 + (118 * 4), rely=0.65)
            bottle6desc = ttk.Label(self, text="Content:\n" + totalStatus[16] + "\nFill Status: " + totalStatus[18] + "%", background='gray24', foreground='gray99')
            bottle6desc.place(x=bottlePlacerX + 25 + (118 * 5), rely=0.65)

        refresh = ttk.Button(self, text="Refresh", command=lambda: settingsUpdate())
        refresh.place(x=1, y=1)


class p5(tk.Frame):  # priming menu
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray24')
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=15)

        backSettings = ttk.Button(self, text="← Back to Settings", command=lambda: controller.show_frame(p4))
        backSettings.place(x=0, y=0, height=60, width=225)

        primemenuheader1 = ttk.Label(self, text="What is Pump Priming?", font=headerFont, background='gray24', foreground='gray99')
        primemenuheader1.place(relx=(512 - 200) / 1024, rely=0.025, width=400)
        primemenuheader2 = ttk.Label(self, text="Priming Instructions:", font=headerFont, background='gray24', foreground='gray99')
        primemenuheader2.place(relx=(512 - 175) / 1024, rely=0.475, width=350)

        primeInstructText1 = "Our pumps use the principle of a vaccuum to move your ingredients without contamination.\n\n" \
                             "The process of priming clears any remaining liquid from the pump lines and preps them\n\nwith your new ingredient selection. " \
                             "This process should be repeated every time a bottle\n\nis replaced to ensure we can deliver your favorite drinks " \
                             "with optimal speed and quality!"

        primeInstructText2 = "Before priming the pumps, please place a container below the BotTender nozzle to\n\ncatch excess liquid. " \
                             "With the new bottle installed press 'PRIME and select the bottle\n\nlocation. An LED indicator will light up " \
                             "to confirm your selection. This process will\n\ntake approximately xx seconds and the LED indicator will turn off when it is done."

        primeInstruct = tk.Label(self, text=primeInstructText1, font=fatFingerFont, bg='gray24', fg='gray99', justify=tk.LEFT)
        primeInstruct.place(relx=0.075, rely=0.15)
        primeInstruct2 = tk.Label(self, text=primeInstructText2, font=fatFingerFont, bg='gray24', fg='gray99', justify=tk.LEFT)
        primeInstruct2.place(relx=0.075, rely=0.6)


class p10(tk.Frame):  # help menu
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray24')

        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=18)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)
        welcomeFont = tkFont.Font(family='Bell Gothic Std Light', size=42, weight='bold')

        backtoMenu = ttk.Button(self, text="← Back to Main Menu", command=lambda: controller.show_frame(p1))
        backtoMenu.place(x=0, y=0, height=70, width=240)

        instructionList = "Welcome to BotTender!\n\nTo get started with your drink, click one of the " + \
                          "two buttons \nfor Custom/Shots or Mixed Drinks:\n\n    -The Custom Shots button will allow you " + \
                          "to dispense individual shots\n\n    -The Mixed Drinks " + \
                          "button will allow you to choose from one of our \n" + \
                          "    pre-set recipes based on the options you have " + \
                          "loaded your BotTender with.\n\n    -There are options to " + \
                          "sort by ingredient or search for your favorite recipe\n\n" + \
                          "    -The settings menu will show you the fill status of " + \
                          'your containers and\n    allow you to prime the pumps ' + \
                          "when replacing your containers."

        helpInstructions = ttk.Label(self, text=instructionList, font=headerFont, background='gray24', foreground='gray99')
        helpInstructions.place(relx=0.09, rely=0.2)


app = MainView()
app.mainloop()

#from MainView import *


#global primeArray
#primeArray = ["10\n", "10\n", "10\n", "10\n", "10\n", "10\n"]


#if __name__ == "__main__":
#    root = tk.Tk()
#    main = MainView(root)
#    main.pack(side="top", fill="both", expand=True)
#    root.overrideredirect(True)
#    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
#    root.resizable(0, 0)
#    root.wm_geometry("1024x600")
#    root.mainloop()
