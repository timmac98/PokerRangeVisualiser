import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PyQt5.QtWidgets import QApplication, QLabel

rank_o = ['Ao', 'Ko', 'Qo', 'Jo', 'To', '9o', '8o', '7o', '6o', '5o', '4o', '3o', '2o']
rank_s = ['2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As']
rank1 = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
rank2 = ['s', 'o']
hand_list = []
card_num = len(rank1)
card_num_list = range(card_num)

# create list of hand rankings ordered from A to 2 (s, o)
for i in card_num_list:
    hand = rank1[i] + rank1[i]
    hand_list.append(hand)
    for j in range(card_num - (i + 1)):
        j += i + 1
        hand_suit = rank1[i] + rank1[j] + rank2[0]
        hand_off = rank1[i] + rank1[j] + rank2[1]
        hand_list.append(hand_suit)
        hand_list.append(hand_off)


def create_dict(filename='ReportExport', stat='Raise First', stat2=''):
    """
    Assigns weights for the desired statistic to hand dictionary
    :param filename: filename not including csv extension
    :param stat: desired statistic other potential options: 'Raise First', '3Bet PF'
    :param stat2: same as stat
    :return: returns dictionary with hand list as keys and weights from file as value
    """
    hand_dict = dict(zip(hand_list, np.zeros(169)))
    raw_data = pd.read_csv(f'{filename}.csv')
    hand_data = raw_data[['Hand', stat, 'Hands']]
    for i in range(len(hand_data.iloc[:, 0])):
        hand_dict[str(hand_data.iloc[i, 0])] = hand_data.iloc[i, 1]
    return hand_dict


def create_array(hand_dict, hand_list):
    """
    Converts dictionary of weights into an array for use with plotly
    :param hand_dict: key = hand, value = weight
    :param hand_list: list of starting hands from A to 2
    :return: an array of data and starting hands
    """
    a_list = [0, 22, 42, 60, 76, 90, 102, 112, 120, 126, 130, 132, 132]
    inc_list = [-1, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]
    data = [[] for i in card_num_list]
    label = [[] for i in card_num_list]
    for i in card_num_list:
        i_new = 0 + 2 * i
        for j in card_num_list:
            k = i + 1
            if j >= k:
                b = j + a_list[i] + inc_list[i] + card_num_list[j - i]
                data[i].append(hand_dict[hand_list[b]])
                label[i].append(hand_list[b])
            elif j == k - 1:
                b = j + a_list[i] + inc_list[i] + 1
                data[i].append(hand_dict[hand_list[b]])
                label[i].append(hand_list[b])
            elif j < k:
                b = j + i_new + a_list[j]
                data[i].append(hand_dict[hand_list[b]])
                label[i].append(hand_list[b])
    return data, label
