"""
    This is part of Kerykeion (C) 2022 Giacomo Battaglia
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math
from pathlib import Path
from typing import Union

from swisseph import difdeg2n

from py_astrolab import KrInstance


class NatalAspects():
    """
    Generates an object with all the aspects of a birthcart.
    """

    def __init__(
            self, kr_object: KrInstance,
            settings: Union[str, None] = None
    ):
        self.user = kr_object
        self.settings = settings
        self.colors_settings = settings['colors']
        self.planets_settings = settings['planets']
        self.axes_settings = settings['axes']
        self.aspects_settings = settings['aspects']
        self.axes_orbit_settings = settings['axes_orbit']

        if not hasattr(self.user, "sun"):
            self.user.__get_all()

        self.init_point_list = self.user.planets_list + self.user.houses_list + self.user.axis_list

    def asp_calc(self, point_one, point_two):
        """ 
        Utility function.
        It calculates the aspects between the 2 points.
        Args: first point, second point. 
        """

        distance = abs(difdeg2n(point_one, point_two))
        diff = abs(point_one - point_two)
        if int(distance) <= self.aspects_settings[0]['orb']:
            name = self.aspects_settings[0]['name']
            aspect_degrees = self.aspects_settings[0]['degree']
            color = self.colors_settings['aspect_0']
            verdict = True
            aid = 0

        elif (self.aspects_settings[1]['degree'] - self.aspects_settings[1]['orb']) <= int(distance) <= (self.aspects_settings[1]['degree'] + self.aspects_settings[1]['orb']):
            name = self.aspects_settings[1]['name']
            aspect_degrees = self.aspects_settings[1]['degree']
            color = self.colors_settings['aspect_30']
            verdict = True
            aid = 1

        elif (self.aspects_settings[2]['degree'] - self.aspects_settings[2]['orb']) <= int(distance) <= (self.aspects_settings[2]['degree'] + self.aspects_settings[2]['orb']):
            name = self.aspects_settings[2]['name']
            aspect_degrees = self.aspects_settings[2]['degree']
            color = self.colors_settings['aspect_45']
            verdict = True
            aid = 2

        elif (self.aspects_settings[3]['degree'] - self.aspects_settings[3]['orb']) <= int(distance) <= (self.aspects_settings[3]['degree'] + self.aspects_settings[3]['orb']):
            name = self.aspects_settings[3]['name']
            aspect_degrees = self.aspects_settings[3]['degree']
            color = self.colors_settings['aspect_60']
            verdict = True
            aid = 3

        elif (self.aspects_settings[4]['degree'] - self.aspects_settings[4]['orb']) <= int(distance) <= (self.aspects_settings[4]['degree'] + self.aspects_settings[4]['orb']):
            name = self.aspects_settings[4]['name']
            aspect_degrees = self.aspects_settings[4]['degree']
            color = self.colors_settings['aspect_72']
            verdict = True
            aid = 4

        elif (self.aspects_settings[5]['degree'] - self.aspects_settings[5]['orb']) <= int(distance) <= (self.aspects_settings[5]['degree'] + self.aspects_settings[5]['orb']):
            name = self.aspects_settings[5]['name']
            aspect_degrees = self.aspects_settings[5]['degree']
            color = self.colors_settings['aspect_90']
            verdict = True
            aid = 5

        elif (self.aspects_settings[6]['degree'] - self.aspects_settings[6]['orb']) <= int(distance) <= (self.aspects_settings[6]['degree'] + self.aspects_settings[6]['orb']):
            name = self.aspects_settings[6]['name']
            aspect_degrees = self.aspects_settings[6]['degree']
            color = self.colors_settings['aspect_120']
            verdict = True
            aid = 6

        elif (self.aspects_settings[7]['degree'] - self.aspects_settings[7]['orb']) <= int(distance) <= (self.aspects_settings[7]['degree'] + self.aspects_settings[7]['orb']):
            name = self.aspects_settings[7]['name']
            aspect_degrees = self.aspects_settings[7]['degree']
            color = self.colors_settings['aspect_135']
            verdict = True
            aid = 7

        elif (self.aspects_settings[8]['degree'] - self.aspects_settings[8]['orb']) <= int(distance) <= (self.aspects_settings[8]['degree'] + self.aspects_settings[8]['orb']):
            name = self.aspects_settings[8]['name']
            aspect_degrees = self.aspects_settings[8]['degree']
            color = self.colors_settings['aspect_144']
            verdict = True
            aid = 8

        elif (self.aspects_settings[9]['degree'] - self.aspects_settings[9]['orb']) <= int(distance) <= (self.aspects_settings[9]['degree'] + self.aspects_settings[9]['orb']):
            name = self.aspects_settings[9]['name']
            aspect_degrees = self.aspects_settings[9]['degree']
            color = self.colors_settings['aspect_150']
            verdict = True
            aid = 9

        elif (self.aspects_settings[10]['degree'] - self.aspects_settings[10]['orb']) <= int(distance) <= (self.aspects_settings[10]['degree'] + self.aspects_settings[10]['orb']):
            name = self.aspects_settings[10]['name']
            aspect_degrees = self.aspects_settings[10]['degree']
            color = self.colors_settings['aspect_180']
            verdict = True
            aid = 10

        else:
            verdict = False
            name = None
            distance = 0
            aspect_degrees = 0
            color = None
            aid = None
        return verdict, name, distance - aspect_degrees, aspect_degrees, color, aid, diff

    def p_id_decoder(self, name):
        """ 
        Check if the name of the planet is the same in the settings and return
        the correct id for the planet.
        """
        str_name = str(name)
        settings = self.planets_settings.copy()
        settings.extend(self.axes_settings)
        for a in settings:
            if a['name'] == str_name:
                result = a['id']
                return result

    def filter_by_settings(self, init_point_list):
        """
        Creates a list of all the desired
        points filtering by the settings.
        """

        set_points_name = []
        settings = self.planets_settings.copy()
        settings.extend(self.axes_settings)
        for p in settings:
            if p['visible']:
                set_points_name.append(p['name'])

        point_list = []
        for l in init_point_list:
            if l['name'] in set_points_name:
                point_list.append(l)

        return point_list

    def get_all_aspects(self):
        """
        Return all the aspects of the points in the natal chart in a dictionary,
        first all the individual aspects of each planet, second the aspects
        whitout repetitions.
        """

        point_list = self.filter_by_settings(self.init_point_list)
        self.all_aspects_list = []
        for first in range(len(point_list)):
            # Generates the aspects list whitout repetitions
            for second in range(first + 1, len(point_list)):
                if point_list[first]['point_type'] == 'Axis' and point_list[second]['point_type'] == 'Axis':
                    continue
                verdict, name, orbit, aspect_degrees, color, aid, diff = self.asp_calc(point_list[first]["abs_pos"],
                                                                                       point_list[second]["abs_pos"])

                if verdict == True:
                    d_asp = {"p1_name": point_list[first]['name'],
                             "p1_abs_pos": point_list[first]['abs_pos'],
                             "p2_name": point_list[second]['name'],
                             "p2_abs_pos": point_list[second]['abs_pos'],
                             "aspect": name,
                             "orbit": orbit,
                             "aspect_degrees": aspect_degrees,
                             "color": color,
                             "aid": aid,
                             "diff": diff,
                             "p1": self.p_id_decoder(point_list[first]['name']),
                             "p2": self.p_id_decoder(point_list[second]['name'],)
                             }
                    self.all_aspects_list.append(d_asp)

        return self.all_aspects_list

    def is_fake_aspect(self, aspect: dict) -> bool:
        p1_name = aspect['p1_name'].lower().replace(' ', '_')
        p2_name = aspect['p2_name'].lower().replace(' ', '_')
        p1_attr = getattr(self.user, p1_name)
        p2_attr = getattr(self.user, p2_name)
        if p1_name == 'true_node' and p2_name == 'south_node':
            return True
        if p1_attr['element'] == p2_attr['element'] and aspect['aspect'] == 'square':
            return True
        if aspect['aspect'] in {'trine', 'conjunction'} and p1_attr['element'] != p2_attr['element'] and aspect['orbit'] > 3:
            return True
        if aspect['aspect'] == 'opposition':
            p1_sign = p1_attr['signs'][0]
            p2_sign = p2_attr['signs'][0]
            p1_sign_opposite = self.user.signs_dict[p1_sign]['opposite']
            return not p1_sign_opposite.startswith(p2_sign)
        return False

    def get_relevant_aspects(self):
        self.get_all_aspects()
        aspects_filtered = [a for a in self.all_aspects_list if self.aspects_settings[a["aid"]]["visible"] == True]
        axes_set = {
            "Ascendant",
            "Midheaven",
            "Descendant",
            "Imum Coeli"
        }
        aspects_filtered = [a for a in aspects_filtered if not (
            (a['p1_name'] in axes_set and abs(a['orbit']) >= self.axes_orbit_settings) or
            (a['p2_name'] in axes_set and abs(a['orbit']) >= self.axes_orbit_settings) or
            self.is_fake_aspect(a)
        )]
        self.aspects = aspects_filtered
        return self.aspects


class CompositeAspects(NatalAspects):
    """
    Generates an object with all the aspects between two persons.
    """

    def __init__(self, kr_object_one: KrInstance, kr_object_two: KrInstance, settings: Union[str, None] = None):
        self.first_user = kr_object_one
        self.second_user = kr_object_two

        self.settings = settings
        self.colors_settings = settings['colors']
        self.planets_settings = settings['planets']
        self.axes_settings = settings['axes']
        self.aspects_settings = settings['aspects']
        self.axes_orbit_settings = settings['axes_orbit']

        if not hasattr(self.first_user, "sun"):
            self.first_user.__get_all()

        if not hasattr(self.second_user, "sun"):
            self.second_user.__get_all()

        self.first_init_point_list = self.first_user.planets_list + \
            self.first_user.houses_list + self.first_user.axis_list
        self.second_init_point_list = self.second_user.planets_list + \
            self.second_user.houses_list + self.second_user.axis_list

    def is_fake_aspect(self, aspect: dict) -> bool:
        is_fake_aspect = False
        user_1 = json.loads(self.first_user.json())
        user_2 = json.loads(self.second_user.json())
        p1_name = aspect['p1_name'].lower().replace(' ', '_')
        p2_name = aspect['p2_name'].lower().replace(' ', '_')
        if p1_name == 'true_node' and p2_name == 'south_node':
            is_fake_aspect = True
        if user_1[p1_name]['element'] == user_2[p2_name]['element'] and aspect['aspect'] == 'square':
            is_fake_aspect = True
        if aspect['aspect'] in {'trine', 'conjunction'}:
            if user_1[p1_name]['element'] != user_2[p2_name]['element']:
                # if aspect['orbit'] > 3:
                is_fake_aspect = True
        elif aspect['aspect'] == 'opposition':
            p1_sign = user_1[p1_name]['signs'][0]
            p2_sign = user_2[p2_name]['signs'][0]
            p1_sign_opposite = self.first_user.signs_dict[p1_sign]['opposite']
            if not p1_sign_opposite.startswith(p2_sign):
                is_fake_aspect = True
        return is_fake_aspect

    def get_all_aspects(self):
        """
        Return all the aspects of the points in the natal chart in a dictionary,
        first all the individual aspects of each planet, second the aspects
        whitout repetitions.
        """

        f_1 = self.filter_by_settings(self.first_init_point_list)
        f_2 = self.filter_by_settings(self.second_init_point_list)

        self.all_aspects_list = []

        for first in range(len(f_1)):
            # Generates the aspects list whitout repetitions
            for second in range(len(f_2)):

                verdict, name, orbit, aspect_degrees, color, aid, diff = self.asp_calc(f_1[first]["abs_pos"],
                                                                                       f_2[second]["abs_pos"])

                if verdict == True:
                    d_asp = {"p1_name": f_1[first]['name'],
                             "p1_abs_pos": f_1[first]['abs_pos'],
                             "p2_name": f_2[second]['name'],
                             "p2_abs_pos": f_2[second]['abs_pos'],
                             "aspect": name,
                             "orbit": orbit,
                             "aspect_degrees": aspect_degrees,
                             "color": color,
                             "aid": aid,
                             "diff": diff,
                             "p1": self.p_id_decoder(f_1[first]['name']),
                             "p2": self.p_id_decoder(f_2[second]['name'],)
                             }

                    self.all_aspects_list.append(d_asp)

        return self.all_aspects_list

    def get_points_in_houses(self):
        def point_between(p1, p2, p3):
            """Finds if a point is between two other in a circle
            args: first point, second point, point in the middle"""
            p1_p2 = math.fmod(p2 - p1 + 360, 360)
            p1_p3 = math.fmod(p3 - p1 + 360, 360)
            if (p1_p2 <= 180) != (p1_p3 > p1_p2):
                return True
            else:
                return False
        
        points_in_houses = list()
        users_list = [self.first_user, self.second_user]
        for j, user in enumerate(users_list):
            user_houses_index = 0 if j == 1 else 1
            other_user = users_list[user_houses_index]
            other_houses_list = other_user.houses_list
            points = user.planets_list + user.axis_list
            for point in points:
                point_degrees = point.abs_pos
                for m, house in enumerate(other_houses_list):
                    if m < len(other_houses_list) - 1:
                        if point_between(other_houses_list[m].abs_pos, other_houses_list[m+1].abs_pos, point_degrees):
                            points_in_houses.append({f'p{j + 1}_name': point.name, f'p{user_houses_index + 1}_house': house.name})
        return points_in_houses
        

if __name__ == "__main__":
    kanye = KrInstance("Kanye", 1977, 6, 8, 8, 45, "New York")
    jack = KrInstance("Jack", 1990, 6, 15, 13, 00, "Montichiari")
    # kanye.get_all()
    # natal = NatalAspects(kanye)
    # natal.get_relevant_aspects()
    # for a in natal.aspects:
    #     print(a['p1_name'], a['p2_name'], a['orbit'])
    cm = CompositeAspects(kanye, jack)
    res = cm.get_relevant_aspects()
    for a in res:
        print(a['p1_name'], 'number is', a['p1'], a['p2_name'],
              'number is', a['p2'], a['orbit'], a['aspect'])
    print(len(res))
    print(res[0])
