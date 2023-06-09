**Project info:**

This generates musical sequences of stacked note embeddings which are then converted to midi files.
Not all the melodies are actually good but most of them are enjoyable. Example outputs can be found in the identically titled folder.
Training data extracted from on gp5/midi files from songsterr.com
Supports conditioning on style (tech, black, other).
The model was trained to predict the temporal difference between notes too, but currently the results with this feature aren't satisfying, so the example sequences all use fixed times but it still forms chords.

**Detailed model describtion:**

Because I was quite selective when manually downloading training songs (as songsterr.com lacks an API), my training dataset comprised only about 80k sequences. Due to scarce data, I aimed to keep the model size small.
A Unet-like architecture with 4 consecutive MHSA layers in the bottleneck. Unlike in image data diffusion, the attention is calculated between sequence elements concatenated along all channels, instead of individual values. 
The diffusion process works in windows of 64 notes, but coherent sequences of any length can be generated by re-feeding n last notes and do a kind of inpainting. The generate function handles it.

![Diffusion process](/MusicGenDiffusion/Example_outputs/diffusion.png)

**To test:**
1-Unpack model weights (in modeldata)

2-Run notebook cells until the output save, commenting the dataset creation. The generate function:
'black' tends to generate more melodic sequences, so I'd stick with it.
The "number" argument is the number of sequences the diffusion process generates, which when joined form a consistent melody. The resulting length also depends on the next argument:
The "context" argument refers to how many notes from the generated sequence are used to give context to the generation of the continuation of the melody. For example, a context of 20 and number = 3 will give 64 + (64-20)*2 long sequence.

3-Run get_midi.py file in the outputs, you now have a generated midi file

**To train:**
The miditodata.py converts midi files to data that can be loaded for training. 

Converitng gp5 to midi requires MuseScore3. This is done by the bat file, modify paths to folders in .bat.
