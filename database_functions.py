import sqlite3
import datetime
import random

def list_available_players():
    con = sqlite3.connect('players.sqlite')
    cur = con.cursor()
    cur.execute("SELECT name from stammdaten")
    results = cur.fetchall()
    player_names = [result[0] for result in results]
    cur.close()
    return player_names

def get_playerId_by_name(name):
    con = sqlite3.connect('players.sqlite')
    cur = con.cursor()
    cur.execute("SELECT id from stammdaten where LOWER(name)='{}'".format(name.lower()))
    results = cur.fetchall()
    player_id = results[0][0] if len(results) > 0 else -1
    cur.close()
    return player_id


def get_img_by_name(name):
    con = sqlite3.connect('players.sqlite')
    cur = con.cursor()
    cur.execute("SELECT img_filename from stammdaten where LOWER(name)='{}'".format(name.lower()))
    results = cur.fetchall()
    img_filename = results[0][0] if len(results) > 0 else -1
    cur.close()
    return img_filename


def add_game_to_history(player1, player2, winner_pl1 = True, testEntry=0):
    id_1=get_playerId_by_name(player1)
    id_2=get_playerId_by_name(player2)
    w_id = id_1 if winner_pl1 else id_2
    winner = player1 if winner_pl1 else player2
    con = sqlite3.connect('players.sqlite')
    cur = con.cursor()
    cur.execute("INSERT INTO game_history VALUES (NULL, date('now'), {}, {}, {}, {})".format(id_1, id_2, w_id, testEntry))
    con.commit()
    cur.close()
    print(f"Added new match to database: {player1} vs. {player2}. Winner was {winner}.")

#add_game_to_history("Señor Hot Fingers", "El Gran Caero", winner_pl1=True)

def add_average_to_history(player, opponent, average, twenty6, testEntry=0):
    playerId = get_playerId_by_name(player)
    opponentId = get_playerId_by_name(opponent)
    con = sqlite3.connect('players.sqlite')
    cur = con.cursor()
    cur.execute("INSERT INTO averages VALUES (NULL, date('now'), {}, {}, {}, {}, {})".format(playerId, average, opponentId, twenty6, testEntry))
    con.commit()
    cur.close()
    print(f"Added new average to database: {player} - {average}.")

def create_new_player(name, img_path="unknown.jpg"):
    con = sqlite3.connect('players.sqlite')
    cur = con.cursor()
    statement = "INSERT INTO stammdaten VALUES (NULL, '{}', '{}')".format(name,img_path)
    cur.execute(statement)
    con.commit()
    cur.close()
    print(f"Player {name} successfully added.")

# def add_players_img(name,file):
#     with open(file, "x") as new_file:
#         new_file.write(file)
        
        


def return_players_stats(playername):
    stats = {}
    playerId = get_playerId_by_name(playername)
    
    if playerId == -1:
        print("No stats available.")
        return
    else:
        con = sqlite3.connect('players.sqlite')
        cur = con.cursor()
        
        cur.execute("SELECT COUNT(*) FROM game_history WHERE first_playerId = '{}' OR second_playerId='{}'".format(playerId, playerId))
        result = cur.fetchall()
        stats["Games"] = result[0][0]
        
        cur.execute("SELECT COUNT(*) FROM game_history WHERE winner_playerId = '{}'".format(playerId))
        result = cur.fetchall()
        stats["Wins"] = result[0][0]
        
        stats["Wins in %"] = stats["Wins"] / stats["Games"] * 100
        cur.execute("SELECT AVG(average) FROM averages WHERE playerId = '{}'".format(playerId))
        result = cur.fetchall()
        stats["Average"] = result[0][0]
        
        cur.close()
        return stats
    
# shf_stats = return_players_stats("Señor Hot Fingers")
# add_game_to_history("El Gran Caero", "Señor Hot Fingers", winner_pl1=False, testEntry=1)
# add_average_to_history("Señor Hot Fingers", "Hallos", random.randint(1, 60), 3, testEntry=1)