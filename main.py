import pygame
from pong import Game
import neat
import os


class PongGame:
    def __init__(self, window, width, height):
        self.game = Game(window, width, height)
        self.left_paddle = self.game.left_paddle
        self.right_paddle = self.game.right_paddle
        self.ball = self.game.ball

    def test_ai(self):
        """ Test AI without training, allowing manual paddle control """
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.game.move_paddle(left=True, up=True)
            if keys[pygame.K_s]:
                self.game.move_paddle(left=True, up=False)
            output = net.activate((self.right_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision = output.index(max(output))

            if decision == 0:
                pass
            elif decision == 1:
                self.game.move_paddle(left = False, up= True)
            else :
                self.game.move_paddle(left = False, up= True)

            game_info = self.game.loop()
            print(game_info.left_score, game_info.right_score)
            self.game.draw(True, False)
            pygame.display.update()

        pygame.quit()

    def train_ai(self, genome1, genome2, config):
        """ Train AI using NEAT """
        net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
        net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            # AI outputs based on paddle & ball positions
            output1 = net1.activate((self.ball.y, self.left_paddle.y, abs(self.left_paddle.x - self.ball.x)))
            output2 = net2.activate(( self.ball.y, self.right_paddle.y, abs(self.right_paddle.x - self.ball.x)))
            

            # AI decision logic
            decision1 = output1.index(max(output1))
            decision2 = output2.index(max(output2))

            if decision1 == 0:
                self.game.move_paddle(left=True, up=True)
            elif decision1 == 1:
                self.game.move_paddle(left=True, up=False)

            if decision2 == 0:
                self.game.move_paddle(left=False, up=True)
            elif decision2 == 1:
                self.game.move_paddle(left=False, up=False)

            game_info = self.game.loop()
            self.game.draw(draw_score=False, draw_hits=True)
            pygame.display.update()

            # Stop training when a score is reached or 50 hits are reached by the left paddle
            if game_info.left_score >= 1 or game_info.right_score >= 1 or game_info.left_hits > 50:
                self.calculate_fitness(genome1, genome2, game_info)
                break

    def calculate_fitness(self, genome1, genome2, game_info):
        """ Assign fitness scores based on game performance """
        genome1.fitness += game_info.left_hits
        genome2.fitness += game_info.right_hits


def eval_genomes(genomes, config):
    """ Evaluate each genome (AI) by playing against another AI """
    width, height = 800, 600
    window = pygame.display.set_mode((width, height))

    for i, (genome_id1, genome1) in enumerate(genomes):
        if i == len(genomes) - 1:
            break  # Avoid out-of-bounds errors

        genome1.fitness = 0  # Reset fitness

        for genome_id2, genome2 in genomes[i+1:]:  # Corrected loop
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            game = PongGame(window, width, height)
            game.train_ai(genome1, genome2, config)


def run_neat(config_path):
    """ Run NEAT algorithm to train AI """
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, 
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Initialize NEAT population
    p = neat.Population(config)
    # For checkpoint loading uncomment the below line
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-26')

    # Add reporters for monitoring progress
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(3))  # make a checkpoint for every third generation 


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run_neat(config_path)
   