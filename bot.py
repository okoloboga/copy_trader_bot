from pybit.unified_trading import HTTP
import pprint
import time

api_key_donare=input('Введи API KEY аккаунта, с которого будут копироваться ордера:')
api_secret_donare=input('Введи API secret аккаунта, с которого будут копироваться ордера:')
api_key_target=input('Введи API KEY аккаунта, на который будут копироваться ордера:')
api_secret_target=input('Введи API secret аккаунта, на который будут копироваться ордера:')

session_donare = HTTP(
    testnet=False,
    api_key=api_key_donare,
    api_secret=api_secret_donare
)

session_target = HTTP(
    testnet=False,
    api_key=api_key_target,
    api_secret=api_secret_target
)

category = 'spot'


def get_and_place_order(category: str, orderbook_donare: dict, orderbook_donare_cleaned: dict, orderbook_target_cleaned: dict):

    for order in orderbook_donare['result']['list']:      
        clean_order =  {'orderId': order['orderId'],
                        'category': category,
                        'symbol': order['symbol'],
                        'isLeverage': order['isLeverage'],
                        'side': order['side'],
                        'orderType': order['orderType'],
                        'price': order['price'],
                        'triggerDirection': order['triggerDirection'],
                        'triggerBy': order['triggerBy'],
                        'triggerPrice': order['triggerPrice'],
                        'orderIv': order['orderIv'],
                        'positionIdx': order['positionIdx'],
                        'orderLinkId': order['orderLinkId'],
                        'takeProfit': order['takeProfit'],
                        'stopLoss': order['stopLoss'],
                        'tpTriggerBy': order['tpTriggerBy'],
                        'slTriggerBy': order['slTriggerBy'],
                        'smpType': order['smpType'],
                        'qty': order['qty'],
                        'timeInForce': order['timeInForce'],
                        'reduceOnly': order['reduceOnly'],
                        'closeOnTrigger': order['closeOnTrigger']
                        }
        
        if clean_order['orderId'] not in orderbook_donare_cleaned:
            orderbook_donare_cleaned[clean_order['orderId']]=clean_order        
           
        if clean_order['orderId'] not in orderbook_target_cleaned:             
            session_target.place_order(
                category=clean_order['category'],
                symbol=clean_order['symbol'],
                isLeverage=clean_order['isLeverage'],
                side=clean_order['side'],
                orderType=clean_order['orderType'],
                price=clean_order['price'],
                triggerDirection=clean_order['triggerDirection'],
                triggerBy=clean_order['triggerBy'],
                triggerPrice=clean_order['triggerPrice'],
                orderIv=clean_order['orderIv'],
                positionIdx=clean_order['positionIdx'],
                takeProfit=clean_order['takeProfit'],
                stopLoss=clean_order['stopLoss'],
                tpTriggerBy=clean_order['tpTriggerBy'],
                slTriggerBy=clean_order['slTriggerBy'],
                smpType=clean_order['smpType'],
                qty=clean_order['qty'],
                timeInForce=clean_order['timeInForce'],
                reduceOnly=clean_order['reduceOnly'],
                closeOnTrigger=clean_order['closeOnTrigger']
            )
            orderbook_target = session_target.get_open_orders(
                            category=category,
                            openOnly=0
                            )
            new_order_real_id=orderbook_target['result']['list'][0]['orderId']
            orderbook_target_cleaned[clean_order['orderId']]=clean_order.copy()
            orderbook_target_cleaned[clean_order['orderId']].update({'orderId': new_order_real_id})
      

def check_orderbook(orderbook_donare: dict, orderbook_donare_cleaned: dict, orderbook_target_cleaned: dict):

    donare_real_ids = [order['orderId'] for order in orderbook_donare['result']['list']]

    for id in orderbook_donare_cleaned.copy():
        if id not in donare_real_ids:
            real_target_id=orderbook_target_cleaned[id]['orderId']
            category=orderbook_target_cleaned[id]['category']
            symbol=orderbook_target_cleaned[id]['symbol']
            session_target.cancel_order(category=category,
                                        symbol=symbol,
                                        orderId=real_target_id)
            del orderbook_target_cleaned[id]
            del orderbook_donare_cleaned[id]


def main():
    print('Started work')

    orderbook_donare_cleaned = {}
    orderbook_target_cleaned = {}

    while True:

        orderbook_donare = session_donare.get_open_orders(
                            category=category,
                            openOnly=0
                            )
        
        print('Donare\n')
        pprint.pprint(orderbook_donare_cleaned)
        print('Target\n')
        pprint.pprint(orderbook_target_cleaned)
        

        get_and_place_order(category, orderbook_donare, orderbook_donare_cleaned, orderbook_target_cleaned)
        check_orderbook(orderbook_donare, orderbook_donare_cleaned, orderbook_target_cleaned)        

        time.sleep(5)

if __name__ == '__main__':
    main()
