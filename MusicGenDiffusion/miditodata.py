import os
import mido
import pickle
import guitarpro
from mido import tick2second
import os
import mido

import mido
import os

def midi_note_to_semitones_and_octaves(midi_note):
    semitones = midi_note % 12
    octaves = midi_note // 12
    return [semitones, octaves]

def parse_midi_files(directory):
    output = []

    # Iterate over all MIDI files in the directory
    for filename in os.listdir(directory):
        if not filename.endswith('.mid'):
            continue

        # Load the MIDI file
        mid = mido.MidiFile(os.path.join(directory, filename))

        # Default tempo (in microseconds per beat) and time signature
        tempo = 500000
        time_signature = (4, 4)  # 4/4 is a common time signature

        song = []

        # Iterate over all tracks in the MIDI file
        for i, track in enumerate(mid.tracks):
            beats = []
            elapsed_ticks = 0  # Total elapsed time in ticks
            name = ''

            # Iterate over all messages in the track
            for msg in track:
                elapsed_ticks += msg.time

                if msg.type == 'track_name':
                    name = msg.name.strip().lower()
                elif msg.type == 'set_tempo':
                    tempo = msg.tempo
                elif msg.type == 'time_signature':
                    time_signature = (msg.numerator, msg.denominator)
                elif msg.type == 'note_on' and msg.velocity > 0:
                    notes = midi_note_to_semitones_and_octaves(msg.note)
                    start = mido.tick2second(elapsed_ticks, mid.ticks_per_beat, tempo) * 1000  # Convert to milliseconds
                    beats.append({'notes': [notes], 'start': start, 'time_signature': time_signature})

            song.append({'file_name': str(filename[:-3]), 'track_name' : name,  'track_beats': beats})
        
        output.append(song)

    return output






try:

    
    def gather_track_info(src_folder):
        files = [f for f in os.listdir(src_folder) if f.endswith('.gp5')]
        songs_data = {}
        for file in files:
            try:
                song = guitarpro.parse(os.path.join(src_folder, file))
                artist = song.artist.lower().strip()
                songs_data[str(file[:-3])] = {"artist" : artist , "track_strings": [(len(track.strings) if track.strings is not None else 0)for track in song.tracks]}
                
            except Exception as e:
                print("can't read "+file+":",e)
                
        return songs_data
            
    # Call the function with your source and destination directories
    songs_tracks = parse_midi_files('./training_midi/') #RETURNS array of songs, one song is a list of dict[track_data, track_beats]
    songs_info = gather_track_info('./training_data/')
    
    
    print(len(songs_tracks), len(songs_info))
    out = []
    skipped = 0
    for i, song in enumerate(songs_tracks):
    
    
        for n, track in enumerate(song):
            try:
                song_info = songs_info[track['file_name']]
            except:
                skipped+=1
                continue
            song_artist = song_info['artist']
            tracks_num_strings = song_info['track_strings']

        
            track_name = track['track_name']
            track_beats = track['track_beats']
    
        
            try:
                if any(word in track_name for word in ['vocal', 'bass', 'orchestra', 'choir', 'key', 'drum', 'percussion']) or len(track_beats) < 128 or tracks_num_strings[n] not in range(6, 9):
                    continue
            except:
                continue
            
            if song_artist == 'wintersun / jari mäenpää':
                song_artist = 'wintersun'
            if song_artist == 'equipoise':
                song_artist = 'first fragment'
            if song_artist == 'immemorial':
                song_artist = ''

            if song_artist in ['dissection', 'dark funeral', 'emperor']:
                song_artist = "black"
            elif song_artist in ['spawn of possession', 'psycroptic', 'obscura', 'necrophagist', 'first fragment', 'beyond creation', 'revocation', 'archspire', 'inferi']:
                song_artist = "tech"
            else:
                song_artist = "other"
                
            out.append([song_artist, track_beats])

    pickle.dump(out, open("./preprocessed_data/data", 'wb'))
    print('success, skipped =',skipped)
    input()
            

    
except Exception as e:
    print(e)
    input()
