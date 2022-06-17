import os
import gc
import numpy as np
from PIL import Image
import librosa
import noisereduce as nr
#import matplotlib.pyplot as plt

#def graph_spectrogram(data, file_path):
    #fig,ax=plt.subplots(1)
    #fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    #librosa.display.specshow(data)
    #fig.savefig(file_path, dpi=300, frameon='false')
    #plt.close(fig)

def graph_linear_spectrogram_as_mono_channel(chunk, file_path):
    D = librosa.stft(chunk)  # STFT of chunk
    data = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    im = Image.fromarray(data.astype(np.uint8))
    im = im.resize((1024, 1024))
    im.save(file_path)


def graph_mel_spectrogram_as_mono_channel(y, sr, n_mels, file_path):
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels)
    data = librosa.power_to_db(S, ref=np.max)
    im = Image.fromarray(data.astype(np.uint8))
    im = im.resize((1024, 1024))
    im.save(file_path)



def get_spectrograms_from_file(input_path, output_path, window, overlap, noise_red):
    start_time=0.0
    filename=os.path.splitext(input_path)[0]
    assert overlap < window
    print('Loading audio file ...')
    y, sr = librosa.load(input_path)
    print('DONE!')
    if noise_red:
        print('Reducing noise ...')
        y = nr.reduce_noise(y=y, sr=sr)
        print('DONE!')

    duration = librosa.get_duration(y=y, sr=sr)
    start_times=[]
    chunk_number=0
    while start_time+window < duration:
        if chunk_number == 0:
            print('Generating Images ...')

        if chunk_number%100==0:
            print(chunk_number, ' processed images.')
            gc.collect()

        start = int(start_time*sr)
        win = int(window*sr)
        chunk = y[start:start+win]
        complete_output_path=os.path.join(output_path,filename+'_'+str(chunk_number)+'.jpg')
        if not os.path.exists(complete_output_path):
            #graph_linear_spectrogram_as_mono_channel(chunk, complete_output_path)
            graph_mel_spectrogram_as_mono_channel(chunk, sr, 128, complete_output_path)

        start_times.append(start_time)
        chunk_number = chunk_number + 1
        start_time=start_time+(window-overlap)

    if chunk_number > 0:
        print('DONE!')

    print('Saving time registry of spectrograms ...')
    start_times=np.array(start_times)
    np.save(os.path.join(output_path,filename+'_Start_time_marks'),start_times)
    print('DONE!')







def get_spectrograms_from_directory(window, overlap, in_dir, out_dir=None, filetype='wav', noise_red=True):
    # if out_dir is None, just save the spectrograms in the same folder as the input
    if out_dir==None:
        out_dir=in_dir

    # iterate over files in in_dir
    for filename in os.listdir(in_dir):
        f = os.path.join(in_dir, filename)

        # checking if it is a file
        if os.path.isfile(f):
            if f.endswith('.' + filetype):
                get_spectrograms_from_file(f, out_dir, window, overlap, noise_red=noise_red)
