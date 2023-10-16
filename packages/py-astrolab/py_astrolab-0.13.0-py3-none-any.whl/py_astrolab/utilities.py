import json
import math
from pathlib import Path
from typing import Literal, Union

import jsonpickle

from py_astrolab.types import KerykeionException, KerykeionPoint


def get_number_from_name(name: str) -> int:
    """Utility function, gets planet id from the name."""
    name = name.lower()

    if name == "sun":
        return 0
    elif name == "moon":
        return 1
    elif name == "mercury":
        return 2
    elif name == "venus":
        return 3
    elif name == "mars":
        return 4
    elif name == "jupiter":
        return 5
    elif name == "saturn":
        return 6
    elif name == "uranus":
        return 7
    elif name == "neptune":
        return 8
    elif name == "pluto":
        return 9
    elif name == "mean_node":
        return 10  # change!
    elif name == "true_node":
        return 11
    elif name == 'mean_apog':
        return 12
    elif name == 'oscu_apog':
        return 13
    else:
        return int(name)


def calculate_position(degree: Union[int, float], number_name: str, point_type: Literal["Planet", "House", "Axis", "Synod"]) -> KerykeionPoint:
    """Utility function to create a dictionary deviding
    the houses or the planets list."""

    if degree < 30:
        dictionary = {"name": number_name, "quality": "Cardinal", "element":
                      "Fire", "signs": ["Ari"], "sign_num": 0, "position": degree, "abs_pos": degree,
                      "emoji": "♈️", "point_type": point_type}
        if point_type == 'House' and degree > 0:
            dictionary['signs'].append('Tau')

    elif degree < 60:
        result = degree - 30
        dictionary = {"name": number_name, "quality": "Fixed", "element":
                      "Earth", "signs": ["Tau"], "sign_num": 1, "position": result, "abs_pos": degree,
                      "emoji": "♉️", "point_type": point_type}
        if point_type == 'House' and degree > 30:
            dictionary['signs'].append('Gem')
    elif degree < 90:
        result = degree - 60
        dictionary = {"name": number_name, "quality": "Mutable", "element":
                      "Air", "signs": ["Gem"], "sign_num": 2, "position": result, "abs_pos": degree,
                      "emoji": "♊️", "point_type": point_type}
        if point_type == 'House' and degree > 60:
            dictionary['signs'].append('Can')
    elif degree < 120:
        result = degree - 90
        dictionary = {"name": number_name, "quality": "Cardinal", "element":
                      "Water", "signs": ["Can"], "sign_num": 3, "position": result, "abs_pos": degree,
                      "emoji": "♋️", "point_type": point_type}
        if point_type == 'House' and degree > 90:
            dictionary['signs'].append('Leo')
    elif degree < 150:
        result = degree - 120
        dictionary = {"name": number_name, "quality": "Fixed", "element":
                      "Fire", "signs": ["Leo"], "sign_num": 4, "position": result, "abs_pos": degree,
                      "emoji": "♌️", "point_type": point_type}
        if point_type == 'House' and degree > 120:
            dictionary['signs'].append('Vir')
    elif degree < 180:
        result = degree - 150
        dictionary = {"name": number_name, "quality": "Mutable", "element":
                      "Earth", "signs": ["Vir"], "sign_num": 5, "position": result, "abs_pos": degree,
                      "emoji": "♍️", "point_type": point_type}
        if point_type == 'House' and degree > 150:
            dictionary['signs'].append('Lib')
    elif degree < 210:
        result = degree - 180
        dictionary = {"name": number_name, "quality": "Cardinal", "element":
                      "Air", "signs": ["Lib"], "sign_num": 6, "position": result, "abs_pos": degree,
                      "emoji": "♎️", "point_type": point_type}
        if point_type == 'House' and degree > 180:
            dictionary['signs'].append('Sco')
    elif degree < 240:
        result = degree - 210
        dictionary = {"name": number_name, "quality": "Fixed", "element":
                      "Water", "signs": ["Sco"], "sign_num": 7, "position": result, "abs_pos": degree,
                      "emoji": "♏️", "point_type": point_type}
        if point_type == 'House' and degree > 210:
            dictionary['signs'].append('Sag')
    elif degree < 270:
        result = degree - 240
        dictionary = {"name": number_name, "quality": "Mutable", "element":
                      "Fire", "signs": ["Sag"], "sign_num": 8, "position": result, "abs_pos": degree,
                      "emoji": "♐️", "point_type": point_type}
        if point_type == 'House' and degree > 240:
            dictionary['signs'].append('Cap')
    elif degree < 300:
        result = degree - 270
        dictionary = {"name": number_name, "quality": "Cardinal", "element":
                      "Earth", "signs": ["Cap"], "sign_num": 9, "position": result, "abs_pos": degree,
                      "emoji": "♑️", "point_type": point_type}
        if point_type == 'House' and degree > 270:
            dictionary['signs'].append('Aqu')
    elif degree < 330:
        result = degree - 300
        dictionary = {"name": number_name, "quality": "Fixed", "element":
                      "Air", "signs": ["Aqu"], "sign_num": 10, "position": result, "abs_pos": degree,
                      "emoji": "♒️", "point_type": point_type}
        if point_type == 'House' and degree > 300:
            dictionary['signs'].append('Pis')
    elif degree < 360:
        result = degree - 330
        dictionary = {"name": number_name, "quality": "Mutable", "element":
                      "Water", "signs": ["Pis"], "sign_num": 11, "position": result, "abs_pos": degree,
                      "emoji": "♓️", "point_type": point_type}
        if point_type == 'House' and degree > 330:
            dictionary['signs'].append('Ari')
    else:
        raise KerykeionException(
            f'Error in calculating positions! Degrees: {degree}')

    return KerykeionPoint(**dictionary)

