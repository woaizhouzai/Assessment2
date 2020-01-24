# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:08:13 2020

@author: ZHOU_YuZHAO
"""

import numpy as np
import csv

class Read():
    def readFromFile(self,filename):
        data = []
        with open(filename, "r") as csvfile:
            # The data is returned with each row of data as a list
            reader = csv.reader(csvfile)
            for row in reader:
            # Output the row list
                line = []
                for x in row:
                    line.append(int(x))
                data.append(line)
        
        return np.array(data)