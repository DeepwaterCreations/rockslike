"""A module for generating map files from text input"""
import sys
import json
import functools

import mapfeatures
import entities
from tile import Tile

__map_dict = {
        '.': mapfeatures.Floor,
        '#': mapfeatures.Wall,
        ' ': mapfeatures.Void
        }

def parse_file(map_file):
    """Divide file into map features section and entities section

    Sections are delimited by blank lines
    Map Art: An ASCII picture of the map
    Map Features: A JSON object with coordinate pairs keyed to lists containing objects with these fields:
            classname - the name of a subclass of MapFeature that should be generated for this tile
            fgcolor, bgcolor - strings describing the foreground and background color of
                the tile
            args - a list of arguments to pass to the object's constructor
            kwargs - a dict of keyword arguments to pass to the object's constructor
        All of these fields are optional for MapFeatures. If omitted, they will
        be inferred from the ASCII art. Additionally, MapFeatures displayed in the ASCII art will be
        created even if there is no associated listing in the object.
    Entities: A JSON list of objects with these fields:
            classname - the name of a subclass of Entity that describes this entity
            x_coord - the x coordinate of the entity's position
            y_coord - the y coordinate of the entity's position
            tilechar - the character to display for the object
            fgcolor, bgcolor - strings describing the foreground and backgrounc color
                of the tile
            args - (optional) a list of arguments to pass to the entity's constructor
            ksargs - (optional) a dict of keyword arguments to pass to the entity's constructor
    """
    mapfeatures_delimiter = "((MAPFEATURES))"
    entities_delimiter = "((ENTITIES))"

    map_text = map_file.read()
    map_text = map_text.strip()
    map_text = map_text.splitlines()

    #Break the file into its component chunks
    mapart_end_index = map_text.index("") if "" in map_text else len(map_text)
    mapart_text = map_text[:mapart_end_index]
    json_text = map_text[mapart_end_index:]
    
    mapfeatures_text = None
    entities_text = None
    if mapfeatures_delimiter in json_text:
        mapfeatures_start_index = json_text.index(mapfeatures_delimiter)+1
        mapfeatures_end_index = json_text.index(entities_delimiter) if entities_delimiter in json_text \
                else len(json_text)
        mapfeatures_text = json_text[mapfeatures_start_index:mapfeatures_end_index]

    if entities_delimiter in json_text:
        entities_start_index = json_text.index(entities_delimiter)+1
        entities_end_index = len(json_text)
        entities_text = json_text[entities_start_index:entities_end_index]

    matrix = __parse_map_features(mapart_text, mapfeatures_text)
    map_entities = __parse_entities(entities_text)
    return (matrix, map_entities)

def __parse_map_features(mapart_text, mapfeatures_text):
    """Read a description of a map from a file and generate a matrix of map features"""
    matrix = []
    if mapfeatures_text is not None:
        mapfeatures_text = "".join(mapfeatures_text)
        json_mapfeatures = json.loads(mapfeatures_text)
    else:
        json_mapfeatures = {}

    for y, line in enumerate(mapart_text):
        parsed_line = []
        for x, cell in enumerate(line):
            if "{0},{1}".format(x, y) in json_mapfeatures:
                obj = json_mapfeatures["{0},{1}".format(x, y)]
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
            parsed_line.append([feature])
        matrix.append(parsed_line)
    return matrix

def __parse_entities(entities_text):
    """Build a list of callable game object constructors from a list of JSON objects"""
    if entities_text is None:
        return []

    entities_text = "".join(entities_text)
    json_entities = json.loads(entities_text)

    map_entities = []
    for obj in json_entities:
        x_coord = int(obj['x_coord'])
        y_coord = int(obj['y_coord'])
        fgcolor = obj['fgcolor'] if 'fgcolor' in obj else "WHITE"
        bgcolor = obj['bgcolor'] if 'bgcolor' in obj else "BLACK"
        tile = Tile(obj['tilechar'], fgcolor, bgcolor) if 'tilechar' in obj else None
        args = obj['args'] if 'args' in obj else []
        if tile is not None:
            args.append(tile)
        args.append(x_coord)
        args.append(y_coord)
        kwargs = obj['kwargs'] if 'kwargs' in obj else {}
        entity_class = getattr(sys.modules["entities"], obj['classname'])
        entity_partial = functools.partial(entity_class, *args, **kwargs)
        map_entities.append(entity_partial)
    return map_entities
