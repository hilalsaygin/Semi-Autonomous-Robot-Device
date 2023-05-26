#include <iostream>
#include <wiringPiI2C.h>
#include <wiringPi.h>
#include <cmath>

class PCA9685 {
private:
  const int __SUBADR1 = 0x02;
  const int __SUBADR2 = 0x03;
  const int __SUBADR3 = 0x04;
  const int __MODE1 = 0x00;
  const int __PRESCALE = 0xFE;
  const int __LED0_ON_L = 0x06;
  const int __LED0_ON_H = 0x07;
  const int __LED0_OFF_L = 0x08;
  const int __LED0_OFF_H = 0x09;
  const int __ALLLED_ON_L = 0xFA;
  const int __ALLLED_ON_H = 0xFB;
  const int __ALLLED_OFF_L = 0xFC;
  const int __ALLLED_OFF_H = 0xFD;

  int address;
  int fd;
  bool debug;

public:
  PCA9685(int addr = 0x40, bool dbg = false) {
    address = addr;
    debug = dbg;
    fd = wiringPiI2CSetup(address);
    reset();
  }

  void reset() {
    write(__MODE1, 0x00);
  }

  void write(int reg, int value) {
    wiringPiI2CWriteReg8(fd, reg, value);
  }

  int read(int reg) {
    return wiringPiI2CReadReg8(fd, reg);
  }

  void setPWMFreq(float freq) {
    float prescaleval = 25000000.0; // 25MHz
    prescaleval /= 4096.0;          // 12-bit
    prescaleval /= freq;
    prescaleval -= 1.0;
    int prescale = std::floor(prescaleval + 0.5);

    int oldmode = read(__MODE1);
    int newmode = (oldmode & 0x7F) | 0x10; // sleep
    write(__MODE1, newmode);               // go to sleep
    write(__PRESCALE, std::floor(prescale));
    write(__MODE1, oldmode);
    delay(5);
    write(__MODE1, oldmode | 0x80);
  }

  void setPWM(int channel, int on, int off) {
    write(__LED0_ON_L + 4 * channel, on & 0xFF);
    write(__LED0_ON_H + 4 * channel, on >> 8);
    write(__LED0_OFF_L + 4 * channel, off & 0xFF);
    write(__LED0_OFF_H + 4 * channel, off >> 8);
  }

  void setMotorPwm(int channel, int duty) {
    setPWM(channel, 0, duty);
  }

  void setServoPulse(int channel, int pulse) {
    pulse = pulse * 4096 / 20000; // PWM frequency is 50Hz, the period is 20000us
    setPWM(channel, 0, pulse);
  }
};

 
