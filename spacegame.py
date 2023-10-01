import pygame
import random


pygame.init()


coin_sound = pygame.mixer.Sound('coin.wav')
death_sound = pygame.mixer.Sound('death.wav')


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = pygame.display.get_surface().get_size()


background_image = pygame.image.load('background_new2.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))


block_images = [
    pygame.image.load('block1.png'),
    pygame.image.load('block2.png'),
    pygame.image.load('block3.png'),

]
game_over = False

BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
LIGHT_BLUE = (135, 206, 250)
TRANSPARENT = (0, 0, 0, 0)
DARK_OVERLAY = (0, 0, 0, 150)
WHITE = (255, 255, 255, 255)


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.speed_x = random.randrange(-5, 5)
        self.speed_y = random.randrange(-5, 5)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed_x *= -1
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.speed_y *= -1


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('coin.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - 30)
        self.rect.y = random.randrange(HEIGHT - 30)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('powerup.png')
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - 30)
        self.rect.y = random.randrange(HEIGHT - 30)






class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.image.load('player2.png')
        self.original_image = pygame.transform.scale(self.original_image, (50, 50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.speed = 5
        self.collected_coins = 0
        self.invulnerable = True
        self.invulnerable_timer = 2
        self.invulnerable_start_time = pygame.time.get_ticks()
        self.direction = 0
        self.extra_lives = 0
        self.extra_life_threshold = 5
        self.extra_life_used = False

    def update(self, keys):
        if self.invulnerable and pygame.time.get_ticks() - self.invulnerable_start_time >= self.invulnerable_timer * 1000:
            self.invulnerable = False

        if not self.invulnerable:
            if keys[pygame.K_UP] and self.rect.y > 0:
                self.move(0, -self.speed)
                self.direction = 0
            if keys[pygame.K_DOWN] and self.rect.y < HEIGHT - self.rect.height:
                self.move(0, self.speed)
                self.direction = 180
            if keys[pygame.K_LEFT] and self.rect.x > 0:
                self.move(-self.speed, 0)
                self.direction = 270
            if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
                self.move(self.speed, 0)
                self.direction = 90
        else:
            if keys[pygame.K_UP] and self.rect.y > 0:
                self.move(0, -self.speed)
                self.direction = 0
            if keys[pygame.K_DOWN] and self.rect.y < HEIGHT - self.rect.height:
                self.move(0, self.speed)
                self.direction = 180
            if keys[pygame.K_LEFT] and self.rect.x > 0:
                self.move(-self.speed, 0)
                self.direction = 270
            if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
                self.move(self.speed, 0)
                self.direction = 90

        self.rotate_image()

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def rotate_image(self):
        if self.direction == 0:
            self.image = pygame.transform.rotate(self.original_image, 0)
        elif self.direction == 90:
            self.image = pygame.transform.rotate(self.original_image, -90)
        elif self.direction == 180:
            self.image = pygame.transform.rotate(self.original_image, 180)
        elif self.direction == 270:
            self.image = pygame.transform.rotate(self.original_image, 90)

    def draw_shield(self, screen):
        shield_radius = 45
        pygame.draw.circle(screen, TRANSPARENT, self.rect.center, shield_radius)
        pygame.draw.circle(screen, LIGHT_BLUE, self.rect.center, shield_radius, 2)


game_objects = pygame.sprite.Group()
for _ in range(10):
    block_image = random.choice(block_images)
    game_object = GameObject(block_image)
    game_objects.add(game_object)

coins = pygame.sprite.Group()
power_ups = pygame.sprite.Group()


player = Player()


clock = pygame.time.Clock()
start_ticks = 0
game_over = False


block_spawn_timer = 1.5
last_block_spawn_time = 0


coin_spawn_timer = 4.5
last_coin_spawn_time = 0


power_up_spawn_timer = 8
last_power_up_spawn_time = 0


font = pygame.font.Font(None, 36)


ranking_file = "bestzeiten.txt"
best_times = []
try:
    with open(ranking_file, "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) == 2:
                name, time = data
                best_times.append((name, float(time)))
except FileNotFoundError:
    pass


def save_ranking():
    with open(ranking_file, "w") as file:
        for name, time in best_times:
            file.write(name + "," + str(time) + "\n")


def enter_player_name():
    global player_name
    player_name = ""
    entering_name = True
    while entering_name:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(player_name) > 0:
                    entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        screen.fill(BLACK)
        enter_name_text = font.render("Name eingeben:", True, WHITE)
        text_rect = enter_name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        screen.blit(enter_name_text, text_rect)
        name_text = font.render(player_name, True, BLUE)
        name_rect = name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
        screen.blit(name_text, name_rect)
        pygame.display.flip()
        clock.tick(60)


def restart_game():
    global start_ticks, game_over
    start_ticks = pygame.time.get_ticks()
    game_over = False
    player.rect.centerx = WIDTH // 2
    player.rect.centery = HEIGHT // 2
    player.collected_coins = 0
    game_objects.empty()
    for _ in range(10):
        block_image = random.choice(block_images)
        game_object = GameObject(block_image)
        game_objects.add(game_object)

    coins.empty()
    power_ups.empty()








running = True
show_ranking = False
while running:
    current_time = pygame.time.get_ticks() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r and game_over:
                restart_game()
                player.invulnerable = True
                player.invulnerable_start_time = pygame.time.get_ticks()
                player.extra_life_used = False

            elif event.key == pygame.K_t and not game_over:
                show_ranking = not show_ranking

        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_button_rect.collidepoint(event.pos):
                restart_game()
                player.invulnerable = True
                player.invulnerable_start_time = pygame.time.get_ticks()
                player.extra_life_used = False

    keys = pygame.key.get_pressed()
    if not game_over and not show_ranking:
        player.update(keys)

    screen.blit(background_image, (0, 0))

    if show_ranking:
        screen.fill(DARK_OVERLAY)

    if not game_over and not show_ranking:
        game_objects.update()
        game_objects.draw(screen)

        coins.update()
        coins.draw(screen)

        power_ups.update()
        power_ups.draw(screen)

        if player.invulnerable:
            player.draw_shield(screen)

        screen.blit(player.image, player.rect)

        collected_coins = pygame.sprite.spritecollide(player, coins, True)
        for coin in collected_coins:
            player.collected_coins += 1
            coin_sound.play()

            if player.collected_coins >= player.extra_life_threshold:
                while player.collected_coins >= player.extra_life_threshold:
                    player.extra_lives += 1
                    player.collected_coins -= player.extra_life_threshold

        if pygame.sprite.spritecollide(player, game_objects, True):
            if not player.invulnerable:
                if player.extra_lives > 0:
                    player.extra_lives -= 1
                    player.invulnerable = True
                    player.invulnerable_start_time = pygame.time.get_ticks()
                else:
                    game_over = True
                    death_sound.play()
                    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
                    enter_player_name()
                    best_times.append((player_name, elapsed_time))
                    best_times.sort(key=lambda x: x[1], reverse=True)
                    save_ranking()

        collected_power_ups = pygame.sprite.spritecollide(player, power_ups, True)
        for power_up in collected_power_ups:
            player.invulnerable = True
            player.invulnerable_start_time = pygame.time.get_ticks()

        if current_time - last_block_spawn_time >= block_spawn_timer:
            block_image = random.choice(block_images)
            game_object = GameObject(block_image)
            game_objects.add(game_object)
            last_block_spawn_time = current_time

        if current_time - last_coin_spawn_time >= coin_spawn_timer:
            coin = Coin()
            coins.add(coin)
            last_coin_spawn_time = current_time

        if current_time - last_power_up_spawn_time >= power_up_spawn_timer:
            power_up = PowerUp()
            power_ups.add(power_up)
            last_power_up_spawn_time = current_time

    if not show_ranking and not game_over:
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        time_text = font.render("Spielzeit: {:02d}:{:02d}".format(minutes, seconds), True, WHITE)
        screen.blit(time_text, (10, 10))

    if not show_ranking and not game_over:
        coins_text = font.render("Gesammelte Münzen: {}".format(player.collected_coins), True, WHITE)
        screen.blit(coins_text, (10, 50))

    extra_lives_text = font.render("Extra-Leben: {}".format(player.extra_lives), True, WHITE)
    screen.blit(extra_lives_text, (10, 90))

    if game_over:
        game_over_text = font.render("Spiel vorbei!", True, BLUE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(game_over_text, game_over_rect)

        restart_button = font.render("Neustart", True, BLUE)
        restart_button_rect = restart_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        pygame.draw.rect(screen, BLUE, restart_button_rect, 2)
        screen.blit(restart_button, restart_button_rect)

        if len(best_times) > 0:
            rank_text = font.render("Bestzeiten:", True, BLUE)
            screen.blit(rank_text, (10, 100))
            for i, (name, time) in enumerate(best_times):
                rank = font.render("{}. {} - {:.2f} Sekunden".format(i + 1, name, time), True, WHITE)
                screen.blit(rank, (10, 100 + (i + 1) * 30))

    pygame.display.flip()
    clock.tick(60)


save_ranking()


pygame.quit()
