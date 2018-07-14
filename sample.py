# -*- coding: utf-8 -*-
import numpy as np
index = np.random.randint(0,2012,size=(1,5))
print(index)
with open('couple_city.txt','r') as file:
    with open('couple_city_sample.txt', 'w',encoding='utf-8') as targetfile:  
        count = 1
        for line in file.readlines():
            if count in index:
                targetfile.write(line)
            count += 1