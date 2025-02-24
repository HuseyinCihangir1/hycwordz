import pygame
import json
import random
import time

pygame.init()

# Ekran ayarlari
GENISLIK, YUKSEKLIK = 980, 720
screen = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Word Game")

# Font ayarlari
FONT = pygame.font.Font(None, 36)
FONT_BOLD = pygame.font.Font(None, 48)

def import_db():
    with open('words_db.json', 'r') as file:
        return json.load(file)

# Harf kontrol fonksiyonu
def harf_kontrol(user_word, correct_word):
    result = []
    for i in range(len(user_word)):
        if user_word[i] == correct_word[i]:
            result.append('green')
        else:
            result.append('red')
    return result

# Puzzle çizme fonksiyonu
def ciz_puzzle(surface, start_x, start_y, size, gap, letters, colors):
    start_x = (GENISLIK - (4 * size + 3 * gap)) // 2  # 4 harf için merkezi hizala
    size=70
    for i in range(4):  # 4 harfli kelime için sabit mazgallar
        x = start_x + i * (size + gap)
        y = start_y
        color = pygame.Color(colors[i]) if i < len(letters) else pygame.Color("gray")
        pygame.draw.rect(surface, color, (x, 3*y, size, size), border_radius=5)
        if i < len(letters):
            text_surface = FONT.render(letters[i], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(x + size // 4, y + size // 2))
            surface.blit(text_surface, text_rect)

def ciz_ust_baslik(surface):
    text_surface = FONT_BOLD.render("hycWordz", True, (42, 255, 255))
    text_rect = text_surface.get_rect(center=(GENISLIK // 2, 50))
    surface.blit(text_surface, text_rect)

def ciz_sayaç(surface, deneme_sayisi):
    text_surface = FONT.render(f"Trial count: {deneme_sayisi}", True, (255, 255, 255))
    surface.blit(text_surface, (25, YUKSEKLIK - 75))

def ciz_alt_yazi(surface):
    text_surface = FONT.render("*Find the correct word with letters*", True, (255, 255, 255))
    surface.blit(text_surface, (GENISLIK - 450, YUKSEKLIK - 75))

def ciz_tebrik_mesaji(surface, deneme_sayisi):
    text_surface = FONT_BOLD.render(f"Congrats! Score: {deneme_sayisi}", True, (0, 255, 0))
    text_rect = text_surface.get_rect(center=(GENISLIK // 2, YUKSEKLIK // 2))
    surface.blit(text_surface, text_rect)

def ciz_try_again_butonu():
    button_rect = pygame.Rect(GENISLIK // 2 - 60, YUKSEKLIK // 2 + 50, 120, 40)
    pygame.draw.rect(screen, (0, 255, 0), button_rect, border_radius=5)
    text_surface = FONT.render("Try Again", True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def baslat():
    data = import_db()
    correct_word = random.choice(data["wordz"])
    print("Correct word:", correct_word)

    user_word = []
    colors = ['gray'] * 4  # Başlangıçta kutular gri
    deneme_sayisi = 0
    yanlis_harf_zamani = None
    running = True
    kazandi = False

    while running:
        screen.fill((50, 50, 50))  # background color
        
        ciz_ust_baslik(screen)
        ciz_sayaç(screen, deneme_sayisi)
        ciz_alt_yazi(screen)
        ciz_puzzle(screen, 100, 100, 50, 10, user_word, colors)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not kazandi:
                if event.unicode.isalpha() and len(user_word) < 4:
                    user_word.append(event.unicode.upper())
                if len(user_word) == 4:
                    colors = harf_kontrol("".join(user_word), correct_word)
                    deneme_sayisi += 1
                    if "".join(user_word) == correct_word:
                        kazandi = True
                    else:
                        yanlis_harf_zamani = time.time()
                    user_word = []
            elif event.type == pygame.MOUSEBUTTONDOWN and kazandi:
                x, y = event.pos
                if try_again_button.collidepoint(x, y):
                    baslat()
                    return

        if yanlis_harf_zamani and time.time() - yanlis_harf_zamani > 1.5:
            colors = ['gray'] * 4
            yanlis_harf_zamani = None

        if kazandi:
            ciz_tebrik_mesaji(screen, deneme_sayisi)
            try_again_button = ciz_try_again_butonu()

        pygame.display.flip()
    
    pygame.quit()

baslat()
