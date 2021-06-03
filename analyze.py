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
    #print("Total no. of rows: %d"%(csvreader.line_num))
  
# printing the field names
#print('Field names are:' + ', '.join(field for field in fields))
key_list=list(data.keys())
val_list=list(data.values())
#rint(val_list)
#print(res)
#print(key_list)


players_id = []
players_name = []
i=1
j=1
#players_id.append(return_key("Ally Mallott"))

"""
while i<=5:
    name = input("Enter offensive player "+str(i)+" name ")
    res = val_list.index(name)
    players_id.append(key_list[res])
    i=i+1

while j<=5:
    name = input("Enter defensive player "+str(i)+" name ")
    res = val_list.index(name)
    players_id.append(key_list[res])
    i=i+1

print(players_id)
"""


possessions = pd.read_csv("data/WNBA_rapm_possessions_2018.csv",usecols = ['off1','off2','off3','off4','off5','def1','def2','def3','def4','def5','Points'])
print(type(possessions))
#player_names = pd.read_csv("data/player_names.csv")

def build_player_list(posessions):
    players = list(
        set(list(posessions['off1'].unique()) + list(posessions['off2'].unique()) + list(
            posessions['off3']) + \
            list(posessions['off4'].unique()) + list(posessions['off5'].unique()) + list(
            posessions['def1'].unique()) + \
            list(posessions['def2'].unique()) + list(posessions['def3'].unique()) + list(
            posessions['def4'].unique()) + \
            list(posessions['def5'].unique())))
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

    #rapm_data = pd.read_csv(filename) 
    #gfg = pd.DataFrame(data['Weight'])

    # Convert the columns of player ids into a numpy matrix
    stints_x_base = possessions.to_numpy()
    # Apply our mapping function to the numpy matrix
    stint_X_rows = np.apply_along_axis(map_players, 1, stints_x_base, players)

    # Convert the column of target values into a numpy matrix#
    stint_Y_rows = possessions.to_numpy([name])

    # extract the possessions as a pandas Series
    possessions = possessions['possessions']

    # return matricies and possessions series
    return stint_X_rows, stint_Y_rows, possessions


train_x, train_y, possessions_raw = convert_to_matricies(possessions, 'PointsPerPossession', player_list)



def calculate_rapm(train_x, train_y, possessions, lambdas, name, players):
    # convert our lambdas to alphas
    alphas = [lambda_to_alpha(l, train_x.shape[0]) for l in lambdas]

    # create a 5 fold CV ridgeCV model. Our target data is not centered at 0, so we want to fit to an intercept.
    clf = RidgeCV(alphas=alphas, cv=5, fit_intercept=True, normalize=False)

    # fit our training data
    model = clf.fit(train_x, train_y, sample_weight=possessions)

    # convert our list of players into a mx1 matrix
    player_arr = np.transpose(np.array(players).reshape(1, len(players)))

    # extract our coefficients into the offensive and defensive parts
    coef_offensive_array = np.transpose(model.coef_[:, 0:len(players)])
    coef_defensive_array = np.transpose(model.coef_[:, len(players):])

    # concatenate the offensive and defensive values with the playey ids into a mx3 matrix
    player_id_with_coef = np.concatenate([player_arr, coef_offensive_array, coef_defensive_array], axis=1)
    # build a dataframe from our matrix
    players_coef = pd.DataFrame(player_id_with_coef)
    intercept = model.intercept_

    # apply new column names
    players_coef.columns = ['playerId', '{0}__Off'.format(name), '{0}__Def'.format(name)]

    # Add the offesnive and defensive components together (we should really be weighing this to the number of offensive and defensive possession played as they are often not equal).
    players_coef[name] = players_coef['{0}__Off'.format(name)] + players_coef['{0}__Def'.format(name)]

    # rank the values
    players_coef['{0}_Rank'.format(name)] = players_coef[name].rank(ascending=False)
    players_coef['{0}__Off_Rank'.format(name)] = players_coef['{0}__Off'.format(name)].rank(ascending=False)
    players_coef['{0}__Def_Rank'.format(name)] = players_coef['{0}__Def'.format(name)].rank(ascending=False)

    # add the intercept for reference
    players_coef['{0}__intercept'.format(name)] = intercept[0]

    return players_coef, intercept
#for i in data['players']:
 #   print(i)
 
 
 