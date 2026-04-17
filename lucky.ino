#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

// ================= WIFI =================
const char* ssid = "Jesus_is_King";
const char* password = "moi000000";

WebServer server(80);

// ================= SERVO =================
Servo myServo;
const int servoPin = 14;
int servoPosition = 45;

// ================= BUZZER =================
const int buzzerPin = 13;
bool buzzerActive = false;

// ================= HTML =================
const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ESP32 Control</title>

<style>
body { font-family: Arial; text-align:center; margin-top:60px; background:#f4f4f4; }
.button { padding:20px 40px; font-size:18px; margin:20px; border:none; border-radius:8px; cursor:pointer; color:white; }
.open { background:#4CAF50; }
.close { background:#f44336; }
.buzzer { background:#2196F3; }
.status { font-size:20px; margin-top:20px; }
</style>
</head>

<body>

<h1>ESP32 Door System</h1>

<button class="button open" onclick="sendCommand('open')">OPEN</button>
<button class="button close" onclick="sendCommand('close')">CLOSE</button>
<button class="button buzzer" onclick="sendCommand('buzzer_on')">BUZZER ON</button>
<button class="button" style="background:#777;" onclick="sendCommand('buzzer_off')">BUZZER OFF</button>

<div class="status">
State: <span id="state">Ready</span>
</div>

<script>
function sendCommand(cmd){
    fetch('/' + cmd)
    .then(res => res.text())
    .then(data => document.getElementById("state").innerText = data);
}
</script>

</body>
</html>
)rawliteral";

// ================= SERVO =================
void moveServo(int target){
    int current = myServo.read();

    if(current < target){
        for(int i=current;i<=target;i+=3){
            myServo.write(i);
            delay(5);
        }
    } else {
        for(int i=current;i>=target;i-=3){
            myServo.write(i);
            delay(5);
        }
    }
}

// ================= ROUTES =================
void handleRoot(){
    server.send(200,"text/html",index_html);
}

void handleOpen(){
    moveServo(90);
    servoPosition = 90;
    server.send(200,"text/plain","OPEN");
}

void handleClose(){
    moveServo(45);
    servoPosition = 45;
    server.send(200,"text/plain","CLOSE");
}

// 🔊 BUZZER ON (Python + Web)
void handleBuzzerOn(){
    buzzerActive = true;
    digitalWrite(buzzerPin, HIGH);
    server.send(200,"text/plain","BUZZER ON");
}

// 🔇 BUZZER OFF (Python + Web)
void handleBuzzerOff(){
    buzzerActive = false;
    digitalWrite(buzzerPin, LOW);
    server.send(200,"text/plain","BUZZER OFF");
}

void handleStatus(){
    if(servoPosition == 90)
        server.send(200,"text/plain","OPEN");
    else
        server.send(200,"text/plain","CLOSED");
}

// ================= SETUP =================
void setup(){
    Serial.begin(115200);

    myServo.setPeriodHertz(50);
    myServo.attach(servoPin, 500, 2400);
    myServo.write(45);

    pinMode(buzzerPin, OUTPUT);
    digitalWrite(buzzerPin, LOW);

    WiFi.begin(ssid,password);

    while(WiFi.status()!=WL_CONNECTED){
        delay(500);
    }

    server.on("/",handleRoot);
    server.on("/open",handleOpen);
    server.on("/close",handleClose);
    server.on("/buzzer_on",handleBuzzerOn);
    server.on("/buzzer_off",handleBuzzerOff);
    server.on("/status",handleStatus);

    server.begin();
}

// ================= LOOP =================
void loop(){
    server.handleClient();

    if(buzzerActive){
        digitalWrite(buzzerPin, HIGH);
    }
}