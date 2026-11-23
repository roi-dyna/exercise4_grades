from PySide6.QtWidgets import QApplication,QWidget
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


if __name__ == '__main__':
    app=QApplication()
    window = MainWindow()
    window.show()
    app.exec()
