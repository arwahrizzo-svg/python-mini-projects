import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

# Define the main application class inheriting from QWidget
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize UI elements (labels, input fields, and buttons)
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        
        # Set up the user interface layout and styling
        self.initUI()

    def initUI(self):
        # Configure the main window properties
        self.setWindowTitle("Weather app☀️")
        self.setFixedSize(450, 600)

        # Create a vertical box layout to stack widgets on top of each other
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        # Apply the layout to the main widget
        self.setLayout(vbox)

        # Center-align the text inside all labels and input fields
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Set Object Names to target specific elements in the stylesheet (CSS)
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Define CSS-like styles for custom fonts, sizing, and specific layouts
        self.setStyleSheet("""
            QLabel, QPushButton {
                font-family: calibri;
            }
            QLabel#city_label {
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input {
                font-size: 40px;
            }
            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label {
                font-size: 70px;
            }
            QLabel#emoji_label {
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label {
                font-size: 50px;
            }
        """)

        # Connect the button click event to the get_weather function
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        # API credentials and target URL setup
        api_key = "7aff9f4222bc408dfc496424d0c90347"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            # Send an HTTP GET request to OpenWeatherMap
            response = requests.get(url)
            # Raise an exception if the server returned an error status code
            response.raise_for_status()
            # Parse the API response into a Python dictionary
            data = response.json()
            
            # If the response code indicates success, display the weather data
            if data["cod"] == 200:
                self.display_weather(data)
                
        except requests.exceptions.HTTPError as http_error:
            # Handle specific HTTP error status codes gracefully
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API Key")
                case 403:
                    self.display_error("Forbidden:\nAccess denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal server error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred\n{http_error}")
                    
        except requests.exceptions.ConnectionError:
            print("Connection error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            print("Timeout error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            print(f"Request error:\n{req_error}")

    def display_error(self, message):
        # Shrink font size dynamically to make sure the error message fits on the screen
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        # Clear out obsolete weather details when an error occurs
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        # Reset the temperature label size back to its standard display size
        self.temperature_label.setStyleSheet("font-size: 75px;")
        
        # Extract temperature data (API defaults to Kelvin) and convert to Celsius
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        
        # Extract the condition ID and text description
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        # Update the UI labels with the fetched details
        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        # Map OpenWeatherMap's condition codes to specific emojis
        if 200 <= weather_id <= 232:
            return "⛈️"  # Thunderstorm
        elif 300 <= weather_id <= 321:
            return "🌦️"  # Drizzle
        elif 500 <= weather_id <= 531:
            return "🌧️"  # Rain
        elif 600 <= weather_id <= 622:
            return "❄️"  # Snow
        elif 701 <= weather_id <= 741:
            return "🌫️"  # Atmosphere / Fog
        elif weather_id == 762:
            return "🌋"   # Volcanic Ash
        elif weather_id == 771:
            return "💨"   # Squall
        elif weather_id == 781:
            return "🌪️"  # Tornado
        elif weather_id == 800:
            return "☀️"   # Clear sky
        elif 801 <= weather_id <= 804:
            return "☁️"   # Clouds
        else:
            return ""    # Fallback default empty string

# Execution checkpoint ensuring the script only runs if executed directly
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
