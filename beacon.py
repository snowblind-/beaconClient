import requests
import time
import ssl
import random
import logging
import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress SSL warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# C2 server URL (you can modify this to the actual server you're targeting)
C2_SERVER_URL = [
    "https://mycommand.f5.com/beacon",
    "https://mocommand1.f5.com/beacon",
    "https://mocommand2.f5.com/beacon",
    "https://mocommand0.f5.com/beacon"
]

# Payload to send
PAYLOAD = "{beacon:fire away!}"

# Time interval between beacons (in seconds)
BEACON_INTERVAL = 30  # 30 seconds as an example

# Simulate the beacon
def send_beacon():
    try:
        # Randomizing the headers slightly to avoid detection
        headers = {
            "User-Agent": f"CustomUserAgent/{random.randint(1, 100)}",
            "Content-Type": "application/json"
        }

        # Payload data that is sent to the C2 server
        data = {
            "payload": PAYLOAD
        }

        selected_URL = random.choice(C2_SERVER_URL)
        # Send POST request to the C2 server, skipping SSL verification
        response = requests.post(selected_URL, json=data, headers=headers, verify=False)

        # Log the response from the server
        if response.status_code == 200:
            logging.info("Beacon sent successfully. Server Response: %s", response.text)
        else:
            logging.warning("Failed to send beacon. Status Code: %d, Response: %s", response.status_code, response.text)

    except requests.exceptions.RequestException as e:
        logging.error("Error sending beacon: %s", e)

# Main function to repeatedly send beacons
def main():
    logging.info("Beacon script started.")
    while True:
        send_beacon()
        time.sleep(BEACON_INTERVAL)

if __name__ == "__main__":
    main()
