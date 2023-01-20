import pickle as pkl
import numpy as np
from math import * 
from distance_calculator import DistanceCalculator 
from sklearn.ensemble import GradientBoostingRegressor


class FoodPrepModel: 
    def __init__(self):
        self.model = pkl.load(open('gbdt_m_foodprep.pkl', 'rb'))
        self.features = ['FoodCategories_อาหารตามสั่ง', 'FoodCategories_ร้านก๋วยเตี๋ยว',
       'FoodCategories_อาหารอีสาน', 'FoodCategories_อาหารทะเล',
       'NationFoodCategory_Thai', 'NationFoodCategory_International',
       'FoodCategories_อาหารจานด่วน', 'FoodCategories_ของหวาน',
       'NationFoodCategory_Japanese', 'FoodCategories_Fast Food',
       'FoodCategories_สเต๊ก', 'FoodCategories_เครื่องดื่ม',
       'FoodCategories_สุกี้ยากี้', 'FoodCategories_สปาเก็ตตี้',
       'FoodCategories_ปิ้งย่าง', 'FoodCategories_อาหารใต้',
       'FoodCategories_ขนมจีน', 'FoodCategories_อาหารเหนือ',
       'FoodCategories_ไก่ทอด', 'FoodCategories_อาหารคลีน',
       'NationFoodCategory_Vietnam', 'NationFoodCategory_Myanmar',
       'FoodCategories_ร้านอาหาร', 'FoodCategories_พิซซ่า',
       'NationFoodCategory_Korean', 'NationFoodCategory_Isram',
       'FoodCategories_Quick Meal', 'FoodCategories_อาหารฮาลาล']
        self.length = len(self.features)

    def predict(self, u, v, NationFoodCategory="Thai", FoodCategories="อาหารตามสั่ง"):
        
        '''
        u = (lat,long) of merchant location 
        v = (lat,long) of customer location
        '''
        merchant_lat = u[0]
        merchant_long = u[1]

        customer_lat = v[0]
        customer_long = v[1]
        input = []
        tmp = self.length*[0]
        for i in range(tmp):
            if ("NationFoodCategory_"+NationFoodCategory) == features[i]:
                tmp[i]=1
            elif ("FoodCategories_"+FoodCategories) == features[i]: 
                tmp[i]=1
            else :
                tmp[i]=0
        
        input += tmp 
        return self.model.predict(input)
    