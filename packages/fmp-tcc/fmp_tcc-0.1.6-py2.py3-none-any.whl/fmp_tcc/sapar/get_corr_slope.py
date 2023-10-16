import pandas as pd
import numpy as np

import statsmodels.formula.api as smf

def slope_corr_ols(metric0: float='inventory'):
    def slope_corr(data_frame):
        data_frame = data_frame.dropna()

        if len(data_frame) <= 0:
            return pd.Series([None, None], index=["slope", "correlation"])
    
        cols = list(set(data_frame.columns).difference([metric0]))
        col = cols[0]

        inventory_model = smf.ols(formula=col + ' ~ ' + metric0, data=data_frame)
        inventory_model = inventory_model.fit()
    
        return pd.Series([inventory_model.params[metric0], 
                      data_frame[metric0].corr(data_frame[col])], 
                      index=["slope", "correlation"])

    return slope_corr