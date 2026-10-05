import qrcode

# 1. Gather Wi-Fi Network Information
ssid = input("Enter your Wi-Fi Network Name (SSID): ").strip()
password = input("Enter your Wi-Fi Password: ").strip()
security_type = input("Enter Security Type (WPA, WEP, or leave blank for open network): ").strip().upper()

# Default to WPA if not specified, or leave blank for no password
if not security_type:
    security_type = "WPA" if password else "nopass"

# 2. Format the data string specifically for Wi-Fi configurations
# Structure: WIFI:S:NetworkName;T:WPA;P:SecretPassword;;
wifi_data = f"WIFI:S:{ssid};T:{security_type};P:{password};;"

file_path = "wifi_qrcode.png"

# 3. Generate the QR code using your setup
qr = qrcode.QRCode(
    version=1,
    box_size=10,

    border=5
)
qr.add_data(wifi_data)
qr.make(fit=True)

# 4. Create and save the image
img = qr.make_image(fill_color="black", back_color="white")
img.save(file_path)

print(f"\nQR Code for Wi-Fi '{ssid}' was generated successfully as '{file_path}'!")
