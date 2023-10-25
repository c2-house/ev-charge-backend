import math
from dataclasses import dataclass


@dataclass
class MarkerType:
    AVAILABLE_FAST: int = 0
    AVAILABLE_SLOW: int = 1
    UNAVAILABLE_FAST: int = 2
    UNAVAILABLE_SLOW: int = 3


class PublicEvChagerDataHandler:
    def is_fast_charger(self, charget_type: str) -> bool:
        return charget_type != "02"

    def is_available(self, stat: str) -> bool:
        return stat == "2"

    def remove_null_string(self, text: str) -> str:
        text = text.replace("null", "")
        return text

    def convert_to_bool(self, text: str) -> bool:
        return text == "Y"

    def convert_to_bool_or_none(self, text: str) -> bool:
        match text:
            case "Y":
                return True
            case "N":
                return False
            case _:
                return None

    def convert_usetime(self, use_time: str) -> str:
        return (
            "24시간" if use_time.startswith("24") else self.remove_null_string(use_time)
        )

    def get_marker_type(self, availableCount: int, hasFastCharger: bool):
        if availableCount > 0:
            return (
                MarkerType.AVAILABLE_FAST
                if hasFastCharger
                else MarkerType.AVAILABLE_SLOW
            )
        else:
            return (
                MarkerType.UNAVAILABLE_FAST
                if hasFastCharger
                else MarkerType.UNAVAILABLE_SLOW
            )

    def get_haversine_distance(self, current_location: tuple, target_location: tuple):
        current_lat, current_lng = current_location
        target_lat, target_lng = target_location
        radius_of_earth = 6371

        d_lat = math.radians(target_lat - current_lat)
        d_lng = math.radians(target_lng - current_lng)

        a = math.sin(d_lat / 2) * math.sin(d_lat / 2) + math.cos(
            math.radians(current_lat)
        ) * math.cos(math.radians(target_lat)) * math.sin(d_lng / 2) * math.sin(
            d_lng / 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = radius_of_earth * c
        distance = round(distance, 3)
        return distance

    def convert_distance(self, distance: float) -> str:
        if distance < 1:
            return f"{distance*1000}m"
        else:
            distance = round(distance, 1)
            return f"{distance}km"

    def convert_to_coord(self, lat: str, lng: str) -> tuple:
        return (float(lat), float(lng))
