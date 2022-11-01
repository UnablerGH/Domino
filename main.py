
from random import shuffle
from itertools import combinations_with_replacement
# define turn function


def turn_func(func_input, func_pieces):
    # stop if there is no pieces
    if int(func_input) == 0 and len(stock_pieces) == 0:
        return None
    # give piece to player
    elif int(func_input) == 0 and len(stock_pieces) > 0:
        func_pieces.append(stock_pieces[-1])
        stock_pieces.remove(stock_pieces[-1])
        return None
    # place piece right after snake
    if int(func_input) > 0:
        # get piece from player or computer
        piece_to_end = func_pieces[int(func_input) - 1]
        # reverse piece
        if piece_to_end[1] == snake[-1][-1]:
            piece_to_end.reverse()
        # place piece
        snake.append(piece_to_end)
        # remove piece from player or computer
        func_pieces.remove(func_pieces[int(func_input) - 1])
    # place piece left after snake
    else:
        # get piece from player or computer
        piece_to_start = func_pieces[-int(func_input) - 1]
        # reverse piece
        if piece_to_start[0] == snake[0][0]:
            piece_to_start.reverse()
        # place piece
        snake.insert(0, piece_to_start)
        # remove piece from player or computer
        func_pieces.remove(func_pieces[-int(func_input) - 1])
# Check if this snake is winning


def win_snake(func_snake):
    if func_snake[0][0] == func_snake[-1][-1] and sum(x.count(func_snake[0][0]) for x in func_snake) == 8:
        return True


# define list of dominoes
dominoes = list(combinations_with_replacement(range(0, 7), 2))
# convert list of tuples to list of lists
dominoes = [list(x) for x in dominoes]
# shuffle dominoes
shuffle(dominoes)
# define coefficient equal to half of the number of dominoes
coefficient = len(dominoes) // 2
# get first half of the dominoes
stock_pieces = dominoes[:coefficient]
# get computer's and player's pieces
computer_pieces = dominoes[coefficient:int(coefficient * 1.5)]
player_pieces = dominoes[int(coefficient * 1.5):]
# find snake
snake = [max([[x, y] for x, y in computer_pieces + player_pieces if x == y])]
# remove snake from computer's or player's pieces
computer_pieces.remove(snake[0]) if snake[0] in computer_pieces else player_pieces.remove(snake[0])
# define massages for player
player_turn = "It's your turn to make a move. Enter your command."
computer_turn = "Computer is about to make a move. Press Enter to continue..."
player_won = 'The game is over. You won!'
computer_won = 'The game is over. The computer won!'
# define who is first
turn_num = 0 if len(player_pieces) > len(computer_pieces) else 1
# start game
while True:
    # show stock, player's and computer's pieces
    print('=' * 70)
    print('Stock size:', len(stock_pieces))
    print('Computer pieces:', len(computer_pieces), '\n')
    print(*snake, '\n', sep='') if len(snake) <= 6 else print(*snake[:3], '...', *snake[-3:], '\n', sep='')
    print("Your pieces:")
    for num, piece in enumerate(player_pieces):
        print(f"{num + 1}: {piece}")
    # condition for player's win if there is no pieces
    if len(player_pieces) == 0:
        print("\nStatus:", player_won)
        break
    # condition for computer's win if there is no pieces
    if len(computer_pieces) == 0:
        print("\nStatus:", computer_won)
        break
    # condition for player's win if snake is winning
    if win_snake(snake) and turn_num == 0:
        print("\nStatus:", player_won)
        break
    # condition for computer's win if snake is winning
    if win_snake(snake) and turn_num == 1:
        print("\nStatus:", computer_won)
        break
    # define snake ends
    connection_keys = [snake[0][0], snake[-1][-1]]
    # condition for draw
    if len(stock_pieces) == 0 and \
            any([verb[1] for verb in player_pieces + computer_pieces if verb[0] in connection_keys]):
        print("\nStatus: The game is over. It's a draw!")
        break
    # player's turn
    if turn_num % 2 == 0:
        # count turn number
        turn_num += 1
        # show message
        print("\nStatus:", player_turn)
        # get player's input
        user_input = input()
        # check if player's input is valid
        if user_input.lstrip("-").isdigit() and int(user_input) in range(-len(player_pieces), len(player_pieces) + 1):
            # provide piece to player
            if int(user_input) == 0:
                turn_func(user_input, player_pieces)
                continue
            # define current piece
            current_piece = player_pieces[int(user_input) - 1] if int(user_input) > 0 \
                else player_pieces[-int(user_input) - 1]
            # check if piece is valid
            if connection_keys[-1] in current_piece and int(user_input) > 0 or \
                    connection_keys[0] in current_piece and int(user_input) < 0:
                turn_func(user_input, player_pieces)
            else:
                print("Illegal move. Please try again.")
                turn_num -= 1
                continue
        else:
            print("Invalid input. Please try again.")
            turn_num -= 1
            continue
    # computer's turn
    else:
        # count turn number
        turn_num += 1
        # show message
        print("\nStatus:", computer_turn)
        # wait for player's input
        input()

        # counting numbers in hand and on the table

        count = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for element in computer_pieces + snake:
            for i in range(2):
                match element[i]:
                    case 0:
                        count[0] += 1
                    case 1:
                        count[1] += 1
                    case 2:
                        count[2] += 1
                    case 3:
                        count[3] += 1
                    case 4:
                        count[4] += 1
                    case 5:
                        count[5] += 1
                    case 6:
                        count[6] += 1

        # defining score:

        scores = []

        for element in computer_pieces:
            scores.append(count[element[0]] + count[element[1]])

        # make computer's move

        while True:
            try:
                max_value = max(scores)
            except ValueError:
                turn_func('0', computer_pieces)
                break

            max_index = scores.index(max_value) + 1
            if computer_pieces[max_index][0] == connection_keys[-1]:
                turn_func(str(max_index), computer_pieces)
                break
            elif computer_pieces[max_index][1] == connection_keys[0]:
                turn_func(str(-max_index), computer_pieces)
                break
            scores.remove(max_value)
