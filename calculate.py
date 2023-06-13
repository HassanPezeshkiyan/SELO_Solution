import os

def delta(player_1, player_2):
    return 1 / (1 + 2**((player_1 - player_2) / 100))


def read_SELO_point():
    player_point ={}
    with open('players.csv', 'r') as readFile:
        next(readFile)
        for line in readFile:
            try:
                line = line.split(',')
                player_point[line[0]] = int(line[1])
            except:
                pass
    readFile.close()
    return player_point



def winner(dataRow):
    if str(dataRow[2]).strip() == '1-0':
        return dataRow[0], dataRow[1]
    elif str(dataRow[2]).strip() == '0-1':
        return dataRow[1], dataRow[0]



def calculate_SELO():
    
    players_SELO = read_SELO_point()
    players_name = players_SELO.keys()
    match_winner = ''
    match_loser = ''
    output_list = []
    with open('games.csv', 'r') as readFile:
        
        next(readFile)
        
        for line in readFile:
            
            line = line.split(',')
            
            if line[2].strip() != '1/2-1/2':
                match_winner = winner(line)[0]
                match_loser = winner(line)[1]
            
            if match_loser in players_name:
                loser_pre_point = players_SELO[match_loser]
            else:
                loser_pre_point = 1500
                
            if match_winner in players_name:
                winner_pre_point = players_SELO[match_winner]
            else:
                winner_pre_point = 1500
                
            point_value = round(delta(winner_pre_point, loser_pre_point)*200)
            
            if point_value > 0 :
                winner_new_point = point_value + winner_pre_point
                loser_new_point = loser_pre_point - point_value 
            else:
                winner_new_point = winner_pre_point 
                loser_new_point = loser_pre_point
            output_list.append({
                
                    'winner' : match_winner,
                    'loser' : match_loser,
                    'winnerPoint' : winner_new_point,
                    'loserPoint' : loser_new_point
                    
                })
    readFile.close()
    
    return output_list


def update_SELO(dictOfResult : dict):
    
    pre_players_file = read_SELO_point()
    pre_players_name = pre_players_file.keys()

    try:
        os.remove('players.csv')
    except:
        print("something wrong...")
        
        
    if dictOfResult['winner'] in pre_players_name:
        pre_players_file[dictOfResult['winner']] = dictOfResult['winnerPoint']
    else:
        pre_players_file[dictOfResult['winner']] = dictOfResult['winnerPoint']

    if dictOfResult['loser'] in pre_players_name:
        pre_players_file[dictOfResult['loser']] = dictOfResult['loserPoint']
    else:
        pre_players_file[dictOfResult['loser']] = dictOfResult['loserPoint']


    with open('players.csv', 'w') as writeFile:
        writeFile.write('PLAYER,SELO \n')
        for i in pre_players_file.items():
            writeFile.write(f"{i[0]},{i[1]} \n")

def display_players():
    with open('players.csv', 'r') as read:
        
        next(read)
        data = read.readlines()
        
        def sorting_items(data):
           return data.split(',')[1].strip()

    data.sort(key=sorting_items, reverse=True)
    
    for item in data:
        item = item.split(',')
        print(f"{item[0]}: {item[1]}")
        
        
def main():
    calculating_selo = calculate_SELO()
    for item in calculating_selo:
        update_SELO(item)

    display_players()
    
if __name__ == "__main__":
    main()