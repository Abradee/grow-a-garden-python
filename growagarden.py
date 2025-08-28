# Grow A Garden in Python
# (c) Abradee 2025
# GPL v3 License
# v3.7, More the Merrier Update (+ Bug Fixes)
# https://abradee.github.io/growagarden/ for more info about the game (not done yet)

import time
import random
import json
import os
import platform

# Platform detection
def osdetect():
    os_name = platform.system()
    
    if os_name == "Linux":
        print("\n\nWARNING: Save files do not work on your version.\nFor them to work, use a Windows PC\n\n")

# Save/Load system
SAVE_FILE = "save.growagarden"  # Change if you want a different file type or to use a different save file.

def save_game():
    print("Saving game...")
    save_data = {
        "grownitems": grownitems,
        "inventory": inventory,
        "plantingitems": plantingitems,
        "money": money,
        "last_restock_time": last_restock_time,
        "shop_stock": shop_stock
    }
    with open(SAVE_FILE, "w") as file:
        json.dump(save_data, file)
    print("Game saved.")

def load_game():
    global grownitems, inventory, plantingitems, money, last_restock_time, shop_stock
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            save_data = json.load(file)
            grownitems = save_data.get("grownitems", [])
            inventory = save_data.get("inventory", [])
            plantingitems = save_data.get("plantingitems", [])
            money = float(save_data.get("money", 0.0))
            last_restock_time = float(save_data.get("last_restock_time", time.time()))
            shop_stock = save_data.get("shop_stock", {})
        print("Save loaded from", SAVE_FILE)
    else:
        print("No save file found, starting new game.")

# Startup
print("Welcome to Grow a Garden PYTHON EDITION")
print("(c) Abradee 2025")
print("Hint: You start with one carrot! Do 'plant' to get started!")
osdetect()

# Setup variables
grownitems = []
inventory = ["carrot seed"]
plantingitems = []
money = 0.0
shop_stock = {}
last_restock_time = time.time()
restock_interval = 120.0  # 2 minutes
autosave_interval = 30.0  # 30 seconds
last_autosave_time = time.time()
crasha = False
total_earned = 0.0


mutations = [
    "obama",
    "moonlit", 
    "touched by god",
    "silver",
    "golden",
    "platinum",
    "sigma",
    "lava",
    "touched jaymins rolls",
    "windstruck",
    "",
]
mutatechance = random.randint(0,10)
mutationinterval = 300
lastmutation = 0

plant_data = {
    "carrot": {"seed_price": 5.0, "sell_price": 10.0},
    "potato": {"seed_price": 8.0, "sell_price": 15.0},
    "tomato": {"seed_price": 12.0, "sell_price": 18.0},
    "strawberry": {"seed_price": 18.0, "sell_price": 20.0},
    "pumpkin": {"seed_price": 50.0, "sell_price": 80.0},
    "dragonfruit": {"seed_price": 100.0, "sell_price": 150.0},
    "blueberry": {"seed_price": 10.0, "sell_price": 13.0},
    "beanstalk": {"seed_price": 150.0, "sell_price": 200.0},
    "cocoa": {"seed_price": 125.0, "sell_price": 175.0},
    "ember lily": {"seed_price": 175.0, "sell_price": 250.0},
    "sugar apple": {"seed_price": 250.0, "sell_price": 300.0},
    "burning bud": {"seed_price": 150.0, "sell_price": 275.0},
    "elder strawberry": {"seed_price": 300.0, "sell_price": 325.0},
    "giant pinecone": {"seed_price": 350.0, "sell_price": 400.0},
    "romanesco": {"seed_price": 500.0, "sell_price": 1500.0},
    "dih": {"seed_price": 1.0, "sell_price": 50000.0},
    "jaymin": {"seed_price": 10000, "sell_price": -10.0},
}

item_weights = {
    "carrot": 100.0,
    "potato": 30.0,
    "tomato": 15.0,
    "strawberry": 10.0, 
    "pumpkin": 12.0,     
    "dragonfruit": 6.0,
    "blueberry": 60.0,
    "beanstalk": 20.0,
    "cocoa": 18.0,
    "ember lily": 15.0,
    "sugar apple": 13.0,
    "burning bud": 10.0,
    "elder strawberry": 6.0,
    "giant pinecone": 5.0,
    "romanesco": 2.0,
    "dih": 0.001,
    "jaymin": 2,
}

