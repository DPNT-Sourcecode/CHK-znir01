import re

data = {

    "A": [50, "3A for 130, 5A for 200"],
    "B": [30, "2B for 45"],
    "C": [20, ""],
    "D": [15, ""],
    "E": [40, "2E get one B free"],
    "F": [10, "2F get one F free"],
    "G": [20, ""],
    "H": [10, "5H for 45, 10H for 80"],
    "I": [35, ""],
    "J": [60, ""],
    "K": [70, "2K for 120"],
    "L": [90, ""],
    "M": [15, ""],
    "N": [40, "3N get one M free"],
    "O": [10, ""],
    "P": [50, "5P for 200"],
    "Q": [30, "3Q for 80"],
    "R": [50, "3R get one Q free"],
    "S": [20, "buy any 3 of (S,T,X,Y,Z) for 45"],
    "T": [20, "buy any 3 of (S,T,X,Y,Z) for 45"],
    "U": [40, "3U get one U free"],
    "V": [50, "2V for 90, 3V for 130"],
    "W": [20, ""],
    "X": [17, "buy any 3 of (S,T,X,Y,Z) for 45"],
    "Y": [20, "buy any 3 of (S,T,X,Y,Z) for 45"],
    "Z": [21, "buy any 3 of (S,T,X,Y,Z) for 45"]
}

# I am assuming you can't get more than 19 free items in an offer
UNITS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
        ]


def convert_number_string_to_int(number_string):

    if number_string.isnumeric():
        return int(number_string)
    
    for i, word in enumerate(UNITS):
        if word == number_string.lower():
            return i
    
    # If it can't figure out what it is, just return 1
    return 1


def pre_process_discounts(item_data):

    discount_data = {}

    for item in item_data:

        if item not in list(discount_data.keys()):
            discount_data[item] = []

        special_offer_string = item_data[item][1]
        special_offers = special_offer_string.split(",")
        
        for offer_index, offer in enumerate(special_offers):

            if offer: 
                
                parsed_special_offer = parse_special_offer(item, offer_index, item_data)

                if parsed_special_offer["discount quantity"] == "special":
                    discount_data[item].append(parsed_special_offer)
                    break

                else:
                    discount_data[parsed_special_offer["discount target"]].append(parsed_special_offer)

                    # sort it in reverse order of discount value
                    discount_data[parsed_special_offer["discount target"]] = sorted(discount_data[parsed_special_offer["discount target"]], key=lambda d: d['discount value'], reverse=True)
    
    return discount_data


# the occurances of each item category in the skus list

def count_occurances(shopping_list, uniques):

    # create a list of zeroes to represent 
    counts = {}

    # Cycle through all the items and count the occurances of each one 
    for item in uniques:

        # count the occurances 
        count = shopping_list.count(item)

        # store the count 
        counts[item] = count


    return counts


def parse_special_offer(item, offer_index, item_data):

    item_special_offers = item_data[item][1]

    if "any" in item_special_offers:
        
        return parse_bag_special_offer(item_special_offers, item)

    special_offer = item_special_offers.split(",")[offer_index].strip()
  
    special_offer_words = special_offer.split(" ") 

    # the quantity involved in the special offer
    # strip out the words and just leave the number from the 
    # first word of the special offer string
    buy_target_quantity = int(re.findall("\d+", special_offer_words[0])[0])

    buy_target_item = re.findall("[A-Z]", special_offer_words[0])[0]

    if "free" in special_offer_words:
        discount_target = special_offer_words[-2]
        discount_quantity = convert_number_string_to_int(special_offer_words[-3])
        normal_price = 0

        if buy_target_item == discount_target:
            buy_target_quantity += 1

    else:
        discount_target = buy_target_item
        discount_quantity = buy_target_quantity
        normal_price = int(special_offer_words[-1])
        

    discount_target_individual_value = item_data[discount_target][0]
    discount_value = (discount_quantity * discount_target_individual_value) - normal_price
    
    return {
        "buy target": buy_target_item,
        "buy quantity": buy_target_quantity,
        "discount target": discount_target,
        "discount value": discount_value,
        "discount quantity": discount_quantity
         }



