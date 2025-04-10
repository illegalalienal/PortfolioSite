import random
import noise

import pygame
import sys

def main():
    # Initialize pygame
    pygame.init()

    # Constants
    isovalue = 0.5
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    dt = 0

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    # Initialize the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Marching Squares")
    clock = pygame.time.Clock()


    # initialize the grid
    grid = []
    rez = 10
    for i in range((WIDTH // rez) + 1):
        row = []
        for j in range((HEIGHT // rez) + 1):
            #value = random.randint(0, 1)
            value = random.randint(0, 1)
            row.append(1 if value >= 1 else 0)
        grid.append(row)
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Fill the screen
        screen.fill("white")


        # Update the grid
        raw_values = []
        for i in range((WIDTH // rez) + 1):
            #row = []

            for j in range((HEIGHT // rez) + 1):
                zoom = 0.1
                zoom_diff = 0.01
                zoom = zoom + zoom_diff * dt
                x_speed = 0
                y_speed = 0
                value = noise.snoise2((i * zoom) + dt*x_speed, (j * zoom) - dt*y_speed)
                #row.append(value)

                # clamp input to between 0 and 1
                grid[i][j] = (value + 1) / 2
            #raw_values.append(row)

        # Draw the grid
        for i in range((WIDTH // rez) + 1):
            for j in range((HEIGHT // rez) + 1):
                # for each dot, draw a circle of darkness depending on the value
                red = 255 * grid[i][j]
                green = 255 * grid[i][j]
                blue = 255 * grid[i][j]

                pygame.draw.circle(screen, (red, green, blue), (i * rez, j * rez), rez // 4)

                """
                if grid[i][j] > isovalue:
                    pygame.draw.circle(screen, BLACK, (i * rez, j * rez), rez // 4)
                    pass
                else:
                    pygame.draw.circle(screen, WHITE, (i * rez, j * rez), rez // 4)
                    pass
                """


        # draw the marching squares
        for i in range((WIDTH // rez)):
            for j in range((HEIGHT // rez)):

                # define corners
                top_left = grid[i][j]
                top_right = grid[i + 1][j]
                bottom_left = grid[i][j + 1]
                bottom_right = grid[i + 1][j + 1]

                # get corner coordinates
                tl_coords = (i * rez, j * rez)
                tr_coords = (i * rez + rez, j * rez)
                bl_coords = (i * rez, j * rez + rez)
                br_coords = (i * rez + rez, j * rez + rez)

                # define midpoints
                # a = top middle
                a = (i * rez + (rez // 2), j * rez)
                # b = right middle
                b = (i * rez + rez, j * rez + (rez // 2))
                # c = bottom middle
                c = (i * rez + (rez // 2), j * rez + rez)
                # d = left middle
                d = (i * rez, j * rez + (rez // 2))

                # Helper function for interpolation with zero check
                def interpolate(a, b, fa, fb):
                    if abs(fa - fb) < 1e-5:  # Avoid division by zero
                        return 0.5
                    return (isovalue - fa) / (fb - fa)

                # Check which edges cross the isovalue
                cell_size = rez

                # Initialize points to None
                top_point = right_point = bottom_point = left_point = None

                # Top edge
                if (top_left > isovalue) != (top_right > isovalue):
                    t = interpolate(tl_coords[0], tr_coords[0], top_left, top_right)
                    top_point = (tl_coords[0] + t * cell_size, tl_coords[1])

                # Right edge
                if (top_right > isovalue) != (bottom_right > isovalue):
                    t = interpolate(tr_coords[1], br_coords[1], top_right, bottom_right)
                    right_point = (tr_coords[0], tr_coords[1] + t * cell_size)

                # Bottom edge
                if (bottom_left > isovalue) != (bottom_right > isovalue):
                    t = interpolate(bl_coords[0], br_coords[0], bottom_left, bottom_right)
                    bottom_point = (bl_coords[0] + t * cell_size, bl_coords[1])

                # Left edge
                if (top_left > isovalue) != (bottom_left > isovalue):
                    t = interpolate(tl_coords[1], bl_coords[1], top_left, bottom_left)
                    left_point = (tl_coords[0], tl_coords[1] + t * cell_size)

                # Get the case using binary values
                tl_bin = 1 if top_left > isovalue else 0
                tr_bin = 1 if top_right > isovalue else 0
                br_bin = 1 if bottom_right > isovalue else 0
                bl_bin = 1 if bottom_left > isovalue else 0

                case = tl_bin * 8 + tr_bin * 4 + br_bin * 2 + bl_bin * 1

                # Draw the lines based on the case
                line_color = BLACK
                line_thickness = 5
                if case == 1:  # Only bottom-left is above isovalue
                    if left_point and bottom_point:
                        pygame.draw.line(screen, line_color, left_point, bottom_point, line_thickness)
                elif case == 2:  # Only bottom-right is above isovalue
                    if bottom_point and right_point:
                        pygame.draw.line(screen, line_color, bottom_point, right_point, line_thickness)
                elif case == 3:  # Both bottom corners are above isovalue
                    if left_point and right_point:
                        pygame.draw.line(screen, line_color, left_point, right_point, line_thickness)
                elif case == 4:  # Only top-right is above isovalue
                    if top_point and right_point:
                        pygame.draw.line(screen, line_color, top_point, right_point, line_thickness)
                elif case == 5:  # Top-right and bottom-left are above isovalue (ambiguous case)
                    if top_point and left_point:
                        pygame.draw.line(screen, line_color, top_point, left_point, line_thickness)
                    if bottom_point and right_point:
                        pygame.draw.line(screen, line_color, bottom_point, right_point, line_thickness)
                elif case == 6:  # Right edge is above isovalue
                    if top_point and bottom_point:
                        pygame.draw.line(screen, line_color, top_point, bottom_point, line_thickness)
                elif case == 7:  # All except top-left are above isovalue
                    if top_point and left_point:
                        pygame.draw.line(screen, line_color, top_point, left_point, line_thickness)
                elif case == 8:  # Only top-left is above isovalue
                    if top_point and left_point:
                        pygame.draw.line(screen, line_color, top_point, left_point, line_thickness)
                elif case == 9:  # Left edge is above isovalue
                    if top_point and bottom_point:
                        pygame.draw.line(screen, line_color, top_point, bottom_point, line_thickness)
                elif case == 10:  # Top-left and bottom-right are above isovalue (ambiguous case)
                    if top_point and right_point:
                        pygame.draw.line(screen, line_color, top_point, right_point, line_thickness)
                    if bottom_point and left_point:
                        pygame.draw.line(screen, line_color, bottom_point, left_point, line_thickness)
                elif case == 11:  # All except top-right are above isovalue
                    if top_point and right_point:
                        pygame.draw.line(screen, line_color, top_point, right_point, line_thickness)
                elif case == 12:  # Top edge is above isovalue
                    if left_point and right_point:
                        pygame.draw.line(screen, line_color, left_point, right_point, line_thickness)
                elif case == 13:  # All except bottom-right are above isovalue
                    if bottom_point and right_point:
                        pygame.draw.line(screen, line_color, bottom_point, right_point, line_thickness)
                elif case == 14:  # All except bottom-left are above isovalue
                    if bottom_point and left_point:
                        pygame.draw.line(screen, line_color, bottom_point, left_point, line_thickness)
                # Cases 0 and 15 don't have lines (all below or all above)




        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        dt += 1/FPS
        clock.tick(FPS)

    # Quit pygame
    pygame.quit()
    sys.exit()

def corners_to_case(top_left, top_right, bottom_right, bottom_left):
    return top_left * 8 + top_right * 4 + bottom_right * 2 + bottom_left * 1

main()