# pitch bending is NOT supported
import re
from midiutil import MIDIFile
from word_dict import word_dict
import zipfile
import json
# path = input("[INPP] path: ")
# path = "./1.vpr"


def convert(path, export_lyric=True):
    ZIP = zipfile.ZipFile(path, "r")

    print("[INFO] files found:")
    print("[INFO] {}".format(ZIP.namelist()))

    print("[INFO] files info:")
    for i in ZIP.infolist():
        print("[INFO] {} real size: {} zip size: {}".format(i.filename, i.file_size, i.compress_size))

    print("[INFO] openning Project/sequence.json ...")
    vpr = json.loads(ZIP.open("Project/sequence.json").read())

    TEMPO = vpr["masterTrack"]["tempo"]["events"]
    print("[INFO] tempo: ")
    for i in TEMPO:
        print("[INFO] {}".format(i))

    TRACKTYPES = [int(i["type"]) for i in vpr["tracks"]]
    print("[INFO] tracktypes: {}".format(TRACKTYPES))

    TRACKS = len(TRACKTYPES) - sum(TRACKTYPES)
    print("[INFO] convertable tracks: {}".format(TRACKS))

    mf = MIDIFile(TRACKS, removeDuplicates=False)

    offset = 0
    tracknum = 0

    for track in vpr["tracks"]:
        if (track["type"] == 1):
            offset += 1
            continue
        time = 0
        mf.addTrackName(tracknum, time, track["name"])
        for tempo in TEMPO:
            mf.addTempo(tracknum, tempo["pos"] / 480, tempo["value"] / 100)
        try:
            for part in track["parts"]:
                try:
                    for note in part["notes"]:

                        mf.addNote(tracknum, 0, note["number"], (note["pos"] + part["pos"]) / 480,
                                   note["duration"] / 480,
                                   note["velocity"])
                        if export_lyric:
                            lyc = note['lyric']
                            if re.fullmatch('[a-zA-Z-]+', lyc) and note['lyric'] in word_dict:
                                lyc = word_dict[note['lyric']]
                            # print(lyc)
                            mf.addLyric(tracknum, (note["pos"] + part["pos"]) / 480, lyc)
                except KeyError:
                    # print(
                    #     "[WARN] part {}, in track {}, does not have \"notes\" key".format(part["name"], track["name"]))
                    return False, "[WARN] part {}, in track {}, does not have \"notes\" key".format(part["name"],
                                                                                                    track["name"])
        except KeyError:
            # print("[WARN] track {} does not have \"parts\" key".format(track["name"]))
            return False, "[WARN] track {} does not have \"parts\" key".format(track["name"])
        tracknum += 1

    with open(path + ".mid", 'wb') as outf:
        mf.writeFile(outf)

    ZIP.close()

    print("[INFO] finished export")
    return True, path + ".mid"
