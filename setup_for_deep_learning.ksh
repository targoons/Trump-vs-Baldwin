echo "----------------------------------"
echo ""
echo "      Install prerequisites     "
echo ""
echo "----------------------------------"

sudo apt update
sudo apt install python3-dev python3-pip
sudo apt install python3-dev python3-pip

echo "----------------------------------"
echo ""
echo "      Install Tensorflow     "
echo ""
echo "----------------------------------"

pip3 install --user --upgrade tensorflow-gpu  # install in $HOME

echo "----------------------------------"
echo ""
echo "  Add NVIDIA package repository   "
echo ""
echo "----------------------------------"

sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
sudo apt install ./cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64/nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb
sudo apt install ./nvidia-machine-learning-repo-ubuntu1604_1.0.0-1_amd64.deb
sudo apt update

echo "----------------------------------"
echo ""
echo "          Install CUDA            "
echo ""
echo "----------------------------------"

sudo apt install cuda9.0 cuda-cublas-9-0 cuda-cufft-9-0 cuda-curand-9-0 \
    cuda-cusolver-9-0 cuda-cusparse-9-0 libcudnn7=7.2.1.38-1+cuda9.0 \
    libnccl2=2.2.13-1+cuda9.0 cuda-command-line-tools-9-0


echo "----------------------------------"
echo ""
echo "     Install TensorRT runtime     "
echo ""
echo "----------------------------------"

sudo apt update
sudo apt install libnvinfer4=4.1.2-1+cuda9.0

echo "----------------------------------"
echo ""
echo "  Test Tensorflow installations   "
echo ""
echo "----------------------------------"

python3 -c "import tensorflow as tf; print(tf.__version__)"


echo "----------------------------------"
echo ""
echo "  Install Keras and OpenAI Gym   "
echo ""
echo "----------------------------------"

pip3 install keras
pip3 install gym
