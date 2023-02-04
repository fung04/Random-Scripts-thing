@ECHO OFF

:: check export folder is exist or not else create it
if not exist ".\export" mkdir ".\export"

:: input subtile type
SET /p stype="Enter subtile type: "

:: input subtitle track name
SET /p stname="Enter subtitle track name: "

:: location of the mkvmerger.exe file
SET MKV_MERGER_DIR=D:\Download\Compressed\mkvtoolnix\

:: location of the output mkv files
SET OUTPUT_DIR=.\export\

:: let INPUT_DIR be the current directory
SET INPUT_DIR=.\

:: loop through each mkv file in the input directory
FOR %%f IN (*.mkv) DO (
    
    :: merge the mkv file with subtitle and subtitle track name
	%MKV_MERGER_DIR%mkvmerge.exe -o "%OUTPUT_DIR%%%f" "%INPUT_DIR%%%f" --language 0:zh --track-name 0:"%stname%" "%INPUT_DIR%%%~nf.%stype%"
    	
)

:: move and replace all file in OUTPUT_DIR to INPUT_DIR
move /Y %OUTPUT_DIR%*.mkv %INPUT_DIR%

:: DELETE OUTPUT_DIR
rmdir /S /Q %OUTPUT_DIR%

PAUSE