import time
import serial

arduino = serial.Serial()
arduino.port = 'COM5'
arduino.baudrate = 9600
arduino.timeout = 0.1
arduino.setRTS(False)

arduino.open()
arduino.flush()
#outgoing = "Hi\n"
#arduino.write(outgoing.encode())
#print(outgoing)
#arduino.flush()


#while True:
#    print("Hello from Raspberry Pi!")
#    arduino.write(b"Hello from Raspberry Pi!\n")
#    line = arduino.readline().decode('utf-8').rstrip()
#    print(line)
#    time.sleep(1)
#    #if arduino.in_waiting > 0:
#        #line = arduino.readline().decode('utf-8').rstrip()
#        #print(line)

while True:
    incoming = arduino.read()
    print(int.from_bytes(incoming, byteorder='big'))
    if incoming != b'':
        if int.from_bytes(incoming, byteorder='big') == 10:
            arduino.write(b"bay1\n")
            print("bay 1")
        elif int.from_bytes(incoming, byteorder='big') == 1:
            arduino.write(b"bay2\n")
        elif int.from_bytes(incoming, byteorder='big') == 2:
            arduino.write(b"bay3\n")
        elif int.from_bytes(incoming, byteorder='big') == 3:
            arduino.write(b"bay4\n")
        elif int.from_bytes(incoming, byteorder='big') == 4:
            arduino.write(b"bay5\n")
        elif int.from_bytes(incoming, byteorder='big') == 5:
            arduino.write(b"bay6\n")
        elif int.from_bytes(incoming, byteorder='big') == 6:
            arduino.write(b"Good Talk!\n")
            print("Complete!")
            arduino.flush()
        elif int.from_bytes(incoming, byteorder='big') == 16:
            print("Arduino Waiting!")
    else:
        arduino.write(b"listen\n")
        print("calling")



