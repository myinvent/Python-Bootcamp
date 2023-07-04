import qrcode

def generate_qr_code(data, filename):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # Add the data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Generate the QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image to the local drive
    qr_image.save(filename)
    print(f"QR code saved as {filename}")

# Prompt the user to enter the data for the QR code
data = input("Enter the data for the QR code: ")

# Prompt the user to enter the filename for the QR code image
filename = input("Enter the filename for saving the QR code image (e.g., qrcode.png): ")

# Generate and save the QR code image
generate_qr_code(data, filename)