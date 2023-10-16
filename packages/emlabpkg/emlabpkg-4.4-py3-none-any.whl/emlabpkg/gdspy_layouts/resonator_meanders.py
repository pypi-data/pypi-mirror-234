import numpy as np

import gdspy
lib = gdspy.GdsLibrary()

def create_1_transmission(x, y, path_width, path3_width, gap, inner_angle, length_of_one_segment, loops_after_one, padding, rotation_angle=0, layers=[0, 1], points=43):

    """
    Create 1 GDSII transmission resonator. Doesn't create touch pads or holes. Returns 3 paths, 2 for the meander and a third one that
    envelops the meander for holes. Units are in microns by default.

    Parameters:
        x (float): X-coordinate of the starting point.
        y (float): Y-coordinate of the starting point.
        path_width (float): Width of the paths (film being etched away).
        path3_width (float): Width of the third larger path.
        gap (float): Gap between the first and second paths (the actual meander width).
        inner_angle (float): The diameter of what the first curve should be in microns.
        length_of_one_segment (float): Length of one segment of the hanger.
        loops_after_one (int): Number of loops to create after the first loop and before the last loop.
        padding (float): Padding distance just at the start and end of the meander.
        rotation_angle (float, optional): Rotation angle in degrees (default is 0).
        layers (list of int, optional): List of GDSII layer numbers for each path (default is [0, 1]).
        points (int): The maximum number of points in a polygon (Usually 43 works best).

    Returns:
        tuple: A tuple containing three GDSII Path objects representing the hanger paths.

    Example:
        path1, path2, path3 = create_1_transmission(x=0, y=0, path_width=15, path3_width=95, gap=10,
                                              length_of_one_segment=700, loops_after_one=4,
                                              padding=40, rotation_angle=0)
    """
    
    outer_angle = inner_angle + gap + path_width

    path1 = gdspy.Path(path_width, (x, y))
    path2 = gdspy.Path(path_width, (path_width + gap + x, y))
    path3 = gdspy.Path(path3_width, ((path_width + gap) / 2 + x, (y - padding)))

    path1.segment(40, "+y", layer=layers[0])
    path1.turn(outer_angle, "r", number_of_points=points, layer=layers[0])
    path1.segment(0.8 * length_of_one_segment , "+x", layer=layers[0])
    path1.turn(inner_angle, "ll", number_of_points=points, layer=layers[0])
    path1.segment(length_of_one_segment, "-x", layer=layers[0])
    path1.turn(outer_angle, "rr", number_of_points=points, layer=layers[0])
    for i in range(loops_after_one):
        path1.segment(length_of_one_segment, "+x", layer=layers[0])
        path1.turn(inner_angle, "ll", number_of_points=points, layer=layers[0])
        path1.segment(length_of_one_segment, "-x", layer=layers[0])
        path1.turn(outer_angle, "rr", number_of_points=points)
    path1.segment(length_of_one_segment, "+x", layer=layers[0])
    path1.turn(inner_angle, "ll", number_of_points=points, layer=layers[0])
    path1.segment(length_of_one_segment, "-x", layer=layers[0])
    path1.turn(outer_angle, "r", number_of_points=points, layer=layers[0])
    path1.segment(40, "+y", layer=layers[0])
    path1.rotate(rotation_angle, center=(x, y))

    path2.segment(40, "+y", layer=layers[0])
    path2.turn(inner_angle, "r", number_of_points=points, layer=layers[0])
    path2.segment(0.8 * length_of_one_segment, "+x", layer=layers[0])
    path2.turn(outer_angle, "ll", number_of_points=points, layer=layers[0])
    path2.segment(length_of_one_segment, "-x", layer=layers[0])
    path2.turn(inner_angle, "rr", number_of_points=points, layer=layers[0])
    for i in range(loops_after_one):
        path2.segment(length_of_one_segment, "+x", layer=layers[0])
        path2.turn(outer_angle, "ll", number_of_points=points, layer=layers[0])
        path2.segment(length_of_one_segment, "-x", layer=layers[0])
        path2.turn(inner_angle, "rr", number_of_points=points, layer=layers[0])
    path2.segment(length_of_one_segment, "+x", layer=layers[0])
    path2.turn(outer_angle, "ll", number_of_points=points, layer=layers[0])
    path2.segment(length_of_one_segment, "-x", layer=layers[0])
    path2.turn(inner_angle, "r", number_of_points=points, layer=layers[0])
    path2.segment(40, "+y", layer=layers[0])
    path2.rotate(rotation_angle, center=(x, y))

    path3.segment(padding + 40, "+y", layer=layers[1])
    path3.turn((inner_angle + outer_angle) / 2, "r", layer=layers[1])
    path3.segment(0.8 * length_of_one_segment, "+x", layer=layers[1])
    path3.turn((inner_angle + outer_angle) / 2, "ll", layer=layers[1])
    path3.segment(length_of_one_segment, "-x", layer=layers[1])
    path3.turn((inner_angle + outer_angle) / 2, "rr", layer=layers[1])
    for i in range(loops_after_one):
        path3.segment(length_of_one_segment, "+x", layer=layers[1])
        path3.turn((inner_angle + outer_angle) / 2, "ll", layer=layers[1])
        path3.segment(length_of_one_segment, "-x", layer=layers[1])
        path3.turn((inner_angle + outer_angle) / 2, "rr", layer=layers[1])
    path3.segment(length_of_one_segment, "+x", layer=layers[1])
    path3.turn((inner_angle + outer_angle) / 2, "ll", layer=layers[1])
    path3.segment(length_of_one_segment + (path_width + gap) / 2, "-x", layer=layers[1])
    path3.turn((inner_angle + outer_angle) / 2, "r", layer=layers[1])
    path3.segment(padding + 40, "+y", layer=layers[1])
    path3.rotate(rotation_angle, center=(x, y))
    
    return path1, path2, path3

