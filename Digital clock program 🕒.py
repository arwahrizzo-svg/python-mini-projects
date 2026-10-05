# Import necessary system and PyQt5 modules
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont, QFontDatabase


# Define the main window class for the digital clock inheriting from QWidget
class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        # Create a label widget to display the time string
        self.time_label = QLabel(self)
        # Create a timer object to trigger updates at regular intervals
        self.timer = QTimer(self)
        # Initialize the User Interface components and layout
        self.initUI()

    def initUI(self):
        # Set the window title
        self.setWindowTitle("Digital Clock")
        # Set window position (X=600, Y=400) and initial size (Width=300, Height=100)
        self.setGeometry(600, 400, 300, 100)

        # Create a vertical box layout to structure widgets vertically
        vbox = QVBoxLayout()
        # Add the time label to the layout
        vbox.addWidget(self.time_label)
        # Apply the layout to the main window
        self.setLayout(vbox)

        # Center the text alignment inside the label both horizontally and vertically
        self.time_label.setAlignment(Qt.AlignCenter)
        # Style the time label with a large font size and neon green color using CSS
        self.time_label.setStyleSheet("font-size: 150px;" "color: hsl(111,100%,50%);")
        # Set the main window background color to black
        self.setStyleSheet("background-color: black;")

        # Load the custom digital font file from the project directory
        font_id = QFontDatabase.addApplicationFont("DS-DIGIT.TTF")
        # Retrieve the font family name from the loaded font ID
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # Create a QFont object using the loaded family name at 150pt size
        my_font = QFont(font_family, 150)
        # Apply the custom digital font to the time label
        self.time_label.setFont(my_font)

        # Connect the timer's timeout signal to the update_time method
        self.timer.timeout.connect(self.update_time)
        # Start the timer to trigger every 1000 milliseconds (1 second)
        self.timer.start(1000)
        # Call update_time immediately so the clock displays the time without a 1-second delay
        self.update_time()

    def update_time(self):
        # Get the current system time and format it as 12-hour format with AM/PM (e.g., 01:51:23 PM)
        current_time = QTime.currentTime().toString("hh:mm:ss AP")
        # Update the text of the label with the formatted time string
        self.time_label.setText(current_time)

    # Ensure the script only runs when executed directly, not when imported as a module


if __name__ == "__main__":
    # Initialize the application instance passing command-line arguments
    app = QApplication(sys.argv)
    # Create an instance of the DigitalClock window
    clock = DigitalClock()
    # Render the window visible on screen
    clock.show()
    # Start the application's main event loop and exit the script when closed
    sys.exit(app.exec_())
