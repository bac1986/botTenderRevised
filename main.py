import tkinter as tk
from tkinter import ttk, Canvas
import tkinter.font as tkFont
from tkinter import messagebox
from PIL import Image, ImageTk  # pip install pillow
from gpiozero import *
from time import *
import csv

#global bays
#bays = [LED(2), LED(3), LED(4), LED(17), LED(27), LED(22)]

#************************************CSV Implementing********************************

options = [["", "", "", "", "", ""],    # 0 name
           ["", "", "", "", "", ""],    # 1 label
           ["", "", "", "", "", ""],    # 2 binary_id
           ["", "", "", "", "", ""],    # 3 loaded
           ["", "", "", "", "", ""],    # 4 num_bays
           ["", "", "", "", "", ""]]    # 5 bay

option_labels = ["", "", "", "", "", ""]

recipeArray = [["Cuba Libre", "Harpoon", "Cape Codder", "Kamikaze", "Vodka Gimlet", "Cranberry Vodka"],
               ["011001", "100101", "100111", "100011", "100001", "100101"],
               [0,  40, 36, 34, 50, 25],    # vodka
               [27, 0,  0,  0,  0,  0],     # rum
               [66, 0,  0,  0,  0,  0],     # coke
               [0,  53, 50, 0,  0,  65],    # cran juice
               [0,  0,  7,  33, 0,  0],     # triple sec
               [7,  7,  7,  33, 50, 10],    # lime juice
               ["Rum: 1 2/3 oz\nLime Juice: 1/4 oz\nCoke: 4 oz",
                "Vodka: 1 1/2 oz\nLime Juice: 1/4 oz\nCranberry Juice: 2 oz",
                "Vodka: 1 1/2 oz\nTriple Sec: 1/4 oz\nLime Juice: 1/4 oz\nCranberry Juice: 2 oz",
                "Vodka: 1 oz\nTriple Sec: 1 oz\nLime Juice: 1 oz",
                "Vodka: 1 oz\nLime Juice: 1 oz",
                "Vodka: 1 1/3 oz\nLime Juice: 1/3 oz\nCranberry Juice: 3 oz"]]

dname = 0
dlabel = 1
bin_id = 2
loaded = 3
num_bays = 4
bay_id = 5
inv_file = 'inventory.csv'

with open(inv_file, 'r') as inv:
    csvreader = csv.reader(inv)
    for row in range(6):
        options[row] = next(csvreader)
        print(options[row])
for each in range(6):
    if options[loaded][each] == 'true':
        bay_count = int(options[num_bays][each])
        if bay_count > 1:
            for this in range(6):
                if list(options[bay_id][each])[this] == '1':
                    # assign some text to this label index
                    option_labels[this] = options[1][each]
        else:
            option_labels[each] = options[1][each]
print(option_labels)

