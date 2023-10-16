import numpy as np
import gdspy

class HangerConfiguration:
    def __init__(self, path_width, path3_width, gap, inner_angle, length_of_one_segment, total_loops, padding=40, 
                 rotation_angle=0, layers=[0, 1], points=43, x=0, y=0, first_seg_length=None, coupler_length=None, 
                 want_feedline_and_pads=False, feedline_extend_length=0, feedline_width=0, feedline_path_width=0,
                 coupler_gap=0):
        self.path_width = path_width
        self.path3_width = path3_width
        self.gap = gap
        self.inner_angle = inner_angle
        self.length_of_one_segment = length_of_one_segment
        self.total_loops = total_loops
        self.padding = padding
        self.rotation_angle = rotation_angle
        self.layers = layers
        self.points = points
        self.x = x
        self.y = y
        self.first_seg_length = first_seg_length
        self.coupler_length = coupler_length
        self.want_feedline_and_pads = want_feedline_and_pads
        self.feedline_extend_length = feedline_extend_length
        self.feedline_width = feedline_width
        self.feedline_path_width = feedline_path_width
        self.coupler_gap = coupler_gap
        self.outer_angle = self.inner_angle + self.gap + self.path_width

class HangerArrayConfiguration:
    def __init__(self, config, num_hangers_bottom, num_hangers_top, feedline_width, feedline_path_width):
        if isinstance(config, list):
            if len(config) == 2:
                if len(config[0]) == num_hangers_bottom and len(config[1]) == num_hangers_top:
                    self.configs = config
                elif len(config[0]) == 1 and len(config[1]) == 1:
                    self.configs = [config[0] * num_hangers_bottom, config[1] * num_hangers_top]
                else:
                    raise AttributeError("Length of the sublists of config objects should match the number of resonators.")
            else:
                raise AttributeError("The outer list should have exactly 2 sublists for top and bottom resonators.")
        elif isinstance(config, HangerConfiguration):
            self.configs = [[config] * num_hangers_bottom, [config] * num_hangers_top]
        
        for config_list in self.configs:
            for config in config_list:
                if config.want_feedline_and_pads:
                    raise AttributeError("The configurator passed to this function cannot have 'want_feedline_and_pads' set to True.")
        
        self.num_hangers_top = num_hangers_top
        self.num_hangers_bottom = num_hangers_bottom
        self.feedline_width = feedline_width
        self.feedline_path_width = feedline_path_width

class TransmissionConfiguration:
    def __init__(self, path_width, path3_width, gap, inner_angle, length_of_one_segment, total_loops, padding=40, rotation_angle=0, layers=[0, 1], points=43,
                 x=0, y=0, first_seg_length=None, last_seg_length=None, want_touch_pads=False):
        self.path_width = path_width
        self.path3_width = path3_width
        self.gap = gap
        self.inner_angle = inner_angle
        self.length_of_one_segment = length_of_one_segment
        self.total_loops = total_loops
        self.padding = padding
        self.rotation_angle = rotation_angle
        self.layers = layers
        self.points = points
        self.x = x
        self.y = y
        self.first_seg_length = first_seg_length
        self.last_seg_length = last_seg_length
        self.want_touch_pads = want_touch_pads
        self.outer_angle = self.inner_angle + self.gap + self.path_width

def create_1_transmission(config: TransmissionConfiguration):
    
    """
    Create a GDSII transmission resonator using the specified configurator.

    This function generates a GDSII transmission resonator based on the provided configurator object.
    The configurator defines the geometry and properties of the transmission resonator. Units are in microns by default.

    Parameters:
        configurator (TransmissionResonatorConfigurator): An instance of the TransmissionResonatorConfigurator
            class that defines the configuration for the transmission resonator.

    Returns:
        tuple: A tuple containing three GDSII Path objects representing the transmission resonator paths and,
        if touch pads are included, two GDSII Polygon objects for the touch pads.

    Example:
        configurator = TransmissionResonatorConfigurator(path_width=15, path3_width=95, gap=10, inner_angle=50,
                                                         length_of_one_segment=700, total_loops=4)
        path1, path2, path3 = create_1_transmission(configurator)
    """
    
    path_width = config.path_width
    path3_width = config.path3_width
    gap = config.gap
    inner_angle = config.inner_angle
    length_of_one_segment = config.length_of_one_segment
    total_loops = config.total_loops
    padding = config.padding
    rotation_angle = config.rotation_angle
    layers = config.layers
    points = config.points
    x = config.x
    y = config.y
    first_seg_length = config.first_seg_length
    last_seg_length = config.last_seg_length
    want_touch_pads = config.want_touch_pads
    outer_angle = config.outer_angle
    
    if first_seg_length is None:
        first_seg_length = 0.8 * length_of_one_segment
    if last_seg_length is None:
        last_seg_length = 0.8 * length_of_one_segment

    loops_after_one =- total_loops - 2

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
    
