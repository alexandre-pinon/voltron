#include "Segment.hpp"

Segment::Segment(int pinA, int pinB, int pinC, int pinD, int pinE, int pinF, int pinG, int pinDot) {
    this->pinA = pinA;
    this->pinB = pinB;
    this->pinC = pinC;
    this->pinD = pinD;
    this->pinE = pinE;
    this->pinF = pinF;
    this->pinG = pinG;
    this->pinDot = pinDot;

    pinMode(pinA, OUTPUT);
    pinMode(pinB, OUTPUT);
    pinMode(pinC, OUTPUT);
    pinMode(pinD, OUTPUT);
    pinMode(pinE, OUTPUT);
    pinMode(pinF, OUTPUT);
    pinMode(pinG, OUTPUT);
    pinMode(pinDot, OUTPUT);

    this->print(8);

    delay(1000);

    this->reset();
}

void Segment::print(unsigned int nbr) {
    unsigned char storage_array[10];
    Vector<unsigned char> array(storage_array);
    while (nbr > 0) {
        array.push_back(nbr % 10);
        nbr /= 10;
    }
    for (int i = array.size() - 1; i >= 0; i--) {
        delay(500);
        this->PrintDigit(array[i]);
    }
    digitalWrite(pinDot, true);
    if (array.size() > 1) {
        delay(500);
        this->reset();
    }
}

void Segment::reset() {
    digitalWrite(pinA, false);
    digitalWrite(pinB, false);
    digitalWrite(pinC, false);
    digitalWrite(pinD, false);
    digitalWrite(pinE, false);
    digitalWrite(pinF, false);
    digitalWrite(pinG, false);
    digitalWrite(pinDot, false);
}

void Segment::PrintDigit(unsigned char c) {
    this->reset();
    switch (c)
    {
    case 0:
        digitalWrite(pinA, true);
        digitalWrite(pinB, true);
        digitalWrite(pinC, true);
        digitalWrite(pinD, true);
        digitalWrite(pinE, true);
        digitalWrite(pinF, true);
        break;
    case 1:
        digitalWrite(pinB, true);
        digitalWrite(pinC, true);
        break;
    case 2:
        digitalWrite(pinA, true);
        digitalWrite(pinB, true);
        digitalWrite(pinG, true);
        digitalWrite(pinE, true);
        digitalWrite(pinD, true);
        break;
    case 3:
        digitalWrite(pinA, true);
        digitalWrite(pinB, true);
        digitalWrite(pinG, true);
        digitalWrite(pinC, true);
        digitalWrite(pinD, true);
        break;
    case 4:
        digitalWrite(pinF, true);
        digitalWrite(pinG, true);
        digitalWrite(pinB, true);
        digitalWrite(pinC, true);
        break;
    case 5:
        digitalWrite(pinA, true);
        digitalWrite(pinF, true);
        digitalWrite(pinG, true);
        digitalWrite(pinC, true);
        digitalWrite(pinD, true);
        break;
    case 6:
        digitalWrite(pinA, true);
        digitalWrite(pinF, true);
        digitalWrite(pinG, true);
        digitalWrite(pinC, true);
        digitalWrite(pinD, true);
        digitalWrite(pinE, true);
        break;
    case 7:
        digitalWrite(pinA, true);
        digitalWrite(pinB, true);
        digitalWrite(pinC, true);
        break;
    case 8:
        digitalWrite(pinA, true);
        digitalWrite(pinB, true);
        digitalWrite(pinC, true);
        digitalWrite(pinD, true);
        digitalWrite(pinE, true);
        digitalWrite(pinF, true);
        digitalWrite(pinG, true);
        break;
    case 9:
        digitalWrite(pinA, true);
        digitalWrite(pinB, true);
        digitalWrite(pinC, true);
        digitalWrite(pinF, true);
        digitalWrite(pinG, true);
        break;
    default:
        break;
    }
}