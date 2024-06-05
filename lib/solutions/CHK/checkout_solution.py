data = {

    "A": [50, "3A for 130 "],
    "B": [30, "2B for 45"],
    "C": [20, ""],
    "D": [15, ""]
}

skus = "ABBACDDA"


# the occurances of each item category in the skus list

def count_occurances(shopping_list):

    # create a list of zeroes to represent 
    counts = [ 0 for _ in data.keys() ]

    # get the unique items from the shopping list by using a Set
    uniques = Set(shopping_list)


# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    



