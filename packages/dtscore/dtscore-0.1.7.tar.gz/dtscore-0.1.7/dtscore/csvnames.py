"""
    CSV report column names
"""

#--------------------------------------------------------------------------------------------------
#   Common names
DATE = 'Date'
PORTFOLIO = 'Portfolio'
EQUITY = 'Equity'
STRATEGY = 'Strategy'
ANALYSIS = 'Strategy'       # alias for STRATEGY
DAYS = 'Days'

#--------------------------------------------------------------------------------------------------
#   Strategy Detail report names
#       Equity, Strategy, Date, Open, High, Low, Close, Volume, Split, HiChan, LoChan, Orders, Fills, Position, ""Txn P/L"", Cash, NetBookValue, MV, ""Posn P/L""";
OPEN = 'Open'
HIGH = 'High'
LOW = 'Low'
CLOSE = 'Close'
VOLUME = 'Volume'
SPLIT = 'Split'
HICHAN = 'HiChan'
LOCHAN = 'LoChan'
ORDERS = 'Orders'
FILLS = 'Fills'
POSITION = 'Position'
TXN_PL = 'Txn P/L'
CASH = 'Cash'
BV = 'NetBookValue'
MV = 'MV'
POSN_PL = 'Posn P/L'

#--------------------------------------------------------------------------------------------------
#   Strategy summary report names
#       "Equity", "Strategy", "Days", "Gains", "Losses", "Comms", "SkidCost", "ETD", "EPD", "ROI%", "Txns", "GT/Txn", "E/Txn", "G/Txn",
#       "L/Txn", "Long Gain", "Long Loss", "Short Gain", "Short Loss", "Max Gain", "Max Loss"
GAINS = 'Gains'
LOSSES = 'Losses'
COMMS = 'Comms'
SKID = 'Skid'
EARNINGS = 'ETD'
EPD = 'EPD'
ROI = 'ROI%'
TXNS = 'Txns'
GTPerTXN = 'GT/Txn'
EPerTXN = 'E/Txn'
GPerTXN = 'G/Txn'
LPerTXN = 'L/Txn'
LONG_GAINS = 'Long Gain'
LONG_LOSSES = 'Long Loss'
SHORT_GAINS = 'Short Gain'
SHORT_LOSSES = 'Short Loss'
MAX_GAIN = 'Max Gain'
MAX_LOSS = 'Max Loss'

#--------------------------------------------------------------------------------------------------
#   Strategy transaction detail report names
#       Date, Equity, Strategy, Shares, Days, AcquirePrice, DisposePrice, PL, Commission";
SHARES = 'Shares'
ACQUIRE_PRICE = 'AcquirePrice'
DISPOSE_PRICE = 'DisposePrice'
PL = 'PL'
COMMISSION = 'Commission'

#--------------------------------------------------------------------------------------------------
#   Portfolio detail report names
#       Portfolio, Date, GainTxns, LossTxns, TotTxns, CumGainTxns, CumLossTxns, CumTotTxns, GainTxnRatio, Gain, Loss, Earn, CumGain, CumLoss, CumEarn, 
#       MaxGain, MaxLoss, CashAtRisk, AvgCashAtRisk
GAIN_TXNS = 'GainTxns'
LOSS_TXNS = 'LossTxns'
TOT_TXNS = 'TotTxns'
CUM_GAIN_TXNS = 'CumGainTxns'
CUM_LOSS_TXNS = 'CumLossTxns'
CUM_TOT_TXNS = 'CumTotTxns'
GAIN_TXN_RATIO = 'GainTxnRatio'
GAIN = 'Gain'
LOSS = 'Loss'
EARN = 'Earn'                   # FIXME normalize earnings column names see EARNINGS above
CUM_GAIN = 'CumGain'
CUM_LOSS = 'CumLoss'
CUM_EARN = 'CumEarn'
PD_MAX_GAIN = 'MaxGain'         # FIXME duplicates MAX_GAIN but header text is different
PD_MAX_LOSS = 'MaxLoss'         # FIXME ditto
CASH_AT_RISK = 'CashAtRisk'
AVG_CASH_AT_RISK = 'AvgCashAtRisk'

#--------------------------------------------------------------------------------------------------
#   Portfolio summary report - Same columns as strategy summary except Portfolio replaces Equity,Strategy
#       "Portfolio", "Days", "Gains", "Losses", "Comms", "SkidCost", "ETD", "EPD", "ROI%", "Txns", "GT/Txn", "E/Txn", "G/Txn", "L/Txn", "Long Gain", "Long Loss",
#       "Short Gain", "Short Loss", "Max Gain", "Max Loss"

#--------------------------------------------------------------------------------------------------
#   Portfolio holding summary report - same columns as Portfolio Summary plus Equity column
#       "Portfolio", "Equity", "Days", "Gains", "Losses", "Comms", "SkidCost", "ETD", "EPD", "ROI%", "Txns", "GT/Txn", "E/Txn", "G/Txn", "L/Txn", "Long Gain", "Long Loss",
#       "Short Gain", "Short Loss", "Max Gain", "Max Loss"

#--------------------------------------------------------------------------------------------------
#   Portfolio holding detail report - Same columns as Portfolio detail report plus Equity, Strategy columns
#       Portfolio, Equity, Strategy, Date, GainTxns, LossTxns, TotTxns, CumGainTxns, CumLossTxns, CumTotTxns, GainTxnRatio, Gain, Loss, Earn, CumGain, CumLoss, CumEarn,
#       MaxGain, MaxLoss, CashAtRisk, AvgCashAtRisk

#   Portfolio ordersheet report
#       Date, Portfolio, Equity, Strategy, Fills, Position, Orders
FILLS = 'Fills'
POSITION = 'Position'
ORDERS = 'Orders'

#--------------------------------------------------------------------------------------------------
#   raw PL file names
NORM_PL = 'NormalizedPL'

#--------------------------------------------------------------------------------------------------
#   Detail derived / calculated
CUM_PL=0.0
FILL_ACTION = 'FillAction'
FILL_QTY = 'FillQty'
FILL_PRICE = 'FillPrice'

#   Summary derived / calculated
ME_RATIO = 'MaxGain/ETD'  # to identify if a single trade is dominating result
R_GT = 'R_GT'
R_MER = 'R_MER'
R_ROI = 'R_ROI'
R_COMP = 'R_COMP'
R_AVG = 'R_AVG'
