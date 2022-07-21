#ifndef ESP_H_
#define ESP_H_

#include <Arduino.h>

class ESP {
    public:
        ESP(String WifiName, String WifiPass);
        ~ESP();
        void SendRequest(String remoteHost, String port, String request);

    private:
        String GetFromESP8266(const int timeout, bool display = false);

        String _wifiName;
        String _wifiPass;
};

#endif