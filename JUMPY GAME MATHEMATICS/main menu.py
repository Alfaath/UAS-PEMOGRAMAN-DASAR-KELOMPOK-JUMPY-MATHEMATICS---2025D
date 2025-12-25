import pygame
import sys
import random

pygame.init()

# ============================================================
# SETTINGS
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 658
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jumpy Game Mathematics")

clock = pygame.time.Clock()
FPS = 60

# ============================================================
# BACKGROUND
menu_bg = pygame.image.load("assets/MAIN2.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

stage_bg = pygame.image.load("assets/stage1.png").convert()
stage_bg = pygame.transform.scale(stage_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# ============================================================
# BUTTON MENU
start_button = pygame.Rect(474, 322, 330, 90)
quit_button  = pygame.Rect(474, 430, 330, 90)

# ============================================================
# LEVEL BUTTONS DI STAGE
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
    8: pygame.Rect(753, 350, button_w, button_h)  # dikunci
}

# ============================================================
# POPUP PYGAME (GANTI TKINTER)
def popup_locked():
    font = pygame.font.Font(None, 48)
    text1 = font.render("SEE YOU SOON!", True, (255, 255, 255))
    text2 = font.render("Selesaikan misinya, dan nantikan proyek selanjutnya!", True, (255, 255, 255))

    # semi transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))

    screen.blit(overlay, (0, 0))
    screen.blit(text1, (SCREEN_WIDTH//2 - text1.get_width()//2, 240))
    screen.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, 300))
    pygame.display.update()

    # tunggu klik atau tombol apapun
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


# ============================================================
# START LEVEL
def start_level(n):
    print(f"Masuk ke Level {n}!")
    # nanti diisi game level
    # sementara bikin layar hitam + tulisan
    running = True
    font = pygame.font.Font(None, 70)
    text = font.render(f"LEVEL {n}", True, (255, 255, 255))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                running = False

        screen.fill((0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2,
                           SCREEN_HEIGHT//2 - text.get_height()//2))
        pygame.display.update()
        clock.tick(FPS)


# ============================================================
# MAIN MENU
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    return "stage"
                if quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.blit(menu_bg, (0, 0))
        pygame.display.update()


# ============================================================
# STAGE SCREEN
def stage_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for number, rect in level_buttons.items():
                    if rect.collidepoint(event.pos):
                        if number <= 7:
                            start_level(number)
                        else:
                            popup_locked()

        screen.blit(stage_bg, (0, 0))
        pygame.display.update()


# ============================================================
# PROGRAM START
state = main_menu()

if state == "stage":
    stage_screen()
