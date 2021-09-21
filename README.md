# KABLAM

_Turns whistling into MIDI_

## Installation

First, you'll want `pipenv` installed, which is outside the scope of this README. Please refer to [the pipenv documentation](https://pipenv.pypa.io/en/ latest/) for details on installing `pipenv` for your OS.

Once you have `pipenv` installed, run:

`$ pipenv install`

To install the dependencies needed (at the moment: scipy, numpy, and midiutils).

## Usage

Once you have dependencies installed, you can run the main script like so:

`$ pipenv run python main.py ~/test.wav`

This will run the script against the `test.wav` file, and it'll create a MIDI file called `out.midi` in the current working directory.

This MIDI file can be imported into any DAW, such as Logic Pro. With a bit of cleanup (mainly with regards to "noisy notes", notes that don't belong in the main output), you should have what amounts to a note-for-note transcription of what you whistled!

## Note

This is a highly experimental work in progress. You might have to adjust certain parameters to get it to work for you, and the result isn't going to be perfect. That said, it's a good approximation from the results I've seen so far.

## Future plans

The idea is to turn this into a mobile app, where I can whistle into my phone and it'll save it to shared storage. For now, though, I give you the script.

## License

Copyright 2021, Austin Pocus, under the MIT license. See LICENSE file for details.
