import serial
import time


def recv(ser):
    while True:
        data = ser.read_all()
        if data == '':
            continue
        else:
            break
        time.sleep(0.5)
    return data


def main():
    ser=serial.Serial("com1", 9600, timeout=0.5)
    if ser.isOpen():
        print("open success")
    else:
        print("open failed")
    ser.close()

    while True:
        data = recv(ser)
        if data != b'':
            print('receive:{0}'.format(data))
            ser.write(data)


if __name__ == '__main__':
    main()        
