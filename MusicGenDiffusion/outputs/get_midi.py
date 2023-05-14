try:
    import pickle
    import pretty_midi
    from qt import quantize_times as qt
    def create_midi_file(data, output_file):
        # Create a PrettyMIDI object
        midi = pretty_midi.PrettyMIDI()

        guitar_program = pretty_midi.instrument_name_to_program('Acoustic Guitar (steel)') #'Acoustic Grand Piano' 'Acoustic Guitar (steel)'
        guitar = pretty_midi.Instrument(program=guitar_program)
        
        # Initialize the time
        current_time = 0.0

        # Initialize a list of currently playing notes
        current_notes = []
        for i in range(len(data)):
            
            semitone, octave, time = data[i]
            
            
            # Convert semitone and octave to MIDI note number
            note_number = (octave) * 12 + semitone
            
            #if octave < 4:
                #note_number += (4-octave)*12
                
            if time < 50:
                time = 0

            time /= 1000
            
            # If time is not zero, stop all currently playing notes
            
            # Create a Note instance for this note and add it to the current notes
            note = pretty_midi.Note(velocity=64, pitch=note_number, start=current_time, end = current_time+1)
            current_notes.append(note)
            current_time += time
            # Add it to our guitar instrument
            guitar.notes.append(note)

            # Update the current time
            

        # If there are any notes still playing at the end, stop them
        for note in current_notes:
            note.end = current_time

        # Add the guitar instrument to the PrettyMIDI object
        midi.instruments.append(guitar)

        # Write out the MIDI data
        midi.write(output_file)
        
    data = pickle.load(open("generated_sequence", "rb"))

    create_midi_file(data, 'output.mid')
except Exception as e:
    print(e)
    input()


