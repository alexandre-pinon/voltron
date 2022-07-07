#include <Arduino.h>
#include "ESP.hpp"
#include "DHT.h"


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

bool firstPass = true;

void setup ()
{
  Serial.begin(115200);

  pinMode(digitalPin, INPUT); 

  dht = new DHT(DHTPIN, DHTTYPE);
  dht->begin();

  Esp = new ESP(WifiName, WifiPass);

  Serial.println("-----INITIALISATION TERMINÉE-----");
}
void loop ()
{
  // Read the analog interface
  // FALSE = aimant, TRUE = pas d'aimant
  digitalVal = digitalRead(digitalPin);
  temperature = dht->readTemperature();
  humidity = dht->readHumidity();

  Serial.print("Temp: ");
  Serial.print(temperature);
  Serial.print("°C - Humidity: ");
  Serial.print(humidity);
  Serial.print(" Door open: ");
  Serial.println(digitalVal);

  if (firstPass || digitalVal != oldDigitalVal) {
    //Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?name=door&state=" + String(digitalVal));
  }
  if (firstPass || oldHumidity != humidity) {
    //Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?name=humidity&state=" + String(humidity));
  }
  if (firstPass || oldTemperature != temperature) {
    //Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?name=temperature&state=" + String(temperature));
  }
  oldDigitalVal = digitalVal;
  oldHumidity = humidity;
  oldTemperature = temperature;

  firstPass = false;

  delay(1000);
}