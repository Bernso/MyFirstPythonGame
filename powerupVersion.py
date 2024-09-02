try:
    import pygame
    import time
    import random
    import pyautogui
    from datetime import datetime
    import os
    import requests


    image_urls = [
        "https://raw.githubusercontent.com/Bernso/MyFirstPythonGame/5ed27eb12f68210431f12ada0ea2f5a1ff221f7c/assets/lazer.png",
        "https://raw.githubusercontent.com/Bernso/MyFirstPythonGame/5ed27eb12f68210431f12ada0ea2f5a1ff221f7c/assets/body-bg.jpg",
        "https://raw.githubusercontent.com/Bernso/MyFirstPythonGame/5ed27eb12f68210431f12ada0ea2f5a1ff221f7c/assets/player.png",
        "https://raw.githubusercontent.com/Bernso/MyFirstPythonGame/main/assets/powerup.png",
        "https://raw.githubusercontent.com/Bernso/MyFirstPythonGame/main/assets/shield.png"
    ]

    download_dir = os.path.join(os.getcwd(), "assets")

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
    BG = pygame.transform.scale(pygame.image.load("assets/body-bg.jpg"), (WIDTH, HEIGHT))
    PLAYER_IMAGE = pygame.transform.scale(pygame.image.load("assets/player.png"), (40, 60))
    STAR_IMAGE = pygame.transform.scale(pygame.image.load("assets/lazer.png"), (10, 20))
    SHIELD_IMAGE = pygame.transform.scale(pygame.image.load("assets/shield.png"), (30, 30))  # Add shield asset
    POWERUP_IMAGE = pygame.transform.scale(pygame.image.load("assets/powerup.png"), (20, 20))  # Add power-up asset

    # Sound Effects
    pygame.mixer.init()
    #HIT_SOUND = pygame.mixer.Sound("assets/hit.wav")  # Add sound file for hit
    #POWERUP_SOUND = pygame.mixer.Sound("assets/powerup.wav")  # Add sound file for power-up

    # Player Properties
    PLAYER_WIDTH = PLAYER_IMAGE.get_width()
    PLAYER_HEIGHT = PLAYER_IMAGE.get_height()
    PLAYER_VELOCITY = 5

    # Star Properties (enemies)
    STAR_WIDTH = STAR_IMAGE.get_width()
    STAR_HEIGHT = STAR_IMAGE.get_height()
    STAR_VELOCITY = 3

    # Game Properties
    player_health = 3  # Player has 3 lives
    shield_active = False
    shield_duration = 5000  # Shield lasts for 5 seconds
    shield_start_time = 0
    powerup_active = False
    powerup_start_time = 0
    powerup_duration = 5000  # Power-up lasts for 5 seconds
    high_score = 0

    def screenshot():
        path = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        save_directory = path
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}.png"
        file_path = os.path.join(save_directory, filename)
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
        print(f"Screenshot saved to {file_path}")

    def draw(player, elapsed_time, stars, score, health, powerups, shields):
        WIN.blit(BG, (0, 0))

        # Score and Time Display
        text_score = FONT.render(f"Score: {score}", 1, "Black")
        WIN.blit(text_score, (10, 10))

        text_time = FONT.render(f"Time: {round(elapsed_time)}", 1, "Black")
        WIN.blit(text_time, (10, 10 + text_score.get_height()))

        # Draw the player as a spaceship
        WIN.blit(PLAYER_IMAGE, (player.x, player.y))

        # Draw stars as laser beams
        for star in stars:
            WIN.blit(STAR_IMAGE, (star.x, star.y))

        # Draw power-ups
        for powerup in powerups:
            WIN.blit(POWERUP_IMAGE, (powerup.x, powerup.y))

        # Draw shield if active
        if shield_active:
            WIN.blit(SHIELD_IMAGE, (player.x, player.y))

        # Draw shields on the screen
        for shield in shields:
            WIN.blit(SHIELD_IMAGE, (shield.x, shield.y))

        # Display health
        text_health = FONT.render(f"Health: {health}", 1, "Red")
        WIN.blit(text_health, (10, 10 + text_score.get_height() + text_time.get_height()))

        pygame.display.update()

    def main():
        global shield_active, shield_start_time, powerup_active, powerup_start_time, high_score, player_health, PLAYER_VELOCITY

        run = True
        score = 0
        player = pygame.Rect(random.randint(0, WIDTH - PLAYER_WIDTH), HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
        print(f"Player Spawned at ({player.x}, {player.y})")

        clock = pygame.time.Clock()
        start_time = time.time()
        elapsed_time = 0
        star_add_increment = 2000
        star_count = 0
        stars = []
        powerups = []
        shields = []
        hit = False

        while run:
            score += 1
            star_count += clock.tick(60)
            elapsed_time = time.time() - start_time

            # Add stars (laser beams)
            if star_count > star_add_increment:
                for _ in range(3):
                    star_x = random.randint(0, WIDTH - STAR_WIDTH)
                    star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                    stars.append(star)

                star_add_increment = max(200, star_add_increment - 50)
                star_count = 0

            # Add power-ups occasionally
            if random.randint(1, 1000) > 995:
                powerup_x = random.randint(0, WIDTH - 20)
                powerup = pygame.Rect(powerup_x, -20, 20, 20)
                powerups.append(powerup)

            # Add shields occasionally
            if random.randint(1, 1000) > 995:
                shield_x = random.randint(0, WIDTH - 30)
                shield = pygame.Rect(shield_x, -30, 30, 30)
                shields.append(shield)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Closing game...")
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
                player.x -= PLAYER_VELOCITY
            elif keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + PLAYER_WIDTH <= WIDTH:
                player.x += PLAYER_VELOCITY

            # Update stars, power-ups, and shields positions
            for star in stars[:]:
                star.y += STAR_VELOCITY
                if star.y > HEIGHT:
                    stars.remove(star)
                elif star.y + star.height >= player.y and star.colliderect(player):
                    if not shield_active:
                        stars.remove(star)
                        #HIT_SOUND.play()
                        player_health -= 1
                        if player_health <= 0:
                            hit = True
                            break
                    else:
                        shield_active = False
                        stars.remove(star)

            for powerup in powerups[:]:
                powerup.y += 2
                if powerup.y > HEIGHT:
                    powerups.remove(powerup)
                elif powerup.colliderect(player):
                    powerups.remove(powerup)
                    #POWERUP_SOUND.play()
                    powerup_active = True
                    powerup_start_time = pygame.time.get_ticks()
                    PLAYER_VELOCITY = 10

            for shield in shields[:]:
                shield.y += 2
                if shield.y > HEIGHT:
                    shields.remove(shield)
                elif shield.colliderect(player):
                    shields.remove(shield)
                    shield_active = True
                    shield_start_time = pygame.time.get_ticks()

            # Check for shield and power-up expiration
            if shield_active and pygame.time.get_ticks() - shield_start_time > shield_duration:
                shield_active = False
            if powerup_active and pygame.time.get_ticks() - powerup_start_time > powerup_duration:
                powerup_active = False
                PLAYER_VELOCITY = 5

            if hit:
                print("Game Over!")
                if score > high_score:
                    high_score = score
                    print(f"New High Score: {high_score}")

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

                break

            draw(player=player, elapsed_time=elapsed_time, stars=stars, score=score, health=player_health, powerups=powerups, shields=shields)

        pygame.quit()

    if __name__ == "__main__":
        main()
except Exception as e:
    input(e)