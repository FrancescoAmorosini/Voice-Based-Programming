conda update -y -n base -c defaults conda &&^
conda create -y --name dsd-env pyaudio &&^
conda activate dsd-env &&^
conda install -y -n dsd-env -c conda-forge word2number pynput &&^
pip install wit