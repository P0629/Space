import pygame
import random

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

# Laden der Bilder für den Spieler und die Gegner
player_image = pygame.image.load("schiff.png")
player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))

enemy1_image = pygame.image.load("alien1.png")
enemy1_image = pygame.transform.scale(enemy1_image, (ENEMY_WIDTH, ENEMY_HEIGHT))

enemy2_image = pygame.image.load("alien2.png")
enemy2_image = pygame.transform.scale(enemy2_image, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Laden des Hintergrunds
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Initialisierung des Bildschirms
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Weiche den Feinden aus")
clock = pygame.time.Clock()

# Funktion zum Erzeugen eines neuen Gegners
def create_enemy():
    x = random.randint(0, WIDTH - ENEMY_WIDTH)
    y = 0 - ENEMY_HEIGHT
    enemy_type = random.choice([1, 2])  # Zufällig zwischen den beiden Gegnertypen wählen
    return pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT), enemy_type

# Funktion zum Bewegen der Gegner
def move_enemies(enemies):
    for enemy in enemies:
        enemy[0].y += ENEMY_SPEED

# Funktion um GAME OVER anzuzeigen
def display_game_over():
    font = pygame.font.SysFont(None, 48)
    game_over_text = font.render("GAME OVER", True, (255, 255, 0))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))

# Funktion zum Zeichnen von Schüssen
def draw_shots(shots):
    for shot in shots:
        pygame.draw.rect(screen, (255, 0, 0), shot)

# Hauptspiel
def main():
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - 50, PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = []
    shots = []  # Liste für die Schüsse des Spielers
    shoot_cooldown = 0

    running = True
    game_over = False  # Spielstatus verfolgen

    while running:
        screen.blit(background, (0, 0)) # Hintergrund zeichnen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                # Spieler mit Maus bewegen
                player.centerx, player.centery = event.pos
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                # Schießen, wenn linke Maustaste gedrückt wird
                if shoot_cooldown == 0:
                    shots.append(pygame.Rect(player.centerx - 2, player.top - 10, 4, 10))
                    shoot_cooldown = PLAYER_SHOOT_COOLDOWN

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

            # Zeichne Spieler
            screen.blit(player_image, player)

            # Zeichne Gegner
            for enemy, enemy_type in enemies:
                if enemy_type == 1:
                    screen.blit(enemy1_image, enemy)
                else:
                    screen.blit(enemy2_image, enemy)

            # Zeichne Schüsse
            draw_shots(shots)

            # Reduziere die Abklingzeit für Schüsse
            if shoot_cooldown > 0:
                shoot_cooldown -= 1

        if game_over:
            display_game_over()  # GAME OVER anzeigen

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
