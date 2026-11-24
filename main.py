import os
import platform
import subprocess

from PySide6.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QLineEdit,QTableWidget, QFileDialog,QTableWidgetItem,QHeaderView
from PySide6.QtGui import QIntValidator, QColor
from About import AboutWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Grades Fixer')
        self.setGeometry(100,100,600,500)
        with open(os.path.join(os.path.dirname(__file__), 'style.qss'), 'r') as style_file:
            self.setStyleSheet(style_file.read())

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.about_window= AboutWindow()

        self.load_button = QPushButton('Load CSV', self)
        self.load_button.setGeometry(20, 20, 140, 35)
        self.load_button.clicked.connect(self.load_file)
        self.load_button.setObjectName('primaryBtn')

        self.update_button = QPushButton('Update File', self)
        self.update_button.setGeometry(180, 20, 140, 35)
        self.update_button.clicked.connect(self.update_file)
        self.update_button.setObjectName('successBtn')

        self.about_button = QPushButton('About', self)
        self.about_button.setGeometry(460, 20, 120, 35)
        self.about_button.clicked.connect(self.show_about)
        self.about_button.setObjectName('secondaryBtn')

        self.bonus_label = QLabel('Bonus Points:', self)
        self.bonus_label.setGeometry(20, 75, 100, 30)

        self.bonus_input = QLineEdit(self)
        self.bonus_input.setGeometry(120, 75, 100, 30)
        self.bonus_input.returnPressed.connect(self.apply_bonus)
        self.bonus_input.setValidator(QIntValidator(-100, 100))

        self.stats_label = QLabel('Avg: -  |  Pass: -', self)
        self.stats_label.setGeometry(240, 75, 340, 30)

        self.table = QTableWidget(50, 3, self)
        self.table.setGeometry(20, 125, 560, 350)
        self.table.setHorizontalHeaderLabels(['ID', 'Original Grades', 'Corrected Grades'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(28)

    def show_about(self):
        self.about_window.show()


    def load_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select Grades File', '', 'CSV Files (*.csv)')
        if not filename:
            return

        self.selected_file = filename
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.table.clearContents()
        self.bonus_input.clear()

        with open(self.selected_file, 'r') as f:
            self.header = next(f)
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split(',')
                self.student_ids.append(parts[0])
                grade = int(parts[1])
                self.original_grades.append(grade)
                self.corrected_grades.append(grade)

        self.update_table()

    def update_table(self):
        if len(self.student_ids) == 0:
            return

        orig_pass = 0
        corr_pass = 0

        for i in range(len(self.student_ids)):
            id_item = QTableWidgetItem(str(self.student_ids[i]))
            orig_item = QTableWidgetItem(str(self.original_grades[i]))
            corr_item = QTableWidgetItem(str(self.corrected_grades[i]))

            if self.original_grades[i] < 60:
                orig_item.setBackground(QColor('#fee2e2'))
            else:
                orig_item.setBackground(QColor('#dcfce7'))
                orig_pass += 1

            if self.corrected_grades[i] < 60:
                corr_item.setBackground(QColor('#fee2e2'))
            else:
                corr_item.setBackground(QColor('#dcfce7'))
                corr_pass += 1

            self.table.setItem(i, 0, id_item)
            self.table.setItem(i, 1, orig_item)
            self.table.setItem(i, 2, corr_item)

        orig_avg = sum(self.original_grades) / len(self.original_grades)
        corr_avg = sum(self.corrected_grades) / len(self.corrected_grades)
        total = len(self.student_ids)
        self.stats_label.setText(f'Avg: {orig_avg:.1f} → {corr_avg:.1f}  |  Pass: {orig_pass}/{total} → {corr_pass}/{total}')
    
    def apply_bonus(self):
        text = self.bonus_input.text()
        if not text or text == '-':
            return
        bonus = int(text)

        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + bonus
            if new_grade > 100:
                new_grade = 100
            elif new_grade < 0:
                new_grade = 0
            self.corrected_grades[i] = new_grade

        self.update_table()

    def update_file(self):
        if not self.selected_file:
            return

        with open(self.selected_file, 'w') as f:
            f.write(self.header)
            for i in range(len(self.student_ids)):
                f.write(f'{self.student_ids[i]},{self.corrected_grades[i]}\n')

        if platform.system() == 'Windows':
            os.startfile(self.selected_file)
        elif platform.system() == 'Darwin':
            subprocess.Popen(['open', self.selected_file])
        else:
            subprocess.Popen(['xdg-open', self.selected_file])

if __name__ == '__main__':
    app=QApplication()
    window = MainWindow()
    window.show()
    app.exec()
