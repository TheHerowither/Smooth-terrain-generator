# Smooth-terrain-generator



A smooth terrain generator created in python
I made this for fun, after i had made a minecraft style terrain generator also based on perlin noise.


# How to use

Once you start the program it will ask for the folloing inputs:

You can leave them empty for them to use standard values.

Seed: Decides the random seed used for the noise map, standard: random value.

Level of Detail (LoD): This decides how many noise maps will be layered on top of each other, standard: 3.

Octaves: This decides what octave level the first map will have, and how much it will increase for each map, standard: 2.

Skip value: This decides how many values in the array that will be skipped for each verticie (Helps if its a highly detailed map), standard: 1.

Noise multiplier: This decides how much the noise will be multiplied, can be a range from 0 to 255 (In my expirience its best at 100), standard: 255.
