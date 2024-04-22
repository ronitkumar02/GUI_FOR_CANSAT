# CANSAT INDIA
## Overview
It is a project aimed at acquiring telemetry data from a spacecraft equipped with XBee modules and visualizing it in real-time through a user-friendly graphical interface. This project demonstrates skills in Python programming, serial communication, data visualization, and PyQt5 GUI development.

## Features
- Real-time visualization of telemetry data including accelerometer, magnetometer, gyroscope, velocity, humidity, pressure, and battery level.
- GPS location display with map integration.
- Battery status indicator.
- Expanded view for detailed data analysis.
- Custom font integration for a space-themed UI.
- Modular code structure for easy maintenance and scalability.

## How to Run
1. **Setup Serial Communication**: Connect the XBee module to the designated serial port on your computer (default: `COM15`). Ensure that the baud rate is set to `9600`.
2. **Install Dependencies**: Install the required Python libraries by running:
    ```
    pip install -r requirements.txt
    ```
3. **Read the data from Xbee**: Execute the `Read_data_XBee.py` script using Python:
    ```
    python Read_data_XBee.py
    ```
    This will start the read the data from the xbee.
4. **Run the Application**: Execute the `stardust_ui.py` script using Python:
    ```
    python stardust_ui.py
    ```
5. **Interact with the Interface**: Once the GUI window appears, you can view real-time telemetry data, GPS location, battery status, and more. Use the buttons to perform various actions such as calibration and enabling data acquisition.

## Screenshots
![GUI Screenshot](https://github.com/ronitkumar02/GUI_FOR_CANSAT/blob/main/icons/Screenshot%202024-04-14%20231847.png)
![GUI Screenshot](https://github.com/ronitkumar02/GUI_FOR_CANSAT/blob/main/icons/Screenshot%202024-04-14%20231942.png)

## API Reference
#### Get all items
Get your api_key from [Bing Maps APIs](https://www.bingmapsportal.com/?_gl=1*gq1sfr*_gcl_au*ODE2OTk5NjQ0LjE3MTMwOTYxMzk.)
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `api_key` | `string` | **Required**. Your API key |

## Notes
- This project is designed to work with XBee-equipped spacecraft, but the code can be adapted for other telemetry systems with minimal modifications.
- Feel free to explore and customize the UI elements, data visualization plots, and data processing logic according to your requirements.
