# To use this module to predict the travel time from u -> v where u = (lat,long), v = (lat,long) : 
# 
# from module.delivery_model import DeliveryModel
# deliveryModel = DeliveryModel()
# u=(13.840180,100.542326) 
# v=(13.803957,100.513704)
# predictedDuration = deliveryModel.predict(u,v)[0]
# 
# predictedDuration will be the total time in minute 
# 

import pickle as pkl
import numpy as np
from math import * 
from module.distance_calculator import DistanceCalculator 
from sklearn.ensemble import GradientBoostingRegressor

class DeliveryModel: 
    def __init__(self):
        self.model = pkl.load(open('gbdt_m_delivery.pkl', 'rb'))
        self.distanceCalculator = DistanceCalculator()
        self.dayMap = {"MON":0, "TUE":1, "WED":2, "THU":3, "FRI":4, "SAT":5, "SUN":6}

    def get_euc(self,coords_1, coords_2):
        R = 6371000; conversion_const = 0.0174533
        c_1 = (coords_1[0]*conversion_const, coords_1[1]*conversion_const)
        c_2 = (coords_2[0]*conversion_const, coords_2[1]*conversion_const)
        delta_phi = abs(c_1[1]-c_2[1])
        theta = c_1[0]
        delta_theta = abs(c_1[0]-c_2[0])
        del_x = R*cos(theta)*delta_phi 
        del_y = R*delta_theta
        return sqrt(del_x**2 + del_y**2)

    def predict(self, u, v, day_of_week="MON"):

        '''
        input:
        - u = (lat,long) of merchant location 
        - v = (lat,long) of customer location
        - (optional) day_of_week: choose one of these -> "MON", "TUE, "WED", "THU", "FRI", "SAT", "SUN"
        
        output:
        - The prediction of the duration in minute (m) needed to travel from point u to point v 
        (please note that if you want to predict the duration needed from rider currently at point x and need to pick up food at point y and deliver at point z, you need to calculate the time it takes for x to go to y and the time it takes from a rider to from y to z)
        '''
        
        merchant_lat = u[0]
        merchant_long = u[1]

        customer_lat = v[0]
        customer_long = v[1]

        EucDist = self.get_euc(u,v)
        ShortestDist = self.distanceCalculator.shortestDistance(u,v)

        day_of_week_sin = np.sin(self.dayMap[day_of_week]*(2.*np.pi/7))
        day_of_week_cos = np.cos(self.dayMap[day_of_week]*(2.*np.pi/7))
        
        inp = [[merchant_lat, merchant_long, customer_lat, customer_long, EucDist, ShortestDist, day_of_week_sin, day_of_week_cos]]
        return self.model.predict(inp)
