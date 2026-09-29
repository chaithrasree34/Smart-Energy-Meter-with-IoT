# Smart-Energy-Meter-with-IoT
import time
import requests
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------

THINGSPEAK_API_KEY = "YOUR_API_KEY"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

POWER_LIMIT = 2000       # Watts
UPDATE_INTERVAL = 15     # seconds

# -----------------------------
# Simulated sensor function
# Replace this with PZEM-004T
# sensor reading code
# -----------------------------

def read_energy_meter():
    """
    Replace these values with actual
    PZEM-004T sensor readings.
    """

    voltage = 230.0
    current = 4.2
    power = voltage * current

    return voltage, current, power


# -----------------------------
# Calculate energy
# -----------------------------

total_energy = 0.0
previous_time = time.time()


def calculate_energy(power):
    global total_energy, previous_time

    current_time = time.time()

    elapsed_hours = (current_time - previous_time) / 3600

    energy = power * elapsed_hours / 1000

    total_energy += energy

    previous_time = current_time

    return total_energy


# -----------------------------
# Send data to ThingSpeak
# -----------------------------

def send_to_thingspeak(voltage, current, power, energy):

    data = {
        "api_key": THINGSPEAK_API_KEY,
        "field1": voltage,
        "field2": current,
        "field3": power,
        "field4": energy
    }

    try:
        response = requests.get(
            THINGSPEAK_URL,
            params=data,
            timeout=10
        )

        if response.status_code == 200:
            print("Data uploaded successfully")

        else:
            print("Upload failed")

    except requests.RequestException as error:
        print("Internet error:", error)


# -----------------------------
# Save data locally
# -----------------------------

def save_data(voltage, current, power, energy):

    with open("energy_log.csv", "a") as file:

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        file.write(
            f"{now},{voltage:.2f},"
            f"{current:.2f},{power:.2f},"
            f"{energy:.6f}\n"
        )


# -----------------------------
# Main program
# -----------------------------

print("Smart Energy Meter Started")
print("--------------------------------")

while True:

    voltage, current, power = read_energy_meter()

    energy = calculate_energy(power)

    print("\nTime:", datetime.now())
    print("Voltage :", round(voltage, 2), "V")
    print("Current :", round(current, 2), "A")
    print("Power   :", round(power, 2), "W")
    print("Energy  :", round(energy, 4), "kWh")

    # Overload detection
    if power > POWER_LIMIT:
        print("WARNING: High power consumption!")

    # Store locally
    save_data(
        voltage,
        current,
        power,
        energy
    )

    # Upload to IoT
    send_to_thingspeak(
        voltage,
        current,
        power,
        energy
    )

    time.sleep(UPDATE_INTERVAL)
