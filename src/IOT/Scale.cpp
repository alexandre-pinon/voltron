#include "Scale.hpp"

Scale::Scale(int datPin, int sckPin) {
  // Initialize library with data output pin, clock input pin and gain factor.
  // Channel selection is made by passing the appropriate gain:
  // - With a gain factor of 64 or 128, channel A is selected
  // - With a gain factor of 32, channel B is selected
  // By omitting the gain factor parameter, the library
  // default "128" (Channel A) is used here.
  this->DatPin = datPin;
  this->SckPin = sckPin;

  this->scale.begin(datPin, sckPin);
  // calibrated on 16/07/2022
  this->scale.set_scale(1350.5F);   // this value is obtained by calibrating the scale with known weights; see the README for details
  this->scale.tare();				        // reset the scale to 0
}

double Scale::getWeight() {
    double value;

    this->scale.power_up();
    value = scale.get_units(10);
    this->scale.power_down();

    return value;
}

void Scale::tare() {
    this->scale.tare();
}