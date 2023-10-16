import datetime
from typing import List, Optional, Dict, Union

import aiohttp
from aiohttp import ClientResponse

from ftwgl.enum import UserTeamRole, MatchType, GameType


class FTWClient:
    def __init__(self, ftw_api_key: str, ftw_host: str = 'https://ftwgl.net'):
        if ftw_api_key is None or len(ftw_api_key) == 0:
            raise ValueError('ftw_api_key required, but not set')

        self.ftw_host = ftw_host
        self.ftw_api_key = ftw_api_key

    @staticmethod
    async def _handle_response_body(resp: ClientResponse) -> Union[Dict, str]:
        if resp.content_type == 'application/json':
            return await resp.json()
        else:
            return await resp.text()

    async def _handle_response(self, resp: ClientResponse, extract_key: str = None) -> Optional[Union[dict, str, int]]:
        resp_body = await self._handle_response_body(resp)
        print(f"Request {resp.status} {resp.request_info.method} {resp.request_info.url}")
        print(resp_body)
        if extract_key is None:
            return resp_body
        elif extract_key in resp_body:
            return resp_body[extract_key]
        else:
            return None

    async def cup_create(self, name: str, abbreviation: str, playoff_length: int, minimum_roster_size: int,
                         start_date: datetime, roster_lock_date: datetime) -> int:
        request_body = {
            'name': name,
            'abbreviation': abbreviation,
            'playoff_length': playoff_length,
            'minimum_roster_size': minimum_roster_size,
            'start_date': start_date.timestamp(),
            'roster_lock_date': roster_lock_date.timestamp()
        }
        print(request_body)
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.post(f"{self.ftw_host}/api/v1/cup", json=request_body) as resp:
                return await self._handle_response(resp, 'cup_id')

    async def launch_ac(self, cup_id: int, match_id, discord_id):
        request_body = {
            'cup_id': cup_id,
            'match_id': match_id,
            'discord_id': discord_id
        }
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.post(f"{self.ftw_host}/api/v1/cup/user/launch", json=request_body) as resp:
                return await self._handle_response(resp)

    # Creates a user if one does not exist, otherwise updates based on existing discord_id
    async def user_create_or_update(self, discord_id: int, discord_username: str, urt_auth: str):
        request_body = {
            'discord_id': discord_id,
            'discord_username': discord_username,
            'urt_auth': urt_auth
        }
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.post(f"{self.ftw_host}/api/v1/user", json=request_body) as resp:
                return await self._handle_response(resp)

    async def team_create(self, creator_discord_id: int, team_name: str, team_tag: str) -> int:
        request_body = {
            'creator_discord_id': creator_discord_id,
            'name': team_name,
            'tag': team_tag
        }
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.post(f"{self.ftw_host}/api/v1/team", json=request_body) as resp:
                return await self._handle_response(resp, 'team_id')

    async def cup_add_team(self, team_id: int, cup_id: int):
        request_body = {
            'team_id': team_id,
            'cup_id': cup_id
        }
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.post(f"{self.ftw_host}/api/v1/cup/team/add", json=request_body) as resp:
                await self._handle_response(resp)

    async def cup_remove_team(self, team_id: int, cup_id: int):
        request_body = {
            'team_id': team_id,
            'cup_id': cup_id
        }
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.post(f"{self.ftw_host}/api/v1/cup/team/remove", json=request_body) as resp:
                await self._handle_response(resp)

    async def cup_set_team_division(self, cup_id: int, team_id: int, division: int):
        request_body = {
            'cup_id': cup_id,
            'team_id': team_id,
            'division': division
        }
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.put(f"{self.ftw_host}/api/v1/cup/team/division", json=request_body) as resp:
                await self._handle_response(resp)

    async def team_add_user_or_update_role(self, team_id: int, discord_id: int, role: UserTeamRole):
        request_body = {
            'team_id': team_id,
            'discord_id': discord_id,
            'role': role.value
        }
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.post(f"{self.ftw_host}/api/v1/team/user/join", json=request_body) as resp:
                await self._handle_response(resp)

    async def team_remove_user(self, team_id: int, discord_id: int):
        request_body = {
            'team_id': team_id,
            'discord_id': discord_id
        }
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.post(f"{self.ftw_host}/api/v1/team/user/quit", json=request_body) as resp:
                await self._handle_response(resp)

    async def match_create(self, cup_id: int, team_ids: List[int], best_of: int,
                           match_type: MatchType, match_date: Optional[datetime.datetime]) -> int:
        request_body = {
            'cup_id': cup_id,
            'team_ids': team_ids,
            'best_of': best_of,
            'match_type': match_type.value,
            'match_date': match_date.timestamp() if match_date is not None else match_date
        }

        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.post(f"{self.ftw_host}/api/v1/match", json=request_body) as resp:
                return await self._handle_response(resp, 'match_id')

    async def match_update(self, match_id: int, match_date: datetime.datetime):
        request_body = {
            'match_id': match_id,
            'match_date': match_date.timestamp()
        }

        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.put(f"{self.ftw_host}/api/v1/match", json=request_body) as resp:
                await self._handle_response(resp)

    async def get_match_rounds(self, match_id: int):
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.get(f"{self.ftw_host}/api/v1/match/round/{match_id}") as resp:
                return await self._handle_response(resp)

    async def server_locations(self) -> dict:
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.get(f"{self.ftw_host}/api/v1/rent/locations") as resp:
                return await self._handle_response(resp)

    async def server_get_with_id(self, server_id: int) -> Optional[dict]:
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.get(f"{self.ftw_host}/api/v1/rent/{server_id}") as resp:
                return await self._handle_response(resp)

    async def server_active(self) -> dict:
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.get(f"{self.ftw_host}/api/v1/rent/active") as resp:
                return await self._handle_response(resp)

    # Server will likely take a couple of minutes to boot, so use the returned
    async def server_rent(self, match_id: int, dcid: str, gametype: GameType,
                          rcon: str, password: str, ttl_hours: int) -> int:
        request_body = {
            'match_id': match_id,
            'dcid': dcid,
            'gametype': gametype.value,
            'rcon': rcon,
            'password': password,
            'ttl_hours': ttl_hours
        }
        async with aiohttp.ClientSession() as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.post(f"{self.ftw_host}/api/v1/rent/match", json=request_body) as resp:
                return await self._handle_response(resp, 'id')

    async def match_ac_check(self, match_id: int):
        async with aiohttp.ClientSession as session:
            session.headers.add("Authorization", f"{self.ftw_api_key}")
            async with session.get(f"/api/v1/match/ac_usage/{match_id}") as resp:
                return await self._handle_response(resp)
