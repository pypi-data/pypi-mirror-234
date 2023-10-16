from ftwgl import FTWClient, GameServer


def gameserver_from_dict(server: dict, ftw_client: FTWClient) -> GameServer:
    return GameServer(
        id=server['id'],
        dcid=server['config']['dcid'],
        ip=None,
        password=server['config']['password'],
        rcon_password=server['config']['rcon'],
        ftw_client=ftw_client
    )
