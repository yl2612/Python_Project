import numpy as np
import pandas as pd
import pandas.io.data as web
import matplotlib.pyplot as plt
from Utilities.Inputfunctions import *
from Utilities.Exceptions import *
from Utilities.CheckInternet import *
from ClassPackage.MarketClass import *
from ClassPackage.StockClass import *
from collections import defaultdict


class Portfolio():
    '''
    Generate a class describe the stock containing several attributes and functions.
    
    '''
    
    def __init__(self,stock_company_list, start_date, end_date, amount_list):
        '''
        Constructor:
            
        Input:
            stock_company_list(list of strings): a list of the stock symbols from user input.
            start_date: the start date of the portfolio from user input.
            end_date: the end date of the portfolio from user input.
        
        Attributes:
            stock_company_list(list of strings): a list of the stock symbols.
            start_date: the start date of the portfolio.
            end_date: the end date of the portfolio.
        '''
        
        self.stock_company_list = stock_company_list
        self.start_date = start_date
        self.end_date = end_date
        self.amount_list = amount_list
    
    def pair_up(self):
        """
        Pair up the stock with the amount,
        return a dictionary that both stock and amount are not null.
        """
        dictionary = dict(zip(self.stock_company_list, self.amount_list))
        delete_key_dictionary = {k: dictionary[k] for k in dictionary if not k==""}
<<<<<<< HEAD
        delete_value_dictionary = {k: delete_key_dictionary[k] for k in delete_key_dictionary if (delete_key_dictionary[k] != "" and delete_key_dictionary[k] !="0")}
=======
        delete_value_dictionary = {k: delete_key_dictionary[k] for k in delete_key_dictionary if not delete_key_dictionary[k] == ""}
>>>>>>> 49f39cc4d5762349dd8fe53d6829d8bcf52dae87
        if IsEmptyPortfolio(delete_value_dictionary):
            raise EmptyPortfolioException()
        else:
            return delete_value_dictionary

    
    def merge_same_stock(self):
        """
        This function adds amount together if repetitive stock names exist.
        """   
        raw_dictionary = self.pair_up() #add the trade amount together if two names are the same.
        
        stock_amount_dictionary = defaultdict(int)
        for stock, amount in raw_dictionary.iteritems():
            stock_amount_dictionary[stock.upper()] += ParseValidNum(amount) #add the trade amount together if the two capitalized names are the same.
    
        unique_stock_company_list = stock_amount_dictionary.keys() #get a list of unique stock names
        trade_amount_list = stock_amount_dictionary.values() #get a list of trade amount corresponding to the stock names.
        return unique_stock_company_list, trade_amount_list
    
    def get_portfolio_df(self):
        """
        Take a list of stock companies, date range and trade amount of each stock,
        return a dataframe showing each stock and total portfolio performance
        """
        unique_stock_companies, trade_amount = self.merge_same_stock()
        stock_class_dict = {stock:Stock(stock,self.start_date,self.end_date) for stock in unique_stock_companies} #get validated stocks list
    
        pricecols = {stock:stock_class.close_price for stock, stock_class in stock_class_dict.iteritems()}
        closed_price_df = pd.DataFrame(data=pricecols, columns=unique_stock_companies)
        portfolio = closed_price_df.mul(trade_amount, axis=1)
        portfolio_add_sum = portfolio.copy()
        portfolio_add_sum['Sum']= portfolio.sum(1)     
        return portfolio_add_sum
    
    def portfolio_weight(self):
        """
        Calculate the weight of each stock in the portfolio each day
        """
        portfolio_df = self.get_portfolio_df()
        portfolio_weight_df = portfolio_df.div(portfolio_df['Sum'], axis='index')       
        return portfolio_weight_df
    
    def describe_portfolio(self):
        """
        Get descriptic statistics of the portfolio
        """
        portfolio_df = self.get_portfolio_df()    
        describe_stat_df = portfolio_df.describe()
