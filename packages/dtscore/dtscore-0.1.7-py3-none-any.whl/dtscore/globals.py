"""
    Global configuration
"""

import os
import logging
from datetime import date

from dtscore import schema_enums as se

#   logging constants
logshome = r"C:\users\dgsmith\dev\logs"
loglevel = logging.DEBUG
portfoliogenlogfilename = "portfolio_gen_.log"
logfilepath = os.path.join(logshome, portfoliogenlogfilename)
logformat = '%(asctime)s: %(levelname)-5s: %(module)-15s - %(message)s'

#   general paths and folders not related to a single analysis environment
apphome = r'c:\users\dgsmith\documents\personal\financial\trading\dts'
analyzerexepath = r"analyzer\dtsanalyzer.exe"
coredatafolder = r"coredata"
analysesfolder = r"analyses"

#   analysis subfolder names and a collection of subfolder names 
reportsfolder = "reports"
configsfolder = "configs"
scriptsfolder = "scripts"
portfoliosfolder = "portfolios"
subfoldernames = [reportsfolder, configsfolder, scriptsfolder, portfoliosfolder]

#   default portfolio file name template
portfoliofilename = 'portfolios.json'
#   configuration file names
summaryconfigfilename = 'config_summary.json'
detailconfigfilename = 'config_detail.json'
ordersheetconfigfilename = 'config_ordersheet.json'
holdingdetailconfigfilename = 'config_holdingdetail.json'
#   script file names
summaryscriptfilename = 'runportfolio_summary.ps1'
detailscriptfilename = 'runportfolio_detail.ps1'
ordersheetscriptfilename = 'runportfolio_ordersheet.ps1'
holdingdetailscriptfilename = 'runportfolio_holdingdetail.ps1'

#   input csv glob filters
glob_template = 'txndetail_*.csv'
glob_portfolio_detail = 'portfolio_detail_*.csv'
glob_portfolioholding_detail = 'portfolio_holdingdetail_*.csv'
glob_ordersheet = 'portfolio_ordersheet_*.csv'

#   path convenience functions
def getreportsrelativepath(analysisfolder:str): return os.path.join(analysesfolder, analysisfolder, reportsfolder)
def getreportspath(analysisfolder:str): return os.path.join(apphome, getreportsrelativepath(analysisfolder))

def getconfigsrelativepath(analysisfolder:str): return os.path.join(analysesfolder, analysisfolder, configsfolder)
def getconfigspath(analysisfolder:str): return os.path.join(apphome, getconfigsrelativepath(analysisfolder))

def getscriptsrelativepath(analysisfolder:str): return os.path.join(analysesfolder, analysisfolder, scriptsfolder)
def getscriptspath(analysisfolder:str): return os.path.join(apphome, getscriptsrelativepath(analysisfolder))

def getportfoliosrelativepath(analysisfolder:str): return os.path.join(analysesfolder, analysisfolder, portfoliosfolder)
def getportfoliospath(analysisfolder:str): return os.path.join(apphome, getportfoliosrelativepath(analysisfolder))


#   iex url components
iex_urlsuffix = r"/previous?token=pk_05b9fc2f3b9648cb8debcd407ad90b26"
iex_urlprefix = r"https://cloud.iexapis.com/stable/stock/"

#   analysis specific ******************************************************************************
mer_cutoff = 0.3                # select observations with MER less than or equal to this value
pl_cutoff = 0.0                 # drop summaries with less than or equal this PL amount
investmentlimit = 100_000.00
topxcount = 20

#   script/config output ***************************************************************************
as_db_environment = se.DbEnvironment.Prod
as_dataset_type = se.DatasetType.FullDay
as_reports_folder = r"C:\users\dgsmith\Documents\personal\financial\trading\dts\results"
as_report_name_template = "portfolio_summary.csv"
as_logging_level = se.LogLevel.Info
as_log_folder = r"C:/Users/dgsmith/dev/logs/portfolio_summary_.log"
as_runtype = se.RunType.MultiPortfolioAnalysis

#   Portfolio section default parameter values
ps_name = f"PortfolioSummary_{date.today()}"
ps_report_type = se.ReportType.PortfolioSummary
ps_tracking_start_date = date.today()
ps_market_entry_method = se.MarketEntryMethod.ConditionalOrder
ps_portfolios = []

#   Parameter defaults
default_trading_side = se.TradingSide.Both
default_autosubmit = True
default_submit_order_at = "Immediate"
