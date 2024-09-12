import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import finalstore1


def simulate_cargo_shipping(product_name, order_date):
    delivery_time_mean = 48 
    delivery_time_std = 12  
    delivery_time = max(1, int(np.random.normal(delivery_time_mean, delivery_time_std)))
    delivery_dates = [order_date + timedelta(hours=i) for i in range(delivery_time)]

    data = []
    delivered = False
    for timestamp in delivery_dates:
        if not delivered:
            data.append({
                'Timestamp': timestamp,
                'Status': 'In Transit' if timestamp < delivery_dates[-1] else 'Delivered'
            })
            if timestamp >= delivery_dates[-1]:
                delivered = True
        else:
            
            data.append({
                'Timestamp': timestamp,
                'Status': 'Delivered'
            })
            break

    tracking_df = pd.DataFrame(data)
    return tracking_df
# Define the cargo_tracking_main function
def cargo_tracking_main():
    file_names = ["day1 (1).csv", "day2 (1).csv", "day3 (1).csv", "day4 (1).csv", "day5 (1).csv", "day6 (1).csv", "day7 (1).csv"]
    product_name_input = input("Enter the product name: ")  

    # Get reorder date from demand forecasting module
    reorder_date = finalstore1.demand_forecasting_main(file_names, product_name_input)
    
    if reorder_date:
        confirm_reorder = input(f"Reorder needed on {reorder_date}. Do you want to proceed with the cargo tracking simulation? (yes/no): ")
        if confirm_reorder.lower() == 'yes':
            print("Simulating cargo shipping...")
            tracking_df = simulate_cargo_shipping(product_name_input, reorder_date)
            print(tracking_df)  # Print tracking_df here
        else:
            print("Reorder is cancelled by the user.")
    else:
        print("No reorder needed")

# Main function for demand forecasting
def demand_forecasting_main(file_names, product_name_input):
    # Your existing demand forecasting code here
    pass

if __name__ == "__main__":
    cargo_tracking_main()
