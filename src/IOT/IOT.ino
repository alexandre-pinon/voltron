#include <Arduino.h>
#include "ESP.hpp"

ESP *Esp;


int digitalPin = A0; // linear Hall magnetic sensor analog interface
int digitalVal; // digital readings
int oldDigitalVal;

String WifiName = "ONEPLUS vm";
String WifiPass = "24081998";
String WifiRemoteHost = "localhost", WifiRemotePort = "8080"; // need to change this and the request route

bool firstPass = true;

void setup ()
{
  Serial.begin(115200);
  Serial.println("Starting...");

  pinMode(digitalPin, INPUT); 
  Esp = new ESP(WifiName, WifiPass);

  Serial.println("-----INITIALISATION TERMINÉE-----");
}
void loop ()
{
  // Read the analog interface
  // FALSE = aimant, TRUE = pas d'aimant
  digitalVal = digitalRead(digitalPin) ; 
  
  Serial.println(digitalVal); // print analog value

  if (firstPass || digitalVal != oldDigitalVal) {
    oldDigitalVal = digitalVal;
    Esp->SendRequest(WifiRemoteHost, WifiRemotePort, "POST /sensor?state=" + String(digitalVal));
  }

  firstPass = false;

  delay(100);
}