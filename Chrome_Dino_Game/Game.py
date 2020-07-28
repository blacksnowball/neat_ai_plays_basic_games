import pygame, Floor, Cactus, Dino, Score, Ptero, Cloud, random, neat, os

pygame.mixer.init()
pygame.init()

APP_WIDTH = 1400
APP_HEIGHT = 500
window = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
clock = pygame.time.Clock()

# load visual assets
floor_img = pygame.transform.scale2x(pygame.image.load('Assets/Images/ground.png')).convert_alpha()
cloud_img = pygame.transform.scale2x(pygame.image.load('Assets/Images/1x-cloud.png')).convert_alpha()

cactus_1 = pygame.transform.scale2x(pygame.image.load('Assets/Images/CACTUS1.png')).convert_alpha()
cactus_2 = pygame.transform.scale2x(pygame.image.load('Assets/Images/CACTUS2.png')).convert_alpha()
cactus_3 = pygame.transform.scale2x(pygame.image.load('Assets/Images/CACTUS3.png')).convert_alpha()
cactus_4 = pygame.transform.scale2x(pygame.image.load('Assets/Images/CACTUS4.png')).convert_alpha()
cactus_5 = pygame.transform.scale2x(pygame.image.load('Assets/Images/CACTUS5.png')).convert_alpha()
cacti_img = [cactus_1, cactus_2, cactus_3, cactus_4, cactus_5]


jump = pygame.transform.scale2x(pygame.image.load('Assets/Images/jump.png')).convert_alpha()
run_1 = pygame.transform.scale2x(pygame.image.load('Assets/Images/run1.png')).convert_alpha()
run_2 = pygame.transform.scale2x(pygame.image.load('Assets/Images/run2.png')).convert_alpha()
running_sprites = [run_1, run_2]
duck_1 = pygame.image.load('Assets/Images/low1.png').convert_alpha()
duck_2 = pygame.image.load('Assets/Images/low2.png').convert_alpha()
ducking_sprites = [duck_1, duck_2]

ptero1 = pygame.image.load('Assets/Images/enemy1.png').convert_alpha()
ptero2 = pygame.image.load('Assets/Images/enemy2.png').convert_alpha()
ptero_sprites = [ptero1, ptero2]

# load audio assets
jump_sound = pygame.mixer.Sound('Assets/Audio/jump.wav')
death_sound = pygame.mixer.Sound('Assets/Audio/die.wav')

gen = 0
deaths = 0
score = Score.Score(APP_HEIGHT, APP_WIDTH)

