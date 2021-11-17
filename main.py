import numpy as np
import os 
import matplotlib.pyplot as plt
from SaM import laserscan

#read in file:
def readData(path):
    print(path)
    try:
        with open(path, 'r') as l:
            lasers = []
            # first, go through the laser file
            for line in l:
                tokens = line.split(' ')
                if tokens[0] == 'LASER':
                    # get amount of readings
                    num_readings = int(tokens[2])
                    # get opening angle from laser
                    opening_angle = float(tokens[3])
                    # get each laser range from scan
                    scans = np.array(tokens[4:4+num_readings], dtype=np.float64)
                    noise = np.random.normal(-0.03,0.03,len(scans))
                    scans = scans+noise
                    # get angle of each beam 
                    index = np.arange(-opening_angle/2, opening_angle/2 + opening_angle/num_readings, opening_angle/num_readings)
                    angles = np.delete(index, num_readings//2)
                    converted_scans = []
                    converted_scans = np.array([np.cos(angles), np.sin(angles)]).T * scans[:, np.newaxis]

                    lasers.append(np.array(converted_scans))

       

        return lasers, num_readings, opening_angle
    
    except:
        print(path, " is not a correct path. Check it!!")


if __name__ == "__main__":

    path = os.getcwd() + '/laserscanner_data.txt'

    laser_data, num_readings, opening_angle = readData(path)
    for laser in laser_data:
        x,y=[],[]
        for elem in laser:
            x.append(elem[0])
            y.append(elem[1])

        ls = laserscan(x,y, 10, 0.2 , num_readings, opening_angle)
        _ = ls.get_corners(filter=1)

        plt.plot(x,y,'.')
        plt.xlim([-10,10])
        plt.ylim([-10,10])
        plt.show()

        for elem in ls.line_clusters:
            x_,y_ = [],[]
            for point in elem:
                x_.append(point[0])
                y_.append(point[1])
            plt.scatter(x_,y_)
        
        x_,y_ = [],[]
        for point in ls.corners:
            x_.append(point[0])
            y_.append(point[1])
        plt.scatter(x_,y_,color='lime')

        plt.xlim([-10,10])
        plt.ylim([-10,10])
        plt.show()