from datetime import datetime, timedelta
from PyQt5.QtWidgets import QDialog, QGridLayout, QGroupBox, QLabel,\
    QVBoxLayout, QComboBox, QPushButton, QHBoxLayout,\
    QLineEdit, QListWidget, QCalendarWidget, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate


class AppointmentBooker(QDialog):

    def __init__(self, holiday_check):
        super().__init__()
        self._holiday_class = holiday_check
        # Using a dictionary to store the data of {date:[appointments]}
        self.dates_dict = {}
        self.content = ""
        self.result = ""
        self.First = True

        # Used to organize the app
        grid = QGridLayout()
        grid.addWidget(self.header(), 0, 0, 1, 5)
        grid.addWidget(self.booking(), 2, 0, 1, 3)
        grid.addWidget(self.book_multiple_appointments(), 3, 0, 1, 3)
        grid.addWidget(self.current_bookings(), 1, 3, 3, 2)
        grid.addWidget(self.calendar_preview(), 1, 0, 1, 3)
        grid.setSpacing(15)

        self.setLayout(grid)
        self.setWindowTitle((" " * 90) + "Ziyad's Appointment Booker")
        self.setGeometry(450, 50, 1000, 900)


    # The "Highlighted" Section
    def header(self):
        group_box = QGroupBox()
        self.top_label = QLabel()
        self.top_label.setFont(QFont('Arial',15))
        self.top_label.setStyleSheet("color: black; background-color: SkyBlue;"
                                     " border-radius: 5px; padding: 10px;")
        vbox = QVBoxLayout()
        vbox.addWidget(self.top_label)
        group_box.setLayout(vbox)

        return group_box


    # The "Calendar Preview" Section
    def calendar_preview(self):
        group_box = QGroupBox("Calendar Preview")
        group_box.setStyleSheet("font-size: 15px;")
        self.calendar = QCalendarWidget()
        # lower bound date (Current Date)
        l_date = QDate().currentDate()
        # upper bound date (End FIT's Classes)
        u_date = QDate(2023, 5, 5)
        # setting date range
        self.calendar.setDateRange(l_date, u_date)
        self.calendar.clicked.connect(self.header_label)
        self.calendar.clicked.connect(self.show_list)
        self.date = self.calendar.selectedDate()
        self.date = self.date.toString("dddd, MMMM d, yyyy")
        self.top_label.setText(self.date)
        self.add_booking()
        self.update_list()
        vbox = QVBoxLayout()
        vbox.addWidget(self.calendar)

        group_box.setLayout(vbox)

        return group_box


    # Used to represent the date on the "Highlighted" Section in certain format
    def header_label(self):
        self.date = self.calendar.selectedDate()
        self.date = self.date.toString("dddd, MMMM d, yyyy")
        self.top_label.setText(self.date)


    # The "Book Single Appointment" Section
    def booking(self):
        group_box = QGroupBox("Book Single Appointment")
        group_box.setStyleSheet("font-size: 15px;")

        # Used to store the comboboxes data
        hour = [str(i+1) for i in range(12)]
        minutes = [str(i) for i in range(60)]
        meridiem = ["AM", "PM"]
        duration = ["10 minutes", "15 minutes", "20 minutes",
                    "25 minutes", "30 minutes"]

        self.hour_box = QComboBox()
        self.hour_box.addItems(hour)

        self.minutes_box = QComboBox()
        self.minutes_box.addItems(minutes)

        self.meridiem_box = QComboBox()
        self.meridiem_box.addItems(meridiem)

        self.duration_box = QComboBox()
        self.duration_box.addItems(duration)

        book_button = QPushButton("Book")
        book_button.pressed.connect(self.add_booking)
        book_button.pressed.connect(self.update_list)

        vbox = QHBoxLayout()
        vbox.addWidget(self.hour_box)
        vbox.addWidget(self.minutes_box)
        vbox.addWidget(self.meridiem_box)
        vbox.addWidget(self.duration_box)
        vbox.addWidget(book_button)
        vbox.setSpacing(50)

        group_box.setLayout(vbox)

        return group_box

    # Used to format the content
    def add_booking(self):
        data =  self.hour_box.currentText() + self.minutes_box.currentText() + \
                self.meridiem_box.currentText()

        time1 = datetime.strptime(data, "%I%M%p")
        time1_format = time1.strftime("%I:%M%p")

        duration = str(self.duration_box.currentText())[:2]
        time2 = time1 + timedelta(minutes=int(duration))
        time2_format = time2.strftime("%I:%M%p")

        self.content = time1_format + " - " + time2_format + "  " + \
                       self.duration_box.currentText()


    # The "Book Multiple Appointments" Section
    # The format should be: 6:30am - 7:00am, 7:00am - 7:15am, 7:20am - 7:30am
    def book_multiple_appointments(self):
        group_box = QGroupBox('Book Multiple Appointments (Ex. 6:30am - 7:00am, 7:00am - 7:15am)')
        group_box.setStyleSheet("font-size: 15px;")

        label = QLabel("Times: ")
        self.text_box = QLineEdit()
        book_button = QPushButton("Book")
        book_button.clicked.connect(self.multiple_appointments_format)

        vbox = QHBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(self.text_box)
        vbox.addWidget(book_button)

        group_box.setLayout(vbox)
        return group_box


    # Used to format the multiple appointments and update the list
    def multiple_appointments_format(self):
        # Used to get the text from the text box when the button is clicked
        value = self.text_box.text().split(",")
        test_list = [s.strip() for s in value]

        for items in test_list:
            self.content = self.format_multiple_appointments(items)
            self.update_list()
        self.text_box.clear()


    # The "Current Bookings" Section
    def current_bookings(self):
        group_box = QGroupBox("Current Bookings")
        group_box.setStyleSheet("font-size: 15px;")

        self.list_update = QListWidget()
        self.list_update.setStyleSheet("color: black; background-color: lightgray;"
                                       " border-radius: 5px; padding: 20px;"
                                       " font-size: 18px;")

        vbox = QVBoxLayout()
        vbox.addWidget(self.list_update)

        group_box.setLayout(vbox)

        return group_box


    # Used to update the list by using a dictionary when the user click "Book"
    def update_list(self):
        if self.First == True:
            self.First = False
            pass
        else:
            is_holiday_format = self.calendar.selectedDate()
            format_date = is_holiday_format.toString("MMM. d yyyy")
            self.holiday = self._holiday_class.is_holiday(format_date)

            # Used to format the date for the message boxes
            self.date_formated = self.calendar.selectedDate()
            self.date_formated = self.date_formated.toString("ddd,MMM d,yyyy ")

            if not(self.holiday):
                # If the dictionary contains the date, then just append the appointment
                if self.dates_dict.__contains__(self.date):
                    # Used to check if there is a conflict between the new appointment
                    # and the list's appointments. If so, do not put the new appointment
                    if self.is_conflict(self.dates_dict[self.date], self.content):
                        pass
                    else:
                        self.dates_dict[self.date].append(self.content)
                        self.successful_book()
                # If not, then update the dictionary
                # and add the new appointment with the selected date
                else:
                    self.dates_dict.update({self.date:[self.content]})
                    self.successful_book()

                self.list_update.clear()
                self.list_update.addItems(self.dates_dict[self.date])
            else:
                self.error_book()


    # Used to present the items on the "Current Bookings" section
    def show_list(self):
        self.list_update.clear()
        # Used to check if the dictionary contains items or not.
        if self.dates_dict.__contains__(self.date):
            # If so, present the items
            self.list_update.addItems(self.dates_dict[self.date])
        else:
            self.list_update.addItem("No appointments for the selected date")


    # Used to format the multiple appointments
    def format_multiple_appointments(self, time):
        # start time
        start_time = time[:6]
        end_time = time[9:]

        # convert time string to datetime
        t1 = datetime.strptime(start_time, "%I:%M%p")
        t2 = datetime.strptime(end_time, "%I:%M%p")

        time_difference = str(t2 - t1)

        t1_format = t1.strftime("%I:%M%p")
        t2_format = t2.strftime("%I:%M%p")

        return (t1_format + " - " + t2_format + "  " + time_difference[2:4] +
                " minutes")


    # Used to check if there is conflict between two times
    def is_conflict(self, check_list, check_time):
        given_time1 = datetime.strptime(check_time[:7], "%I:%M%p").time()
        given_time2 = datetime.strptime(check_time[10:17], "%I:%M%p").time()

        for i in range(len(check_list)):
            given_time3 = datetime.strptime(check_list[i][:7], "%I:%M%p").time()
            given_time4 = datetime.strptime(check_list[i][10:17], "%I:%M%p").time()

            if (given_time1 < given_time4 and given_time3 < given_time2):
                show_msg = QMessageBox(QMessageBox.Warning, "Error",
                                       "Sorry, there is a conflict!", QMessageBox.Ok)
                show_msg.exec_()
                return True
        return False

    # Used to format the successful statement
    def successful_book(self):
        self.result = ("An appointment for " + str(self.date_formated) +
                        self.content[:10] +
                        str(self.date_formated) +
                        self.content[10:17] + " was booked successfully")
        self.show_success_box()

    # Used to show the message in QMessageBox
    def show_success_box(self):
        show_msg = QMessageBox(QMessageBox.Information, "Success",
                               self.result, QMessageBox.Ok)
        show_msg.exec_()


    # Used to format the error statement
    def error_book(self):
        self.result = ("Sorry," + str(self.date_formated) +
                        self.content[:10] +
                        str(self.date_formated) +
                        self.content[10:17] + " is not available." + self.holiday)
        self.show_error_box()

    # Used to show the message in QMessageBox
    def show_error_box(self):
        show_msg = QMessageBox(QMessageBox.Warning, "Error",
                               self.result, QMessageBox.Ok)
        show_msg.exec_()
