import serial

ser=serial.Serial("com1", 9600, timeout=0.5)

ser.close()
