import pygame, Floor, Bird, Pipe, Score

# initialise critical parameters
pygame.mixer.init()
pygame.init()
APP_WIDTH = 512
APP_HEIGHT = 1024
window = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
clock = pygame.time.Clock()

# load visual assets and establish custom event timers
bg_day_img = pygame.transform.scale2x(pygame.image.load('Assets/Images/background-day.png')).convert_alpha()
bg_night_img = pygame.transform.scale2x(pygame.image.load('Assets/Images/background-night.png')).convert_alpha()

bird_downflap = pygame.transform.scale2x(pygame.image.load('Assets/Images/bluebird-downflap.png')).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load('Assets/Images/bluebird-midflap.png')).convert_alpha()
bird_upflap = pygame.transform.scale2x(pygame.image.load('Assets/Images/bluebird-upflap.png')).convert_alpha()
bird_sprites = [bird_downflap, bird_midflap, bird_upflap]
bird_sprites_hitboxes = [
    bird_upflap.get_rect(center=(APP_WIDTH / 3, APP_HEIGHT / 2)),
    bird_midflap.get_rect(center=(APP_WIDTH / 3, APP_HEIGHT / 2)),
    bird_upflap.get_rect(center=(APP_WIDTH / 3, APP_HEIGHT / 2))
]

BIRD_TRANSITION = pygame.USEREVENT
pygame.time.set_timer(BIRD_TRANSITION, 200)

bot_pipe_img = pygame.transform.scale2x(pygame.image.load('Assets/Images/pipe-green.png')).convert_alpha()
top_pipe_img = pygame.transform.flip(bot_pipe_img, False, True)
pipes = [Pipe.Pipe(bot_pipe_img, top_pipe_img)]
SPAWN_PIPE = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_PIPE, 1400)

floor_img = pygame.transform.scale2x(pygame.image.load('Assets/Images/base.png')).convert_alpha()
overview_img = pygame.transform.scale2x(pygame.image.load('Assets/Images/message.png')).convert_alpha()
overview_rect = overview_img.get_rect(center=(APP_WIDTH / 2, APP_HEIGHT / 2))

# load audio assets
flap_sound = pygame.mixer.Sound('Assets/Audio/sfx_wing.wav')
death_sound = pygame.mixer.Sound('Assets/Audio/sfx_hit.wav')
score_sound = pygame.mixer.Sound('Assets/Audio/sfx_point.wav')


def draw_window(window, floor, bird, score, game_active):
    window.blit(bg_night_img, (0, 0))
    floor.draw_floor(window)

    # if game_active:
    #     bird.draw_bird(window)
    #     [pipe.draw_pipe(window) for pipe in pipes]

    #floor.draw_floor(window)
    #score.display_score(window, game_active)

    # if not game_active:
    #     window.blit(overview_img, overview_rect)


def objects_move(floor, bird, game_active):
    floor.move()
    if game_active:
        bird.move()
        [pipe.move_pipe() for pipe in pipes]

def collision_detect(bird, pipes):
    if Pipe.Pipe.collision_detect(pipes, bird.current_hitbox) or bird.collide_check():
        return True
    return False

def points_check(bird, pipes, score, score_sound):
    if len(pipes) >= 1 and bird.current_hitbox.bottomleft[0] > pipes[0].bot_pipe_hitbox.bottomright[0] and pipes[0].passed == False:
        pipes[0].passed = True
        score.update_score()
        score_sound.play()

def start_game():
    # initialise objects
    running = True
    game_active = False
    floor = Floor.Floor(875, floor_img)
    bird = Bird.Bird(bird_sprites, bird_sprites_hitboxes)
    score = Score.Score(APP_HEIGHT, APP_WIDTH)

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and game_active:
            #         bird.flap()
            #         flap_sound.play()
            #     if event.key == pygame.K_SPACE and game_active == False:
            #         game_active = True
            #         bird.reset(APP_WIDTH / 3, APP_HEIGHT / 2)
            #         score.reset_score()
            # if event.type == SPAWN_PIPE and game_active:
            #     pipes.append(Pipe.Pipe(bot_pipe_img, top_pipe_img))
            # if event.type == BIRD_TRANSITION:
            #     bird.transition()

        #window.blit(bg_night_img, (0, 0))
        floor.draw_floor(window)
        #objects_move(floor, bird, game_active)
        #points_check(bird, pipes, score, score_sound)
        #Pipe.Pipe.remove_pipes(pipes, bird)
        #draw_window(window, floor, bird, score, game_active)

        # if collision_detect(bird, pipes) and game_active:
        #     death_sound.play()
        #     game_active = False
        #     pipes.clear()
        #     score.update_high_score()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()



start_game()
