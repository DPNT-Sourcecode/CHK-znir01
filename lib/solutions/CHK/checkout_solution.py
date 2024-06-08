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
    "K": [80, "2K for 150"],
    "L": [90, ""],
    "M": [15, ""],
    "N": [40, "3N get one M free"],
    "O": [10, ""],
    "P": [50, "5P for 200"],
    "Q": [30, "3Q for 80"],
    "R": [50, "3R get one Q free"],
    "S": [30, ""],
    "T": [20, ""],
    "U": [40, "3U get one U free"],
| V    | 50    | 2V for 90, 3V for 130  |
| W    | 20    |                        |
| X    | 90    |                        |
| Y    | 10    |                        |
| Z    | 50    |                        |
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
    
    special_offer = item_data[item][1].split(",")[offer_index].strip()
  
    special_offer_words = special_offer.split(" ") 

    # the quantity involved in the special offer
    # strip out the words and just leave the number from the 
    # first word of the special offer string
    buy_target_quantity = int(re.findall("\d+", special_offer_words[0])[0])

    buy_target_item = re.findall("[A-Z]", special_offer_words[0])[0]


    # # discount target 

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


def calculate_item_discount(item_counts, discounts):

    discount_value_total = 0
    
    number_of_discounted_items = 0

    for discount in discounts:
        
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


print(checkout("FFFFFFFFF"))














