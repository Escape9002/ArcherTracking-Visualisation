from tokenize import String
from numpy import unicode_
import serial

ser1 = serial.Serial('COM10', 115200, timeout = 1)
ser1.flushInput()
msg1 = ""

ser2 = serial.Serial('COM15', 115200, timeout = 1)
ser2.flushInput()
msg2=""

dataString =""

# kopfzeile = "DataRate=50.000000\nDataType=Quaternion\nversion=3\nOpenSimVersion=4.3-2021-08-27-4bc7ad9\nendheader\ntime\ttorso_imu\tpelvis_imu\n" #\ttorso_imu\ttorso_imu\tpelvis_imu \thumerus_l_imu
kopfzeile = "DataRate=50.000000\nDataType=Quaternion\nversion=3\nOpenSimVersion=4.3-2021-08-27-4bc7ad9\nendheader\ntime\thumerus_l_imu\tulna_l_imu\n" #\ttorso_imu\ttorso_imu\tpelvis_imu \thumerus_l_imu

sec = 10
timer = int(sec / (1/10))
msg = []

print(timer * (1/10))

#trial = "lift_l.sto"
trial = "lift_forw_l.sto"
#trial = "flex_l.sto"
#trial = "wink_l.sto"

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