def create_1_hanger(config: HangerConfiguration):
    """
    Create 1 GDSII hanger resonator. Doesn't create touch pads or holes. Returns 3 paths, 2 for the meander and a third one that
    envelops the meander for holes. Units are in microns by default.

    Parameters:
        config (HangerConfiguration): An instance of HangerConfiguration class that contains configuration parameters.

    Returns:
        tuple: A tuple containing three GDSII Path objects representing the hanger paths or three GDSII Path objects and two
        GDSII Polygon objects.

    Example:
        path1, path2, path3 = create_1_hanger(HangerConfiguration(path_width=15, path3_width=95, gap=10, inner_angle=50,
                                              length_of_one_segment=700, total_loops=4, coupler_length=600))
    """

    path_width = config.path_width
    path3_width = config.path3_width
    gap = config.gap
    inner_angle = config.inner_angle
    length_of_one_segment = config.length_of_one_segment
    total_loops = config.total_loops
    padding = config.padding
    rotation_angle = config.rotation_angle
    layers = config.layers
    points = config.points
    x = config.x
    y = config.y
    first_seg_length = config.first_seg_length
    coupler_length = config.coupler_length
    want_feedline_and_pads = config.want_feedline_and_pads
    feedline_extend_length = config.feedline_extend_length
    feedline_width = config.feedline_width
    feedline_path_width = config.feedline_path_width
    coupler_gap = config.coupler_gap
    outer_angle = config.outer_angle

    if first_seg_length is None:
        first_seg_length = 0.95 * length_of_one_segment
    if coupler_length is None:
        coupler_length = 0.95 * length_of_one_segment

    loops_after_one = total_loops - 2
    coupler_gap = coupler_gap - feedline_path_width - path_width

    path1 = gdspy.Path(path_width, (0, path_width + gap))
    path2 = gdspy.Path(path_width, (0, 0))
    path3 = gdspy.Path(path3_width, (-padding, (path_width + gap) / 2))

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

    if want_feedline_and_pads:
        y_max = np.max(path2.polygons[-1][:, 1])
        x_max = np.max(path2.polygons[-1][:, 0])
        x_min = np.min(path2.polygons[-1][:, 0])
        
        points_feedline_lower = [[x_min - feedline_extend_length, y_max + coupler_gap], 
                                 [x_max + feedline_extend_length, y_max + coupler_gap],
                                 [x_max + feedline_extend_length, y_max + coupler_gap + feedline_path_width],
                                 [x_min - feedline_extend_length, y_max + coupler_gap + feedline_path_width]]

        points_feedline_upper = [[x_min - feedline_extend_length, y_max + coupler_gap + feedline_width + feedline_path_width], 
                                 [x_max + feedline_extend_length, y_max + coupler_gap + feedline_width + feedline_path_width],
                                 [x_max + feedline_extend_length, y_max + coupler_gap + feedline_path_width + feedline_width + feedline_path_width],
                                 [x_min - feedline_extend_length, y_max + coupler_gap + feedline_path_width + feedline_width + feedline_path_width]]
        
        feedline_lower = gdspy.Polygon(points_feedline_lower)
        feedline_upper = gdspy.Polygon(points_feedline_upper)
        
        all_objs = [path1, path2, path3, feedline_lower, feedline_upper]
        
        for obj in all_objs:
            obj.translate(dx=x, dy=y)
            obj.rotate(rotation_angle, center=(x, y))
        
        return all_objs

    else:
        
        all_objs = [path1, path2, path3]
        
        for obj in all_objs:
            obj.rotate(rotation_angle, center=(x, y))

        return all_objs
    
