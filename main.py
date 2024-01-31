import pygame
import sys

class Boxes:
    def __init__(self, screen, tile_size):
        self.screen = screen
        self.tile_size = tile_size

        # Levels
        self.boxes1 = [[2,1],[2,2],[2,3],[2,4],[2,5],[2,6]]
        self.boxes2 = [[2,1],[2,3],[1,4],[1,3],[3,2]]
        self.boxes3 = [[1,2],[2,2],[3,2],[4,2],[5,2],[6,2],[7,2],[8,2],[7,3],[6,3],[5,3],[4,3],[3,3],[2,3],[1,3]]
        self.boxes4 = [[1,2],[1,3],[2,2],[2,3],[3,3],[3,2],[4,2],[4,3],[5,2],[5,3],[8,3],[7,2],[8,4],[8,5],[7,6],[3,6],[3,5],[3,4],[4,5],[1,4],[2,4],[3,4],[4,4],[5,4],[6,3],[6,4]]
        self.boxes5 = [[1,2],[5,5],[2,3],[6,5],[3,2],[4,2],[5,2],[8,3],[7,2],[8,4],[8,5],[7,5],[2,6],[4,5],[1,5],[2,4],[3,4],[6,3],[6,4]]

        self.boxes = self.boxes1

        self.box_image = pygame.image.load("img/box.png")
        self.box_image = pygame.transform.scale(self.box_image, (self.tile_size, self.tile_size))

    def update(self, box_index, direction):
        self.box_index = box_index
        self.direction = direction
        
    def draw(self):
        for box_pos in self.boxes:
            self.screen.blit(self.box_image, (box_pos[0] * self.tile_size, box_pos[1] * self.tile_size))
    
    def collide_player(self, player_pos):
        if player_pos in self.boxes:
            return self.boxes.index(player_pos)
        
class Game:
    def __init__(self):

        # Setup
        pygame.init()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 640, 512
        self.TILE_SIZE = 64
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Level 1")

        # Map
        self.map_image = pygame.image.load("img/map.png")
        self.map_image = pygame.transform.scale(self.map_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Player
        self.player_image = pygame.image.load("img/player.png")
        self.player_image = pygame.transform.scale(self.player_image, (self.TILE_SIZE, self.TILE_SIZE))
        self.player_pos = [1, 1]

        # Boxes
        self.boxes = Boxes(self.screen, self.TILE_SIZE)
        
        # Cherry
        self.cherry_image = pygame.image.load("img/cherry.png")
        self.cherry_image = pygame.transform.scale(self.cherry_image, (self.TILE_SIZE, self.TILE_SIZE))
        self.cherry_pos1 = [8, 6]
        self.cherry_pos2 = [1, 1]
        self.cherry_pos3 = [8, 6]
        self.cherry_pos4 = [1, 1]
        self.cherry_pos5 = [8, 6]
        self.cherry_pos = self.cherry_pos1
        self.level = 1

        # Clock
        self.clock = pygame.time.Clock()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player_pos[1] -= 1
                    self.direction = "UP"
                    self.check_walls(self.player_pos)
                    self.check_boxes()
                    self.check_cherry()
                elif event.key == pygame.K_DOWN:
                    self.player_pos[1] += 1
                    self.direction = "DOWN"
                    self.check_walls(self.player_pos)
                    self.check_boxes()
                    self.check_cherry()
                elif event.key == pygame.K_LEFT:
                    self.player_pos[0] -= 1
                    self.direction = "LEFT"
                    self.check_walls(self.player_pos)
                    self.check_boxes()
                    self.check_cherry()
                elif event.key == pygame.K_RIGHT:
                    self.player_pos[0] += 1
                    self.direction = "RIGHT"
                    self.check_walls(self.player_pos)
                    self.check_boxes()
                    self.check_cherry()

    def check_walls(self, pos):
        if pos[0] < 1:
            pos[0] = 1
            return True
        
        elif pos[0] >= (self.SCREEN_WIDTH - self.TILE_SIZE) // self.TILE_SIZE:
           pos[0] = (self.SCREEN_WIDTH - self.TILE_SIZE) // self.TILE_SIZE - 1
           return True

        if pos[1] < 1:
            pos[1] = 1
            return True
        
        elif pos[1] >= (self.SCREEN_HEIGHT - self.TILE_SIZE) // self.TILE_SIZE:
            pos[1] = (self.SCREEN_HEIGHT - self.TILE_SIZE) // self.TILE_SIZE - 1
            return True

    def check_boxes(self):
        index = self.boxes.collide_player(self.player_pos)
        if index is not None:
            dest_x, dest_y = self.boxes.boxes[index][0], self.boxes.boxes[index][1]
            if self.direction == "RIGHT":
                dest_x += 1
            elif self.direction == "LEFT":
                dest_x -= 1
            elif self.direction == "UP":
                dest_y -= 1
            elif self.direction == "DOWN":
                dest_y += 1
            # check if the destination is within walls
            if 1 <= dest_x < (self.SCREEN_WIDTH - self.TILE_SIZE) // self.TILE_SIZE and 1 <= dest_y < (self.SCREEN_HEIGHT - self.TILE_SIZE) // self.TILE_SIZE:
                # check if the destination is not occupied by another box
                if [dest_x, dest_y] not in self.boxes.boxes:
                    # check if the destination is not inside the cherry
                    if [dest_x, dest_y] != self.cherry_pos:
                        # update the box position
                        self.boxes.boxes[index][0] = dest_x
                        self.boxes.boxes[index][1] = dest_y
                        self.check_walls(self.player_pos)
                    else:
                        self.pushback(self.direction)
                else:
                    self.pushback(self.direction)
            else:
                self.pushback(self.direction)

    def check_cherry(self):
        if self.player_pos == self.cherry_pos:
            self.switch_level()
            self.level += 1
        
    def pushback(self, direction):
        self.direction = direction
        if self.direction == "RIGHT":
            self.player_pos[0] -= 1
        elif self.direction == "LEFT":
            self.player_pos[0] += 1
        elif self.direction == "UP":
            self.player_pos[1] += 1
        elif self.direction == "DOWN":
            self.player_pos[1] -= 1
                
    def draw_map(self):
        self.screen.blit(self.map_image, (0, 0))

    def switch_level(self):
        if self.level == 1:
            self.cherry_pos = self.cherry_pos2
            self.boxes.boxes = self.boxes.boxes2
            pygame.display.set_caption("Level 2")
        if self.level == 2:
            self.cherry_pos = self.cherry_pos3
            self.boxes.boxes = self.boxes.boxes3
            pygame.display.set_caption("Level 3")
        if self.level == 3:
            self.cherry_pos = self.cherry_pos4
            self.boxes.boxes = self.boxes.boxes4
            pygame.display.set_caption("Level 4")
        if self.level == 4:
            self.cherry_pos = self.cherry_pos5
            self.boxes.boxes = self.boxes.boxes5
            pygame.display.set_caption("Level 5")
        if self.level == 5:
            print('YOU WIN!')
            pygame.quit()
            sys.exit()

    def update_screen(self):
        self.screen.fill((255, 255, 255))
        self.draw_map()
        self.boxes.draw()
        self.screen.blit(self.player_image, (self.player_pos[0] * self.TILE_SIZE, self.player_pos[1] * self.TILE_SIZE))
        self.screen.blit(self.cherry_image, (self.cherry_pos[0] * self.TILE_SIZE, self.cherry_pos[1] * self.TILE_SIZE))
        pygame.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.update_screen()
            self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()