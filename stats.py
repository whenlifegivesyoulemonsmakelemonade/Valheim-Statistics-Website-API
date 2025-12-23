from systemd import journal
from flask import Flask

import time
import json
from threading import Thread, Event
import signal


class Profile():
    def __init__(self, name: str,
                 online: bool = False, 
                 connectTime: float = 0.0, connectTimestamp: float = 0.0, 
                 disconnectTime: float = 0.0, disconnectTimestamp: float = 0.0,
                 totalPlaytime: float = 0.0):
        self.profiles.append(self)

        self.name = name

        self.online = online
        self.connectTime = connectTime
        self.connectTimestamp = connectTimestamp
        self.disconnectTime = disconnectTime
        self.disconnectTimestamp = disconnectTimestamp
        self.totalPlaytime = totalPlaytime

    def count(self) -> int:
        return len(self.profiles)
    

    # Playtime tracking methods
    def getOntime(self) -> float:
        if hasattr(self, 'connectTime'):
            return time.monotonic() - self.connectTime
        return 0.0
    
    def getOfftime(self) -> float:
        if hasattr(self, 'disconnectTime'):
            return time.monotonic() - self.disconnectTime
        return 0.0

    def getPlaytime(self) -> float:
        if hasattr(self, 'connectTime') and hasattr(self, 'disconnectTime'):
            return self.disconnectTime - self.connectTime
        return 0.0


    # Event handlers
    def OnConnect(self):
        self.online = True
        self.connectTime = time.monotonic()
        self.connectTimestamp = time.time()     # Time in seconds since epoch (1970-01-01 00:00:00 UTC) (Unix time)

    def OnDisconnect(self):
        self.online = False
        self.disconnectTime = time.monotonic()
        self.disconnectTimestamp = time.time()      # Time in seconds since epoch (1970-01-01 00:00:00 UTC) (Unix time)
        self.totalPlaytime += self.getPlaytime()


class Player():
    count: int
    all: list

    def __init__(self, steamID: str, 
                 profiles: list = [], 
                 online: bool = False,
                 connectTime: float = 0.0, connectTimestamp: float = 0.0, 
                 disconnectTime: float = 0.0, disconnectTimestamp: float = 0.0,
                 totalPlaytime = 0.0):
        Player.all.append(self)

        self.steamID = steamID

        self.profiles = profiles
        self.online = online
        self.connectTime = connectTime
        self.connectTimestamp = connectTimestamp
        self.disconnectTime = disconnectTime
        self.disconnectTimestamp = disconnectTimestamp
        self.totalPlaytime = totalPlaytime

    def count(self) -> int:
        return Player.count
    
    def getAll(self) -> list:
        return Player.all


    # Profile Management
    def addProfile(self, profile: Profile):
        self.profiles.append(profile)


    # Playtime tracking methods
    def getOntime(self) -> float:
        if hasattr(self, 'connectTime'):
            return time.monotonic() - self.connectTime
        return 0.0
    
    def getOfftime(self) -> float:
        if hasattr(self, 'disconnectTime'):
            return time.monotonic() - self.disconnectTime
        return 0.0

    def getPlaytime(self) -> float:
        if hasattr(self, 'connectTime') and hasattr(self, 'disconnectTime'):
            return self.disconnectTime - self.connectTime
        return 0.0


    # Event handlers
    def pullRequest(self) -> json:
        data: json = {"steamID": self.steamID,
                      "online": self.online,
                      "ontime": self.getOntime(), "onsince": self.connectTimestamp,
                      "offtime": self.getOfftime(), "offsince": self.disconnectTimestamp,
                      "totalPlaytime": self.totalPlaytime + self.getOntime(),
                      "profileCount": Profile.count(),
                      "profiles": [{"name": profile.name,
                                    "online": profile.online,
                                    "ontime": profile.getOntime(), "onsince": profile.connectTimestamp,
                                    "offtime": profile.getOfftime(), "offsince": profile.disconnectTimestamp,
                                    "totalPlaytime": profile.totalPlaytime + profile.getOntime()} for profile in self.profiles]}
        return data


    def OnConnect(self, profileName: str):
        for profile in self.profiles:
            if profile.name == profileName:
                profile.OnConnect()
                break
        
        Player.count += 1
        self.online = True
        self.connectTime = time.monotonic()
        self.connectTimestamp = time.time()     # Time in seconds since epoch (1970-01-01 00:00:00 UTC) (Unix time)

    def OnDisconnect(self, profileName: str):
        for profile in self.profiles:
            if profile.name == profileName:
                profile.OnDisconnect()
                break

        Player.count -= 1
        self.online = False
        self.disconnectTime = time.monotonic()
        self.disconnectTimestamp = time.time()      # Time in seconds since epoch (1970-01-01 00:00:00 UTC) (Unix time)
        self.totalPlaytime += self.getPlaytime()


