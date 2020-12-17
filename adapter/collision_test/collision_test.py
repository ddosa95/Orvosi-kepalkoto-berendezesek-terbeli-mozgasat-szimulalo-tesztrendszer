import numpy as np


def add_axes(a_part, b_part):  ########### Tudom, hogy undorító, még kitalálom, hogyan tudnám megoldani
    axes = []
    for unit_vector in a_part['unit_vectors'].values():
        axes.append(unit_vector)

    for unit_vector in b_part['unit_vectors'].values():
        axes.append(unit_vector)

    for a_unit_vector in a_part['unit_vectors'].values():
        for b_unit_vector in a_part['unit_vectors'].values():
            axes.append(np.cross(a_unit_vector, b_unit_vector))

    return axes


def are_collision(a_part, b_part):
    a_params = a_part.get_collision_test_parameters()
    b_params = b_part.get_collision_test_parameters()

    axes = add_axes(a_params, b_params)

    t = np.subtract(b_params['position'], a_params['position'])

    for axis in axes:
        inequality_left = np.absolute(np.dot(t, axis))

        inequality_right = np.absolute(
            np.dot(a_params['half_axis'] * a_params['unit_vectors']['axis_parallel'], np.transpose(axis))) + \
                           np.absolute(np.dot(a_params['half_up'] * a_params['unit_vectors']['up_parallel'],
                                              np.transpose(axis))) + \
                           np.absolute(np.dot(a_params['half_face'] * a_params['unit_vectors']['face_parallel'],
                                              np.transpose(axis))) + \
                           np.absolute(np.dot(b_params['half_axis'] * b_params['unit_vectors']['axis_parallel'],
                                              np.transpose(axis))) + \
                           np.absolute(np.dot(b_params['half_up'] * b_params['unit_vectors']['up_parallel'],
                                              np.transpose(axis))) + \
                           np.absolute(np.dot(b_params['half_face'] * b_params['unit_vectors']['face_parallel'],
                                              np.transpose(axis)))

        if inequality_left > inequality_right:
            return False

    return True
