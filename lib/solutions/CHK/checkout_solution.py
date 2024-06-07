import re

data = {

    "A": [50, "3A for 130, 5A for 200"],
    "B": [30, "2B for 45"],
    "C": [20, ""],
    "D": [15, ""],
    "E": [40, "2E get one B free"]
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

    item_special_offers_all = {}

    for item in item_data:

        item_special_offers = []
        special_offer_string = item_data[item][1]
        special_offers = special_offer_string.split(",")
        
        for offer_index, offer in enumerate(special_offers):

            if offer: 

                parsed_special_offer = parse_special_offer(item, offer_index, item_data)
                # print(parsed_special_offer)
                # pass


            # if parse_special_offer["discount target"] == item:
            #     print(parse_special_offer["discount target"])
            #     print(item)

            # else: 
            #     pass



# the occurances of each item category in the skus list

def count_occurances(shopping_list, uniques):

    # create a list of zeroes to represent 
    counts = [ 0 for _ in data.keys() ]

    # Cycle through all the items and count the occurances of each one 
    for item in uniques:

        # first, get the index of the item from the original order
        index = list(data.keys()).index(item)

        # count the occurances 
        count = shopping_list.count(item)

        # store the count 
        counts[index] = count

    
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
        

    else:
        discount_target = buy_target_item
        discount_quantity = buy_target_quantity

    print(discount_quantity)
    # discount value

    



    
    



    # the inclusive price of the special offer
    # price = int(special_offer_words[-1])

    # return quantity, price
        

def checkout(skus):

    # an empty string should return 0 
    if not skus:
        return 0

    if not skus.isalpha() or not skus.isupper():
        return -1

    # a cumulative total of the price
    total_price = 0

    # make sure the shopping list is capitalised
    # skus = skus.upper()

    # get the unique items from the shopping list by using a Set
    uniques = set(skus)

    # validate that the items in the shopping list are actually in the available items
    for item in uniques:
        if not item in list(data.keys()):
            print(f"Item {item} is not in our database.")
            return -1

    counts = count_occurances(skus, uniques)
    
    for key, item_count in zip(data.keys(), counts):
        
        item_data = data[key]
        price = item_data[0]
        special_offer = item_data[1]
        
        # check if there's a special offer. If there is, calculate its effect on the bill
        if special_offer:
            
            # get the quantity and inclusive price of the special offer
            special_quantity, special_price = parse_special_offer(special_offer)
            
            # get the number of times this special offer can be accounted for, rounded down 
            # to the nearest whole number
            special_occurances = int(item_count / special_quantity)

            # add the special offer pricing to the total price
            total_price += special_occurances * special_price
            
            # take the special offer items out of the item count
            item_count -= special_occurances * special_quantity

        
        # account for normal non special offer prices of items

        total_price += item_count * price

    return total_price        



pre_process_discounts(data)
# print(convert_number_string_to_int("THREE"))





