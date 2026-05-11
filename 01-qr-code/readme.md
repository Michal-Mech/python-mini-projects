# QR Code Generator

An application for generating QR codes from text or URLs, built with Python and CustomTkinter.

## Preview

![QR Code Generator Screenshot](main_window.png)

## Features

- Real-time QR code generation as you type
- Save QR code to file
- Save with `Enter` key
- UI with CustomTkinter and transparent title bar

## Built with

- **CustomTkinter** – library built on top of Tkinter
- **Tkinter** – GUI library
- **qrcode** – QR code generation
- **Pillow (PIL)** – image processing and conversion
- **ctypes** – used to create custom title bar


## How to use

1. Type any text or URL in the input field at the bottom
2. The QR code is generated automatically as you type
3. Click **Save** (or press `Enter`) to save the QR code to a file
4. Choose the file format (PNG by default) and location

## Project structure

```
01-qr-code/
├── main.py             # Main application
├── main_window.png     # Screenshots used in README
└── README.md           
```
 