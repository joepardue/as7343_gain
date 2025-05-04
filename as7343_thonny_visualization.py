# spectral_color_display.py - Color bar graph display for AS7343
import board
import time
import as7343

# ANSI color codes that work in your terminal
COLORS = {
    'RESET': '\033[0m',
    'VIOLET': '\033[95m',  # Magenta as violet
    'BLUE': '\033[94m',    # Blue  
    'CYAN': '\033[96m',    # Cyan
    'GREEN': '\033[92m',   # Green
    'YELLOW': '\033[93m',  # Yellow
    'RED': '\033[91m',     # Red
    'WHITE': '\033[97m',   # White for clear
    'GRAY': '\033[90m',    # Gray for dim values
}

# Channel wavelength to color mapping
CHANNEL_COLORS = {
    'F2_425nm': 'VIOLET',
    'FZ_450nm': 'BLUE',
    'F3_475nm': 'BLUE',
    'F4_515nm': 'CYAN',
    'FY_555nm': 'GREEN', 
    'FXL_600nm': 'YELLOW',
    'F6_640nm': 'RED',
    'NIR_855nm': 'RED',
    'VIS': 'WHITE',
    'VIS2': 'WHITE',
    'VIS3': 'WHITE', 
    'VIS4': 'WHITE'
}

def color_bar(value, max_value=65535, width=50, color='RESET'):
    """Create a colored bar graph"""
    if max_value == 0:
        max_value = 1
    
    # Calculate bar length
    bar_length = int((value / max_value) * width)
    bar_length = max(0, min(bar_length, width))
    
    # Create the bar using block characters
    bar = '█' * bar_length
    empty = '░' * (width - bar_length)
    
    # Apply color
    color_code = COLORS.get(color, COLORS['RESET'])
    reset = COLORS['RESET']
    
    # Format with value
    return f"{color_code}{bar}{empty}{reset} {value:5d}"

def display_spectrum(sensor):
    """Display a single spectral reading with colored bars"""
    channels = sensor.all_channels
    
    # Calculate max value for scaling
    spectral_channels = ['F2_425nm', 'FZ_450nm', 'F3_475nm', 'F4_515nm',
                        'FY_555nm', 'FXL_600nm', 'F6_640nm', 'NIR_855nm']
    spectral_values = [channels[ch] for ch in spectral_channels]
    max_value = max(spectral_values) if spectral_values else 1
    
    # Print header
    print(f"\n=== Spectral Reading (max: {max_value}) ===")
    print(f"Gain: {sensor.gain}x | Integration: {sensor.integration_time_ms:.1f}ms")
    print("-" * 60)
    
    # Display spectral channels
    for channel in spectral_channels:
        value = channels[channel]
        color = CHANNEL_COLORS[channel]
        bar = color_bar(value, max_value, 40, color)
        print(f"{channel:10s} {bar}")
    
    # Display clear channels
    print("\nClear channels:")
    clear_channels = ['VIS', 'VIS2', 'VIS3', 'VIS4']
    clear_max = max([channels[ch] for ch in clear_channels]) if clear_channels else 1
    
    for channel in clear_channels:
        value = channels[channel]
        color = CHANNEL_COLORS[channel]
        bar = color_bar(value, clear_max, 40, color)
        print(f"{channel:10s} {bar}")

# Main program
def main():
    i2c = board.STEMMA_I2C()
    
    try:
        sensor = as7343.AS7343(i2c)
        print("AS7343 sensor initialized!")
        
        # Configure sensor
        sensor.set_gain(16)
        sensor.set_integration_time_ms(100)
        
        print("\nStarting continuous spectral display...")
        print("Press Ctrl+C to stop")
        
        while True:
            display_spectrum(sensor)
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exception(type(e), e, e.__traceback__)

if __name__ == "__main__":
    main()
