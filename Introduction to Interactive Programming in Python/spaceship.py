# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

# key handler constants
KEYS = {simplegui.KEY_MAP['left']: -0.05, simplegui.KEY_MAP['right']: 0.05}

# Motion constants
FRICTION_FACTOR = 0.1
THRUST_fACTOR = 0.8
MISSLE_FACTOR = 3

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self, canvas):
        if not self.thrust:
            canvas.draw_image(self.image, self.image_center, self.image_size, 
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], 
                                           self.image_center[1]], self.image_size, self.pos, 
                              self.image_size, self.angle)

    def update(self):
        global time
        
        # Position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # Friction update
        self.vel[0] *= (1 - FRICTION_FACTOR)
        self.vel[1] *= (1 - FRICTION_FACTOR)
        
        # Angle update
        self.angle += self.angle_vel
        
        # Thrust update
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += THRUST_fACTOR * forward[0]
            self.vel[1] += THRUST_fACTOR * forward[1]
    
    def update_angle_vel(self, key):
        self.angle_vel += KEYS[key]
    
    def recover_angle_vel(self, key):
        self.angle_vel -= KEYS[key]
        
    def turn_thruster(self):
        if not self.thrust:
            self.thrust = True
            ship_thrust_sound.play()
        else:
            self.thrust = False
            ship_thrust_sound.rewind()
            
    def shoot(self):
        global a_missile
        
        # Forward vector
        forward = angle_to_vector(self.angle)
      
        # Position
        missle_pos = [self.pos[0], self.pos[1]]
        missle_pos[0] += self.image_size[1] / 2 * forward[0]
        missle_pos[1] += self.image_size[1] / 2 * forward[1]
     
        # Velocity
        missle_vel = [self.vel[0], self.vel[1]]
        missle_vel[0] += MISSLE_FACTOR * forward[0]
        missle_vel[1] += MISSLE_FACTOR * forward[1]
        
        # Shoot
        a_missile = Sprite(missle_pos, missle_vel, 0, 0, missile_image, missile_info, missile_sound)    

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, 
                          self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), 
                      nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, 
                      (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, 
                      (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # update scores and lives
    canvas.draw_text("Lives", [50, 50], 30, "White")
    canvas.draw_text(str(lives), [50, 80], 30, "White")
    canvas.draw_text("Score", [WIDTH  - 150, 50], 30, "White")
    canvas.draw_text(str(score), [WIDTH - 150, 80], 30, "White")
            
# timer handler that spawns a rock    
def rock_spawner():
    global time, a_rock
    # Position initialization
    random_x_pos = random.random() * WIDTH
    random_y_pos = random.random() * HEIGHT
    random_pos = [random_x_pos, random_y_pos]
    
    # Velocity initialization
    random_x_vel = 2 * random.random() - 1
    random_y_vel = 2 * random.random() - 1
    random_vel = [random_x_vel, random_y_vel]
        
    # Angle velocity initialization
    random_angle = 2 * math.pi * random.random()
    random_angle_vel = 0.2 * random.random() - 0.1
        
    # Spawn a rock
    a_rock = Sprite(random_pos, random_vel, random_angle, random_angle_vel, 
                    asteroid_image, asteroid_info)

# keydown handler
def keydown_handler(key):
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        my_ship.update_angle_vel(key)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.turn_thruster()
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

# keyup handler
def keyup_handler(key):
    if key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        my_ship.recover_angle_vel(key)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.turn_thruster()

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize one ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1, 1], 0, 0, 
                   missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
