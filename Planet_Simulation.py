import pygame
import math
pygame.init()

WIDTH, HEIGHT = (1000,750)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (188,39,50)
BLUE = (100,149,237)
GREEN = (0,255,0)
YELLOW = (255,255,0)
DARK_GREY = (80,78,81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000 #AU in meters => *1000
    G = 6.674288e-11
    SCALE = 250/AU # 1AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius 
        self.color = color 
        self.mass = mass 
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0

        self.fx_magnetude = 0
        self.fy_magnetude = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y))
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        pygame.draw.circle(win, self.color, (x,y), self.radius)
        # if not self.sun:
        #     distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)}km",1,WHITE)
        #     win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
        if not self.sun:
            pygame.draw.line(win,YELLOW, [x,y],[self.fx_magnetude + WIDTH / 2, y], 3)
            # pygame.draw.line(win,YELLOW, [x,y],[x, self.fy_magnetude + HEIGHT/2], 3)
    
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        # print("dist_x:",distance_x,", dist_y:",distance_y)

        if other.sun:
            self.distance_to_sun = distance 
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        # print("theta: ", theta, ",F=",force)

        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        # print("t:", theta,", cos(t): ", math.cos(theta),", sin(t): ", math.sin(theta))
        # print("fx: ", force_x, ", fy: ", force_y)
        # print("fy/fx:", force_y/force_x)
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy 

        self.x_vel += total_fx / self.mass * self.TIMESTEP # F = ma, a = F/m, a*t = v
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        # print("tfx:", total_fx, ", tfy:",total_fy)
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
        # print(len(self.orbit))
        self.fx_magnetude = total_fx / 10000000000000000000000000000000
        # self.fy_magnetude = total_fy / 10000000000000000000000000000000
        print("fx_mag: ", self.fx_magnetude, ", fy_mag: ", self.fy_magnetude)

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0,0,30,YELLOW,1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000
    mars = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000
    mercury = Planet(0.387*Planet.AU, 0, 8, DARK_GREY, 3.30* 10**23)
    mercury.y_vel = -47.4 * 1000
    venus = Planet(0.723*Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000
    
    planets = [sun, earth, mars, mercury, venus]
    # planets = [sun, earth]
    while run:
        clock.tick(FPS)
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
    pygame.quit()
main()