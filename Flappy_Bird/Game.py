import pygame, Bird, Floor, Pipe, Score, os, neat

pygame.mixer.init()
pygame.init()

APP_WIDTH = 450
APP_HEIGHT = 850
window = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
clock = pygame.time.Clock()

# load visual assets
bg_night_img = pygame.transform.scale2x(pygame.image.load('Assets/Images/background-night.png')).convert_alpha()
floor_img = pygame.transform.scale2x(pygame.image.load('Assets/Images/base.png')).convert_alpha()
bird_downflap = pygame.transform.scale2x(pygame.image.load('Assets/Images/bluebird-downflap.png')).convert_alpha()
bird_midflap = pygame.transform.scale2x(pygame.image.load('Assets/Images/bluebird-midflap.png')).convert_alpha()
bird_upflap = pygame.transform.scale2x(pygame.image.load('Assets/Images/bluebird-upflap.png')).convert_alpha()
bird_sprites = [bird_downflap, bird_midflap, bird_upflap]
bot_pipe_img = pygame.transform.scale2x(pygame.image.load('Assets/Images/pipe-green.png')).convert_alpha()
top_pipe_img = pygame.transform.flip(bot_pipe_img, False, True)

# custom events to determine bird sprite transition speed
BIRD_TRANSITION = pygame.USEREVENT
pygame.time.set_timer(BIRD_TRANSITION, 200)

# load audio assets
flap_sound = pygame.mixer.Sound('Assets/Audio/sfx_wing.wav')
death_sound = pygame.mixer.Sound('Assets/Audio/sfx_hit.wav')
score_sound = pygame.mixer.Sound('Assets/Audio/sfx_point.wav')

gen = 0
deaths = 0
score = Score.Score(APP_HEIGHT, APP_WIDTH)


def window_draw(window, birds, pipes, floor, score):
    window.blit(bg_night_img, (0, 0))
    [pipe.draw(window) for pipe in pipes]
    floor.draw(window)
    score.display_score(window)
    [bird.draw(window) for bird in birds]

def start_game(input_genomes, config):

    global gen, deaths, score
    gen += 1

    networks = []
    birds = []
    genomes = []

    for genome_id, genome in input_genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(net)
        birds.append(Bird.Bird(bird_sprites, APP_WIDTH / 3, APP_HEIGHT / 2, APP_HEIGHT))
        genomes.append(genome)

    running = True
    game_active = True
    floor = Floor.Floor(.85 * APP_HEIGHT, floor_img)
    pipes = [Pipe.Pipe(APP_WIDTH + 150, bot_pipe_img, top_pipe_img)]

    while running and birds:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                break
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE and game_active:
            #         birds[0].flap(flap_sound)
                # if event.key == pygame.K_SPACE and game_active == False:
                #     game_active = True
                #     bird.reset()
                #     score.reset_score()
                #     pipes.clear()
            if event.type == BIRD_TRANSITION:
                [bird.transition() for bird in birds]

        # determine which pipe to use as input neuron into network
        # by default first pipe but switch to next immediatley after we pass it
        floor.move()

        target_pipe_index = 0
        if birds:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].bot_img.get_width():
                target_pipe_index = 1

        for index, bird in enumerate(birds):
            genomes[index].fitness += 0.2
            bird.move()

            network_output = networks[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[target_pipe_index].height),
                                                              abs(bird.y - pipes[target_pipe_index].bot_pipe_y)))

            if network_output[0] > 0.45:
                bird.flap(flap_sound)

        pipes_to_remove = []
        add_pipe = False

        for pipe in pipes:
            pipe.move()

            for bird in birds:
                if pipe.collision_detect(bird) or bird.window_collide_check():
                    bird.death_event(death_sound)
                    genomes[birds.index(bird)].fitness -= 1
                    networks.pop(birds.index(bird))
                    genomes.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                    deaths += 1

                if not pipe.bird_passed and pipe.x < bird.x:
                    pipe.bird_pass(score_sound)
                    score.update_score()
                    add_pipe = True

            if pipe.x + pipe.bot_img.get_width() < 0:
                pipes_to_remove.append(pipe)

        if add_pipe:
            pipes.append(Pipe.Pipe(APP_WIDTH + 150, bot_pipe_img, top_pipe_img))
            for genome in genomes:
                genome.fitness += 3

        for pipe in pipes_to_remove:
            pipes.remove(pipe)

        if not birds:
            score.reset_score()

        window_draw(window, birds, pipes, floor, score)

        score.report_stats(window, gen, birds, deaths)
        score.update_high_score()

        pygame.display.update()
        clock.tick(60)

def run_NEAT(config_path):
    # define subheadings used in config file - all properties to be set
    # assumes neat.NEAT is included
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # generates poppulation based on config
    population = neat.Population(config)

    # reports stats for performance of each generation
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # evolve network for 30 generations, final stats
    best_genome = population.run(start_game, 1000)
    print('Best genome: {}'.format(best_genome))

if __name__ == '__main__':
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, 'NEAT_config.txt')
    run_NEAT(config_path)

