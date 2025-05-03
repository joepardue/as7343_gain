import time
import board
from as7343 import AS7343, GAIN_1X, GAIN_4X, GAIN_64X, GAIN_2048X

i2c = board.STEMMA_I2C()
sensor = AS7343(i2c)

def print_data(label, data):
    print(f"\n{label}")
    for k in sorted(data.keys()):
        print(f"{k:>5}: {data[k]}")
    print("-" * 30)

print("\n=== AS7343 Gain Verification ===")
input("Test 1: FIXED LIGHT, VARY GAIN.\nPlace flashlight in fixed position. Press Enter to begin...")

for gain, label in [(GAIN_1X, "GAIN 1X"), (GAIN_4X, "GAIN 4X"), (GAIN_64X, "GAIN 64X")]:
    print(f"\nSetting gain to {label}...")
    sensor.set_gain(gain)
    time.sleep(0.5)
    data = sensor.read_all()
    print_data(label, data)

input("\nTest 2: FIXED GAIN, VARY LIGHT.\nSet gain to 4X. Cycle through DARK ➜ LOW ➜ FULL light.\nPress Enter to begin...")
sensor.set_gain(GAIN_4X)

for label in ["Dark", "Low Light", "Flashlight On"]:
    input(f"\nReady to read in condition: {label} — press Enter when stable.")
    data = sensor.read_all()
    print_data(f"{label} (Gain 4X)", data)

input("\nTest 3: SATURATION CHECK.\nSet gain to 2048X. Shine flashlight directly.\nPress Enter when ready...")
sensor.set_gain(GAIN_2048X)
data = sensor.read_all()
print_data("GAIN 2048X - Bright Flashlight", data)

print("\nAll tests complete.")
