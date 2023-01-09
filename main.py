from holidaychecker import HolidayChecker
from PyQt5.QtWidgets import QApplication
import sys
from mainwindow import MainWindow


def main():
    spring_holiday_checker = HolidayChecker(
        "https://www.fit.edu/registrar/academic-calendar/spring-2023/")

    App = QApplication(sys.argv)

    # Used to create the instance of our Window
    window = MainWindow(App, spring_holiday_checker)

    window.open_app()

main()
