#include <iostream>
#include "PCA9685.h"
#include <unistd.h>

class Servo {
private:
    int angleMin = 18;
    int angleMax = 162;
    PCA9685 pwm;

public:
    Servo()  : pwm(0x40, true){
        
        pwm.setPWMFreq(50);
    }

    int map(int value, int fromLow, int fromHigh, int toLow, int toHigh) {
        return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow;
    }

    void setServoAngle(int channel, int angle) {
        if (angle < angleMin) {
            angle = angleMin;
        } else if (angle > angleMax) {
            angle = angleMax;
        }
        int pulse = map(angle, 0, 180, 102, 512);
        pwm.setPWM(channel, 0, pulse);
    }
};

int main() {
    /*std::cout << "Now servos will rotate to 90°." << std::endl;
    std::cout << "If they have already been at 90°, nothing will be observed." << std::endl;
    std::cout << "Please keep the program running when installing the servos." << std::endl;
    std::cout << "After that, you can press ctrl-C to end the program." << std::endl;
*/
    Servo servo;

    servo.setServoAngle(13, 60);
    //servo.setServoAngle(5, 90);
    //servo.setServoAngle(10, 90);
    //servo.setServoAngle(13, 90);

    return 0;
}
