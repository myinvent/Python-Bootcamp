import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog
from pyzbar import pyzbar
from PIL import Image

def open_image():
    # Open a file dialog to select an image file
    file_dialog = QFileDialog()
    file_dialog.setNameFilter("Image Files (*.png *.jpg *.jpeg)")
    if file_dialog.exec_():
        file_path = file_dialog.selectedFiles()[0]
        read_qr_code(file_path)

def read_qr_code(image_path):
    try:
        # Open the image file using PIL (Python Imaging Library)
        with Image.open(image_path) as img:
            # Convert the image to grayscale
            img = img.convert("L")
            
            # Use pyzbar to detect and decode QR codes
            qr_codes = pyzbar.decode(img)
            
            if qr_codes:
                # Extract the data from the QR code
                data = qr_codes[0].data.decode("utf-8")
                result_label.setText(f"QR Code Data: {data}")
            else:
                result_label.setText("No QR code found")
    
    except Exception as e:
        result_label.setText("Error reading QR code")

# Create the application instance
app = QApplication(sys.argv)

# Create the main window
window = QWidget()
window.setWindowTitle("QR Code Reader")

# Create the result label
result_label = QLabel("Scan a QR code")
result_label.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 10px;")

# Create the "Open Image" button and connect it to the open_image function
button = QPushButton("Open Image")
button.clicked.connect(open_image)

# Create the layout and add the result label and button
layout = QVBoxLayout()
layout.addWidget(result_label)
layout.addWidget(button)

# Set the layout for the main window
window.setLayout(layout)

# Show the main window
window.show()

# Run the application event loop
sys.exit(app.exec_())
