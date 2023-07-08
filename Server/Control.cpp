#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <tuple>
#include <thread>
#include <sstream>
#include "Command.h"
#include "PID.h"
#include "Servo.cpp"
using namespace std;
class Control {
private:
    COMMAND cmd;
    Servo servo;
    Incremental_PID pid;
    int speed;
    int height;
    int timeout;
    int move_flag;
    int move_count;
    int move_timeout;
    vector<string> order;
    vector<vector<int>> point;
    vector<vector<int>> calibration_point;
    vector<vector<int>> angle;
    vector<vector<int>> calibration_angle;
    bool relax_flag;
    bool balance_flag;
    bool attitude_flag;
    thread Thread_conditiona;

public:
    Control() : pid(0.5, 0.0, 0.0025) {
        speed = 8;
        height = 99;
        timeout = 0;
        move_flag = 0;
        move_count = 0;
        move_timeout = 0;
        order = {"", "", "", "", ""};
        point = {{0, 99, 10}, {0, 99, 10}, {0, 99, -10}, {0, 99, -10}};
        calibration_point = readFromTxt("point");
        angle = {{90, 0, 0}, {90, 0, 0}, {90, 0, 0}, {90, 0, 0}};
        calibration_angle = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}, {0, 0, 0}};
        relax_flag = true;
        balance_flag = false;
        attitude_flag = false;
        calibration();
    }

    vector<vector<int>> readFromTxt(const string& filename) {
        ifstream file(filename + ".txt");
        vector<vector<int>> list_source;
        string line;
        while (getline(file, line)) {
            vector<int> column_list;
            istringstream iss(line);
            string value;
            while (iss >> value) {
                column_list.push_back(stoi(value));
            }
            list_source.push_back(column_list);
        }
        file.close();
        return list_source;
    }

    void saveToTxt(const vector<vector<int>>& list, const string& filename) {
        ofstream file(filename + ".txt");
        for (const auto& row : list) {
            for (const auto& value : row) {
                file << value << '\t';
            }
            file << '\n';
        }
        file.close();
    }
    tuple<double, double, double> coordinateToAngle(double x, double y, double z) {
    double l1 = 23,l2 = 55,l3 = 55;
    double a = M_PI / 2 - atan2(z, y);
    double x_3 = 0;
    double x_4 = l1 * sin(a);
    double x_5 = l1 * cos(a);
    double l23 = sqrt(pow(z - x_5, 2) + pow(y - x_4, 2) + pow(x - x_3, 2));
    double w = (x - x_3) / l23;
    double v = (pow(l2, 2) + pow(l23, 2) - pow(l3, 2)) / (2 * l2 * l23);
    double b = asin(round(w * 100) / 100) - acos(round(v * 100) / 100);
    double c = M_PI - acos(round((pow(l2, 2) + pow(l3, 2) - pow(l23, 2)) / (2 * l3 * l2)) * 100) / 100;
    double deg_a = round(a * 180 / M_PI);
    double deg_b = round(b * 180 / M_PI);
    double deg_c = round(c * 180 / M_PI);
    return make_tuple(deg_a, deg_b, deg_c);
}

