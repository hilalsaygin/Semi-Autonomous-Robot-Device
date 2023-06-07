#ifndef COMMAND_H
#define COMMAND_H

#include <string>

class COMMAND {
public:
    static const std::string CMD_MOVE_STOP;
    static const std::string CMD_MOVE_FORWARD;
    static const std::string CMD_MOVE_BACKWARD;
    static const std::string CMD_MOVE_LEFT;
    static const std::string CMD_MOVE_RIGHT;
    static const std::string CMD_TURN_LEFT;
    static const std::string CMD_TURN_RIGHT;
    static const std::string CMD_BUZZER;
    static const std::string CMD_LED_MOD;
    static const std::string CMD_LED;
    static const std::string CMD_BALANCE;
    static const std::string CMD_SONIC;
    static const std::string CMD_HEIGHT;
    static const std::string CMD_HORIZON;
    static const std::string CMD_HEAD;
    static const std::string CMD_CALIBRATION;
    static const std::string CMD_POWER;
    static const std::string CMD_ATTITUDE;
    static const std::string CMD_RELAX;
    static const std::string CMD_WORKING_TIME;
};
    const std::string CMD_MOVE_STOP = "CMD_MOVE_STOP";
    const std::string CMD_MOVE_FORWARD = "CMD_MOVE_FORWARD";
    const std::string CMD_MOVE_BACKWARD = "CMD_MOVE_BACKWARD";
    const std::string CMD_MOVE_LEFT = "CMD_MOVE_LEFT";
    const std::string CMD_MOVE_RIGHT = "CMD_MOVE_RIGHT";
    const std::string CMD_TURN_LEFT = "CMD_TURN_LEFT";
    const std::string CMD_TURN_RIGHT = "CMD_TURN_RIGHT";
    const std::string CMD_BUZZER = "CMD_BUZZER";
    const std::string CMD_LED_MOD = "CMD_LED_MOD";
    const std::string CMD_LED = "CMD_LED";
    const std::string CMD_BALANCE = "CMD_BALANCE";
    const std::string CMD_SONIC = "CMD_SONIC";
    const std::string CMD_HEIGHT = "CMD_HEIGHT";
    const std::string CMD_HORIZON = "CMD_HORIZON";
    const std::string CMD_HEAD = "CMD_HEAD";
    const std::string CMD_CALIBRATION = "CMD_CALIBRATION";
    const std::string CMD_POWER = "CMD_POWER";
    const std::string CMD_WORKING_TIME = "CMD_WORKING_TIME";
#endif
