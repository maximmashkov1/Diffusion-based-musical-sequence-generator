Project info:

This generates musical sequences of stacked note embeddings which are then converted to midi files
Training data extracted from on gp5/midi files from songsterr.com
Supports conditioning on style (tech, black, other)
The model was trained to predict the temporal difference between notes too, but currently the rusults with this feature aren't satisfying, so the example sequences all use fixed times

![Diffusion process](/MusicGenDiffusion/Example%20outputs/diffusion.png)

To test:
1-Unpack model weights (in modeldata)
2-Run notebook cells until the output save, commenting the dataset creation, the band names can be found in model.encoding.bands_list
3-Run get_midi.py file in the outputs, you now have a generated midi file

To train:
The miditodata.py converts midi files to data that can be loaded for training. 

Converitng gp5 to midi requires MuseScore3. This is done by the bat file, modify paths to folders in .bat.