def create_hangers_array(super_config: HangerArrayConfiguration):
    
    configs = super_config.configs
    num_reson_bottom = len(super_config.configs[0])
    num_reson_top = len(super_config.configs[1])
    
    distance_between_meanders = 100
    
    path1s_left = []
    path2s_left = []
    path3s_left = []
    feedlines = []
    width_of_paths = []
    all_coupler_gaps1 = [config.coupler_gap for config in configs[0]]
    
    for i in range(num_reson_bottom):
        config = configs[0][i]
        
        path1, path2, path3 = create_1_hanger(config)

        all_vertices = np.vstack(path2.polygons)
        x_coordinates = all_vertices[:, 0]
        max_x = np.max(x_coordinates)
        
        all_vertices = np.vstack(path1.polygons)
        x_coordinates = all_vertices[:, 0]
        min_x = np.min(x_coordinates)
        
        width_of_paths.append((np.abs(max_x) + np.abs(min_x)))
        
        if i != 0:
            width = sum(width_of_paths[0 : i])
            dx = width + distance_between_meanders * i
            dy = all_coupler_gaps1[0] - all_coupler_gaps1[i]
            for path in [path1, path2, path3]:
                path.translate(dx, dy)
                
        elif i == 0:
            y_max = np.max(path2.polygons[-1][:, 1])
            x_max = np.max(path2.polygons[-1][:, 0])
            x_min = np.min(path2.polygons[-1][:, 0])
            
            feedline_extend_length = 10000
            feedline_width = super_config.feedline_width
            feedline_path_width = super_config.feedline_path_width
            coupler_gap = all_coupler_gaps1[0] - feedline_path_width - config.path_width
            
            points_feedline_lower = [[x_min - feedline_extend_length, y_max + coupler_gap], 
                                     [x_max + feedline_extend_length, y_max + coupler_gap],
                                     [x_max + feedline_extend_length, y_max + coupler_gap + feedline_path_width],
                                     [x_min - feedline_extend_length, y_max + coupler_gap + feedline_path_width]]

            points_feedline_upper = [[x_min - feedline_extend_length, y_max + coupler_gap + feedline_width + feedline_path_width], 
                                     [x_max + feedline_extend_length, y_max + coupler_gap + feedline_width + feedline_path_width],
                                     [x_max + feedline_extend_length, y_max + coupler_gap + feedline_path_width + feedline_width + feedline_path_width],
                                     [x_min - feedline_extend_length, y_max + coupler_gap + feedline_path_width + feedline_width + feedline_path_width]]

            feedline_lower = gdspy.Polygon(points_feedline_lower)
            feedline_upper = gdspy.Polygon(points_feedline_upper)
            feedlines.append(feedline_lower)
            feedlines.append(feedline_upper)

        path1s_left.append(path1)
        path2s_left.append(path2)
        path3s_left.append(path3)
    
    all_coupler_gaps2 = [config.coupler_gap for config in configs[1]]
    for i in range(num_reson_top):
        config = configs[1][i]
        
        path1, path2, path3 = create_1_hanger(config)

        all_vertices = np.vstack(path2.polygons)
        x_coordinates = all_vertices[:, 0]
        max_x = np.max(x_coordinates)
        y_coordinates = all_vertices[:, 1]
        max_y = np.max(y_coordinates)
        min_y = np.min(y_coordinates)
        height_of_resonator = max_y - min_y
        
        all_vertices = np.vstack(path1.polygons)
        x_coordinates = all_vertices[:, 0]
        min_x = np.min(x_coordinates)
        
        width_of_paths.append(max_x - min_x)
        
        if i != 0:
            width = sum(width_of_paths[0 : i])
            dx = width + distance_between_meanders * i
            dy = height_of_resonator + 1 * all_coupler_gaps1[0] + all_coupler_gaps2[i] - 2 * config.path_width + feedline_width
            for path in [path1, path2, path3]:
                path.translate(dx, dy)
                
        elif i == 0:
            dx = 0
            dy = height_of_resonator + all_coupler_gaps1[0] + all_coupler_gaps2[0] - 2 * config.path_width + feedline_width
            for path in [path1, path2, path3]:
                path.translate(dx, dy)

        path1s_left.append(path1)
        path2s_left.append(path2)
        path3s_left.append(path3)
    
    return [path1s_left, path2s_left, path3s_left, feedlines]

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