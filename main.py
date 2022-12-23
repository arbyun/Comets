"""''''''''
''IMPORTS''
''''''''"""
import math
import time
import random

import pygame.time

from end_screen import *

'''''''''''''''''
'PYGAME CONFIGS''
'''''''''''''''''

pygame.init()
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Comets")
timer = 0

ends_active = False

# Shop upgrades
moredmg = False
dmgamount = 0
buyable = True
speedtimer = False
SPEED_BOOST_EVENT = pygame.USEREVENT + 1
speed_boost_duration = 10000

# Now the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CRIMSON = (220, 20, 60)
CYAN = (0, 255, 255)
PASTEL_YELLOW = (255, 255, 153)
NIGHT_SKY_BLUE = (25, 35, 63)

'''''''''''''''''
'LETS MAKE MUSIC'
'''''''''''''''''

# pygame.mixer.init()

# Types of sounds
# 1 - Explosion
# 2 - Bullet
# 3 - Music
# 4 - Game Over
# 5 - Buy
# 6 - Error

M_1 = pygame.mixer.Sound("sounds/explosion.wav")
M_2 = pygame.mixer.Sound("sounds/bullet.wav")
M_3 = pygame.mixer.Sound("sounds/music.wav")
M_4 = pygame.mixer.Sound("sounds/game_over.wav")
M_5 = pygame.mixer.Sound("sounds/buy.wav")
M_6 = pygame.mixer.Sound("sounds/error.wav")

# Play the music 3
M_3.play(-1)

''''''''''''''''''''
'COLLISION CHECKER'
''''''''''''''''''''


# Making a personal collision function
# A better collision checker method because pygame.sprite.collide_rect() is not working and IS driving me mad
def check_collision(rect, circle):
    # Calculate the distance between the center of the rectangle and the center of the circle
    dx = circle.x - rect.x - rect.size / 2
    dy = circle.y - rect.y - rect.size / 2

    # If the distance is less than the radius of the circle, there is a collision
    if dx ** 2 + dy ** 2 < circle.radius ** 2:
        return True
    else:
        return False


'''''''''
'CLASSES'
'''''''''


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.color = CYAN
        self.image = pygame.draw.polygon(screen, self.color, ((x + 20, y + 40), (x, y), (x - 20, y + 40)))
        self.midvertice = (x, y)
        self.x = x
        self.y = y
        self.health = 1
        self.size = 50
        self.speed = 5
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.rect.x = self.x
        self.rect.y = self.y
        self.protected = False
        self.aoe = False

    def update(self):
        global speedtimer

        self.rect.x = self.x
        self.rect.y = self.y

        if self.health == 1:
            self.color = CYAN

        if self.protected:
            self.health = 2
            self.color = PASTEL_YELLOW
        else:
            self.health = 1
            self.color = CYAN

    def draw(self):
        self.image = pygame.draw.polygon(screen, self.color,
                                         ((self.x + 20, self.y + 40), (self.x, self.y), (self.x - 20, self.y + 40)))
        self.update()


class Bullet(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.size = 5
        self.image = pygame.draw.line(screen, (255, 255, 255), (x, y), (x, y - self.size), self.size)
        self.speed = 10
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.size
        self.rect.height = self.size
        bullet_group.add(self)

    def update(self):
        self.y -= self.speed
        self.rect.y -= self.speed

    def draw(self):
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (self.x, self.y - self.size), self.size)
        self.update()


class Comet(pygame.sprite.Sprite):
    def __init__(self, x, y, ctype):
        super().__init__()

        self.ctype = ctype

        if ctype == "BIG":
            self.size = 50
            self.speed = 2
            self.health = 3
        if ctype == "MEDIUM":
            self.size = 30
            self.speed = 4
            self.health = 2
        if ctype == "SMALL":
            self.size = 10
            self.speed = 6
            self.health = 1

        self.radius = self.size
        self.color = (255, 255, 255)
        self.image = pygame.draw.circle(screen, self.color, (x, y), self.radius)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.size
        self.rect.height = self.size
        comet_group.add(self)

    def update(self):
        self.y += self.speed

        # Update the comet's rect to match its new position
        self.rect.y = self.y
        self.rect.x = self.x

        if self.y < 0 or self.rect.y > window_size[1]:
            self.kill()

        # if self.rect.colliderect(player.rect):
        #    self.kill()
        #    player.kill()
        #    screen.fill(BLACK)
        #    ending_screen()

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        self.update()


