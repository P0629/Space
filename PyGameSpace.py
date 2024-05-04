import pygame
import random
import sys
import os

# Initialisierung von Pygame
pygame.init()

# Bildschirmabmessungen
WIDTH, HEIGHT = 600, 400

# Spieler Eigenschaften
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 20
PLAYER_SPEED = 5
PLAYER_SHOOT_COOLDOWN = 20  # Abklingzeit zwischen den Schüssen

# Gegner Eigenschaften
ENEMY_WIDTH, ENEMY_HEIGHT = 30, 30
ENEMY_SPEED = 3
ENEMY_INTERVAL = 60  # Intervall, in dem ein neuer Gegner erscheint

# Sterne Eigenschaften
STAR_WIDTH, STAR_HEIGHT = 20, 20
STAR_SPEED = 2
STAR_INTERVAL = 100  # Intervall, in dem ein neuer Stern erscheint

# Laden der Bilder für den Spieler, die Gegner und die Sterne
player_image = pygame.image.load("schiff.png")
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

enemy1_image = pygame.image.load("alien1.png")
enemy1_image = pygame.transform.scale(enemy1_image, (ENEMY_WIDTH, ENEMY_HEIGHT))

enemy2_image = pygame.image.load("alien2.png")
enemy2_image = pygame.transform.scale(enemy2_image, (ENEMY_WIDTH, ENEMY_HEIGHT))

star_image = pygame.image.load("Stern.png")
star_image = pygame.transform.scale(star_image, (STAR_WIDTH, STAR_HEIGHT))

# Laden des Hintergrunds
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Datei für Highscores
HIGHSCORE_FILE = "highscores.txt"

# Initialisierung des Bildschirms
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weiche den Feinden aus")
clock = pygame.time.Clock()

# Funktion zum Laden der Highscores aus der Datei
def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    with open(HIGHSCORE_FILE, "r") as file:
        lines = file.readlines()
        highscores = [line.strip().split(",") for line in lines]
        highscores.sort(key=lambda x: int(x[1]), reverse=True)
        return highscores

# Funktion zum Speichern der Highscores in die Datei
def save_highscores(highscores):
    with open(HIGHSCORE_FILE, "w") as file:
        for name, score in highscores:
            file.write(f"{name},{score}\n")

# Funktion zum Erzeugen eines neuen Gegners
def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = 0 - ENEMY_HEIGHT
    enemy_type = random.choice([1, 2])  # Zufällig zwischen den beiden Gegnertypen wählen
    return pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT), enemy_type

# Funktion zum Erzeugen eines neuen Sterns
def create_star():
    x = random.randint(0, WIDTH - STAR_WIDTH)
    y = 0 - STAR_HEIGHT
    return pygame.Rect(x, y, STAR_WIDTH, STAR_HEIGHT)

# Funktion zum Bewegen der Gegner
def move_enemies(enemies):
    for enemy in enemies:
        enemy[0].y += ENEMY_SPEED

# Funktion zum Bewegen der Sterne
def move_stars(stars):
    for star in stars:
        star.y += STAR_SPEED

