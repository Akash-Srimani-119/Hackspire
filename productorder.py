import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import finalstore1
import finalstore2
import finalstore3

def load_orders():
    try:
        orders_df = pd.read_csv('orders.csv', parse_dates=['Order Date'])
        return orders_df
    except FileNotFoundError:
        print("No orders found, starting with an empty order list.")
        return pd.DataFrame(columns=['Product Name', 'Shop', 'Order Date', 'Order Quantity'])

def save_orders(orders_df):
    orders_df.to_csv('orders.csv', index=False)

def combine_csv_files(file_names):
    dataframes = [pd.read_csv(file) for file_names in file_names]
    combined_df = pd.concat(dataframes, ignore_index=True)
    return combined_df

def demand_forecasting_for_all_shops(product_name):
    shop1_files = ["shop_1_combined.csv"]
    shop2_file = ["shop_2.csv"]
    shop3_file = ["shop_3.csv"]

    reorder_dates = {}
    reorder_dates['shop1'] = finalstore1.demand_forecasting_main(shop1_files, product_name)
    reorder_dates['shop2'] = finalstore2.demand_forecasting_main(shop2_file, product_name)
    reorder_dates['shop3'] = finalstore3.demand_forecasting_main(shop3_file, product_name)

    return reorder_dates

def take_orders(product_name):
    reorder_dates = demand_forecasting_for_all_shops(product_name)
    orders_df = load_orders()

    new_orders = []
    for shop, reorder_date in reorder_dates.items():
        if reorder_date:
            new_order = {
                'Product Name': product_name,
                'Shop': shop,
                'Order Date': reorder_date[0],
                'Order Quantity': reorder_date[1]
            }
            new_orders.append(new_order)
            print(f"Order placed for {product_name} in {shop} on {reorder_date[0]} for {reorder_date[1]} units")
        else:
            print(f"No reorder needed for {product_name} in {shop}")

    if new_orders:
        new_orders_df = pd.DataFrame(new_orders)
        orders_df = pd.concat([orders_df, new_orders_df], ignore_index=True)

    save_orders(orders_df)

if __name__ == "__main__":
    product_name_input = input("Enter the product name: ")
    take_orders(product_name_input)
