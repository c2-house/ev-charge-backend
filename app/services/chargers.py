import json
from fastapi import status
from app.core.config import app_settings
from app.core.lifespan import states
from app.utils.data_handlers import PublicEvChagerDataHandler
from fastapi_mctools.cache.redis import RedisCache
from fastapi_mctools.exceptions import HTTPException

redis = RedisCache("redis://redis:6379/0")


async def get_chagers_from_public(district_code: str) -> dict:
    api_key = app_settings.PUBLIC_API_KEY
    url = "http://apis.data.go.kr/B552584/EvCharger/getChargerInfo"
    params = {
        "serviceKey": api_key,
        "numOfRows": 9999,
        "pageNo": 1,
        "dataType": "JSON",
        "zscode": district_code,
    }
    session = states["api_client"]

    try:
        resp = await session.get(url, params=params)
        data = await resp.json()
        return data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
            code="INTERNAL_SERVER_ERROR",
            message="발생하면 안되는 에러가 발생하는건디?!",
        )


async def get_organized_chargers(districtCode: str, lat: str, lng: str) -> dict:
    data_handler = PublicEvChagerDataHandler()
    cached_data = await redis.get(districtCode)
    if cached_data:
        cached_data = json.loads(cached_data)
        current_lat_lng = data_handler.convert_to_coord(lat, lng)

        for station in cached_data["stations"]:
            station["distance"] = data_handler.get_haversine_distance(
                current_lat_lng,
                data_handler.convert_to_coord(station["lat"], station["lng"]),
            )

        cached_data["stations"].sort(key=lambda x: x["distance"])
        return cached_data

    all_chargers_data = await get_chagers_from_public(districtCode)
    total_count = all_chargers_data.get("totalCount")
    chargers = all_chargers_data.get("items").get("item")

    stations = []
    for charger in chargers:
        existing_station = next(
            (station for station in stations if station["statId"] == charger["statId"]),
            None,
        )
        if existing_station:
            existing_station["availableCount"] += (
                1 if data_handler.is_available(charger["stat"]) else 0
            )
            existing_station["hasFastCharger"] = existing_station[
                "hasFastCharger"
            ] or data_handler.is_fast_charger(charger["chgerType"])
            existing_station["chargers"].append(
                {
                    "chgerId": charger["chgerId"],
                    "chgerType": charger["chgerType"],
                    "stat": charger["stat"],
                    "statUpdDt": charger["statUpdDt"],
                    "lastTedt": charger["lastTedt"],
                    "nowTsdt": charger["nowTsdt"],
                    "output": charger["output"],
                }
            )

        else:
            data = {
                "statId": charger["statId"],
                "statNm": charger["statNm"],
                "addr": charger["addr"],
                "lat": charger["lat"],
                "lng": charger["lng"],
                "distance": data_handler.get_haversine_distance(
                    data_handler.convert_to_coord(lat, lng),
                    data_handler.convert_to_coord(charger["lat"], charger["lng"]),
                ),
                "location": data_handler.remove_null_string(charger["location"]),
                "useTime": data_handler.convert_usetime(charger["useTime"]),
                "bnm": data_handler.remove_null_string(charger["bnm"]),
                "busiCall": data_handler.remove_null_string(charger["busiCall"]),
                "kindDetail": data_handler.remove_null_string(charger["kindDetail"]),
                "parkingFree": data_handler.convert_to_bool_or_none(
                    charger["parkingFree"]
                ),
                "note": data_handler.remove_null_string(charger["note"]),
                "limitDetail": data_handler.remove_null_string(charger["limitDetail"]),
                "delDetail": data_handler.remove_null_string(charger["delDetail"]),
                "availableCount": 1
                if data_handler.is_available(charger["stat"])
                else 0,
                "hasFastCharger": data_handler.is_fast_charger(charger["chgerType"]),
                "markerType": 0,
                "chargers": [
                    {
                        "chgerId": charger["chgerId"],
                        "chgerType": charger["chgerType"],
                        "stat": charger["stat"],
                        "statUpdDt": charger["statUpdDt"],
                        "lastTedt": charger["lastTedt"],
                        "nowTsdt": charger["nowTsdt"],
                        "output": charger["output"],
                    }
                ],
            }
            stations.append(data)

    for station in stations:
        station["markerType"] = data_handler.get_marker_type(
            station["availableCount"], station["hasFastCharger"]
        )

    stations.sort(key=lambda x: x["distance"])
    result = {
        "chargerCount": total_count,
        "stationCount": len(stations),
        "stations": stations,
    }

    await redis.set(districtCode, json.dumps(result), 60 * 5)

    return result
