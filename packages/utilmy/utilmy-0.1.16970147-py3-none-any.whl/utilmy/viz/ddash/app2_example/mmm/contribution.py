import pandas as pd
import numpy as np
import pystan
import json


class MarketingMixModeling():

    def __init__(self, app_df, imp_df, prior_params):
        self.app = app_df
        self.imp = imp_df
        self.prior_params = prior_params

    def fit_posterior(self, stan_code):
        stan_data = {
            'N': len(self.app),
            'Y': self.app.application.values,
            'num_media': self.imp.shape[1],
            'X_media': self.imp.values,
        }
        sm = pystan.StanModel(model_code=stan_code)
        self.fit = sm.sampling(data=stan_data, iter=2000, chains=1)
        return self.fit

    def dump_posterior_params(self, json_name)
        params_dict = {}
        for p in self.fit.model_pars[:-2]:
            params_dict[p] = self.fit[p].mean()   
        with open(json_name, 'w') as fp:
            json.dump(params_dict, fp)
        return params_dict

    def monthly_mmm







