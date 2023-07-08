#ifndef INCREMENTAL_PID_H
#define INCREMENTAL_PID_H

class Incremental_PID {
private:
    double setPoint;
    double Kp;
    double Ki;
    double Kd;
    double last_error;
    double P_error;
    double I_error;
    double D_error;
    double I_saturation;
    double output;

public:
    Incremental_PID(double P=0.0, double I=0.0, double D=0.0);
    double PID_compute(double feedback_val);
    void setKp(double proportional_gain);
    void setKi(double integral_gain);
    void setKd(double derivative_gain);
    void setI_saturation(double saturation_val);
};

#endif // INCREMENTAL_PID_H

// Implementations

Incremental_PID::Incremental_PID(double P, double I, double D) {
    setPoint = 0.0;
    Kp = P;
    Ki = I;
    Kd = D;
    last_error = 0.0;
    P_error = 0.0;
    I_error = 0.0;
    D_error = 0.0;
    I_saturation = 10.0;
    output = 0.0;
}

double Incremental_PID::PID_compute(double feedback_val) {
    double error = setPoint - feedback_val;
    P_error = Kp * error;
    I_error += error;
    D_error = Kd * (error - last_error);
    if (I_error < -I_saturation) {
        I_error = -I_saturation;
    } else if (I_error > I_saturation) {
        I_error = I_saturation;
    }
    output = P_error + (Ki * I_error) + D_error;
    last_error = error;
    return output;
}

void Incremental_PID::setKp(double proportional_gain) {
    Kp = proportional_gain;
}

void Incremental_PID::setKi(double integral_gain) {
    Ki = integral_gain;
}

void Incremental_PID::setKd(double derivative_gain) {
    Kd = derivative_gain;
}

void Incremental_PID::setI_saturation(double saturation_val) {
    I_saturation = saturation_val;
}
