import DriverMP
import os


if __name__ == '__main__':

    try:

        newpid = os.fork()

        if newpid > 0:
            print(str(os.getpid()))
            execfile('DriverMP.py')
                        

        if(newpid == 0):
            print("Child")
            execfile('DriverMP.py')

    except KeyboardInterrupt:
        print("Measurement stopped by user")