def create_1_hanger(x, y, path_width, path3_width, gap, inner_angle, length_of_one_segment, loops_after_one, padding, rotation_angle=0, layers=[0, 1], points=43):
    
    """
    Create 1 GDSII hanger resonator. Doesn't create touch pads or holes. Returns 3 paths, 2 for the meander and a third one that
    envelops the meander for holes. Units are in microns by default.

    Parameters:
        x (float): X-coordinate of the starting point.
        y (float): Y-coordinate of the starting point.
        path_width (float): Width of the paths (film being etched away).
        path3_width (float): Width of the third larger path.
        gap (float): Gap between the first and second paths (the actual meander width).
        inner_angle (float): The diameter of what the first curve should be in microns.
        length_of_one_segment (float): Length of one segment of the hanger.
        loops_after_one (int): Number of loops to create after the first loop and before the last loop.
        padding (float): Padding distance just at the start and end of the meander.
        rotation_angle (float, optional): Rotation angle in degrees (default is 0).
        layers (list of int, optional): List of GDSII layer numbers for each path (default is [0, 1]).
        points (int): The maximum number of points in a polygon (Usually 43 works best).

    Returns:
        tuple: A tuple containing three GDSII Path objects representing the hanger paths.

    Example:
        path1, path2, path3 = create_1_hanger(x=0, y=0, path_width=15, path3_width=95, gap=10,
                                              length_of_one_segment=700, loops_after_one=4,
                                              padding=40, rotation_angle=0)
    """
    
    outer_angle = inner_angle + gap + path_width

    path1 = gdspy.Path(path_width, (x, y))
    path2 = gdspy.Path(path_width, (path_width + gap + x, y))
    path3 = gdspy.Path(path3_width, ((path_width + gap) / 2 + x, (y - padding)))

    path1.segment(40, "+y", layer=layers[0])
    path1.turn(outer_angle, "r", number_of_points=points, layer=layers[0])
    path1.segment(0.8 * length_of_one_segment , "+x", layer=layers[0])
    path1.turn(inner_angle, "ll", number_of_points=points, layer=layers[0])
    path1.segment(length_of_one_segment, "-x", layer=layers[0])
    path1.turn(outer_angle, "rr", number_of_points=points, layer=layers[0])
    for i in range(loops_after_one):
        path1.segment(length_of_one_segment, "+x", layer=layers[0])
        path1.turn(inner_angle, "ll", number_of_points=points, layer=layers[0])
        path1.segment(length_of_one_segment, "-x", layer=layers[0])
        path1.turn(outer_angle, "rr", number_of_points=points)
    path1.segment(length_of_one_segment * 2 / 3, "+x", layer=layers[0])
    path1.turn(inner_angle, "ll", number_of_points=points, layer=layers[0])
    path1.segment(length_of_one_segment / 2, "-x", layer=layers[0])
    path1.turn((gap + path_width) / 2, "rr", number_of_points=points, layer=layers[0])
    path1.rotate(rotation_angle, center=(x, y))

    path2.segment(40, "+y", layer=layers[0])
    path2.turn(inner_angle, "r", number_of_points=points, layer=layers[0])
    path2.segment(0.8 * length_of_one_segment, "+x", layer=layers[0])
    path2.turn(outer_angle, "ll", number_of_points=points, layer=layers[0])
    path2.segment(length_of_one_segment, "-x", layer=layers[0])
    path2.turn(inner_angle, "rr", number_of_points=points, layer=layers[0])
    for i in range(loops_after_one):
        path2.segment(length_of_one_segment, "+x", layer=layers[0])
        path2.turn(outer_angle, "ll", number_of_points=points, layer=layers[0])
        path2.segment(length_of_one_segment, "-x", layer=layers[0])
        path2.turn(inner_angle, "rr", number_of_points=points, layer=layers[0])
    path2.segment(length_of_one_segment * 2 / 3, "+x", layer=layers[0])
    path2.turn(outer_angle, "ll", number_of_points=points, layer=layers[0])
    path2.segment(length_of_one_segment / 2, "-x", layer=layers[0])
    path2.rotate(rotation_angle, center=(x, y))

    path3.segment(padding + 40, "+y", layer=layers[1])
    path3.turn((inner_angle + outer_angle) / 2, "r", layer=layers[1])
    path3.segment(0.8 * length_of_one_segment, "+x", layer=layers[1])
    path3.turn((inner_angle + outer_angle) / 2, "ll", layer=layers[1])
    path3.segment(length_of_one_segment, "-x", layer=layers[1])
    path3.turn((inner_angle + outer_angle) / 2, "rr", layer=layers[1])
    for i in range(loops_after_one):
        path3.segment(length_of_one_segment, "+x", layer=layers[1])
        path3.turn((inner_angle + outer_angle) / 2, "ll", layer=layers[1])
        path3.segment(length_of_one_segment, "-x", layer=layers[1])
        path3.turn((inner_angle + outer_angle) / 2, "rr", layer=layers[1])
    path3.segment(length_of_one_segment * 2 / 3, "+x", layer=layers[1])
    path3.turn((inner_angle + outer_angle) / 2, "ll", layer=layers[1])
    path3.segment(length_of_one_segment / 2 + (path_width + gap) / 2 + padding, "-x", layer=layers[1])
    path3.rotate(rotation_angle, center=(x, y))
    
    return path1, path2, path3


