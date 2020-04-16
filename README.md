# Introduction
I wanted to get a deeper insight on the current state of things here in Ontario.  This is by no means a comprehensive look at all possible models but only the models that I have come across through my readings.

# Data Set
Berry I, Soucy J-PR, Tuite A, Fisman D. Open access epidemiologic data and an interactive dashboard to monitor the COVID-19 outbreak in Canada. CMAJ. 2020 Apr 14;192(15):E420.

# To Do:

- Trend Analysis:
	- [x] Log Regression
	- [x] fbProphet

- Model Creation:
	- [x] SIR(M)
	- [x] SAIR(M)
	- [x] SDIR(M)
	- [x] SIGR(M)
	- [x] SEIR(M)

- Prediction:
	- [ ] 


# Order of Reading

##[Looking at Growth Rates](https://github.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/blob/master/notebooks/GrowthFactor.ipynb)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/weeklyGrowthFactor.PNG)

##[Looking at Trends](https://github.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/blob/master/notebooks/TrendLines_fbprophet.ipynb)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/trendAnalysis_1.PNG)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/trendAnalysis_2.PNG)
These are the critical dates
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/criticalDates.PNG)

##[Modeling Trends](https://github.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/blob/master/notebooks/ModelComparison.ipynb)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/3PhaseModelComparison.PNG)


##[Comapring Trends](https://github.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/blob/master/notebooks/ModelComparison.ipynb)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/entireTimeModelComparison.PNG)
![](https://raw.githubusercontent.com/mgaringoDev/myOntarioCovidModelTrendAnalysis/master/imgs/modelErrorComparison.png)

