import random

# Variables to store constraints
total_bids = 160
high_bid_count = 120
high_rated_cust_bid_count = 60
samsung_bids = 50
high_samsung_bids = 20
high_rated_samsung_bids = 5

# List of customers with rating > 20 and < 20
high_rating_customers = list(range(250, 301))  # Customer IDs from 250 to 300
low_rating_customers = list(range(200, 250))  # Customer IDs from 200 to 250

# List of products
products = list(range(51, 100))    # Product IDs from 51 to 99
samsung_product = [100]  # Product ID for Samsung S23 Ultra

# Function to generate a bid
def generate_bid(custIDs, prodIDs, min_bid, max_bid):
    custID = random.choice(custIDs)
    prodID = random.choice(prodIDs)
    bid = round(random.uniform(min_bid, max_bid), 2)
    return (custID, prodID, bid)

# Containers to store bids
all_bids = []

# Generate 50 bids for Samsung S23 Ultra
for _ in range(samsung_bids):
    if _ < high_samsung_bids:
        if _ < high_rated_samsung_bids:
            # High rated customer bids for Samsung S23 Ultra
            bid = generate_bid(high_rating_customers, samsung_product, 1000, 2000)
        else:
            # Low rated customer bids for Samsung S23 Ultra
            bid = generate_bid(low_rating_customers, samsung_product, 1000, 2000)
    else:
        # Lower bids for Samsung S23 Ultra
        bid = generate_bid(low_rating_customers, samsung_product, 200, 999)
    all_bids.append(bid)

# Generate other bids
for _ in range(total_bids - samsung_bids):
    if _ < high_bid_count - high_samsung_bids:
        if _ < high_rated_cust_bid_count - high_rated_samsung_bids:
            # High rated customer bids for other products
            bid = generate_bid(high_rating_customers, products, 1000, 2000)
        else:
            # Low rated customer bids for other products
            bid = generate_bid(low_rating_customers, products, 1000, 2000)
    else:
        # Lower bids for other products
        bid = generate_bid(low_rating_customers, products, 200, 999)
    all_bids.append(bid)

# Print out the bids
for bid in all_bids:
    print(f"INSERT INTO `Auction` (`custID`, `prodID`, `bid`) VALUES ({bid[0]}, {bid[1]}, {bid[2]});")
