#include "ESP.hpp"

ESP::ESP(String WifiName, String WifiPass) {
    this->_wifiName = WifiName;
    this->_wifiPass = WifiPass;
    Serial1.begin(115200);
    Serial1.println("AT");
    this->GetFromESP8266(10000);
    Serial1.println("AT+RST"); // reset
    this->GetFromESP8266(10000);
    Serial1.println("AT+CWMODE=3");
    this->GetFromESP8266(10000);
    Serial1.println("AT+CWJAP=\"" + WifiName + "\",\"" + WifiPass + "\""); // connect to wifi hotspot
    this->GetFromESP8266(10000);
    Serial1.println("AT+CIFSR"); // display connection IP
    this->GetFromESP8266(10000);
    Serial1.println("AT+CWJAP?"); // display connection infos
    this->GetFromESP8266(10000);
}

ESP::~ESP() {}

void ESP::SendRequest(String remoteHost, String port, String request) {
    Serial1.println("AT+CIPSTART=\"TCP\",\"" + remoteHost + "\"," + port);
    if (GetFromESP8266(10000) == "ERROR")
        return;
    String message = request + " HTTP/1.1\r\nHost: " + remoteHost + "\r\n"; //state=OK/NOK/NA, id=1/2/3
    Serial1.println(String("AT+CIPSEND=") + String(message.length() + 2));
    if (GetFromESP8266(10000) == "ERROR")
        return;
    Serial1.println(message.c_str());
    if (GetFromESP8266(10000) == "ERROR")
        return;
    GetFromESP8266(10000);
    Serial1.println("AT+CIPCLOSE");
    delay(30);
}

String ESP::GetFromESP8266(const int timeout) {
    String reponse = "";
    long int time = millis();
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
    if (reponse.endsWith("\r\n"))
        Serial.print(reponse);
    else
        Serial.println(reponse);
        
    return (reponse);
}

