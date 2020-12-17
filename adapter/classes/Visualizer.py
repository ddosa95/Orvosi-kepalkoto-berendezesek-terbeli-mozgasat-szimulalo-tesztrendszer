import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from adapter.visualizer import visualizer_constants as v, shapes_to_display
import numpy as np


class Visualizer:
    def __init__(self):
        self.is_rotating = False
        self.mx = 0
        self.my = 0
        self.is_running = True
        pygame.init()
        pygame.display.set_mode(v.DISPLAY, DOUBLEBUF | OPENGL)
        gluPerspective(45, (v.DISPLAY[0] / v.DISPLAY[1]), 0.1, 1000.0)
        glTranslatef(-200, -100, -655)
        glRotatef(20, 2, 1, 0)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)


    def render(self, simulation):

        mx_minus = self.mx
        my_minus = self.my
        self.mx, self.my = pygame.mouse.get_pos()

        if self.is_rotating:
            x_rot_angle = self.my - my_minus
            y_rot_angle = self.mx - mx_minus
        else:
            x_rot_angle = 0
            y_rot_angle = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    glTranslatef(10, 0, 0)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    glTranslatef(-10, 0, 0)
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    glTranslatef(0, -10, 0)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    glTranslatef(0, 10, 0)
                if event.key == pygame.K_p:
                    simulation.simulation_is_running = not simulation.simulation_is_running
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                    self.is_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    mouse_zoom_position = np.array([(v.DISPLAY[0] / 2 - self.mx), (v.DISPLAY[1] / 2 - self.my)])
                    x_shift = np.dot(mouse_zoom_position, v.X_VECTOR) / 20
                    y_shift = np.dot(mouse_zoom_position, v.Y_VECTOR) / 20
                    glTranslatef(x_shift, y_shift * -1, 10)

                if event.button == 5:
                    glTranslatef(0, 0, -10)

                if event.button == 1:
                    self.is_rotating = True

            if event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.is_rotating = False

        glRotatef(x_rot_angle, 1, 0, 0)
        glRotatef(y_rot_angle, 0, 1, 0)

        shapes_to_display.arrows()
        for part in simulation.dict_of_parts.values():
            shapes_to_display.boundary_box(part.calculate_vertices())
        pygame.display.flip()
        pygame.time.wait(10)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)