# Need to ensure this works and add docstring use case etc.
def make_touch_pad_for_feedline(feedline_left, feedline_right, direction, length_of_pad=200, width_of_pad=200, thickness_of_pad=50):
    
    if direction == "+y":
        
        poly1 = feedline_left.polygons[0]
        poly2 = feedline_right.polygons[0]
        
        feedline_width = np.abs(feedline_left.polygons[0][0][0]) + np.abs(feedline_left.polygons[0][1][0])
        diff = thickness_of_pad - feedline_width
        x_constant = 95
        y_constant = 75
        
        points = [poly1[1], poly1[0], poly1[0] - [x_constant + diff, y_constant], 
                  poly1[0] - [x_constant + diff, y_constant + length_of_pad + thickness_of_pad], 
                  poly2[1] + [x_constant + diff, -(y_constant + length_of_pad + thickness_of_pad)], 
                  poly2[1] + [x_constant + diff, -(y_constant)], poly2[1], poly2[0], 
                  poly2[0] + [x_constant, -(y_constant)], poly2[0] + [x_constant, -(y_constant + length_of_pad)], 
                  poly1[1] - [x_constant, y_constant + length_of_pad], poly1[1] - [x_constant, y_constant], poly1[1]]
        pad = gdspy.Polygon(points, layer=0)
        
        return pad
    
    if direction == "-y":
        
        poly1 = feedline_left.polygons[0]
        poly2 = feedline_right.polygons[0]
        
        feedline_width = np.abs(feedline_left.polygons[0][3][0]) + np.abs(feedline_left.polygons[0][2][0])
        diff = thickness_of_pad - feedline_width
        x_constant = 95
        y_constant = 75 
        
        points = [poly1[2], poly1[3], poly1[3] - [x_constant + diff, -(y_constant)], 
                  poly1[3] - [x_constant + diff, -(y_constant + length_of_pad + thickness_of_pad)], 
                  poly2[2] + [x_constant + diff, (y_constant + length_of_pad + thickness_of_pad)], 
                  poly2[2] + [x_constant + diff, y_constant], poly2[2], poly2[3], poly2[3] + [x_constant, y_constant], 
                  poly2[3] + [x_constant, y_constant + width_of_pad], poly1[2] - [x_constant, -(y_constant + width_of_pad)], 
                  poly1[2] - [x_constant, -(y_constant)], poly1[2]]
        pad = gdspy.Polygon(points, layer=0)
        
        return pad