#include "ESP.hpp"

ESP::ESP(String WifiName, String WifiPass) {
    this->_wifiName = WifiName;
    this->_wifiPass = WifiPass;
    Serial1.begin(115200);
    Serial1.println("AT");
    this->GetFromESP8266(10000);
    Serial1.println("AT+RST"); // reset
    this->GetFromESP8266(10000);
    Serial1.println("AT+CIPMUX=1");
    this->GetFromESP8266(10000);
    Serial1.println("AT+CWMODE=3");
    this->GetFromESP8266(10000);
    Serial1.println("AT+CWJAP=\"" + WifiName + "\",\"" + WifiPass + "\""); // connect to wifi hotspot
    this->GetFromESP8266(10000);
    Serial1.println("AT+CIFSR"); // display connection IP
    this->GetFromESP8266(10000, true);
}

ESP::~ESP() {}

void ESP::SendRequest(String remoteHost, String port, String request) {
    Serial.println(request);

    for (char try_count = 0; try_count < 3; try_count++) {

        if (try_count > 0) {
            Serial.println("\tRetrying...");
            Serial1.println("AT+CIPCLOSE");
            GetFromESP8266(300);
        }

        Serial1.println("AT+CIPSTART=\"TCP\",\"" + remoteHost + "\"," + port);
        if (GetFromESP8266(3000).endsWith("ERROR")) {
            Serial.println("\tERROR AT +CIPSTART");
            continue;
        }

        String message = request + " HTTP/1.1\r\nHost: " + remoteHost + "\r\n"; //state=OK/NOK/NA, id=1/2/3
        Serial1.println(String("AT+CIPSEND=") + String(message.length() + 2));
        if (GetFromESP8266(3000).endsWith("ERROR")) {
            Serial.println("\tERROR AT +CIPSEND");
            continue;
        }
        Serial1.println(message.c_str());
        if (GetFromESP8266(3000).endsWith("ERROR")) {
            Serial.println("\tERROR WHEN SENDING DATA");
            continue;
        }
        Serial.println("SEND OK");
        break;
    }
    Serial1.println();
    Serial1.println();
    Serial1.println("AT+CIPCLOSE");
    GetFromESP8266(300);
    delay(100);
    return;
}

String ESP::GetFromESP8266(const int timeout, bool display) {
    long int time = millis();
    String reponse = "";
    while ((time + timeout) > millis())
    {
        if (Serial1.available())
        {
            char c = Serial1.read();
            reponse += c;
        }
        if (reponse.endsWith("OK\r\n") ||
            reponse.endsWith("ERROR\r\n"))
            break;
    }
    reponse.trim();
    if (display) {
        Serial.println(reponse);
    }
    while (Serial1.available()) Serial1.read(); // flush IO
    return (reponse);
}

