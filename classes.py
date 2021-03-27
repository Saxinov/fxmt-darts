from helpers import possible_scores
from playsound import playsound
from database_functions import get_playerId_by_name, get_img_by_name



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
    
     
    def validate_user_score(self):
        next_player = False
        
        while not next_player:
            correct_input = False
            while not correct_input:
                try:
                    user_score = int(input("What was your Score?: "))
                    correct_input = True
                except ValueError:
                    print("Score must be a number.")
            
            if user_score not in possible_scores :
                print("That score doesn't exist.")
            elif user_score > self.current_score:
                print("Bust. That was too much.")
                next_player = True
                self.dart_counter += 3
                self.last_score
                return user_score
            else:
                next_player = True
                self.dart_counter += 3
                self.last_score = user_score
                return user_score
    
    
    def play_round(self):
        name = self.name
        print(f"\n{name}: It's your turn...")
        open_score = self.current_score - self.validate_user_score() #validate user score refactoren --> user score muss benutzbar sein
        self.comment()
        if self.last_score == 26:
            self.twenty6 += 1
        if open_score == 0:
            print(f"Win for {name}!! You are a hero. Open a beer and smoke a Joint!")
            self.has_won = True
            return
        self.current_score = open_score
        average = self.calc_average()
        print(f"\n{name}: {open_score} points left.\n")
        print(f"Current 3-dart average: {average}")
    
    def comment(self):
        if self.last_score in audio_dict.keys():
            playsound(audio_dict[self.last_score])
        else:
            return
        
    
    def calc_average(self):
        number_darts = self.dart_counter
        already_scored = 501 - self.current_score
        avg = round((already_scored / number_darts) * 3, 1)
        self.average = avg
        return avg
    
    def calc_finish(self):
        pass
    
