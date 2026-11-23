from PySide6.QtWidgets import QApplication,QWidget,QPushButton
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

    def show_about(self):
        self.about_window.show()

if __name__ == '__main__':
    app=QApplication()
    window = MainWindow()
    window.show()
    app.exec()
