from PySide6.QtWidgets import QApplication, QLineEdit, QMainWindow, QPushButton
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QWidget


class Button(QPushButton):
    def __init__(self, title: str):
        super().__init__()
        self.setText(title)
        self.setFixedSize(50, 50)

    def btn_pressed(self):
        self.text


class MainWindow(QMainWindow):
    waiting_for_operand = True

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Py-Calc")

        self.display = QLineEdit('0')
        self.btn_digits = []
        for i in range(10):
            self.btn_digits.append(Button(str(i)))
            self.btn_digits[i].clicked.connect(self.digit_clicked)
        self.btn_sep = Button(',')
        self.btn_sep.clicked.connect(self.seperator_clicked)
        self.btn_equal = Button('=')
        self.btn_add = Button('+')
        self.btn_sub = Button('-')
        self.btn_mul = Button('*')
        self.btn_div = Button('/')

        layout = QVBoxLayout()
        layout.addWidget(self.display)

        layout_btn = QGridLayout()
        for i in range(1, 10):
            row = (9 - i) // 3
            col = (i - 1) % 3
            layout_btn.addWidget(self.btn_digits[i], row, col)
        layout_btn.addWidget(self.btn_digits[0], 3, 0)
        layout_btn.addWidget(self.btn_sep, 3, 1)
        layout_btn.addWidget(self.btn_equal, 3, 2)
        layout_btn.addWidget(self.btn_add, 0, 3)
        layout_btn.addWidget(self.btn_sub, 1, 3)
        layout_btn.addWidget(self.btn_mul, 2, 3)
        layout_btn.addWidget(self.btn_div, 3, 3)

        layout.addLayout(layout_btn)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    """
    Responding to a digit button being pressed.
    Appends the corresponding digit to the display.
    """

    def digit_clicked(self, clicked):
        btn = self.sender()
        digit = int(btn.text())
        # 0 input is not recognized if no value is displayed
        if self.display.text() == "0" and digit == 0:
            return
        if self.waiting_for_operand:
            self.display.clear()
            self.waiting_for_operand = False
        self.display.setText(self.display.text() + btn.text())

    def seperator_clicked(self, clicked):
        if '.' in self.display.text():
            return
        self.display.setText(self.display.text() + '.')
        self.waiting_for_operand = False


def render_window(args: list) -> int:
    app = QApplication(args)
    window = MainWindow()
    window.show()
    return app.exec()