def parse_bag_special_offer(offer, thing):
    
    offer_words = offer.split(" ")

    buy_target_quantity = int(re.findall("\d+", offer_words[2])[0])
    buy_target_item =  offer_words[4].strip("()").split(",")

    # lets say the user purchases buy_target_quantity of an item, how much are they saving individually?
    
    # The total price if a bag discount is invoked
    discount_price = int(offer_words[-1])

    # the individual price of each item if the bag discount is invoked
    discount_price_individual = discount_price // buy_target_quantity
    
    individual_discounts = {}

    for item in buy_target_item:
        individual_normal_price = data[item][0]
        discount_amount_individual = individual_normal_price - discount_price_individual
        individual_discounts[item] = discount_amount_individual

    
    return {
        "buy target": buy_target_item,
        "buy quantity": buy_target_quantity,
        "discount target": thing,
        "discount value": individual_discounts,
        "discount quantity": "special"
         }


def bag_discount_value(counts, individual_target, discount):
    
    discount_target_values = discount["discount value"]

    individual_target_discount_value = discount_target_values[individual_target] 

    discount_values_ordered = {k: v for k, v in sorted(discount_target_values.items(), key=lambda item: item[1], reverse=True)}
    
    bag_quantity = discount["buy quantity"]

    discount_targets = discount["buy target"]

    # Make a string containing multiples of each bag item, ordered by value
    bag_string = ""

    for item in list(discount_values_ordered.keys()):
        if item in counts.keys():
            item_count = counts[item]
            bag_string += item * item_count

    number_of_bag_items = len(bag_string)
    
    number_of_discounted_bags = number_of_bag_items // bag_quantity

    number_of_discounted_items = number_of_discounted_bags * bag_quantity

    bag_string_discounted_slice = bag_string[:number_of_discounted_items]

    number_of_target_items_discounted = bag_string_discounted_slice.count(individual_target)

    return number_of_target_items_discounted * individual_target_discount_value


def calculate_item_discount(item_counts, discounts):


    discount_value_total = 0
    
    number_of_discounted_items = 0

    for discount in discounts:

        if discount["discount quantity"] == "special":
            
            discount_value_total = bag_discount_value(item_counts, discount["discount target"], discount)
        
        else:
            discount_target = discount["discount target"]
            discount_value = discount["discount value"]
            discount_quantity = discount["discount quantity"]

            buy_target_count = item_counts[discount["buy target"]]
            buy_target_quantity = discount["buy quantity"]

            # print(buy_target_count, discount["buy target"])
            number_of_discounts = max((buy_target_count - number_of_discounted_items) // buy_target_quantity, 0)
            

            discount_value_total += number_of_discounts * discount_value
            

            number_of_discounted_items = number_of_discounts * discount_quantity
        
        

    return discount_value_total


def checkout(skus):

    # an empty string should return 0 
    if not skus:
        return 0

    if not skus.isalpha() or not skus.isupper():
        return -1

    # a cumulative total of the price
    price_totals_undiscounted = {}
    price_totals_discounts = {}

    uniques = set(skus)

    # validate that the items in the shopping list are actually in the available items
    for item in uniques:
        if not item in list(data.keys()):
            print(f"Item {item} is not in our database.")
            return -1

    counts = count_occurances(skus, data.keys())
    
    discount_data = pre_process_discounts(data)


    for key in data.keys():
        
        item_count = counts[key]
        item_data = data[key]
        price_item = item_data[0]

        item_total_undiscounted = price_item * item_count

        price_totals_undiscounted[key] = item_total_undiscounted

        # ---------------
        # Discounting

        discounts = discount_data[key]
        item_total_discount = calculate_item_discount(counts, discounts)

        item_total_discounted = max(item_total_undiscounted - item_total_discount, 0)

        price_totals_discounts[key] = item_total_discounted

        # --------
        # summing up


    undiscounted_total = sum(list(price_totals_undiscounted.values()))
    print("Total before discounts:", undiscounted_total)

    discounted_total = sum(list(price_totals_discounts.values()))
    print("Total after discounts:", discounted_total)

    print("Total savings:", undiscounted_total - discounted_total)
    
    return discounted_total


shopping = "AASSASTTXXX"

checkout(shopping)












