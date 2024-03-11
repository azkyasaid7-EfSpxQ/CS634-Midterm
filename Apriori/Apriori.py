#!/usr/bin/env python
# coding: utf-8

# In[6]:


#!/usr/bin/env python
import random
import pandas as pd
import itertools

store_choices = {
    1: "Walmart",
    2: "Target",
    3: "Costco",
    4: "Kmart",
    5: "Smiths"
}

# Get store selection from the user
while True:
    print("Select a store:")
    for number, store in store_choices.items():
        print(f"{number}. {store}")
    try:
        store_choice = int(input("Enter your choice (1-5): "))
        if 1 <= store_choice <= 5:
            store_name = store_choices[store_choice]
            break
        else:
            print("Invalid choice. Please select a number between 1 and 5.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Get support and confidence thresholds from the user
while True:
    try:
        support_threshold = float(input("Enter the minimum support threshold (e.g., 0.01, hint: pick a low #): "))
        min_confidence = float(input("Enter the minimum confidence threshold (e.g., 0.5, hint: pick a low #): "))
        if 0 < support_threshold <= 1 and 0 < min_confidence <= 1:
            break
        else:
            print("Thresholds must be between 0 and 1.")
    except ValueError:
        print("Invalid input. Please enter numerical values.")


# In[8]:


# Load and pre-process data efficiently
d = pd.read_csv(f"{store_name}_data.csv")
d.fillna("", inplace=True)  # Assuming filling NaN with empty strings is sufficient

data = d.values.tolist()
data_clean = [[item for item in transaction if item] for transaction in data]

# Support and confidence thresholds

# Calculate item counts
item_counts = {}
for transaction in data_clean:
    for item in transaction:
        item_counts[item] = item_counts.get(item, 0) + 1

# Filter frequent items (k=1)
frequent_items = {item for item, count in item_counts.items()
                  if count / len(data_clean) >= support_threshold}
supportk1 = {item: count / len(data_clean) for item, count in item_counts.items() if count / len(data_clean) >= support_threshold}

# Calculate pair counts efficiently
pair_counts = {pair: 0 for pair in itertools.combinations(frequent_items, 2)}
for transaction in data_clean:
    transaction_set = set(transaction)  # Faster membership checks
    for pair in pair_counts:
        if pair[0] in transaction_set and pair[1] in transaction_set:
            pair_counts[pair] += 1

# Generate association rules
all_rules = {}
for item_A, item_B in itertools.combinations(frequent_items, 2):
    support_AB = pair_counts[(item_A, item_B)]
    support_A = item_counts[item_A]
    confidence = support_AB / support_A

    if confidence >= min_confidence:
        rule_key = (item_A, item_B)
        all_rules[rule_key] = ((item_A,), (item_B,), confidence)


# In[9]:


supportk2 = {pair: count / len(data_clean) for pair, count in pair_counts.items() if count / len(data_clean) >= support_threshold}

# Frequent Itemsets (k=3) 
triplet_counts = {triplet: 0 for triplet in itertools.combinations(frequent_items, 3)}
for transaction in data_clean:
    transaction_set = set(transaction)
    for triplet in triplet_counts:
        if set(triplet).issubset(transaction_set):  # Efficient check
            triplet_counts[triplet] += 1

supportk3 = {triplet: count / len(data_clean) for triplet, count in triplet_counts.items() if count / len(data_clean) >= support_threshold}


# In[10]:


for itemset in supportk3.keys(): 
    for antecedent in itertools.combinations(itemset, r=2):  
        consequent = tuple(set(itemset) - set(antecedent))
        support_XUY = supportk3[itemset]
        support_X = supportk2[antecedent]  # Get support from k=2
        confidence = support_XUY / support_X

        if confidence >= min_confidence:
            rule_key = antecedent, consequent
            all_rules[rule_key] = (antecedent, consequent, confidence)


# In[11]:


all_frequent_itemsets = {**supportk1, **supportk2, **supportk3}

print("\nFrequent Itemsets:")
sorted_itemsets = sorted(all_frequent_itemsets.items(), key=lambda item: item[1], reverse=True)
for itemset, support in sorted_itemsets:
    print(f"{itemset} (Support: {support:.2f})")
print("\nAssociation Rules:")
sorted_rules = sorted(all_rules.items(), key=lambda item: item[1][2], reverse=True)
for rule, (antecedent, consequent, confidence) in sorted_rules:
    print(f"{antecedent} -> {consequent} (Confidence: {confidence:.2f})") 

