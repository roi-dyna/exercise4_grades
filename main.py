from PySide6.QtWidgets import QApplication,QWidget,QPushButton,QLabel,QLineEdit,QTableWidget
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

        self.update_button = QPushButton('Update File', self)
        self.update_button.setGeometry(180, 20, 140, 35)

        self.about_button = QPushButton('About', self)
        self.about_button.setGeometry(460, 20, 120, 35)
        self.about_button.clicked.connect(self.show_about)

        self.bonus_label = QLabel('Bonus Points:', self)
        self.bonus_label.setGeometry(20, 75, 100, 30)

        self.bonus_input = QLineEdit(self)
        self.bonus_input.setGeometry(120, 75, 100, 30)

        self.table = QTableWidget(50, 3, self)
        self.table.setGeometry(20, 125, 560, 350)
        self.table.setHorizontalHeaderLabels(['ID', 'Original Grades', 'Corrected Grades'])

    def show_about(self):
        self.about_window.show()

if __name__ == '__main__':
    app=QApplication()
    window = MainWindow()
    window.show()
    app.exec()