#************************************************************************************

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
        self.update()
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

        def selected():
            if sum(customCount) == 0:
                return False

        def resetCount():
            #print("reset")
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
            if sum(customCount) != 0:
                if messagebox.askquestion("Confirm", "Do you want to dispense this custom order?") == "yes":
                    customPourFunc(event=custom_pour)
                else:
                    tk.messagebox.showinfo("Reset", "Resetting Selection")
                    resetCount()
            else:
                tk.messagebox.showerror("Selection", "Select ingredient(s)")

        def customPourFunc(event):
            # gui stuff
            global customIngredients
            currentOrder = ["", "", "", "", "", "", ""]
            newline = "\n"
            for i in range(6):
                currentOrder[i] = str(customCount[i] * 100)
                currentOrder[i] = currentOrder[i] + newline

            currentOrder[6] = "1\n"

            print(currentOrder)


        custom_pour = tk.Button(self, text="Pour Custom Selection", font=fatFingerFont, bg='gray50', command=lambda: confirm_pour())
        custom_pour.place(relx=.16, rely=.85, height=70, width=420)

        resetCounterButton = tk.Button(self, text="Reset Count", font=fatFingerFont, bg='gray50', command=lambda: resetCount())
        resetCounterButton.place(relx=.63, rely=.85, height=70, width=240)

        shotOption1 = ttk.Label(self, text=option_labels[0], font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption1.place(relx=125 / 1024, rely=0.17)
        shotCounter1 = ttk.Label(self, text="0", font=fatFingerFont, background='gray24', foreground='gray99', wraplength=10)
        shotCounter1.place(height=50, width=50, relx=125 / 1024, rely=0.24)
        ounceLabel = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel.place(height=50, width=70, relx=175 / 1024, rely=0.24)
        optAdd1 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter1))
        optAdd1.place(height=80, width=80, relx=320 / 1024, rely=0.19)
        optSub1 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter1))
        optSub1.place(height=80, width=80, relx=420 / 1024, rely=0.19)

        shotOption2 = ttk.Label(self, text=option_labels[1], font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption2.place(relx=125 / 1024,  rely=0.4)
        shotCounter2 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=11)
        shotCounter2.place(height=50, width=50, relx=125 / 1024, rely=0.47)
        ounceLabel2 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel2.place(height=50, width=70, relx=175 / 1024, rely=0.47)
        optAdd2 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter2))
        optAdd2.place(height=80, width=80, relx=320 / 1024, rely=0.415)
        optSub2 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter2))
        optSub2.place(height=80, width=80, relx=420 / 1024, rely=0.415)

        shotOption3 = ttk.Label(self, text=option_labels[2], font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption3.place(relx=125 / 1024, rely=0.63)
        shotCounter3 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=12)
        shotCounter3.place(height=50, width=50, relx=125 / 1024, rely=0.7)
        ounceLabel3 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel3.place(height=50, width=70, relx=175 / 1024, rely=0.7)
        optAdd3 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter3))
        optAdd3.place(height=80, width=80, relx=320 / 1024, rely=0.65)
        optSub3 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter3))
        optSub3.place(height=80, width=80, relx=420 / 1024, rely=0.65)

        shotOption4 = ttk.Label(self, text=option_labels[3], font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption4.place(relx=575 / 1024, rely=0.17)
        shotCounter4 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=13)
        shotCounter4.place(height=50, width=50, relx=575 / 1024, rely=0.24)
        ounceLabel4 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel4.place(height=50, width=70, relx=615 / 1024, rely=0.24)
        optAdd4 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter4))
        optAdd4.place(height=80, width=80, relx=765 / 1024, rely=0.19)
        optSub4 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter4))
        optSub4.place(height=80, width=80, relx=865 / 1024, rely=0.19)

        shotOption5 = ttk.Label(self, text=option_labels[4], font=fatFingerFont, background='gray24', foreground='gray99')
        shotOption5.place(relx=575 / 1024, rely=0.4)
        shotCounter5 = ttk.Label(self, text=0, font=fatFingerFont, background='gray24', foreground='gray99', wraplength=14)
        shotCounter5.place(height=50, width=50, relx=575 / 1024, rely=0.47)
        ounceLabel5 = ttk.Label(self, text="(oz)", font=fatFingerFont, background='gray24', foreground='gray99')
        ounceLabel5.place(height=50, width=70, relx=615 / 1024, rely=0.47)
        optAdd5 = tk.Button(self, text="+", font=fatFingerFont, command=lambda: addShot(shotCounter5))
        optAdd5.place(height=80, width=80, relx=765 / 1024, rely=0.415)
        optSub5 = tk.Button(self, text="-", font=fatFingerFont, command=lambda: lessShot(shotCounter5))
        optSub5.place(height=80, width=80, relx=865 / 1024, rely=0.415)

        shotOption6 = ttk.Label(self, text=option_labels[5], font=fatFingerFont, background='gray24', foreground='gray99')
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

        # ***************************************Variables*********************************************
        cb_labels = [["0", "0", "0", "0", "0", "0"],
                     ["", "", "", "", "", ""]]
        rvar = tk.IntVar()
        dispense = [0, 0, 0, 0, 0, 0, 0]

        # ***************************************Labels*********************************************
        label = ttk.Label(self, text="Mixed Drink Menu", font=mainHeaderFont, background='gray24', foreground='gray99')
        label.place(relx=400 / 1024, rely=.06)
        recipeSort = ttk.Label(self, text='Sort by Ingredient:', font=fatFingerFont, background='gray24',
                               foreground='gray99')
        recipeSort.place(relx=35 / 1024, rely=125 / 600)

        # ***************************************Buttons*********************************************
        backtoMenu = ttk.Button(self, text="← Back to Main Menu", command=lambda: controller.show_frame(p1))
        backtoMenu.place(relx=0, rely=0, height=60, width=225)
        pour = tk.Button(self, text="Pour Selection", font=fatFingerFont, bg='gray50',
                         command=lambda: confirm_pour_func())
        pour.place(relx=680 / 1024, rely=470 / 600, height=80, width=300)

        # ***************************************Other widgets*********************************************
        recipeScroll = ttk.Scrollbar(self)
        recipeScroll.place(height=420, width=25, relx=610 / 1024, rely=130 / 600)
        recipeList = tk.Listbox(self, yscrollcommand=recipeScroll.set, font=headerFont)
        for i in range(6):
            recipeList.insert(i, (recipeArray[0][i]))
        recipeList.place(height=420, width=250, relx=360 / 1024, rely=130 / 600)
        recipeScroll.config(command=recipeList.yview)
        drinkDesc = tk.Text(self, height=13.4, font=headerFont)
        drinkDesc.place(relx=680 / 1024, rely=130 / 600, height=300, width=300)

        # ***************************************Functions*********************************************
        def onSelect(evt):
            ev = evt.widget
            global index2
            index2 = int(ev.curselection()[0])
            global drinkName
            drinkName = ev.get(index2)
            for i in range(6):
                if drinkName == recipeArray[0][i]:
                    drinkDesc.delete('1.0', tk.END)
                    drinkDesc.insert(tk.END, drinkName + "\n\nIngredients:\n")
                    drinkDesc.insert(tk.END, recipeArray[8][i] + "\n")

        def resetAll():
            self.destroy()  # destroys the canvas and therefore all of its child-widgets too

        def clear():
            checkSort()

        recipeList.bind('<<ListboxSelect>>', onSelect)

        def checkSort():
            temp = rvar.get()
            for k in range(6):
                recipeList.delete(k)
                recipeList.insert(k, (recipeArray[0][k]))
            temp = rvar.get()
            print(cb_labels[1][temp])
            for i in range(len(list(cb_labels[1][temp]))):
                if int(list(str(cb_labels[1][temp]))[i]) == 1:
                    for j in reversed(range(6)):
                        if int(list(str(recipeArray[1][j]))[i]) != 1:
                            recipeList.delete(j)

        def set_cb():
            for m in range(6):
                if option_labels[m] not in cb_labels[0]:
                    if option_labels[m] != '':
                        cb_labels[0][m] = option_labels[m]

            cb_labels[0].sort(reverse=True)
            print(cb_labels[0])

            for e in range(6):
                if cb_labels[0][e] == 'Vodka':
                    cb_labels[1][e] = "100000"
                elif cb_labels[0][e] == "Triple Sec":
                    cb_labels[1][e] = "000010"
                elif cb_labels[0][e] == "Rum":
                    cb_labels[1][e] = "010000"
                elif cb_labels[0][e] == "Lime":
                    cb_labels[1][e] = "000001"
                elif cb_labels[0][e] == "Cranberry":
                    cb_labels[1][e] = "000100"
                elif cb_labels[0][e] == "Coke":
                    cb_labels[1][e] = "001000"

            print(cb_labels[1])

            if cb_labels[0][0] != "0":
                C1 = tk.Radiobutton(self, text=cb_labels[0][0], font=fatFingerFont, bg='gray24', value=0,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C1.place(width=265, height=40, relx=.04, rely=185 / 600)
            if cb_labels[0][1] != "0":
                C2 = tk.Radiobutton(self, text=cb_labels[0][1], font=fatFingerFont, bg='gray24', value=1,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C2.place(width=265, height=40, relx=.04, rely=245 / 600)
            if cb_labels[0][2] != "0":
                C3 = tk.Radiobutton(self, text=cb_labels[0][2], font=fatFingerFont, bg='gray24', value=2,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C3.place(width=265, height=40, relx=.04, rely=305 / 600)
            if cb_labels[0][3] != "0":
                C4 = tk.Radiobutton(self, text=cb_labels[0][3], font=fatFingerFont, bg='gray24', value=3,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C4.place(width=265, height=40, relx=.04, rely=365 / 600)
            if cb_labels[0][4] != "0":
                C5 = tk.Radiobutton(self, text=cb_labels[0][4], font=fatFingerFont, bg='gray24', value=4,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C5.place(width=265, height=40, relx=.04, rely=425 / 600)
            if cb_labels[0][5] != "0":
                C6 = tk.Radiobutton(self, text=cb_labels[0][5], font=fatFingerFont, bg='gray24', value=5,
                                    fg='gray99', variable=rvar, command=lambda: checkSort())
                C6.place(width=265, height=40, relx=.045, rely=485 / 600)

        set_cb()

        def choice():
            # find whats been selected
            for t in recipeList.curselection():
                # print(select_from.get(t))
                select = recipeList.get(t)
                return select

        def confirm_pour_func():
            if choice():
                if messagebox.askquestion("Confirm", "Do you want to dispense this selection?") == "yes":
                    pourFunc(event=confirm_pour_func)
            else:
                tk.messagebox.showerror("Selection", "Select a drink")

        def findLowTime():
            high = 0
            for i in range(6):
                if dispense[i] > high:
                    high = dispense[i]
            low = high
            for j in range(6):
                if (0 < dispense[j]) and (dispense[j] < low):
                    low = dispense[j]
            return low

        def dispenseFluid():
            dispenseTime = findLowTime()
            print(dispenseTime)
            while (dispenseTime > 0):
                for j in range(6):
                    if dispense[j] > 0:
                        dispense[j] = dispense[j] - dispenseTime
                        # bays[j].on()
                        print("bay " + str(j) + " is on")
                sleep(dispenseTime)
                for l in range(6):
                    if dispense[l] == 0:
                        # bays[l].off()
                        print("bay " + str(l) + " is off")
                dispenseTime = findLowTime()
                print(dispenseTime)

        def pourFunc(event):
            # python side
            for i in range(6):
                if recipeArray[0][i] == drinkName:
                    for each in range(6):
                        if list(recipeArray[1][i])[each] == '1':
                            count = int(options[num_bays][each])
                            if count > 1:
                                meas = recipeArray[each+2][i] / count
                                for every in range(6):
                                    if list(options[bay_id][each])[every] == '1':
                                        dispense[every] = meas
                            elif count == 1:
                                dispense[each] = recipeArray[each+2][i]
            dispense[6] = 8
            print(dispense)
            dispenseFluid()
            clear()
            controller.show_frame(p1)



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
        led_menu = tk.Button(self, text="LED Menu", font=fatFingerFont, bg='gray50', command=lambda: msg_box()) #command=lambda: controller.show_frame(p#)
        led_menu.place(relx=650 / 1024, rely=345 / 600, height=150, width=250)

        def msg_box():
            tk.messagebox.showerror("Sorry", "Sorry, this feature is still under development!")


class p5(tk.Frame):  # inventory menu
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='gray28')
        self.bays = ImageTk.PhotoImage(Image.open('tv_of_bays.png'))
        headerFont = tkFont.Font(family='Bell Gothic Std Light', size=30)
        fatFingerFont = tkFont.Font(family='Bell Gothic Std Light', size=20)

        #*************************local vars**************************
        inv_label = {}
        list_start = 325
        prime_bay = {}
        cb_var1 = tk.IntVar()
        cb_var2 = tk.IntVar()
        cb_var3 = tk.IntVar()
        cb_var4 = tk.IntVar()
        cb_var5 = tk.IntVar()
        cb_var6 = tk.IntVar()
        cb_vars = [cb_var1, cb_var2, cb_var3, cb_var4, cb_var5, cb_var6]
        instructions = "1) Select ingredient\n2) Select bay(s)\n" \
                       "3) Click \"Update\n    Inventory\""

        # **************************Canvas***************************
        bay_view = Canvas(self, bg="gray50", height=400, width=400, highlightthickness=0)
        bay_view.create_image(200, 200, image=self.bays)
        bay_view.place(relx=282 / 1024, rely=130 / 600)
        # self.bay_view = tk.Label(self, image=self.bays)
        # self.bay_view.place(relx=80 / 1024, rely=128 / 600)

        #*************************Buttons**************************
        backSettings = ttk.Button(self, text="← Back to Settings", command=lambda: controller.show_frame(p4))
        backSettings.place(x=0, y=0, height=60, width=225)
        set_inv = tk.Button(self, text="Update Inventory", font=fatFingerFont, bg='gray50',
                            command=lambda: upd_inv_confirm())
        set_inv.place(relx=695 / 1024, rely=460 / 600, height=70, width=275)
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
        C1.place(width=50, height=30, relx=512 / 1024, rely=183 / 600)
        C2.place(width=50, height=30, relx=565 / 1024, rely=279 / 600)
        C3.place(width=50, height=30, relx=512 / 1024, rely=373 / 600)
        C4.place(width=50, height=30, relx=399 / 1024, rely=373 / 600)
        C5.place(width=50, height=30, relx=349 / 1024, rely=279 / 600)
        C6.place(width=50, height=30, relx=402 / 1024, rely=183 / 600)

        #**************************Labels***************************
        inv_header = ttk.Label(self, text="Inventory Control", font=headerFont, background='gray28',
                                     foreground='gray99')
        inv_header.place(relx=340 / 1024, rely=40/600, width=400)
        ingredients = ttk.Label(self, text="Ingredients: Choose one \nfor the selected bays", font=fatFingerFont,
                                background='gray28', foreground='gray99')
        ingredients.place(relx=695 / 1024, rely=120/600, width=350)
        current_inv = ttk.Label(self, text="Current Inventory:", font=fatFingerFont, background='gray28',
                                     foreground='gray99')
        current_inv.place(relx=60/1024, rely=290/600)
        instruct = ttk.Label(self, text=instructions, font=fatFingerFont, background='gray28',
                                foreground='gray99')
        instruct.place(relx=60 / 1024, rely=120 / 600)

        #**************************other widgets***************************
        select_from_scroll = ttk.Scrollbar(self)
        select_from_scroll.place(height=250, width=25, relx=945 / 1024, rely=190 / 600)
        select_from = tk.Listbox(self, yscrollcommand=select_from_scroll.set, font=fatFingerFont)
        for i in range(6):
            select_from.insert(i, (options[1][i]))
        select_from.place(height=250, width=250, relx=695 / 1024, rely=190 / 600)
        #select_from_scroll.config(command=options.yview)

        #**************************functions***************************
        def set_labels():
            for x in range(6):
                bottle = "Bay " + str(x + 1) + ": " + option_labels[x]
                inv_label[x] = ttk.Label(self, text="", font=fatFingerFont, background='gray28',
                                            foreground='gray99')
                inv_label[x].config(text="")
                inv_label[x].config(text=bottle)
                inv_label[x].place(relx=60 / 1024, rely=(list_start + (x * 35)) / 600)
        set_labels()

        def clear():
            cb_var1.set(0)
            cb_var2.set(0)
            cb_var3.set(0)
            cb_var4.set(0)
            cb_var5.set(0)
            cb_var6.set(0)

        def choice():
            # find whats been selected
            for t in select_from.curselection():
                # print(select_from.get(t))
                select = select_from.get(t)
                return select

        def bay_choice():
            for i in range(6):
                if cb_vars[i].get() == 1:
                    return True

        def upd_inv_confirm():
            if bay_choice():
                if choice():
                    if messagebox.askquestion("Confirm", "Is there a cup under the dispenser for priming?") == "yes":
                        upd_inv(event=set_inv)
                    else:
                        tk.messagebox.showinfo("Cancel", "Cancel inventory update")
                else:
                    tk.messagebox.showerror("Selection", "Select an ingredient")
            else:
                tk.messagebox.showerror("Selection", "Select bay(s)")

        def upd_inv(event):
            #*******************internal
            chosen = choice()

            #set up the labels and priming
            for bay in range(6):
                #print(cb_vars[n].get())
                if cb_vars[bay].get() == 1:
                    prime_bay[bay] = 1
                    option_labels[bay] = chosen
                else:
                    prime_bay[bay] = 0

            #modify the options lists
            for it in range(6):
                if options[1][it] == chosen:
                    if options[3][it] == 'false':
                        options[3][it] = "true"
                    options[4][it] = option_labels.count(chosen)
                    options[5][it] = ""
                    for digit in prime_bay:
                        options[5][it] += str(prime_bay[digit])
                elif options[1][it] not in option_labels:
                    options[3][it] = "false"
                    options[4][it] = 0
                    options[5][it] = "000000"
                else:
                    #if something is in labels array, update count and binary array for placement
                    options[4][it] = option_labels.count(options[1][it])
                    temp = ""
                    for c in range(6):
                        if list(options[5][it])[c] == str(prime_bay[c]):
                            #set digit to opposite
                            temp += "0"
                        else:
                            temp += list(options[5][it])[c]
                    options[5][it] = temp
                    print(temp)

            #*******************file io
            with open(inv_file, 'w', newline='') as inv:
                csvwriter = csv.writer(inv)
                # for each row...
                csvwriter.writerows(options)

            #*******************arduino comm
            priming = ["", "", "", "", "", ""]
            newline = "\n"

            for i in range(6):
                priming[i] = str(prime_bay[i])
                priming[i] = priming[i] + newline
                print(options[i])


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
