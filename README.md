# License Plate Detection with WhatsApp & ESP32 Buzzer

A computer vision system that detects license plates using YOLOv8, sends notifications via WhatsApp Cloud API, and triggers an ESP32 buzzer for alerts.

## Features

- Real-time license plate detection using YOLOv8
- WhatsApp notifications with detection details
- ESP32 buzzer integration for immediate alerts
- Cooldown system to prevent spam notifications
- Live video feed with bounding boxes

## Prerequisites

- Python 3.10 or higher
- Webcam or video input device
- Internet connection for WhatsApp API
- ESP32 device with buzzer (optional)
- **Microsoft Visual C++ Redistributable** (required for PyTorch)
  - Download: https://aka.ms/vs/17/release/vc_redist.x64.exe

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Install Python dependencies:**
   ```bash
   pip install opencv-python ultralytics requests
   ```

3. **Download the YOLO model:**
   - Place `license-plate-finetune-v1s.pt` in the project root directory
   - (This file should be included in the repository)

## Configuration

Edit the following variables in `final2.py`:

### WhatsApp Settings
```python
self.PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"
self.ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
self.RECIPIENT_NUMBER = "RECIPIENT_PHONE_NUMBER"  # Include country code, no + sign
```

### ESP32 Settings
```python
self.ESP32_IP = "YOUR_ESP32_IP_ADDRESS"
```

## Usage

Run the detection system:
```bash
python final2.py
```

The system will:
- Open camera feed
- Detect license plates in real-time
- Trigger ESP32 buzzer on detection
- Send WhatsApp message (with cooldown protection)
- Display bounding boxes on video feed

Press 'q' to quit.

## Project Files

- `final2.py` - Main detection script
- `final.py` - Alternative version (if needed)
- `final1.py` - Another version (if needed)
- `license-plate-finetune-v1s.pt` - Trained YOLO model
- `README.md` - This file

## Dependencies

- `opencv-python` - Computer vision library
- `ultralytics` - YOLOv8 implementation
- `requests` - HTTP client for APIs
- `torch` - PyTorch (installed with ultralytics)
- `numpy` - Numerical computing (dependency)

## Troubleshooting

### Import Errors
- Ensure all packages are installed: `pip install opencv-python ultralytics requests`
- Install VC Redistributable if PyTorch fails to load

### Camera Issues
- Check camera permissions
- Ensure no other applications are using the camera
- Try different camera index in `cv2.VideoCapture(0)`

### WhatsApp API Errors
- Verify your WhatsApp Business API credentials
- Check recipient number format (include country code)
- Ensure API access token is valid

### ESP32 Connection Issues
- Verify ESP32 IP address
- Check network connectivity
- Ensure ESP32 endpoints match: `/buzzer` and `/open`

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]</content>
<parameter name="filePath">d:\proj\README.md