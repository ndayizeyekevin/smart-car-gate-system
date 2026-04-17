"""
License Plate Detection + WhatsApp + ESP32 Buzzer (STABLE FIX VERSION)
"""

import cv2
from ultralytics import YOLO
import requests
import time
from datetime import datetime
import os



class WhatsAppCloudDetector:
    def __init__(self):
        print("🚀 Loading license plate detection model...")

        model_path = "license-plate-finetune-v1s.pt"

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found: {model_path}")

        self.model = YOLO(model_path)
        self.model.to('cpu')

        # ==============================
        # DETECTION SETTINGS
        # ==============================
        self.confidence_threshold = 0.5
        self.processing_width = 640
        self.processing_height = 480

        # ==============================
        # 📱 WHATSAPP CONFIG
        # ==============================
        self.PHONE_NUMBER_ID = "1083520474843012"
        self.ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
        self.RECIPIENT_NUMBER = "250732828490"

        self.WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{self.PHONE_NUMBER_ID}/messages"

        # ==============================
        # 🔊 ESP32 CONFIG (FIXED - MATCH OLD WORKING SYSTEM)
        # ==============================
        self.ESP32_IP = "192.168.203.146"

        # ⚠️ IMPORTANT: SAME ENDPOINT LIKE YOUR OLD CODE
        self.ESP_BUZZ_URL = f"http://{self.ESP32_IP}/buzzer"
        self.ESP_OPEN_URL = f"http://{self.ESP32_IP}/open"

        # cooldown system
        self.last_detection_time = 0
        self.detection_cooldown = 30

        self.detection_count = 0
        self.detected_plates = []

        self.cap = None

        print("✅ System initialized")

    # ==============================
    # 🔊 ESP32 COMMUNICATION
    # ==============================
    def send_to_esp32(self, url):
        try:
            print("➡️ Sending to ESP32:", url)
            response = requests.get(url, timeout=3)

            if response.status_code == 200:
                print("🔊 ESP32 command sent successfully")
                return True
            else:
                print(f"⚠️ ESP32 error: {response.status_code}")
                return False

        except Exception as e:
            print(f"❌ ESP32 connection failed: {e}")
            return False

    # ==============================
    # 📱 WHATSAPP FUNCTION
    # ==============================
    def send_whatsapp_message(self, plate_id, confidence):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        confidence_percent = int(confidence * 100)

        message = (
            f"🚗 *PLATE DETECTED!*\n\n"
            f"Plate ID: `{plate_id}`\n"
            f"Confidence: {confidence_percent}%\n"
            f"Time: {current_time}"
        )

        headers = {
            "Authorization": f"Bearer {self.ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        data = {
            "messaging_product": "whatsapp",
            "to": self.RECIPIENT_NUMBER,
            "type": "text",
            "text": {"body": message, "preview_url": False}
        }

        try:
            response = requests.post(
                self.WHATSAPP_API_URL,
                headers=headers,
                json=data,
                timeout=10
            )

            if response.status_code == 200:
                print("📱 WhatsApp sent successfully")
                return True
            else:
                print(f"❌ WhatsApp error: {response.text}")
                return False

        except Exception as e:
            print(f"❌ WhatsApp failed: {e}")
            return False

    # ==============================
    # CAMERA
    # ==============================
    def init_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.processing_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.processing_height)

        if not self.cap.isOpened():
            print("❌ Camera not found")
            return False

        print("✅ Camera ready")
        return True

    # ==============================
    # DETECTION
    # ==============================
    def detect_plates(self, frame):
        results = self.model(frame, conf=self.confidence_threshold, verbose=False)

        plates = []
        for result in results:
            if result.boxes:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    confidence = float(box.conf[0])

                    plates.append({
                        "bbox": (x1, y1, x2, y2),
                        "confidence": confidence
                    })
        return plates

    # ==============================
    # MAIN LOOP
    # ==============================
    def run(self):
        if not self.init_camera():
            return

        print("\n🎯 SYSTEM RUNNING...")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue

            plates = self.detect_plates(frame)
            current_time = time.time()

            # ==============================
            # 🔊 SIMPLE & RELIABLE BUZZER TRIGGER
            # ==============================
            if plates:
                # ALWAYS trigger buzzer like your old working system
                self.send_to_esp32(self.ESP_BUZZ_URL)

            # ==============================
            # 🚨 WHATSAPP (COOLDOWN PROTECTED)
            # ==============================
            if plates and (current_time - self.last_detection_time > self.detection_cooldown):

                best_plate = max(plates, key=lambda x: x["confidence"])
                confidence = best_plate["confidence"]

                self.detection_count += 1
                plate_id = f"PLATE_{self.detection_count:04d}"

                print("\n==============================")
                print(f"🎯 PLATE DETECTED: {confidence:.1%}")

                print("📱 Sending WhatsApp...")
                self.send_whatsapp_message(plate_id, confidence)

                self.last_detection_time = current_time

                self.detected_plates.append({
                    "id": plate_id,
                    "confidence": confidence,
                    "time": datetime.now().strftime("%H:%M:%S")
                })

                print("✅ Event completed")
                print("==============================\n")

            # ==============================
            # DISPLAY
            # ==============================
            for plate in plates:
                x1, y1, x2, y2 = plate["bbox"]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.imshow("Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cleanup()

    def cleanup(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

        print("\n📊 SESSION SUMMARY")
        print(f"Total detections: {self.detection_count}")
        print("System stopped")


# ==============================
# START
# ==============================
if __name__ == "__main__":
    detector = WhatsAppCloudDetector()
    detector.run()