# Funktion um GAME OVER anzuzeigen und Optionen für Neustart oder Beenden
def display_game_over(score):
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("GAME OVER", True, (255, 255, 0))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    
    # Anzeigen der besten 3 Highscores
    highscores = load_highscores()
    font = pygame.font.SysFont(None, 30)
    for i, (name, highscore) in enumerate(highscores[:3], start=1):
        score_text = font.render(f"{i}. {name}: {highscore}", True, (255, 255, 255))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 30 + 30 * i))
    
    # Eingabeaufforderung für den Namen des Spielers
    input_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 30 * 6, WIDTH // 2, 30)
    pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
    font = pygame.font.SysFont(None, 24)
    input_text = font.render("Deinen Namen eingeben:", True, (255, 255, 255))
    screen.blit(input_text, (WIDTH // 4, HEIGHT // 2 + 30 * 5))
    
    pygame.display.flip()
    
    name = ""
    input_active = True
    while input_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        input_rect.w = max(200, input_text.get_width() + 10)
        input_rect.x = WIDTH // 2 - input_rect.w // 2
        pygame.draw.rect(screen, (0, 0, 0), input_rect)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
        screen.blit(font.render(name, True, (255, 255, 255)), (input_rect.x + 5, input_rect.y + 5))
        pygame.display.flip()
    
    # Füge den neuen Highscore hinzu und speichere ihn
    highscores.append((name, str(score)))
    highscores.sort(key=lambda x: int(x[1]), reverse=True)
    save_highscores(highscores)
    
    # Anzeige des Neustartmenüs und Verarbeitung der Benutzeraktionen
    display_restart_menu()

# Funktion zum Zeichnen von Schüssen
def draw_shots(shots):
    for shot in shots:
        pygame.draw.rect(screen, (255, 0, 0), shot)
    
# Funktion zum Anzeigen des Scores
def display_score(score):
    font = pygame.font.SysFont(None, 30)
    score_text = font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(score_text, (10, 10))

# Funktion zur Anzeige des Neustartmenüs
def display_restart_menu():
    font = pygame.font.SysFont(None, 30)
    restart_text = font.render("Drücke R zum Neustarten oder Q zum Beenden", True, (255, 255, 255))
    text_width, text_height = font.size("Drücke R zum Neustarten oder Q zum Beenden")
    screen.blit(restart_text, ((WIDTH - text_width) // 2, HEIGHT // 2 - text_height - 20))  # Position über dem "GAME OVER"-Schriftzug
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Starte das Spiel neu
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()  # Beende das Spiel
    return False

# Hauptspiel
def main():
    global ENEMY_SPEED # Zugriff auf die globale Variable

    # Ursprüngliche Geschwindigkeit der Gegner nach Neustart
    original_enemy_speed = ENEMY_SPEED

    enemy_speed_increase_timer = 0 # Initialisierung der Variable
    enemy_speed_increase_interval = 5000 # Timerintervall für die Geschwindigkeitserhöhung
    enemy_speed_increase_amount = 1 # Betrag, um den die Geschwindigkeit des Feindes erhöht wird

    # Timer für Sterne
    star_timer = 0

    paused = False  # Variable für den Pausenzustand des Spiels

    # PAUSE-Text anzeigen
    font = pygame.font.SysFont(None, 48)
    pause_text = font.render("PAUSE", True, (255, 255, 0))  # Gelber Text
    pause_text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    while True:  # Spielenschleife für Neustarts
        player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - 50, PLAYER_WIDTH, PLAYER_HEIGHT)
        enemies = []
        stars = []  # Liste für die Sterne
        shots = []  # Liste für die Schüsse des Spielers
        shoot_cooldown = 0
        score = 0   # Score des Spielers
        score_timer = 0 # Initialisierung des Score-Timers

        running = True
        game_over = False  # Spielstatus verfolgen

        # Zurücksetzen der Geschwindigkeit auf Anfangswert
        ENEMY_SPEED = original_enemy_speed

        while running:
            screen.blit(background, (0, 0)) # Hintergrund zeichnen

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    # Spieler mit Maus bewegen
                    player.centerx, player.centery = event.pos
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                    # Schießen, wenn linke Maustaste gedrückt wird
                    if shoot_cooldown == 0:
                        shots.append(pygame.Rect(player.centerx - 2, player.top - 10, 4, 10))
                        shoot_cooldown = PLAYER_SHOOT_COOLDOWN
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Pausentaste
                        paused = not paused

            if paused:
                screen.blit(pause_text, pause_text_rect) # PAUSE-Text anzeigen
                pygame.display.flip()
                continue  # Springe zurück zur Schleifenbeginn

            if not game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    player.x -= PLAYER_SPEED
                if keys[pygame.K_RIGHT]:
                    player.x += PLAYER_SPEED

                # Begrenze den Spieler auf den Bildschirm
                player.x = max(0, min(player.x, WIDTH - PLAYER_WIDTH))
                player.y = max(0, min(player.top, HEIGHT - PLAYER_HEIGHT))

                # Bewege die Gegner und füge neue hinzu
                move_enemies(enemies)
                if random.randint(0, ENEMY_INTERVAL) == 0:
                    enemy, enemy_type = create_enemy()
                    enemies.append((enemy, enemy_type))
                
                # Bewege die Sterne und füge neue hinzu
                move_stars(stars)
                star_timer += 1
                if star_timer == STAR_INTERVAL:
                    stars.append(create_star())
                    star_timer = 0
                
                # Erhöhe die Geschwindigkeit der Feinde basierend auf den Timer
                enemy_speed_increase_timer += clock.get_time()
                if enemy_speed_increase_timer >= enemy_speed_increase_interval:
                    ENEMY_SPEED += enemy_speed_increase_amount
                    enemy_speed_increase_timer = 0

                # Bewege Schüsse und entferne sie, wenn sie den Bildschirm verlassen
                for shot in shots[:]:
                    shot.y -= 5
                    if shot.bottom < 0:
                        shots.remove(shot)

                # Kollisionserkennung für Schüsse und Gegner
                for shot in shots[:]:
                    for enemy in enemies[:]:
                        if shot.colliderect(enemy[0]):
                            shots.remove(shot)
                            enemies.remove(enemy)

                # Kollisionserkennung für Spieler und Gegner
                for enemy in enemies:
                    if player.colliderect(enemy[0]):
                        game_over = True  # Spielstatus aktualisieren
                
                # Kollisionserkennung für Spieler und Sterne
                for star in stars[:]:
                    if player.colliderect(star):
                        stars.remove(star)
                        score += 10  # Bonuspunkte für das Einsammeln eines Sterns

                # Zeichne Spieler
                screen.blit(player_image, player)

                # Zeichne Gegner
                for enemy, enemy_type in enemies:
                    if enemy_type == 1:
                        screen.blit(enemy1_image, enemy)
                    else:
                        screen.blit(enemy2_image, enemy)

                # Zeichne Sterne
                for star in stars:
                    screen.blit(star_image, star)

                # Zeichne Schüsse
                draw_shots(shots)

                # Reduziere die Abklingzeit für Schüsse
                if shoot_cooldown > 0:
                    shoot_cooldown -= 1

                # Aktualisiere den Score-Timer und füge Bonuspunkte hinzu, wenn der Timer abläuft
                score_timer += 1
                if score_timer == 60:  # Füge alle 60 Frames (1 Sekunde) Bonuspunkte hinzu
                    score += 5
                    score_timer = 0

                # Zeichne Score
                display_score(score)

            if game_over:
                display_game_over(score)
                running = False

            pygame.display.flip()
            clock.tick(60)

        # Anzeige des Neustartmenüs und Verarbeitung der Benutzeraktionen
        if not display_restart_menu():
            break  # Beende die Schleife, wenn der Benutzer das Spiel beendet

    pygame.quit()

if __name__ == "__main__":
    main()
