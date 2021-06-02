import json
import numpy as np
import pandas as pd
import csv

f=open("data/wnba_players.json")
player_id = []
data = json.load(f)
#for k,v in data.items():
    #print(k, v)
#    player_id.append(v)

#for i in data:
 #   print(i, data[i])


pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
filename = "data/WNBA_rapm_possessions_2018.csv"
fields = []
rows = []
  
# reading csv file
with open(filename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)
      
    # extracting field names through first row
    fields = next(csvreader)
  
    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)
  
    # get total number of rows
    print("Total no. of rows: %d"%(csvreader.line_num))
  
# printing the field names
print('Field names are:' + ', '.join(field for field in fields))




#possessions = pd.read_csv("data/rapm_possessions.csv")
#player_names = pd.read_csv("data/player_names.csv")
"""
def build_player_list(posessions):
    players = list(
        set(list(posessions['offensePlayer1Id'].unique()) + list(posessions['offensePlayer2Id'].unique()) + list(
            posessions['offensePlayer3Id']) + \
            list(posessions['offensePlayer4Id'].unique()) + list(posessions['offensePlayer5Id'].unique()) + list(
            posessions['defensePlayer1Id'].unique()) + \
            list(posessions['defensePlayer2Id'].unique()) + list(posessions['defensePlayer3Id'].unique()) + list(
            posessions['defensePlayer4Id'].unique()) + \
            list(posessions['defensePlayer5Id'].unique())))
    players.sort()
    return players

player_list = build_player_list(possessions)

def map_players(row_in, players):
    p1 = row_in[0]
    p2 = row_in[1]
    p3 = row_in[2]
    p4 = row_in[3]
    p5 = row_in[4]
    p6 = row_in[5]
    p7 = row_in[6]
    p8 = row_in[7]
    p9 = row_in[8]
    p10 = row_in[9]

    rowOut = np.zeros([len(players) * 2])

    rowOut[players.index(p1)] = 1
    rowOut[players.index(p2)] = 1
    rowOut[players.index(p3)] = 1
    rowOut[players.index(p4)] = 1
    rowOut[players.index(p5)] = 1

    rowOut[players.index(p6) + len(players)] = -1
    rowOut[players.index(p7) + len(players)] = -1
    rowOut[players.index(p8) + len(players)] = -1
    rowOut[players.index(p9) + len(players)] = -1
    rowOut[players.index(p10) + len(players)] = -1

    return rowOut


# Break the dataframe into x_train (nxm matrix), y_train (nx1 matrix of target values), and weights (not necessary because all rows will have 1 possession)
def convert_to_matricies(possessions, name, players):
    # extract only the columns we need

    # Convert the columns of player ids into a numpy matrix
    stints_x_base = possessions.as_matrix(columns=['offensePlayer1Id', 'offensePlayer2Id',
                                                      'offensePlayer3Id', 'offensePlayer4Id', 'offensePlayer5Id',
                                                      'defensePlayer1Id', 'defensePlayer2Id', 'defensePlayer3Id',
                                                      'defensePlayer4Id', 'defensePlayer5Id'])
    # Apply our mapping function to the numpy matrix
    stint_X_rows = np.apply_along_axis(map_players, 1, stints_x_base, players)

    # Convert the column of target values into a numpy matrix
    stint_Y_rows = possessions.as_matrix([name])

    # extract the possessions as a pandas Series
    possessions = possessions['possessions']

    # return matricies and possessions series
    return stint_X_rows, stint_Y_rows, possessions

#for i in data['players']:
 #   print(i)
 """
 
 