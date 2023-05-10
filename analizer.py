import matplotlib.pyplot as plt
import numpy as np

def showAnglePlot(angles):
    angles=np.array(angles)
    plt.plot(range(0,len(angles)),angles[::,0], 'r',range(0,len(angles)),angles[::,1],'g',range(0,len(angles)),angles[::,2],'y',range(0,len(angles)),angles[::,3],'b')
    plt.xlabel('frames')
    plt.ylabel('angles')
    plt.legend(["Left elbow", "Right elbow", "Left knee", "Right knee"], loc ="lower right")
    plt.show()