tuple<double, double, double> angleToCoordinate(double a, double b, double c) {
    double l1 = 23,  l2 = 55,  l3 = 55;
    double rad_a = M_PI / 180 * a;
    double rad_b = M_PI / 180 * b;
    double rad_c = M_PI / 180 * c;
    double x = l3 * sin(rad_b + rad_c) + l2 * sin(rad_b);
    double y = l3 * sin(rad_a) * cos(rad_b + rad_c) + l2 * sin(rad_a) * cos(rad_b) + l1 * sin(rad_a);
    double z = l3 * cos(rad_a) * cos(rad_b + rad_c) + l2 * cos(rad_a) * cos(rad_b) + l1 * cos(rad_a);
    return make_tuple(x, y, z);
}
void calibration() {
    for (int i = 0; i < 4; i++) {
        auto calibration_angles = coordinateToAngle(calibration_point[i][0], calibration_point[i][1], calibration_point[i][2]);
        calibration_angle[i][0] = get<0>(calibration_angles);
        calibration_angle[i][1] = get<1>(calibration_angles);
        calibration_angle[i][2] = get<2>(calibration_angles);
    }

    for (int i = 0; i < 4; i++) {
        auto angles = coordinateToAngle(point[i][0], point[i][1], point[i][2]);
        angle[i][0] = get<0>(angles);
        angle[i][1] = get<1>(angles);
        angle[i][2] = get<2>(angles);
    }

    for (int i = 0; i < 4; i++) {
        calibration_angle[i][0] -= angle[i][0];
        calibration_angle[i][1] -= angle[i][1];
        calibration_angle[i][2] -= angle[i][2];
    }
}
double restriction(double var, double v_min, double v_max)
{
    if (var < v_min)
        return v_min;
    else if (var > v_max)
        return v_max;
    else
        return var;
}
bool checkPoint() {
        bool flag = true;
        vector<double> leg_length(6, 0.0);

        for (int i = 0; i < 4; i++) {
            leg_length[i] = sqrt(pow(point[i][0], 2) + pow(point[i][1], 2) + pow(point[i][2], 2));
        }

        for (int i = 0; i < 4; i++) {
            if (leg_length[i] > 130 || leg_length[i] < 25) {
                flag = false;
            }
        }

        return flag;
}
 void run() {
        if (checkPoint()) {
            try {
                for (int i = 0; i < 4; i++) {
                    auto angles = coordinateToAngle(point[i][0], point[i][1], point[i][2]);
                     angle[i][0] = get<0>(angles);
                    angle[i][1] = get<1>(angles);
                    angle[i][2] = get<2>(angles);
                }

                for (int i = 0; i < 2; i++) {
                    angle[i][0] = restriction(angle[i][0] + calibration_angle[i][0], 0, 180);
                    angle[i][1] = restriction(90 - (angle[i][1] + calibration_angle[i][1]), 0, 180);
                    angle[i][2] = restriction(angle[i][2] + calibration_angle[i][2], 0, 180);
                    angle[i + 2][0] = restriction(angle[i + 2][0] + calibration_angle[i + 2][0], 0, 180);
                    angle[i + 2][1] = restriction(90 + angle[i + 2][1] + calibration_angle[i + 2][1], 0, 180);
                    angle[i + 2][2] = restriction(180 - (angle[i + 2][2] + calibration_angle[i + 2][2]), 0, 180);
                }

                for (int i = 0; i < 2; i++) {
                    servo.setServoAngle(4 + i * 3, angle[i][0]);
                    servo.setServoAngle(3 + i * 3, angle[i][1]);
                    servo.setServoAngle(2 + i * 3, angle[i][2]);
                    servo.setServoAngle(8 + i * 3, angle[i + 2][0]);
                    servo.setServoAngle(9 + i * 3, angle[i + 2][1]);
                    servo.setServoAngle(10 + i * 3, angle[i + 2][2]);
                }
            } catch (const exception& e) {
                // Hata yönetimini burada yapabilirsiniz
            }
        } else {
            cout << "This coordinate point is out of the active range" << endl;
        }
}
double map(double value, double fromLow, double fromHigh, double toLow, double toHigh) {
    return (toHigh - toLow) * (value - fromLow) / (fromHigh - fromLow) + toLow;
}
void changeCoordinates(string move_order, int X1 = 0, int Y1 = 96, int Z1 = 0,
                           int X2 = 0, int Y2 = 96, int Z2 = 0,
                           vector<vector<int>> pos = vector<vector<int>>(3, vector<int>(4, 0))) {
        if (move_order == "turnLeft") {
            for (int i = 0; i < 2; i++) {
                point[2 * i][0] = pow(-1, 1 + i) * X1 + 10;
                point[2 * i][1] = Y1;
                point[2 * i][2] = pow(-1, i) * Z1 + pow(-1, i) * 10;
                point[1 + 2 * i][0] = pow(-1, 1 + i) * X2 + 10;
                point[1 + 2 * i][1] = Y2;
                point[1 + 2 * i][2] = pow(-1, 1 + i) * Z2 + pow(-1, i) * 10;
            }
        } else if (move_order == "turnRight") {
            for (int i = 0; i < 2; i++) {
                point[2 * i][0] = pow(-1, i) * X1 + 10;
                point[2 * i][1] = Y1;
                point[2 * i][2] = pow(-1, 1 + i) * Z1 + pow(-1, i) * 10;
                point[1 + 2 * i][0] = pow(-1, i) * X2 + 10;
                point[1 + 2 * i][1] = Y2;
                point[1 + 2 * i][2] = pow(-1, i) * Z2 + pow(-1, i) * 10;
            }
        } else if (move_order == "height" || move_order == "horizon") {
            for (int i = 0; i < 2; i++) {
                point[3 * i][0] = X1 + 10;
                point[3 * i][1] = Y1;
                point[1 + i][0] = X2 + 10;
                point[1 + i][1] = Y2;
            }
        } else if (move_order == "Attitude Angle") {
            for (int i = 0; i < 2; i++) {
                point[3 - i][0] = pos[0][1 + 2 * i] + 10;
                point[3 - i][1] = pos[2][1 + 2 * i];
                point[3 - i][2] = pos[1][1 + 2 * i];
                point[i][0] = pos[0][2 * i] + 10;
                point[i][1] = pos[2][2 * i];
                point[i][2] = pos[1][2 * i];
            }
        } else {
            for (int i = 0; i < 2; i++) {
                point[i * 2][0] = X1 + 10;
                point[i * 2][1] = Y1;
                point[i * 2 + 1][0] = X2 + 10;
                point[i * 2 + 1][1] = Y2;
                point[i * 2][2] = Z1 + pow(-1, i) * 10;
                point[i * 2 + 1][2] = Z2 + pow(-1, i) * 10;
            }
        }
        run();
}
void backWard() {
        for (int i = 450; i >= 89; i -= speed) {
            double angle = i * M_PI / 180.0;
            double X1 = 12 * cos(angle);
            double Y1 = 6 * sin(angle) + height;
            double X2 = 12 * cos((angle + 180) * M_PI / 180.0);
            double Y2 = 6 * sin((angle + 180) * M_PI / 180.0) + height;

            if (Y2 > height) {
                Y2 = height;
            }
            if (Y1 > height) {
                Y1 = height;
            }

            changeCoordinates("backWard", X1, Y1, 0, X2, Y2, 0);

            this_thread::sleep_for(chrono::milliseconds(10));
        }
}
void forWard() {
        for (int i = 90; i <= 451; i += speed) {
            double angle = i * M_PI / 180.0;
            double X1 = 12 * cos(angle);
            double Y1 = 6 * sin(angle) + height;
            double X2 = 12 * cos((angle + 180) * M_PI / 180.0);
            double Y2 = 6 * sin((angle + 180) * M_PI / 180.0) + height;

            if (Y2 > height) {
                Y2 = height;
            }
            if (Y1 > height) {
                Y1 = height;
            }

            changeCoordinates("forWard", X1, Y1, 0, X2, Y2, 0);

            this_thread::sleep_for(chrono::milliseconds(10));
        }
}

