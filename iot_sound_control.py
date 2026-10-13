from gpiozero import DigitalInputDevice
from time import sleep, time
import requests

urls = ("http://192.168.1.6/", "http://192.168.1.3/")
sound_sensor = DigitalInputDevice(14)

MAX_CLAP_INTERVAL = 0.40
MIN_CLAP_INTERVAL = 0.20

def iot_control(command):
    for url in urls:
        try:
            requests.get(
                url + command,
                timeout = 5
            )
            print("Success")
        except requests.exceptions.RequestException as e:
            print("Failed")

def main():
    try:
        while True:
            sound_sensor.wait_for_active()
            first_clap_time = time()
            sleep(MIN_CLAP_INTERVAL)

            double_clap = False

            while time() - first_clap_time < MAX_CLAP_INTERVAL:
                if sound_sensor.is_active:
                    double_clap = True
                    print(first_clap_time, time())
                    break
                sleep(0.01)

            if double_clap:
                print("Double Clap")
                iot_control("off")
            else:
                print("Single Clap")
                iot_control("on")
            sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting...")

if __name__ == "__main__":
    main()
