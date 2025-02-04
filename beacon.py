import requests
import time
import ssl
import random
import logging
import warnings
from urllib3.exceptions import InsecureRequestWarning
import socket

# Suppress SSL warnings
warnings.simplefilter('ignore', InsecureRequestWarning)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Specify the source IP address for the beacon (you can modify this as needed)
src_ip = '192.168.80.222'  # Example source IP (change to your desired IP)


# C2 server URL (you can modify this to the actual server you're targeting)
C2_SERVER_URL = [
    "https://1c27eace-eb71-4548-8e0d-0c711ce2c699.cloudsecurity.ninja/beacon",
    "https://60bc6420-c2ef-49f0-86e1-8cea63070032.cloudsecurity.ninja/beacon",
    "https://716316b6-6836-4bb5-8cab-c5c94236952e.cloudsecurity.ninja/beacon",
    "https://www.cloudsecurity.ninja/beacon"
]

# Payload to send
PAYLOAD = "{beacon:fire away!}"

# Time interval between beacons (in seconds)
BEACON_INTERVAL = 30  # 30 seconds as an example

# Create a session that binds to the specified source address
def session_for_src_addr(addr: str) -> requests.Session:
    """
    Create a `Session` which will bind to the specified local address
    """
    session = requests.Session()
    for prefix in ('http://', 'https://'):
        session.get_adapter(prefix).init_poolmanager(
            connections=requests.adapters.DEFAULT_POOLSIZE,
            maxsize=requests.adapters.DEFAULT_POOLSIZE,
            # This binds to the specified IP address
            source_address=(addr, 0),
        )
    return session


# Simulate the beacon
def send_beacon(src_ip: str):
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

        # Randomly select one of the C2 server URLs
        selected_URL = random.choice(C2_SERVER_URL)

        # Create the session that binds to the given source IP address
        session = session_for_src_addr(src_ip)

        # Send POST request to the C2 server, skipping SSL verification
        response = session.post(selected_URL, json=data, headers=headers, verify=False)

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
        send_beacon(src_ip)
        time.sleep(BEACON_INTERVAL)


if __name__ == "__main__":
    main()
