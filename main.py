import tkinter as tk
from tkinter import ttk, Canvas
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import Image, ImageTk  # pip install pillow
import serial
import time
import csv

global ingredientsArray
ingredientsArray = [["vodka", "rum", "coke", "cran", "trip_sec", "lime"],
                    ["1000000", "0100000", "0010000", "0001000", "0000100", "0000010"]]

ingredient_options = ["Vodka", "Rum", "Coke", "Cranberry", "Triple Sec", "Lime"]

global recipeArray
recipeArray =   [["Cuba Libre", "Harpoon", "Cape Codder", "Kamikaze", "Vodka Gimlet", "Cranberry Vodka"],
                ["0011010", "1101100", "1001100", "1101000", "1001000", "1000100"],
                ["0\n", "60\n", "38\n", "34\n", "50\n", "47\n"],     # vodka
                ["47\n", "0\n", "0\n", "0\n", "0\n", "0\n"],         # rum
                ["47\n", "0\n", "0\n", "0\n", "0\n", "0\n"],         # coke
                ["0\n", "10\n", "57\n", "0\n", "0\n", "57\n"],       # cran juice
                ["0\n", "20\n", "0\n", "33\n", "0\n", "0\n"],        # triple sec
                ["6\n", "10\n", "5\n", "33\n", "50\n", "0\n"]]       # lime juice

inv_file = 'inventory.csv'

inv = open(inv_file, 'r')
csvreader = csv.reader(inv)
inv_now = next(csvreader)
inv.close()
for x in range(6):
    ingredientsArray[0][x] = inv_now[x]

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

        backtoMenu = ttk.Button(self, text="← Back to Main Menu", command=lambda: [resetCount(), controller.show_frame(p1)])
        backtoMenu.place(x=0, y=0, height=60, width=225)

        global customCount
        customCount = [0] * 6

        def resetCount():
            #print("reset")
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
                #print("Current Order:")
                #print(currentOrder[i])

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
                resetCount()
                controller.show_frame(p1)

        custom_pour = tk.Button(self, text="Pour Custom Selection", font=fatFingerFont, bg='gray50', command=lambda: confirm_pour())
        custom_pour.place(relx=.16, rely=.85, height=70, width=420)

        resetCounterButton = tk.Button(self, text="Reset Count", font=fatFingerFont, bg='gray50', command=lambda: resetCount())
        resetCounterButton.place(relx=.63, rely=.85, height=70, width=240)

        shotOption1 = ttk.Label(self, text=ingredientsArray[0][0], font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption1.place(relx=125 / 1024, rely=0.17)
        shotCounter1 = ttk.Label(self, text="0", font=fatFingerFont, background='gray24', foreground='gray99', wraplength=10)
        shotCounter1.place(height=50, width=50, relx=125 / 1024, rely=0.24)
        ounceLabel = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel.place(height=50, width=70, relx=175 / 1024, rely=0.24)
        optAdd1 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter1))
        optAdd1.place(height=80, width=80, relx=320 / 1024, rely=0.19)
        optSub1 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter1))
        optSub1.place(height=80, width=80, relx=420 / 1024, rely=0.19)

        shotOption2 = ttk.Label(self, text=ingredientsArray[0][1], font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption2.place(relx=125 / 1024,  rely=0.4)
        shotCounter2 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=11)
        shotCounter2.place(height=50, width=50, relx=125 / 1024, rely=0.47)
        ounceLabel2 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel2.place(height=50, width=70, relx=175 / 1024, rely=0.47)
        optAdd2 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter2))
        optAdd2.place(height=80, width=80, relx=320 / 1024, rely=0.415)
        optSub2 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter2))
        optSub2.place(height=80, width=80, relx=420 / 1024, rely=0.415)

        shotOption3 = ttk.Label(self, text=ingredientsArray[0][2], font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption3.place(relx=125 / 1024, rely=0.63)
        shotCounter3 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=12)
        shotCounter3.place(height=50, width=50, relx=125 / 1024, rely=0.7)
        ounceLabel3 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel3.place(height=50, width=70, relx=175 / 1024, rely=0.7)
        optAdd3 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter3))
        optAdd3.place(height=80, width=80, relx=320 / 1024, rely=0.65)
        optSub3 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter3))
        optSub3.place(height=80, width=80, relx=420 / 1024, rely=0.65)

        shotOption4 = ttk.Label(self, text=ingredientsArray[0][3], font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption4.place(relx=575 / 1024, rely=0.17)
        shotCounter4 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=13)
        shotCounter4.place(height=50, width=50, relx=575 / 1024, rely=0.24)
        ounceLabel4 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel4.place(height=50, width=70, relx=615 / 1024, rely=0.24)
        optAdd4 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter4))
        optAdd4.place(height=80, width=80, relx=765 / 1024, rely=0.19)
        optSub4 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter4))
        optSub4.place(height=80, width=80, relx=865 / 1024, rely=0.19)

        shotOption5 = ttk.Label(self, text=ingredientsArray[0][4], font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption5.place(relx=575 / 1024, rely=0.4)
        shotCounter5 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=14)
        shotCounter5.place(height=50, width=50, relx=575 / 1024, rely=0.47)
        ounceLabel5 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel5.place(height=50, width=70, relx=615 / 1024, rely=0.47)
        optAdd5 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter5))
        optAdd5.place(height=80, width=80, relx=765 / 1024, rely=0.415)
        optSub5 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter5))
        optSub5.place(height=80, width=80, relx=865 / 1024, rely=0.415)

        shotOption6 = ttk.Label(self, text=ingredientsArray[0][5], font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption6.place(relx=575 / 1024, rely=0.63)
        shotCounter6 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=15)
        shotCounter6.place(height=50, width=50, relx=575 / 1024, rely=0.7)
        ounceLabel6 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel6.place(height=50, width=70, relx=615 / 1024, rely=0.7)
        optAdd6 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter6))
        optAdd6.place(height=80, width=80, relx=765 / 1024, rely=0.65)
        optSub6 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter6))
        optSub6.place(height=80, width=80, relx=865 / 1024, rely=0.65)


