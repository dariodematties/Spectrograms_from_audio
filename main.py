import argparse
from graph_spectrogram import get_spectrograms_from_directory

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--i', default='audio', help='Path to input file or directory.')
    parser.add_argument('--o', default='', help='Path to output directory. If not specified, the input directory will be used.')
    parser.add_argument('--filetype', default='wav', help='Filetype of sound recordings. Defaults to \'wav\'.')
    parser.add_argument('--results', default='raven', help='Output format of analysis results. Values in [\'audacity\', \'raven\']. Defaults to \'raven\'.')
    parser.add_argument('--window', type=float, default=3.0, help='Window duration in seconds of extracted spectrograms.')
    parser.add_argument('--overlap', type=float, default=0.0, help='Overlap in seconds between extracted spectrograms.')
    parser.add_argument('--noise_red', default=True, type=bool,help='Whether or not to apply noise reduction. Defaults to \'False\'.')
    args = parser.parse_args()

    get_spectrograms_from_directory(args.window, args.overlap, args.i, args.o, args.filetype, args.noise_red)

if __name__ == '__main__':

    main()
