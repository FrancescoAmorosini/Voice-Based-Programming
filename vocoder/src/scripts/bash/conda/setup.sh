conda create -y --name dsd-env pyaudio &&\
conda install -y -n dsd-env -c conda-forge word2number &&\
eval "$(conda shell.bash hook)" &&\
conda activate dsd-env &&\
pip install wit