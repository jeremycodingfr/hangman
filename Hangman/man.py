import pygame
import math
import random

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# Button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 500
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# Fonts
LETTER_FONT = pygame.font.SysFont('Lora', 40)
WORD_FONT = pygame.font.SysFont('Lora', 60)
TITLE_FONT = pygame.font.SysFont('Lora', 70)
HINT_FONT = pygame.font.SysFont('Lora', 30)

# Load images
images = [pygame.image.load(f"hangman{i}.png") for i in range(7)]

# Game variables
word_hints = {
    "PYTHON": "A popular programming language",
    "DEVELOPER": "A person who writes code",
    "GAME": "An interactive form of entertainment",
    "CODING": "The process of writing computer programs",
}

def reset_game():
    global word, hint, guessed, hangman_status, reset_count, score
    word = random.choice(list(word_hints.keys())).upper()
    hint = word_hints[word]
    guessed = []
    hangman_status = 0
    for letter in letters:
        letter[3] = True

def show_hint():
    pygame.draw.rect(win, (255, 255, 255), (100, 350, 600, 100))
    pygame.draw.rect(win, (50, 150, 255), (100, 350, 600, 100), 3)
    hint_text = HINT_FONT.render(f"Hint: {hint}", True, (255, 0, 0))
    win.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, 380))
    pygame.display.update()
    pygame.time.delay(2000)
    draw()

word = random.choice(list(word_hints.keys())).upper()
hint = word_hints[word]
guessed = []
hangman_status = 0
reset_count = 3
score = 0

# Draw function
def draw():
    win.fill((255, 255, 255))
    title_text = TITLE_FONT.render("Hangman", True, (50, 150, 255))
    win.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))
    display_word = " ".join([letter if letter in guessed else "_" for letter in word])
    word_text = WORD_FONT.render(display_word, True, (0, 0, 0))
    win.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, 300))
    score_text = HINT_FONT.render(f"Score: {score}", True, (0, 0, 0))
    win.blit(score_text, (20, 20))
    
    for x, y, ltr, visible in letters:
        if visible:
            pygame.draw.circle(win, (50, 150, 255), (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, True, (0, 0, 0))
            win.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
    
    pygame.draw.rect(win, (50, 150, 255), (WIDTH // 2 - 60, 600, 120, 40), 2)
    hint_text = HINT_FONT.render("Hint", True, (0, 0, 0))
    win.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, 610))
    
    pygame.draw.rect(win, (50, 150, 255), (WIDTH // 2 - 60, 650, 120, 40), 2)
    reset_text = HINT_FONT.render(f"Reset ({reset_count})", True, (0, 0, 0))
    win.blit(reset_text, (WIDTH // 2 - reset_text.get_width() // 2, 660))
    
    win.blit(images[min(hangman_status, 6)], (150, 100))
    pygame.display.update()

def end_screen(won):
    win.fill((255, 255, 255))
    if won:
        result_text = WORD_FONT.render("You Win!", True, (0, 200, 0))
    else:
        result_text = WORD_FONT.render("You Lose!", True, (255, 0, 0))
    win.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 300))

    word_text = WORD_FONT.render(f"The word was: {word}", True, (0, 0, 0))
    win.blit(word_text, (WIDTH // 2 - word_text.get_width() // 2, 400))
    
    reset_text = HINT_FONT.render("Click to Restart", True, (0, 0, 0))
    win.blit(reset_text, (WIDTH // 2 - reset_text.get_width() // 2, 500))
    pygame.display.update()
    
    # Wait for a mouse click to restart the game
    waiting_for_click = True
    while waiting_for_click:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # After clicking, restart the game without quitting
                global reset_count
                if reset_count > 0:
                    reset_count -= 1
                    reset_game()
                waiting_for_click = False
                return

def main():
    global hangman_status, score, reset_count
    clock = pygame.time.Clock()
    run = True
    won = False
    
    # Start a new game at the beginning
    reset_game()

    while run:
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if hangman_status >= 6 or all(l in guessed for l in word):
                    end_screen(hangman_status < 6)
                else:
                    m_x, m_y = pygame.mouse.get_pos()
                    if WIDTH // 2 - 60 <= m_x <= WIDTH // 2 + 60 and 600 <= m_y <= 640:
                        show_hint()
                    elif WIDTH // 2 - 60 <= m_x <= WIDTH // 2 + 60 and 650 <= m_y <= 690:
                        if reset_count > 0:
                            reset_count -= 1
                            reset_game()
                    for letter in letters:
                        x, y, ltr, visible = letter
                        if visible:
                            distance = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                            if distance < RADIUS:
                                letter[3] = False
                                guessed.append(ltr)
                                if ltr not in word:
                                    hangman_status += 1
                                if all(l in guessed for l in word):
                                    won = True
                                    score += 10
                                if hangman_status >= 6:
                                    won = False
                                    run = False
        if hangman_status >= 6 or all(l in guessed for l in word):
            end_screen(hangman_status < 6)
        else:
            draw()
    
    pygame.quit()

if __name__ == "__main__":
    main()
