import pygame
import time
import random
import pyautogui
from datetime import datetime
import os

# Allow for fonts
pygame.font.init()

# Dimesntions
WIDTH = 1000
HEIGHT = 800

# Window Properties
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My First Game")
FONT = pygame.font.SysFont("Gang Of Three", 30)

# Assets
BG = pygame.transform.scale(pygame.image.load("assets/body-bg.jpg"), (WIDTH, HEIGHT))

# Player Properties
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VELOCITY = 5

# Star Dimensions (enemies)
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VELOCITY = 3

def screenshot():
    path = os.path.join(os.getcwd(), "screenshots")
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    
    save_directory = path

    # Generate the screenshot filename based on the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}.png"

    # Full path
    file_path = os.path.join(save_directory, filename)

    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot
    screenshot.save(file_path)

    print(f"Screenshot saved to {file_path}")

def draw(player, elapsed_time, stars, score):
    WIN.blit(BG, (0, 0))
    
    text_score = FONT.render(f"Score: {score}", # Text
                            1, "Black" # Properties (anti-aliusing, colour)
                            )
    
    WIN.blit(text_score, # Text
            (10, 10) # Co-ordinates
            )
    
    text_time = FONT.render(f"Time: {round(elapsed_time)}", # Text
                            1, "Black" # Properties (anti-aliusing, colour)
                            )
    
    WIN.blit(text_time, # Text
            (10, 10 + text_score.get_height()) # Co-ordinates
            )
    
    
    
    
    pygame.draw.rect(WIN, "Green", player)
    
    for star in stars:
        pygame.draw.rect(WIN, "White", star)
    
    pygame.display.update()


def main():
    run = True
    score = 0
    
    player = pygame.Rect(
        random.randint(0, WIDTH - PLAYER_WIDTH), (HEIGHT - PLAYER_HEIGHT), # Spawn co-ordinates of the player
        PLAYER_WIDTH, PLAYER_HEIGHT # Dimensions of the player
        )
    print(f"Player Spawned at ({player.x}, {player.y})")
    
    clock = pygame.time.Clock() # To regulate the while loop (make sure it doesnt run too fast)
    
    start_time = time.time()
    elapsed_time = 0
    
    star_add_increment = 2000
    star_count = 0
    
    stars = []
    hit = False
    
    while run:
        score += 1
        
        star_count += clock.tick(60) # How many milliseconds since the last click and To regulate the while loop (make sure it doesnt run too fast)
        elapsed_time = time.time() - start_time
        
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH) # Position where the star spawns (x value)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT) # Position
                stars.append(star)
                
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0
        
        
        for event in pygame.event.get():
            # Check if the game has been stopped
            if event.type == pygame.QUIT:
                print("Closing game...")
                run = False
                break
        
        # Keybinds
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
            #print(f"Player moved to position {player.x}")
            
        elif keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VELOCITY
            #print(f"Player moved to position {player.x}")
        
        for star in stars[:]: # Copy of the stars list
            star.y += STAR_VELOCITY
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                print("Player hit a star")
                hit = True
                break
                
        if hit:
            print("Game Over!")
            
            FONT = pygame.font.SysFont("Gang Of Three", 80)
    
            lost_text = FONT.render(f"You Lost", 1, "Red")
            
            text_border_border = pygame.Rect(
                WIDTH/2 - lost_text.get_width()/2 - 50 - 5, HEIGHT/2 - lost_text.get_height()/2 - 50 - 5, # Co-ordiantes (with padding)
                (lost_text.get_width() + 100 + 10), (lost_text.get_height() + 100 + 10) # Dimensions (with padding)
            )
            pygame.draw.rect(WIN, "White", text_border_border)
            
            text_border = pygame.Rect(
                WIDTH/2 - lost_text.get_width()/2 - 50, HEIGHT/2 - lost_text.get_height()/2 - 50, # Co-ordiantes (with padding)
                (lost_text.get_width()+100), (lost_text.get_height()+100) # Dimensions (with padding)
            )
            pygame.draw.rect(WIN, "Black", text_border)
            
            
            
            WIN.blit(lost_text, # Text
                    (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2)) # Co-ordinates
            
            pygame.display.update()
            
            screenshot()
            
            for seconds in range(4):
                print(f"Game closing in {4 - seconds}")
                pygame.time.delay(1000)
            
            break # Stops the while loop, that makes the game do stuff
        
        
        draw(player=player, elapsed_time=elapsed_time, stars=stars, score=score)

    
    # Close the game once everything has been run
    pygame.quit()
    

if __name__ == "__main__":
    main()