def dangerous_json_dump(subject, dump=True, new_output_directory=None):
    """
        Dumps the Kerykeion object to a json file located in the home folder.
        This json file allows the object to be recreated with jsonpickle.
        It's dangerous since it contains local system information.
        """

    OUTPUT_DIR = Path.home()

    try:
        subject.sun
    except:
        subject.__get_all()

    if new_output_directory:
        output_directory_path = Path(new_output_directory)
        json_dir = new_output_directory / \
            f"{subject.name}_kerykeion.json"
    else:
        json_dir = f"{subject.name}_kerykeion.json"

    json_string = jsonpickle.encode(subject)

    if dump:
        json_string = json.loads(json_string.replace(
            "'", '"'))  # type: ignore TODO: Fix this

        with open(json_dir, "w", encoding="utf-8") as file:
            json.dump(json_string, file,  indent=4, sort_keys=True)
            subject.__logger.info(f"JSON file dumped in {json_dir}.")
    else:
        pass
    return json_string

def for_every_planet(kr_object, planet, planet_deg):
    """Function to do the calculation.
    Args: planet dictionary, planet degree"""

    def point_between(p1, p2, p3):
        """Finds if a point is between two other in a circle
        args: first point, second point, point in the middle"""
        p1_p2 = math.fmod(p2 - p1 + 360, 360)
        p1_p3 = math.fmod(p3 - p1 + 360, 360)
        if (p1_p2 <= 180) != (p1_p3 > p1_p2):
            return True
        else:
            return False

    if point_between(kr_object.houses_degree_ut[0], kr_object.houses_degree_ut[1],
                        planet_deg) == True:
        planet["house"] = "First House"
    elif point_between(kr_object.houses_degree_ut[1], kr_object.houses_degree_ut[2],
                        planet_deg) == True:
        planet["house"] = "Second House"
    elif point_between(kr_object.houses_degree_ut[2], kr_object.houses_degree_ut[3],
                        planet_deg) == True:
        planet["house"] = "Third House"
    elif point_between(kr_object.houses_degree_ut[3], kr_object.houses_degree_ut[4],
                        planet_deg) == True:
        planet["house"] = "Fourth House"
    elif point_between(kr_object.houses_degree_ut[4], kr_object.houses_degree_ut[5],
                        planet_deg) == True:
        planet["house"] = "Fifth House"
    elif point_between(kr_object.houses_degree_ut[5], kr_object.houses_degree_ut[6],
                        planet_deg) == True:
        planet["house"] = "Sixth House"
    elif point_between(kr_object.houses_degree_ut[6], kr_object.houses_degree_ut[7],
                        planet_deg) == True:
        planet["house"] = "Seventh House"
    elif point_between(kr_object.houses_degree_ut[7], kr_object.houses_degree_ut[8],
                        planet_deg) == True:
        planet["house"] = "Eighth House"
    elif point_between(kr_object.houses_degree_ut[8], kr_object.houses_degree_ut[9],
                        planet_deg) == True:
        planet["house"] = "Ninth House"
    elif point_between(kr_object.houses_degree_ut[9], kr_object.houses_degree_ut[10],
                        planet_deg) == True:
        planet["house"] = "Tenth House"
    elif point_between(kr_object.houses_degree_ut[10], kr_object.houses_degree_ut[11],
                        planet_deg) == True:
        planet["house"] = "Eleventh House"
    elif point_between(kr_object.houses_degree_ut[11], kr_object.houses_degree_ut[0],
                        planet_deg) == True:
        planet["house"] = "Twelfth House"
    else:
        planet["house"] = "error!"

    return planet

def parse_json_settings(new_settings_file: Union[str, Path, None] = None):
    # Load settings file
    DATADIR = Path(__file__).parent

    if not new_settings_file:
        settings_file = DATADIR / "kr.config.json"
    else:
        settings_file = Path(new_settings_file)

    with open(settings_file, 'r', encoding="utf-8", errors='ignore') as f:
        settings = json.load(f)

    return settings