"""
This modula provides generals utilities to the project
"""

import random

def select_on_prob(item_list, prob_list):
    """
    select an item form item_list based on the probability provided in prob_list.
    note that the element of item_list and prob_list should be one to one match
    :param item_list: a list of items
    :param prob_list: a list of numeric values, each one element represents the probability of choosing the corresponding
            item
    :return: the item selected
    """
    if not len(item_list) == len(prob_list):
        raise Exception('util: selct_on_prob func: invalid input')
    total = 0
    for num in prob_list:
        total += num
    flag = random.uniform(0,total)
    cumulative_probability = 0.0
    for item,prob in (item_list,prob_list):
        cumulative_probability += prob_list
        if flag < cumulative_probability:
            return item