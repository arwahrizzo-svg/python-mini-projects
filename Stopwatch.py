# Python PyQt5 Stopwatch
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import QTimer, QTime, Qt

class StopWatch(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize the baseline time structure at 0 hours, minutes, seconds, and milliseconds
        self.time = QTime(0, 0, 0, 0)
        self.time_label = QLabel("00:00:00.00", self)
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.reset_button = QPushButton("reset")
        # Create a timer instance to drive the background loop cycles
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
       self.setWindowTitle("Stopwatch")

       # Set up the main vertical box layout container
       vbox = QVBoxLayout()
       vbox.addWidget(self.time_label)

       # Place control buttons vertically into the primary layout
       vbox.addWidget(self.start_button)
       vbox.addWidget(self.stop_button)
       vbox.addWidget(self.reset_button)

       self.setLayout(vbox)
       self.time_label.setAlignment(Qt.AlignCenter)

       # Group the buttons into a horizontal row container
       hbox = QHBoxLayout()
       hbox.addWidget(self.start_button)
       hbox.addWidget(self.stop_button)
       hbox.addWidget(self.reset_button)

       # Nest the horizontal layout directly into the vertical window architecture
       vbox.addLayout(hbox)

       # Apply custom CSS styling for layout boundaries, spacing, and HSL colors
       self.setStyleSheet("""
          QPushButton, QLabel{ padding: 20px;
                               font-weight: bold;
                               font-family: calibri;
          } 
          QPushButton{ font-size: 50px;
                       background-color: hsl(34, 80%, 50%);
          }
          QLabel{ font-size: 120px;
                  background-color: hsl(34, 80%, 80%);
                  border-radius: 20px;
          }
       """)
       # Connect button interactions and timing events to their respective logic methods
       self.start_button.clicked.connect(self.start)
       self.stop_button.clicked.connect(self.stop)
       self.reset_button.clicked.connect(self.reset)
       self.timer.timeout.connect(self.update_display)

    def start(self):
        # Fire background timeout flags precisely every 10 milliseconds
        self.timer.start(10)

    def stop(self):
        # Freeze active background loops instantly to pause runtime calculation
        self.timer.stop()

    def reset(self):
       # Turn off the active countdown track and restore parameters to defaults
       self.timer.stop()
       self.time = QTime(0, 0, 0, 0)
       self.time_label.setText(self.format_time(self.time))

    def format_time(self, time):
        # Extract individual runtime components to generate display labels
        hours = self.time.hour()
        minutes = self.time.minute()
        seconds = self.time.second()
        # Truncate raw 3-digit millisecond loops down to 2 digits for rendering
        milliseconds = self.time.msec() // 10
        # Return a zero-padded text string conforming to "HH:mm:ss.zz" formats
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}"

    def update_display(self):
        # Advance the core calculation instance by adding 10 milliseconds per tick
        self.time = self.time.addMSecs(10)
        self.time_label.setText(self.format_time(self.time))


if __name__ == "__main__":
    # Configure underlying framework bindings and pass window configurations live
    app = QApplication(sys.argv)
    stopwatch = StopWatch()
    stopwatch.show()
    sys.exit(app.exec_())
