from attrs import frozen

from gd.enums import Difficulty, LevelLength
from gd.versions import GameVersion

__all__ = ("OFFICIAL_LEVELS", "OfficialLevel")


@frozen()
class OfficialLevel:
    id: int
    song_id: int
    name: str
    stars: int
    coins: int
    difficulty: Difficulty
    length: LevelLength
    game_version: GameVersion
    demon: bool


OFFICIAL_LEVELS = (
    OfficialLevel(
        id=1,
        song_id=1,
        name="Stereo Madness",
        stars=1,
        coins=3,
        difficulty=Difficulty.EASY,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 0),
        demon=False,
    ),
    OfficialLevel(
        id=2,
        song_id=2,
        name="Back On Track",
        stars=2,
        coins=3,
        difficulty=Difficulty.EASY,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 0),
        demon=False,
    ),
    OfficialLevel(
        id=3,
        song_id=3,
        name="Polargeist",
        stars=3,
        coins=3,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 0),
        demon=False,
    ),
    OfficialLevel(
        id=4,
        song_id=4,
        name="Dry Out",
        stars=4,
        coins=3,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 0),
        demon=False,
    ),
    OfficialLevel(
        id=5,
        song_id=5,
        name="Base After Base",
        stars=5,
        coins=3,
        difficulty=Difficulty.HARD,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 0),
        demon=False,
    ),
    OfficialLevel(
        id=6,
        song_id=6,
        name="Can't Let Go",
        stars=6,
        coins=3,
        difficulty=Difficulty.HARD,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 0),
        demon=False,
    ),
    OfficialLevel(
        id=7,
        song_id=7,
        name="Jumper",
        stars=7,
        coins=3,
        difficulty=Difficulty.HARDER,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 0),
        demon=False,
    ),
    OfficialLevel(
        id=8,
        song_id=8,
        name="Time Machine",
        stars=8,
        coins=3,
        difficulty=Difficulty.HARDER,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 1),
        demon=False,
    ),
    OfficialLevel(
        id=9,
        song_id=9,
        name="Cycles",
        stars=9,
        coins=3,
        difficulty=Difficulty.HARDER,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 2),
        demon=False,
    ),
    OfficialLevel(
        id=10,
        song_id=10,
        name="xStep",
        stars=10,
        coins=3,
        difficulty=Difficulty.INSANE,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 3),
        demon=False,
    ),
    OfficialLevel(
        id=11,
        song_id=11,
        name="Clutterfunk",
        stars=11,
        coins=3,
        difficulty=Difficulty.INSANE,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 4),
        demon=False,
    ),
    OfficialLevel(
        id=12,
        song_id=12,
        name="Theory of Everything",
        stars=12,
        coins=3,
        difficulty=Difficulty.INSANE,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 5),
        demon=False,
    ),
    OfficialLevel(
        id=13,
        song_id=13,
        name="Electroman Adventures",
        stars=10,
        coins=3,
        difficulty=Difficulty.INSANE,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 6),
        demon=False,
    ),
    OfficialLevel(
        id=14,
        song_id=14,
        name="Clubstep",
        stars=14,
        coins=3,
        difficulty=Difficulty.EASY_DEMON,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 6),
        demon=True,
    ),
    OfficialLevel(
        id=15,
        song_id=15,
        name="Electrodynamix",
        stars=12,
        coins=3,
        difficulty=Difficulty.INSANE,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 7),
        demon=False,
    ),
    OfficialLevel(
        id=16,
        song_id=16,
        name="Hexagon Force",
        stars=12,
        coins=3,
        difficulty=Difficulty.INSANE,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 8),
        demon=False,
    ),
    OfficialLevel(
        id=17,
        song_id=17,
        name="Blast Processing",
        stars=10,
        coins=3,
        difficulty=Difficulty.HARDER,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 9),
        demon=False,
    ),
    OfficialLevel(
        id=18,
        song_id=18,
        name="Theory of Everything 2",
        stars=14,
        coins=3,
        difficulty=Difficulty.EASY_DEMON,
        length=LevelLength.LONG,
        game_version=GameVersion(1, 9),
        demon=True,
    ),
    OfficialLevel(
        id=19,
        song_id=19,
        name="Geometrical Dominator",
        stars=10,
        coins=3,
        difficulty=Difficulty.HARDER,
        length=LevelLength.LONG,
        game_version=GameVersion(2, 0),
        demon=False,
    ),
    OfficialLevel(
        id=20,
        song_id=20,
        name="Deadlocked",
        stars=15,
        coins=3,
        difficulty=Difficulty.MEDIUM_DEMON,
        length=LevelLength.LONG,
        game_version=GameVersion(2, 0),
        demon=True,
    ),
    OfficialLevel(
        id=21,
        song_id=21,
        name="Fingerdash",
        stars=12,
        coins=3,
        difficulty=Difficulty.INSANE,
        length=LevelLength.LONG,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=1001,
        song_id=22,
        name="The Seven Seas",
        stars=1,
        coins=3,
        difficulty=Difficulty.EASY,
        length=LevelLength.LONG,
        game_version=GameVersion(2, 0),
        demon=False,
    ),
    OfficialLevel(
        id=1002,
        song_id=23,
        name="Viking Arena",
        stars=2,
        coins=3,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.LONG,
        game_version=GameVersion(2, 0),
        demon=False,
    ),
    OfficialLevel(
        id=1003,
        song_id=24,
        name="Airborne Robots",
        stars=3,
        coins=3,
        difficulty=Difficulty.HARD,
        length=LevelLength.LONG,
        game_version=GameVersion(2, 0),
        demon=False,
    ),
    OfficialLevel(
        id=2001,
        song_id=26,
        name="Payload",
        stars=2,
        coins=0,
        difficulty=Difficulty.EASY,
        length=LevelLength.SHORT,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=2002,
        song_id=27,
        name="Beast Mode",
        stars=3,
        coins=0,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.MEDIUM,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=2003,
        song_id=28,
        name="Machina",
        stars=3,
        coins=0,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.MEDIUM,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=2004,
        song_id=29,
        name="Years",
        stars=3,
        coins=0,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.MEDIUM,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=2005,
        song_id=30,
        name="Frontlines",
        stars=3,
        coins=0,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.MEDIUM,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=2006,
        song_id=31,
        name="Space Pirates",
        stars=3,
        coins=0,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.MEDIUM,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=2007,
        song_id=32,
        name="Striker",
        stars=3,
        coins=0,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.MEDIUM,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=2008,
        song_id=33,
        name="Embers",
        stars=3,
        coins=0,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.SHORT,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=2009,
        song_id=34,
        name="Round 1",
        stars=3,
        coins=0,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.MEDIUM,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=2010,
        song_id=35,
        name="Monster Dance Off",
        stars=3,
        coins=0,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.MEDIUM,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=3001,
        song_id=25,
        name="The Challenge",
        stars=3,
        coins=0,
        difficulty=Difficulty.HARD,
        length=LevelLength.SHORT,
        game_version=GameVersion(2, 1),
        demon=False,
    ),
    OfficialLevel(
        id=4001,
        song_id=36,
        name="Press Start",
        stars=4,
        coins=3,
        difficulty=Difficulty.NORMAL,
        length=LevelLength.LONG,
        game_version=GameVersion(2, 2),
        demon=False,
    ),
    OfficialLevel(
        id=4002,
        song_id=37,
        name="Nock Em",
        stars=6,
        coins=3,
        difficulty=Difficulty.HARD,
        length=LevelLength.LONG,
        game_version=GameVersion(2, 2),
        demon=False,
    ),
    OfficialLevel(
        id=4003,
        song_id=38,
        name="Power Trip",
        stars=8,
        coins=3,
        difficulty=Difficulty.HARDER,
        length=LevelLength.LONG,
        game_version=GameVersion(2, 2),
        demon=False,
    ),
)
