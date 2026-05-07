import pygame
import time
import sys
import random

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((700, 350))

run = True

pygame.display.set_caption("Cat's adventure")

lose = pygame.font.Font('fonts/Roboto_Condensed-Black.ttf', 30)
lost = lose.render("Game Over", False, 'black')

win_font = pygame.font.Font('fonts/Roboto_Condensed-Black.ttf', 40)
win_text = win_font.render("BOSS DEFEATED! YOU WIN!", False, 'Green')

rest = pygame.font.Font('fonts/Roboto_Condensed-Black.ttf', 30)
restart = rest.render("Restart", False, 'yellow')
restrect = restart.get_rect(topleft=(275, 150))

icon = pygame.image.load('images/img.png')
pygame.display.set_icon(icon)

player = pygame.image.load('images/img.png')
player = pygame.transform.scale(player, (50, 50))
speed = 10
playerx = 100
playery = 250

isjump = False
jump = 7

bg = pygame.image.load('images/bg.png')
bgx = 0

enemy = pygame.image.load('images/enemy.png')
enemy = pygame.transform.scale(enemy, (50, 50))

flying_enemy = pygame.image.load('images/enemy.png')
flying_enemy = pygame.transform.scale(flying_enemy, (50, 50))

boss = pygame.image.load('images/enemy.png')
boss = pygame.transform.scale(boss, (100, 100))

enemy_list_in_game = []
flying_enemy_list_in_game = []

boss_active = False
boss_health = 10
boss_x = 600
boss_y = 150
boss_speed = 3
boss_direction = 1

enemytime = pygame.USEREVENT + 1
pygame.time.set_timer(enemytime, 1500)

flying_enemy_timer_event = pygame.USEREVENT + 3
pygame.time.set_timer(flying_enemy_timer_event, 2000)

score_timer_event = pygame.USEREVENT + 2
pygame.time.set_timer(score_timer_event, 1000)

bullet = pygame.image.load('images/bullet.png')
bullet = pygame.transform.scale(bullet, (25, 25))
bullets = []

cau = pygame.font.Font('fonts/Roboto_Condensed-Black.ttf', 20)
caution = cau.render("Одномоментно есть только 2 пули!", False, 'Red')

score = 0
co = pygame.font.Font('fonts/Roboto_Condensed-Black.ttf', 20)
cou = co.render(f'Score: {score}', False, 'black')
gameplay = True

game_won = False

