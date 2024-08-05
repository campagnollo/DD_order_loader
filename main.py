#import sweetgreen_nyc
from DD_order_loader import active_orders, cava_nyc, sweetgreen_nyc


def main():
    cava_nyc_list = cava_nyc.order_pull()
    sweetgreen_list = sweetgreen_nyc.order_pull()
    pulled_list = cava_nyc_list + sweetgreen_list
    print(pulled_list)
    if pulled_list:
        active_orders.active_order_list(order_list=pulled_list)




if __name__ == '__main__':
    main()