# Path for saving Stats
statsFilePath: str = "/home/babo/.config/unity3d/IronGate/Valheim/stats.json"

# Json Tools
def readJson(path: str) -> json:
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("The file was not found!")
    except json.JSONDecodeError:
        print("Syntax error in json!")
def writeJson(path: str, data: json):
    try:
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
    except FileNotFoundError:
        print("The file was not found!")
    except json.JSONDecodeError:
        print("Syntax error in json!")

# ID Attribute Tools
def readOfItem(collection: json, IDname: str, ID: str, attribute: str) -> float:
    for item in collection:
        if item[IDname] == ID:
            itemFound = item
            break
    if attribute in itemFound:
        return itemFound[attribute]
    return 0.0
def writeToItem(collection: json, IDname: str, ID: str, attribute: str, value: float):
    if ID in collection:
        for item in collection:
            if item[IDname] == ID:
                item[attribute] = value
                break
    else:
        print("ID not found ( ID: " + ID + " )")

def getItemsFromData(itemType: str, data: json) -> list:
    items: list = []
    if itemType in data:
        for item in data[itemType]:
            items.append(item)
            break
    return []
    

# Load existing stats from file
data = readJson(statsFilePath)

# Server
    # Add when i have a Server class

# Players
playersJson = []
playersJson = getItemsFromData("players", data)

players = []
for player in playersJson:
    steamID = player["steamID"]
    profiles = []
    for profile in player["profiles"]:
        profiles.append(profile)
    online = player["online"]
    connectTime = player["ontime"]
    connectTimestamp = player["onsince"]
    disconnectTime = player["offtime"]
    disconnectTimestamp = player["offsince"]
    totalPlaytime = player["totalPlaytime"]

    p = Player(steamID, profiles, online, connectTime, connectTimestamp, disconnectTime, disconnectTimestamp, totalPlaytime)
    players.append(p)

    #Profiles
    for profile in profiles:
        name = profile["name"]
        online = profile["online"]
        connectTime = profile["ontime"]
        connectTimestamp = profile["onsince"]
        disconnectTime = profile["offtime"]
        disconnectTimestamp = profile["offsince"]
        totalPlaytime = profile["totalPlaytime"]

        pro = Profile(name, online, connectTime, connectTimestamp, disconnectTime, disconnectTimestamp, totalPlaytime)
        p.addProfile(pro)


dataServer: json                    # For later use in shutdown method # Refactor when adding server class


# Restful API Endpoints
app = Flask(__name__)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

@app.route('/', methods=['GET'])
def get_server_stats():
    dataServer = {"playerCount": Player.count(), "steamIDs": [player.steamID for player in Player.getAll()]}
    return dataServer

@app.route('/<steamID>', methods=['GET'])
def get_player_stats(steamID):
    for player in Player.getAll():
        if player.steamID == steamID:
            return player.pullRequest()
    return {"error": "Player not found"}


# Parse Thread
stop_event = Event()

def parse_loop():
    while not stop_event.is_set():      # Parsing and initializing Players off of it
        j = journal.Reader()
        j.this_boot()
        j.add_match(_SYSTEMD_UNIT="valheim-server.service")
        j.seek_tail()
        j.get_previous()

        # Controlling update frequency
        stop_event.wait(60)

parse_thread = Thread(target=parse_loop, daemon=False)
parse_thread.start()

# Graceful Shutdown Handler
def graceful_shutdown(signum, frame):
    print("StatsAPI: SIGTERM received, shutting down gracefully...")

    # Stop the parse thread
    stop_event.set()
    parse_thread.join()
    # pullRequest all for writing to Save File on shutdown
    get_server_stats()
    data = {"server": {dataServer}, "players": [player.pullRequest() for player in Player.getAll()]}
    writeJson(statsFilePath, data)

    print("StatusAPI: Shutdown complete.")
    exit(0)

signal.signal(signal.SIGTERM, graceful_shutdown)