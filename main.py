import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1200,1000
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planet Simulation")

BACKGROUND = 'E:/Intermediate Python/Projects/Planet_Simulation/space.png'
background = pygame.image.load(BACKGROUND).convert()
WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (100,149,237)
RED = (188,39,50)
DARK_GREY = (80,78,81)
LIGHT_ORANGE = (255,178,102)
LIGHT_YELLOW = (255,255,204)
PURPLE = (153,51,255)
DARK_BLUE = (51,51,255)

FONT = pygame.font.SysFont("comicsans", 14)


class Planet:
    AU = 149.6e6 * 1000  # distance of earth from sun in meters
    G = 6.67428e-11 # gravitational constant
    SCALE = 150 / AU # 1AU = 100 pixels
    TIMESTEP = 3600*24 # ! day of a planet

    def __init__(self,name,x,y,radius,color,mass,revolution):
        self.x = x
        self.y = y
        self.name = name
        self.radius = radius
        self.color = color
        self.mass = mass
        self.revolution = revolution
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self,win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        if len(self.orbit) > 2:
                updated_points = []
                for point in self.orbit:
                    x, y = point
                    x = x * self.SCALE + WIDTH / 2
                    y = y * self.SCALE + HEIGHT / 2
                    updated_points.append((x, y))
                pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win,self.color,(x,y),self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.revolution,1)} days", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

    def attraction(self, other):
            other_x, other_y = other.x, other.y
            distance_x = other_x - self.x
            distance_y = other_y - self.y
            distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
            if other.sun:
                self.distance_to_sun = distance/10**12
            force = self.G * self.mass * other.mass / distance**2 # f = G(Mm/r**2) 
            theta = math.atan2(distance_y, distance_x)
            force_x = math.cos(theta) * force
            force_y = math.sin(theta) * force
            return force_x, force_y

    def update_position(self, planets):
            total_fx = total_fy = 0
            for planet in planets:
                if self == planet:
                    continue

                fx, fy = self.attraction(planet)
                total_fx += fx
                total_fy += fy

            self.x_vel += total_fx / self.mass * self.TIMESTEP #f = ma a = f/m
            self.y_vel += total_fy / self.mass * self.TIMESTEP

            self.x += self.x_vel * self.TIMESTEP
            self.y += self.y_vel * self.TIMESTEP
            self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet('SUN',0, 0, 32, YELLOW, 1.98892 * 10**30,0)  #in kilograms
    sun.sun = True
    
    earth = Planet('EARTH',-1 * Planet.AU, 0, 20, BLUE, 5.9742 * 10**24,365)
    earth.y_vel = 29.8 * 1000

    mars = Planet('MARS',-1.524 * Planet.AU, 0, 16, RED, 6.39 * 10**23,687)
    mars.y_vel = 24.1 * 1000

    mercury = Planet('MERCURY',0.387 * Planet.AU, 0, 12, DARK_GREY, 3.30 * 10**23,88)
    mercury.y_vel = -47.9 * 1000

    venus = Planet('VENUS',0.723 * Planet.AU, 0, 18, WHITE, 4.8685 * 10**24,224.7)
    venus.y_vel = -35.0 * 1000

    jupiter = Planet('JUPITER',-1.9 * Planet.AU, 0, 26, LIGHT_ORANGE, 4.30 * 10**23,11.9)
    jupiter.y_vel = 21.8 * 1000

    saturn = Planet('SATURN',-2.5 * Planet.AU, 0,24, LIGHT_YELLOW, 3.30 * 10**23,29.5)
    saturn.y_vel = 18.7 * 1000

    uranus = Planet('URANUS',-2.8 * Planet.AU, 0, 22, PURPLE, 5.681 * 10**23,84)
    uranus.y_vel = 17.8 * 1000

    neptune = Planet('NEPTUNE',-3.2 * Planet.AU, 0, 20, DARK_BLUE, 6.024 * 10**23,164.8)
    neptune.y_vel = 16.7 * 1000

    planets = [sun,earth,mars,mercury,venus,jupiter,saturn,uranus,neptune]

    while run:
        clock.tick(60)
        WIN.blit(background, (0, 0))   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()