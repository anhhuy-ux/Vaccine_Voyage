import random
from databaseconnection import connection
import functions_game
from functions_game import insert_data_disease_table
from functions_game import multiple_choice
from functions_game import insert_session

list_first_countries = ["Finland", "Cambodia", "Canada", "Peru", "Croatia", "South Africa", "Dubai"]
first_country = random.choice(list_first_countries)


game_rules = ("On Vaccine Voyage you are a researcher trying to find ingredients for a vaccine "
              "before the whole world is infected. You will do that by travelling around the world "
              "to find those ingredients. First name the disease you want to treat, then use the "
              "trivia tips to rightly guess the country where the ingredients are. You will start "
              "with 300 points, every mistake and new hint you ask will be debited from points. "
              "Good luck! We'll start now! Let's save the world together!\n")

print(game_rules)

print(f"The first infected country is {first_country}.\n")

disease_name = input("What disease are you going to treat? \n")

print(f"Now we start our journey to fight {disease_name}...\n")

points = 300
guess_count = 1
guess = ""


#randomize 7 countries, and assign 7 variables accordingly
from functions_game import ingredient_country
final_country_list = ingredient_country()


#for loop that will loop for 7 times, representing 7 levels

from functions_game import retrieve_hints

from functions_game import point_per_level

game_movement = ""
countries_guessed = []
game_over = "No"

for game_level in range(0,7):
        #generate randomly 6 hints for the country for the current level
        #enter into the function: the country after being randomly picked and game level
        #example: in the 1st level final_country_list[0] - which is the 1st country, and enter into the current level parameter as 1 (0+1),
        #print(game_level)
        #print(final_country_list[game_level])



    print(final_country_list[game_level])
    right_answer = final_country_list[game_level]
    current_level = game_level + 1
    hint_list = retrieve_hints(final_country_list[game_level], current_level)
    #print(hint_list)
    print('Level',current_level)


    for hint_number in range(0,6):
        print('Your current points:', points)
        print(hint_list[hint_number])
        level_status = ""
        game_movement = input("What do you want to do: guess, new hint or quit?\n").upper()
        while game_movement not in ["QUIT", "GUESS", "NEW HINT"]:
            game_movement = input("What do you want to do: guess, new hint or quit?\n").upper()
            print('\n')
        #if commands to decide if they want to guess, new hint or quit; they said guess, then provide with a hint
        if game_movement == "GUESS":
            guess = input(f"This ingredient is in: ").upper()
            while guess != right_answer:
                if points >= 0:
                    if hint_number < 5:
                        points = points - int(point_per_level(current_level))
                        guess_count += 1
                        print('Your guess was wrong, please view the next hint and try again')
                        print('Your current points:', points)
                        print('\n')
                        break
                    else:
                        points = points - int(point_per_level(current_level)) * 1.5
                        multiple_choice(final_country_list[game_level])
                        print('Your current points:', points)
                        guess = input(f"This ingredient is in: \n").upper()
                else:
                    game_over = "Yes"
                    break
        elif game_movement == "NEW HINT":
            if guess_count < 6:
                guess_count += 1
                points = points - int(point_per_level(current_level))

            else:
                print('You have used up all hints of this level, please pick your guess!')
                points = points - int(point_per_level(current_level)) * 2
                print('Your current points:', points)
                multiple_choice(right_answer)
                while guess != right_answer:
                    guess = input(f"This ingredient is in: ").upper()
                    print('\n')
        elif game_movement == "QUIT":
            game_over = "Yes"
            print('Sorry to see you go. Come back soon!')
            print(f'Your current record is {points} points, you have guess {countries_guessed})
            print('\n')
            break
        while guess != right_answer:
            level_status = ""
            if points >= 0:
                if hint_number < 6:
                    points = points - int(point_per_level(current_level))
                    guess_count += 1
                    print('Your guess was wrong, please view the next hint and try again')
                    print('Your current points:', points)
                    print('\n')
                    break
                else:
                    points = points - int(point_per_level(current_level)) * 1.5
                    multiple_choice(final_country_list[game_level])
                    print('Your current points:', points)
                    guess = input(f"This ingredient is in: \n").upper()
            else:
                game_over = "Yes"
                break
        if guess == right_answer:
            if current_level < 7:
                print(f"Congratulations! You have found ingredient number {current_level}, let's move on!\n")
            else:
                countries_guessed.append(right_answer)
                level_status = "success"
            if guess_count == 1:
                points = points + int(point_per_level(current_level))
                print('Thanks to your quick thinking, you got some extra points. Your current points:', points)
                print('\n')
            else:
                guess_count = 1
            break
        if (game_over == "Yes" or level_status == "success"):
            break
    if game_over == "Yes":
        break
#add the game session into database
insert_session(disease_name,right_answer,current_level)
print('Your game has been saved')

if game_movement != "QUIT" :
    if points > 0:
        print(f'Congratulation, you have found all ingredients with {points} points left.')
    else:
        print('GAME OVER - You failed to find all ingredients within the points given.\n')
else:
    print()
#need to improve the finishing lines
decision = input('Do you want to retry or quit?').upper()
if decision == "RETRY":
    game_over = "No"
    points = 300
    guess_count = 1
elif decision == "QUIT":
    print("Thank you for playing! You're welcomed to try again")