class p3(tk.Frame):  # Mixed drink menu
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray24')

        mainHeaderFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=20)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=26)

        backtoMenu = ttk.Button(self, text="← Back to Main Menu", command=lambda: controller.show_frame(p1))
        backtoMenu.place(relx=0, rely=0, height=60, width=225)

        label = ttk.Label(self, text="Mixed Drink Menu", font=mainHeaderFont, background='gray24', foreground='gray99')
        label.place(relx=400 / 1024, rely=.06)

        recipeScroll = ttk.Scrollbar(self)
        recipeScroll.place(height=420, width=25, relx=610 / 1024, rely=130 / 600)
        recipeList = tk.Listbox(self, yscrollcommand=recipeScroll.set, font=headerFont)
        for i in range(6):
            recipeList.insert(i, (recipeArray[0][i]))
        recipeList.place(height=420, width=250, relx=360 / 1024, rely=130 / 600)
        recipeScroll.config(command=recipeList.yview)

        ingredientsDet = ["", "", "", "", "", "", ""]
        cb_labels = [["0", "0", "0", "0", "0", "0"],
                    ["", "", "", "", "", ""]]

        for m in range(6):
            if ingredientsArray[0][m] not in cb_labels[0]:
                cb_labels[0][m] = ingredientsArray[0][m]

        cb_labels[0].sort(reverse=True)
        print(cb_labels[0])
        for e in range(6):
            if cb_labels[0][e] == 'Vodka':
                cb_labels[1][e] = "1000000"
            elif cb_labels[0][e] == "Triple Sec":
                cb_labels[1][e] = "0100000"
            elif cb_labels[0][e] == "Rum":
                cb_labels[1][e] = "0010000"
            elif cb_labels[0][e] == "Lime":
                cb_labels[1][e] = "0001000"
            elif cb_labels[0][e] == "Cranberry":
                cb_labels[1][e] = "0000100"
            elif cb_labels[0][e] == "Coke":
                cb_labels[1][e] = "0000010"


        #print(cb_labels)

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
                            ingredientsDet[j] = ingredient_options[j]
                            drinkDesc.insert(tk.END, str(ingredientsDet[j]) + "\n")

        def resetAll():
            self.destroy()  # destroys the canvas and therefore all of its child-widgets too

        def clear():
            checkSort()

        drinkDesc = tk.Text(self, height=13.4, font=headerFont)
        drinkDesc.place(relx=680 / 1024, rely=130 / 600, height=300, width=300)
        recipeList.bind('<<ListboxSelect>>', onSelect)

        checkSortSum = 000000
        rvar = tk.IntVar()

        def checkSort():
            for k in range(6):
                recipeList.delete(k)
                recipeList.insert(k, (recipeArray[0][k]))
            i = rvar.get()
            for j in reversed(range(6)):
                text = str(i) + ", " + str(j) + ": " + str(list(cb_labels[1][i])[i]) + ", " + str(
                    list(recipeArray[1][j])[i])
                print(text)
                print(list(cb_labels[1][i]))
                print(list(recipeArray[1][j]))
                if list(cb_labels[1][i])[i] != list(recipeArray[1][j])[i]:
                    recipeList.delete(j)

        sortHeight = 15

        def set_cb():
            if cb_labels[0][0] != "0":
                C1 = tk.Radiobutton(self, text=cb_labels[0][0], font=fatFingerFont, bg='gray24', value=0,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C1.place(width=265, height=40, relx=.04, rely=(sortHeight + 170) / 600)
            if cb_labels[0][1] != "0":
                C2 = tk.Radiobutton(self, text=cb_labels[0][1], font=fatFingerFont, bg='gray24', value=1,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C2.place(width=265, height=40, relx=.04, rely=(sortHeight + 230) / 600)
            if cb_labels[0][2] != "":
                C3 = tk.Radiobutton(self, text=cb_labels[0][2], font=fatFingerFont, bg='gray24', value=2,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C3.place(width=265, height=40, relx=.04, rely=(sortHeight + 290) / 600)
            if cb_labels[0][3] != "0":
                C4 = tk.Radiobutton(self, text=cb_labels[0][3], font=fatFingerFont, bg='gray24', value=3,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C4.place(width=265, height=40, relx=.04, rely=(sortHeight + 350) / 600)
            if cb_labels[0][4] != "0":
                C5 = tk.Radiobutton(self, text=cb_labels[0][4], font=fatFingerFont, bg='gray24', value=4,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C5.place(width=265, height=40, relx=.04, rely=(sortHeight + 410) / 600)
            if cb_labels[0][5] != "0":
                C6 = tk.Radiobutton(self, text=cb_labels[0][5], font=fatFingerFont, bg='gray24', value=5,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C6.place(width=265, height=40, relx=.045, rely=(sortHeight + 470) / 600)

        set_cb()

        recipeSort = ttk.Label(self, text='Sort by Ingredient:', font=fatFingerFont, background='gray24', foreground='gray99')
        recipeSort.place(relx=35 / 1024, rely=(sortHeight + 110) / 600)

        pour = tk.Button(self, text="Pour Selection", font=fatFingerFont, bg='gray50', command=lambda: confirm_pour_func())
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
                clear()
                #resetAll()
                controller.show_frame(p1)

            if data == 'Done':
                arduino.close()
                arduino.open()


class p4(tk.Frame):  # Settings
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray24')
        self.settingButton = ImageTk.PhotoImage(Image.open('settingButton.png').resize((75, 75), Image.ANTIALIAS))
        mainHeaderFont = tkFont.Font(family='Bell Gothic Std Light', size=26)
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=40)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)
        label = tk.Label(self, text="Settings", font=headerFont, image=self.settingButton, compound=tk.LEFT, bg='gray24', fg='gray99')
        label.place(relx=160/1024, rely=150/600)
        read_me = "Settings menu allows access to:" \
                  "\n\n    -The INVENTORY MENU: used when replacing \n    inventory and priming the pumps." \
                  "\n\n    -The LED MENU: used to modify the lighting \n    scheme of BotTender."
        read_me_settings = tk.Label(self, text=read_me, font=fatFingerFont, background='gray24', foreground='gray99')
        read_me_settings.place(relx=70/1024, rely=285/600)
        backtoMenu = ttk.Button(self, text="← Back to Main Menu", command=lambda: controller.show_frame(p1))
        backtoMenu.place(x=0, y=0, height=60, width=225)
        inventory_menu = tk.Button(self, text="Inventory Menu", font=fatFingerFont, bg='gray50',
                                   command=lambda: controller.show_frame(p5))
        inventory_menu.place(relx=650/1024, rely=145/600, height=150, width=250)
        led_menu = tk.Button(self, text="LED Menu", font=fatFingerFont, bg='gray50') #command=lambda: controller.show_frame(p5)
        led_menu.place(relx=650 / 1024, rely=345 / 600, height=150, width=250)


class p5(tk.Frame):  # inventory menu
    def __init__(self, parent, controller):
        self.bays = ImageTk.PhotoImage(Image.open('tv_of_bays.png'))
        tk.Frame.__init__(self, parent, bg='gray28')
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=30)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=20)
        backSettings = ttk.Button(self, text="← Back to Settings", command=lambda: controller.show_frame(p4))
        backSettings.place(x=0, y=0, height=60, width=225)
        bay_view = Canvas(self, bg="gray50", height=400, width=400, highlightthickness=0)
        bay_view.create_image(200, 200, image=self.bays)
        bay_view.place(relx=282 / 1024, rely=130 / 600)
        #self.bay_view = tk.Label(self, image=self.bays)
        #self.bay_view.place(relx=80 / 1024, rely=128 / 600)
        inv_header = ttk.Label(self, text="Inventory Control", font=headerFont, background='gray28',
                                     foreground='gray99')
        inv_header.place(relx=340 / 1024, rely=40/600, width=400)
        ingredients = ttk.Label(self, text="Ingredients: Choose one \nfor the selected bays", font=fatFingerFont,
                                background='gray28', foreground='gray99')
        ingredients.place(relx=695 / 1024, rely=120/600, width=350)
        current_inv = ttk.Label(self, text="Current Inventory:", font=fatFingerFont, background='gray28',
                                     foreground='gray99')
        current_inv.place(relx=60/1024, rely=120/600)
        inv_label = {}
        list_start = 170
        prime_bay = {}

        def set_labels():
            for x in range(6):
                #print(str(x) + ingredientsArray[0][x])
                bottle = "Bay " + str(x + 1) + ": " + ingredientsArray[0][x]
                inv_label[x] = ttk.Label(self, text="", font=fatFingerFont, background='gray28',
                                         foreground='gray99')
                inv_label[x].config(text="")
                inv_label[x].config(text=bottle)
                inv_label[x].place(relx=60 / 1024, rely=(list_start + (x * 60)) / 600)
        set_labels()

        def clear():
            cb_var1.set(0)
            cb_var2.set(0)
            cb_var3.set(0)
            cb_var4.set(0)
            cb_var5.set(0)
            cb_var6.set(0)

        def upd_inv_confirm():
            if messagebox.askquestion("Confirm", "Is there a cup under the dispenser for priming?") == "yes":
                upd_inv(event=set_inv)
            else:
                tk.messagebox.showinfo("Selection", "Make a Selection")

        def upd_inv(event):
            inv = open(inv_file, 'w')
            csvwriter = csv.writer(inv)
            for t in recipeList.curselection():
                # print(recipeList.get(t))
                selected = recipeList.get(t)
            #print(selected)
            for n in range(6):
                #print(cb_vars[n].get())
                if cb_vars[n].get() == 1:
                    prime_bay[n] = 1
                    ingredientsArray[0][n] = selected
                else:
                    prime_bay[n] = 0

            csvwriter.writerow(ingredientsArray[0])
            inv.close()
            priming = ["", "", "", "", "", ""]

            newline = "\n"
            for i in range(6):
                priming[i] = str(prime_bay[i])
                priming[i] = priming[i] + newline

            arduino.flush()
            arduino.write("prime\n".encode())
            arduino.flush()
            data = arduino.readline().decode('utf-8').rstrip()
            print(data)
            while data != 'bay1':
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
            if data == 'bay1':
                arduino.write(priming[0].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                # time.sleep(0.05)
            if data == 'bay2':
                arduino.write(priming[1].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'bay3':
                arduino.write(priming[2].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'bay4':
                arduino.write(priming[3].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'bay5':
                arduino.write(priming[4].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            if data == 'bay6':
                arduino.write(priming[5].encode('utf-8'))
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                time.sleep(0.05)
            while data != 'Done':
                data = arduino.readline().decode('utf-8').rstrip()
                print(data)
                set_labels()
                clear()

        cb_var1 = tk.IntVar()
        cb_var2 = tk.IntVar()
        cb_var3 = tk.IntVar()
        cb_var4 = tk.IntVar()
        cb_var5 = tk.IntVar()
        cb_var6 = tk.IntVar()
        cb_vars = [cb_var1, cb_var2, cb_var3, cb_var4, cb_var5, cb_var6]

        C1 = tk.Checkbutton(self, text="1", font=fatFingerFont, background='gray24',
                            foreground='gray99', indicatoron=0, variable=cb_var1, onvalue=1, offvalue=0)
        C2 = tk.Checkbutton(self, text="2", font=fatFingerFont, background='gray24',
                            foreground='gray99', indicatoron=0, variable=cb_var2, onvalue=1, offvalue=0)
        C3 = tk.Checkbutton(self, text="3", font=fatFingerFont, background='gray24',
                            foreground='gray99', indicatoron=0, variable=cb_var3, onvalue=1, offvalue=0)
        C4 = tk.Checkbutton(self, text="4", font=fatFingerFont, background='gray24',
                            foreground='gray99', indicatoron=0, variable=cb_var4, onvalue=1, offvalue=0)
        C5 = tk.Checkbutton(self, text="5", font=fatFingerFont, background='gray24',
                            foreground='gray99', indicatoron=0, variable=cb_var5, onvalue=1, offvalue=0)
        C6 = tk.Checkbutton(self, text="6", font=fatFingerFont, background='gray24',
                            foreground='gray99', indicatoron=0, variable=cb_var6, onvalue=1, offvalue=0)
        C1.place(width=50, height=30, relx=512/1024, rely=183/600)
        C2.place(width=50, height=30, relx=565/1024, rely=279/600)
        C3.place(width=50, height=30, relx=512/1024, rely=373/600)
        C4.place(width=50, height=30, relx=399/1024, rely=373/600)
        C5.place(width=50, height=30, relx=349/1024, rely=279/600)
        C6.place(width=50, height=30, relx=402/1024, rely=183/600)

        recipeScroll = ttk.Scrollbar(self)
        recipeScroll.place(height=250, width=25, relx=945 / 1024, rely=190 / 600)
        recipeList = tk.Listbox(self, yscrollcommand=recipeScroll.set, font=fatFingerFont)
        for i in range(6):
            recipeList.insert(i, (ingredient_options[i]))
        recipeList.place(height=250, width=250, relx=695 / 1024, rely=190 / 600)
        recipeScroll.config(command=recipeList.yview)

        set_inv = tk.Button(self, text="Update Inventory", font=fatFingerFont, bg='gray50', command=lambda: upd_inv_confirm())
        set_inv.place(relx=695/1024, rely=460/600, height=70, width=275)


class p10(tk.Frame):  # help menu
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray24')

        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=16)
        welcomeFont = tkFont.Font(family='Bell Gothic Std Light', size=42, weight='bold')

        backtoMenu = ttk.Button(self, text="← Back to Main Menu", command=lambda: controller.show_frame(p1))
        backtoMenu.place(x=0, y=0, height=70, width=240)

        instructionList = "Welcome to BotTender!\n\nTo get started with BotTender, click one of the menu " + \
                          "options\nfrom the MAIN MENU for CUSTOM DRINKS or " \
                          "DRINKS LIST:\n\n    -The CUSTOM DRINKS option will allow you " + \
                          "to dispense customized drinks \n    or individual shots\n\n    -The DRINKS LIST " + \
                          "option will allow you to choose from one of our pre-set \n" + \
                          "    recipes loaded your with BotTender based on the ingredients available. " + \
                          "\n    With options to sort by ingredient, it's easy to find a drink.\n\n" + \
                          "    -The settings menu will lead to the INVENTORY MENU to manage " \
                          "ingredient\n    refills and change, and the LED MENU to control the lighting scheme"

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
