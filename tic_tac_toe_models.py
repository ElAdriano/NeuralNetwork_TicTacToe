from keras.models import Sequential
from keras.layers import Dense
import keras
import numpy as np
import random

class NeuralNetwork:
    model = None

    def __init__(self, input_neurons, hidden_neurons1, hidden_neurons2, output_neurons):
        self.model = Sequential()
        self.model.add( Dense(hidden_neurons1, activation='sigmoid', input_shape=(input_neurons,)) )
        self.model.add( Dense(hidden_neurons2, activation='relu') )
        self.model.add( Dense(output_neurons, activation='softmax') )
        self.model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['accuracy'])

    def predict(self, input_data):
        return self.model.predict(input_data)

class Trainer:
    training_set = None

    def __init__(self):
        self.training_set = []
    
    def learn_networks(self, network1, network2):
        tictactoe = TicTacToe()
        self.training_set = tictactoe.generate_random_games()
        prepared_dataset = self.__prepare_data()
        learning_input_values = prepared_dataset["learning_input_data"]
        learning_output_values = prepared_dataset["learning_output_data"]
        test_input_values = prepared_dataset["test_input_data"]
        test_output_values = prepared_dataset["test_output_data"]

        network1.model.fit(learning_input_values, learning_output_values, epochs=150, validation_data=(test_input_values, test_output_values))
        network2.model.fit(learning_input_values, learning_output_values, epochs=150, validation_data=(test_input_values, test_output_values))
            
    def __prepare_data(self):
        input_values = []
        output_values = []
        
        for i in range(0, len(self.training_set)-1):
            input_values.append(self.training_set[i][0])
            output_values.append(self.training_set[i][1])
        input_values = np.array(input_values).reshape((-1,9))
        output_values = np.eye(3)[output_values]

        divider = int(0.78 * len(input_values))

        divided_data = {
            "learning_input_data": input_values[0:divider],
            "learning_output_data": output_values[0:divider],
            "test_input_data": input_values[divider:-1],
            "test_output_data": output_values[divider:-1]
        }
        return divided_data

