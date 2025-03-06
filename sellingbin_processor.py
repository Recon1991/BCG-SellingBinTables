import os
import json
import csv

# Define the directory where the JSON file is located
directory = 'zip_archives/sellingbin'

# Define the specific JSON file name to look for
json_filename = 'selling_bin.json'
json_file_path = os.path.join(directory, json_filename)

# Define the emerald to coin conversion rate
EMERALD_TO_COIN_RATE = 4  # 1 emerald = 4 coins

# Coin tier conversion rates
COIN_TIERS = {
    "gold": 64,
    "iron": 16,
    "copper": 4
}  # 64 copper = 1 gold, 16 copper = 1 iron, 4 copper = 1 coin

# Function to convert coins into tiered denominations
def convert_to_coins(total_coins):
    gold = total_coins // COIN_TIERS["gold"]
    remainder = total_coins % COIN_TIERS["gold"]
    iron = remainder // COIN_TIERS["iron"]
    remainder %= COIN_TIERS["iron"]
    copper = remainder // COIN_TIERS["copper"]
    coin = remainder % COIN_TIERS["copper"]
    
    return {
        "gold": gold,
        "iron": iron,
        "copper": copper,
        "coin": coin
    }

# Check if the file exists in the directory
if not os.path.isfile(json_file_path):
    print(f"{json_filename} not found in the directory.")
else:
    # Step 1: Load the JSON data from the file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Step 2: Prepare a list to store trade data along with trade ratios
    trade_data = []

    # Step 3: Process each trade, convert emeralds to coins, and calculate trade ratios
    for trade in data['trades']:
        # Extract item names and counts
        input_item = trade['input']['filter'].split(':')[-1].replace('_', ' ')
        input_count = trade['input']['count']
        output_item = trade['output']['item'].split(':')[-1].replace('_', ' ')
        output_count = trade['output']['count']
        
        # Convert emeralds to coins if applicable
        if output_item == 'emerald':
            output_item = 'coin'
            output_count *= EMERALD_TO_COIN_RATE
        
        # Convert coins into tiered denominations
        coin_conversion = convert_to_coins(output_count)
        
        # Calculate trade ratio (output count / input count)
        trade_ratio = output_count / input_count if input_count != 0 else 0
        
        # Append the trade data including trade ratio and coin breakdown
        trade_data.append({
            'Input Item': input_item,
            'Input Count': input_count,
            'Output Item': output_item,
            'Output Count': output_count,
            'Trade Ratio': trade_ratio,
            'Gold Coins': coin_conversion["gold"],
            'Iron Coins': coin_conversion["iron"],
            'Copper Coins': coin_conversion["copper"],
            'Coins': coin_conversion["coin"]
        })

    # Step 4: Sort trades by trade ratio in descending order
    sorted_trade_data = sorted(trade_data, key=lambda x: x['Trade Ratio'], reverse=True)

    # Step 5: Write sorted trade data to CSV
    output_csv_path = 'trades_output_sorted.csv'
    with open(output_csv_path, 'w', newline='') as csv_file:
        fieldnames = ['Input Item', 'Input Count', 'Output Item', 'Output Count', 'Trade Ratio', 'Gold Coins', 'Iron Coins', 'Copper Coins', 'Coins']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        
        for trade in sorted_trade_data:
            writer.writerow({
                'Input Item': trade['Input Item'],
                'Input Count': f"{trade['Input Count']:,}",
                'Output Item': trade['Output Item'],
                'Output Count': f"{trade['Output Count']:,}",
                'Trade Ratio': f"{trade['Trade Ratio']:.4f}",
                'Gold Coins': f"{trade['Gold Coins']:,}",
                'Iron Coins': f"{trade['Iron Coins']:,}",
                'Copper Coins': f"{trade['Copper Coins']:,}",
                'Coins': f"{trade['Coins']:,}"
            })

    print(f"Data written to {output_csv_path} successfully from {json_file_path}!")
