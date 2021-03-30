from flask import Flask, render_template, make_response, jsonify, request, session, redirect, url_for
from database_functions import *
from urllib.parse import unquote

app = Flask(__name__)
app.secret_key = "Random String"

POSSIBLE_SCORES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 164, 165, 167, 168, 170, 171, 174, 177, 180]
class Player:
    def __init__(self, name, game_length):
        self.name = name
        self.game_length = game_length
        self.current_score = game_length
        self.has_won = False
        self.dart_counter = 0
        self.average = 0
        self.twenty6 = 0
        self.last_score = 0
        self.playerId = get_playerId_by_name(self.name)
        self.img_path = get_img_by_name(self.name)

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

@app.route("/welcome/<player>")
def welcome(player):
    new_player = unquote(player)
    return render_template("welcome.html", player=new_player)


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
   if score not in POSSIBLE_SCORES:
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

  
@app.route("/game-end/<player>")
def end_game(player):
    delete_test_entries()
    try:
        winner = session[player]
        add_game_to_history(session["1"]["name"], session["2"]["name"], winner_pl1=(player=="1"),testEntry=1)
        add_average_to_history(session["1"]["name"], session["2"]["name"], session["1"]["average"],session["1"]["twenty6"])
        add_average_to_history(session["2"]["name"], session["1"]["name"], session["2"]["average"],session["2"]["twenty6"])
        session["1"] = None
        session["2"] = None
        return render_template("game-end.html", winner=winner)
    
    except TypeError:
        return redirect(url_for('greet'), 301)
    
    

    
        

if __name__=="__main__":           
    app.run(debug=True)
    
    
    
    
### wie kann ich die Spiel Logik in Flask importieren?