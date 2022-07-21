#ifndef SEGMENT_H_
#define SEGMENT_H_

#include <Arduino.h>
#include <Vector.h>

class Segment {
    public:
        Segment(
            int pinA = 22,
            int pinB = 23,
            int pinC = 24,
            int pinD = 25,
            int pinE = 26,
            int pinF = 27,
            int pinG = 28,
            int pinDot = 29
        );
        void print(unsigned int number);
        void PrintDigit(unsigned char c);
    private:
        void reset();
        int pinA, pinB, pinC, pinD, pinE, pinF, pinG, pinDot;
};

#endif