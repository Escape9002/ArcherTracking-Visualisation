# from numpy import unicode_
import serial

ser = serial.Serial('COM9', 115200, timeout = 1)
ser.flushInput()

kopfzeile = "DataRate=50.000000\nDataType=Quaternion\nversion=3\nOpenSimVersion=4.3-2021-08-27-4bc7ad9\nendheader\ntime\tpelvis_imu\ttorso_imu\n" #\thumerus_l_imu\ttorso_imu\tulna_l_imu \thumerus_l_imu

sec = 10
timer = int(sec / (1/10))
msg = []

print(timer * (1/10))

with open('Table.sto', 'w') as data:
    data.write(kopfzeile)

    for i in range(timer+1):
        line = ser.readline()   # read a byte
        if line:
            string = (line.decode().replace("\n","").replace("b",""))  # convert the byte string to a unicode string and replace \n with emptyness
            #print(str(i) +"\t"+string)
            values = string.split(",")
            for dat in values:
                msg.append((int(dat) -100) / 100)
            mag = str(i) + "\t" + str(msg[0]) +"," + str(msg[1]) +","+ str(msg[2]) +","+ str(msg[3]) + "\n"
            print(mag)
            data.write(mag)
            msg.clear()
            mag= ""