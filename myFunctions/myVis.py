import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
import numpy as np
import pandas as pd
from datetime import date, timedelta

def line_plot(df, title, ylabel="Cases", h=None, v=None,
              xlim=(None, None), ylim=(0, None), math_scale=True, y_logscale=False, y_integer=False):
    """
    Show chlonological change of the data.
    """
    ax = df.plot()
    if math_scale:
        ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.ticklabel_format(style="sci",  axis="y",scilimits=(0, 0))
    if y_logscale:
        ax.set_yscale("log")
    if y_integer:
        fmt = matplotlib.ticker.ScalarFormatter(useOffset=False)
        fmt.set_scientific(False)
        ax.yaxis.set_major_formatter(fmt)
    ax.set_title(title)
    ax.set_xlabel(None)
    ax.set_ylabel(ylabel)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.legend(bbox_to_anchor=(1.02, 0), loc="lower left", borderaxespad=0)
    if h is not None:
        ax.axhline(y=h, color="black", linestyle="--")
    if v is not None:
        if not isinstance(v, list):
            v = [v]
        for value in v:
            ax.axvline(x=value, color="black", linestyle="--")
    plt.tight_layout()
    plt.show()

def show_trend(df, name='Ontario', typeToVis="contracted", n_changepoints=2,
               startDate=None,returnForcast=False,typeOfFit='linear'):
    """
    Show trend of log10(@variable) using fbprophet package.
    @ncov_df <pd.DataFrame>: the clean data
    @variable <str>: variable name to analyse
        - if Confirmed, use Infected + Recovered + Deaths
    @n_changepoints <int>: max number of change pointsimport matplotlib.pyplot as plt
    from fbprophet import Prophet
    from fbprophet.plot import add_changepoints_to_plot
    import numpy as np
    import pandas as pd
    from datetime import date, timedelta
    @kwargs: keword arguments of select_area()
    """
   
    # get only typeToVis and convert the data to log
    # note that we are replacing anything with inf - -inf to 0 there are nans basically
    # or the crit points of log
    if startDate==None:
        df = df[typeToVis]
    else:
        # split the date comming in 
        splitDate = startDate.split('-')
        int(splitDate[2]), int(splitDate[1]), int(splitDate[0])
        # create a time index 
        startDate = date(int(splitDate[0]), int(splitDate[1]), int(splitDate[2]))
        endDate = date.today()
        df = df.loc[startDate:endDate,typeToVis]
    
    if typeOfFit == 'linear':
        df = np.log10(df).replace([np.inf, -np.inf], 0)
    
    
    # massage the date to be placed in fbprophet
    # the data frame must contain coloumn with "ds" and "y"
    # these are string dates and values respectively
    dfProphetIn = pd.DataFrame({'ds':df.index,
                           'y':df}).reset_index()
    dfProphetIn  = dfProphetIn.drop(columns='date')
    if typeOfFit == 'logistic':        
        dfProphetIn['cap'] = 15000
    #dfProphetIn.tail()
    
    # fbprophet
    # note that the growth in linear here because we transformed the data into log scale
    # pipeline is as follows:
    # model generation ---> model fit ----> model generate future ----> forecast
    if typeOfFit == 'linear':
        model = Prophet(growth="linear", daily_seasonality=False, n_changepoints=n_changepoints) 
    else:
        model = Prophet(growth="logistic", daily_seasonality=False, n_changepoints=n_changepoints) 
        
    model.fit(dfProphetIn)
    future = model.make_future_dataframe(periods=3)
    if typeOfFit =='logistic':
        future['cap'] = 15000
    forecast = model.predict(future)
    
    # Printing the change points of the model
    print(model.changepoints)    
    
    # Create figure
    # plot the model using prophet    
    fig = model.plot(forecast)
    _ = add_changepoints_to_plot(fig.gca(), model, forecast)
    plt.title(f"{name} log10({typeToVis}) over time and change points")
    plt.ylabel(f"log10(the number of cases)")
    plt.xlabel("")
    plt.show()
    
    if returnForcast:
        return forecast
    
    
    
    
    
    
   