#include <Arduino.h>
#include "ESP.hpp"
#include "Scale.hpp"
#include "DHT.h"
#include <Adafruit_BMP280.h>


#define DHTPIN 2
#define DHTTYPE DHT11

DHT *dht;
int humidity, oldHumidity;
int temperature, oldTemperature;

int digitalPin = A0; // linear Hall magnetic sensor analog interface
int digitalVal; // digital readings
int oldDigitalVal;

String WifiName = "ONEPLUS vm";
String WifiPass = "24081998";
String WifiRemoteHost = "localhost", WifiRemotePort = "8080"; // need to change this and the request route
ESP *Esp;

const int LOADCELL_DOUT_PIN = 8;
const int LOADCELL_SCK_PIN = 9;
Scale *scale;
int weight, oldWeight;

bool firstPass = true;

void setup ()
{
  Serial.begin(115200);

  pinMode(digitalPin, INPUT); 

  dht = new DHT(DHTPIN, DHTTYPE);
  dht->begin();

  scale = new Scale(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

  //Esp = new ESP(WifiName, WifiPass);

  Serial.println("-----INITIALISATION TERMINÉE-----");
}
void loop ()
{
  // Read the analog interface
  // FALSE = aimant, TRUE = pas d'aimant
  digitalVal = digitalRead(digitalPin);
  temperature = dht->readTemperature();
  humidity = dht->readHumidity();
  weight = scale->getWeight();

  Serial.println("Temp: " + String(temperature) +
                 "°C - Humidity: " + String(humidity) +
                 " - Door open: " + String(digitalVal) +
                 " - Weight: " + String(weight));

  if (firstPass || digitalVal != oldDigitalVal) {
    //Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?name=door&state=" + String(digitalVal));
  }
  if (firstPass || oldHumidity != humidity) {
    //Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?name=humidity&state=" + String(humidity));
  }
  if (firstPass || oldTemperature != temperature) {
    //Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?name=temperature&state=" + String(temperature));
  }
  if (firstPass || oldWeight != weight) {
    //Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?name=weight&state=" + String(weight));
  }
  oldDigitalVal = digitalVal;
  oldHumidity = humidity;
  oldTemperature = temperature;
  oldWeight = weight;

  firstPass = false;

  delay(1000);
}