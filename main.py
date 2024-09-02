try:
    import pygame
    import time
    import random
    import pyautogui
    from datetime import datetime
    import os
    import requests

    # Create all the required dirs
    os.makedirs(os.getcwd(), "gameFiles")
    os.makedirs(os.getcwd(), "gameFiles/gameAssets")
    os.makedirs(os.getcwd(), "gameFiles/gameInfo")
    os.makedirs(os.getcwd(), "gameFiles/gameScreenshots")
    
    image_urls = [
        "https://raw.githubusercontent.com/Bernso/MyFirstPythonGame/main/gameFiles/gameAssets/lazer.png",
        "https://raw.githubusercontent.com/Bernso/MyFirstPythonGame/main/gameFiles/gameAssets/body-bg.jpg",
        "https://raw.githubusercontent.com/Bernso/MyFirstPythonGame/main/gameFiles/gameAssets/player.png",
        "https://raw.githubusercontent.com/Bernso/MyFirstPythonGame/main/gameFiles/gameAssets/powerup.png",
        "https://raw.githubusercontent.com/Bernso/MyFirstPythonGame/main/gameFiles/gameAssets/shield.png"
    ]

    download_dir = os.path.join(os.getcwd(), "gameFiles/gameAssets")

    def download_images(image_urls, download_dir):
        # Ensure the download directory exists
        os.makedirs(download_dir, exist_ok=True)

        for image_url in image_urls:
            file_name = image_url.split('/')[-1]  # Extract the file name from URL
            file_path = os.path.join(download_dir, file_name)

            if os.path.exists(file_path):
                print(f"{file_name} already exists in {download_dir}")
                continue
            
            # Download the image
            print(f"Downloading {file_name} from {image_url}...")
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(file_path, 'wb') as handler:
                    handler.write(response.content)
                print(f"Saved {file_name} to {download_dir}")
            else:
                print(f"Failed to download {file_name}: {response.status_code}")

    download_images(image_urls=image_urls, download_dir=download_dir)


    # Allow for fonts
    pygame.font.init()

    # Dimensions
    WIDTH = 1000
    HEIGHT = 800

    # Window Properties
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My First Game")
    FONT = pygame.font.SysFont("Gang Of Three", 30)

    # Assets
    BG = pygame.transform.scale(pygame.image.load("gameFiles/gameAssets/body-bg.jpg"), (WIDTH, HEIGHT))
    PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("gameFiles/gameAssets/player.png"), (40, 60))
    STAR_IMAGE = pygame.transform.scale(pygame.image.load("gameFiles/gameAssets/lazer.png"), (10, 20))  
    
    # Player Properties
    PLAYER_WIDTH = PLAYER_IMAGE.get_width()
    PLAYER_HEIGHT = PLAYER_IMAGE.get_height()
    PLAYER_VELOCITY = 5

    # Star Properties (enemies)
    STAR_WIDTH = STAR_IMAGE.get_width()
    STAR_HEIGHT = STAR_IMAGE.get_height()
    STAR_VELOCITY = 3

    def screenshot():
        path = os.path.join(os.getcwd(), "gameFiles/gameScreenshots")
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
        
        text_score = FONT.render(f"Score: {score}", 1, "Black")
        WIN.blit(text_score, (10, 10))
        
        text_time = FONT.render(f"Time: {round(elapsed_time)}", 1, "Black")
        WIN.blit(text_time, (10, 10 + text_score.get_height()))
        
        # Draw the player as a spaceship
        WIN.blit(PLAYER_IMAGE, (player.x, player.y))
        
        # Draw stars as laser beams
        for star in stars:
            WIN.blit(STAR_IMAGE, (star.x, star.y))
        
        pygame.display.update()

    def main():
        run = True
        score = 0
        player = pygame.Rect(random.randint(0, WIDTH - PLAYER_WIDTH), HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
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
            
            star_count += clock.tick(60) # How many milliseconds since the last tick and To regulate the while loop (make sure it doesnt run too fast)
            elapsed_time = time.time() - start_time
            
            if star_count > star_add_increment:
                for _ in range(5):
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
                text_border_border = pygame.Rect(WIDTH/2 - lost_text.get_width()/2 - 55, HEIGHT/2 - lost_text.get_height()/2 - 55, lost_text.get_width() + 110, lost_text.get_height() + 110)
                pygame.draw.rect(WIN, "White", text_border_border)
                text_border = pygame.Rect(WIDTH/2 - lost_text.get_width()/2 - 50, HEIGHT/2 - lost_text.get_height()/2 - 50, lost_text.get_width() + 100, lost_text.get_height() + 100)
                pygame.draw.rect(WIN, "Black", text_border)
                WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
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
except Exception as e:
    input(e)