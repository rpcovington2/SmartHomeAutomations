    import network
    import time
    from umqtt.simple import MQTTClient
    from neopixel import Neopixel
    import random
    import dht
    from machine import Pin, SoftI2C
    import ssd1306
    from ota import OTAUpdater
    from WIFI_CONFIG import SSID, PASSWORD
    import json
    import uasyncio as asyncio
    import framebuf

    # LOGO
    ronco_logo = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x31, 0x80, 0x10, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x87, 0xc4, 0x60, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x00, 0x03, 0x0f, 0x8d, 0x88, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0f, 0xc0, 0x44, 0x1f, 0x3a, 0x40, 0x00, 0x08, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x70, 0x18, 0x3c, 0x60, 0x00, 0x00, 0xe4, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00, 0x03, 0xff, 0xff, 0xe4, 0x3c, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x07, 0x00, 0x00, 0x00, 0x07, 0xf1, 0xff, 0xe0, 0x04, 0x24, 0x18, 0x00,
                            0x00, 0x00, 0x00, 0x60, 0x00, 0x00, 0x07, 0xff, 0x8f, 0x88, 0x00, 0x00, 0x7f, 0xe6, 0x00, 0x00,
                            0x00, 0x00, 0x04, 0x07, 0xff, 0xc7, 0xff, 0x80, 0x40, 0x38, 0x3f, 0xc0, 0xc0, 0x3b, 0x4c, 0x00,
                            0x00, 0x00, 0xc1, 0xf8, 0x00, 0x70, 0x00, 0x01, 0xe0, 0x68, 0x60, 0x31, 0x80, 0x0c, 0xb0, 0x00,
                            0x00, 0x06, 0x1f, 0x00, 0x00, 0x18, 0x7f, 0x83, 0x30, 0x40, 0xc0, 0x13, 0x00, 0x00, 0x1f, 0x80,
                            0x00, 0x0c, 0xe0, 0x00, 0x00, 0x18, 0xc0, 0x73, 0x08, 0x41, 0x80, 0x02, 0x00, 0x00, 0x7f, 0x80,
                            0x00, 0x06, 0x00, 0x00, 0x01, 0x00, 0x80, 0x1b, 0x04, 0x61, 0x00, 0x04, 0x06, 0x02, 0x40, 0x00,
                            0x00, 0x03, 0x00, 0x20, 0x03, 0x00, 0x00, 0x0d, 0x02, 0x63, 0x00, 0x04, 0x00, 0x20, 0x40, 0x00,
                            0x00, 0x00, 0xc0, 0x30, 0x06, 0x00, 0x00, 0x85, 0x01, 0x23, 0x00, 0x04, 0x00, 0x30, 0x40, 0x00,
                            0x03, 0xfc, 0x00, 0x10, 0x18, 0x00, 0x00, 0x45, 0x80, 0x21, 0x00, 0x00, 0x23, 0x3e, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x10, 0x70, 0x04, 0x00, 0x40, 0x80, 0x01, 0xe0, 0x63, 0xf0, 0x3f, 0x2f, 0xe0,
                            0x00, 0x1f, 0xf8, 0x9b, 0x80, 0x04, 0x00, 0x60, 0x80, 0x39, 0xf0, 0xdb, 0xf8, 0x3e, 0x7f, 0xe0,
                            0x00, 0x7f, 0xf8, 0x1c, 0x00, 0x04, 0x20, 0x7c, 0xe0, 0xfc, 0xf8, 0xf9, 0xfc, 0x7c, 0x7f, 0xe0,
                            0x00, 0x38, 0x00, 0x00, 0x01, 0x82, 0xe0, 0x7c, 0xf0, 0x7c, 0xfd, 0xfc, 0x7f, 0xf8, 0xff, 0x00,
                            0x00, 0x00, 0x00, 0x08, 0x00, 0x63, 0xf0, 0x7c, 0xf0, 0x3c, 0x3f, 0xf0, 0x3f, 0xe0, 0x80, 0x00,
                            0x00, 0x00, 0x00, 0x0c, 0x00, 0x38, 0xf8, 0xfc, 0x78, 0x1e, 0x08, 0x00, 0x00, 0x02, 0x7f, 0x00,
                            0x00, 0x00, 0x00, 0x0f, 0xc0, 0x7e, 0x3c, 0xf8, 0x70, 0x00, 0x01, 0x80, 0x00, 0x06, 0x7e, 0x00,
                            0x00, 0x00, 0x00, 0x0f, 0xc0, 0x3f, 0x8f, 0xe0, 0x40, 0x03, 0x06, 0x0f, 0xff, 0xc0, 0x7e, 0x00,
                            0x00, 0x00, 0x7e, 0x07, 0xe0, 0x0f, 0xe3, 0x80, 0x0f, 0x00, 0x08, 0x1c, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x3f, 0xff, 0x07, 0xe0, 0x01, 0xf8, 0x01, 0x80, 0x04, 0x18, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x0f, 0xff, 0x07, 0xe0, 0x00, 0x7e, 0x18, 0x02, 0x06, 0x10, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x0f, 0xfc, 0x03, 0xe0, 0xfc, 0x1f, 0xc0, 0x02, 0x02, 0x30, 0x00, 0x70, 0x4c, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x03, 0xe3, 0xe0, 0x07, 0xf0, 0x02, 0x03, 0x39, 0x00, 0xff, 0x00, 0x00, 0x00,
                            0x00, 0x03, 0xf0, 0x13, 0xc0, 0x00, 0x00, 0x7c, 0x03, 0xc9, 0xf1, 0x00, 0x03, 0xe0, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x0f, 0x09, 0xc9, 0xe2, 0x00, 0x00, 0x38, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x18, 0x00, 0x00, 0x00, 0x00, 0xc1, 0xc8, 0xe4, 0x20, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x08, 0x40, 0x00, 0x00, 0x00, 0x01, 0xc4, 0x44, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x09, 0x00, 0x00, 0x00, 0x30, 0x00, 0x8c, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfc, 0x04, 0x1c, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
                            ])

    # Define a simple 8x8 degree symbol bitmap
    degree_symbol = bytearray([
        0b00111000,
        0b01101100,
        0b01101100,
        0b00111000,
        0b00000000,
        0b00000000,
        0b00000000,
        0b00000000
    ])

    # UPDATE OTA FIRMWARE
    firmware_url = "https://raw.githubusercontent.com/rpcovington2/SmartHomeAutomations/"

    # You can choose any other combination of I2C pins
    i2c = SoftI2C(scl=Pin(5), sda=Pin(4))
    oled_width = 128
    oled_height = 64
    try:
        oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
        fb = framebuf.FrameBuffer(ronco_logo, 128, 64, framebuf.MONO_HLSB)

        # Display the image
        oled.blit(fb, 0, 0)

        oled.text("Updating...", 0, 0)
        oled.show()
    except OSError as e:
        print('No OLED Connected.')

    ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
    ota_updater.download_and_install_update_if_available()

    try:
        oled.text("Done", 50, 0)
        oled.show()
    except NameError as e:
        print('No OLED Connected.')

    with open('version.json') as f:
        current_version = int(json.load(f)['version'])
    print(f"Current device firmware version is '{current_version}'")

    # Temperature/Humidity Sensors
    # sensor = dht.DHT22(Pin(22))
    sensor = dht.DHT11(Pin(22))

    # GLOBAL LED light control
    numpix = 23  # PIXELS
    pixels = Neopixel(numpix, 0, 28, "RGB")
    BRIGHTNESS = 50
    MAX = 3.0
    MIN = 3.0
    animation = 0
    off_color = (0, 0, 0)
    color = off_color
    color2 = off_color

    hostname = 'MyPicoDevice'  # Change to your desired device name
    # TODO: Add Loop to Create ID Based on # of devices on Network
    client_id = 'FrontLEDControl'  # Client ID
    # oled.fill_rect(0, 0, 0, 128, 0)  # Update top-left quarter
    # oled.show()

    try:
        oled.text("Connecting WiFi...", 0, 50)
        oled.show()
    except NameError as e:
        print("Connecting WiFi...")

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(SSID, PASSWORD)
    time.sleep(15)

    if wlan.isconnected():
        try:
            oled.text("Connected", 100, 0)
            oled.show()
        except NameError as e:
            print("Connected.")

    else:
        try:
            oled.text("Retrying", 100, 0)
            oled.show()
        except NameError as e:
            print("Retrying WiFi...")
        wlan.connect(SSID, PASSWORD)
        time.sleep(15)

    # MQTT Server Details
    mqtt_server = '192.168.1.121'
    topic_sub = b'home/lights'
    Connection_topic = b'home/pico/status'
    temp_text = f'home/temperature/{client_id}'
    temperature_sub = temp_text.encode('utf-8')  # temperature topics
    temp_humidity = f'home/humidity/{client_id}'
    humidity_sub = temp_humidity.encode('utf-8')  # Humidity Topics
    Retry_sub = b'home/pico/status/retry'  # Retry


    def Updater():
        fb = framebuf.FrameBuffer(ronco_logo, 128, 64, framebuf.MONO_HLSB)

        # Display the image
        oled.blit(fb, 0, 0)

        oled.text("Updating...", 0, 0)
        oled.show()

        ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
        ota_updater.download_and_install_update_if_available()

        oled.text("Done", 50, 0)
        oled.show()


    def sub_cb(topic, msg):
        global color
        global color2
        global animation
        global off_color
        global BRIGHTNESS
        global MAX
        global MIN

        print("New message on topic {}".format(topic.decode('utf-8')))
        msg = msg.decode('utf-8')

        print(msg.split(":"))
        temp = msg.split(":")

        # color = rgb_str_to_tuple(msg)

        if temp[0] == "color1":
            color = rgb_str_to_tuple(temp[1].strip())

        elif temp[0] == "color2":
            color2 = rgb_str_to_tuple(temp[1].strip())

        elif temp[0] == "animation":
            animation = int(temp[1].strip())

        elif temp[0] == "Brightness":
            BRIGHTNESS = int(temp[1].strip())

        elif temp[0] == "Min:":
            MIN = int(temp[1].strip())

        elif temp[0] == "Max:":
            MAX = int(temp[1].strip())

        elif temp[0] == "off":
            color = off_color
            color = off_color
            animation = 0


    def LED_off(np):
        np.fill(off_color)
        np.show()


    def mqtt_connect():
        client = MQTTClient(client_id, mqtt_server, keepalive=60)
        client.set_callback(sub_cb)
        client.connect()
        print('Connected to %s MQTT Broker' % (mqtt_server))
        return client


    def reconnect():
        print('Failed to connect to MQTT Broker. Reconnecting...')
        time.sleep(5)
        machine.reset()


    def dim_color(color, factor):
        """Dim the color by a certain factor (between 0 and 1)."""
        return tuple(int(c * factor) for c in color)


    def frange(start, stop, step):
        while start < stop:
            yield round(start, 10)  # Limiting to 10 decimal places to avoid floating-point precision issues
            start += step


    def rgb_str_to_tuple(rgb_str):
        """Convert an RGB string (e.g., '255, 87, 51') to an RGB tuple."""
        # Split the string by commas and convert to integers
        rgb = tuple(map(int, rgb_str.split(',')))

        return rgb


    def chase_animation2(np, num_leds, delay=0.1, dim_factor=0.8):
        global color
        global color2
        global BRIGHTNESS

        """Chase animation with dimming and color change every 5th LED."""
        color_index = 0  # Start with the first color
        # while True:
        for i in range(num_leds):
            if i <= 0:
                num1 = i + 1
                num2 = i + 2
            else:
                num1 = i - 1
                num2 = i - 2

            np.set_pixel(i, color)
            # np.set_pixel(num1,color)
            # np.set_pixel(num2,color)
            np.brightness(BRIGHTNESS)
            # Write the color to the LED strip
            np.show()

            time.sleep(delay)

            # Turn off the current LED (chase effect)
            # np.set_pixel(i-3, color2)
            # np.set_pixel(i-2, color2)
            # np.set_pixel(i-1, color2)

        tempColor = color
        tempColor2 = color2
        color = tempColor2
        color2 = tempColor


    def set_leds(np, value, num_leds):
        # Clear all LEDs
        np.fill((0, 0, 0))

        # Map the value to the number of LEDs to light
        max_brightness = 255
        num_active = int((value / 4095) * (num_leds // 2))  # Scale value to LED range

        # Light LEDs from the center outward
        mid = num_leds // 2
        for i in range(num_active):
            color = (max_brightness, 0, 0)  # Red color, adjust as needed
            np[mid - i] = color  # Light left side
            np[mid + i] = color  # Light right side

        # Update the strip
        np.write()

    def chase_animation(np, num_leds, delay=0.1, dim_factor=0.8):
        global color
        global color2
        global BRIGHTNESS

        """Chase animation with dimming and color change every 5th LED."""
        color_index = 0  # Start with the first color
        # while True:
        for i in range(num_leds):
            if i <= 0:
                num1 = i + 1
                num2 = i + 2
            else:
                num1 = i - 1
                num2 = i - 2

            np.set_pixel(i, color)
            # np.set_pixel(num1,color)
            # np.set_pixel(num2,color)
            np.brightness(BRIGHTNESS)
            # Write the color to the LED strip
            np.show()

            time.sleep(delay)

            # Turn off the current LED (chase effect)
            # np.set_pixel(i-3, color2)
            # np.set_pixel(i-2, color2)
            # np.set_pixel(i-1, color2)

        tempColor = color
        tempColor2 = color2
        color = tempColor2
        color2 = tempColor


    def flash_animation(np, min_val, max_val):
        global color
        global color2

        # min_val = 0.01
        # max_val = 0.5

        on_value = min_val + (random.random() * (max_val - min_val))
        off_value = min_val + (random.random() * (max_val - min_val))

        np.fill(color)
        np.show()
        time.sleep(on_value)

        np.fill(color2)
        np.show()
        time.sleep(off_value)


    def TemperatureReading():
        temp = 25
        hum = 100
        try:
            time.sleep(1)
            sensor.measure()
            temp = sensor.temperature()
            hum = sensor.humidity()
            temp_f = temp * (9 / 5) + 32.0

            # print('Temperature: %3.1f C' %temp)
            print('Temperature: %3.1f F' % temp_f)
            print('Humidity: %3.1f %%' % hum)

        except OSError as e:
            print('Failed to read sensor.')

        return temp_f, hum


    try:
        client = mqtt_connect()
    except OSError as e:
        reconnect()

    TotalTimeElpased = 1
    TimeElpased = 1

    while True:
        if TimeElpased > 14400:
            try:
                oled.fill(0)
                oled.show()
            except NameError as e:
                print("No OLED Connected")
            with open('version.json') as f:
                current_version = int(json.load(f)['version'])
            print(f"Current device firmware version is '{current_version}'")

            try:
                fb = framebuf.FrameBuffer(ronco_logo, 128, 64, framebuf.MONO_HLSB)
                # Display the image
                oled.blit(fb, 0, 0)

                oled.text("Updating...", 0, 0)
                oled.text(f"Version: {current_version}", 0, 50)
                oled.show()
            except NameError as e:
                print("Updating...")

            ota_updater = OTAUpdater(SSID, PASSWORD, firmware_url, "main.py")
            ota_updater.download_and_install_update_if_available()
            try:
                oled.text("Done", 100, 0)
                oled.show()
            except NameError as e:
                print("Connecting WiFi...")

            TimeElpased = 1

        try:
            DataReading = TemperatureReading()
            client.publish(temperature_sub, f'Temperature: {DataReading[0]}')
            client.publish(humidity_sub, f'Humidity: {DataReading[1]}')

        except NameError as e:
            print("No Temperature Sensor Attached")

        try:
            client.subscribe(topic_sub)
            client.publish(Connection_topic, f'{client_id}: Active')
        except OSError as e:
            print(e)

        if animation == 0:

            # Generate a random number between 50000 and 610000
            random_number = random.randint(50000, 61000)
            set_leds(pixels,random_number,numpix)
            #LED_off(pixels)
        elif animation == 1:
            chase_animation(pixels, numpix, delay=.1, dim_factor=0.7)
        elif animation == 2:
            flash_animation(pixels, MAX, MIN)
        else:
            LED_off(pixels)

        try:
            oled.fill(0)  # Fill screen with black

            # Create a framebuffer for the degree symbol
            degree_fb = framebuf.FrameBuffer(degree_symbol, 8, 8, framebuf.MONO_HLSB)

            # Draw it on the OLED at a specific position
            oled.blit(degree_fb, 30, 15)  # Adjust coordinates as needed
            oled.text("Temp.", 10, 0)
            oled.text(f"{str((int(DataReading[0])))} F", 15, 15)

            oled.text("Humidity", 60, 0)
            oled.text(f"{str(round(DataReading[1], 0))}%", 80, 15)

            oled.text("IP Address", 25, 27)
            oled.text(wlan.ifconfig()[0], 15, 40)

            oled.text("Version:", 0, 50)
            oled.text(str(current_version), 110, 50)

            # oled.pixel(10, 10 ,1)
            oled.show()
        except NameError as e:
            print("Connecting WiFi...")

        TimeElpased += 1
        TotalTimeElpased += 1