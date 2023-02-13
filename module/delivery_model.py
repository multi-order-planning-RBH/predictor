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
# from module.distance_calculator import DistanceCalculator 
from distance_calculator import DistanceCalculator 
from sklearn.ensemble import GradientBoostingRegressor

class DeliveryModel: 
    def __init__(self):
        self.model = pkl.load(open('gbdt_m_delivery.pkl', 'rb'))
        self.distanceCalculator = DistanceCalculator()
        self.dayMap = {"MON":0, "TUE":1, "WED":2, "THU":3, "FRI":4, "SAT":5, "SUN":6}

    def get_euc(self,coords_1, coords_2):
        R = 6371000
        conversion_const = 0.0174533
        c_1 = (coords_1[0]*conversion_const, coords_1[1]*conversion_const)
        c_2 = (coords_2[0]*conversion_const, coords_2[1]*conversion_const)
        delta_phi = abs(c_1[1]-c_2[1])
        theta = c_1[0]
        delta_theta = abs(c_1[0]-c_2[0])
        del_x = R*cos(theta)*delta_phi 
        del_y = R*delta_theta
        return sqrt(del_x**2 + del_y**2)
    
    def batch_predict(self, locations, day_of_week=[]):
        '''
        input:
        - locations = numpy array [(u_i,v_i) | i] where u_i = (lat,long) of the start location, 
        v_i = (lat_long) of the destination location 
        - (optional) day_of_week = numpy array [day_i | i] : choose one of these -> "MON", "TUE, "WED", "THU", "FRI", "SAT", "SUN"
        
        output:
        - The array prediction of the duration in minute (m) needed to travel from point u to point v 
        (please note that if you want to predict the duration needed from rider currently at point x and need to pick up food at point y and deliver at point z, you need to calculate the time it takes for x to go to y and the time it takes from a rider to from y to z)
        '''
        n = len(locations)
        if len(day_of_week) != n : 
            day_of_week = np.full(n,"MON")
        u = np.apply_along_axis(lambda loc_i : loc_i[0], axis=1, arr=locations)
        v = np.apply_along_axis(lambda loc_i : loc_i[1], axis=1, arr=locations)
            
        merchant_lat = np.apply_along_axis(lambda u_i : u_i[0], axis=1, arr=u)
        merchant_long = np.apply_along_axis(lambda u_i : u_i[1], axis=1, arr=u)
        
        customer_lat = np.apply_along_axis(lambda v_i : v_i[0], axis=1, arr=v)
        customer_long = np.apply_along_axis(lambda v_i : v_i[1], axis=1, arr=v)
    
        # print(np.apply_along_axis(lambda p:p, axis=1, arr=locations)
              
        EucDist = np.apply_along_axis(lambda p :self.get_euc(p[0],p[1]) , axis=1, arr=locations)
              
#         ShortestDist = np.apply_along_axis(lambda p :self.distanceCalculator.shortestDistance(p[0],p[1]) , axis=1, arr=locations)

#         day_of_week_sin = np.apply_along_axis(lambda day : np.sin(self.dayMap[day]*(2.*np.pi/7)) , axis=1, arr=day_of_week)
#         day_of_week_cos = np.apply_along_axis(lambda day : np.cos(self.dayMap[day]*(2.*np.pi/7)) , axis=1, arr=day_of_week)
        
# #         inp = [[merchant_lat, merchant_long, customer_lat, customer_long, EucDist, ShortestDist, day_of_week_sin, day_of_week_cos]]
#         X = np.column_stack((merchant_lat, merchant_long, customer_lat, customer_long, EucDist, ShortestDist, day_of_week_sin, day_of_week_cos))
#         print(X)
#         return self.model.predict(X)
        return 0
    
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


