from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import quantstats as qs

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# baseFolder: str = os.path.dirname((os.path.abspath(os.path.dirname(''))))
# dataFolder: str = os.path.join(baseFolder, 'Data')
# resultsFolder: str = os.path.join(baseFolder, 'Results')
# sys.path.append(baseFolder)
# sys.path.append(dataFolder)
# sys.path.append(resultsFolder)
WORKYEAR = 252


class Calculate:

    def __init__(self, name, colunas:tuple, returns_data: pd.DataFrame):
        self._check_correct_base_folder()

        self.name = name
        self.returns = returns_data

        self.collumn_indice = colunas[1]
        self.collumn_cdi = colunas[0]
        self.collumn_allocation = f'Alocacao{self.name}'

        self.returns_allocation: pd.Series = pd.Series(dtype=float)
        self.benchmark_allocation: pd.Series = pd.Series(dtype=float)

        self.returns_dict = dict()
        self.benchmark_dict = dict()
        self.allocation_dict = dict()
        self.info_results_qs: pd.DataFrame = pd.DataFrame()

        self.current_period = None

    ##### STATISTICS ######

    def calculateStrategyReturn(self, allocation: pd.Series, max_allowed: float=1.0, benchmark_portfolio_ratio:float=0.5, period: int=21):
        """ Returns a series with the Strategy returns (linear combination of 2
        return series).

            Keyword arguments:

            allocation -- pandas series or float with allocation for Asset2.
            max_allowed -- float with the maximum allowed allocation in Asset1.
        
        """
        self.current_period = period
        self.allocation_dict[self.current_period] = allocation

        allocation_returns = pd.merge(left=allocation, right=self.returns, on="Data", how="inner")
        cdi = allocation_returns[self.collumn_cdi]
        ibov = allocation_returns[self.collumn_indice]
        allocation = allocation_returns[self.collumn_allocation]
        self.returns_allocation = (cdi.multiply(max_allowed-allocation) + ibov.multiply(allocation))
        self.benchmark_allocation = cdi.multiply(max_allowed-benchmark_portfolio_ratio) + ibov.multiply(benchmark_portfolio_ratio)

        self.returns_dict[self.current_period] = self.returns_allocation
        self.benchmark_dict[self.current_period] = self.benchmark_allocation
        

    def reset_info_df(self):
        self.info_results_qs = pd.DataFrame()

    def get_info_quantstats(self, indicador: str) -> pd.DataFrame:

        returns = self.returns_allocation.copy()
        bench = self.benchmark_allocation.copy()

        rollingReturnsBench = bench.rolling(WORKYEAR).apply(self.expectedReturn)  # returns compounded every 252 days
        percentageWin, avgWin, medianRollingReturns = self.rollingYearlyReturns(returns, bench)
        annualizedReturnsBench = np.prod(bench+1) ** (252/len(bench)) - 1

        cumulative = qs.stats.comp(returns)
        # alphaGeo = (cumulative - qs.stats.comp(bench) + 1)
        # alphaGeo = np.sign(alphaGeo) * np.abs(alphaGeo) ** (252/len(returns)) - 1 # one single point (expected return X - expected return Y)

        annualizedVol = qs.stats.volatility(returns, annualize=True)

        rollingReturns = returns.rolling(WORKYEAR).apply(self.expectedReturn)    # returns compounded every 252 days
        alpha_series = rollingReturns - rollingReturnsBench
        # arithmetic mean of rolling alphas
        alphaAri = np.mean(alpha_series)
        annualizedReturns = np.prod(returns+1) ** (252/len(returns)) - 1
        
        alphaGeo = annualizedReturns - annualizedReturnsBench
        
        volAlpha = np.std(alpha_series)
        positiveReturns = (returns > 0).mean(axis=0, skipna=True)

        data_to_frame = {'Indicador': indicador, 'Retorno Acumulado': cumulative, 'Retorno Anualizado': annualizedReturns, 'Retorno Anualizado (bench)': annualizedReturnsBench,
                         'Volatilidade Anual': annualizedVol, 'Alpha Geom.': alphaGeo, 'Alpha Arit.': alphaAri, '% Ret. Positivos (daily)': positiveReturns*100,
                         '% Win (annualized)': percentageWin*100, 'AvgWin (annualized)': avgWin, 'Mediana Dif. Retorno (annualized)': medianRollingReturns,
                         'Information Ratio': alphaAri/volAlpha, "Periodo": self.current_period}

        info = pd.DataFrame([data_to_frame])
        if self.info_results_qs.empty:
            self.info_results_qs = info
        else:
            self.info_results_qs = pd.concat([self.info_results_qs, info], ignore_index=True)
        return self.info_results_qs

    ##### AUXILIARY FUNCTIONS ######

    def get_max_alpha_df(self):
        return self.info_results_qs.loc[self.info_results_qs["Alpha Geom."] == max(self.info_results_qs["Alpha Geom."])]
    
    def get_max_alpha_value(self):
        return self.get_max_alpha_df().iloc[0]["Alpha Geom."]

    def get_period_stats(self, periodo):
        """ Select the period collumn which is equal to "periodo" and return the whole row"""
        return self.info_results_qs.loc[self.info_results_qs["Periodo"] == periodo]

    def get_alpha_value(self, periodo):
        return self.get_period_stats(periodo).iloc[0]["Alpha Geom."]

    def rollingYearlyReturns(self, retornoStrat: pd.Series, retornoBase: pd.Series):
        """ Calculates percentage, average return and median of days with yearly
        returns above benchmark.

        Keyword arguments:

        retornoStrat -- daily returns for desired strategy
        retornoBase  -- daily returns for benchmark
        """

        rollingReturnsStrat = retornoStrat.rolling(
            WORKYEAR).apply(self.expectedReturn)
        rollingReturnsBase = retornoBase.rolling(
            WORKYEAR).apply(self.expectedReturn)

        win = rollingReturnsStrat > rollingReturnsBase
        percentageWin = np.sum(win)/rollingReturnsStrat.size
        averageReturnsWin = np.mean(rollingReturnsStrat[win])

        medianRollingReturns = np.median(
            (rollingReturnsStrat.dropna() - rollingReturnsBase.dropna()))

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

    def _check_correct_base_folder(self):
        global baseFolder
        global dataFolder
        global resultsFolder
        if "MarketTiming" not in baseFolder.lower():
            baseFolder = baseFolder + "\\MarketTiming"
            dataFolder = os.path.join(baseFolder, 'Dados')
            resultsFolder = os.path.join(baseFolder, 'Resultados')
