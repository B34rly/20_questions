import sqlite3
con = sqlite3.connect('data.db')
cur = con.cursor()

import gi
gi.require_version("Gtk","3.0")
from gi.repository import Gtk

animal_columns = {"Name":"",
        "Legs Count": [0,2,4,6,8],
        "Tail": [True, False],
        "Diet Type": ["Carnivore", "Herbivore", "Omnivore"],
        "Normal Pet": [True, False],
        "Skin Type": ["Scales", "Fur", "Skin", "Exoskeleton"],
        "Barks": [True, False],
        "Habitat": ["Aquatic", "Terrestrial", "Avian", "Amphibious"]
        }
animal_columnKeys = list(animal_columns.keys())

fruit_columns = {
        "Name":"",
        "Single Seed": [True, False],
        "Edible Skin": [True, False],
        "Type": ["Pome", "Drupe", "Berry", "Aggregate", "Melon", "Citrus"],
        "Colour": ["Red", "Orange", "Blue", "Yellow", "Green"],
        "Grown On": ["Tree", "Bush", "Vine", "Stolon"]
        }
fruit_columnKeys = list(fruit_columns.keys())

columns = {
        "Name": "",
        "Fruit or Animal": ["Fruit", "Animal"]
        } 
columnKeys = None

cur.execute("SELECT * from animals ORDER BY name;")
animal_data = cur.fetchall()

cur.execute("SELECT * from fruit ORDER BY name;")
fruit_data = cur.fetchall()
print(fruit_data)
data = None
useFruitData = None

names = []
for i in fruit_data:
    names.append([i[1],"Fruit"])
for i in animal_data:
    print(i)
    names.append([i[1], "Animal"])
print(names)
def diff(x,y):
    if x > y:
        return (x-y)
    else:
        return (y-x)

def range_mean(quantities):
    total = 0 
    smallestDiff = 100
    mostPolarizingIndex = 0
    print("In RANGE MEAN")
    for i in quantities:
        total += i
    print("Total ", total)
    for i in quantities:
        print(i)
        elimQuantity = diff(i, total)
        print(elimQuantity)
        if elimQuantity < smallestDiff and elimQuantity != total and elimQuantity != 0:
            smallestDiff = elimQuantity
            mostPolarizingIndex = quantities.index(i)
    if len(quantities) == 2:
        mostPolarizingIndex = 0
    return (mostPolarizingIndex, smallestDiff)

