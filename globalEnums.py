import enum

class Expiry(enum.Enum):
    WEEKLY = 1
    MONTHLY = 2

class OrderSide(enum.Enum):
    BUY  = 1
    SELL = -1

# Position Side
class PosSide(enum.Enum):
    LONG   =  1
    SHORT  = -1
    CLOSED =  0

class OrderType(enum.Enum):
    LIMIT      = 1	# Limit order
    MARKET     = 2	# Market order
    STOP       = 3	# Stop order (SL-M)
    STOP_LIMIT = 4	# Stoplimit order (SL-L)

class OrderStatus(enum.Enum):
    CXL     = 1	    # Cancelled
    TRADED  = 2	    # Traded / Filled
    TRANSIT = 4	    # Transit
    REJ     = 5	    # Rejected
    PEND    = 6	    # Pending

class OrderState(enum.Enum):
    
    NO_BID      =   1   # no order is placed yet
    IN_BID      =   2   # order is placed but not confirmed
    IN_TRADE    =   3   # trade is placed 

class StrategyState(enum.Enum):
    
    BLACKHOLE = 0

    # Possible states for new order
    NEWREQ_PRE_SENT = 1     # no new order is placed at this moment, we can have running trades at this moment
    NEWREQ_SENT     = 11    # request sent for new order (it can get confirmed, rejected or we will cancel it)
    TRADE_CONFIRM   = 111   # trade is confirmed for the request sent 
    NEWREQ_CXL      = -11   # we have canceled the request we had sent 
    NEWREQ_REJ      = -111  # request for new order has been rejected from exchange
    
    # Possible states for order modification
    MODREQ_PRE_SENT = 2     # no new order is placed at this moment, we can have running trades at this moment
    MODREQ_SENT     = 22    # request sent for new order (it can get confirmed, rejected or we will cancel it)
    MOD_CONFIRM  = 222   # trade is confirmed for the request sent 
    MODREQ_CXL      = -22   # we have canceled the request we had sent 
    MODREQ_REJ      = -222  # request for new order has been rejected from exchange
    
    # Possible states for order cancellation
    CXLREQ_PRE_SENT = 3     # no new order is placed at this moment, we can have running trades at this moment
    CXLREQ_SENT     = 33    # request sent for new order (it can get confirmed, rejected or we will cancel it)
    CXL_CONFIRM  = 333   # trade is confirmed for the request sent 
    CXLREQ_CXL      = -33   # we have canceled the request we had sent 
    CXLREQ_REJ      = -333  # request for new order has been rejected from exchange

class Exchanges(enum.Enum):
    NSE = 10        # (National Stock Exchange)
    MCX = 11        # (Multi Commodity Exchange)
    BSE = 12        # (Bombay Stock Exchange)

class Segments(enum.Enum):
    CM   = 10	    # Capital Market
    ED   = 11	    # Equity Derivatives
    CURD = 12	    # Currency Derivatives
    COMD = 20	    # Commodity Derivatives

class InstrumentType(enum.Enum):
	# EQ (EQUITY)
    PREFSHARES  =   1
    DEBENTURES  =   2
    WARRANTS    =   3
    MISC        =   4
    INDEX       =   10
	# FO segment 
    FUTIDX      =   11      # Future Index
    FUTIVX      =   12      # Future Volatility Index
    FUTSTK      =   13      # Future Stock
    OPTIDX      =   14      # Option Index
    OPTSTK      =   15      # Option Stock
	# CD segment
    FUTCUR      =   16
    FUTIRT      =   17
    FUTIRC      =   18
    OPTCUR      =   19
    UNDCUR      =   20
    UNDIRC      =   21
    UNDIRT      =   22
    UNDIRD      =   23
    INDEX_CD    =   24
    FUTIRD      =   25
	# COM segment
    # FUTIDX    =   11
    FUTCOM      =   30
    OPTFUT      =   31
    OPTCOM      =   32


class LotSize(enum.Enum):

    NIFTY     = 50
    BANKNIFTY = 25

#print(InstrumentType.FUTIDX.value)