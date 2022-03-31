from time import sleep

from numpy import append
from globalEnums import StrategyState
# from log import get_logger
from dataFeed import DataFeed
from globalStructs import OrderTkt

# logger  = get_logger()

class ExchComm:

    def __init__(self, fyers_client, orders_queue, ord_rsp_queue, global_objects) -> None:
        
        self.fyers_client   = fyers_client
        self.orders_queue   = orders_queue
        self.ord_rsp_queue  = ord_rsp_queue
        #self.logs_queue     = logs_queue
        
        self.strategy_state = global_objects["strategy_state"]
        #self.order_state    = global_objects["order_state"]

        self.num_of_ords_placed = 0   # number of orders placed


        self.call_rsp = OrderTkt().order_response()
        self.put_rsp  = OrderTkt().order_response()

        self.datafeed = DataFeed(self.fyers_client)

        self.ord_rsp_list = []
        self.ord_tkt = None

    def handle_ord_rsp(self, ord_rsp):
        
        if ord_rsp['code'] != 200:
            
#             for rsp in ord_rsp['data']:
#                 logger.info(rsp['body']['message'])

            return None
        
        # if order response is 200 then check order code for both legs 
        for rsp in ord_rsp['data']:

#             if rsp['statusCode'] == 200:
                
#                 logger.info(rsp['body']['message'])

                #self.order_ids_list.append(rsp["body"]["id"])

                self.num_of_ords_placed += 1

#         if self.num_of_ords_placed == 2: 
#             logger.info("Both Orders are placed.")   
            
        
#         else:
#             logger.info("All Orders are not placed.")
            
   
    def manage_ord_rsp_queue(self):
        '''
        if all orders are placed then fetch order details from exchange and fill order rsp queue with order details
        '''

      
#         logger.info("Manage order response queue.")

        for order in self.ord_tkt:
            
            sym = order["symbol"]
            # data = {
            #     "id": order_id
            # }
            


            #order_detail = self.fyers_client.orderbook(data=data)

            order_detail = {
                'orderDateTime': '07-Aug-2020 13:09:23', 
                'id': '120080789053', 
                'exchOrdId': '1300000009419529', 
                'side': 1, 
                'segment': 10, 
                'instrument': 0, 
                'productType': 'INTRADAY', 
                'status': 2, 
                'qty': 1, 
                'remainingQuantity': 0, 
                'filledQty': 1, 
                'limitPrice': 0.0, 
                'stopPrice': 0.0, 
                'type': -1, 
                'discloseQty': 0, 
                'dqQtyRem': 0, 
                'orderValidity': 'DAY', 
                'source': 'ITS', 
                'slNo': 2, 
                'fyToken': '10100000003045', 
                'offlineOrder': 'False', 
                'message': 'TRADE CONFIRMED', 
                'orderNumStatus': '120080789053:2', 
                'tradedPrice': self.datafeed.get_ltp(sym), 
                'exchange': 10, 
                'pan': 'AXXXXXXXXN', 
                'clientId': 'FXXXXX2', 
                'symbol': sym, 
                'ch': 0.65, 
                'chp': 0.35, 
                'lp': 185.25, 'ex_sym': 'SBIN', 'description': 'STATE BANK OF INDIA'}

            #logger.info(f"Getting order details for id: {order_id}")
#             logger.info(f"Order Detail: {order_detail}")

            self.ord_rsp_queue.put(order_detail)
            
           


    # def manage_order_state(self):
    #     pass 
   
    def start(self):
#         logger.info("Exchange Communication process has started.")
        
        while True:
            #logger.info("Exch Comm Process is running!")

                try:
                    order_type, order_tkt = self.orders_queue.get(block=False)

                    if order_type == 1:
                        self.ord_tkt = order_tkt

#                         logger.info("Firing New Basket Order.")

                        # for dummy strategy
                        ord_rsp = {
                            "code" : 200,

                            "data" : [
                                        {
                                            "statusCode" : 200,
                                            "body"       : {
                                                            "s":"ok",
                                                            "code":1101,
                                                            "message":"Order submitted successfully. Your Order Ref. No.52104097619",
                                                            "id":"52104097619"
                                                        }
                                        },

                                        {
                                            "statusCode":200,
                                            "body":{
                                            "s":"ok",
                                            "code":1101,
                                            "message":"Order submitted successfully. Your Order Ref. No.52104097620",
                                            "id":"52104097620"
                                        },
                                }
                            ]
                        }

                    # Exit all Open Positions
                    if order_type == -1:
#                         logger.info("Exiting all open positions.")
                        #ord_rsp = self.fyers_client.exit_positions(order_tkt)
                        #print(ord_rsp)
                        break
                        
                    #print("Got an order")
                    #print(order_tkt)

                    if self.num_of_ords_placed < 2:
                        self.handle_ord_rsp(ord_rsp)
                    

                except: 
                    pass
                
                

                if self.num_of_ords_placed == 2:
                    self.manage_ord_rsp_queue()
                    self.num_of_ords_placed += 1
                    
                #print("Just Checking")
        

                

           

                
