from math import sqrt
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
    pending_add_operator = ""
    pending_mul_operator = ""
    sum_so_far = 0.0
    factor_so_far = 0.0

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
        self.btn_equal.clicked.connect(self.equal_clicked)
        self.btn_add = Button('+')
        self.btn_add.clicked.connect(self.add_op_clicked)
        self.btn_sub = Button('-')
        self.btn_sub.clicked.connect(self.add_op_clicked)
        self.btn_mul = Button('*')
        self.btn_mul.clicked.connect(self.mul_op_clicked)
        self.btn_div = Button('/')
        self.btn_div.clicked.connect(self.mul_op_clicked)
        self.btn_neg = Button('±')
        self.btn_neg.clicked.connect(self.unary_operator)
        self.btn_inv = Button('1/x')
        self.btn_inv.clicked.connect(self.unary_operator)
        self.btn_sqr = Button('x^2')
        self.btn_sqr.clicked.connect(self.unary_operator)
        self.btn_sqrt = Button('SQRT')
        self.btn_sqrt.clicked.connect(self.unary_operator)

        layout = QVBoxLayout()
        layout.addWidget(self.display)

        layout_btn = QGridLayout()
        for i in range(1, 10):
            row = (9 - i) // 3 + 1
            col = (i - 1) % 3
            layout_btn.addWidget(self.btn_digits[i], row, col)
        layout_btn.addWidget(self.btn_digits[0], 4, 1)
        layout_btn.addWidget(self.btn_inv, 0, 0)
        layout_btn.addWidget(self.btn_sqr, 0, 1)
        layout_btn.addWidget(self.btn_sqrt, 0, 2)
        layout_btn.addWidget(self.btn_neg, 4, 0)
        layout_btn.addWidget(self.btn_sep, 4, 2)
        layout_btn.addWidget(self.btn_equal, 4, 3)
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

    def unary_operator(self, clicked):
        btn_txt = self.sender().text()
        disp_txt = self.display.text()
        disp_val = float(disp_txt)
        if btn_txt == '±':
            disp_val *= -1
        if btn_txt == 'SQRT':
            if disp_val < 0.0:
                self._clear_all()
                return
            disp_val = sqrt(disp_val)
        elif btn_txt == 'x^2':
            disp_val *= disp_val
        elif btn_txt == '1/x':
            if disp_val == 0.0:
                return
            else:
                disp_val = 1.0 / disp_val
        self.display.setText(str(disp_val))
        self.waiting_for_operand = True

    def add_op_clicked(self):
        btn = self.sender().text()
        operand = float(self.display.text())
        if self.pending_mul_operator:
            if not self._calculate(operand, self.pending_mul_operator):
                self._clear_all()
                return
            self.display.setText(str(self.factor_so_far))
            operand = self.factor_so_far
            self.factor_so_far = 0.0
            self.pending_mul_operator = ""

        if self.pending_add_operator:
            if not self._calculate(operand, self.pending_add_operator):
                self._clear_all()
                return
            self.display.setText(str(self.sum_so_far))
        else:
            self.sum_so_far = operand

        self.waiting_for_operand = True
        self.pending_add_operator = btn

    def mul_op_clicked(self):
        btn = self.sender().text()
        operand = float(self.display.text())

        if self.pending_mul_operator:
            if not self._calculate(operand, self.pending_mul_operator):
                self._clear_all()
                return
            self.display.setText(str(self.factor_so_far))
        else:
            self.factor_so_far = operand

        self.waiting_for_operand = True
        self.pending_mul_operator = btn

    def equal_clicked(self):
        operand = float(self.display.text())

        if self.pending_mul_operator:
            if not self._calculate(operand, self.pending_mul_operator):
                self._clear_all()
                return
            operand = self.factor_so_far
            self.factor_so_far = 0.0
            self.pending_mul_operator = ""

        if self.pending_add_operator:
            if not self._calculate(operand, self.pending_add_operator):
                self._clear_all()
                return
            self.pending_add_operator = ""
        else:
            self.sum_so_far = operand

        self.display.setText(str(self.sum_so_far))
        self.sum_so_far = 0.0
        self.waiting_for_operand = True

    def _calculate(self, rightOp: float, pendingOp: str):
        if pendingOp == '+':
            self.sum_so_far += rightOp
        elif pendingOp == '-':
            self.sum_so_far -= rightOp
        elif pendingOp == '*':
            self.factor_so_far *= rightOp
        elif pendingOp == '/':
            if rightOp == 0:
                return False
            else:
                self.factor_so_far /= rightOp
        return True

    def _clear_all(self):
        self.sum_so_far = 0.0
        self.factor_so_far = 0.0
        self.display.setText('0')
        self.pending_add_operator = ''
        self.pending_mul_operator = ''
        self.waiting_for_operand = True


def render_window(args: list) -> int:
    app = QApplication(args)
    window = MainWindow()
    window.show()
    return app.exec()