# Restock shop with weighted randomness (supports floats)
def restock_shop():
    global shop_stock, last_restock_time
    shop_stock.clear()

    items = list(item_weights.keys())
    weights = list(item_weights.values())

    for _ in range(random.randint(3, 5)):
        plant = random.choices(items, weights=weights, k=1)[0]
        seed_name = f"{plant} seed"
        quantity = float(random.randint(1, 5))
        shop_stock[seed_name] = shop_stock.get(seed_name, 0.0) + quantity

    last_restock_time = time.time()
    print("\nThe shop has been restocked!\n")

# Load game if possible
load_game()

# If shop is empty, restock initially
if not shop_stock:
    restock_shop()

# Main game loop
while True:
    if crasha == True:
        while crasha == True:
            print("pow pow!!")
    current_time = time.time()

    # Auto-restock
    if current_time - last_restock_time > restock_interval:
        restock_shop()

    # Auto-save
    if current_time - last_autosave_time > autosave_interval:
        save_game()
        last_autosave_time = current_time
    
    # Mutate every 300 seconds
    if current_time - lastmutation > mutationinterval:
        mutatechance = random.randint(0,1)
        if mutatechance == 1:
            lastmutation = current_time
            
            

    cmd = input("Type 'help' for help: ").strip().lower()

    if cmd == "help":
        print("Commands:")
        print("sell - Sell all grown crops")
        print("plant - Plants all available seeds")
        print("shop - Open the shop")
        print("inventory - View your items")
        print("save - saves the game")
        print("quit - Exit the game")

    elif cmd == "shop":
        print("\nWelcome to the Shop!")
        print("Your Money:", money)
        if not shop_stock:
            print("The shop is currently out of stock. Please check back later.")
        else:
            seed_list = list(shop_stock.items())
            for i, (seed, qty) in enumerate(seed_list, start=1):
                plant = seed.replace(" seed", "")
                price = plant_data[plant]["seed_price"]
                print(f"{i}. {seed} - ${price} (In stock: {qty})")

            choice = input("Enter the number of the item to buy (or 'exit'): ").strip()
            if choice.lower() == "exit":
                print("Leaving the shop.")
                continue
            if not choice.isdigit() or not (1 <= int(choice) <= len(seed_list)):
                print("Invalid choice.")
                continue

            selected_seed, available_qty = seed_list[int(choice) - 1]
            plant = selected_seed.replace(" seed", "")
            price = plant_data[plant]["seed_price"]

            qty_input = input(f"How many {selected_seed}s would you like to buy? ").strip()
            if not qty_input.isdigit():
                print("Invalid quantity.")
                continue

            qty = float(qty_input)
            total_cost = qty * price

            if qty > available_qty:
                print("The shop doesn't have that many in stock.")
            elif money < total_cost:
                print("You don't have enough money.")
            else:
                money -= total_cost
                shop_stock[selected_seed] -= qty
                if shop_stock[selected_seed] <= 0.0:
                    del shop_stock[selected_seed]
                inventory.extend([selected_seed] * int(qty))
                print(f"Bought {qty} x {selected_seed} for ${total_cost}.")
                print("Money left:", money)

    elif cmd == "plant":
        seeds_planted = False
        for item in inventory[:]:
            if item.endswith("seed"):
                plant = item.replace(" seed", "")
                inventory.remove(item)
                plantingitems.append(plant)
                print(f"Planting a {plant}...")
                for pct in range(0, 101, 10):
                    print(f"{pct}%")
                    time.sleep(random.uniform(0.3, 1.6))
                print(f"Your {plant} is fully grown! Sell it with the command 'sell'")
                grownitems.append(plant)
                seeds_planted = True
        if not seeds_planted:
            print("You have no seeds to plant!")

    elif cmd == "sell":
        if not grownitems:
            print("You have nothing to sell!")
        else:
            total_earned = 0.0
            sellwhat = input("What do you want to sell: ").strip().lower()
            if sellwhat in grownitems:
                
                item = sellwhat
                value = plant_data[item]["sell_price"]
                money += value
                total_earned += value
                print(f"Sold {item} for ${value}")
            else:
                print("You don't have that item.")
        print("Total earned:", total_earned)
        print("Money:", money)

    elif cmd == "inventory":
        print("Inventory:", inventory)
        print("Grown Items:", grownitems)
        print("Money:", money)
    
    if cmd == "save":
        save_game()
    
    if cmd == "crasha":
        confirm = input("Are you sure? (y/n)").strip().lower()
        if confirm == "y":
            print("Enabling in 2 seconds...")
            time.sleep(2.0)
            crasha = True
            print("Hit enter.")
        if confirm == "n":
            print("Ok.")
            
    if cmd == "info":
        print("Game info:")
        print(" ")
        print("Most info at https://abradee.github.io")
        print("Do help for a list of commands")


    
    elif cmd == "quit":
        save_game()
        print("Thanks for playing! Goodbye.")
        break
    
    