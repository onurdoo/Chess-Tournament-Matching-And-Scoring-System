import math


def main():
    player_data = get_player_input()
    sorted_player_data = sorting_players(player_data)
    print_starting_table(sorted_player_data)
    set_tournament_data(sorted_player_data)


def get_player_input():  # Created a function for getting input data
    NON_ELO_BORDER = 0  # the value of the player without elo and ukd points
    MIN_ELO_BORDER = 1000  # lowest elo and ukd value a player can get
    player_l_no = []  # Store license numbers of players
    player_data_dict = {}  # Store all players data
    score = 0.00  # Player's tournament score
    rank = 0  # Player's tournament rank
    color = ''  # Player's color value
    result_list = []  # Store players match results
    bye_check = False  # variable that controls whether the player has passed the round bye
    starting_no = 0  # Player's tournament starting rank
    color_list = []  # Store players color that they had
    opponent_list = []  # Store the license number of opponents faced by players
    opponent_srno_list = []  # Store the starting ranks of opponents faced by players
    play_check = False  # variable that controls whether the player has played in the round
    BH_1 = 0  # Player's Buchholz-1 value
    BH_2 = 0  # Player's Buchholz-2 value
    SB = 0  # Player's Sonneborn Berger value
    GS = 0  # Player's win number value

    l_no = get_digit_input("Please enter the player's license number(0 or negative to terminate): ")

    while l_no > 0:

        player_l_no.append(l_no)
        name = input("Please enter the player's name and surname: ").replace('i', 'İ').upper()
        while name == '':  # Incorrect inputs are received again
            name = input("Please enter the player's name and surname: ").replace('i', 'İ').upper()

        elo = get_digit_input("Please enter player's elo(at least 1000, otherwise 0): ")
        while not (elo >= MIN_ELO_BORDER or elo == NON_ELO_BORDER):  # Incorrect inputs are received again
            elo = get_digit_input("Please enter player's elo(at least 1000, otherwise 0): ")

        ukd = get_digit_input("Please enter player's ukd(at least 1000, otherwise 0): ")
        while not (ukd >= MIN_ELO_BORDER or ukd == NON_ELO_BORDER):  # Incorrect inputs are received again
            ukd = get_digit_input("Please enter player's ukd(at least 1000, otherwise 0): ")

        player_data_dict.update({
            l_no: [elo, ukd, name, score, starting_no, color, rank,
                   color_list[:], bye_check, result_list[:], opponent_list[:], play_check, BH_1, BH_2, SB, GS,
                   opponent_srno_list[:]]
        })  # Dictionary filled with .update method

        l_no = get_digit_input("Please enter the player's license number(0 or negative to terminate): ")
        while l_no in player_l_no:  # Incorrect inputs are received again
            l_no = get_digit_input("Please enter the player's license number(0 or negative to terminate): ")

    return player_data_dict  # return all player's data as dictionary


def get_digit_input(input_text):  # Created a function for checking digits
    while True:
        number = input(input_text)
        if number.lstrip('-').isdigit():
            return int(number)
        else:
            print('Invalid data!')


def sorting_players(player_data):  # Created a function for sorting player lists
    sorted_player_list = []  # Store all players data
    alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ "
    if type(player_data) == dict:
        sorted_player_list = sorted(player_data.items(), key=lambda players: (players[0]))
    elif type(player_data) == list:
        sorted_player_list = sorted(player_data, key=lambda players: (players[0]))

    sorted_player_list.sort(key=lambda players: [alphabet.index(c) for c in players[1][2]])  # [i][1][2] keeps player's name
    sorted_player_list = sorted(sorted_player_list, key=lambda players: (players[1][3], players[1][0],  # [i][1][0] keeps player's elo [i][1][3] keeps player's score
                                                                         players[1][1]), reverse=True)  # [i][1][1] keeps player's ukd
    # List sorted by priorities with sorted and lambda function
    for i in range(len(sorted_player_list)):
        sorted_player_list[i][1][6] = i + 1  # [i][1][6] keeps player's rank
    return sorted_player_list


def print_starting_table(sorted_player_list):  # Created a function for print starting rank table
    print("Starting Ranking List:")
    print("SRNo\tLNo\tName-Surname\t\t  ELO\tUKD")
    print('-' * 4, '', '-' * 5, '-' * 20, '-' * 4, '', '-' * 4)

    for i in range(len(sorted_player_list)):
        sorted_player_list[i][1][4] = i + 1  # [i][1][4] keeps player's starting rank
        print(f'{sorted_player_list[i][1][4]:>4}', end='  ')
        print(f'{sorted_player_list[i][0]:>5} {sorted_player_list[i][1][2]:<20}'  # [i][0] keeps player's license number
              f'{sorted_player_list[i][1][0]:>5}  {sorted_player_list[i][1][1]:>4}')  # [i][1][0] keeps player's elo


