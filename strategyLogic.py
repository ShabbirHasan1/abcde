from time import sleep
import datetime

from pyparsing import condition_as_parse_action
from globalEnums import OrderType, StrategyState, Expiry, OrderState
from globalStructs import OrderTkt
from globalFunctions import get_atm_strike, get_equity_symbol, get_opt_symbol, get_script_info, get_expiry
from log import get_logger

logger = get_logger()

class StrategyLogic:

    def __init__(self, fyers_client, strategy_details, orders_queue, ord_rsp_queue, global_objects) -> None:
        
        self.fyers_client   = fyers_client
        self.orders_queue   = orders_queue
        self.ord_rsp_queue  = ord_rsp_queue
        #self.logs_queue     = logs_queue

        self.strategy_details = strategy_details
        self.base_sym         = strategy_details['base_sym']
        self.script_info      = get_script_info(self.base_sym)

        self.base_formatted_sym      = get_equity_symbol(self.script_info["exchange"], self.base_sym)

        self.strategy_state = 0
        #self.order_state    = global_objects["order_state"]

        # main order tickets for legs fired
        self.call_info = OrderTkt().local_ord_tkt()
        self.put_info  = OrderTkt().local_ord_tkt()

        self.entry_price = None
        self.curr_price  = None

        self.stoploss = None
        self.target   = None

        self.dummy_count = 0
        self.trading_start_datetime = datetime.datetime.combine(self.strategy_details["date"], self.strategy_details["start_time"])

        self.local_id = 0

    def get_ltp(self, symbol):

        data_info = {
            "symbols" : symbol
        }

        response = self.fyers_client.quotes(data_info)

        #print("Response: ", response)
        if response["s"] == "error":
            print(response['message'])
            logger.info(response['message'])

            return None

        if response is None:
            logger.info("Response from Exchange is None. May be you are not connected to internet.")
            return response

        #logger.info(f"Response from exchange is: {response}")
        #print("Response from exchange is: ", response)

        for data in response['d']:
            symbol  = data['n']
            ltp     = data['v']['lp']
            bid     = data['v']['bid']
            ask     = data['v']['ask']
            spread  = data['v']['spread']

        #print("Ltp is: ", ltp)

        return ltp

    def creating_local_ord_tkts(self):
        
        base_sym_ltp = self.get_ltp(self.base_formatted_sym)
        
        
        if base_sym_ltp is None:
            logger.info("Base symbol Ltp is None.")
            return

        logger.info(f"Base Symbol ltp is: {base_sym_ltp}")
        
        #listt.append((self.base_formatted_sym, base_sym_ltp, "INDEX"))

        atm_strike = get_atm_strike(base_sym_ltp, self.script_info["strike_diff"])

        self.put_info["ticker"] = get_opt_symbol(self.script_info["exchange"], self.base_sym, atm_strike, get_expiry(Expiry.WEEKLY.value), "PE")
        self.call_info["ticker"]  = get_opt_symbol(self.script_info["exchange"], self.base_sym, atm_strike, get_expiry(Expiry.WEEKLY.value), "CE")
        logger.info(f"Call Symbol: {self.call_info['ticker']}")
        logger.info(f"Put Symbol: {self.put_info['ticker']}")

        #call_ltp = self.get_ltp(self.call_sym)
        #listt.append((self.call_sym, call_ltp, "CE"))

        #put_ltp = self.get_ltp(self.put_sym)
        #listt.append((self.put_sym, put_ltp, "PE"))

    #def set_default_values(self):

    def manage_lcl_ord_tkt(self, symbol, ord_tkt):
        
        if self.call_info['ticker'] == symbol:
            self.call_info["local_id"]      = self.local_id
            self.call_info["original_qty"]  = ord_tkt["qty"]
            self.call_info["side"]          = ord_tkt["side"]
            self.call_info["type"]          = ord_tkt["type"]

        elif self.put_info['ticker'] == symbol:
            self.put_info["local_id"] = self.local_id
            self.put_info["original_qty"] = ord_tkt["qty"]
            self.put_info["side"] = ord_tkt["side"]
            self.put_info["type"] = ord_tkt["type"]
        
        self.local_id += 1

    def create_order_tickets(self, symbol):
        '''
        this function will validate all things before creating an order ticket
        '''

        logger.info("Creating Order Ticket.")

        lot_size = 25

        ord_tkt = {
            "symbol"       : symbol,
            "qty"          : 1*lot_size,
            "type"         : OrderType.MARKET.value,
            "side"         : -1,
            "productType"  : "MARGIN",
            "limitPrice"   : 0,
            "stopPrice"    : 0,
            "validity"     : "DAY",
            "disclosedQty" : 0,
            "offlineOrder" : "False",
            "stopLoss"     : 0,
            "takeProfit"   : 0
        } 

        logger.info(f"Order ticket created for {symbol}")
        logger.info(ord_tkt)

        #self.manage_lcl_ord_tkt(symbol, ord_tkt)

        return ord_tkt

    def fire_new_order(self):
        '''
        this function will fill order queue once the tickets are created
        '''
        listt = []
        listt.append(self.create_order_tickets(self.call_info["ticker"]))
        listt.append(self.create_order_tickets(self.put_info["ticker"]))

        self.orders_queue.put((1, listt))
        
        logger.info("Order is filled by Strategy Logic Class.")

        self.strategy_state += 1
        #self.manage_strategy_state()

    def manage_strategy_state(self):
        
        if self.strategy_state.value == StrategyState.NEWREQ_PRE_SENT.value:
            self.strategy_state.value = StrategyState.NEWREQ_SENT.value
            logger.info(f"Current Strategy State is: {self.strategy_state.value}")

    def trade_confirmed(self, ord_rsp):

        sym = ord_rsp["symbol"]

        if self.call_info["ticker"] == sym:
        
            
            self.call_info['busy']          = 1
            self.call_info['order_id']      = ord_rsp["id"] 
            self.call_info['state']         = OrderState.IN_TRADE.value
            self.call_info['side']          = ord_rsp["side"]
            self.call_info['ticker']        = sym     
            self.call_info['last_filled_price'] = float(ord_rsp["tradedPrice"])   
            self.call_info['filled_qty']    =  ord_rsp["filledQty"]   
            self.call_info['remaining_qty'] = ord_rsp["remainingQuantity"]    
            self.call_info['opt_type']      = "CE"
        

        elif self.put_info["ticker"] == sym:
        
            
            self.put_info['busy']          = 1
            self.put_info['order_id']      = ord_rsp["id"] 
            self.put_info['state']         = OrderState.IN_TRADE.value
            self.put_info['side']          = ord_rsp["side"]
            self.put_info['ticker']        = sym        
            self.put_info['last_filled_price'] = float(ord_rsp["tradedPrice"])
            self.put_info['filled_qty']    =  ord_rsp["filledQty"]   
            self.put_info['remaining_qty'] = ord_rsp["remainingQuantity"]    
            self.put_info['opt_type']      = "PE"

        else:
            logger.info("Invalid Order Response.")
            logger.info(self.call_info['last_filled_price'])

        if self.call_info['last_filled_price'] is not None and self.put_info['last_filled_price'] is not None: 
            self.entry_price =  self.call_info['last_filled_price'] + self.put_info['last_filled_price']
            logger.info(f"EntryPrice: {self.entry_price}")

            self.stoploss = self.entry_price + self.strategy_details["stoploss_points"]
            logger.info(f"Stoploss for this trade is: {self.stoploss}")
            
            self.target   = self.entry_price - self.strategy_details["target_points"]
            logger.info(f"Target for this trade is: {self.target}")

            self.strategy_state += 1

    def handle_in_trade(self):
        
    
        call_ltp = self.get_ltp(self.call_info['ticker'])
        put_ltp  = self.get_ltp(self.put_info['ticker'])

        if call_ltp is None or put_ltp is None:
            logger.info("Response is None. Check Whether your are connected to Exchange or not. ")
            return None

        self.curr_price = call_ltp + put_ltp

        logger.info(f"Current Premium is: {self.curr_price}")

        if self.stoploss is not None and  self.curr_price >= self.stoploss:
            # send empty dict to exit all open positions
            data = (-1, {}) # -1 means we are exiting a position

            logger.info(f"Stoploss: {self.stoploss} is hit. Sending order to exit all open positions.")
            self.orders_queue.put(data)
            self.strategy_state += 1
        
        elif self.target is not None and self.curr_price <= self.target:
            # send empty dict to exit all open positions
            data = (-1, {}) # -1 means we are exiting a position

            logger.info("Target is hit. Sending order to exit all open positions.")
            self.orders_queue.put(data)
            self.strategy_state += 1

 

    def restart(self):
        self.start()

    def start(self):

        logger.info("Strategy Logic process has started.")
        # curr_dt = datetime.datetime.now()

        # sleep(1)

        while True:
            
            if self.strategy_state == 0:
                self.creating_local_ord_tkts()
            
                self.fire_new_order()

                #print(self.strategy_state)
                #print("Orders Filled are")
                #print(self.orders_queue.get())

            if self.strategy_state == 1:
                self.strategy_state += 1
            #print("Checking")
            
            if self.strategy_state == 2:
                try:

                    # for now we will recieve order here only when both orders are placed 
                    ord_rsp = self.ord_rsp_queue.get(block=False)
                
                    logger.info("Trade confirmation response is received from ExchComm.")
                    self.trade_confirmed(ord_rsp)
                
                except:
                    pass
                

            if self.entry_price is not None and self.strategy_state == 3:
            
                self.handle_in_trade()

                sleep(3)
            
            if self.strategy_state == 4:
                break

            #print("Hello")
            #print(StrategyState.TRADE_CONFIRM.value)
        