from enum import Enum


class UserTeamRole(str, Enum):
    leader = 'leader'
    captain = 'captain'
    member = 'member'
    inactive = 'inactive'
    invited = 'invited'


class MatchType(str, Enum):
    group = 'group'
    quarter_final = 'quarter_final'
    semi_final = 'semi_final'
    silver_final = 'silver_final'
    grand_final = 'grand_final'


class GameType(int, Enum):
    team_survivor = 4
    capture_the_flag = 7
