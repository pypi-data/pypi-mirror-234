import numpy as np

import gdspy
lib = gdspy.GdsLibrary()

def create_1_transmission(path_width, path3_width, gap, inner_angle, length_of_one_segment, total_loops, padding=40, rotation_angle=0, layers=[0, 1], points=43, x=0, y=0, first_seg_length=None,
                          last_seg_length=None, want_touch_pads=False):
    
    """
    Create 1 GDSII transmission resonator. Doesn't create touch pads or holes. Returns 3 paths, 2 for the meander and a third one that
    envelops the meander for holes. Units are in microns by default.

    Parameters:
        path_width (float): Width of the paths (film being etched away).
        path3_width (float): Width of the third larger path.
        gap (float): Gap between the first and second paths (the actual meander width).   
        inner_angle (float): The diameter of what the first curve should be in microns.
        length_of_one_segment (float): Length of one segment of the hanger.
        total_loops (int): Number of loops to create.
        padding (float, optional): Padding distance just at the start and end of the meander (default is 40).
        rotation_angle (float, optional): Rotation angle in degrees (default is 0) (unit in radians).
        layers (list of int, optional): List of GDSII layer numbers for each path (default is [0, 1]).
        points (int, optional): The maximum number of points in a polygon (default is 43).
        x (float, optional): X-coordinate of the starting point (default is 0).
        y (float, optional): Y-coordinate of the starting point (default is 0).
        first_seg_length (float, optional): Length of the first segment (default is 0.8 * length_of_one_segment).
        last_seg_length (float, optional): Length of the last segment (default is 0.8 * length_of_one_segment).

    Returns:
        tuple: A tuple containing three GDSII Path objects representing the hanger paths.

    Example:
        path1, path2, path3 = create_1_transmission(path_width=15, path3_width=95, gap=10, inner_angle=50,
                                              length_of_one_segment=700, total_loops=4)
    """

    if first_seg_length is None:
        first_seg_length = 0.8 * length_of_one_segment
    if last_seg_length is None:
        last_seg_length = 0.8 * length_of_one_segment

    loops_after_one =- total_loops - 2
    outer_angle = inner_angle + gap + path_width

    path1 = gdspy.Path(path_width, (x, y))
    path2 = gdspy.Path(path_width, (path_width + gap + x, y))
    path3 = gdspy.Path(path3_width, ((path_width + gap) / 2 + x, (y - padding)))

    path1.segment(40, "+y", layer=layers[0])
    path1.turn(outer_angle, "r", number_of_points=points, layer=layers[0])
    path1.segment(first_seg_length , "+x", layer=layers[0])
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
    path1.segment(last_seg_length, "-x", layer=layers[0])
    path1.turn(outer_angle, "r", number_of_points=points, layer=layers[0])
    path1.segment(40, "+y", layer=layers[0])

    path2.segment(40, "+y", layer=layers[0])
    path2.turn(inner_angle, "r", number_of_points=points, layer=layers[0])
    path2.segment(first_seg_length, "+x", layer=layers[0])
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
    path2.segment(last_seg_length, "-x", layer=layers[0])
    path2.turn(inner_angle, "r", number_of_points=points, layer=layers[0])
    path2.segment(40, "+y", layer=layers[0])

    path3.segment(padding + 40, "+y", layer=layers[1])
    path3.turn((inner_angle + outer_angle) / 2, "r", layer=layers[1])
    path3.segment(first_seg_length, "+x", layer=layers[1])
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
    path3.segment(last_seg_length, "-x", layer=layers[1])
    path3.turn((inner_angle + outer_angle) / 2, "r", layer=layers[1])
    path3.segment(padding + 40, "+y", layer=layers[1])

    if want_touch_pads:
        pad1 = make_touch_pad_for_transmission_resonator(path1, path2, '+y')
        pad2 = make_touch_pad_for_transmission_resonator(path1, path2, '-y')

        path1.rotate(rotation_angle, center=(x, y))
        path2.rotate(rotation_angle, center=(x, y))
        path3.rotate(rotation_angle, center=(x, y))
        pad1.rotate(rotation_angle, center=(x, y))
        pad2.rotate(rotation_angle, center=(x, y))

        return path1, path2, path3, pad1, pad2

    else:
        path1.rotate(rotation_angle, center=(x, y))
        path2.rotate(rotation_angle, center=(x, y))
        path3.rotate(rotation_angle, center=(x, y))
        
        return path1, path2, path3

