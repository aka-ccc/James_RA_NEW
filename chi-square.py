# -*- coding: utf-8 -*-
import pandas as pd
import math

'''
2022/04/14 CCC
讀檔, 值域, 值域出現值, 機率分配, 值域卡方值 =====> 算完了
特徵值域你要output的時候再加總吧
數字應該沒啥問題, 但我沒取小數點第幾位那個, 有點懶就直接算了
阿計算的東西基本上都在feature的cal_chi_square那個function裡面了
要拿的東西都print出來了, 你再看要怎處理吧hehe
'''

class domain:
    domain_name = ''
    domain_conclusion = {}

    def __init__(self, domain_name):
        self.reset()
        self.domain_name = domain_name

    def reset(self):
        self.domain_name = ''
        self.domain_conclusion = {}

    def set_conclusion(self, con):
        if con not in self.domain_conclusion:
            self.domain_conclusion[con] = 1
        else:    
            self.domain_conclusion[con] += 1

class feature:
    feature_name = '' # 特徵名稱
    feature_domain = {} # 值域出現值 {'值域名稱': 次數}
    feature_con_domain = {} # 值域出現值結果 {'good': 次數, 'no-good': 次數,...}
    prob = {} # 機率分配
    domain_chi_square = {} # 值域卡方值

    def __init__(self, feature_name, feature_domain = None, feature_con_domain = None, prob = {}):
        self.reset()
        self.feature_name = feature_name
        self.feature_domain = feature_domain
        self.feature_con_domain = feature_con_domain
        self.prob = prob
        self.cal_chi_square()
    
    def reset(self):
        self.feature_name = ''
        self.feature_domain = {}
        self.feature_con_domain = {}
        self.prob = {}
        self.domain_chi_square = {}
    
    def cal_chi_square(self):
        # class值域
        if self.feature_con_domain == None:
            data_sum = 0.0
            print('======================================')
            print(f'{self.feature_name}值域')
            for key in self.feature_domain:
                data_sum += self.feature_domain[key]
                print(f'{key}的值域出現值為{self.feature_domain[key]}')
            for key in self.feature_domain:
                self.prob[key] = self.feature_domain[key]/data_sum
                print(f'{key}的機率分配為{self.prob[key]}')
            print('--------------------------------------')
        # 其他值域
        else:
            print('======================================')
            print(f'特徵{self.feature_name}')
            for key in self.feature_con_domain:
                temp_chi_square = 0.0
                domain_sum = 0.0
                for outcome in self.feature_con_domain[key].domain_conclusion:
                    domain_sum += self.feature_con_domain[key].domain_conclusion[outcome]
                print(key) # 值域名稱
                print(f'{key}的值域出現值為{domain_sum}')
                for outcome in self.prob:
                    theo_value = domain_sum*self.prob[outcome] # 計算理論值
                    print(f'{outcome}的理論值:{theo_value}')
                    if outcome not in self.feature_con_domain[key].domain_conclusion:
                        temp_chi_square += math.pow(0 - theo_value, 2) / theo_value
                    else:    
                        temp_chi_square += math.pow(self.feature_con_domain[key].domain_conclusion[outcome] - theo_value, 2) / theo_value
                print(f'{key}的值域卡方:{temp_chi_square}')
                print('--------------------------------------')

class raw_data:
    '''
    file_path ====> 給檔案路徑
    讀取資料並建立資料特徵字典集
    '''
    raw_data = pd.DataFrame() # 原始資料(csv檔內容)
    conclusions = {} # 結論 {'good': 次數, 'no-good': 次數,...}
    data_features = {} # 資料特徵
    prob = {} # class值域的機率分佈

    def __init__(self, file_path):
        self.reset()
        self.raw_data = pd.read_csv(file_path)
        self.create_features()

    def create_features(self):
        # 結論總數======>計算class值域
        for outcome in self.raw_data[self.raw_data.columns[-1]]:
            if outcome not in self.conclusions:
                self.conclusions[outcome] = 1
            else:
                self.conclusions[outcome] += 1
        self.data_features['class'] = feature(feature_name = 'class', feature_domain = self.conclusions)
        self.prob = self.data_features['class'].prob
        for col in self.raw_data.columns[:-1]:
            temp_domain = {}
            temp_conclusion = {}
            idx = 0
            for item in self.raw_data[col]:
                outcome = self.raw_data[self.raw_data.columns[-1]][idx]
                if item not in temp_conclusion:
                    temp_conclusion[item] = domain(domain_name = item)
                temp_conclusion[item].set_conclusion(outcome)
                if item not in temp_domain:
                    temp_domain[item] = 1
                else:
                    temp_domain[item] += 1
                idx += 1
            self.data_features[col] = feature(feature_name = col, feature_domain = temp_domain, feature_con_domain = temp_conclusion, prob = self.prob)

    def reset(self):
        self.raw_data = pd.DataFrame()
        self.conclusions = {}
        self.data_features = {}
        self.prob = {}
        

def main():
    data = raw_data(file_path = 'Weather-排序.csv')

if __name__ == '__main__':
    main()
    