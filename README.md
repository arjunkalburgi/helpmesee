# helpmesee
Blind glasses for nwHacks

Inspiration
The idea was to help people who are blind, to be able to discretely gather context during social interactions and general day-to-day activities

What it does
The glasses take a picture and analyze them using Microsoft, Google, and IBM Watson's Vision Recognition APIs and try to understand what is happening. They then form a sentence and let the user know. There's also a neural network at play that discerns between the two dens and can tell who is in the frame

How I built it
We took a RPi Camera and increased the length of the cable. We then made a hole in our lens of the glasses and fit it in there. We added a touch sensor to discretely control the camera as well.

Challenges I ran into
The biggest challenge we ran into was Natural Language Processing, as in trying to parse together a human-sounding sentence that describes the scene.

What I learned
I learnt a lot about the different vision APIs out there and creating/trainingyour own Neural Network.

What's next for Let Me See
We want to further improve our analysis and reduce our analyzing time.

https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/000/489/350/datas/gallery.jpg


To run:
```python
cd nwHacks
sudo su
export GOOGLE_APPLICATION_CREDENTIALS=apiKey.json
python ser.py
```
