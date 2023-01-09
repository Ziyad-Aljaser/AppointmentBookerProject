from PyQt5.QtWidgets import QMainWindow
from appointmentbooker import AppointmentBooker
import sys

class MainWindow(QMainWindow):
    def __init__(self, App, spring_holiday_checker):
        super(MainWindow, self).__init__()
        self._app = App
        self.spring_holiday_checker = spring_holiday_checker


    def open_app(self):
        dialog = AppointmentBooker(self.spring_holiday_checker)
        dialog.show()
        sys.exit(self._app.exec_())