void turnLeft() {
        for (int i = 0; i <= 361; i += speed) {
            double angle = i * M_PI / 180.0;
            double X1 = 3 * cos(angle);
            double Y1 = 8 * sin(angle) + height;
            double X2 = 3 * cos((angle + 180) * M_PI / 180.0);
            double Y2 = 8 * sin((angle + 180) * M_PI / 180.0) + height;

            if (Y2 > height) {
                Y2 = height;
            }
            if (Y1 > height) {
                Y1 = height;
            }

            double Z1 = X1;
            double Z2 = X2;

            changeCoordinates("turnLeft", X1, Y1, Z1, X2, Y2, Z2);

            this_thread::sleep_for(chrono::milliseconds(10));
        }
}

void turnRight() {
        for (int i = 0; i <= 361; i += speed) {
            double angle = i * M_PI / 180.0;
            double X1 = 3 * cos(angle);
            double Y1 = 8 * sin(angle) + height;
            double X2 = 3 * cos((angle + 180) * M_PI / 180.0);
            double Y2 = 8 * sin((angle + 180) * M_PI / 180.0) + height;

            if (Y2 > height) {
                Y2 = height;
            }
            if (Y1 > height) {
                Y1 = height;
            }

            double Z1 = X1;
            double Z2 = X2;

            changeCoordinates("turnRight", X1, Y1, Z1, X2, Y2, Z2);

            this_thread::sleep_for(chrono::milliseconds(10));
        }
}
void stop() {
        vector<vector<int>> p = {{10, height, 10}, {10, height, 10}, {10, height, -10}, {10, height, -10}};
        
        for (int i = 0; i < 4; i++) {
            p[i][0] = (p[i][0] - point[i][0]) / 50;
            p[i][1] = (p[i][1] - point[i][1]) / 50;
            p[i][2] = (p[i][2] - point[i][2]) / 50;
        }
        
        for (int j = 0; j < 50; j++) {
            for (int i = 0; i < 4; i++) {
                point[i][0] += p[i][0];
                point[i][1] += p[i][1];
                point[i][2] += p[i][2];
            }
            run();

            this_thread::sleep_for(chrono::milliseconds(10));
        }
}

void setpLeft() {
        for (int i = 90; i <= 451; i += speed) {
            double Z1 = 10 * cos(i * M_PI / 180.0);
            double Y1 = 5 * sin(i * M_PI / 180.0) + height;
            double Z2 = 10 * cos((i + 180) * M_PI / 180.0);
            double Y2 = 5 * sin((i + 180) * M_PI / 180.0) + height;

            if (Y1 > height) {
                Y1 = height;
            }
            if (Y2 > height) {
                Y2 = height;
            }

            changeCoordinates("setpLeft", 0, Y1, Z1, 0, Y2, Z2);

            this_thread::sleep_for(chrono::milliseconds(10));
        }
}

void setpRight() {
        for (int i = 450; i >= 89; i -= speed) {
            double Z1 = 10 * cos(i * M_PI / 180.0);
            double Y1 = 5 * sin(i * M_PI / 180.0) + height;
            double Z2 = 10 * cos((i + 180) * M_PI / 180.0);
            double Y2 = 5 * sin((i + 180) * M_PI / 180.0) + height;

            if (Y1 > height) {
                Y1 = height;
            }
            if (Y2 > height) {
                Y2 = height;
            }

            changeCoordinates("setpRight", 0, Y1, Z1, 0, Y2, Z2);

            this_thread::sleep_for(chrono::milliseconds(10));
        }
}


void upAndDown(int var) {
        height = var + 99;
        changeCoordinates("height", 0, height, 0, 0, height, 0);
}

void beforeAndAfter(int var) {
        changeCoordinates("horizon", var, height, 0, var, height, 0);
}

};

