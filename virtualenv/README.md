# Virtualenv Install

## 1. Install python
```
brew install python2  # or python3 
```
## 2. Get get-pip.py
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```
## 3. Install pip
```
python get-pip.py
```
## 4. System-wide install
```
sudo pip install -U virtualenv
```
## 5. Create python virtual env
```
virtualenv --system-site-packages -p python3.6 ./venv
```
## 6. Activate or deactivate virtual env
```
source ./venv/bin/activate
deactivate
```
## 7. Show package installed within the virtual env
```
(venv) $ pip list
```
## 8. Install tensorflow
```
(venv) $ pip install --upgrade tensorflow
(venv) $ python -c "import tensorflow as tf"
```
## 9. Install jupyter
```
pip install jupyter
```
## 10. Config jupyter kernal with venv
```
python -m ipykernal install --user --name=venv
```
