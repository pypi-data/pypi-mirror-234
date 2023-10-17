# QRlocator

## Overview
This package allows a user to get the 3D postion of QR codes from an image. It uses the OpenCV and Pyzbar libraries to scan and decode the QR codes, but you can also use other QR code scanning libraries and add information to the class using `add_qr_code`. This class mainly provides the `X`, `Y`, and `Z` coordinates of the center point of a code, where `Y` is a horizontal axis parallel to the camera's direction, `X` is a horizontal axis perpendicular to the camera's direction, and `Z` is a vertical axis representing the codes height.

add pictures

## Homepage
```
https://test.pypi.org/project/qrlocator/
```

## Install
```
pip install -i https://test.pypi.org/simple/ qrlocator 
from qrlocator.QRlocator import QRlocator
```

## Quick Start

The creation of the QRlocator class requires 4 parameters. It is very likely that you don't know some of these values, or the values you have are incorrect. This tool can automatically find the 3 best fit values for your camera:

- `image_path` (str): The file path of the image you wish to scan.
- `focal_ratio` (float): This is the focal length in mm over the sensor width in mm (focal/sensor) of the camera that was used to take the current image.
- `x_focal_angle_scalar` (float): A scalar value to correct the x-angle calculated from the image.
- `z_focal_angle_scalar` (float): A scalar value to correct the z-angle calculated from the image.
```python
qr_locator = QRlocator(r'path_to_image', focal_ratio, x_focal_angle_scalar, z_focal_angle_scalar)
qr_locator.scan_image()
qr_locator.show_visualization(qr_code_side_length_mm)
```

## Functions

```python
qr_locator.scan_image()
```
Scans and saves the QR codes from the current image
#
```python
qr_locator.modify_image(image)
qr_locator.modify_image_path(r'image_path')
```
Used to modify the locator's current image
#
```python
qr_locator.get_y_position(data, qr_code_side_length_mm)
```
Calculates and returns the Y coordinate (horizontal axis parallel to the camera's direction) of the QR code in inches.
- `data` (str): The string of data present in your QR code
- `qr_code_side_length_mm` (float): The actual side length of the QR code in millimeters
#
```python
qr_locator.get_x_position(data, qr_code_side_length_mm)
```
Calculates and returns the X coordinate (horizontal axis perpendicular to the camera's direction) of the QR code in inches.
- `data` (str): The string of data present in your QR code
- `qr_code_side_length_mm` (float): The actual side length of the QR code in millimeters
#
```python
qr_locator.get_z_position(data, qr_code_side_length_mm)
```
Calculates and returns the Z coordinate (vertical axis representing the code’s height) of the QR code in inches.
- `data` (str): The string of data present in your QR code
- `qr_code_side_length_mm` (float): The actual side length of the QR code in millimeters
#
```python
qr_locator.show_visualization(qr_code_side_length_mm, qr_codes=None)
```
Generates and displays a 2D visualization of the located QR codes in XY and XZ planes.
- `qr_code_side_length_mm` (float): The actual side length of the QR code in millimeters
- `qr_codes` (dict, optional): A dictionary containing QR codes. If not provided, the method will use the QR codes stored in the object.
#
```python
qr_locator.add_qr_code(data, tl, tr, br, bl)
```
Adds a QR code to the class 
- `tl` (float): The pixel location pair (x,y) of the top left corner of the QR code
- `tr` (float): The pixel location pair (x,y) of the top right corner of the QR code
- `br` (float): The pixel location pair (x,y) of the botom right corner of the QR code
- `bl` (float): The pixel location pair (x,y) of the bottom left corner of the QR code
#
```python
qr_locator.get_qr_codes()
qr_locator.get_qr_code(data)
```
Returns the dictionary of the locator's code(s)
- `data` (str): The string of data present in your QR code
#
```python
qr_locator.get_max_side_length(data)
```
Calculates and returns the maximum side length of the QR code in pixels.
- `data` (str): The string of data present in your QR code
#






