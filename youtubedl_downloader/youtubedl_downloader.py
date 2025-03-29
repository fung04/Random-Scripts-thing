import os
import subprocess

def download_videos(input_file):
    """
    Read links from a text file and download videos as 16-bit FLAC
    
    Args:
        input_file (str): Path to the text file containing YouTube links
    """
    # Check if youtube-dl.exe exists
    if not os.path.exists('youtube-dl.exe'):
        print("Error: youtube-dl.exe not found in the current directory")
        return

    # Read links from the file
    try:
        with open(input_file, 'r') as file:
            links = file.read().splitlines()
    except FileNotFoundError:
        print(f"Error: File {input_file} not found")
        return
    except IOError:
        print(f"Error: Could not read file {input_file}")
        return

    # Download each link
    for link in links:
        if link.strip():  # Skip empty lines
            try:
                # Construct the youtube-dl command with 16-bit FLAC specification
                cmd = [
                    'youtube-dl.exe', 
                    '-x',  # extract audio
                    '-v',  # verbose 
                    '-k',  # keep video file
                    '--audio-format', 'aac',  # convert to FLAC
                    '--embed-thumbnail',
                    '--audio-quality', '0',  # highest quality
                    '--add-metadata',  # add metadata
                    '-f', 'bestaudio',  # best audio quality
                    '--user-agent', 'Mozilla/5.0 (Android 14; Mobile; rv:128.0) Gecko/128.0 Firefox/128.0',
                    link.strip()
                ]
                
                # Execute the command
                print(f"Downloading: {link}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                # Print output
                print(result.stdout)
                
                # Print any errors
                if result.stderr:
                    print("Errors:", result.stderr)
            
            except Exception as e:
                print(f"Error downloading {link}: {e}")

def main():
    # Specify the input file with links
    input_file = 'youtube_links.txt'
    download_videos(input_file)

if __name__ == '__main__':
    main()