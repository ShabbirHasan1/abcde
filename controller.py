import yaml
from fyers_api import fyersModel
import datetime
import logging
from time import sleep
from multiprocessing import Process, Queue, Value
from dataFeed import DataFeed
from strategyLogic import StrategyLogic
from exchComm import ExchComm
from access_token import get_fyers_object
from globalEnums import StrategyState

from log import get_logger

logger = get_logger()

class Controller:

    def __init__(self, strategy_details) -> None:
        
        self.strategy_details = strategy_details
        self.client_local_id  = strategy_details["local_id"]
        self.client_info      = self.get_client_info()
        self.base_sym         = strategy_details["base_sym"]

        self.access_token = self.get_access_token()
        self.fyers_client = get_fyers_object(self.client_info["client_app_id"], self.access_token)

        # initialize all queues
        
        self.orders_queue   = Queue()
        self.exch_ord_queue = Queue()
        self.ord_rsp_queue  = Queue()

        self.global_objects = self.get_global_objects()

        self.initialize_all_processes()

    def validate_conn(self):
        pass

    def get_client_info(self):

        filee = open("client_details.yml")
        parser = yaml.load(filee, Loader=yaml.FullLoader)

        for id in parser:
            if id == self.client_local_id:
                return parser[id]        

    def get_access_token(self):

        filee = open("tokens.yml")
        parser = yaml.load(filee, Loader=yaml.FullLoader)

        for id in parser:
            if id == self.client_local_id:
                return parser[id]["access_token"]

    def get_global_objects(self):
        
        global_obj = {
            
            # Value('i') is a multiprocessing integer value placed in a shared memory block
            # multiple processes can access this value and also modify them
            'strategy_state'   :  Value('i', StrategyState.NEWREQ_PRE_SENT.value),  # new request present state
            #'call_order_state' :  Value('i', 1),  # new request present state,
            #'put_order_state'  :  Value('i', 1)   
        }

        return global_obj
 
    def initialize_all_processes(self):
        #self.datafeed       = DataFeed(self.fyers_client, self.base_sym, self.ticks_queue, self.logs_queue, self.global_objects)
        self.exch_comm      = ExchComm(self.fyers_client, self.orders_queue, self.ord_rsp_queue, self.global_objects)
        self.strategy_logic = StrategyLogic(self.fyers_client, self.strategy_details, self.orders_queue, self.ord_rsp_queue, self.global_objects)

        #self.datafeed_proc       = Process(target=self.datafeed.start)
        self.exch_comm_proc      = Process(target=self.exch_comm.start)
        self.strategy_logic_proc = Process(target=self.strategy_logic.start)

    def start_all_processes(self):
        #print("Start All Processes.")
        logger.info("Start All Processes.")
        #self.datafeed_proc.start()
        self.exch_comm_proc.start()
        self.strategy_logic_proc.start()
        

    def kill_all_processes(self):
        #self.datafeed_proc.join()
        self.exch_comm_proc.join()
        self.strategy_logic_proc.join()

    def check(self):
        #print(self.fyers_client.get_profile())
        #print(self.client_info)
        obj = DataFeed(self.fyers_client)
        print(obj.get_ltp("NSE:NIFTY50-INDEX"))

    def start(self):
        
        self.start_all_processes()

        #print("All Processes have started.")
        logger.info("All Processes have started.")

        while True:

            try:
                logger.info("Validating connection")
                self.validate_conn()
            
            except KeyboardInterrupt:

                print("Killing all processes.")
                self.kill_all_processes()

                print("All Processes are killed successfully.")

                break
            
            sleep(2)



# if __name__ == "__main__":

trading_date   = datetime.date.today()
start_time     = datetime.time(9, 20)  

strategy_details = {
    'local_id'   : 3,
    'date'       : trading_date,
    'start_time' : start_time,
    'base_sym'   : "BANKNIFTY",
    'stoploss_points'   : 100,
    'target_points'     : 200,
}

controller = Controller(strategy_details)

controller.start()
#controller.check()

#print(strategy_details)
        