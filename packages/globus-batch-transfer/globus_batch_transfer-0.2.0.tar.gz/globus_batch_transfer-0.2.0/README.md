# Globus Batch Transfer
### Requirements
  * Python >= 3.9
  * Poetry
### Install
    $ pip install globus-batch-transfer
    $ pip install --upgrade globus-batch-transfer
    $ pip uninstall globus-batch-transfer
### Install From Source
    1. $ git clone https://github.com/adnanzaih/globus-batch-transfer.git ; cd globus_batch_transfer/
    2. $ poetry install
### Build Wheel / Dist From Source
    1. $ git clone https://github.com/adnanzaih/globus-batch-transfer.git ; cd globus_batch_transfer/
    2. $ poetry build
### Execution
    1. $ poetry shell 
    1.2 Or activate virtual environment where globus_batch_transfer is installed.
    2. $ python -m globus_batch_transfer "/path/to/config.yaml/"
