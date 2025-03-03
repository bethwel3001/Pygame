import pygame
import random
import sys

pygame.init()

# Screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Game title
pygame.display.set_caption("Plane Fighting Game - A Next-Space Software")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load images
player_image = pygame.image.load("images/player_imagejpeg.jpeg").convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 50)) 
enemy_image = pygame.image.load("images/enemy_image.jpeg").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
background_image = pygame.image.load("images/background.webp")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
bullet_image = pygame.Surface((8, 20))
bullet_image.fill((255, 0, 0))

# Load sounds
shoot_sound = pygame.mixer.Sound("sounds/shot.mp3")
explosion_sound = pygame.mixer.Sound("sounds/explode.mp3")

# Score variables
score = 0
font = pygame.font.Font(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 20
        self.speed = 5
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.defeated = False

    def update(self):
        if self.defeated:
            return

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))

        # Shooting
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

    def update(self):
        if player.defeated:
            return
        self.rect.y += self.speed
        if self.rect.top > screen_height:
            self.reset()

    def reset(self):
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Initialize player
player = Player()

# Sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Spawn initial enemies
for _ in range(10):
    enemy = Enemy()
    enemies.add(enemy)
    all_sprites.add(enemy)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Check for collisions between bullets and enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit_enemy in hits:
        explosion_sound.play()
        score += 5  # Add 5 points for each enemy hit
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check for collisions between player and enemies
    if pygame.sprite.spritecollide(player, enemies, False):
        player.defeated = True

    # Draw everything
    screen.blit(background_image, (0, 0))  # Draw background
    all_sprites.draw(screen)

    # Display score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Game over logic
    if player.defeated:
        game_over_text = font.render("Game Over! Final Score: " + str(score), True, (255, 0, 0))
        screen.blit(game_over_text, (screen_width // 2 - 150, screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait 3 seconds before quitting
        running = False

    # Refresh screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()