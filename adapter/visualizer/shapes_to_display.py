from OpenGL.GL import *
from adapter.visualizer import visualizer_constants as v


def arrows():
    glBegin(GL_LINES)
    x = 0
    for axis in v.COORDINATE_AXLES:
        for vertex in axis:
            glColor3fv(v.ARROWS_COLORS[x])
            glVertex3fv(v.COORDINATE_LINES[vertex])
        x += 1
    glEnd()

    x = 0
    for arrow in v.ARROWS:

        glBegin(GL_TRIANGLES)
        for surface in v.ARROW_SURFACES:
            for vertex in surface:
                glColor3fv(v.ARROWS_COLORS[x])
                glVertex3fv(arrow[vertex])
        glEnd()

        glBegin(GL_QUADS)
        for vertex in (0, 1, 2, 3):
            glColor3fv(v.ARROWS_COLORS[x])
            glVertex3fv(arrow[vertex])
        glEnd()
        x += 1


def boundary_box(vertices):
    glBegin(GL_QUADS)
    for surface in v.SURFACE:
        x = 0
        for vertex in surface:
            x += 1
            glColor3fv(v.COLORS[x])
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in v.EDGES:
        for vertex in edge:
            glColor3fv([1, 1, 1])
            glVertex3fv(vertices[vertex])
    glEnd()
