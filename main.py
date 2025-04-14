import matplotlib.pyplot as p
import numpy as np
import pygame
import config
import time
import math


def z(z, c):
    return z**2 + c


def point_in_mandelbrot(c, max_iterations):
    z_val = 0
    i = 0
    while i < max_iterations:
        z_val = z(z_val, c)
        if abs(z_val) > 2:
            return (i, False)
        i += 1
    return (i, True)


def generate_mandelbrot(points, max_iterations):
    M = []
    x = np.linspace(-2.0, 1.0, points)
    y = np.linspace(-1.5, 1.5, points)

    for p_x in x:
        for p_y in y:
            c = complex(p_x, p_y)
            if point_in_mandelbrot(c, max_iterations):
                M.append(c)
    return M


def g_mandelbrot_pygame(max_iterations, xmin, xmax, ymin, ymax):

    points = config.window_x * config.window_y
    count = 0
    for p_x in range(config.window_x):
        for p_y in range(config.window_y):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

            x = xmin + (p_x / config.window_x) * (xmax - xmin)
            y = ymax - (p_y / config.window_y) * (ymax - ymin)
            c = complex(x, y)
            iterations_taken, in_mandelbrot = point_in_mandelbrot(c, max_iterations)
            if in_mandelbrot:
                config.screen.set_at((p_x, p_y), (0, 0, 0))
            else:
                value = math.log(iterations_taken + 1) / math.log(max_iterations)
                r = int(255 * value)
                g = int(255 * (value**0.5))
                b = 255 - r
                color = (r, g, b)
                config.screen.set_at((p_x, p_y), color)
            pygame.display.flip()
            count += 1
            print(f"Computed {count} out of {points} points")


if __name__ == "__main__":
    # Simple plot:
    # M = generate_mandelbrot(1000, 50)
    # p.scatter([c.real for c in M], [c.imag for c in M], s=0.1, color="black")
    # p.show()

    # Running Visualisation:
    pygame.init()
    running = True
    config.screen.fill((255, 255, 255))
    start = time.time()
    max_iterations = 1000
    xmin, xmax, ymin, ymax = (-1.5, -1, 0, 0.5)
    g_mandelbrot_pygame(max_iterations, xmin, xmax, ymin, ymax)
    end = time.time()
    print(f"Time taken: {end - start:.4f} seconds")
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                elif event.key == pygame.K_0:
                    pygame.image.save(
                        config.screen,
                        f"mandelbrot_max_iters{max_iterations}_size{config.size}_xaxis{xmin}v{xmax}_yaxis{ymin}v{ymax}.jpeg",
                    )
