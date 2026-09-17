#include "WebServer.h"
#include "WiFi.h"
#include "esp32cam.h"

const char* WIFI_SSID = "Android";
const char* WIFI_PASS = "oumaima123";

WebServer server(80);

static auto RES = esp32cam::Resolution::find(640, 480);


// ============================================================
// CAMERA
// ============================================================

void initCamera() {

  using namespace esp32cam;

  Config cfg;

  cfg.setPins(pins::AiThinker);

  cfg.setResolution(
    Resolution::find(640, 480)
  );

  cfg.setBufferCount(1);

  cfg.setJpeg(60);

  bool ok = Camera.begin(cfg);

  if (ok) {
    Serial.println("CAMERA OK");
  } else {
    Serial.println("CAMERA FAIL");
  }
}


// ============================================================
// WIFI
// ============================================================

void initWifi() {

  WiFi.persistent(false);

  WiFi.mode(WIFI_STA);

  WiFi.begin(
    WIFI_SSID,
    WIFI_PASS
  );

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");
  }

  Serial.println();

  Serial.println("WiFi connected");

  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}


// ============================================================
// MJPEG STREAM
// ============================================================

void handleStream() {

  WiFiClient client = server.client();

  Serial.println("STREAM STARTED");

  // HTTP MJPEG header
  client.print(
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: multipart/x-mixed-replace; boundary=frame\r\n"
    "Cache-Control: no-cache\r\n"
    "Pragma: no-cache\r\n"
    "Connection: close\r\n"
    "\r\n"
  );

  while (client.connected()) {

    // Capture frame
    auto frame = esp32cam::capture();

    if (frame == nullptr) {

      Serial.println("CAPTURE FAILED");

      delay(100);

      continue;
    }

    // Send MJPEG boundary
    client.print("--frame\r\n");

    client.print(
      "Content-Type: image/jpeg\r\n"
    );

    client.print(
      "Content-Length: "
    );

    client.print(
      frame->size()
    );

    client.print(
      "\r\n\r\n"
    );

    // Send JPEG
    frame->writeTo(client);

    // End frame
    client.print("\r\n");

    // Control FPS
    delay(50);
  }

  Serial.println("STREAM STOPPED");

  client.stop();
}


// ============================================================
// SERVER
// ============================================================

void initServer() {

  server.on(
    "/stream",
    handleStream
  );

  server.begin();

  Serial.println("HTTP server started");

  Serial.print("Stream URL: http://");
  Serial.print(WiFi.localIP());
  Serial.println("/stream");
}


// ============================================================
// SETUP
// ============================================================

void setup() {

  Serial.begin(115200);

  initWifi();

  initCamera();

  initServer();
}


// ============================================================
// LOOP
// ============================================================

void loop() {

  server.handleClient();
}
