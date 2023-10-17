import os, json
encodeJSON = json.JSONEncoder().encode
decodeJSON = json.JSONDecoder().decode

class Paths:
    join          = os.path.join
    directoryName = os.path.dirname