class TicTacToe:
    '''
        1   - X
        0   - empty field
        -1  - O
    '''

    grid = []

    def __init__(self):
        self.grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
    
    def generate_random_games(self):
        training_set = []
        for i in range(0, 70000):
            self.grid = [[0,0,0],[0,0,0],[0,0,0]]
            turn_counter = 0
            current_player = 1
            states = []
            game_status = self.__check_game_status()

            while game_status[0] and turn_counter < 9:
                turn_counter += 1
                moves = self.__calculate_moves()

                move = moves[random.randint(0, len(moves)-1)]
                self.grid[move[0]][move[1]] = current_player
                
                current_player *= (-1)
                game_status = self.__check_game_status()
                copy = self.__copy_grid()
                states.append( [copy, game_status[1]] )

            for state in states:
                state[1] = game_status[1]

            for result in states:
                training_set.append(result)
        return training_set

    def game_network_against_network(self, network1, network2):
        self.grid = [[0,0,0],[0,0,0],[0,0,0]]
        current_player = 1 if random.randint(0,1) == 1 else -1
        turn_counter = 0
        game_status = self.__check_game_status()
        ai_1 = 1
        ai_2 = -1

        while game_status[0] and turn_counter < 9:
            turn_counter += 1
            moves = self.__calculate_moves()

            if current_player == ai_1:
                move = self.__make_ai_move(moves, network1, ai_1)
                self.grid[move[0]][move[1]] = ai_1
            else:
                move = self.__make_ai_move(moves, network2, ai_2)
                self.grid[move[0]][move[1]] = ai_2
            
            current_player *= (-1)
            game_status = self.__check_game_status()
        
        return game_status[1]
    
    def game_network_against_random(self, network):
        self.grid = [[0,0,0],[0,0,0],[0,0,0]]
        current_player = 1 if random.randint(0,1) == 1 else -1
        turn_counter = 0
        game_status = self.__check_game_status()
        ai = 1
        random_sign = -1

        while game_status[0] and turn_counter < 9:
            turn_counter += 1
            moves = self.__calculate_moves()

            if current_player == ai:
                move = self.__make_ai_move(moves, network, ai)
                self.grid[move[0]][move[1]] = ai
            else:
                move = moves[random.randint(0, len(moves)-1)]
                self.grid[move[0]][move[1]] = random_sign
            
            current_player *= (-1)
            game_status = self.__check_game_status()
        
        return game_status[1]

    def play_against_network(self, network):
        self.grid = [[0,0,0],[0,0,0],[0,0,0]]
        turn_counter = 0

        my_sign = 1
        ai_sign = -1
        current_player = 1 if random.randint(0,1) == 1 else -1
        game_status = self.__check_game_status()
        while game_status[0] and turn_counter < 9:
            self.__show_grid()
            turn_counter += 1

            if current_player == my_sign:
                coordinates = self.__get_input_from_player()
                self.grid[coordinates[0]][coordinates[1]] = my_sign
            else:
                moves = self.__calculate_moves()
                move = self.__make_ai_move(moves, network, ai_sign)
                self.grid[move[0]][move[1]] = ai_sign

            current_player *= (-1)
            game_status = self.__check_game_status()

        self.__show_grid()
        self.__show_result(game_status[1], ai_sign)

    def __show_result(self, winner, ai_sign):
        if winner == ai_sign:
            print("Sorry, NeuralNetwork won")
        elif winner == 0:
            print("It's a draw")
        else:
            print("Nice, you won")

    def __show_grid(self):
        print("\n\n\n\n\n\n\n")
        for i in range(0,3):
            sign1 = self.__get_sign(i, 0)
            sign2 = self.__get_sign(i, 1)
            sign3 = self.__get_sign(i, 2)
            print(" {} | {} | {} ".format(sign1, sign2, sign3))
            if i != 2:
                print("-----------")
    
    def __get_sign(self, x, y):
        number = self.grid[x][y]
        if number == 1:
            return 'X'
        elif number == 0:
            return ' '
        else:
            return 'O'

    def __make_ai_move(self, moves, network, ai_sign):
        max_value = 0
        final_move = moves[0]
        for move in moves:
            copy = self.__copy_grid()
            copy[move[0]][move[1]] = ai_sign
            
            values_vector = network.predict(np.array(copy).reshape(-1, 9))
            current_move_value = max(values_vector[0][0], values_vector[0][1 if ai_sign == 1 else 2])
            if current_move_value > max_value:
                final_move = move
                max_value = current_move_value

        return final_move

    def __get_input_from_player(self):
        coordinate_x = input("Enter coordinates x of field to mark: ")
        coordinate_y = input("Enter coordinate y of field to mark: ")
        correct_input = self.__validate_input([coordinate_x, coordinate_y])
        
        while correct_input != 0:
            if correct_input == 2:
                print("Incorrect field coordinates entered. Please enter correct one.\n")
            elif correct_input == -1:
                print("I'm sorry, that field is actually marked. Please choose another one.\n")
            
            coordinate_x = input("Enter coordinates x of field to mark: ")
            coordinate_y = input("Enter coordinate y of field to mark: ")
            correct_input = self.__validate_input([coordinate_x, coordinate_y])
        
        return [int(coordinate_x) - 1, int(coordinate_y) - 1]
    
    def __validate_input(self, given_input):
        x = given_input[0]
        y = given_input[1]
        if len(x) != 1 or len(y) != 1:
            return 2

        if ord(x) < 49 or ord(x) > 51 or ord(y) < 49 or ord(y) > 51:
            return 2
        x = int(x)
        y = int(y)

        if self.grid[x - 1][y - 1] != 0:
            return -1
        return 0

    def __check_game_status(self):
        # checking all rows and columns whether game ended or not 
        row_sums = np.sum(self.grid, axis=1)
        columns_sums = np.sum(self.grid, axis=0)
        
        # checking diagonal win
        d1_sum = self.grid[0][0] + self.grid[1][1] + self.grid[2][2]
        d2_sum = self.grid[2][0] + self.grid[1][1] + self.grid[0][2]

        if (-3) in row_sums or (-3) in columns_sums or (-3) == d1_sum or (-3) == d2_sum:
            return (False, -1)
        if 3 in row_sums or 3 in columns_sums or 3 == d1_sum or 3 == d2_sum:
            return (False, 1)
        return (True, 0)

    def __calculate_moves(self):
        calculated_moves = []
        for i in range(0,3):
            for j in range(0,3):
                if self.grid[i][j] == 0:
                    calculated_moves.append((i,j))
        return calculated_moves

    def __copy_grid(self):
        copy = []
        for i in range(0,3):
            row = []
            for j in range(0,3):
                row.append(self.grid[i][j])
            copy.append(row)
        return copy