def biggest_differentiator(currentData):
    print(columns)
    variables = len(columns)
    fruitsLeft = len(currentData)

    target = (fruitsLeft//2)
    smallestDiffIndex = (0,0) 
    smallestDiff = 50

    for i in range(0, variables):
        trueCount = 0
        valuesSeparated = []
        amountOfEachValue = []
        for j in currentData: 
            valuesSeparated.append(j[i])

        for k in columns.get(columnKeys[i]):
            amountOfEachValue.append(valuesSeparated.count(k))
        trueCount = range_mean(amountOfEachValue) 
        print(columnKeys[i])
        print(trueCount[1])
        print(diff(trueCount[1], target))
        if diff(trueCount[1], target) < smallestDiff:
            smallestDiff = diff(trueCount[1], target)
            smallestDiffIndex = [i, trueCount[0]]
    print(smallestDiffIndex)
    return tuple(smallestDiffIndex)

class mainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Aiden - 20 Questions")
        self.grid = Gtk.Grid(column_homogeneous = True,
                column_spacing = 10,
                row_spacing = 10,
                margin = 10)
        self.datatableLbl = Gtk.Label(use_markup=True, label="<big><b>Datatable</b></big>")
        self.datatableInfoLbl = Gtk.Label(label="Choose a fruit or animal from the datatable below! For accurate findings, please double check the answer with the datatable before selecting!")

        # self.valueStore = Gtk.ListStore(str, int, bool, str, bool, str, bool, str)
        self.valueStore = Gtk.ListStore(str, str)
        self.treeView = Gtk.TreeView(model = self.valueStore)
        self.treeView.set_hexpand(True)
        self.treeView.set_vexpand(True)

        self.scrollableView = Gtk.ScrolledWindow()
        self.scrollableView.set_vexpand(True)
        self.scrollableView.add(self.treeView)

        self.questionLbl = Gtk.Label(use_markup=True, label="<big><b>Loading...</b></big>")
        self.qTopic = ("Fruit", "") 
        self.qTopicIndex = (0,0)

        self.yesBtn = Gtk.Button(label="Yes")
        self.yesBtn.connect("clicked", self.yes)
        self.noBtn = Gtk.Button(label="No")
        self.noBtn.connect("clicked", self.no)

        self.grid.attach(self.datatableLbl, 0,0,2,1)
        self.grid.attach(self.datatableInfoLbl, 0,1,2,1)
        self.grid.attach(self.scrollableView,0,2,2,1)
        self.grid.attach(self.questionLbl,0,3,2,1)
        self.grid.attach(self.noBtn, 0,4,1,1)
        self.grid.attach(self.yesBtn,1,4,1,1)

        self.add(self.grid)

        for row in self.valueStore:
            print(row[:])
        
        self.reset()

    def reset(self, chosenFruit=False):
        global useFruitData
        if not chosenFruit:
            useFruitData = None
        if useFruitData == None:
            self.valueStore = Gtk.ListStore(str, str)
            
            for column in self.treeView.get_columns():
                self.treeView.remove_column(column)
            columns = {
                "Name": "",
                "Fruit or Animal": ["Fruit", "Animal"]
                }

            for i, column_title in enumerate(columns):
                renderer = Gtk.CellRendererText()
                column = Gtk.TreeViewColumn(column_title, renderer, text=i)
                self.treeView.append_column(column)

            self.treeView.set_model(self.valueStore)
            for name in names:
                self.valueStore.append(name)

            self.questionLbl.set_label("<big><b>Is it a fruit</b></big>")
        else:
            for row in self.valueStore:
                self.valueStore.remove(row.iter)
            print(data)
            for fruit in data:
                self.valueStore.append(fruit[1:])
        self.update()

    def update(self):
        if useFruitData != None:
            if len(self.valueStore) > 1:
                self.qTopicIndex = biggest_differentiator(self.valueStore)
                self.qTopic = (columnKeys[self.qTopicIndex[0]],columns.get(columnKeys[self.qTopicIndex[0]])[self.qTopicIndex[1]])
                qTopic = self.qTopic[0]
                qTopicAnswer = self.qTopic[1]
                
                print("when")
                match qTopic:
                    case "Fruit":
                        self.questionLbl.set_label("<big><b>Is it a fruit or an animal?</b></big>")
                    case "Name":
                        self.questionLbl.set_label("<big><b>Is your chosen animal {}?</b></big>".format(self.valueStore[0][columns.index(self.qTopic)]))
                    case "Legs Count":
                        self.questionLbl.set_label(f"<big><b>Does your chosen animal have {qTopicAnswer} legs?</b></big>")
                    case "Tail":
                        self.questionLbl.set_label("<big><b>Does your animal have a tail?</b></big>")
                    case  "Diet Type":
                        self.questionLbl.set_label(f"<big><b>Is your animal {'an' if (qTopicAnswer[0] in 'AOEUI') else 'a'} {qTopicAnswer}?</b></big>")
                    case "Normal Pet":
                        self.questionLbl.set_label("<big><b>Is your animal a normal pet? If you're not sure, check the data table above.</b></big>")
                    case "Skin Type":
                        self.questionLbl.set_label(f"<big><b>Does your animal have {qTopicAnswer}?</b></big>")
                    case "Barks":
                        self.questionLbl.set_label("<big><b>Does your animal bark?</b></big>")
                    case "Habitat":
                        self.questionLbl.set_label(f"<big><b>Is your animal {qTopicAnswer}?</b></big>")
                    case "Single Seed":
                        self.questionLbl.set_label(f"<big><b>Does your fruit have only one seed?</b></big>")
                    case "Edible Skin":
                        self.questionLbl.set_label("<big><b>Do you eat your fruit's skin?</b></big>")
                    case "Type":
                        self.questionLbl.set_label(f"<big><b>Is your fruit {'an' if (qTopicAnswer[0] in 'AOEUI') else 'a'} {qTopicAnswer}?</b></big>")
                    case "Colour":
                        self.questionLbl.set_label(f"<big><b>Is your fruit normally {qTopicAnswer} once ripe?</b></big>")
                    case "Hand Peeled":
                        self.questionLbl.set_label("<big><b>Do you need more than just your hands to peel your fruit?</b></big>")
                    case "Grown On":
                        self.questionLbl.set_label(f"<big><b>Does your fruit grow on a {qTopicAnswer}?</b></big>")
            else:
                self.questionLbl.set_label(f"<big><b>Based on your answers, your chosen animal is {'an' if (self.valueStore[0][0][0] in 'AOEUI') else 'a'} {self.valueStore[0][0]}! Click \"Yes\" when you would like to restart.</b></big>")
        else:
            self.questionLbl.set_label("<big><b>Is it a fruit?</b></big>")

    def delete(self, column, inverse):
        qTopicIndex = columnKeys.index(self.qTopic[0])
        ifFruit = self.valueStore[0][qTopicIndex]
        for row in self.valueStore:
             if self.qTopic[0] != "Name":
                 if bool(row[qTopicIndex] == self.qTopic[1])== inverse:
                    self.valueStore.remove(row.iter)
             else:
                 print(row[columns.index(self.qTopic)])
                 print(ifFruit)
                 print(bool(row[columns.index(self.qTopic)] == [0][columns.index(self.qTopic)]))
                 if bool(row[qTopicIndex] == ifFruit) == inverse:
                     self.valueStore.remove(row.iter)
        self.update()

    def setFruitOrAnimals(self, fruitOrNot):
        global useFruitData
        global data
        global columns
        global columnKeys
        useFruitData = fruitOrNot
        for column in self.treeView.get_columns():
            self.treeView.remove_column(column)

        if useFruitData:
            columns = fruit_columns
            columnKeys = fruit_columnKeys
            data = fruit_data
            self.valueStore = Gtk.ListStore(str, bool, bool, str, str, str ) #whatever complete fruit data!
        else:
            columns = animal_columns
            columnKeys = animal_columnKeys
            data = animal_data
            self.valueStore = Gtk.ListStore(str, int, bool, str, bool, str, bool, str)

        for i, column_title in enumerate(columns):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.treeView.append_column(column)
        self.treeView.set_model(self.valueStore)
        self.reset(True)

    def yes(self, widget):
        if useFruitData != None:
            if len(self.valueStore) > 1:
                self.delete(self.qTopic, False)
            else:
                self.reset()
        else:
            self.setFruitOrAnimals(True)

    def no(self, widget):
        if useFruitData != None:
            if len(self.valueStore) > 1:
                self.delete(self.qTopic, True)
        else:
            self.setFruitOrAnimals(False)

win = mainWindow()
win.connect("destroy",Gtk.main_quit)
win.show_all()
Gtk.main()
