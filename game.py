import json
import pygame
import sys
import xbox360_controller
pygame.init()
MY_FONT = pygame.font.Font(None, 50)
MY_FON = pygame.font.Font(None, 25)
MY_FONSMOLL = pygame.font.Font(None, 18)
# Window settings
WIDTH = 960
HEIGHT = 640
SIZE = (WIDTH, HEIGHT)
TITLE = "The SMILE"
window = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("The blockening")
screen = pygame.display.set_mode(SIZE)
FPS = 40
GRID_SIZE = 32
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 15)
levels = ["levels/world-1.json",
          "levels/world-2.json",
          "levels/world-3.json"]



# Options
#
#
#
#
##  FIX THE TIME THING
#
#
sound_on = True
# Colors
TRANSPARENT = (0, 0, 0, 0)
DARK_BLUE = (16, 86, 103)
WHITE = (255, 255, 255)

# Fonts
FONT_SM = pygame.font.Font("assets/fonts/Play-Regular.ttf", 32)
FONT_MD = pygame.font.Font("assets/fonts/Play-Regular.ttf", 64)
FONT_LG = pygame.font.Font("assets/fonts/KeaniaOne-Regular.ttf", 72)

# Helper functions
def load_image(file_path):
    img = pygame.image.load(file_path)
    img = pygame.transform.scale(img, (GRID_SIZE, GRID_SIZE))

    return img

def play_sound(sound, loops=0, maxtime=0, fade_ms=0):
    if sound_on:
        if maxtime == 0:
            sound.play(loops, maxtime, fade_ms)
        else:
            sound.play(loops, maxtime, fade_ms)

def play_music():
    if sound_on:
        pygame.mixer.music.play(-1)

# Images
spike_img = load_image("assets/spike.jpg")
hero_walk1 = load_image("assets/aholland.jpg")
hero_walk2 = load_image("assets/aholland.jpg")
hero_jump = load_image("assets/aholland.jpg")
hero_idle = load_image("assets/aholland.jpg")
black_heart = load_image("assets/St-Basil-Cathedral-Moscow_cs.jpg")
hero_images = {"run": [hero_walk1, hero_walk2],
               "jump": hero_jump,
               "idle": hero_idle}
hearts_img = load_image("assets/8bitheart.png")
block_images = {"TL": load_image("assets/bamamas.png"),
                "TM": load_image("assets/bamamas.png"),
                "TR": load_image("assets/bamamas.png"),
                "ER": load_image("assets/bamamas.png"),
                "EL": load_image("assets/bamamas.png"),
                "TP": load_image("assets/bamamas.png"),
                "CN": load_image("assets/bamamas.png"),
                "LF": load_image("assets/bamamas.png"),
                "SP": load_image("assets/bamamas.png")}
fakeblock_img = load_image("assets/fakebamamas.png")
coin_img = load_image("assets/coin.png")
heart_img = load_image("assets/healthpack.png")
oneup_img = load_image("assets/items/first_aid.png")
flag_img = load_image("assets/items/flag.png")
flagpole_img = load_image("assets/items/flagpole.png")
clock_img = load_image("assets/clock.jpg")

monster_img1 = load_image("assets/enemies/monster-1.png")
monster_img2 = load_image("assets/enemies/monster-2.png")
monster_images = [monster_img1, monster_img2]

bear_img = load_image("assets/antismile.png")
bear_images = [bear_img]

# Sounds
JUMP_SOUND = pygame.mixer.Sound("assets/sounds/pickup_coin.wav")
COIN_SOUND = pygame.mixer.Sound("assets/sounds/pickup_coin.wav")
POWERUP_SOUND = pygame.mixer.Sound("assets/sounds/pickup_coin.wav")
HURT_SOUND = pygame.mixer.Sound("assets/sounds/pickup_coin.wav")
DIE_SOUND = pygame.mixer.Sound("assets/sounds/pickup_coin.wav")
LEVELUP_SOUND = pygame.mixer.Sound("assets/sounds/pickup_coin.wav")
GAMEOVER_SOUND = pygame.mixer.Sound("assets/sounds/pickup_coin.wav")
# render text
label = myfont.render("Pixel perfect", True, (255,255,0))

controller = xbox360_controller.Controller(0)
# Colors
SKY_BLUE = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255,0,0)
BLUE = (120,200,10)
god_mode = False
# Fonts
font_small = pygame.font.Font(None, 50)
font_big = pygame.font.Font(None, 64)