while run:
    clock.tick(20)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullets.append(bullet.get_rect(topleft=(playerx + 30, playery + 10)))
        if event.type == pygame.QUIT:
            run = False

        if gameplay and event.type == enemytime and score < 500 and not boss_active:
            enemy_list_in_game.append(enemy.get_rect(topleft=(600, 250)))

        if gameplay and event.type == score_timer_event:
            score += 1
            cou = co.render(f'Score: {score}', False, 'black')

            if score >= 500 and not boss_active and not game_won:
                boss_active = True
                enemy_list_in_game.clear()
                flying_enemy_list_in_game.clear()

        if gameplay and event.type == flying_enemy_timer_event and 100 <= score < 500 and not boss_active:
            flying_height = random.randint(100, 150)
            flying_enemy_list_in_game.append({
                'rect': flying_enemy.get_rect(topleft=(600, flying_height)),
                'speed': random.randint(15, 25)
            })

    if not run:
        break

    screen.blit(bg, (bgx, 0))
    screen.blit(bg, (bgx + 700, 0))
    screen.blit(caution, (200, 50))
    screen.blit(cou, (10, 10))

    if 100 <= score < 500:
        flying_warning = cau.render("Осторожно! Появились летающие враги!", False, 'Orange')
        screen.blit(flying_warning, (150, 80))

    if score >= 500 and not game_won:
        boss_warning = cau.render("ФИНАЛЬНЫЙ БОСС!", False, 'Red')
        screen.blit(boss_warning, (250, 80))

        boss_health_text = cau.render(f"Здоровье босса: {boss_health}", False, 'White')
        screen.blit(boss_health_text, (250, 110))

    if gameplay and not game_won:
        screen.blit(player, (playerx, playery))

        playerrect = player.get_rect(topleft=(playerx, playery))

        if enemy_list_in_game and score < 500:
            for (i, el) in enumerate(enemy_list_in_game):
                screen.blit(enemy, el)
                el.x -= 25
                if el.x < -10:
                    enemy_list_in_game.pop(i)

                if playerrect.colliderect(el):
                    gameplay = False

        if flying_enemy_list_in_game and 100 <= score < 500:
            for (i, flying_enemy_data) in enumerate(flying_enemy_list_in_game):
                el = flying_enemy_data['rect']
                enemy_speed = flying_enemy_data['speed']
                screen.blit(flying_enemy, el)
                el.x -= enemy_speed

                if el.x < -10:
                    flying_enemy_list_in_game.pop(i)
                    continue

                if playerrect.colliderect(el):
                    gameplay = False

        if boss_active and not game_won:
            screen.blit(boss, (boss_x, boss_y))
            boss_rect = boss.get_rect(topleft=(boss_x, boss_y))

            boss_y += boss_speed * boss_direction

            if boss_y <= 50:
                boss_direction = 1
            elif boss_y >= 250:
                boss_direction = -1

            boss_x -= 1

            if playerrect.colliderect(boss_rect):
                gameplay = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and playerx > 50:
            playerx -= speed
        elif keys[pygame.K_d] and playerx < 600:
            playerx += speed

        if not isjump:
            if keys[pygame.K_SPACE]:
                isjump = True
        else:
            if jump >= -7:
                if jump > 0:
                    playery -= (jump ** 2) / 2
                else:
                    playery += (jump ** 2) / 2
                jump -= 1
            else:
                isjump = False
                jump = 7

        bgx -= 2
        if bgx == -700:
            bgx = 0

        if bullets and len(bullets) < 3:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 15
                if el.x > 700:
                    bullets.pop(i)

                if enemy_list_in_game and score < 500:
                    for (index, en) in enumerate(enemy_list_in_game):
                        if el.colliderect(en):
                            enemy_list_in_game.pop(index)
                            bullets.pop(i)
                            score += 5
                            cou = co.render(f'Score: {score}', False, 'black')
                            break

                if flying_enemy_list_in_game and 100 <= score < 500:
                    for (index, flying_enemy_data) in enumerate(flying_enemy_list_in_game):
                        if el.colliderect(flying_enemy_data['rect']):
                            flying_enemy_list_in_game.pop(index)
                            bullets.pop(i)
                            score += 10
                            cou = co.render(f'Score: {score}', False, 'black')
                            break

                if boss_active and not game_won:
                    boss_rect = boss.get_rect(topleft=(boss_x, boss_y))
                    if el.colliderect(boss_rect):
                        bullets.pop(i)
                        boss_health -= 1

                        if boss_health <= 0:
                            game_won = True
                            boss_active = False
                            score += 100
                            cou = co.render(f'Score: {score}', False, 'black')
                        break

    elif game_won:
        screen.fill((50, 200, 50))
        screen.blit(win_text, (100, 100))
        screen.blit(restart, restrect)
        mouse = pygame.mouse.get_pos()
        if restrect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            game_won = False
            boss_active = False
            playerx = 100
            enemy_list_in_game.clear()
            flying_enemy_list_in_game.clear()
            bullets.clear()
            score = 0
            boss_health = 10
            boss_x = 600
            boss_y = 150
            cou = co.render(f'Score: {score}', False, 'black')

    else:
        screen.fill((250, 2, 2))
        screen.blit(lost, (250, 50))
        screen.blit(restart, restrect)
        mouse = pygame.mouse.get_pos()
        if restrect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            game_won = False
            boss_active = False
            playerx = 100
            enemy_list_in_game.clear()
            flying_enemy_list_in_game.clear()
            bullets.clear()
            score = 0
            boss_health = 10
            boss_x = 600
            boss_y = 150
            cou = co.render(f'Score: {score}', False, 'black')

    pygame.display.flip()

pygame.quit()
sys.exit()
