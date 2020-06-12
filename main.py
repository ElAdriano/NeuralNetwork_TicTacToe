from tic_tac_toe_models import NeuralNetwork, Trainer, TicTacToe
import numpy as np

trainer = Trainer()

network1 = NeuralNetwork(9, 84, 60, 3)
network2 = NeuralNetwork(9, 84, 60, 3)

trainer.learn_networks(network1, network2)

def prepare_efficiency_statistics(network1, network2, games_played):
    network_1_wins = 0 # for network1
    network_2_wins = 0 # for network2
    draws = 0

    print("Data for statics generation started...")
    game = TicTacToe()
    for i in range(0, games_played):
        winner = game.game_network_against_network(network1, network2)
        if winner == 1:
            network_1_wins += 1
        elif winner == 0:
            draws += 1
        else:
            network_2_wins += 1

    networks = [network1, network2]
    overall_data = []
    for n in range(0, len(networks)):
        network = networks[n]
        network_wins = 0
        random_wins = 0
        draws = 0
        for i in range(0, games_played):
            winner = game.game_network_against_random(network)
            if winner == 1:
                network_wins += 1
            elif winner == 0:
                draws += 1
            else:
                random_wins += 1
        dictionary = {
            "network_wins": network_wins,
            "random_wins": random_wins,
            "draws": draws,
            "network_id": n + 1   
        }
        overall_data.append(dictionary)
    print("Data generation completed...")
    # show final statistics
    print("=============== STATISTICS FOR GAMES BETWEEN 2 NEURAL NETWORKS ===============")
    print("\t     Network 1 won at "+ str( 100 * network_1_wins / (network_1_wins + network_2_wins + draws) ) + "%" + " of all attempts.")
    print("\t     Network 2 won at "+ str( 100 * network_2_wins / (network_1_wins + network_2_wins + draws) ) + "%" + " of all attempts.")
    print("\tDraws were reached at "+ str( 100 * draws / (network_1_wins + network_2_wins + draws) ) + "%" + " of all attempts.")

    for element in overall_data:
        network_wins = element["network_wins"]
        random_wins = element["random_wins"]
        draws = element["draws"]
        n = element["network_id"]
        print("\n")
        print("============ STATISTICS FOR NETWORK {} ============".format(n))
        print("\t    Network {} won at ".format(n) + str(100 * network_wins / (network_wins + random_wins + draws)) + "%" + " of all attempts.")
        print("\t        Random won at " + str(100 * random_wins / (network_wins + random_wins + draws)) + "%" + " of all attempts.")
        print("\tDraws were reached at " + str(100 * draws / (network_wins + random_wins + draws)) + "%" + " of all attempts.")

def play_game_with_neural_network(network):
    wanna_play_again = True
    tictactoe = TicTacToe()

    while wanna_play_again:
        tictactoe.play_against_network(network)
        answer = input("Do you want to play TicTacToe again? Enter Y or N: ").capitalize()
        if answer == 'Y':
            wanna_play_again = True
        else:
            wanna_play_again = False

prepare_efficiency_statistics(network1, network2, 5000)

answer = input("Do you want to play with TicTacToe against neural network? Enter Y or N: ").capitalize()
if answer == "Y":
    play_game_with_neural_network(network1)
