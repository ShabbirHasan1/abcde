class OrderTkt:

    def local_ord_tkt(self):

        ord_tkt = {
            'busy'              : None,
            'local_id'          : None,
            'order_id'          : None,
            'state'             : None,
            'side'              : None, # bought or sold
            'ticker'            : None,
            'original_qty'      : None,
            'filled_qty'        : None,
            'canceled_qty'      : None,
            'order_type'        : None,
            'last_filled_price' : None,
            'avg_filled_price'  : None,
            'last_filled_qty'   : None,
            'tot_filled_qty'    : None,
            'exchange'          : None,
            'instrument_type'   : None,
            'opt_type'          : None # call or put
        }

        return ord_tkt

    def exch_order_tkt(self):

        ord_tkt = {

            "symbol"       : None,
            "qty"          : None,  # multiple of lot size
            "type"         : None,  # Market, Limit
            "side"         : None,  # Buy or Sell
            "productType"  : None,  # Margin, Intraday, CNC
            "limitPrice"   : None,
            "stopPrice"    : None,
            "validity"     : None,
            "disclosedQty" : None,
            "offlineOrder" : None,
            "stopLoss"     : None,
            "takeProfit"   : None,
        } 

        return ord_tkt

    def order_response(self):

        ord_rsp = {

            "exch_order_id" : None,
            "id"            : None,
            "local_id"      : None,
            "side"          : None,
            "traded_price"  : None,
            "original_qty"  : None,
            "filled_qty"    : None,
            "canceled_qty"  : None,
            "rem_qty"       : None,
            "status"        : None,
            "type"          : None,
            "message"       : None,
            "symbol"        : None,
        }

        return ord_rsp