import pandas as pd
import datetime as datetime
import pickle
import os
import numpy as np

# ---------- Utilities for Logistic Regression
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import scipy.optimize as opt
from sklearn.preprocessing import MinMaxScaler
# -----------

# ---------- Utilities for Growth Rates
from datetime import date, timedelta
# -----------

# modeling
def logistic(x, a, c, d):
    """Fit a logistic function."""
    return a / (1. + np.exp(-c * (x - d)))


def fit_predict(x, y, f, x_pred=None):
    """Fit a function and predict on some input"""
    popt, pcov = opt.curve_fit(f, x, y, maxfev=100000)
    if x_pred is None:
        x_pred = x
    return f(x_pred, *popt)
#

class covid():
    
    data = []
    dataProvince = 'Ontario'
    dataProcess = []
    dfData = []    

    def __init__(self,cached=False):
        print('Getting COVID data')
        self.data = self.getData(cached)
        
    def dispGrowthFactor(self):
        dfData = self.dfData
        dfGrowthFactor = dfData['contracted'].diff()/dfData['contracted'].diff().shift(freq="D")
        dfGrowthFactor = dfGrowthFactor.fillna(1)
        
        # look at weekly growth factor
        dfGrowthFactorWeekly = dfGrowthFactor.rolling(7).mean()
        
        # get range of dates
        startDate = date(2020, 3, 14)
        endDate = date.today()
        
        dfGrowthFactorWeekly = dfGrowthFactorWeekly[startDate:endDate].fillna(1)
        
        dfGrowthFactorWeekly.plot()
        
        gf = dfGrowthFactorWeekly[endDate-timedelta(days=4)]
        trendGf = dfGrowthFactorWeekly[endDate-timedelta(days=4)]
        print(f"The current growth rate is {gf} while the 7 day trend growth rate is {trendGf}")
        
    def dispCurve(self,lenPred=30,showPredict=False):
        y = self.dfData['contracted'].to_numpy()
        x = np.arange(len(y))
        lenPred = 30
        xFuture = np.arange(lenPred) + len(x)
        
        # fit the model
        m = MinMaxScaler()
        yTrans = m.fit_transform(y.reshape(-1, 1) )
        yTrans = yTrans.reshape(1, -1)[0]
        yPredLogReg = fit_predict(x, yTrans, logistic, x_pred=xFuture).reshape(-1, 1)
        yPredLogReg = m.inverse_transform(yPredLogReg).reshape(1, -1)[0]
        
        ### Plot
        plt.scatter(x, y)
        #plt.plot(x, Y_pred_weighted,label='Weighted')
        plt.plot(xFuture, yPredLogReg,'r',label='Prediction')
        plt.xlabel('Days since record')
        plt.ylabel('Cases')
        plt.legend()

        plt.show()
        
        if showPredict:
            cur = 0
            prev = 0
            delta = 0

            for xVal,yVal in zip(xFuture,yPredLogReg):
                prev = cur
                cur = yVal
                print('Day from now={} CumSum={} Delta={}'.format(xVal,
                                                                 yVal,
                                                                 np.abs(cur-prev)))


            
    
    def getData(self,cached=False):
        urlCases = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/cases.csv'
        urlCodebook = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/codebook.csv'
        urlMortality = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/mortality.csv'
        urlRecovered = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/recovered_cumulative.csv'
        urlTesting = 'https://raw.githubusercontent.com/ishaberry/Covid19Canada/master/testing_cumulative.csv'
        ##cachedFile = os.getcwd()+'.\data\covidData.pickle'
        cachedFile = '..//data//covidData.pickle'

        if cached:
            # pickle in
            print('cached') 
            covidDataPickleIn = open(cachedFile,"rb")
            covidData = pickle.load(covidDataPickleIn)
            return covidData        
        else:
            try:
                cases = pd.read_csv(urlCases)
                codebook = pd.read_csv(urlCodebook)
                mortality = pd.read_csv(urlMortality)
                recovered = pd.read_csv(urlRecovered)
                testing = pd.read_csv(urlTesting)        
            except Exception as e:
                print('Something went wrong in getting the data')
                print(e)

        covidData = {'cases':cases,
                'codebook':codebook,
                'mortality':mortality,
                'recovered':recovered,
                'testing':testing}


        # pickle out
        covidDataPickleOut = open(cachedFile,"wb")
        pickle.dump(covidData,covidDataPickleOut)
        covidDataPickleOut.close()
        return covidData    
    
    def getAllDates(self):
        allDates = []    

        s = datetime.date(2020, 1, 1)   # start date
        e = datetime.date.today()
        delta = e - s       # as timedelta
        for i in range(delta.days + 1):
            day = s + datetime.timedelta(days=i)
            allDates.append(day.strftime('%d-%m-%Y'))
        return allDates        
    
    def getDateColName(self,df):
        for col in df.columns:
            if 'date_' in col:
                return col
        else:
            print("Couldn't find date, returning 'date' instead")
            return 'date'
    
    def getCumSumColName(self,df):
        for col in df.columns:
            if 'cumulative_' in col:
                return col
        else:
            print("Couldn't find cumulative, returning 'cumSum' instead")
            return 'cumSum'

    def getGroupByProvince(self,df,prov='Ontario'):
        dfProvince = df.loc[df['province']==prov]
        dfProvinceDate = dfProvince.groupby([self.getDateColName(df)])
        dfProvinceDateCounts = dfProvinceDate['province'].value_counts()
        return dfProvinceDateCounts    
    
    def getCount(self,dateToFind,groupDF,provOfInterest,cumSum):
        
        dfDates = groupDF.index.get_level_values(groupDF.index.names[0]).unique().tolist()
        try:
            if dateToFind in dfDates:
                return (cumSum + groupDF[dateToFind][provOfInterest])
            else:            
                return (cumSum)
        except Exception as e:
            print('Something went wrong trying to find date:{} in {}'.format(dateToFind,groupDF.index.names[0]))
    
    def getCountCumSum(self,df,dateToFind,provOfInterest,cumSum):    
        try:
            dfQuery = df.query("{} == '{}' & province=='{}'".format(self.getDateColName(df),dateToFind,provOfInterest))

            if dfQuery.empty:
                return 0
            else:
                val = dfQuery[self.getCumSumColName(df)].tolist()[0]    
                return int(val)
        except Exception as e:
            print(print('Something went wrong trying to find date:{} in {}'.format(dateToFind,df.index.names[0])))
            print(e)
            return cumSum

    def getProcessedData(self,provOfInterest = 'Ontario'):  
        self.dataProvince = provOfInterest
        # Get all dates
        allDates = self.getAllDates()
        
        rawDataClc = self.data        
        cases = rawDataClc['cases']
        codebook = rawDataClc['codebook']
        mortality = rawDataClc['mortality']
        recovered = rawDataClc['recovered']
        testing = rawDataClc['testing']
        
        # Need to convert these into cumsum values
        casesProv = self.getGroupByProvince(cases,prov=provOfInterest)
        mortalityProv = self.getGroupByProvince(mortality,prov=provOfInterest)
        # These are already in cumsum values
        recoveredProv = self.getGroupByProvince(recovered,prov=provOfInterest)
        testingProv = self.getGroupByProvince(testing,prov=provOfInterest)
        
        dataDict = []

        caseDates = casesProv.index.get_level_values('date_report').unique().tolist()
        mortalityDates = mortalityProv.index.get_level_values('date_death_report').unique().tolist()
        recoveredDates = recoveredProv.index.get_level_values('date_recovered').unique().tolist()
        testingDates = testingProv.index.get_level_values('date_testing').unique().tolist()
        conCumSum = 0
        mortCumSum = 0
        recCumSum = 0
        testCumSum = 0

        for date in allDates:
            if ((date in caseDates) or (date in mortalityDates) or (date in recoveredDates) or (date in testingDates)):
                d = date

                day = d.split('-')[0]
                month = d.split('-')[1]
                year = d.split('-')[2]

                # Need to generate cumsum for these because they are daily cases
                conCumSum = self.getCount(dateToFind = d,
                               groupDF = casesProv,
                               provOfInterest= provOfInterest,
                                    cumSum = conCumSum)

                mortCumSum = self.getCount(dateToFind = d,
                               groupDF = mortalityProv,
                               provOfInterest = provOfInterest,
                                     cumSum = mortCumSum)

                # just grab the cumsum dates for rec and testing     
                recCumSum = self.getCountCumSum(df = recovered,
                                           dateToFind = d,
                                           provOfInterest = provOfInterest,
                                          cumSum = recCumSum)        

                testCumSum = self.getCountCumSum(df = testing,
                                           dateToFind = d,
                                           provOfInterest = provOfInterest,
                                              cumSum = testCumSum)                

                dateDict = {'date':'{}-{}-{}'.format(month,day,year),
                        'contracted':conCumSum,
                        'mortality':mortCumSum,
                        'recovered':recCumSum,
                        'testing':testCumSum}


                dataDict.append(dateDict)

        self.dataProcess = dataDict
        