/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew install cmake
brew install python3
brew install git
brew install gmp
brew install libsodium
git clone https://github.com/Chia-Network/bls-signatures.git
cd bls-signatures
git submodule update --init --recursive
mkdir build
cd build
cmake ../
cmake --build . -- -j 6
./src/runtest
./src/runbench
cd ..
pip3 install .
pip3 install ecdsa
