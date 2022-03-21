from globalEnums import LotSize, Expiry
from datetime import datetime
import yaml

def get_expiry(typee):

    filee = open("otherInfo.yml")
    parser = yaml.load(filee, Loader=yaml.FullLoader)

    if typee == Expiry.WEEKLY.value:

        return parser["expiry"]["weekly"]
    
    elif typee == Expiry.MONTHLY.value:

        return parser["expiry"]["mothly"]

def get_script_info(base_sym):

    filee = open("ScriptInfo.yml")
    parser = yaml.load(filee, Loader=yaml.FullLoader)
    #print(parser)
    
    for sym in parser:
        if sym == base_sym.upper():
            return parser[sym]

def get_atm_strike(price, factor):
    
    rem = price%factor

    if rem > 0.5*factor:

        return int(price - rem + factor)
    
    else:

        return int(price - rem)

def get_base_sym(symbol):

    if symbol == "NSE:NIFTY50-INDEX" or symbol == "NSE:NIFTY22JANFUT":
        return "NIFTY"
    elif symbol == "NSE:NIFTYBANK-INDEX" or symbol == "NSE:BANKNIFTY22JANFUT":
        return "BANKNIFTY"


def get_lot_size(sym):

    if sym.upper() == "NIFTY":
        return LotSize.NIFTY.value
    elif sym.upper() == "BANKNIFTY":
        return LotSize.BANKNIFTY.value 

def get_expiry_part(expiry, last_week):

    '''
    expiry: 03-Feb-2022
    '''

    split_exp = expiry.split("-")
    DAY   = split_exp[0]
    MONTH = split_exp[1]
    YEAR  = split_exp[2][-2:] # 22

    if last_week == 1:

        MONTH = MONTH.upper()

        return YEAR+MONTH
    
    else:

        if MONTH.upper() == "OCT" or MONTH.upper() == "NOV" or MONTH.upper() == "DEC":
            MONTH = MONTH[0]
        else:
            MONTH = str(datetime.strptime(MONTH, "%b").month)
    
    return YEAR+MONTH+DAY

def get_equity_symbol(exch, base_sym):

    base_symbol = base_sym.upper()

    if base_symbol == "NIFTY":
            
        return f"{exch}:NIFTY50-INDEX"

    elif base_symbol == "BANKNIFTY":

        return f"{exch}:NIFTYBANK-INDEX"

    return f"{exch}:"+base_symbol+"-EQ"

def get_opt_symbol(exch, base_sym, strike, expiry, opt_type):

    '''
    expiry: 03-Feb-2022
    '''
    #exp = get_expiry_part(expiry, last_week)

    sym = f"{exch}:{base_sym}{expiry}{strike}{opt_type}"

    return sym

def get_option_chain(exch, base_sym, expiry, atm, depth, mltp, dir):

    call_list = []
    put_list  = []

    if dir == 0:  # ITM
        
        limit  = mltp*(depth+1)

        call_list = [f"{exch}:{base_sym}{expiry}{atm-i}CE" for i in range(0, limit, mltp)]

        put_list  = [f"{exch}:{base_sym}{expiry}{atm+i}PE" for i in range(0, limit, mltp)]

        opt_chain = put_list + call_list
    
    elif dir == 1:  # ATM
        
        start  = atm - mltp*depth
        limit  = mltp*(2*depth+1)

        call_list = [f"{exch}:{base_sym}{expiry}{start+i}CE" for i in range(0, limit, mltp)]

        put_list  = [f"{exch}:{base_sym}{expiry}{start+i}PE" for i in range(0, limit, mltp)]

        opt_chain = put_list + call_list

    elif dir == 2:  # OTM
        
        limit  = mltp*(depth+1)

        call_list = [f"{exch}:{base_sym}{expiry}{atm+i}CE" for i in range(0, limit, mltp)]

        put_list  = [f"{exch}:{base_sym}{expiry}{atm-i}PE" for i in range(0, limit, mltp)]

        opt_chain = put_list + call_list
    
    #print(len(opt_chain))

    return opt_chain

if __name__ == "__main__":

    print(get_script_info("banknifty"))