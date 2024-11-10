import logics

mat = logics.initialize()
for i in range(4):
    print(mat[i])

while True:

    user_input = input("Enter your command/move ")

    match user_input.lower():
        case "w":
            mat, change = logics.move_up(mat)
            status = logics.check_game_state(mat)
            print(status)

            if status == "Continue":
                logics.add_new_value(mat)
            else:
                break
        case "s":
            mat, change = logics.move_down(mat)
            status = logics.check_game_state(mat)
            print(status)

            if status == "Continue":
                logics.add_new_value(mat)
            else:
                break
        case "d":
            mat, change = logics.move_right(mat)
            status = logics.check_game_state(mat)
            print(status)

            if status == "Continue":
                logics.add_new_value(mat)
            else:
                break
        case "a":
            mat, change = logics.move_left(mat)
            status = logics.check_game_state(mat)
            print(status)

            if status == "Continue":
                logics.add_new_value(mat)
            else:
                break
        case "q":
            print("Thanks for playing")
            break
        case _:
            print("Please enter correct keyword")

    for i in range(4):
        print(mat[i])