import tkinter as tk
from tkinter import simpledialog
from main_screen import *

ROOT = tk.Tk()


def get_username():
    ROOT.withdraw()
    return simpledialog.askstring(title="Username",
                                  prompt="What is your username?")


game_over_font = pygame.font.Font(None, 96)
leaderboard_font = pygame.font.Font(None, 32)

# Set the clock for controlling the frame rate
clock = pygame.time.Clock()


# Create a function to draw the "Game Over" text on the screen
def draw_game_over():
    text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (400, 300)
    screen.blit(text, text_rect)
    pygame.display.flip()


scores = []


def get_score():
    try:
        leaderboard = open("leaderboard.csv", "r")
        leaderboardscores = leaderboard.read()
        # Divide the lines into tuples
        leaderboardscores = leaderboardscores.splitlines()
        # Split the tuples into two values, the name and the score
        leaderboardscores = [tuple(line.split(",")) for line in leaderboardscores]
        # Make the score an integer
        leaderboardscores = [(name, int(score)) for name, score in leaderboardscores]
        # Append each pair of tuples to scores
        for line in leaderboardscores:
            scores.append(line)
        leaderboard.close()
    except IOError:
        # Error reading file, no high score
        print("There is no high score yet.")
    except ValueError:
        # There's a file there, but we don't understand the number.
        print("I'm confused. Starting with no high score.")


def save_high_score(new_high_score):
    try:
        leaderboard = open("leaderboard.csv", "a")
        # Write the new high score to the file into a new line without erasing the old ones
        leaderboard.write("\n")
        leaderboard.write(new_high_score)
        leaderboard.close()
    except IOError:
        # Hm, can't write it.
        print("Unable to save the high score.")


# Draw the leaderboard on the screen
def draw_leaderboard():
    # Sort the scores from highest to lowest
    scores.sort(key=lambda x: x[1], reverse=True)
    # Draw the leaderboard title
    text = leaderboard_font.render("LEADERBOARD", True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.center = (400, 100)
    screen.blit(text, text_rect)
    # Draw only the top 10 scores with their names
    for i in range(10):
        try:
            text = leaderboard_font.render(f"{i + 1}. {scores[i][0]}: {scores[i][1]}", True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.center = (400, 150 + i * 30)
            # The text starts 10 pixels below the leaderboard title
            text_rect.y += 10

            screen.blit(text, text_rect)
        except IndexError:
            # There are less than 10 scores
            pass

    pygame.display.flip()
