# dj-genre-analyzer

I first began working with my 'audioAnalyzer.py' file, in order to actually break down the user's
uploaded audio sources. 

It returns the BPM and the Key value for the sources in a dictionary format, with the BPM being 99% correct being off 
maybe by ~1 beat in certain cases, however the key value truly depending on the audio source itself and not what maybe 
google stated in some cases. 

I say this because I noticed when testing my function the song 'S&M by Rihanna' was returned to have a key value of 'G#',
however if you google this it states that it should be a 'D#' minor. 

It really depends on the user's audio source rather
what their/my search engine may say when it comes to mixin, as I retrieved this file in not the best 'quality saving' way.

I then engineered the 'GeminiClient' class found within 'gemini.py', in order to take the values we get from
'audioAnalyzer.py' to craft a prompt/response using the gen-ai API to further help our clients know more information on how
to properly mix their requested song.

I will now be working on the back/frontend using FlaskAPI to allow the user's to upload their audio via the browser.