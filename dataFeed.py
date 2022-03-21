from time import sleep
from globalEnums import StrategyState, Expiry
from globalFunctions import get_equity_symbol, get_atm_strike, get_opt_symbol, get_script_info, get_expiry

class DataFeed:
    '''
    this class will fetch symbols data depending on the state of strategy and order
    '''
    def __init__(self, fyers_client) -> None:
    #def __init__(self, fyers_client, base_sym, ticks_queue, logs_queue, global_objects) -> None:
        
        self.fyers_client   = fyers_client
        #self.base_sym       = base_sym
        #self.script_info    = get_script_info(self.base_sym)
        
        #self.ticks_queue    = ticks_queue
        #self.logs_queue     = logs_queue

        #self.strategy_state = global_objects["strategy_state"]

        #self.base_formatted_sym      = get_equity_symbol(self.script_info["exchange"], self.base_sym)
        #self.call_sym, self.put_sym  = None, None

    def get_ltp(self, symbol):

        data_info = {
            "symbols" : symbol
        }

        response = self.fyers_client.quotes(data_info)
        #print(response)
        for data in response['d']:
            sym     = data['n']
            ltp     = data['v']['lp']
            bid     = data['v']['bid']
            ask     = data['v']['ask']
            spread  = data['v']['spread']

        #print("Ltp is: ", ltp)

        return ltp

    def fill_ticks_queue(self):
        
        listt = []

        base_sym_ltp = self.get_ltp(self.base_formatted_sym)
        listt.append((self.base_formatted_sym, base_sym_ltp, "INDEX"))

        atm_strike = get_atm_strike(base_sym_ltp, self.script_info["strike_diff"])

        self.call_sym = get_opt_symbol(self.script_info["exchange"], self.base_sym, atm_strike, get_expiry(Expiry.WEEKLY.value), "CE")
        self.put_sym = get_opt_symbol(self.script_info["exchange"], self.base_sym, atm_strike, get_expiry(Expiry.WEEKLY.value), "PE")

        call_ltp = self.get_ltp(self.call_sym)
        listt.append((self.call_sym, call_ltp, "CE"))

        put_ltp = self.get_ltp(self.put_sym)
        listt.append((self.put_sym, put_ltp, "PE"))

        self.ticks_queue.put(listt)

       
    def start(self):

        print("Datafeed process has started.")

        
        while True:

            if self.strategy_state.value == StrategyState.NEWREQ_PRE_SENT.value:

                self.fill_ticks_queue()

                #print(self.ltp_list)
            
            elif self.strategy_state.value == StrategyState.NEWREQ_SENT.value:

                #print("Request has been sent for new Order.")
                pass
            
            elif self.strategy_state.value == StrategyState.TRADE_CONFIRM.value:

                pass

            elif self.strategy_state.value == StrategyState.NEWREQ_REJ.value:

                pass

            elif self.strategy_state.value == StrategyState.NEWREQ_CXL.value:

                pass

            elif self.strategy_state.value == StrategyState.MODREQ_PRE_SENT.value:

                pass

            elif self.strategy_state.value == StrategyState.MODREQ_SENT.value:

                pass

            elif self.strategy_state.value == StrategyState.MOD_CONFIRM.value:

                pass

            elif self.strategy_state.value == StrategyState.MODREQ_REJ.value:

                pass

            elif self.strategy_state.value == StrategyState.MODREQ_CXL.value:

                pass

            elif self.strategy_state.value == StrategyState.CXLREQ_PRE_SENT.value:

                pass

            elif self.strategy_state.value == StrategyState.CXLREQ_SENT.value:

                pass

            elif self.strategy_state.value == StrategyState.CXL_CONFIRM.value:

                pass

            elif self.strategy_state.value == StrategyState.CXLREQ_REJ.value:

                pass

            elif self.strategy_state.value == StrategyState.CXLREQ_CXL.value:

                pass

            sleep(1)


    