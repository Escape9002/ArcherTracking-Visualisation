/************************************************************
MPU9250_DMP_Quaternion
 Quaternion example for MPU-9250 DMP Arduino Library 
Jim Lindblom @ SparkFun Electronics
original creation date: November 23, 2016
https://github.com/sparkfun/SparkFun_MPU9250_DMP_Arduino_Library

The MPU-9250's digital motion processor (DMP) can calculate
four unit quaternions, which can be used to represent the
rotation of an object.

This exmaple demonstrates how to configure the DMP to 
calculate quaternions, and prints them out to the serial
monitor. It also calculates pitch, roll, and yaw from those
values.

Development environment specifics:
Arduino IDE 1.6.12
SparkFun 9DoF Razor IMU M0

Supported Platforms:
- ATSAMD21 (Arduino Zero, SparkFun SAMD21 Breakouts)
*************************************************************/
/*
 * Some additions concerning the SerialPort-Messages 
 * have been made by Escape9002
 */
#include <SparkFunMPU9250-DMP.h>
#include <iostream>
#include <tuple>
#include <cmath>

// Structure to represent a quaternion
struct Quaternion {
    double w, x, y, z;
};

#define SerialPort SerialUSB

MPU9250_DMP imu;

// Function to multiply two quaternions
Quaternion quaternionMultiply(const Quaternion& q1, const Quaternion& q2) {
    Quaternion result;
    result.w = q1.w * q2.w - q1.x * q2.x - q1.y * q2.y - q1.z * q2.z;
    result.x = q1.w * q2.x + q1.x * q2.w + q1.y * q2.z - q1.z * q2.y;
    result.y = q1.w * q2.y - q1.x * q2.z + q1.y * q2.w + q1.z * q2.x;
    result.z = q1.w * q2.z + q1.x * q2.y - q1.y * q2.x + q1.z * q2.w;
    return result;
}

// Function to invert the roll axis in a quaternion
Quaternion invertRoll(const Quaternion& quaternion) {
    // Correction quaternion for 180° rotation around x-axis
    Quaternion qCorrection = {0, 1, 0, 0};
    return quaternionMultiply(qCorrection, quaternion);
}

// Helper function to print a quaternion
void printQuaternion(const Quaternion& q) {
    std::cout << "Quaternion: (" << q.w << ", " << q.x << ", " << q.y << ", " << q.z << ")\n";
}

void setup() 
{
  SerialPort.begin(115200);

  // Call imu.begin() to verify communication and initialize
  if (imu.begin() != INV_SUCCESS)
  {
    while (1)
    {
      SerialPort.println("Unable to communicate with MPU-9250");
      SerialPort.println("Check connections, and try again.");
      SerialPort.println();
      delay(5000);
    }
  }
  
  imu.dmpBegin(DMP_FEATURE_6X_LP_QUAT | // Enable 6-axis quat
               DMP_FEATURE_GYRO_CAL, // Use gyro calibration
              10); // Set DMP FIFO rate to 10 Hz
  // DMP_FEATURE_LP_QUAT can also be used. It uses the 
  // accelerometer in low-power mode to estimate quat's.
  // DMP_FEATURE_LP_QUAT and 6X_LP_QUAT are mutually exclusive
}

void loop() 
{
  // Check for new data in the FIFO
  if ( imu.fifoAvailable() )
  {
    // Use dmpUpdateFifo to update the ax, gx, mx, etc. values
    if ( imu.dmpUpdateFifo() == INV_SUCCESS)
    {
      // computeEulerAngles can be used -- after updating the
      // quaternion values -- to estimate roll, pitch, and yaw
      imu.computeEulerAngles();
      printIMUData();
    }
  }
}

void printIMUData()
{  
  // After calling dmpUpdateFifo() the ax, gx, mx, etc. values
  // are all updated.
  // Quaternion values are, by default, stored in Q30 long
  // format. calcQuat turns them into a float between -1 and 1
  float q0 = imu.calcQuat(imu.qw);
  float q1 = imu.calcQuat(imu.qx);
  float q2 = imu.calcQuat(imu.qy);
  float q3 = imu.calcQuat(imu.qz);
  Quaternion qoriginal = {q0,q1,q2,q3};

  Quaternion qCorrected = invertRoll(qoriginal);

  q0 = qCorrected.w;
  q1 = qCorrected.x;
  q2 = qCorrected.y;
  q3 = qCorrected.z;

  SerialPort.println( String(q0*100+100,0)+ "," + String(q1*100+100,0) + "," + String(q2*100+100,0)+ "," +String(q3*100+100,0));
 
}
