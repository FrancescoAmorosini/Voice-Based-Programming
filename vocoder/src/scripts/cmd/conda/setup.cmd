conda update -y -n base -c defaults conda &&^
conda create -y --name dsd-env pyaudio &&^
conda install -y -n dsd-env -c conda-forge word2number &&^
conda activate dsd-env &&^
pip install wit