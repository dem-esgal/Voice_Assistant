### Voice assistant with youtube music.
## Ukraine language with commands in russian
1) Включи
2) Пауза
3) Продолжить

## Model 
Download onnx model from Google Drive (https://drive.google.com/file/d/1gJD-8jLGdPDD7TJ4Kc48Uzvz8CEcw1n_/view?usp=sharing)
and vad.jit (https://drive.google.com/file/d/1Yxe__xuZa553ekIP9nygwCwMFhiSj09K/view?usp=sharing)
and put them to the src folder.
## Dependencies
$pip install pyaudio \
$pip install torchaudio \
$pip install onnxruntime \

You also need to install the audio file I/O backend: \
$pip install soundfile

$pip install yt-dlp \
$pip install youtube-search \
$pip install transliterate \
$pip install python-vlc \
for webm playing (or vlc)

### Many thanks to Silero (https://github.com/snakers4/silero-models)
#### Please take a look (https://github.com/snakers4/silero-models/blob/master/LICENSE) for the license 