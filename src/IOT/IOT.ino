#include <Arduino.h>
#include "ESP.hpp"
#include "Scale.hpp"
#include "DHT.h"
#include <Adafruit_BMP280.h>
#include "Segment.hpp"


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
String WifiRemoteHost = "voltron-team-18.francecentral.cloudapp.azure.com", WifiRemotePort = "80"; // need to change this and the request route
ESP *Esp;

Segment *Display;

const int LOADCELL_DOUT_PIN = 8;
const int LOADCELL_SCK_PIN = 9;
Scale *scale;
int weight, oldWeight;

bool firstPass = true;

unsigned int loop_count, hardwareId;
String hardwareIdStr;

void setup ()
{
  Serial.begin(115200);

  pinMode(digitalPin, INPUT); 

  dht = new DHT(DHTPIN, DHTTYPE);
  dht->begin();

  scale = new Scale(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

  Esp = new ESP(WifiName, WifiPass);

  Display = new Segment();

  randomSeed(analogRead(A7) + analogRead(A5)); //random data from unconnected Pin
  hardwareId = random(1, 999);
  hardwareIdStr = String(hardwareId);

  loop_count = 0;

  Serial.println("-----INITIALISATION TERMINÉE-----");
}
void loop ()
{
  if (loop_count % 10 != 0) {
    loop_count ++;
    return;
  }
  // Read the analog interface
  // FALSE = aimant, TRUE = pas d'aimant
  digitalVal = digitalRead(digitalPin);
  temperature = dht->readTemperature();
  humidity = dht->readHumidity();
  weight = scale->getWeight();

  if (weight < 0) {weight = 0;}

  Display->print(hardwareId);

  Serial.println("Temp: " + String(temperature) +
                 "°C - Humidity: " + String(humidity) +
                 " - Door open: " + String(digitalVal) +
                 " - Weight: " + String(weight));

  if (firstPass || oldDigitalVal != digitalVal) {
    Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?room_id=" + hardwareIdStr + "&name=door&state=" + String(digitalVal));
  }
  if (firstPass || oldHumidity != humidity) {
    Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?room_id=" + hardwareIdStr + "&name=humidity&state=" + String(humidity));
  }
  if (firstPass || oldTemperature != temperature) {
    Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?room_id=" + hardwareIdStr + "&name=temperature&state=" + String(temperature));
  }
  if (firstPass || oldWeight != weight) {
    Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?room_id=" + hardwareIdStr + "&name=weight&state=" + String(weight));
  }
  oldDigitalVal = digitalVal;
  oldHumidity = humidity;
  oldTemperature = temperature;
  oldWeight = weight;

  firstPass = false;
  loop_count = 0;

  delay(100);
}