def start_game(input_genomes, config):

    global gen, deaths, score

    gen += 1

    networks = []
    dinos = []
    genomes = []

    for genome_id, genome in input_genomes:
        genome.fitness = 0
        network = neat.nn.FeedForwardNetwork.create(genome, config)
        networks.append(network)
        dinos.append(Dino.Dino(.1 * APP_WIDTH, .57 * APP_HEIGHT, running_sprites, ducking_sprites, jump))
        genomes.append(genome)

    running = True

    ptero_spawnable = False
    can_add_ptero = False
    next_ptero_spawn = 0

    floor = Floor.Floor(floor_img, .7 * APP_HEIGHT)
    cacti_threshold_spawn = [0.65, 0.7, 0.75]
    cacti = [Cactus.Cactus(cacti_img, .57 * APP_HEIGHT, 0, APP_WIDTH)]
    # cacti.append(Cactus.Cactus(cacti_img, .57 * APP_HEIGHT, cacti[0].initial_previous_x, APP_WIDTH+300))
    pteros = []

    cloud_1 = Cloud.Cloud(cloud_img, .7 * APP_WIDTH, .33 * APP_HEIGHT, APP_WIDTH)
    cloud_2 = Cloud.Cloud(cloud_img, .15 * APP_WIDTH, .15 * APP_HEIGHT, APP_WIDTH)
    cloud_3 = Cloud.Cloud(cloud_img, .5 * APP_WIDTH, .2 * APP_HEIGHT, APP_WIDTH)
    cloud_4 = Cloud.Cloud(cloud_img, .2 * APP_WIDTH, .4 * APP_HEIGHT, APP_WIDTH)
    clouds = [cloud_1, cloud_2, cloud_3, cloud_4]

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        if cacti[-1].x + cacti[-1].img.get_width() <= random.choice(cacti_threshold_spawn) * APP_WIDTH and len(
                cacti) <= 3:
            cacti.append(Cactus.Cactus(cacti_img, .57 * APP_HEIGHT, cacti[-1].initial_previous_x, APP_WIDTH))

        target_cactus_index = 0
        if dinos:
            if dinos[0].x > cacti[0].x + cacti[0].img.get_width():
                target_cactus_index += 1

        target_ptero_index = 0
        if pteros:
            if len(pteros) > 1 and dinos[0].x > pteros[0].x + pteros[0].sprites[pteros[0].current.state].get_width():
                target_ptero_index = 1


        for index, dino in enumerate(dinos):
            genomes[index].fitness += 0.05

            dino.move()

            if dino.is_ducking:
                dino.duck_transition()
            else:
                dino.run_transition()

            if not pteros:
                dino.is_ducking = False


            network_jump_output = networks[dinos.index(dino)].activate((dino.x,
                                                    abs(dino.x - cacti[target_cactus_index].x),
                                                       abs(dino.x - cacti[target_cactus_index].x+cacti[target_cactus_index].img.get_width())))

            network_duck_output = None

            if pteros:
                network_duck_output = networks[dinos.index(dino)].activate((dino.y, abs(dino.y - pteros[target_ptero_index].y),
                                                                            abs(dino.y - pteros[target_ptero_index].y + pteros[target_ptero_index].sprites[pteros[target_ptero_index].current_state].get_width())))


            if network_jump_output[0] > 0.5:
                dino.jump(jump_sound)
            if network_duck_output is not None:
                if network_duck_output[0] > 0.4 and pteros:
                    dino.duck_transition()

        score.update_score()
        floor.move()

        cactus_to_remove = []
        for cactus in cacti:

            cactus.move()

            for dino in dinos:

                if cactus.collide_detect(dino):
                    dino.death_event(death_sound)
                    genomes[dinos.index(dino)].fitness -= 1
                    networks.pop(dinos.index(dino))
                    genomes.pop(dinos.index(dino))
                    dinos.pop(dinos.index(dino))
                    deaths += 1

                if dino.x > cactus.x + cactus.img.get_width():
                    genomes[dinos.index(dino)].fitness += 3

            if cactus.x + cactus.img.get_width() < 0:
                cactus_to_remove.append(cactus)

        for cactus in cactus_to_remove:
            cacti.remove(cactus)

        if score.current_score >= 999999:
            ptero_spawnable = True

        if ptero_spawnable:
            if score.current_score >= next_ptero_spawn:
                can_add_ptero = True
                if can_add_ptero:
                    pteros.append(Ptero.Ptero(APP_WIDTH, random.uniform(0.45, 0.5) * APP_HEIGHT, ptero_sprites))
            if can_add_ptero:
                next_ptero_spawn = random.randint(100, 250) + score.current_score
                can_add_ptero = False

        if pteros:
            pteros_to_remove = []

            for ptero in pteros:
                ptero.move()

                for dino in dinos:
                    if ptero.collide_detect(dino):
                        dino.death_event(death_sound)
                        genomes[dinos.index(dino)].fitness -= 1
                        networks.pop(dinos.index(dino))
                        genomes.pop(dinos.index(dino))
                        dinos.pop(dinos.index(dino))
                        deaths += 1

                    if dino.x > ptero.x + ptero.sprites[ptero.current_state].get_width():
                        genomes[dinos.index(dino)].fitness += 2

                if ptero.x + ptero.sprites[ptero.current_state].get_width() < 0:
                    pteros_to_remove.append(ptero)

            for ptero in pteros_to_remove:
                pteros.remove(ptero)

        if not dinos:
            score.update_high_score()
            score.reset_score()
            break

        [cloud.move() for cloud in clouds]

        window.fill((235, 235, 235))
        floor.draw(window)
        [cactus.draw(window) for cactus in cacti]
        [ptero.draw(window) for ptero in pteros]
        [dino.draw(window) for dino in dinos]
        [cloud.draw(window) for cloud in clouds]
        score.display_score(window)
        score.report_stats(window, gen, dinos, deaths, next_ptero_spawn)
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
    best_genome = population.run(start_game, 10000)
    print('Best genome: {}'.format(best_genome))

if __name__ == '__main__':
    local_directory = os.path.dirname(__file__)
    config_path = os.path.join(local_directory, 'NEAT_config.txt')
    run_NEAT(config_path)