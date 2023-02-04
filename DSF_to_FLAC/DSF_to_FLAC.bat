@ECHO OFF

set /p bit_depth="Enter bit depth(16/32): "
set /p sample_rate="Enter sample rate(44100/48000/96000): "

md export
forfiles /M *.dsf /C "cmd /c ffmpeg -i @file -af lowpass=24000,volume=6dB -sample_fmt s%bit_depth% -ar %sample_rate% ./export/@FNAME.flac || echo fail"  


PAUSE