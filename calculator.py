#!/usr/bin/python
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class Calculator(QWidget):

    def __init__(self):
        super(Calculator, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Calculator")
        self.move(90, 50)
        grid = QGridLayout()
        self.line = QLineEdit()
        self.result = ""
        names = [["7", "8", "9", "/"],
                 ["4", "5", "6", "*"],
                 ["1", "2", "3", "-"],
                 ["0", ".", "=", "+"]]
        self.buttons = [[] for i in range(4)]
        for i in range(4):
            for j in range(4):
                self.buttons[i].append(QPushButton(names[i][j]))
                grid.addWidget(self.buttons[i][j], i, j)
                self.buttons[i][j].pressed.connect(lambda t=names[i][j]: self.writeLine(t))
        clear = QPushButton("Clear")
        clear.clicked.connect(self.clearAction)
        grid.addWidget(self.line, 4, 0, 1, 3)
        grid.addWidget(clear, 4, 3)
        self.setLayout(grid)
        self.show()
        self.setFocus()

    def clearAction(self):
        self.line.clear()
        self.result = ""

    def keyPressEvent(self, event):
        keys = [[Qt.Key_7, Qt.Key_8, Qt.Key_9, Qt.Key_Slash],
                [Qt.Key_4, Qt.Key_5, Qt.Key_6, Qt.Key_Asterisk],
                [Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_Minus],
                [Qt.Key_0, Qt.Key_Period, Qt.Key_Equal, Qt.Key_Plus]]
        if event.key() in [Qt.Key_Enter, Qt.Key_Return]:
            self.buttons[3][2].pressed.emit()
        elif event.key() == Qt.Key_Comma:
            self.buttons[3][1].pressed.emit()
        elif event.key() == Qt.Key_Backspace:
            self.backspaceAction()
        else:
            for i in range(4):
                for j in range(4):
                    if event.key() == keys[i][j]:
                        self.buttons[i][j].pressed.emit()
                        break

    def backspaceAction(self):
        content = str(self.line.text())
        if "error" in content:
            self.clearAction()
        elif "=" in content:
            self.line.setText(content[0:content.index("=")])
        elif len(content) > 1:
            self.line.setText(content[0:len(content)-1])
        else:
            self.line.setText("")

    def writeLine(self, text):
        content = str(self.line.text())
        if content != "" and text == "=":
            if "=" in content:
                content = content[0:content.index("=")]
            self.evaluate(content)
            content += text + self.result
        if content == "" and text not in ["/", "*"]:
            content = text
        elif self.result != "" and text != "=":
            if text.isdigit() == True or text == ".":
                self.result = ""
                content = text
            else:
                content = self.result + text
                self.result = ""
        else:
            content += text
        self.line.setText(content.rstrip("="))
        self.setFocus()

    def evaluate(self, content):
        operation = content.replace("/", " / ")
        operation = operation.replace("*", " * ")
        operation = operation.replace("-", " - ")
        operation = operation.replace("+", " + ")
        operation = operation.replace("(", " ( ")
        operation = operation.replace(")", " ) ")
        cols = []
        for col in operation.split(" "):
            if col.strip() != "":
                cols.append(col.strip())
        operation = ""
        for col in cols:
            if col.isdigit() == True:
                operation += col + ".0"
            else:
                operation += col
        try:
            aux = eval(operation)
            if float(int(aux)) == float(aux):
                aux = int(aux)
            self.result = str(aux)
        except SyntaxError:
            self.result = "error: bad syntax"
        except NameError:
            self.result = "error: bad syntax"
        except ZeroDivisionError:
            self.result = "error: division by 0"

app = QApplication(sys.argv)
calc = Calculator()
sys.exit(app.exec_())
