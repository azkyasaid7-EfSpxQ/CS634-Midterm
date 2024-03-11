#!/usr/bin/env python
# coding: utf-8

# In[5]:


#!/usr/bin/env python
import random
import pandas as pd

items = {
    "Walmart": ["Bread", "Milk", "Coffee", "Eggs", "Cheese"],
    "Target": ["Bananas", "Apples", "Oranges", "Lettuce", "Tomatoes"],
    "Costco": ["Pasta", "Sauce", "Meat", "Chicken", "Rice"],
    "KMart": ["Soap", "Shampoo", "Toothpaste", "Deodorant", "Razors"],
    "Smiths": ["T-shirts", "Jeans", "Shoes", "Hats", "Bags"],
}

store_dataframes = {}
for store_name, items_list in items.items():
    all_items = {
        "high": items_list[:2],
        "medium": items_list[2:4],
        "low": items_list[4:5], 
    }
    transactions = []

    for _ in range(50):
        size = random.randint(1, 4)  
        transaction = []

        for _ in range(size):
            roll = random.random()
            if roll < 0.5:
                item = random.choice(all_items["high"])
            elif roll < 0.8:
                item = random.choice(all_items["medium"])
            else:
                if all_items["low"]:  
                    item = random.choice(all_items["low"])
                else:
                    continue  

            if item not in transaction:
                transaction.append(item)

        transactions.append(transaction)

    df = pd.DataFrame(transactions)
    store_dataframes[store_name] = df
    df.to_csv(f"{store_name}_data.csv", index=False)

