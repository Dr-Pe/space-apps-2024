# Astronotes
This is our project for the challenge "Symphony of the Stars: Harmonizing the James Webb Space Telescope in Music and Images" from the NASA Space Apps 2024.\
Astronotes is a videogame that allows you, as an artist, to play music in a theremin-like musical instrument tuned to the images of the JWST. For each pixel in each image the game generates a note based on the frequency of the dominant wavelength of that point in space.

### What does it do?
It allows the user to make music by using their PC as a theremin-like musical instrument tuned to the pictures taken by the James Webb Space Telescope (JWST). When the user clicks a pixel of the image the game generates a musical note based on the colors of the picture.

### How does it work?
We have used Python 3 as a programming language and the Pygame library to create the game itself, including the GUI and the sounds played.\
On the other hand, we have used Numpy and Colour-Science in order to analyze the JWST images. For every pixel in the picture we have:
* Applied a function to calculate its Dominant Wavelength (between 400 nm and 700 nm).
* Calculated a frequency associated to this wavelength.
* Calculated a frequency based on sound speed instead of light speed.
* Mapped this frequency into one that we humans can hear (from 20 Hz to 20 kHz) but also enjoy (we choose 27 Hz to 4186 Hz, because it is the frequency range of a standard piano).

### What benefits does it have? What do we hope to achieve?
We hope to generate engagement in space exploration, inspire creativity and imagination. We believe that our game can do that because it presents an interactive experience not only based on the beautiful images by the JWST but also in a more immersive way thanks to the music.

## Usage
In order to use Astronotes you can install its requiriments using `pip install -r requiriments.txt` and then execute it:
```
python3 -m src/__init__.py
```
If you are a Windows user, you can also try downloading an executable from this link: https://drive.google.com/drive/folders/1Ty42a9cLEEBkBh2eYQQaX949OitECwKW?usp=sharing
