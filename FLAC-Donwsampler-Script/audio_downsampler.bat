@ECHO OFF

set /p bit_depth="Enter bit depth(16/32): "
set /p sample_rate="Enter sample rate(44100/48000/96000): "

md export
forfiles /M *.flac /C "cmd /c ffmpeg -i @file -af aresample=out_sample_fmt=s%bit_depth%:out_sample_rate=%sample_rate% ./export/@file || echo fail"


PAUSE