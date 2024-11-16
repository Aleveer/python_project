def save_leaderboard(leaderboard):
    with open('leaderboard.txt', 'w') as f:
        for name, score in leaderboard:
            f.write(f"{name} {score}\n")


def load_leaderboard(leaderboard):
    try:
        with open("leaderboard.txt", "r") as f:
            for line in f:
                name, score = line.strip().split(" ")
                leaderboard.append((name, int(score)))
            leaderboard.sort(key=lambda x: x[1], reverse=True)
            print(leaderboard)
    except FileNotFoundError:
        print("File leaderboard.txt not found.")


leaderboard = [('Alice', 100), ('Bob', 200), ('Charlie', 300)]
save_leaderboard(leaderboard)
load_leaderboard(leaderboard)