from PySide6.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QLineEdit,QTableWidget, QFileDialog,QTableWidgetItem
from About import AboutWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Grades Fixer')
        self.setGeometry(100,100,600,500)

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.about_window= AboutWindow()
        self.load_button = QPushButton('Load CSV', self)
        self.load_button.setGeometry(20, 20, 140, 35)
        self.load_button.clicked.connect(self.load_file)

        self.update_button = QPushButton('Update File', self)
        self.update_button.setGeometry(180, 20, 140, 35)

        self.about_button = QPushButton('About', self)
        self.about_button.setGeometry(460, 20, 120, 35)
        self.about_button.clicked.connect(self.show_about)

        self.bonus_label = QLabel('Bonus Points:', self)
        self.bonus_label.setGeometry(20, 75, 100, 30)

        self.bonus_input = QLineEdit(self)
        self.bonus_input.setGeometry(120, 75, 100, 30)
        self.bonus_input.returnPressed.connect(self.apply_bonus)

        self.table = QTableWidget(50, 3, self)
        self.table.setGeometry(20, 125, 560, 350)
        self.table.setHorizontalHeaderLabels(['ID', 'Original Grades', 'Corrected Grades'])

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

        with open(self.selected_file, 'r') as f:
            next(f)
            for line in f:
                parts = line.strip().split(',')
                self.student_ids.append(parts[0])
                grade = int(parts[1])
                self.original_grades.append(grade)
                self.corrected_grades.append(grade)

        self.update_table()

    def update_table(self):
        for i in range(len(self.student_ids)):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.student_ids[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.original_grades[i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.corrected_grades[i])))
    
    def apply_bonus(self):
        text = self.bonus_input.text()
        if not text:
            return
        bonus = int(text)

        for i in range(len(self.original_grades)):
            new_grade = self.original_grades[i] + bonus
            if new_grade > 100:
                new_grade = 100
            self.corrected_grades[i] = new_grade

        self.update_table()

if __name__ == '__main__':
    app=QApplication()
    window = MainWindow()
    window.show()
    app.exec()