<<<<<<< HEAD
        describe_stat_df = describe_stat_df.rename(index = {'count':'trading days'})
=======
        
>>>>>>> 49f39cc4d5762349dd8fe53d6829d8bcf52dae87
        portfolio_weight_df = self.portfolio_weight()
        describe_stat_df.loc['start weight'] = portfolio_weight_df.ix[0]
        describe_stat_df.loc['end weight'] = portfolio_weight_df.ix[-1]
        
        stocks_return = portfolio_df.ix[-1] / portfolio_df.ix[0] -1
        describe_stat_df.loc['total return'] = stocks_return      
        return describe_stat_df
    
    def plot_portfolio(self):
        """
        Plot a gragh showing the performance of the portfolio
        """
        portfolio_df = self.get_portfolio_df()
        plt.figure()
        portfolio_df['Sum'].plot(kind='line',label = 'Portfolio')
        plt.ylabel('Price')
        plt.title('Line plot for the overall portfolio performance')
        plt.legend()
        plt.show()
     
    def percentage_change(self):
        """
        Calculate the return of the stock/portfolio each day
        """
        portfolio_df = self.get_portfolio_df()
        stock_firstday = portfolio_df.ix[0]
        percentage_change_df = (portfolio_df - stock_firstday)/stock_firstday
        return percentage_change_df
        
    def portfolio_value_change_compared_with_market(self):
        """
        Plot the percent change of the portfolio and the actual market.
        """
        plt.figure()
        self.percentage_change()['Sum'].plot(color = 'b',label = 'Portfolio')
        market = Market(self.start_date,self.end_date)
        market.change_price_precent().plot(color = 'r',label = 'Market')
        plt.legend()
        plt.xticks(rotation=45)
        plt.title('Portfolio performance compared with the market')
        plt.xlabel('Date')
        plt.ylabel('Percent Change of Close Price')
        plt.show()
    
    def risk_vs_return(self):
        """
        create a plot to examine the risk and return tradeoff
        """
        percentage_change_df = self.percentage_change()
        only_stocks_percentage_change_df = percentage_change_df[percentage_change_df.columns[:-1]]
        plt.figure()
        plt.scatter(only_stocks_percentage_change_df.mean(),only_stocks_percentage_change_df.std())
        plt.xlabel('Expected Return')
        plt.ylabel('Risk')
        for label, x, y in zip(only_stocks_percentage_change_df.columns, only_stocks_percentage_change_df.mean(), only_stocks_percentage_change_df.std()):
            plt.annotate(label, xy = (x, y),xytext = (10, 10),
                         textcoords = 'offset points', 
                         horizontalalignment = 'right', verticalalignment = 'down', 
                         bbox = dict(boxstyle = 'round,pad=0.2', facecolor='red', alpha = 0.2), 
                         arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3'))
        plt.title('Risk and Return of each stock position')
        plt.show()
         
    def stocks_value_change_corr(self):
        """
        get correlation of the stocks changes.
        """
        percentage_change_df = self.percentage_change()
        stocks_price_change_corr = percentage_change_df[percentage_change_df.columns[:-1]].corr()
        return stocks_price_change_corr
    
    def heat_map(self):
        """
        create a heat map to see the correlation among stocks
        """
        stocks_price_change_corr = self.stocks_value_change_corr()
        plt.figure
        plt.imshow(stocks_price_change_corr, cmap='Blues', interpolation='none')
        plt.colorbar()
        plt.xticks(range(len(stocks_price_change_corr)), stocks_price_change_corr.columns)
        plt.yticks(range(len(stocks_price_change_corr)), stocks_price_change_corr.columns)
        plt.title('Heat map of your portfolio stocks')
        plt.show()
        
#stock_company_list = ['f','AAPL','F']
#amount_list = ['30',20,20]
#start_date = "2011/11/21"
#end_date = "2012/3/21"        
#first = Portfolio(stock_company_list, start_date, end_date, amount_list)
#print first.merge_same_stock()