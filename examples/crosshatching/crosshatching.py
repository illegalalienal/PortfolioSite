import imageio.v2 as imageio
import pygame
import numpy as np
from PIL import Image

async def main():

    # read image using imageio
    image_array = imageio.imread('bird.jpeg')
    target_width = 600
    target_height = 500

    pil_image = Image.fromarray(image_array)
    resized = pil_image.resize((target_width, target_height), Image.LANCZOS)
    image_array = np.array(resized).astype(np.int32)

    HEIGHT, WIDTH = image_array.shape[0], image_array.shape[1]
    print(f'Image Resolution: {WIDTH}x{HEIGHT}')
    cell_size = 10
    HEIGHT -= HEIGHT % cell_size
    WIDTH -= WIDTH % cell_size
    image_array = image_array[:HEIGHT, :WIDTH]

    cell_area = cell_size * cell_size
    print(f'Cell Size: {cell_size}')
    cells_wide, cells_high = WIDTH // cell_size, HEIGHT // cell_size
    print(f'Cell Resolution: {cells_wide}x{cells_high}')

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True
    screen.fill('white')
    pygame.display.update()


    avg_light_rows = [0] * cells_high
    avg_light_cols = [0] * cells_wide

    for i in range(0, image_array.shape[0], cell_size):
        for j in range(0, image_array.shape[1], cell_size):
            # print telemetry
            #print(f'Processing cell ({i//cell_size}, {j//cell_size})')
            # get the average light of the cell

            # define cell as 2d array
            cell = image_array[i:i+cell_size, j:j+cell_size]
            #cell = image_array[i:i+cell_size, j:j+cell_size]
            #cell = image_array[j:j+cell_size, i:i+cell_size]

            # calculate average light in cell
            total_light = 0
            total_red, total_green, total_blue = 0, 0, 0

            for k in range(cell_size):
                for l in range(cell_size):
                    pixel = cell[k, l]
                    #print(f'\tProcessing pixel {k, l}')
                    red, green, blue = pixel[:3]
                    total_red += red
                    total_green += green
                    total_blue += blue
                    light = (.2126 * pixel[0] + .7152 * pixel[1] + .0722 * pixel[2])/255

                    #print(f'\t light value: {light}')

                    #print(f'\n{k*5 + l}')
                    #print(f'\t(cell_x, cell_y), (pixel_x, pixel_y), light -> ({i},{j}), ({k},{l}), {light:.2f}')
                    #print(f'\t(pixel_r, pixel_g, pixel_b), (total_r, total_g, total_b) -> ({red}, {green}, {blue}), ({total_red}, {total_green}, {total_blue})')
                    total_light += light

            average_light = total_light/cell_area

            avg_red = total_red / cell_area
            avg_green = total_green / cell_area
            avg_blue = total_blue / cell_area

            color = (avg_red, avg_green, avg_blue)

            #print(f'(total_red, total_green, total_blue) -> ({total_red}, {total_green}, {total_blue})')
            #print(f'avg_light, (avg_red, avg_green, avg_blue), (color_r, color_g, color_b) -> {average_light:.2f}, ({avg_red}, {avg_green}, {avg_blue}), ({color[0]}, {color[1]}, {color[2]})')

            # draw lines in cell
            line_distance = max(1, int(cell_size * average_light))
            start_buffer = line_distance
            for k in range(0, cell_size, line_distance):
                # vertical
                pygame.draw.line(screen, color, (i + k, j), (i + k, j + cell_size), 1)
                # horizontal
                pygame.draw.line(screen, color, (i, j + k), (i + cell_size, j + k), 1)
                pygame.display.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

main()