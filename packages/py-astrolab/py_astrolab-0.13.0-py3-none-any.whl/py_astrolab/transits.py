from datetime import datetime, timedelta
from typing import Union

import pytz
import swisseph as swe

from py_astrolab import KrInstance
from py_astrolab.aspects import CompositeAspects


class Transits():
    def __init__(self, 
            user: KrInstance, 
            tz_str: str,
            start: datetime, 
            end: datetime,
            transit_latitude: float,
            transit_longitude: float,
            hsys: str,
            settings: Union[str, None] = None):
        self.user = user
        self.tz_str = tz_str
        self.start = self.__get_utc(start)
        self.end = self.__get_utc(end)
        self.transit_latitude = transit_latitude
        self.transit_longitude = transit_longitude
        self.hsys = hsys
        self.settings = settings
        self.natal_aspects_changes = {}
        self.transit_aspects_changes = {}
        self.previous_natal_aspects = None
        self.previous_transit_aspects = None
        self.aspects = [0, 30, 60, 90, 120, 180]
        self.planet_names = {
            swe.SUN: {'name': 'Sun', 'orbit': 3, 'interval': timedelta(minutes=5)}, # 6 giorni in aspetto
            # 365 giorni / 360 gradi = 1 giorni per grado
            # 3 gradi di orbita * 2 * 1 giorni = 6 giorni in aspetto
            swe.MOON: {'name': 'Moon','orbit': 1, 'interval': timedelta(minutes=5)}, # 3,6 ore in aspetto
            # 27.3 giorni / 360 gradi = 1 ora e 49 minuti per grado (109 minuti)
            # 1 gradi di orbita * 2 * 1 ora e 49 minuti = 3,6 ore
            swe.MERCURY: {'name': 'Mercury','orbit': 3, 'interval': timedelta(hours=1)}, # 1,5 giorni in aspetto
            # 88 giorni / 360 gradi = 5,9 ore per grado (351 minuti)
            # 3 gradi di orbita * 2 * 5,9 ore = 1,5 giorni
            swe.VENUS: {'name': 'Venus','orbit': 3, 'interval': timedelta(hours=1)}, # 3,75 giorni in aspetto
            # 225 giorni / 360 gradi = 15 ore per grado
            # 3 gradi di orbita * 2 * 15 ore = 3,75 giorni
            swe.MARS: {'name': 'Mars','orbit': 5, 'interval': timedelta(hours=1)}, # 20 giorni
            # 687 giorni / 360 gradi = 1.9 giorni per grado (45,6 ore)
            # 5 gradi di orbita * 2 * 1.9 giorni = 20 giorni
            swe.JUPITER: {'name': 'Jupiter','orbit': 5, 'interval': timedelta(hours=1)}, # 4 mesi in aspetto
            # (11.86 anni * 365.25 giorni/anno) / 360 gradi = 12 giorni per grado
            # 5 gradi di orbita * 2 * 12 giorni = 120 giorni (4 mesi)
            swe.SATURN: {'name': 'Saturn','orbit': 5, 'interval': timedelta(days=1)}, # 10 mesi
            # (29.5 anni * 365.25 giorni/anno) / 360 gradi = 30 giorni per grado
            # 5 gradi di orbita * 2 * 30 giorni = 300 giorni (10 mesi)
            swe.TRUE_NODE: {'name': 'True_Node','orbit': 5, 'interval': timedelta(days=1)},
            swe.OSCU_APOG: {'name': 'Oscu_Apog','orbit': 5, 'interval': timedelta(days=1)}
        }
        self.aspect_names = {
            0: 'conjunction',
            30: 'semi-sextile',
            60: 'sextile',
            90: 'square',
            120: 'trine',
            150: 'quincunx',
            180: 'opposition',
        }
        self.signs_dict = {
            'Ari': {'extended_name': 'Aries', 'element': 'Fire', 'governor': 'Mars', 'opposite': 'Libra'},
            'Tau': {'extended_name': 'Taurus', 'element': 'Earth', 'governor': 'Venus', 'opposite': 'Scorpio'},
            'Gem': {'extended_name': 'Gemini', 'element': 'Air', 'governor': 'Mercury', 'opposite': 'Sagittarius'},
            'Can': {'extended_name': 'Cancer', 'element': 'Water', 'governor': 'Moon', 'opposite': 'Capricorn'},
            'Leo': {'extended_name': 'Leo', 'element': 'Fire', 'governor': 'Sun', 'opposite': 'Aquarius'},
            'Vir': {'extended_name': 'Virgo', 'element': 'Earth', 'governor': 'Mercury', 'opposite': 'Pisces'},
            'Lib': {'extended_name': 'Libra', 'element': 'Air', 'governor': 'Venus', 'opposite': 'Aries'},
            'Sco': {'extended_name': 'Scorpio', 'element': 'Water', 'governor': 'Mars', 'opposite': 'Taurus'},
            'Sag': {'extended_name': 'Sagittarius', 'element': 'Fire', 'governor': 'Jupiter', 'opposite': 'Gemini'},
            'Cap': {'extended_name': 'Capricorn', 'element': 'Earth', 'governor': 'Saturn', 'opposite': 'Cancer'},
            'Aqu': {'extended_name': 'Aquarius', 'element': 'Air', 'governor': 'Saturn', 'opposite': 'Leo'},
            'Pis': {'extended_name': 'Pisces', 'element': 'Water', 'governor': 'Jupiter', 'opposite': 'Virgo'}
        }
        self.jd_to_dt_cache = dict()
        self.dt_to_jd_cache = dict()
        self.long_cache = dict()
        self.orb_cache = dict()

    def __get_utc(self, dt: datetime):
        local_time = pytz.timezone(self.tz_str)
        naive_datetime = datetime(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            0
        )
        local_datetime = local_time.localize(naive_datetime, is_dst=None)
        utc_datetime = local_datetime.astimezone(pytz.utc)
        return utc_datetime

    def __get_local_time(self, dt: datetime) -> datetime:
        naive_datetime = datetime(
            dt.year,
            dt.month,
            dt.day,
            dt.hour,
            dt.minute,
            0
        )
        utc_time = pytz.utc.localize(naive_datetime)
        local_time = pytz.timezone(self.tz_str)
        local_datetime = utc_time.astimezone(local_time)
        return local_datetime

    def calc_long(self, jd, planet):
        cache_tuple = (jd, planet)
        if cache_tuple in self.long_cache:
            return self.long_cache[cache_tuple]
        long = swe.calc(jd, planet)[0][0]
        self.long_cache[cache_tuple] = long
        return long

    def calc_orb(self, jd, planet1, planet2, aspect, natal_planet_orb=None):
        cache_tuple = (jd, planet1, planet2, aspect)
        if cache_tuple in self.orb_cache:
            return self.orb_cache[cache_tuple]
        lon1 = self.calc_long(jd, planet1)
        lon2 = self.calc_long(jd, planet2) if not natal_planet_orb else natal_planet_orb
        angle = self.angle_difference(lon1, lon2)

        # # Considerazione speciale per le opposizioni
        # if abs(aspect - 180) < 0.001 and abs(angle - 180) < 1:  # Siamo vicini a un'opposizione
        #     orb = 180 - angle
        # else:
        small_interval = 0.0001
        lon1_future = self.calc_long(jd + small_interval, planet1)
        lon2_future = self.calc_long(jd + small_interval, planet2) if not natal_planet_orb else natal_planet_orb
        angle_future = self.angle_difference(lon1_future, lon2_future)

        if angle_future < angle:
            orb = abs(angle) - aspect  # Aspetto applicativo
        else:
            orb = aspect - abs(angle)  # Aspetto separativo

        self.orb_cache[cache_tuple] = orb
        return orb

    def find_aspects(self, look_for_planets, waning_only, full_range=False):
        natal_positions = {planet_data['name']: planet_data['abs_pos'] for planet_data in self.user.planets_list}
        natal_positions['Ascendant'] = self.user.ascendant.abs_pos
        natal_positions['Midheaven'] = self.user.midheaven.abs_pos
        natal_positions['Descendant'] = self.user.descendant.abs_pos
        natal_positions['Imum_Coeli'] = self.user.imum_coeli.abs_pos
        aspects = self.__find_aspects(natal_positions, look_for_planets, waning_only, full_range)
        return aspects

    def angle_difference(self, angle1, angle2):
        return 180 - abs(abs(angle1 - angle2) - 180)

    def jd_to_datetime(self, jd):
        if jd in self.jd_to_dt_cache:
            return self.jd_to_dt_cache[jd]
        jd = jd + 0.5
        Z = int(jd)
        F = jd - Z
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4.)
        B = A + 1524
        C = int((B - 122.1) / 365.25)
        D = int(365.25 * C)
        E = int((B - D) / 30.6001)
        day = B - D - int(30.6001 * E) + F
        month = E - 1 if E < 14 else E - 13
        year = C - 4716 if month > 2 else C - 4715
        day, fractional_day = divmod(day, 1)
        hour, fractional_hour = divmod(fractional_day * 24, 1)
        minute, _ = divmod(fractional_hour * 60, 1)
        if minute == 60:
            hour += 1
            minute = 0
        dt = datetime(int(year), int(month), int(day), int(hour), int(minute))
        self.jd_to_dt_cache[jd] = dt
        return dt
    
    def datetime_to_jd(self, dt: datetime):
        if dt in self.dt_to_jd_cache:
            return self.dt_to_jd_cache[dt]
        julday = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60)
        self.dt_to_jd_cache[dt] = julday
        return julday

    def binary_search_within_interval(self, start_jd, end_jd, objective_function, tol=0.01):
        """Esegue una ricerca binaria sull'intervallo fornito per trovare una radice dell'objective_function."""
        while end_jd - start_jd > tol / (24 * 60):  # Mentre l'intervallo è maggiore di un minuto (tol è in giorni)
            mid_jd = (start_jd + end_jd) / 2.0
            if abs(objective_function(mid_jd)) < 0.001:
                return mid_jd
            if objective_function(start_jd) * objective_function(mid_jd) < 0:
                end_jd = mid_jd
            else:
                start_jd = mid_jd

    def refined_search(self, start_time, end_time, planet1, planet2, aspect, target_orb, natal_planet_orb):
        """Trova l'ora esatta in cui l'orbita si avvicina al target usando prima un intervallo, poi una binary search."""
        # Funzione obiettivo
        def objective_function(jd):
            return self.calc_orb(jd, planet1, planet2, aspect, natal_planet_orb) - target_orb

        start_jd = self.datetime_to_jd(start_time)
        end_jd = self.datetime_to_jd(end_time)
        current_jd = start_jd
        interval = self.planet_names[planet1]['interval'].total_seconds() / 86400.0  # Converti timedelta in giorni

        # Trova l'intervallo in cui l'orbita cambia segno
        while current_jd <= end_jd:
            is_near_opposition = abs(aspect - 180) < 0.001 and abs(objective_function(current_jd)) < 1
            if objective_function(current_jd) * objective_function(current_jd + interval) < 0 or is_near_opposition:
                # Utilizza la binary search all'interno dell'intervallo identificato
                result_jd = self.binary_search_within_interval(current_jd, current_jd + interval, objective_function)
                if result_jd:
                    return self.jd_to_datetime(result_jd), self.calc_orb(result_jd, planet1, planet2, aspect, natal_planet_orb)
            if is_near_opposition:
                current_jd += interval / 10  # avanza di un piccolo intervallo se siamo vicino a un'opposizione
            else:
                current_jd += interval

        # Se non abbiamo trovato un cambio di segno, restituisci None
        return None, None

    def backward_search(self, start_time, planet1, planet2, aspect, target_orb, natal_planet_orb):
        """Ricerca all'indietro per trovare il momento esatto in cui l'aspetto si avvicina al target."""

        def objective_function(jd):
            return abs(self.calc_orb(jd, planet1, planet2, aspect, natal_planet_orb)) - abs(target_orb)

        current_jd = self.datetime_to_jd(start_time)
        one_day = 1.0 / 24 if planet1 == 'Moon' else 1.0

        # Determina l'orientamento iniziale (applicativo o separativo)
        starting_difference = objective_function(current_jd)
        is_applying = starting_difference < 0
        # Ricerca all'indietro
        while True:
            prev_jd = current_jd - one_day
            if (is_applying and objective_function(prev_jd) > 0) or (not is_applying and objective_function(prev_jd) < 0):
                # L'aspetto era separativo e ora è applicativo: abbiamo attraversato il valore target
                result_jd = self.binary_search_within_interval(prev_jd, current_jd, objective_function)
                return self.jd_to_datetime(result_jd), self.calc_orb(result_jd, planet1, planet2, aspect, natal_planet_orb)
            current_jd = prev_jd

    def forward_search(self, start_time, start_orb, planet1, planet2, aspect, target_orb, natal_planet_orb):
        """Searches forward to find the exact time when the aspect reaches the opposite sign of start_orb."""

        def objective_function(jd):
            current_orb = self.calc_orb(jd, planet1, planet2, aspect, natal_planet_orb)
            return current_orb + start_orb  # This will approach zero when the orb is the opposite of start_orb

        current_jd = self.datetime_to_jd(start_time)
        one_day = 1.0 / 24 if planet1 == 'Moon' else 1.0

        # Search forward
        while True:
            next_jd = current_jd + one_day
            if objective_function(current_jd) * objective_function(next_jd) < 0:
                # The orb has passed the opposite value of start_orb
                result_jd = self.binary_search_within_interval(current_jd, next_jd, objective_function)
                return self.jd_to_datetime(result_jd), self.calc_orb(result_jd, planet1, planet2, aspect, natal_planet_orb)
            current_jd = next_jd

    def __find_aspects(self, natal_positions, look_for_planets, waning_only, full_range):
        aspect_list = [] 
        current_aspects = set()
        for planet1 in look_for_planets:
            for planet2_name, natal_position in natal_positions.items():
                if planet2_name in {'Ascendant', 'Midheaven', 'Descendant', 'Imum_Coeli' 'New_Moon'}:
                    planet2_number = planet2_name
                else:
                    planet2_number = next((planet for planet, info in self.planet_names.items() if info['name'] == planet2_name), None)
                if planet2_number is None:
                    continue
                orbit_tolerance = self.planet_names[planet1]['orbit']
                for a in self.aspects:
                    p1_name = self.planet_names[planet1]['name']
                    aspect_name = self.aspect_names[a]
                    aspect_tuple = (p1_name, planet2_name, aspect_name)
                    aspect_tuple = (self.planet_names[planet1]['name'], planet2_name, self.aspect_names[a])
                    if aspect_tuple in current_aspects:
                        continue
                    if waning_only:
                        exact_time, exact_orb = self.refined_search(self.start, self.end, planet1, planet2_number, a, 0, natal_position)
                        start_time, start_orb = None, None
                        if exact_time:
                            start_time, start_orb = self.backward_search(exact_time, planet1, planet2_number, a, -orbit_tolerance, natal_position)
                    else:
                        start_time, start_orb = self.refined_search(self.start, self.end, planet1, planet2_number, a, -orbit_tolerance, natal_position)
                        exact_time, exact_orb = None, None
                    if full_range:
                        cur_orb = self.calc_orb(self.datetime_to_jd(self.start), planet1, planet2_number, a, natal_position)
                        if abs(cur_orb) <= self.planet_names[planet1]['orbit']:
                            start_time, start_orb = self.backward_search(self.start, planet1, planet2_number, a, -orbit_tolerance, natal_position)
                            end_time, end_orb = self.forward_search(start_time, start_orb, planet1, planet2_number, a, orbit_tolerance, natal_position)
                            exact_time, exact_orb = self.refined_search(start_time, end_time, planet1, planet2_number, a, 0, natal_position)
                            duration = end_time - start_time
                    else:
                        end_time, end_orb, duration = None, None, None
                    if start_time:
                        p1_long = self.calc_long(self.datetime_to_jd(start_time), planet1)
                        p1_sign = self.get_zodiac_sign(p1_long)
                        p2_sign = getattr(self.user, planet2_name.lower())['signs'][0]
                        p1_house = self.point_in_house(p1_long)
                        p2_house = getattr(self.user, planet2_name.lower())['house']
    
                        aspect_dict = {
                            'p1_name': p1_name,
                            'p2_name': planet2_name,
                            'p1_sign': p1_sign,
                            'p2_sign': p2_sign,
                            'p1_house': p1_house,
                            'p2_house': p2_house,
                            'aspect': aspect_name,
                            'start': self.__get_local_time(start_time),
                            'exact': self.__get_local_time(exact_time) if exact_time else None,
                            'end': self.__get_local_time(end_time) if end_time else None,
                            'start_orb': start_orb,
                            'exact_orb': exact_orb,
                            'end_orb': end_orb,
                            'duration': duration,
                            'ascendant': {
                                'start': self.find_ascendant(self.datetime_to_jd(start_time)),
                                'exact': self.find_ascendant(self.datetime_to_jd(exact_time)) if exact_time else None,
                                'end': self.find_ascendant(self.datetime_to_jd(end_time)) if end_time else None
                            }
                        }
                        if not self.is_fake_aspect(aspect_dict):
                            if waning_only:
                                if exact_time:
                                    aspect_list.append(aspect_dict)
                                    current_aspects.add(aspect_tuple)
                            else:
                                aspect_list.append(aspect_dict)
                                current_aspects.add(aspect_tuple)
        aspect_list.sort(key=lambda x: x['start'] if x['start'] else x['exact'])
        return aspect_list

    def is_fake_aspect(self, aspect: dict) -> bool:
        p1_name = aspect['p1_name'].lower().replace(' ', '_')
        p2_name = aspect['p2_name'].lower().replace(' ', '_')
        p1_sign = aspect['p1_sign']
        p2_sign = aspect['p2_sign']
        element_1 = self.signs_dict[p1_sign]['element']
        element_2 = self.signs_dict[p2_sign]['element']
        if p1_name == 'true_node' and p2_name == 'south_node':
            return True
        if element_1 == element_2 and aspect['aspect'] == 'square':
            return True
        orb = aspect['exact_orb'] if aspect['exact_orb'] else aspect['start_orb']
        if aspect['aspect'] in {'trine', 'conjunction'} and element_1 != element_2 and abs(orb) > 1.5:
            return True
        if aspect['aspect'] == 'opposition':
            p1_sign_opposite = self.user.signs_dict[p1_sign]['opposite']
            return not p1_sign_opposite.startswith(p2_sign)
        return False

    def get_zodiac_sign(self, lon):
        signs = ['Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 
                'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis']
        return signs[int(lon // 30)]

    def calculate_transitions(self, look_for_planets):
        sign_transitions = dict()
        house_transitions = dict()
        direction_transitions = dict()
        for planet in look_for_planets:
            current_time = self.start
            while current_time <= self.end:
                jd = self.datetime_to_jd(current_time)
                lon = self.calc_long(jd, planet)
                current_sign = self.get_zodiac_sign(lon)
                current_house = self.point_in_house(lon)
                current_direction = swe.calc(jd, planet)[0][3] < 0
                interval = timedelta(minutes=15)
                while current_time <= self.end:
                    current_time += interval
                    jd = self.datetime_to_jd(current_time)
                    lon = self.calc_long(jd, planet)
                    old_sign = current_sign
                    old_house = current_house
                    old_direction = current_direction
                    current_sign = self.get_zodiac_sign(lon)
                    current_house = self.point_in_house(lon)
                    current_direction = swe.calc(jd, planet)[0][3] < 0
                    if old_sign != current_sign:
                        sign_transitions[self.planet_names[planet]['name']] = {'when': self.__get_local_time(current_time), 'old': old_sign, 'new': current_sign, 'ascendant': self.find_ascendant(jd), 'sign': current_sign, 'house': current_house}
                    if old_direction != current_direction:
                        new_motus = "retrograde" if current_direction else "direct"
                        old_motus = "retrograde" if new_motus == "direct" else "direct"
                        direction_transitions[self.planet_names[planet]['name']] = {'when': self.__get_local_time(current_time), 'old': old_motus, 'new': new_motus, 'ascendant': self.find_ascendant(jd), 'sign': current_sign, 'house': current_house}
                    if old_house != current_house:
                        house_transitions[self.planet_names[planet]['name']] = {'when': self.__get_local_time(current_time), 'old': old_house, 'new': current_house, 'ascendant': self.find_ascendant(jd), 'sign': current_sign, 'house': current_house}
        return sign_transitions, house_transitions, direction_transitions

    def prev_new_moon(self):
        """
        Trova il momento del precedente novilunio per una data specificata.

        Parametri:
        - date: una datetime.date o datetime.datetime indicante la data di riferimento.

        Restituisce:
        - Una datetime.datetime rappresentante il momento del precedente novilunio.
        """
        def create_new_moon_obj(jd, orb, aspects):
            moon_longitude = self.calc_long(jd, swe.MOON)
            return {
                'when':  self.__get_local_time(self.jd_to_datetime(jd)),
                'orb': orb,
                'sign': self.get_zodiac_sign(moon_longitude),
                'house': self.point_in_house(moon_longitude),
                'abs_pos': moon_longitude,
                'ascendant': self.find_ascendant(jd),
                'aspects': aspects
            }
        jd_start = self.datetime_to_jd(self.end)
        precision = 1.0 / 2
        delta_long_threshold = 12
        while precision > (1.0 / (24 * 60)):
            sun_long = self.calc_long(jd_start, swe.SUN)
            moon_long = self.calc_long(jd_start, swe.MOON)
            delta_long = (moon_long - sun_long) % 360
            if delta_long < delta_long_threshold:
                precision /= 24
                delta_long_threshold /= 24
            else:
                jd_start -= precision
        new_moon_datetime = self.jd_to_datetime(jd_start)
        new_moon_instance = KrInstance(
            name='New Moon',
            year= new_moon_datetime.year,
            month= new_moon_datetime.month,
            day= new_moon_datetime.day,
            hour= new_moon_datetime.hour,
            minute= new_moon_datetime.minute,
            lat=self.transit_latitude,
            lng=self.transit_longitude,
            tz_str=self.tz_str,
            house_method='Vehlow'
        )
        aspects = CompositeAspects(new_moon_instance, self.user, self.settings)
        relevant_aspects = aspects.get_relevant_aspects()
        relevant_aspects = [relevant_aspect for relevant_aspect in relevant_aspects if relevant_aspect['p1_name'] == 'Sun']
        return create_new_moon_obj(jd_start, delta_long, relevant_aspects)

    def lunar_phase(self, new_moon_date, new_moon_position, start=None, end=None):
        """
        Trova gli aspetti della luna con la posizione del Novilunio.

        Parametri:
        - start: datetime di inizio.
        - end: datetime di fine.
        - new_moon_date: data del Novilunio precedente.
        - new_moon_position: longitudine del punto di Novilunio.

        Restituisce:
        - Una lista di tuple, dove ogni tupla contiene la data e l'aspetto.
        """
        def create_lunar_phase_obj(time, orb, aspect, new_moon_date):
            julian_day = self.datetime_to_jd(time)
            moon_longitude = self.calc_long(julian_day, swe.MOON)
            days_since_new_moon = (self.__get_utc(self.__get_local_time(time)) - self.__get_utc(new_moon_date)).days
            aspect_key = aspect
            if days_since_new_moon > 14 and aspect != 180:
                aspect_key = 360 - aspect  # Fase lunare speculare
            return {
                'when': self.__get_local_time(time),
                'orb': orb,
                'aspect': self.aspect_names[aspect],
                'aspect_degrees': aspect,
                'phase': angle_to_phase(aspect_key),
                'sign': self.get_zodiac_sign(moon_longitude),
                'house': self.point_in_house(moon_longitude),
                'abs_pos': moon_longitude,
                'ascendant': self.find_ascendant(julian_day)
            }

        def angle_to_phase(angle):
            if angle == 0:
                return "New Moon"
            elif 0 < angle < 90:
                return "Waxing Crescent"
            elif angle == 90:
                return "First Quarter"
            elif 90 < angle < 180:
                return "Waxing Gibbous"
            elif angle == 180:
                return "Full Moon"
            elif 180 < angle < 270:
                return "Waning Gibbous"
            elif angle == 270:
                return "Last Quarter"
            elif angle > 270:
                return "Waning Crescent"

        results = []
        start = self.start if start is None else self.__get_utc(start) 
        end = self.end if end is None else self.__get_utc(end)
        for aspect in self.aspects:
            exact_time, orb = self.refined_search(start, end, swe.MOON, "New_Moon", aspect, 0, new_moon_position)
            if exact_time:
                results.append(create_lunar_phase_obj(time=exact_time, orb=orb, aspect=aspect, new_moon_date=new_moon_date))
        return results

    def point_in_house(self, point_long):
        for house in self.user.houses_list:
            lower_bound = house['abs_pos']
            upper_bound = (house['abs_pos'] + 30) % 360
            if lower_bound <= upper_bound:
                if lower_bound <= point_long < upper_bound:
                    return house['name']
            else:
                if point_long >= lower_bound or point_long < upper_bound:
                    return house['name']
    
    def find_ascendant(self, julian_day):
        hsys = bytes(self.hsys, 'ascii') 
        cusps, ascmc = swe.houses(julday=julian_day, lat=self.transit_latitude, lon=self.transit_longitude, hsys=hsys)
        ascendant = ascmc[0]
        house = self.point_in_house(ascendant)
        sign = self.get_zodiac_sign(ascendant)
        return {
            'sign': sign,
            'house': house
        }