from flask import Flask, render_template, make_response, jsonify, request, session, redirect, url_for
from database_functions import list_available_players, add_game_to_history, create_new_player, add_average_to_history
from classes import Player
from helpers import possible_scores
from urllib.parse import unquote

app = Flask(__name__)
app.secret_key = "Random String"

def calculate_average(open_score, dart_counter):
    try:
        avg = round(((501-open_score)/dart_counter)*3,2)
    
    except ZeroDivisionError:
        avg = 0
    return avg

@app.route("/")
def greet():
    
    players = []
    for player in list_available_players():
        players.append(Player(player,501))
        
    return render_template("index.html", players=players)

@app.route("/add-player")
def add_player():
    return render_template("add_player.html")


@app.route("/create-player")
def create_player():
    player_name = request.args["name"]
    create_new_player(unquote(player_name))
    message="Successfully added player."
    return "<p>success.</p>",200

@app.route("/select-player", methods=["POST"])
def select_player():
    data = request.get_json()
    session["1"] = Player(data["player1"], 501).__dict__
    session["2"] = Player(data["player2"], 501).__dict__
    res = jsonify({
        "player1": session["1"],
        "player2": session["2"]
    })
            
    return res, 200

    
@app.route("/validate/<player>/<int:score>")
def validate_score(player, score):
   cur_player=session[player]
   if score not in possible_scores:
       message="That score doesnt exist."
       return(jsonify(message), 420)
   
   elif score > cur_player["current_score"]:
       cur_player["dart_counter"] += 3
       cur_player["average"] = calculate_average(cur_player["current_score"],cur_player["dart_counter"])
       session[player] = cur_player
       res = jsonify(cur_player)
       return (res, 200)
   
   else:
       cur_player["dart_counter"] += 3
       cur_player["current_score"] -= score
       cur_player["average"] = calculate_average(cur_player["current_score"],cur_player["dart_counter"])
       cur_player["last_score"] = score
       
       if score == 26:
        cur_player["twenty6"] += 1 
       
       session[player] = cur_player
       return(jsonify(cur_player),200)  
   
@app.route("/game-end/<player>")
def end_game(player):
    winners_name = session[player]["name"]
    add_game_to_history(session["1"]["name"], session["2"]["name"], winner_pl1=(player=="1"),testEntry=1)
    add_average_to_history(session["1"]["name"], session["2"]["name"], session["1"]["average"],session["1"]["twenty6"])
    add_average_to_history(session["2"]["name"], session["1"]["name"], session["2"]["average"],session["2"]["twenty6"])
    session["1"] = None
    session["2"] = None
    return "<h1>The winner is: {}</h1>".format(winners_name)
    
@app.route("/delete-last-score/<player>")
def delete_score(player):
    cur_player = session[player]
    if cur_player["dart_counter"] > 2:
        cur_player["current_score"] += cur_player["last_score"]
        cur_player["dart_counter"] -= 3
        cur_player["average"] = calculate_average(cur_player["current_score"],cur_player["dart_counter"])
        if cur_player["last_score"] == 26:
            cur_player["twenty6"] -= 1 

        session[player] = cur_player
        return jsonify(session[player]), 200
    
    else:
        res = jsonify({"message": "No score to delete."})
        return res, 400
    
        

if __name__=="__main__":           
    app.run(debug=True)
    
    
    
    
### wie kann ich die Spiel Logik in Flask importieren?