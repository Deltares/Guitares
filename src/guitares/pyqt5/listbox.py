from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore
import traceback

class ListBox(QListWidget):

    def __init__(self, element, parent, gui):
        super().__init__(parent)

        self.element = element
        self.parent  = parent
        self.gui     = gui

        self.add_items()

        # Adjust list value types
        if element["select"] == "item":
            if not type(self.element["option_value"]) == dict:
                for i, val in enumerate(element["option_value"]):
                    if element["type"] == float:
                        element["option_value"][i] = float(val)
                    elif element["type"] == int:
                        element["option_value"][i] = int(val)

        x0, y0, wdt, hgt = gui.get_position(element["position"], parent)

        self.setGeometry(x0, y0, wdt, hgt)

        if element["text"]:
            label = QLabel(element["text"], parent)
            fm = label.fontMetrics()
            wlab = int(fm.size(0, element["text"]).width())
            if element["text_position"] == "above-center" or element["text_position"] == "above":
                label.setAlignment(QtCore.Qt.AlignCenter)
                label.setGeometry(x0, int(y0 - 20 * gui.resize_factor), wdt, int(20 * gui.resize_factor))
            elif element["text_position"] == "above-left":
                label.setAlignment(QtCore.Qt.AlignLeft)
                label.setGeometry(x0, int(y0 - 20 * gui.resize_factor), wlab, int(20 * gui.resize_factor))
            else:
                # Assuming left
                label.setAlignment(QtCore.Qt.AlignRight)
                label.setGeometry(int(x0 - wlab - 3 * gui.resize_factor), int(y0 + 5 * gui.resize_factor), wlab, int(20 * gui.resize_factor))

            label.setStyleSheet("background: transparent; border: none")

            self.text_widget = label


        # First call back to change the variable
        fcn = lambda: self.first_callback()
        self.clicked.connect(fcn)

        if element["module"] and "method" in element:
            if hasattr(element["module"], element["method"]):
                self.callback = getattr(element["module"], element["method"])
                fcn2 = lambda: self.second_callback()
                self.clicked.connect(fcn2)
            else:
                print("Error!. Listbox method " + element["method"] + " does not exist.")

    def set(self):

            # First check if items need to be updated. This is only necessary when "option_string" is a dict
            if type(self.element["option_string"]) == dict:
                self.add_items()

            # Get the items
            items = []
            for x in range(self.count()):
                items.append(self.item(x))

            # Get value
            val = self.gui.getvar(self.element["variable_group"], self.element["variable"])

            # Now get the values
            if self.element["select"] == "item":
                if type(self.element["option_value"]) == dict:
                    name  = self.element["option_value"]["variable"]
                    group = self.element["option_value"]["variable_group"]
                    vals = self.gui.getvar(group, name)
                    if not vals:
                        vals = [""]
                else:
                    vals = self.element["option_value"]

                if val in vals:
                    index = vals.index(val)
                else:
                    index = 0
                    print(self.element["variable"] + ' not found !')

            else:
                index = val

            self.setCurrentItem(items[index])

    def first_callback(self):
        index = self.widgets[0].currentRow()
        if self.element["select"] == "item":
            if type(self.element["option_value"]) == dict:
                name = self.element["option_value"]["variable"]
                group = self.element["option_value"]["variable_group"]
                vals = self.gui.getvar(group, name)
                if not vals:
                    vals = [""]
            else:
                vals = self.element["option_value"]
            newval = vals[index]
        else:
            newval = index

        name  = self.element["variable"]
        group = self.element["variable_group"]
        self.gui.setvar(group, name, newval)

    def second_callback(self):
        try:
            if self.okay and self.isEnabled():
                group = self.element["variable_group"]
                name  = self.element["variable"]
                val   = self.gui.getvar(group, name)
                self.callback(val, self)
                # Update GUI
                self.gui.update()
        except:
            traceback.print_exc()

    def add_items(self):

        # Delete existing items
        self.clear()

        if type(self.element["option_string"]) == dict:
            group = self.element["option_string"]["variable_group"]
            name  = self.element["option_string"]["variable"]
            v     = self.gui.getvar(group, name)
            if not v:
                v = [""]
            for itxt, txt in enumerate(v):
                self.insertItem(itxt, txt)
        else:
            for itxt, txt in enumerate(self.element["option_string"]):
                self.insertItem(itxt, txt)