def create_1_hanger(path_width, path3_width, gap, inner_angle, length_of_one_segment, total_loops, padding, rotation_angle=0, layers=[0, 1], points=43, x=0, y=0, first_seg_length=None, coupler_length=None):
    
    """
    Create 1 GDSII hanger resonator. Doesn't create touch pads or holes. Returns 3 paths, 2 for the meander and a third one that
    envelops the meander for holes. Units are in microns by default.

    Parameters:
        path_width (float): Width of the paths (film being etched away).
        path3_width (float): Width of the third larger path.
        gap (float): Gap between the first and second paths (the actual meander width).   
        inner_angle (float): The diameter of what the first curve should be in microns.
        length_of_one_segment (float): Length of one segment of the hanger.
        total_loops (int): Number of loops to create.
        padding (float, optional): Padding distance just at the start and end of the meander (default is 40).
        rotation_angle (float, optional): Rotation angle in degrees (default is 0) (unit in radians).
        layers (list of int, optional): List of GDSII layer numbers for each path (default is [0, 1]).
        points (int, optional): The maximum number of points in a polygon (default is 43).
        x (float, optional): X-coordinate of the starting point (default is 0).
        y (float, optional): Y-coordinate of the starting point (default is 0).
        first_seg_length (float, optional): Length of the first segment (default is 0.95 * length_of_one_segment).
        last_seg_length (float, optional): Length of the last segment (default is 0.95 * length_of_one_segment).

    Returns:
        tuple: A tuple containing three GDSII Path objects representing the hanger paths.

    Example:
        path1, path2, path3 = create_1_hanger(path_width=15, path3_width=95, gap=10, inner_angle=50,
                                              length_of_one_segment=700, total_loops=4, coupler_length=600)
    """

    if first_seg_length is None:
        first_seg_length = 0.95 * length_of_one_segment
    if coupler_length is None:
        coupler_length = 0.95 * length_of_one_segment

    loops_after_one = total_loops - 2
    outer_angle = inner_angle + gap + path_width

    path1 = gdspy.Path(path_width, (x, y))
    path2 = gdspy.Path(path_width, (x, path_width + gap + y))
    path3 = gdspy.Path(path3_width, (x - padding), (path_width + gap) / 2 + y)
    path3 = gdspy.Path(path3_width, ((path_width + gap) / 2 + x, (y - padding)))

    path1.segment(first_seg_length, "+x", layer=layers[0])
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
    path1.segment(coupler_length, "-x", layer=layers[0])
    path1.turn((gap + path_width) / 2, "rr", number_of_points=points, layer=layers[0])

    path2.segment(first_seg_length, "+x", layer=layers[0])
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
    path2.segment(coupler_length, "-x", layer=layers[0])

    path3.segment(first_seg_length + padding, "+x", layer=layers[1])
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
    path3.segment(coupler_length + (path_width + gap) / 2 + padding, "-x", layer=layers[1])

    path1.rotate(rotation_angle, center=(x, y))
    path2.rotate(rotation_angle, center=(x, y))
    path3.rotate(rotation_angle, center=(x, y))

    return path1, path2, path3

def make_touch_pad_for_transmission_resonator(feedline_left, feedline_right, direction, length_of_pad=200, width_of_pad=200, thickness_of_pad=50):
    
    """
    Creates a touch pad for a transmission resonator. Units are in microns by default.

    Parameters:
        feedline_left (gdspy.Path): The left feedline (path1) of the transmission resonator.
        feedline_right (gdspy.Path): The right feedline (path2) of the transmission resonator.
        direction (str): The direction of the transmission line. Either "+y" (upward) or "-y" (downward).
        length_of_pad (float, optional): The length of the touch pad (default is 200 units).
        width_of_pad (float, optional): The width of the touch pad (default is 200 units).
        thickness_of_pad (float, optional): The thickness of the touch pad (default is 50 units).

    Returns:
        gdspy.Polygon: A Polygon object representing the generated touch pad.

    Example:
        # Create a touch pad for a transmission resonator with upward direction
        pad = make_touch_pad_for_transmission_resonator(path1, path2, direction="+y")
    """

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
        
        poly1 = feedline_left.polygons[-1]
        poly2 = feedline_right.polygons[-1]
        
        feedline_width = np.abs(feedline_left.polygons[-1][3][0]) + np.abs(feedline_left.polygons[-1][2][0])
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