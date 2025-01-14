import csv

def load_data(header, fileName):
    dataArray1 = []
    outputArray = []
    with open(fileName, newline='') as csvfile:
        file = csv.reader(csvfile, delimiter=' ')

        i=0
        while i < header:
            i = i+ 1
            next(file)
        
        for row in file:
            for data in row:
                dataArray1.append(data.split("\t"))

        for data in dataArray1:
            outputArray.append(data[1] + "\t" + data[2])
    print(outputArray)
    return outputArray

def write_data(filename,kopfzeile,data1, data2):
    with open(filename, 'w') as data:
        data.write(kopfzeile)
        i = 0
        while i < len(data1):
            msg = str(i) + "\t" + str(data1[i]) + "\t" + str(data2[i]) + "\n"
            i = i+1
            data.write(msg)

huefte = load_data(6, 'table_flat_30.sto')
wink = load_data(6,'arm_move_2_all_direcions_inverse.sto')
# lift = load_data(6,'lift_l.sto')
# lift_for = load_data(6,'lift_forw_l.sto')
# flex = load_data(6,'flex_l.sto')

write_data('appendData_armMove.sto',
    "DataRate=50.000000\nDataType=Quaternion\nversion=3\nOpenSimVersion=4.3-2021-08-27-4bc7ad9\nendheader\ntime\ttorso_imu\tpelvis_imu\thumerus_l_imu\tulna_l_imu\n",huefte,wink)

# write_data('appendData_lift_l.sto',
#     "DataRate=50.000000\nDataType=Quaternion\nversion=3\nOpenSimVersion=4.3-2021-08-27-4bc7ad9\nendheader\ntime\ttorso_imu\tpelvis_imu\thumerus_l_imu\tulna_l_imu\n",huefte,lift)

# write_data('appendData_lift_forw_l.sto',
#     "DataRate=50.000000\nDataType=Quaternion\nversion=3\nOpenSimVersion=4.3-2021-08-27-4bc7ad9\nendheader\ntime\ttorso_imu\tpelvis_imu\thumerus_l_imu\tulna_l_imu\n",huefte,lift_for)

# write_data('appendData_flex_l.sto',
#     "DataRate=50.000000\nDataType=Quaternion\nversion=3\nOpenSimVersion=4.3-2021-08-27-4bc7ad9\nendheader\ntime\ttorso_imu\tpelvis_imu\thumerus_l_imu\tulna_l_imu\n",huefte,flex)
