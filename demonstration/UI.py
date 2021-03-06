# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sympy as sy
import os
from functions import fun1, fun2, fun3, fun4, fun5, fun6, fun7, fun8

# os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"
from Powell2D import display


def getFunctionName(fun):
    x, y = sy.symbols('x y')
    z = fun(x, y)
    return z


class Ui_display(object):
    def __init__(self, X, Y, function, X0):
        self.display = None
        self.X = X
        self.Y = Y
        self.function = function
        self.X0 = X0
        self.app = QtWidgets.QApplication(sys.argv)
        widget = QtWidgets.QWidget()
        self.generator = None
        self.content = None

        self.setupUi(widget)
        widget.show()
        sys.exit(self.app.exec_())

    def setupUi(self, display):
        self.display = display
        display.setObjectName("display")
        display.resize(573, 698)
        display.setStyleSheet(""
                              "QPushButton {"
                              "    color: black ;"
                              "    font-size:25px;"
                              "    border:1px dotted #4a1491;"
                              "}"
                              "*{"
                              "    font-family:楷体;"
                              "    font-size:30px;"
                              "    color: #1d649c;"
                              "}"
                              "QDialog { "
                              "    background-color: white "
                              "}"
                              "QPushButton:hover {"
                              "    color: red;"
                              "    border:1px solid #1d649c; }"
                              "")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(display)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.line_2 = QtWidgets.QFrame(display)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_3.addWidget(self.line_2)
        self.box_function_name = QtWidgets.QGroupBox(display)
        self.box_function_name.setObjectName("box_function_name")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.box_function_name)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.function_name = QtWidgets.QLineEdit(self.box_function_name)
        self.function_name.setObjectName("function_name")
        self.verticalLayout_2.addWidget(self.function_name)
        self.verticalLayout_3.addWidget(self.box_function_name)
        self.line = QtWidgets.QFrame(display)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_3.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.box_content = QtWidgets.QGroupBox(display)
        self.box_content.setObjectName("box_content")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.box_content)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit = QtWidgets.QPlainTextEdit(self.box_content)
        self.textEdit.setObjectName("textEdit")
        self.horizontalLayout.addWidget(self.textEdit)
        self.horizontalLayout_2.addWidget(self.box_content)
        self.line_4 = QtWidgets.QFrame(display)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_2.addWidget(self.line_4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.button_begin = QtWidgets.QPushButton(display)
        self.button_begin.setObjectName("button_begin")
        self.verticalLayout.addWidget(self.button_begin)
        self.button_next = QtWidgets.QPushButton(display)
        self.button_next.setObjectName("button_next")
        self.verticalLayout.addWidget(self.button_next)
        self.button_clear = QtWidgets.QPushButton(display)
        self.button_clear.setObjectName("button_clear")
        self.verticalLayout.addWidget(self.button_clear)
        self.button_finish = QtWidgets.QPushButton(display)
        self.button_finish.setObjectName("button_finish")
        self.verticalLayout.addWidget(self.button_finish)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.line_3 = QtWidgets.QFrame(display)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_3.addWidget(self.line_3)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        # button
        self.button_finish.clicked.connect(self.display.close)
        self.button_begin.clicked.connect(self.begin)
        self.button_next.clicked.connect(self.clickNext)
        # set text
        function_name = getFunctionName(self.function)
        self.function_name.setText(str(function_name).replace('**', '^').replace('*', ''))
        self.function_name.setEnabled(False)
        self.retranslateUi(display)
        QtCore.QMetaObject.connectSlotsByName(display)

    def begin(self):
        self.generator = display(self.X, self.Y, self.function, X0=self.X0)
        self.content = next(self.generator)

    def clickNext(self):
        self.content = next(self.generator)
        if self.content == '':
            self.textEdit.clear()
        elif self.content == 'result':
            self.textEdit.clear()
        else:
            self.textEdit.appendPlainText(self.content)

    def retranslateUi(self, display):
        _translate = QtCore.QCoreApplication.translate
        display.setWindowTitle(_translate("display", "Form"))
        self.box_function_name.setTitle(_translate("display", "函数表达式："))
        self.box_content.setTitle(_translate("display", "步骤内容输出："))
        self.button_begin.setText(_translate("display", "开始"))
        self.button_next.setText(_translate("display", "下一步"))
        self.button_clear.setText(_translate("display", "清空输出内容"))
        self.button_finish.setText(_translate("display", "结束"))


if __name__ == "__main__":
    object = Ui_display((-5, 7), (-5, 7), fun2, X0=[-5, 4])  # fun2, fun5, fun6
