import pygame
import sys
import random
import os
from pygame import mixer

pygame.init()
mixer.init()

#SOUND
mixer.music.load("assets/snd.mp3")
mixer.music.set_volume(0.9)
mixer.music.play(-1)
# SETTINGS
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 658
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumpy Game Mathematics")
clock = pygame.time.Clock()
FPS = 60

# LOADING SCREEN 
def loading_screen_character():
    font = pygame.font.SysFont("None", 30)

    loading_bg = pygame.transform.scale(
        pygame.image.load("assets/bgloading.png").convert(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    character = pygame.transform.scale(
        pygame.image.load("assets/frame21.png").convert_alpha(),
        (55, 55)
    )

    jump_fx = pygame.mixer.Sound("assets/jumpsnd.mp3")
    jump_fx.set_volume(0.6)

    #SETINGAN BARNYA
    bar_width = 680
    bar_height = 20
    bar_x = SCREEN_WIDTH//2 - bar_width//2
    bar_y = SCREEN_HEIGHT//2 + 120

    #KARAKTER POSISI AWAL
    char_y_base = bar_y - 60
    char_x = bar_x

    #LOGIKA LOMPAT
    jump_offset = 0
    velocity = -8
    gravity = 0.6
    jump_fx.play()

    start_time = pygame.time.get_ticks()
    duration = 4000  # 4 detik loading

    while True:
        clock.tick(FPS)
        elapsed = pygame.time.get_ticks() - start_time
        progress = min(elapsed / duration, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #posisi karakter
        char_x = bar_x + int(bar_width * progress) - 25
        char_x = max(bar_x, min(char_x, bar_x + bar_width - 55))

        #biar loncat terus
        velocity += gravity
        jump_offset += velocity
        if jump_offset > 0:
            jump_offset = 0
            velocity = -8

        #DRAW
        screen.blit(loading_bg, (0, 0))

        pygame.draw.rect(
            screen, (60,60,60),
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=12
        )
        pygame.draw.rect(
            screen, (0,200,120),
            (bar_x, bar_y, int(bar_width * progress), bar_height),
            border_radius=12
        )

        #karakter jalan + lompat ngikut loadingnya
        screen.blit(
            character,
            (char_x, char_y_base + jump_offset)
        )

        pygame.display.update()

        if elapsed >= duration:
            break
        
loading_screen_character()

# BACKGROUND
menu_bg = pygame.image.load("assets/MAIN2.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
stage_bg = pygame.image.load("assets/stage1.png").convert()
stage_bg = pygame.transform.scale(stage_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
# BUTTON MENU
start_button = pygame.Rect(474, 322, 330, 90)
quit_button  = pygame.Rect(474, 430, 330, 90)
# LEVEL BUTTONS
button_w = 56
button_h = 76
level_buttons = {
    1: pygame.Rect(470, 260, button_w, button_h),
    2: pygame.Rect(564, 260, button_w, button_h),
    3: pygame.Rect(660, 260, button_w, button_h),
    4: pygame.Rect(755, 260, button_w, button_h),
    5: pygame.Rect(468, 350, button_w, button_h),
    6: pygame.Rect(563, 350, button_w, button_h),
    7: pygame.Rect(657, 350, button_w, button_h),
    8: pygame.Rect(753, 350, button_w, button_h)  
}
# SKOR MINIMAL UNTUK MEMBUKA LEVEL
min_score_to_unlock = {
    2: 100,
    3: 120,
    4: 150,
    5: 200,
    6: 250,
    7: 300,
    8: 350
}
last_score = 0
# POPUP LEVEL LOCKED
def popup_locked(message="SEE YOU SOON!"):
    font = pygame.font.Font(None, 48)
    text1 = font.render(message, True, (255, 255, 255))
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0,0))
    screen.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, SCREEN_HEIGHT//2))
    pygame.display.update()
    pygame.time.delay(1500)

def generate_math_question(level):
    if level <= 2:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(["+", "-"])
        answer = a + b if op == "+" else a - b
        question = f"{a} {op} {b}"

    elif level <= 4:
        b = random.randint(2, 10)
        a = random.randint(2, 10) * b
        op = random.choice(["×", "÷"])
        if op == "×":
            answer = a * b
            question = f"{a} × {b}"
        else:
            answer = a // b
            question = f"{a} ÷ {b}"

    else:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        c = random.randint(1, 5)
        answer = a + b * c
        question = f"{a} + {b} × {c}"

    return question, answer

def popup_math_question(level):
    font = pygame.font.Font(None, 40)
    input_font = pygame.font.Font(None, 36)

    question_text, correct = generate_math_question(level)
    user_input = ""

    while True:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        q = font.render(f"Jawab soal dulu: {question_text} = ?", True, (255,255,255))
        ans = input_font.render(user_input, True, (255,255,0))
        info = input_font.render("ENTER untuk submit", True, (200,200,200))

        screen.blit(q, (SCREEN_WIDTH//2 - q.get_width()//2, 220))
        screen.blit(ans, (SCREEN_WIDTH//2 - ans.get_width()//2, 280))
        screen.blit(info, (SCREEN_WIDTH//2 - info.get_width()//2, 330))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return user_input.isdigit() and int(user_input) == correct
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.unicode.isdigit():
                    user_input += event.unicode

# GAMEPLAY
def run_gameplay():
    global last_score
    pygame.display.set_caption("Jumpy Game")
    pygame.display.set_icon(pygame.image.load("assets/frame12.png"))
    jump_fx = pygame.mixer.Sound("assets/jumpsnd.mp3")
    death_fx = pygame.mixer.Sound("assets/deathsnd.mp3")
    SCROLL_THRESH = 200
    GRAVITY = 0.8
    MAX_PLATFORMS = 8
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    font_small = pygame.font.SysFont("Lucida Sans", 20)
    font_big = pygame.font.SysFont("Lucida Sans", 24)

    #ASSETS
    jumpy_image = pygame.image.load("assets/frame21.png").convert_alpha()
    bg_image = pygame.image.load("assets/background11.png").convert_alpha()
    platform_image = pygame.image.load("assets/platform.png").convert_alpha()

    #SOAL MATEMATIKA
def run_gameplay():
    global last_score

    jump_fx = pygame.mixer.Sound("assets/jumpsnd.mp3")
    death_fx = pygame.mixer.Sound("assets/deathsnd.mp3")

    SCROLL_THRESH = 200
    GRAVITY = 0.8
    MAX_PLATFORMS = 9

    WHITE = (255,255,255)
    BLACK = (0,0,0)

    font_small = pygame.font.SysFont("Lucida Sans", 20)
    font_big = pygame.font.SysFont("Lucida Sans", 26)

    jumpy_image = pygame.image.load("assets/frame21.png").convert_alpha()
    bg_image = pygame.image.load("assets/background11.png").convert_alpha()
    platform_image = pygame.image.load("assets/platform.png").convert_alpha()

    # ===== SOAL MATEMATIKA =====
    def generate_math():
        a = random.randint(1,5)
        b = random.randint(1,5)
        correct = a + b
        if random.random() < 0.7:
            return f"{a} + {b} = {correct}", True
        else:
            return f"{a} + {b} = {correct + random.choice([-1,1,2])}", False

    # ===== PLAYER =====
    class Player:
        def __init__(self, x, y):
            self.image = pygame.transform.scale(jumpy_image, (45,45))
            self.rect = self.image.get_rect(center=(x,y))
            self.vel_y = 0
            self.flip = False

        def move(self):
            dx, dy, scroll = 0, 0, 0
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                dx = -10
                self.flip = True
            if keys[pygame.K_d]:
                dx = 10
                self.flip = False

            self.vel_y += GRAVITY
            dy += self.vel_y

            for plat in platform_group:
                if plat.rect.colliderect(self.rect.x, self.rect.y+dy, self.rect.width, self.rect.height):
                    if self.vel_y > 0 and self.rect.bottom <= plat.rect.centery:
                        if not plat.safe:
                            death_fx.play()
                            return -1
                        self.rect.bottom = plat.rect.top
                        self.vel_y = -18
                        dy = 0
                        jump_fx.play()

            if self.rect.top <= SCROLL_THRESH and self.vel_y < 0:
                scroll = -dy

            self.rect.x += dx
            self.rect.y += dy + scroll
            return scroll

        def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    # ===== PLATFORM =====
    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y, w, kind="empty"):
            super().__init__()
            self.image = pygame.transform.scale(platform_image, (w,14))
            self.rect = self.image.get_rect(topleft=(x,y))
            self.kind = kind

            if kind == "question":
                self.text, self.safe = generate_math()
                self.moving = random.random() < 0.4
            else:
                self.text = ""
                self.safe = True
                self.moving = False

            self.direction = random.choice([-1,1])
            self.speed = 1

        def update(self, scroll):
            if self.moving:
                self.rect.x += self.direction * self.speed
                if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                    self.direction *= -1

            self.rect.y += scroll
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()

        def draw_text(self):
            if self.text:
                t = font_small.render(self.text, True, (0,0,0))
                screen.blit(t, (self.rect.centerx - t.get_width()//2, self.rect.top-18))

    # ===== INIT =====
    platform_group = pygame.sprite.Group()
    player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT-150)

    platform_group.add(
        Platform(SCREEN_WIDTH//2-60, SCREEN_HEIGHT-50, 120, "empty")
    )

    score = 0
    bg_scroll = 0
    game_over = False
    run = True

    # ===== GAME LOOP =====
    while run:
        clock.tick(FPS)

        if not game_over:
            scroll = player.move()
            if scroll == -1:
                game_over = True
                continue

            bg_scroll += scroll
            if abs(bg_scroll) >= bg_image.get_height():
                bg_scroll = 0

            screen.blit(bg_image, (0, bg_scroll))
            screen.blit(bg_image, (0, bg_scroll-bg_image.get_height()))

            # SPAWN PLATFORM
            if len(platform_group) < MAX_PLATFORMS:
                y = min(p.rect.y for p in platform_group) - random.randint(90,130)
                x = random.randint(50, SCREEN_WIDTH-150)

                kind = "empty" if random.random() < 0.6 else "question"
                platform_group.add(Platform(x,y,100,kind))

            platform_group.update(scroll)
            platform_group.draw(screen)
            for p in platform_group:
                p.draw_text()

            player.draw()

            if scroll > 0:
                score += scroll

            screen.blit(font_small.render(f"SCORE: {score}", True, WHITE), (10,10))

            if player.rect.top > SCREEN_HEIGHT:
                game_over = True
                death_fx.play()

        else:
            last_score = score
            screen.fill(BLACK)
            game_over_text = font_big.render("GAME OVER", True, WHITE)
            score_text = font_big.render(f"SCORE: {score}", True, WHITE)
            press_text = font_small.render("PRESS SPACE", True, WHITE)
            screen.blit(
                game_over_text,
                (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 270)
            )
            screen.blit(
                score_text,
                (SCREEN_WIDTH//2 - score_text.get_width()//2, 320)
            )
            screen.blit(
                press_text,
                (SCREEN_WIDTH//2 - press_text.get_width()//2, 370)
            )
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                return score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        pygame.display.update()

# MAIN MENU
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    return "stage"
                if quit_button.collidepoint(event.pos):
                    pygame.quit(); sys.exit()
        screen.blit(menu_bg, (0,0))
        pygame.display.update()
# STAGE SCREEN
def stage_screen():
    global last_score
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for number, rect in level_buttons.items():
                    if rect.collidepoint(event.pos):
                        if number == 8:
                            popup_locked("LEVEL 8 COMING SOON!")
                            continue
                        if number == 1:
                            last_score = run_gameplay()
                            continue
                        if number in min_score_to_unlock:
                            if last_score >= min_score_to_unlock[number]:
                                last_score = run_gameplay()
                            else:
                                if popup_math_question(number):
                                    last_score = run_gameplay()
                                else: 
                                    popup_locked("JAWABAN SALAH"
                    
                                )
        screen.blit(stage_bg, (0,0))
        pygame.display.update()
# PROGRAM START
state = "menu"
while True:
    if state == "menu":
        state = main_menu()
    elif state == "stage":
        state = stage_screen()