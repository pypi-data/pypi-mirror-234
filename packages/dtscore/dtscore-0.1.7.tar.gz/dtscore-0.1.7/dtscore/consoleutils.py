"""
    Console utilities
"""
import os
import glob
from dtscore import globals as gl

#--------------------------------------------------------------------------------------------------
def getrecentportfoliodetailpath(analysisfolder:str) -> str:
    return _do_glob(analysisfolder, gl.glob_portfolio_detail)

#--------------------------------------------------------------------------------------------------
def getrecentportfolioholdingdetailpath(analysisfolder:str) -> str:
    return _do_glob(analysisfolder, gl.glob_portfolioholding_detail)

#--------------------------------------------------------------------------------------------------
def getrecent_ordersheet_filepath(analysisfolder:str) -> str:
    return _do_glob(analysisfolder, gl.glob_ordersheet)

#--------------------------------------------------------------------------------------------------
# def promptfor_analysisfolder() -> str:
#     return promptfor_text("analysis folder name?", toupper=True)

#--------------------------------------------------------------------------------------------------
# def promptfor_portfolioname() -> str:
#     print('Enter portfolio name: ', end='')
#     return input().upper()

#--------------------------------------------------------------------------------------------------
def promptfor_bool(prompt:str) -> bool:
    print(prompt + " (Y/N)?: ", end="")
    yesno = input().upper()
    match yesno:
        case "Y": return True
        case "N": return False
        case _:
            print("Invalid - response must be Y or N")
            return promptfor_bool(prompt)

#--------------------------------------------------------------------------------------------------
def promptfor_text(prompt:str, toupper:bool=False) -> str:
    print(prompt + ': ', end='')
    response = input()
    return response.upper() if toupper else response

#--------------------------------------------------------------------------------------------------
def promptfor_cutoffandplotrange() -> tuple[str,str]:
    print('enter cutoff date (yyyymmdd): ', end='')
    cutoff = input()

    print(f'plot range start date (yyyymmdd) or enter for {cutoff} default: ', end='')
    response = input()
    startdate = response if len(response) > 0 else cutoff
    print(f'plot range end date (yyyymmdd): ', end='')
    enddate = input()
    plotrange = f'{startdate} - {enddate}'
    return cutoff, plotrange

#--------------------------------------------------------------------------------------------------
#   private methods
def _do_glob(analysisfolder:str, pattern:str) -> str:
    globpath = os.path.join(gl.apphome,gl.analysesfolder,analysisfolder, gl.reportsfolder, pattern)
    all_filenames = glob.glob(globpath, recursive=False)
    #   !!proper sorting relies on date stamped file names!!
    all_filenames.sort(reverse=True)
    #   select the latest filename
    return all_filenames[0]
