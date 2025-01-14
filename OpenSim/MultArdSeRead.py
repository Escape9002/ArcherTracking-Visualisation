from tokenize import String
# from numpy import unicode_
import serial

ser1 = serial.Serial('COM9', 115200, timeout = 1)
ser1.flushInput()
msg1 = ""

ser2 = serial.Serial('COM7', 115200, timeout = 1)
ser2.flushInput()
msg2=""

dataString =""

# kopfzeile = "DataRate=50.000000\nDataType=Quaternion\nversion=3\nOpenSimVersion=4.3-2021-08-27-4bc7ad9\nendheader\ntime\ttorso_imu\tpelvis_imu\n" #\ttorso_imu\ttorso_imu\tpelvis_imu \thumerus_l_imu
kopfzeile = "DataRate=50.000000\nDataType=Quaternion\nversion=3\nOpenSimVersion=4.3-2021-08-27-4bc7ad9\nendheader\ntime\thumerus_l_imu\tulna_l_imu\n" #\ttorso_imu\ttorso_imu\tpelvis_imu \thumerus_l_imu

sec = 30
timer = int(sec / (1/10))
msg = []

print(timer * (1/10))

#trial = "lift_l.sto"
# trial = "table_move_1_yaw.sto"
# trial ="table_spin_body.sto"
# trial = "table_move_1_pitch.sto"
# trial = "table_move_1_roll.sto"
# trial = "table_move_1_roll_inverse.sto"
# trial = "table_move_1_pitch_pitch.sto"
# trial = "arm_move_1_pitch_pitch.sto"
# trial = "table_flat_30.sto"
trial = "arm_move_2_all_direcions_inverse.sto"

with open(trial, 'w') as data:
    data.write(kopfzeile)

    for i in range(timer):
        line1 = ser1.readline()   # read a byte
        line2 = ser2.readline()   # read a byte
        if line1 and line2:
            string = (line1.decode().replace("\n","").replace("b",""))  # convert the byte string to a unicode string and replace \n with emptyness
            #print(str(i) +"\t"+string)
            values = string.split(",")
            for dat in values:
                msg.append((int(dat) -100) / 100)
            msg1 = str(msg[0]) +"," + str(msg[1]) +","+ str(msg[2]) +","+ str(msg[3]) 
            msg.clear()
            #print("1:"+ msg1)
            
            #####################################################################################################################################

            string = (line2.decode().replace("\n","").replace("b",""))  # convert the byte string to a unicode string and replace \n with emptyness
            #print(str(i) +"\t"+string)
            values = string.split(",")
            for dat in values:
                msg.append((int(dat) -100) / 100)
            msg2 =str(msg[0]) +"," + str(msg[1]) +","+ str(msg[2]) +","+ str(msg[3])
            msg.clear()
            #print("2:" + msg2)
            
        
        dataString = str(i) + "\t" + msg1 + "\t" + msg2 + "\n"
        print(dataString)
        data.write(dataString)

ser1.close()
ser2.close()