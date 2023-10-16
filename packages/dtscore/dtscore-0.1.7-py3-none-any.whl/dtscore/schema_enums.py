"""
    Schema enums
"""

from enum import Enum

# ----------------------------------------------------------------------------------------------------
#   Schema enums
ReportType = Enum('ReportType', [
    'StrategySummary', 'StrategyBollDetail', 'StrategyProfitLossDetail', 'StrategyAdxDetail', 'StrategyTradesDetail',
    'StrategyTransactionDetail', 'PortfolioSummary', 'PortfolioDetail', 'PortfolioHoldingOrderSheet',
    'PortfolioHoldingDetail', 'PortfolioHoldingSummary', 'PortfolioSingleFileDetail'
    ])
AnalysisType = Enum("AnalysisType",["Summary", "Detail", "OrderSheet", "HoldingDetail"])
DbEnvironment = Enum('DbEnvironment',['Prod','Dev','Staging','Test','Static'])
LogLevel = Enum('LogLevel',['Error', 'Info', 'Warn', 'Debug', 'Verbose'])
RunType = Enum('RunType',['StrategyAnalysis', 'SinglePortfolioAnalysis', 'MultiPortfolioAnalysis'])
StrategyName = Enum('StrategyName',['BOLL','RBOL','ADX'])
TradingSide = Enum('TradingSide',['Long','Short','Both'])
SkidType = Enum('SkidType',['Percent','Absolute'])
DatasetType = Enum('DatasetType',['FullDay','PartialDay'])
MarketEntryMethod = Enum('MarketEntryMethod',['MarketOrder','ConditionalOrder'])
