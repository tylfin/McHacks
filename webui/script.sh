fluidsynth -F output.wav font.sf2 test.mid
lame --preset standard output.wav test.mp3
chmod 755 test.mp3
cd static
rm test.mp3
cd ../
mv test.mp3 static

