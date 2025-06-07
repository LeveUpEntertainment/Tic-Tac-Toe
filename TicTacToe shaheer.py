import pygame
import sys
import random

pygame.init()

# Screen setup
screen_width, screen_height = 300, 360
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('TicTacToe')

# Define colors
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
gray = (200, 200, 200)
black = (0, 0, 0)
light_gray = (220, 220, 220)

# Fonts
font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 36)

# Game variables
line_width = 6
clicked = False
player = 1
winner = 0
game_over = False
show_play_again = False
tie = False

# Grid
markers = [[0 for _ in range(3)] for _ in range(3)]
cell_size = 100

# Button
play_again_rect = pygame.Rect(90, 310, 120, 40)

# Draw the grid
def draw_grid():
    for x in range(1, 3):
        pygame.draw.line(screen, black, (0, x * cell_size), (screen_width, x * cell_size), line_width)
        pygame.draw.line(screen, black, (x * cell_size, 0), (x * cell_size, screen_height - 60), line_width)

# Draw better-looking markers
def draw_markers():
    for row in range(3):
        for col in range(3):
            center_x = col * cell_size + cell_size // 2
            center_y = row * cell_size + cell_size // 2
            if markers[row][col] == 1:
                pygame.draw.line(screen, red,
                                 (center_x - 30, center_y - 30),
                                 (center_x + 30, center_y + 30), 8)
                pygame.draw.line(screen, red,
                                 (center_x + 30, center_y - 30),
                                 (center_x - 30, center_y + 30), 8)
            elif markers[row][col] == 2:
                pygame.draw.circle(screen, blue,
                                   (center_x, center_y), 38, 8)

# Check for winner or tie
def check_game_over():
    global winner, game_over, tie
    for row in range(3):
        if markers[row][0] == markers[row][1] == markers[row][2] != 0:
            winner = markers[row][0]
            game_over = True
            return
    for col in range(3):
        if markers[0][col] == markers[1][col] == markers[2][col] != 0:
            winner = markers[0][col]
            game_over = True
            return
    if markers[0][0] == markers[1][1] == markers[2][2] != 0:
        winner = markers[0][0]
        game_over = True
        return
    if markers[0][2] == markers[1][1] == markers[2][0] != 0:
        winner = markers[0][2]
        game_over = True
        return
    # Check for tie
    filled = all(cell != 0 for row in markers for cell in row)
    if filled and not winner:
        tie = True
        game_over = True

# Explosion animation
def explosion_effect():
    for _ in range(15):
        for _ in range(8):
            radius = random.randint(5, 25)
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height - 60)
            color = random.choice([red, green, blue, white])
            pygame.draw.circle(screen, color, (x, y), radius)
        pygame.display.update()
        pygame.time.delay(60)

# Draw play again button
def draw_play_again_button():
    pygame.draw.rect(screen, light_gray, play_again_rect)
    pygame.draw.rect(screen, black, play_again_rect, 2)
    text = font.render("Play Again", True, black)
    screen.blit(text, (play_again_rect.x + 15, play_again_rect.y + 10))

# Reset the board
def reset_game():
    global markers, player, winner, game_over, show_play_again, tie
    markers = [[0 for _ in range(3)] for _ in range(3)]
    player = 1
    winner = 0
    game_over = False
    show_play_again = False
    tie = False

# Main game loop
run = True
exploded = False
while run:
    screen.fill(gray)
    draw_grid()
    draw_markers()

    if not game_over:
        text = font.render(f"Player {player}'s Turn", True, black)
        screen.blit(text, (10, 310))
    else:
        if not exploded and not tie:
            explosion_effect()
            exploded = True
            show_play_again = True
        if winner:
            win_text = large_font.render(f"Player {winner} Wins!", True, black)
            screen.blit(win_text, (70, 310))
        elif tie:
            tie_text = large_font.render("It's a Tie!", True, black)
            screen.blit(tie_text, (90, 310))
            show_play_again = True
        if show_play_again:
            draw_play_again_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if not game_over and my < 300:
                row = my // cell_size
                col = mx // cell_size
                if markers[row][col] == 0:
                    markers[row][col] = player
                    player = 2 if player == 1 else 1
                    check_game_over()
                    if game_over:
                        exploded = False  # trigger explosion or tie handling next frame

            if show_play_again and play_again_rect.collidepoint((mx, my)):
                reset_game()

    pygame.display.update()

pygame.quit()
sys.exit()

