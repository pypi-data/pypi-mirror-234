import os
import sys

import numpy as np
import pandas as pd
import quantstats as qs

import plotly.express as px

from benchmark import Benchmark
from strategy import Strategy


baseFolder: str = os.path.dirname((os.path.abspath(os.path.dirname(''))))
dataFolder: str = os.path.join(baseFolder, 'Data')
resultsFolder: str = os.path.join(baseFolder, 'Results')
sys.path.append(baseFolder)
sys.path.append(dataFolder)
sys.path.append(resultsFolder)
WORKYEAR = 252



class Metrics:

    def __init__(self, strategies: pd.DataFrame):
        self.strategies     = strategies
        self.info_results_qs: pd.DataFrame = pd.DataFrame()
        
        
    def get_info_quantstats(self) -> pd.DataFrame:
        """Generate statistics for a given strategy/benchmark using Quantstats"""
        
        rollingReturns      = self.strategies.rolling(WORKYEAR).apply(self.expectedReturn)  # returns compounded every 252 days

        percentageWin, avgWin, medianRollingReturns = self.rollingYearlyReturns(rollingReturns)
        annualizedReturns = self.strategies.apply(lambda column: np.prod(column+1) ** (252/len(column)) - 1, axis=0)

        cumulative = qs.stats.comp(self.strategies)
        annualizedVol = qs.stats.volatility(self.strategies, annualize=True)
        alpha_series = rollingReturns.iloc[:, 0] - rollingReturns.iloc[:, 1]
        alphaAri = np.mean(alpha_series)
        
        alphaGeo = annualizedReturns[0] - annualizedReturns[1]
        
        volAlpha = np.std(alpha_series)
        positiveReturns = (self.strategies > 0).mean(axis=0, skipna=True)

        data_to_frame = {'Indicador': self.strategies.columns[0], 'Retorno Acumulado': cumulative[0], 'Retorno Anualizado': annualizedReturns[0], 'Retorno Anualizado (bench)': annualizedReturns[1],
                         'Volatilidade Anual': annualizedVol[0], 'Alpha Geom.': alphaGeo, 'Alpha Arit.': alphaAri, '% Ret. Positivos (daily)': positiveReturns[0]*100,
                         '% Win (annualized)': percentageWin*100, 'AvgWin (annualized)': avgWin, 'Mediana Dif. Retorno (annualized)': medianRollingReturns,
                         'Information Ratio': alphaAri/volAlpha}

        info = pd.DataFrame([data_to_frame])
        self.info_results_qs = info
        return self.info_results_qs
    
    # Utils
    def rollingYearlyReturns(self, retornos):
        """Function that calculates cumulative returns every X days and generates
            percentage of days above benchmark, average return of those days and the median
            of those differences"""
        # rollingReturns = retornos.rolling(WORKYEAR).apply(self.expectedReturn)
        strat = retornos.iloc[:,0].dropna()
        bench = retornos.iloc[:,1].dropna()

        win = strat > bench
        percentageWin = np.mean(win)
        averageReturnsWin = np.mean(strat[win])

        medianRollingReturns = np.median(strat - bench)

        return percentageWin, averageReturnsWin, medianRollingReturns

    def expectedReturn(self, series):
        return np.product(series+1) - 1

    def match_dates(self, df1, df2):
        df1.dropna(inplace=True)
        df2.dropna(inplace=True)
        df1 = df1[df1.index.isin(df2.index)]
        df2 = df2[df2.index.isin(df1.index)]
        assert df1.shape == df2.shape, "Dates do not match"
        return df1, df2