'''''''''''''''''''''''
'CREATING THE OBJECTS''
'''''''''''''''''''''''

possible_difficulties = ["BEGINNER", "EASY", "MEDIUM", "HARD", "INSANE", "IMPOSSIBLE"]
difficulty_level = possible_difficulties[0]
level = 0

all_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
comet_group = pygame.sprite.Group()

# Create the player in the middle of the screen and 3/4 of the way down
if difficulty_level == "IMPOSSIBLE":
    player = Player(800, 850)
else:
    player = Player(400, 450)

all_sprites.add(player)

comet_sizes = ["BIG", "MEDIUM", "SMALL"]
comets = []
bullets = []
comet_spawn_interval = 0

# Set the maximum number of big comets on the screen
max_comets = 1 + level
clock = pygame.time.Clock()
maingame = True
score = 2000

font = pygame.font.Font(None, 36)
font_color = WHITE
bg_color = NIGHT_SKY_BLUE
text_pos = (10, 10)

'''''''''''
'FUNCTIONS'
'''''''''''


def set_difficulty_level():
    global difficulty_level
    global comet_spawn_interval
    global level
    if difficulty_level == "BEGINNER":
        comet_spawn_interval = 100
        level = 0
        return comet_spawn_interval
    if difficulty_level == "EASY":
        comet_spawn_interval = 100
        level = 1
        return comet_spawn_interval
    if difficulty_level == "MEDIUM":
        comet_spawn_interval = 80
        level = 4
        return comet_spawn_interval
    if difficulty_level == "HARD":
        comet_spawn_interval = 60
        level = 7
        return comet_spawn_interval
    if difficulty_level == "INSANE":
        comet_spawn_interval = 40
        level = 10
        return comet_spawn_interval
    if difficulty_level == "IMPOSSIBLE":
        comet_spawn_interval = 20
        level = 13
        return comet_spawn_interval


def are_comets_in_the_screen():
    for comet in comets:
        if comet.y < window_size[1]:
            return True
    return False


def comet_death(comet):
    global score
    if comet.ctype == "BIG":
        score += 100
        # Create 3 medium comets that spawn randomly
        for i in range(3):
            comets.append(Comet(comet.x + random.randint(-50, 50), comet.y + random.randint(-50, 50), "MEDIUM"))
    elif comet.ctype == "MEDIUM":
        score += 50
        # Create 6 small comets that shoot from the medium comet
        for i in range(6):
            comets.append(Comet(comet.x + random.randint(-350, 350), comet.y + random.randint(-50, 50), "SMALL"))
    elif comet.ctype == "SMALL":
        score += 20
        # Destroy
        pass


def ending_screen():
    global score
    global gobacktoms
    global ends_active
    global maingame

    # Stop the M_3 music
    pygame.mixer.music.stop()
    # Play the game over sound
    M_4.play()
    maingame = False
    # Draw the "Game Over" text on the screen
    screen.fill(BLACK)
    draw_game_over()
    time.sleep(1)
    text = get_username().upper()
    save_high_score(f"{text}, {score}")
    time.sleep(1)
    get_score()
    # Reset the score
    score = 0

    screen.fill((0, 0, 0))
    pygame.display.flip()
    draw_leaderboard()  # Draw the leaderboard
    time.sleep(2)
    # Clear the screen again3
    screen.fill((0, 0, 0))
    ends_active = False
    pass


def handle_speed_boost_event(event, player):
    player.speed = player.speed * 2


'''''''''''
'GAME LOOP'
'''''''''''

paused = False