# Images
coin_img = pygame.image.load("assets/coin.png")
coin_img = pygame.transform.scale(coin_img, (32, 32))



block_img = pygame.image.load("assets/bamamas.png")
block_img = pygame.transform.scale(block_img, (32, 32))


taco = pygame.image.load("assets/download.jpg")
taco = pygame.transform.scale(block_img, (32, 32))


# Controls
LEFT = pygame.K_a
RIGHT = pygame.K_d
JUMP = pygame.K_w 
GODT = pygame.K_g
P = pygame.K_p
##############################################3

    
##########################################################    
class Entity(pygame.sprite.Sprite):

    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.vy = 0
        self.vx = 0

    def apply_gravity(self, level):

        self.vy += level.gravity
        self.vy = min(self.vy, level.terminal_velocity)
    


###############################################################3        
class Block(Entity):
    
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

class FakeBlock(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
################################################################

    
################################################################
class Character(Entity):

    def __init__(self, images):
        super().__init__(0, 0, images['idle'])

        self.image_idle = images['idle']
        self.images_run_right = images['run']
        self.images_run_left = [pygame.transform.flip(img, 1, 0) for img in self.images_run_right]
        self.image_jump_right = images['jump']
        self.image_jump_left = pygame.transform.flip(self.image_jump_right, 1, 0)

        self.running_images = self.images_run_right
        self.image_index = 0
        self.steps = 0

        self.speed = 8
        self.jump_power = 20

        self.vx = 0
        self.vy = 0
        self.facing_right = True
        self.on_ground = True
        self.coins = 0
        self.score = 0
        self.lives = 5
        self.hearts = 4
        self.max_hearts = 4
        self.invincibility = 0
        self.GMOD = False
        self.gravity = 1
    def move(self,x ,y):
        self.vx = x *self.speed
        if x <0:
            self.facing_right = False
        else:
            self.facing_right = True

    def stop(self):
        self.vx = 0
 
    def jump(self, blocks):
        self.rect.y += 1

        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        if len(hit_list) > 0:
            self.vy = -1 * self.jump_power
            play_sound(JUMP_SOUND)

        self.rect.y -= 1

    def check_world_boundaries(self, level):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > level.width:
            self.rect.right = level.width
        if self.rect.y > level.height + 64:
            self.hearts -= 1
    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.vx = 0
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.vx = 0

        self.on_ground = False
        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy >1:
                self.on_ground = True
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
                self.on_ground = True
 #               self.rect.y -= 1
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0
    def process_fakeblock(self, fakeblock):
        hit_list = pygame.sprite.spritecollide(self, fakeblock, True)



    def process_coins(self, coins):
        hit_list = pygame.sprite.spritecollide(self, coins, True)

        for coin in hit_list:
            play_sound(COIN_SOUND)
            self.coins += coin.value
            
    def process_spike(self, spike):
        hit_list = pygame.sprite.spritecollide(self, spike, False)
        for p in hit_list:
            self.hearts -= self.hearts
    def process_enemies(self, enemies):
        hit_list = pygame.sprite.spritecollide(self, enemies, False)
        

        for p in hit_list:
            if len(hit_list) > 0 and self.invincibility == 0 and self.vy <= 0:
                play_sound(HURT_SOUND)
                self.hearts -= 1
                self.invincibility = int(0.75 * FPS)
            elif len(hit_list) > 0 and self.invincibility == 0 and self.vy > 0:
                self.vy -= 20
                pygame.sprite.Sprite.kill(p)
                self.score += 20
                

                
    def process_powerups(self, powerups):
        hit_list = pygame.sprite.spritecollide(self, powerups, True)

        for p in hit_list:
            if self.hearts == self.max_hearts:
                self.score += 1
            play_sound(POWERUP_SOUND)
            p.apply(self)
    
    def check_flag(self, level):
        hit_list = pygame.sprite.spritecollide(self, level.flag, False)

        if len(hit_list) > 0:
            level.completed = True
            play_sound(LEVELUP_SOUND)
            self.score += (level.time_clock // FPS) * 2

    def set_image(self):
        if self.on_ground:
            if self.vx != 0:
                if self.facing_right:
                    self.running_images = self.images_run_right
                else:
                    self.running_images = self.images_run_left

                self.steps = (self.steps + 1) % self.speed # Works well with 2 images, try lower number if more frames are in animation

                if self.steps == 0:
                    self.image_index = (self.image_index + 1) % len(self.running_images)
                    self.image = self.running_images[self.image_index]
            else:
                self.image = self.image_idle
        else:
            if self.facing_right:
                self.image = self.image_jump_right
            else:
                self.image = self.image_jump_left

    def die(self):
        self.lives -= 1

        if self.lives > 0:
            play_sound(DIE_SOUND)
        else:
            play_sound(GAMEOVER_SOUND)

    def respawn(self, level):
        self.rect.x = level.start_x
        self.rect.y = level.start_y
        self.hearts = self.max_hearts
        self.invincibility = 0
        self.GMOD = False
    def update(self, level):
        self.level = level
        
        self.process_enemies(level.enemies)



        if not self.GMOD:
            self.apply_gravity(level)
        self.move_and_process_blocks(level.blocks)
        self.check_world_boundaries(level)
        self.set_image()
        self.process_spike(level.spike)
        
        if self.hearts > 0:
            self.process_fakeblock(level.fakeblock)
            self.process_coins(level.coins)
            self.process_powerups(level.powerups)
            self.check_flag(level)

            if self.invincibility > 0:
                self.invincibility -= 1
        else:
            
            self.die()
######################################################
class Coin(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

        self.value = 1
#############################################
class Spike(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        
class GodeMode(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
    def apply(self, character):
        character.GMOD = True
###############################################
class Timeplus(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def apply(self, character):
        character.level.time_clock += 20 * FPS
###############################################
class Heart(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def apply(self, character):
        character.hearts += 1
        character.hearts = max(character.hearts, character.max_hearts)

            

######################################################
class Enemy(Entity):
    def __init__(self, x, y, images):
        super().__init__(x, y, images[0])

        self.images_left = images
        self.images_right = [pygame.transform.flip(img, 1, 0) for img in images]
        self.current_images = self.images_left
        self.image_index = 0
        self.steps = 0

    def reverse(self):
        self.vx *= -1

        if self.vx < 0:
            self.current_images = self.images_left
        else:
            self.current_images = self.images_right

        self.image = self.current_images[self.image_index]

    def check_world_boundaries(self, level):
        if self.rect.left < 0:
            self.rect.left = 0
            self.reverse()
        elif self.rect.right > level.width:
            self.rect.right = level.width
            self.reverse()
        if self.rect.y > level.height:
            pygame.sprite.Sprite.kill(self)

    def move_and_process_blocks(self):
        pass

    def set_images(self):
        if self.steps == 0:
            self.image = self.current_images[self.image_index]
            self.image_index = (self.image_index + 1) % len(self.current_images)

        self.steps = (self.steps + 1) % 20 # Nothing significant about 20. It just seems to work okay.

    def is_near(self, hero):
        return abs(self.rect.x - hero.rect.x) < 2 * WIDTH

    def update(self, level, hero):
        if self.is_near(hero):
            self.apply_gravity(level)
            self.move_and_process_blocks(level.blocks)
            self.check_world_boundaries(level)
            self.set_images()

    def reset(self):
        self.rect.x = self.start_x
        self.rect.y = self.start_y
        self.vx = self.start_vx
        self.vy = self.start_vy
        self.image = self.images_left[0]
        self.steps = 0

###################################################################

class Bear(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.start_x = x
        self.start_y = y
        self.start_vx = -2
        self.start_vy = 0

        self.vx = self.start_vx
        self.vy = self.start_vy

    def move_and_process_blocks(self, blocks):
        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vy > 0:
                self.rect.bottom = block.rect.top
                self.vy = 0
            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0
###################################################################
class Monster(Enemy):
    def __init__(self, x, y, images):
        super().__init__(x, y, images)

        self.start_x = x
        self.start_y = y
        self.start_vx = -2
        self.start_vy = 0

        self.vx = self.start_vx
        self.vy = self.start_vy

    def move_and_process_blocks(self, blocks):
        reverse = False

        self.rect.x += self.vx
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        for block in hit_list:
            if self.vx > 0:
                self.rect.right = block.rect.left
                self.reverse()
            elif self.vx < 0:
                self.rect.left = block.rect.right
                self.reverse()

        self.rect.y += self.vy
        hit_list = pygame.sprite.spritecollide(self, blocks, False)

        reverse = True

        for block in hit_list:
            if self.vy >= 0:
                self.rect.bottom = block.rect.top
                self.vy = 0

                if self.vx > 0 and self.rect.right <= block.rect.right:
                    reverse = False

                elif self.vx < 0 and self.rect.left >= block.rect.left:
                    reverse = False

            elif self.vy < 0:
                self.rect.top = block.rect.bottom
                self.vy = 0

        if reverse:
            self.reverse()
################################################################################
class OneUp(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def apply(self, character):
        character.lives += 1
################################################################################
class Heart(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)

    def apply(self, character):
        character.hearts += 1
        character.hearts = min(character.hearts, character.max_hearts)
################################################################################
class Flag(Entity):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
################################################################################
class Level():
    
    def __init__(self, file_path):
        self.starting_blocks = []
        self.starting_enemies = []
        self.starting_coins = []
        self.starting_powerups = []
        self.starting_flag = []
        self.starting_fakeblock = []
        self.starting_spike = []
        self.spike = pygame.sprite.Group()
    
        self.blocks = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.flag = pygame.sprite.Group()
        self.fakeblock = pygame.sprite.Group()
        self.active_sprites = pygame.sprite.Group()
        self.inactive_sprites = pygame.sprite.Group()

        with open(file_path, 'r') as f:
            data = f.read()
          
        map_data = json.loads(data)
        self.clock_extra = map_data['clockextra']
        self.time_clock = FPS * (40 + self.clock_extra)

        self.width = map_data['width'] * GRID_SIZE 
        self.height = map_data['height'] * GRID_SIZE

        self.start_x = map_data['start'][0] * GRID_SIZE
        self.start_y = map_data['start'][1] * GRID_SIZE
        for item in map_data['spike']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_spike.append(Spike(x, y, spike_img))
        for item in map_data['timeplus']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(Timeplus(x, y, clock_img))
        for item in map_data['godmode']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(GodeMode(x, y, clock_img))                             
        for item in map_data['blocks']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            img = block_images[item[2]]
            self.starting_blocks.append(Block(x, y, img))
        for item in map_data['fakeblock']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_fakeblock.append(FakeBlock(x, y, fakeblock_img))

        for item in map_data['bears']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_enemies.append(Bear(x, y, bear_images))

        for item in map_data['monsters']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_enemies.append(Monster(x, y, monster_images))

        for item in map_data['coins']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_coins.append(Coin(x, y, coin_img))

        for item in map_data['oneups']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(OneUp(x, y, oneup_img))

        for item in map_data['hearts']:
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE
            self.starting_powerups.append(Heart(x, y, heart_img))

        for i, item in enumerate(map_data['flag']):
            x, y = item[0] * GRID_SIZE, item[1] * GRID_SIZE

            if i == 0:
                img = flag_img
            else:
                img = flagpole_img

            self.starting_flag.append(Flag(x, y, img))

        self.background_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.scenery_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.inactive_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)
        self.active_layer = pygame.Surface([self.width, self.height], pygame.SRCALPHA, 32)

        if map_data['background-color'] != "":
            self.background_layer.fill(map_data['background-color'])

        if map_data['background-img'] != "":
            background_img = pygame.image.load(map_data['background-img'])

            if map_data['background-fill-y']:
                h = background_img.get_height()
                w = int(background_img.get_width() * HEIGHT / h)
                background_img = pygame.transform.scale(background_img, (w, HEIGHT))

            if "top" in map_data['background-position']:
                start_y = 0
            elif "bottom" in map_data['background-position']:
                start_y = self.height - background_img.get_height()

            if map_data['background-repeat-x']:
                for x in range(0, self.width, background_img.get_width()):
                    self.background_layer.blit(background_img, [x, start_y])
            else:
                self.background_layer.blit(background_img, [0, start_y])

        if map_data['scenery-img'] != "":
            scenery_img = pygame.image.load(map_data['scenery-img'])

            if map_data['scenery-fill-y']:
                h = scenery_img.get_height()
                w = int(scenery_img.get_width() * HEIGHT / h)
                scenery_img = pygame.transform.scale(scenery_img, (w, HEIGHT))

            if "top" in map_data['scenery-position']:
                start_y = 0
            elif "bottom" in map_data['scenery-position']:
                start_y = self.height - scenery_img.get_height()

            if map_data['scenery-repeat-x']:
                for x in range(0, self.width, scenery_img.get_width()):
                    self.scenery_layer.blit(scenery_img, [x, start_y])
            else:
                self.scenery_layer.blit(scenery_img, [0, start_y])

        pygame.mixer.music.load(map_data['music'])
        
        self.name = map_data['name']
        if 'End' in self.name:
            
            for y in range(32,0):  #y 
                b = Block(6800,y, img)
                self.starting_blocks.append(b)
                
        self.gravity = map_data['gravity']
        self.terminal_velocity = map_data['terminal-velocity']
        
        self.completed = False

        self.blocks.add(self.starting_blocks)
        self.enemies.add(self.starting_enemies)
        self.coins.add(self.starting_coins)
        self.powerups.add(self.starting_powerups)
        self.fakeblock.add(self.starting_fakeblock)
        self.spike.add(self.starting_spike)
        self.flag.add(self.starting_flag)
        self.active_sprites.add(self.coins, self.enemies, self.powerups, self.starting_fakeblock)
        self.inactive_sprites.add(self.blocks, self.flag, self.spike)

        self.inactive_sprites.draw(self.inactive_layer)

    def reset(self):

        self.fakeblock.add(self.starting_fakeblock)
        self.enemies.add(self.starting_enemies)
        self.coins.add(self.starting_coins)
        self.powerups.add(self.starting_powerups)
        self.time_clock = FPS * (40 + self.clock_extra)
        self.active_sprites.add(self.coins, self.enemies, self.powerups, self.starting_fakeblock)

        for e in self.enemies:
            e.reset()
##############################################################################        
class Game():

    SPLASH = 0
    START = 1
    PLAYING = 2
    PAUSED = 3
    LEVEL_COMPLETED = 4
    GAME_OVER = 5
    VICTORY = 6
    

    def __init__(self):
        self.window = pygame.display.set_mode([WIDTH, HEIGHT])
#        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.done = False
        self.active_layer = pygame.Surface([1920, 640], pygame.SRCALPHA, 32)
        self.reset()

    def start(self):
        self.level = Level(levels[self.current_level])
        self.grid_layer = pygame.Surface([self.level.width, self.level.height], pygame.SRCALPHA, 32)
        self.y_text = pygame.Surface([self.level.width, self.level.height], pygame.SRCALPHA, 32)
        self.x_text = pygame.Surface([self.level.width, self.level.height], pygame.SRCALPHA, 32)
        self.level.reset()
        self.hero.respawn(self.level)

    def advance(self):
        self.current_level += 1
        self.start()
        self.stage = Game.START

    def reset(self):
        self.hero = Character(hero_images)
        self.current_level = 0
        self.start()
        self.stage = Game.SPLASH
            
    def display_splash(self, surface):
        line1 = FONT_LG.render(TITLE, 1, DARK_BLUE)
        line2 = FONT_SM.render("Press any key to start.", 1, WHITE)

        x1 = WIDTH / 2 - line1.get_width() / 2;
        y1 = HEIGHT / 3 - line1.get_height() / 2;

        x2 = WIDTH / 2 - line2.get_width() / 2;
        y2 = y1 + line1.get_height() + 16;

        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))

    def display_message(self, surface, primary_text, secondary_text):
        line1 = FONT_MD.render(primary_text, 1, WHITE)
        line2 = FONT_SM.render(secondary_text, 1, WHITE)

        x1 = WIDTH / 2 - line1.get_width() / 2;
        y1 = HEIGHT / 3 - line1.get_height() / 2;

        x2 = WIDTH / 2 - line2.get_width() / 2;
        y2 = y1 + line1.get_height() + 16;

        surface.blit(line1, (x1, y1))
        surface.blit(line2, (x2, y2))

    def display_stats(self, surface):
        hearts_text = FONT_SM.render("Hearts: " + str(self.hero.hearts), 1, WHITE)
        lives_text = FONT_SM.render("x"+ str(self.hero.lives), 1, WHITE)
        score_text = FONT_SM.render("Score: " + str(self.hero.score), 1, WHITE)
        coin_text = FONT_SM.render("Coins: " + str(self.hero.coins), 1, WHITE)
        clock_text = FONT_SM.render("Clock: " + str(self.level.time_clock // FPS), 1, WHITE)
        
        gamep_text = FONT_SM.render("The game is pasuedarinos", 2, WHITE)
        surface.blit(score_text, (WIDTH - score_text.get_width() - 32, 32))
        surface.blit(coin_text, (WIDTH - score_text.get_width() - 32, 0))
        surface.blit(clock_text, (WIDTH - score_text.get_width() - 32, 96))
        surface.blit(lives_text, (32, 64))
        for x in range(self.hero.max_hearts):
            if x < self.hero.hearts:
                surface.blit(hearts_img, (x * 20 + 32, 32))
            else:
                surface.blit(black_heart, (x * 20 +32 , 32))
        if self.stage == Game.PAUSED:
            surface.blit(gamep_text, (WIDTH - score_text.get_width() - 432, 320))
        if self.hero.GMOD == True:
            gmod_text = FONT_SM.render("GodMode: ON", 2, WHITE)
        else:
            gmod_text = FONT_SM.render(" ", 0, WHITE)
        surface.blit(hero_idle, (5, 64))
        surface.blit(gmod_text, (WIDTH - score_text.get_width() - 98, 64))

    def make_grid(self, offset_x, offset_y):
        for x in range(0, self.level.width, 32):
            pygame.draw.line(self.grid_layer, WHITE, [x,0],[x,self.level.height])
            
        for y in range(0, self.level.height, 32):
            text1 = MY_FON.render(str(y/32), True, GREEN)
            self.y_text.blit(text1, [0,y-7.5])
            
        for y in range(0, self.level.height, 32):
            pygame.draw.line(self.grid_layer, WHITE, [0,y],[self.level.width, y])
            
        for x in range(0, self.level.width, 32):
            text1 = MY_FONSMOLL.render(str(x/32), True, BLACK)
            self.x_text.blit(text1, [x-7.5,0])
            
        pygame.draw.rect(self.grid_layer, WHITE, [self.hero.rect.right, self.hero.rect.bottom, 1, 1])
        
####################3####################3####################3####################3
    def process_events(self):
        pressed = controller.get_buttons()
        a_btn = pressed[xbox360_controller.A]
        b_btn = pressed[xbox360_controller.B]
        back_btn = pressed[xbox360_controller.BACK]
        start_btn = pressed[xbox360_controller.START]
        pad_up, pad_right,pad_down,pad_left = controller.get_pad()
        lt_x, lt_y = controller.get_left_stick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            
            if self.stage == Game.SPLASH or self.stage == Game.START:
                if event.type == pygame.JOYBUTTONDOWN:
                    self.stage = Game.PLAYING
                    play_music()
                
            elif self.stage == Game.PLAYING:
                if event.type == pygame.JOYBUTTONDOWN:
#                    if event.button == xbox360_controller.BACK:
#                        self.hero.GMOD = not self.hero.GMOD
                    if event.button == xbox360_controller.A:
                        self.hero.jump(self.level.blocks)
                    if event.button == xbox360_controller.START:
                        self.stage = game.PAUSED
                    if event.button == xbox360_controller.Y:
                        sound_on = False
                    
            elif self.stage == Game.PAUSED:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == xbox360_controller.START:
                        self.stage = Game.PLAYING
                    
            elif self.stage == Game.LEVEL_COMPLETED:
                if event.type == pygame.JOYBUTTONDOWN:
                    self.advance()

            elif self.stage == Game.VICTORY or self.stage == Game.GAME_OVER:
                if event.type == pygame.JOYBUTTONDOWN:
                    self.reset()

        if self.hero.GMOD == True:
            if pad_up:
                self.hero.rect.y -= 8
            elif pad_down:
                self.hero.rect.y += 8
            elif pad_right:
                self.hero.rect.x +=8
            elif pad_left:
                self.hero.rect.x -=8
            
        if self.stage == Game.PLAYING:
            self.hero.move(lt_x, lt_y)
                
    def update(self):
        if self.stage == Game.PLAYING:
            self.hero.update(self.level)
            self.level.enemies.update(self.level, self.hero)

        if self.level.completed:
            if self.current_level < len(levels) - 1:
                self.stage = Game.LEVEL_COMPLETED
            else:
                self.stage = Game.VICTORY
            pygame.mixer.music.stop()

        elif self.hero.lives == 0:
            self.stage = Game.GAME_OVER
            pygame.mixer.music.stop()

        elif self.hero.hearts == 0:
            self.level.reset()
            self.hero.respawn(self.level)
        if self.stage == Game.PLAYING:
            self.level.time_clock -= 1
            if self.level.time_clock == 0:
                self.hero.hearts -= self.hero.hearts

    def calculate_offset(self):
        x = -1 * self.hero.rect.centerx + WIDTH / 2

        if self.hero.rect.centerx < WIDTH / 2:
            x = 0
        elif self.hero.rect.centerx > self.level.width - WIDTH / 2:
            x = -1 * self.level.width + WIDTH
  

        y = -1 * self.hero.rect.centery + HEIGHT / 2

        if self.hero.rect.centery < HEIGHT / 2:
            y = 0
        elif self.hero.rect.centery > self.level.height - HEIGHT / 2:
            y = -1 * self.level.height + HEIGHT

        return x, y
    
    def draw(self):
        offset_x, offset_y = self.calculate_offset()

        self.level.active_layer.fill(TRANSPARENT)
        self.level.active_sprites.draw(self.level.active_layer)
        self.active_layer.blit(label, [1088, 384])            

        if self.hero.invincibility % 3 < 2:
            self.level.active_layer.blit(self.hero.image, [self.hero.rect.x, self.hero.rect.y])

        self.window.blit(self.level.background_layer, [offset_x / 3, offset_y])
        self.window.blit(self.level.scenery_layer, [offset_x / 2, offset_y])
        self.window.blit(self.level.inactive_layer, [offset_x, offset_y])
        self.window.blit(self.level.active_layer, [offset_x, offset_y])

        self.display_stats(self.window)

        if self.stage == Game.SPLASH:
            self.display_splash(self.window)
        elif self.stage == Game.START:
            self.display_message(self.window, "Ready?!!!", "Press any key to start.")
        elif self.stage == Game.PAUSED:
            pass
        elif self.stage == Game.LEVEL_COMPLETED:
            self.display_message(self.window, "Level Complete", "Press any key to continue.")
        elif self.stage == Game.VICTORY:
            self.display_message(self.window, "You Win!", "Press 'R' to restart.")
        elif self.stage == Game.GAME_OVER:
            self.display_message(self.window, "Game Over", "Press 'R' to restart.")
                            
                        
#        self.make_grid(offset_x, offset_y)
#        window.blit(self.grid_layer, [offset_x, offset_y])
        window.blit(self.y_text, [0, offset_y])
        window.blit(self.x_text, [offset_x, 0])
        pygame.display.flip()
        
    def loop(self):
        while not self.done:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.start()
    game.loop()
    pygame.quit()
    sys.exit()
########################################################
'''def main():
    # Make sprites
#    hero = Character(500, 512, hero_img)
    hero = Character(1056,576 , hero_img)
    blocks = pygame.sprite.Group()
     
#    for i in range(0, WIDTH * 2, 32):
#        b = Block(i, 576, block_img)
#        blocks.add(b)
    for i in range(0, 640, 32):
        b = Block(i,578, block_img)
        blocks.add(b)
    for i in range(1056,1089, 32):
        b = Block(i,608, block_img)
        blocks.add(b)
#    for y in range(192,576, 32):  #y 
#        b = Block(672,y, block_img)
#        blocks.add(b)
    blocks.add(Block(768,352 , block_img))
    blocks.add(Block(192, 448, block_img))
    blocks.add(Block(256, 448, block_img))
    blocks.add(Block(320, 448, block_img))
    blocks.add(Block(608, 544, block_img))
    blocks.add(Block(1344, 608, block_img))
    blocks.add(Block(1536, 448, block_img))
    blocks.add(Block(512, 320, block_img))

    coins = pygame.sprite.Group()
    coins.add(Coin(768, 384, coin_img))
    coins.add(Coin(256, 320, coin_img))
    #make enimies
    enemies = pygame.sprite.Group()
    enemies.add(Monester(640,512, hero_img))
    enemies.add(Bear(640,512, hero_img))
    #XDDDDDDDDDDDddddddddddddddd
    fakeblock = pygame.sprite.Group()
    fakeblock.add(FakeBlock(1120,576, block_img))
    powerups = pygame.sprite.Group()
    powerups.add(heart(1312, 576, taco))
    
    # Make a level
    level = Level(blocks, coins, enemies, powerups, fakeblock)
#total jump on flat 224 pixels max

    # Start game
    game = Game(hero, level)
    game.reset()
    game.play()

if __name__ == "__main__":
    main()'''
