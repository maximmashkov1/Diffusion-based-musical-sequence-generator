import os
import mido
import pickle
import guitarpro
from mido import tick2second
import os
import mido

def midi_to_array(src_folder):
    files = [f for f in os.listdir(src_folder) if f.endswith('.mid') or f.endswith('.midi')]
    songs_data = []
    
    for file in files:
        mid = mido.MidiFile(os.path.join(src_folder, file))
        tracks = []
        
        for i, track in enumerate(mid.tracks):
            last_msg_time = 0
            current_tempo = 500000  # MIDI default tempo in microseconds per beat
            track_name = ""
            track_beats = []
            song_artist = ""
            beat_data = {'start': 0, 'notes': []}
            accumulated_ticks = 0

            for j, msg in enumerate(track):

                if not msg.is_meta:
                    accumulated_ticks += msg.time

                if msg.type == 'set_tempo':
                    current_tempo = msg.tempo

                if msg.type == 'track_name':
                    track_name = msg.name.strip().lower()

                if msg.type == 'note_on':
                    elapsed_time = mido.tick2second(accumulated_ticks, mid.ticks_per_beat, current_tempo)
                    delta_time = elapsed_time - last_msg_time
                    last_msg_time = elapsed_time
                    if delta_time > 0:  # If a new beat has started
                        if beat_data['notes']:  # Only append if notes are not empty
                            track_beats.append(beat_data)
                        beat_data = {'start': elapsed_time * 1000, 'notes': []}  # Start a new beat

                    beat_data['notes'].append([msg.note % 12, msg.note // 12])

            if beat_data['notes']:  # Append the last beat if it's not empty
                track_beats.append(beat_data)

            track_data = {'file_name': str(file[:-3]), 'track_name': track_name, 'track_beats': track_beats}
            tracks.append(track_data)

        songs_data.append(tracks)
            
    return songs_data



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
    songs_tracks = midi_to_array('./training_midi/') #RETURNS array of songs, one song is a list of dict[track_data, track_beats]
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
                
            out.append([song_artist, track_beats])

    pickle.dump(out, open("./preprocessed_data/data", 'wb'))
    print('success, skipped =',skipped)
    input()
            

    
except Exception as e:
    print(e)
    input()