while maingame:
    ms_active = True
    clock.tick(60)
    timer += 1
    comet_spawn_interval -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ms_active = False
            maingame = False
        if event.type == SPEED_BOOST_EVENT:
            handle_speed_boost_event(event, player)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                newbullet = Bullet(player.x, player.y)
                all_sprites.add(newbullet)
                bullet_group.add(newbullet)
                bullets.append(newbullet)
            if event.key == pygame.K_p:
                paused = True

    if speedtimer:
        custom_event = pygame.event.Event(SPEED_BOOST_EVENT)
        pygame.event.post(custom_event)
        pygame.time.set_timer(SPEED_BOOST_EVENT, speed_boost_duration)
        speedtimer = False

    ''''''''''''
    'GAME PAUSE'
    ''''''''''''

    if paused:
        screen.fill((0, 0, 0))
        options = [("Activate a yellow shield", 500), ("Get your speed doubled for 10 seconds", 750), ("Permanently "
                                                                                                       "double your "
                                                                                                       "speed",
                                                                                                       1000),
                   ("Increase your damage by 1", 1500), ("Change weapon firing mode to AOE", 2000)]
        opt_x = 50
        opt_y = 100
        opt_font = pygame.font.Font(None, 26)
        canbuy = WHITE
        cantbuy = (128, 128, 128)
        selected_color = (0, 0, 255)
        selected_option = 0

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                    elif event.key == pygame.K_p:
                        paused = False
                    elif event.key == pygame.K_UP:
                        selected_option = max(0, selected_option - 1)
                    elif event.key == pygame.K_DOWN:
                        selected_option = min(len(options) - 1 + 1, selected_option + 1)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            if score >= options[0][1]:
                                player.protected = True
                                score -= options[0][1]
                                M_5.play()
                            else:
                                M_6.play()
                        elif selected_option == 1:
                            if score >= options[1][1]:
                                speedtimer = True
                                score -= options[1][1]
                                M_5.play()
                            else:
                                M_6.play()
                        elif selected_option == 2:
                            if buyable:
                                if score >= options[2][1]:
                                    player.speed *= 2
                                    score -= options[2][1]
                                    buyable = False
                                    M_5.play()
                                else:
                                    M_6.play()
                            else:
                                M_6.play()
                        elif selected_option == 3:
                            if score >= options[3][1]:
                                moredmg = True
                                dmgamount += 1
                                score -= options[3][1]
                                M_5.play()
                            else:
                                M_6.play()
                        elif selected_option == 4:
                            if score >= options[4][1]:
                                player.aoe = True
                                score -= options[4][1]
                                M_5.play()
                            else:
                                M_6.play()

            pause_screen = pygame.display.set_mode((800, 600))
            screen.blit(pause_screen, (0, 0))
            screen.fill((0, 0, 0))
            paused_text = font.render("PAUSED", True, WHITE)
            welcome_text = font.render("Welcome to the shop!", True, WHITE)
            # Center the text on the top of the screen
            paused_text_rect = paused_text.get_rect()
            paused_text_rect.centerx = screen.get_rect().centerx
            paused_text_rect.y = 10
            welcome_text_rect = welcome_text.get_rect()
            welcome_text_rect.centerx = screen.get_rect().centerx
            welcome_text_rect.y = 50
            screen.blit(paused_text, paused_text_rect)
            screen.blit(welcome_text, welcome_text_rect)

            for i in range(len(options)):
                if i == selected_option:
                    color = selected_color
                else:
                    if score >= options[i][1]:
                        color = canbuy
                    else:
                        color = cantbuy

                text = opt_font.render(options[i][0], True, color)
                # Blit the text after the welcome text
                text_rect = text.get_rect()
                text_rect.x = opt_x
                text_rect.y = opt_y + (i * 50)
                screen.blit(text, text_rect)
                # Draw the price
                price = opt_font.render(str(options[i][1]), True, color)
                price_rect = price.get_rect()
                price_rect.x = opt_x + 350
                price_rect.y = opt_y + (i * 50)
                screen.blit(price, price_rect)
                # If can buy, draw the buy button, else draw the can't buy button
                if options[i][1] <= score:
                    buy = opt_font.render("BUY", True, color)
                    buy_rect = buy.get_rect()
                    buy_rect.x = opt_x + 450
                    buy_rect.y = opt_y + (i * 50)
                    screen.blit(buy, buy_rect)
                else:
                    notenough = opt_font.render("Score isn't high enough", True, color)
                    notenough_rect = notenough.get_rect()
                    notenough_rect.x = opt_x + 450
                    notenough_rect.y = opt_y + (i * 50)
                    screen.blit(notenough, notenough_rect)
            pygame.display.flip()

    '''''''''''''''''
    'PLAYER CONTROLS'
    '''''''''''''''''

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player.speed
    if keys[pygame.K_RIGHT]:
        player.x += player.speed
    if keys[pygame.K_UP]:
        player.y -= player.speed
    if keys[pygame.K_DOWN]:
        player.y += player.speed

    for b in bullets:
        b.update()
        if b.y < 0:
            bullets.remove(b)

    screen.fill(bg_color)

    # draw scene
    for b in bullets:
        b.draw()

    # make the player warp upon reaching the edge of the screen
    if player.x > window_size[0]:
        player.x = 0
    elif player.x < 0:
        player.x = window_size[0]
    elif player.y > window_size[1]:
        player.y = 0
    elif player.y < 0:
        player.y = window_size[1]

    # spawn comet on top of the screen with random x position and based on the difficulty level and based if the
    # spawn interval has passed
    if (are_comets_in_the_screen() is False) and comet_spawn_interval <= 0:
        # Spawn x number of comets based on the max_comets variable
        for i in range(max_comets):
            if difficulty_level == "BEGINNER":
                # Spawn either a small or medium comet
                comet_type = random.choice(comet_sizes[1:])
            elif difficulty_level == "EASY":
                # Spawn either a small, medium, or big comet
                comet_type = random.choice(comet_sizes)
            elif difficulty_level == "MEDIUM":
                # Spawn either a small, medium, or big comet
                comet_type = random.choice(comet_sizes)
            elif difficulty_level == "HARD":
                # Spawn either a medium or big comet
                comet_type = random.choice(comet_sizes[1:])
            elif difficulty_level == "INSANE":
                # Spawn either a medium or big comet
                comet_type = random.choice(comet_sizes[1:])
            elif difficulty_level == "IMPOSSIBLE":
                # Spawn a big comet
                comet_type = comet_sizes[0]
            comet = Comet(random.randint(0, window_size[0]), 1, comet_type)
            comets.append(comet)
            all_sprites.add(comet)
            comet_group.add(comet)
            # Set the spawn interval based on the difficulty
        comet_spawn_interval = set_difficulty_level()

    '''''''''''''''''''''
    'INCREASE DIFFICULTY'
    '''''''''''''''''''''

    if score >= 500 or timer >= 10000:
        difficulty_level = "EASY"
    if score >= 1000 or timer >= 100000:
        difficulty_level = "MEDIUM"
    if score >= 3000 or timer >= 300000:
        difficulty_level = "HARD"
    if score >= 5000 or timer >= 400000:
        difficulty_level = "INSANE"
    if score >= 8000 or timer >= 500000:
        difficulty_level = "IMPOSSIBLE"

    ''''''''''''
    'COLLISIONS'
    ''''''''''''

    if pygame.sprite.spritecollide(player, comet_group, False):
        if player.protected:
            comet_group.remove(comet)
            player.protected = False
        else:
            player.health -= 1

    if player.health <= 0:
        # Game over
        # Show the game over screen
        ms_active = False
        ends_active = True
        for c in comets:
            c.kill()
        for b in bullets:
            b.kill()
        comets.clear()
        bullets.clear()

    if ends_active is True:
        ending_screen()
        ends_active = False

    for comet in comets:
        for bullet in bullets:
            if check_collision(bullet, comet):
                if player.aoe:
                    # If the player has the aoe upgrade, then kill all comets in the aoe radius
                    aoe_radius = 400
                    for obj in comets:
                        # Calculate the distance between the object and the bullet
                        distance = math.sqrt((math.pow(obj.x - bullet.x, 2)) + (math.pow(obj.y - bullet.y, 2)))

                        if distance <= aoe_radius:
                            obj.health -= 1
                if moredmg:
                    comet.health -= dmgamount
                else:
                    comet.health -= 1
                if comet.health <= 0:
                    M_1.play()
                    comet_death(comet)
                    comet.kill()
                    comets.remove(comet)
                else:
                    M_2.play()
                    bullets.remove(bullet)
                    score += 10

    ''''''
    'DRAW'
    ''''''

    screen.fill(bg_color)
    player.draw()

    for comet in comets:
        comet.draw()

    for bullet in bullets:
        bullet.draw()

    score_text = font.render(str(score), True, font_color)
    screen.blit(score_text, text_pos)

    pygame.display.flip()

pygame.quit()
