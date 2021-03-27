import numpy as np 

def calculate_possible_scores():     
    singles = np.arange(21)
    doubles = singles * 2
    triples = singles * 3

    first_dart = np.unique(np.concatenate((singles, doubles, triples)))
    first_dart = np.sort(np.append(first_dart, [25, 50]))

    second_dart = np.arange(0)

    for first in first_dart:
        for second in first_dart:
            score_sec = first + second
            second_dart = np.append(second_dart,score_sec)
            
    second_dart = np.unique(second_dart)

    third_dart = np.arange(0)

    for second in second_dart:
        for third in first_dart:
            score_third = second + third
            third_dart = np.append(third_dart,score_third)

    third_dart = np.unique(third_dart)
    return third_dart

possible_scores = calculate_possible_scores()



# rules for finishes
## 2 Dart > 3 Dart
## Bonus für Lieblingsdoppel: 16, 20, 18, 8 
## 
