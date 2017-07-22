"""A module for generating map data from file input"""
import sys
import json
import functools

import mapfeatures
import entities
from tile import Tile

__map_dict = {
        '.': mapfeatures.Floor,
        '#': mapfeatures.Wall,
        ' ': mapfeatures.Void,
        '>': mapfeatures.StairsDown,
        '<': mapfeatures.StairsUp
        }

def parse_file(map_file):
    """Divide file into map art section and JSON section, which are separated by a newline

    Map Art: An ASCII picture of the map
    JSON: a JSON object optionally containing some or all of the following:
        "mapdetails": A JSON object with metadata about the map
                version - the parser version to use (not currently observed)
                player_spawn_x - the x coordinate where the player should spawn in
                player_spawn_y - the y coordinate where the player should spawn in
        "mapfeatures": A JSON object with coordinate pairs keyed to lists containing objects with these fields:
                classname - the name of a subclass of MapFeature that should be generated for this tile
                fgcolor, bgcolor - strings describing the foreground and background color of
                    the tile
                args - a list of arguments to pass to the object's constructor
                kwargs - a dict of keyword arguments to pass to the object's constructor
            All of these fields are optional for MapFeatures. If omitted, they will
            be inferred from the ASCII art. Additionally, MapFeatures displayed in the ASCII art will be
            created even if there is no associated listing in the object.
        "entities": A JSON list of objects with these fields:
                classname - the name of a subclass of Entity that describes this entity
                x_coord - the x coordinate of the entity's position
                y_coord - the y coordinate of the entity's position
                tilechar - the character to display for the object
                fgcolor, bgcolor - strings describing the foreground and backgrounc color
                    of the tile
                args - (optional) a list of arguments to pass to the entity's constructor
                ksargs - (optional) a dict of keyword arguments to pass to the entity's constructor
    """
    #Read the file, strip leading and trailing whitespace, and break into a list of strings
    #by line
    file_text = map_file.read()
    file_text = file_text.strip()
    file_text_lines = file_text.splitlines()

    #Separate the file into its component chunks
    mapart_end_index = file_text_lines.index("") if "" in file_text_lines else len(file_text_lines)
    mapart = file_text_lines[:mapart_end_index]

    json_text = file_text_lines[mapart_end_index:] if mapart_end_index < len(file_text_lines) else ""
    json_text = "".join(json_text) #Put JSON lines back together into a single string so JSON can be parsed
    map_obj = json.loads(json_text) if len(json_text) > 0 else {}

    #Get members of JSON objects
    mapdetails = map_obj["mapdetails"] if "mapdetails" in map_obj else {}
    mapfeatures_by_coord = map_obj["mapfeatures"] if "mapfeatures" in map_obj else {}
    entities_list = map_obj["entities"] if "entities" in map_obj else []

    #Parse mapfeature and entity data to create actual game objects
    mapfeatures = __parse_map_features(mapart, mapfeatures_by_coord)
    entities = __parse_entities(entities_list)

    #Pull player spawn info from mapdetails
    if "player_spawn_x" in mapdetails and "player_spawn_y" in mapdetails:
        player_spawn = (mapdetails["player_spawn_x"], mapdetails["player_spawn_y"])
    else:
        player_spawn = (0,0)

    return (mapfeatures, entities, player_spawn)

def __parse_map_features(mapart, mapfeatures_by_coord):
    """Read a description of a map from a file and generate a matrix of map features"""
    mapfeatures_matrix = []

    for y, line in enumerate(mapart):
        parsed_line = []
        for x, cell in enumerate(line):
            if "{0},{1}".format(x, y) in mapfeatures_by_coord:
                obj = mapfeatures_by_coord["{0},{1}".format(x, y)]
                if "classname" in obj:
                    mapfeature_class = getattr(sys.modules["mapfeatures"], obj["classname"])
                elif cell in __map_dict:
                    mapfeature_class = __map_dict[cell]
                else:
                    mapfeature_class = mapfeatures.Void
                tilechar = obj["tilechar"] if "tilechar" in obj else cell
                args = obj["args"] if "args" in obj else []
                args.append(tilechar)
                if 'fgcolor' in obj:
                    args.append(obj['fgcolor'])
                if 'bgcolor' in obj:
                    args.append(obj['bgcolor'])
                if 'bold' in obj:
                    args.append(obj['bold'])
                kwargs = obj["kwargs"] if "kwargs" in obj else {}
                feature = mapfeature_class(*args, **kwargs)
            else:
                feature = __map_dict[cell]() if cell in __map_dict else mapfeatures.Void()
            parsed_line.append(feature)
        mapfeatures_matrix.append(parsed_line)
    return mapfeatures_matrix

def __parse_entities(json_entities):
    """Build a list of callable game object constructors from a list of JSON objects"""

    parsed_entities = []
    for entity_obj in json_entities:
        x_coord = int(entity_obj['x_coord'])
        y_coord = int(entity_obj['y_coord'])
        fgcolor = entity_obj['fgcolor'] if 'fgcolor' in entity_obj else "WHITE"
        bgcolor = entity_obj['bgcolor'] if 'bgcolor' in entity_obj else "BLACK"
        tile = Tile(entity_obj['tilechar'], fgcolor, bgcolor) if 'tilechar' in entity_obj else None
        args = entity_obj['args'] if 'args' in entity_obj else []
        if tile is not None:
            args.append(tile)
        args.append(x_coord)
        args.append(y_coord)
        kwargs = entity_obj['kwargs'] if 'kwargs' in entity_obj else {}
        entity_class = getattr(sys.modules["entities"], entity_obj['classname'])
        entity_partial = functools.partial(entity_class, *args, **kwargs)
        parsed_entities.append(entity_partial)
    return parsed_entities
