#ifndef __SCALE_HPP__
#define __SCALE_HPP__

#include <HX711.h>

class Scale {
    public:
        Scale(int DatPin = 8, int SckPin = 9);
        ~Scale();
        double getWeight();
        void tare();

    private:
        int DatPin, SckPin;
        HX711 scale;
        
};

#endif