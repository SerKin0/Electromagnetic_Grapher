import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from mydesign import Ui_MainWindow


class MyWindow(QtWidgets.QMainWindow):
    count = 0

    def __init__(self, *args, **kwargs):
        super(MyWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.btnClicked)

        layout = QVBoxLayout()
        self.ui.widget.setLayout(layout)
        self.canvas = FigureCanvasQTAgg(Figure())
        layout.addWidget(self.canvas)

    def btnClicked(self):
        file_name = QFileDialog.getOpenFileName(None, "Open File", ".", "Text Files (*.txt);;All Files (*)")[0]

        if not file_name:  # Если файл не был загружен, то ...
            print("Ошибка чтения файла")  # Выводим сообщение об ошибке в консоль и в виде окна
            QMessageBox.warning(None, "Ошибка загрузки", "Файл не загружен.")
        else:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    input_mass = f.readlines()
                    print(f"\ninput_mass - {file_name}: {input_mass}")
                    output_mass = [list(map(float, i.replace("\n", "").replace(",", ".").split()))
                                   for i in input_mass]
                    print(f"output_mass - {file_name}: {output_mass}")
                    MyWindow.create_graphe(self, output_mass)
            except ValueError:
                QMessageBox.warning(None, "Ошибка чтения данных",
                                    f'В файле некорректно введены значения массива. Проверьте на наличие букв или '
                                    f'других символов, отличных от цифр.')
                print("Ошибка размера или значений массива")

    def create_graphe(self, mass: list):
        fig = self.canvas.figure
        fig.clear()
        ax = fig.add_subplot(111)

        title = "Цветовая карта поперечной структуры излучения\n" \
                f"count_X = {len(mass[0])}, count_Y = {len(mass)}."
        ax.set_title(title)
        im = ax.imshow(mass, origin="lower", extent=(0, 140, 0, 140), interpolation="none", cmap="Greys")
        cbar = fig.colorbar(im)
        cbar.set_label('Значение')
        ax.set_xlabel("Координата сканирования по оси x, мм")
        ax.set_ylabel("Координата сканирования по оси y, мм")
        fig.savefig(f"result/{len(mass[0])}-{len(mass)}")

        if MyWindow.count == 0:
            toolbar = NavigationToolbar(self.canvas, self)
            layout = self.ui.widget.layout()
            layout.addWidget(toolbar)
        MyWindow.count += 1

        self.canvas.draw()


app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
sys.exit(app.exec())
