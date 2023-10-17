import aiohttp
import logging

from .const import (
    LOGIN,
    GET_OPERATION_MODE,
    GET_TARGET_TEMPERATURE,
    GET_TEMPERATURE,
    SET_OPERATION_MODE,
    SET_TEMPERATURE,
)

_LOGGER = logging.getLogger(__name__)

async def login(username, password):
    payload = {
                "email": username,
                "password": password,
                "userDeviceId": "h53pr40n3tHomeAssistant",
                "language": "eng",
            }
    url = LOGIN
    try:
        async with aiohttp.ClientSession() as session, session.post(
            url, json=payload
        ) as response:
            if response.status == 200:
                # Authentication successful
                userData = await response.json()
                return {
                        "success": True,
                        "access_token": userData["access_token"],
                        "refresh_token": userData["refresh_token"],
                        "spa_name": userData["spa_name"],
                    }

            # Authentication failed
            _LOGGER.error(
                "Authentication failed with status code: %s",
                response.status,
            )
        return { "success": False }
        

    except aiohttp.ClientError as err:
        _LOGGER.error("Error occurred during API call: %s", err)
        return { "success": False }


async def getCurrentTemperature(access_token) -> float:
        """Retrieve current temperature."""
        headers = {"Authorization": f"Bearer {access_token}"}
        url = GET_TEMPERATURE
        try:
            async with aiohttp.ClientSession() as session, session.get(
                url, headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("temperature") / 10.0

                _LOGGER.error(
                    "Get Temperature failed with status code: %s",
                    response.status,
                )
                return 0.0

        except aiohttp.ClientError as err:
            _LOGGER.error("Error occurred during API call: %s", err)
            return 0.0

async def getTargetTemperature(access_token) -> float:
    """Get target temperature."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = GET_TARGET_TEMPERATURE
    try:
        async with aiohttp.ClientSession() as session, session.get(
            url, headers=headers
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("temperature") / 10.0

            _LOGGER.error(
                "Get Temperature failed with status code: %s",
                response.status,
            )
            return 0.0

    except aiohttp.ClientError as err:
        _LOGGER.error("Error occurred during API call: %s", err)
        return 0.0

async def getOperationMode(access_token) -> str:
    """Retrieve operation mode."""
    headers = {"Authorization": f"Bearer {access_token}"}
    url = GET_OPERATION_MODE
    try:
        async with aiohttp.ClientSession() as session, session.get(
            url, headers=headers
        ) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("mode")

            _LOGGER.error(
                "Get Temperature failed with status code: %s",
                response.status,
            )
            return ""

    except aiohttp.ClientError as err:
        _LOGGER.error("Error occurred during API call: %s", err)
        return ""

async def setTemperature(temperature, access_token):
    """Set target temperature."""
    headers = {
        "Content-Type": "application/json",
    }
    payload = {"temperature": temperature}
    headers = {"Authorization": f"Bearer {access_token}"}
    url = SET_TEMPERATURE
    try:
        async with aiohttp.ClientSession() as session, session.post(
            url, json=payload, headers=headers
        ) as response:
            if response.status == 200:
                _LOGGER.info("New temperature set successfully")
                return True

            _LOGGER.error(
                "Set Temperature failed with status code: %s",
                response.status,
            )
            return False

    except aiohttp.ClientError as err:
        _LOGGER.error("Error occurred during API call: %s", err)
        return False

async def setOperationMode(operation_mode, access_token):
    """Set spa operation mode. Modes are: NORM, AWAY, WEEKEND."""
    headers = {
        "Content-Type": "application/json",
    }
    payload = {"mode": operation_mode}
    headers = {"Authorization": f"Bearer {access_token}"}
    url = SET_OPERATION_MODE
    try:
        async with aiohttp.ClientSession() as session, session.post(
            url, json=payload, headers=headers
        ) as response:
            if response.status == 200:
                _LOGGER.info("New mode set successfully")
                return True

            _LOGGER.error(
                "Set Operation Mode failed with status code: %s",
                response.status,
            )
            return False

    except aiohttp.ClientError as err:
        _LOGGER.error("Error occurred during API call: %s", err)
        return False