def set_tournament_data(sorted_player_list):  # Created a function for generally performing all tournament transactions
    total_player = len(sorted_player_list)
    min_tour = math.ceil(math.log(total_player, 2))
    max_tour = total_player - 1
    tour_num = get_digit_input("Please enter the number of tours in the tournament"
                               "(" + str(min_tour) + "-" + str(max_tour) + "):")  # User determined tournament's tour number
    while not min_tour <= tour_num <= max_tour:  # Incorrect inputs are received again
        tour_num = get_digit_input("Please enter the number of tours in the tournament:")

    first_player_starting_color = input("Please enter the color of the first player in "
                                        "the first tour according to the starting order(w/b)").lower()
    while first_player_starting_color not in ['w', 'b']:  # Incorrect inputs are received again  w: White b: Black
        first_player_starting_color = input("Invalid color try again").lower()
    first_player_starting_color_opp = opposite_color(first_player_starting_color)

    pairing(sorted_player_list, total_player, tour_num, first_player_starting_color, first_player_starting_color_opp)
    tiebreak(sorted_player_list)
    sorted_player_list = final_sorting(sorted_player_list)
    print_final_ranking(sorted_player_list)
    print_cross_table(sorted_player_list, tour_num)


# Created a function for do the pairing process
def pairing(sorted_player_list, total_player, tour_num, first_player_starting_color, first_player_starting_color_opp):
    if total_player % 2 == 0:  # Desks are created according to whether the number of players is odd or even
        total_desk_num = (total_player // 2)
    else:
        total_desk_num = (total_player // 2) + 1
    desks = []  # Stores matched players in each round
    sorted_desks = []  # Stores matched players based on black and white priority each round

    for tours in range(tour_num):
        for i in range(total_desk_num):
            desks.append([])

        if total_player % 2 == 1:
            bye_control(sorted_player_list)

        for i in sorted_player_list:
            temp_score_1 = i[1][3]  # [i][1][3] keeps player's score
            temp_color_1 = i[1][5]  # [i][1][5] keeps player's color

            if tours == 0:
                fist_tour_pairing(desks, first_player_starting_color, first_player_starting_color_opp, i)
            else:

                for x in desks:
                    if len(x) == 0 and not i[1][11]:  # [i][1][11] keeps player's play check
                        x.append(i)
                        i[1][11] = True
                        pair_check = False  # variable controlling player's match
                        while not pair_check and i[1][5] != '-':
                            pairing_1_1(sorted_player_list, i, x, tours, temp_score_1, temp_color_1)
                            if len(x) == 2:  # table length of 2 indicates that the player is matched
                                pair_check = True
                            if not pair_check:
                                pairing_1_2(sorted_player_list, i, x, tours, temp_score_1, temp_color_1)
                                if len(x) == 2:
                                    pair_check = True
                                if not pair_check:
                                    pairing_1_3(sorted_player_list, i, x, tours, temp_score_1, temp_color_1)
                                    if len(x) == 2:
                                        pair_check = True

                                    temp_score_1 -= 0.50  # If the player cannot paired, the temporary score is reduced and the same actions are repeated.
        for i in desks:
            sorted_desks.append(sorted(i, key=lambda players: players[1][5], reverse=True))

        print_pairing_list(sorted_desks, tours)
        match_result(sorted_desks, tours)
        sorted_player_list = sorting_players(sorted_player_list)
        desks.clear()  # The list is emptied for new tour
        sorted_desks.clear()  # The list is emptied for new tour


def bye_control(sorted_player_list):  # Created a function to detect bye players
    for players in reversed(sorted_player_list[:]):
        if not players[1][8]:  # [i][1][8] keeps player's bye check
            players[1][8] = True
            players[1][5] = '-'
            players[1][7].append('-')  # [i][1][7] keeps player's color list
            players[1][9].append('1')  # [i][1][9] keeps player's result list
            players[1][10].append('-')  # [i][1][10] keeps player's opponent list
            players[1][16].append('-')  # [i][1][16] keeps player's opponent starting rank list
            if players[1][8]:
                break


# Created a function to do pairing for only first tour
def fist_tour_pairing(desks, first_player_starting_color, first_player_starting_color_opp, i):
    if i[1][5] != '-':
        if i[1][4] % 2 != 0:
            i[1][5] = first_player_starting_color
            i[1][7].append(first_player_starting_color)

        else:
            i[1][5] = first_player_starting_color_opp
            i[1][7].append(first_player_starting_color_opp)

    for x in desks:
        if len(x) != 2 and not i[1][11]:
            x.append(i)
            i[1][11] = True


# Created a function to make 1.1 legs of matchmaking priority
def pairing_1_1(sorted_player_list, i, x, tours, temp_score_1, temp_color_1):
    for j in range(len(sorted_player_list)+1):
        j += sorted_player_list.index(i) + 1
        if j == len(sorted_player_list):
            break

        temp_score_2 = sorted_player_list[j][1][3]  # possible opponent's score
        temp_color_2 = sorted_player_list[j][1][5]  # possible opponent's color
        if temp_color_1 == '':  # if the previous round is bye, temporary color assignment is made
            if tours > 1:
                temp_color_1 = i[1][7][tours - 2]
            else:
                temp_color_1 = opposite_color(temp_color_2)
        if temp_color_2 == '':  # if the previous round is bye, temporary color assignment is made
            if tours > 1:
                temp_color_2 = sorted_player_list[j][1][7][tours - 2]

        if sorted_player_list[j][0] not in i[1][10] and temp_score_1 == temp_score_2 \
                and len(x) != 2 and sorted_player_list[j][1][5] != '-' and not sorted_player_list[j][1][11]:
            if temp_color_1 == opposite_color(temp_color_2) or temp_color_2 == '' or temp_color_1 == '' and (
                    sorted_player_list[j][1][7].count(temp_color_1)
                    - sorted_player_list[j][1][7].count(opposite_color(temp_color_1))) < 2 \
                    and (i[1][7].count(opposite_color(temp_color_1)) - i[1][7].count(temp_color_1)) < 2:
                if i[1][5] == '':
                    i[1][5] = opposite_color(temp_color_1)
                else:
                    i[1][5] = opposite_color(i[1][5])
                i[1][7].append(i[1][5])
                sorted_player_list[j][1][5] = opposite_color(i[1][5])
                sorted_player_list[j][1][7].append(sorted_player_list[j][1][5])
                x.append(sorted_player_list[j])  # If all conditions are met, the opponent is added to the table next to the wanted player
                sorted_player_list[j][1][11] = True


# Created a function to make 1.2 legs of matchmaking priority
def pairing_1_2(sorted_player_list, i, x, tours, temp_score_1, temp_color_1):
    for j in range(len(sorted_player_list)):
        j += sorted_player_list.index(i) + 1
        if j == len(sorted_player_list):
            break

        temp_score_2 = sorted_player_list[j][1][3]  # possible opponent's score
        temp_color_2 = sorted_player_list[j][1][5]  # possible opponent's color
        if temp_color_1 == '':  # if the previous round is bye, temporary color assignment is made
            temp_color_1 = i[1][7][tours - 2]
        if temp_color_2 == '':  # if the previous round is bye, temporary color assignment is made
            temp_color_2 = sorted_player_list[j][1][7][tours - 2]

        if sorted_player_list[j][0] not in i[1][10] and temp_score_1 == temp_score_2 \
                and len(x) != 2 and sorted_player_list[j][1][5] != '-' and not sorted_player_list[j][1][11]:

            if temp_color_1 == temp_color_2 or temp_color_1 == '' and (
                    sorted_player_list[j][1][7].count(temp_color_1) -
                    sorted_player_list[j][1][7].count(
                        opposite_color(temp_color_1))) < 2 \
                    and (i[1][7].count(opposite_color(temp_color_1)) - i[1][7].count(temp_color_1)) < 2:
                if tours >= 2:
                    if (sorted_player_list[j][1][7][tours - 1] and
                            sorted_player_list[j][1][7][tours - 2] != sorted_player_list[j][1][5]):
                        if i[1][5] == '':
                            i[1][5] = opposite_color(temp_color_1)
                        else:
                            i[1][5] = opposite_color(i[1][5])
                        i[1][7].append(i[1][5])
                        sorted_player_list[j][1][5] = opposite_color(i[1][5])
                        sorted_player_list[j][1][7].append(sorted_player_list[j][1][5])
                        x.append(sorted_player_list[j])  # If all conditions are met, the opponent is added to the table next to the wanted player
                        sorted_player_list[j][1][11] = True
                else:
                    if i[1][5] == '':
                        i[1][5] = opposite_color(temp_color_1)
                    else:
                        i[1][5] = opposite_color(i[1][5])
                    i[1][7].append(i[1][5])
                    sorted_player_list[j][1][5] = opposite_color(i[1][5])
                    sorted_player_list[j][1][7].append(sorted_player_list[j][1][5])
                    x.append(sorted_player_list[j])  # If all conditions are met, the opponent is added to the table next to the wanted player
                    sorted_player_list[j][1][11] = True


# Created a function to make 1.3 legs of matchmaking priority
def pairing_1_3(sorted_player_list, i, x, tours, temp_score_1, temp_color_1):
    for j in range(len(sorted_player_list)):
        j += sorted_player_list.index(i) + 1
        if j == len(sorted_player_list):
            break

        temp_score_2 = sorted_player_list[j][1][3]  # possible opponent's score
        temp_color_2 = sorted_player_list[j][1][5]  # possible opponent's score
        if temp_color_1 == '':  # if the previous round is bye, temporary color assignment is made
            temp_color_1 = i[1][7][tours - 2]
        if temp_color_2 == '':  # if the previous round is bye, temporary color assignment is made
            if tours > 1:
                temp_color_2 = sorted_player_list[j][1][7][tours - 2]

        if sorted_player_list[j][0] not in i[1][10] and temp_score_1 == temp_score_2 \
                and len(x) != 2 and sorted_player_list[j][1][5] != '-' and not sorted_player_list[j][1][11]:

            if temp_color_1 == temp_color_2 or temp_color_2 == '' and (
                    sorted_player_list[j][1][7].count(opposite_color(temp_color_1)) -
                    sorted_player_list[j][1][7].count(temp_color_1)) < 2 \
                    and (i[1][7].count(temp_color_1) - i[1][7].count(opposite_color(temp_color_1))) < 2:
                if tours >= 2:
                    if i[1][7][tours - 1] and i[1][7][tours - 2] != i[1][5]:
                        i[1][7].append(i[1][5])

                        sorted_player_list[j][1][5] = opposite_color(i[1][5])
                        sorted_player_list[j][1][7].append(sorted_player_list[j][1][5])
                        x.append(sorted_player_list[j])  # If all conditions are met, the opponent is added to the table next to the wanted player
                        sorted_player_list[j][1][11] = True

                else:
                    i[1][7].append(i[1][5])

                    sorted_player_list[j][1][5] = opposite_color(i[1][5])
                    sorted_player_list[j][1][7].append(sorted_player_list[j][1][5])
                    x.append(sorted_player_list[j])  # If all conditions are met, the opponent is added to the table next to the wanted player
                    sorted_player_list[j][1][11] = True


def print_pairing_list(sorted_desks, tours):  # Created a function to print pairing list for each tour
    for i in sorted_desks:  # bye player desk goes to the end of high school
        if len(i) == 1:
            sorted_desks.pop(sorted_desks.index(i))
            sorted_desks.append(i)

    print("-------------------------------------------")
    print(str(tours + 1) + ". tour matchmaking list")
    print('  \t\tWhites\t\t\t\t\t', 'Blacks')
    print('DNo\tSRNo\tLNo\tScore\t-\tScore\tLNo\tSRNo')
    print('-' * 3, '-' * 4, '', '-' * 5, '-' * 5, '\t   ', '-' * 5, '-' * 5, '-' * 4)
    for i in range(len(sorted_desks)):
        if len(sorted_desks[i]) == 2:
            print(f'{i + 1:>3}', end=' ')
            print(f'{sorted_desks[i][0][1][4]:>4d}  {sorted_desks[i][0][0]:>5d} {sorted_desks[i][0][1][3]:>5.2f}'
                   f'\t\t{sorted_desks[i][1][1][3]:>5.2f} {sorted_desks[i][1][0]:>5d} {sorted_desks[i][1][1][4]:>4d}')
        else:
            print(f'{i + 1:>3}', end=' ')
            print(f'{sorted_desks[i][0][1][4]:>4d}  {sorted_desks[i][0][0]:>5d} {sorted_desks[i][0][1][3]:>5.2f}'
                   '\t\t', 'BYE')
            sorted_desks[i][0][1][3] += 1  # in order not to appear in the table, the bye player is assigned points here.
            sorted_desks[i][0][1][11] = False
            sorted_desks[i][0][1][5] = ''


def match_result(desks, tour):  # Created a function to compute match result
    for i in range(len(desks)):
        if len(desks[i]) == 2:
            result = get_digit_input("Enter the result of the match played on Table "
                                      + str(i + 1) + " in the " + str(tour + 1) + ". tour (0-5)")
            while result not in [0, 1, 2, 3, 4, 5]:
                result = get_digit_input("Enter the result of the match played on Table "
                                          + str(i + 1) + " in the " + str(tour + 1) + ". tour (0-5)")
            if result == 0:  # the match is drawn
                desks[i][0][1][3] += 0.5
                desks[i][0][1][9].append('½')
                desks[i][0][1][10].append(desks[i][1][0])
                desks[i][0][1][11] = False
                desks[i][0][1][16].append(desks[i][1][1][4])
                desks[i][1][1][3] += 0.5
                desks[i][1][1][9].append('½')
                desks[i][1][1][10].append(desks[i][0][0])
                desks[i][1][1][11] = False
                desks[i][1][1][16].append(desks[i][0][1][4])

            elif result == 1:  # white winner in the match
                desks[i][0][1][3] += 1
                desks[i][0][1][9].append('1')
                desks[i][0][1][10].append(desks[i][1][0])
                desks[i][0][1][11] = False
                desks[i][0][1][15] += 1  # [i][1][15] keeps player's win number value
                desks[i][0][1][16].append(desks[i][1][1][4])
                desks[i][1][1][9].append('0')
                desks[i][1][1][10].append(desks[i][0][0])
                desks[i][1][1][11] = False
                desks[i][1][1][16].append(desks[i][0][1][4])

            elif result == 2:  # black winner in the match
                desks[i][0][1][9].append('0')
                desks[i][0][1][10].append(desks[i][1][0])
                desks[i][0][1][11] = False
                desks[i][0][1][16].append(desks[i][1][1][4])
                desks[i][1][1][3] += 1
                desks[i][1][1][9].append('1')
                desks[i][1][1][10].append(desks[i][0][0])
                desks[i][1][1][11] = False
                desks[i][1][1][15] += 1
                desks[i][1][1][16].append(desks[i][0][1][4])

            elif result == 3:  # black did not come in the match
                desks[i][0][1][3] += 1
                desks[i][0][1][8] = True
                desks[i][0][1][9].append('+')
                desks[i][0][1][10].append(desks[i][1][0])
                desks[i][0][1][11] = False
                desks[i][0][1][15] += 1
                desks[i][0][1][16].append(desks[i][1][1][4])
                desks[i][1][1][9].append('-')
                desks[i][1][1][10].append(desks[i][0][0])
                desks[i][1][1][11] = False
                desks[i][1][1][16].append(desks[i][0][1][4])

            elif result == 4:  # black did not come in the match
                desks[i][0][1][9].append('-')
                desks[i][0][1][10].append(desks[i][1][0])
                desks[i][0][1][11] = False
                desks[i][0][1][16].append(desks[i][1][1][4])
                desks[i][1][1][3] += 1
                desks[i][1][1][8] = True
                desks[i][1][1][9].append('+')
                desks[i][1][1][10].append(desks[i][0][0])
                desks[i][1][1][11] = False
                desks[i][1][1][15] += 1
                desks[i][1][1][16].append(desks[i][0][1][4])

            else:  # neither player came to the match
                desks[i][0][1][9].append('-')
                desks[i][0][1][10].append(desks[i][1][0])
                desks[i][0][1][11] = False
                desks[i][0][1][16].append(desks[i][1][1][4])
                desks[i][1][1][9].append('-')
                desks[i][1][1][10].append(desks[i][0][0])
                desks[i][1][1][11] = False
                desks[i][1][1][16].append(desks[i][0][1][4])


def opposite_color(color):  # Created a function for getting opposite color
    if color == 'w':
        return 'b'
    else:
        return 'w'


def final_sorting(sorted_player_list):  # Created a function for make final sorting
    sorted_player_list = sorted(sorted_player_list, key=lambda player:
    (player[1][3], player[1][12], player[1][13], player[1][14], player[1][15],), reverse=True)
# [i][1][12] keeps player's buchholz-1 value
# [i][1][13] keeps player's buchholz-2 value
# [i][1][14] keeps player's sonneborn berger value

    return sorted_player_list


def print_final_ranking(sorted_player_list):  # Created a function for print final ranking table
    print("*******************************************************")
    print("Final Ranking List:")
    print("RNo SRNo   LNo  Name-Surname  ELO  UKD Score  BH-1  BH-2    SB GS")
    print("--- ---- ----- ------------- ---- ---- ----- ----- ----- ----- --")
    for player in sorted_player_list:
        print(format(player[1][6], "3"), end=" ")
        print(format(player[1][4], "4"), end=" ")
        print(format(player[0], "5"), end=" ")
        print(format(player[1][2], "13"), end=" ")
        print(format(player[1][0], "4"), end=" ")
        print(format(player[1][1], "4"), end="  ")
        print(format(player[1][3], "4.2f"), end=" ")
        print(format(player[1][12], "5.2f"), end=" ")
        print(format(player[1][13], "5.2f"), end=" ")
        print(format(player[1][14], "5.2f"), end=" ")
        print(format(player[1][15], "2"))


def print_cross_table(sorted_player_list, tour_num):  # Created a function for print cross table at the end
    print("********************************************************")
    print("Cross Table:")
    print("SRNo  RNo  LNo Name-Surname   ELO  UKD", end=" ")
    for tour in range(tour_num):
        print(" " + str(tour + 1) + ". Tour", end=" ")
    print(" Score  BH-1  BH-2    SB GS")
    print("----- --- ---- ------------- ---- ----", end=" ")
    for tour in range(tour_num):
        print("--------", end=" ")
    print(" ----- ----- ----- ----- --")
    for player in sorted_player_list:
        print(format(player[1][4], "3"), end=" ")
        print(format(player[1][6], "4"), end=" ")
        print(format(player[0], "4"), end=" ")
        print(format(player[1][2], "13"), end="  ")
        print(format(player[1][0], "4"), end=" ")
        print(format(player[1][1], "4"), end="  ")
        for tur in range(tour_num):
            print(format(player[1][16][tur], ">3"), end=" ")
            print(format(player[1][7][tur], "1"), end=" ")
            print(format(player[1][9][tur], "1"), end="  ")
        print(format(player[1][3], "5.2f"), end=" ")
        print(format(player[1][12], "5.2f"), end=" ")
        print(format(player[1][13], "5.2f"), end=" ")
        print(format(player[1][14], "5.2f"), end=" ")
        print(format(player[1][15], "2"))


def tiebreak(sorted_player_list):  # created function to break the tie in the final ranking
    for i in range(len(sorted_player_list)):
        bh_1 = 0  # temporary buchholz value
        sb = 0  # temporary sonneborn berger value
        opp_score_list = []  # Stores opponent player scores
        bye_or_non_played_lno = []  # Stores the bye or lno of non-playing players each round(list)
        for m in range(len(sorted_player_list[i][1][9])):
            bye_or_non_played_score = 0
            if sorted_player_list[i][1][9][m] in ['+', '-'] or sorted_player_list[i][1][10][m] == '-':
                for j in range(m):
                    if sorted_player_list[i][1][9][j] == '1':
                        bh_1 += 1
                        bye_or_non_played_score += 1
                    elif sorted_player_list[i][1][9][j] == '½':
                        bh_1 += 0.5
                        bye_or_non_played_score += 0.5
                bh_1 += (len(sorted_player_list[i][1][9]) - (m + 1)) * 0.5
                bye_or_non_played_score += (len(sorted_player_list[i][1][9]) - (m + 1)) * 0.5
            else:
                for j in sorted_player_list:
                    if sorted_player_list[i][1][10][m] == j[0]:
                        bh_1 += j[1][3]
            if bye_or_non_played_score > 0:
                opp_score_list.append(bye_or_non_played_score)
                bye_or_non_played_lno.append(sorted_player_list[i][1][10][m])

            for k in sorted_player_list:
                if k[0] == sorted_player_list[i][1][10][m] and k[0] not in bye_or_non_played_lno:
                    opp_score_list.append(k[1][3])

            if sorted_player_list[i][1][9][m] in ['+', '1', '½']:
                if sorted_player_list[i][1][9][m] == '½':
                    sb += opp_score_list[m] * 0.5
                else:
                    sb += opp_score_list[m]

        bh_1 -= min(opp_score_list)
        bh_2 = bh_1
        opp_score_list.remove(min(opp_score_list))
        bh_2 -= min(opp_score_list)
        sorted_player_list[i][1][12] = bh_1
        sorted_player_list[i][1][13] = bh_2
        sorted_player_list[i][1][14] = sb


main()  # Called main function
