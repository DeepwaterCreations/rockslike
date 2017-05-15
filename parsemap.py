"""A module for generating map files from text input"""
import mapfeatures

__map_dict = {
        '.': mapfeatures.Floor,
        '#': mapfeatures.Wall,
        ' ': mapfeatures.Void
        }

def parse_line(line):
    """Read a single row of dungeon text and generate a list of cells"""
    return [[__map_dict[feature]()] for feature in line.strip()]

def parse_map_features(map_file):
    """Read a description of a map from a file and generate a matrix of map features"""
    matrix = []
    for line in map_file:
        parsed_line = parse_line(line)
        matrix.append(parsed_line)
    return matrix
