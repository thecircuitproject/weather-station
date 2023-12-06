import network
import urequests
from machine import Pin, I2C
from time import sleep
from key import wifi_key, weather_api_key
from AHT import AHT20
from ssd1306 import SSD1306_I2C

API_KEY = weather_api_key
SSID = wifi_key["ssid"]
PASSWORD = wifi_key["password"]
LAT = "14.605291"
LON = "-90.671337"

sda_sensor = Pin(16)
scl_sensor = Pin(17)
i2c_sensor = I2C(id=0, scl=scl_sensor, sda=sda_sensor, freq=40_000)
sensor = AHT20(i2c_sensor)

sda_oled = Pin(14)
scl_oled = Pin(15)
i2c_screen = I2C(id=1, scl=scl_oled, sda=sda_oled)
display = SSD1306_I2C(128, 64, i2c_screen)

led = Pin(13, Pin.OUT)


def connect() -> str:
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while wlan.isconnected() == False:
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")
    return ip


def get_request() -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={
        LAT}&lon={LON}&appid={API_KEY}&units=metric"
    request = urequests.get(url)
    weather_info = request.json()
    request.close()

    return weather_info


def get_weather(json_response: dict) -> dict[str, str | dict]:
    country = json_response["sys"]["country"]
    temp = json_response["main"]
    city = json_response["name"]

    return {
        "city": city,
        "temp": temp,
        "country": country,
    }


def display_metrics(weather: dict[str, str | dict], sensor: AHT20) -> None:
    for _ in range(15):
        display.fill(0)
        display.show()
        display.text("Weather Station", 0, 5)
        display.text(f"Outside:{weather['temp']['temp']} C", 0, 16)
        display.text(f"Feels:{weather['temp']['feels_like']} C", 0, 26)
        display.text(f"Inside:{sensor.temperature():.2f} C", 0, 36)
        display.text(f"Outside:{weather['temp']['humidity']} %", 0, 46)
        display.text(f"Inside:{sensor.relative_humidity():.2f} %", 0, 56)
        display.show()
        sleep(1)


def initialize(ip: str) -> None:
    if ip:
        led.on()
        display.text("Connected", 25, 25)
        display.text("to WiFi", 35, 35)
        display.show()
        led.off()


def main() -> None:
    led.off()
    ip = connect()
    initialize(ip)

    while True:
        weather_info = get_request()
        weather = get_weather(weather_info)
        display_metrics(weather, sensor)


if __name__ == "__main__":
    main()
