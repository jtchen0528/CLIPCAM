# CLIPCAM

## pyenv install
```
sudo apt install libssl-dev libbz2-dev libreadline-dev libsqlite3-dev
git clone  https://github.com/pyenv/pyenv.git ~/.pyenv
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
pyenv install 3.7.13
pyenv virtualenv 3.7.13 clipcam-app
```

## .bashrc 
```
if shopt -q login_shell; then
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
 eval "$(pyenv init --path)"
fi
if command -v pyenv >/dev/null; then eval "$(pyenv init -)"; fi
eval "$(pyenv virtualenv-init -)"
```

## .profile
```
if [ -z "$BASH_VERSION" ]; then
  export PYENV_ROOT="$HOME/.pyenv"
  export PATH="$PYENV_ROOT/bin:$PATH"
  eval "$(pyenv init --path)"
fi
```

## Install pytorch on Raspberry Pi
```bash
wget https://github.com/KumaTea/pytorch-aarch64/releases/download/v1.9.0/torch-1.9.0-cp37-cp37m-linux_aarch64.whl
wget https://github.com/KumaTea/pytorch-aarch64/releases/download/v1.9.0/torchvision-0.10.0-cp37-cp37m-linux_aarch64.whl
pip install --force-reinstall torchvision-0.10.0-cp37-cp37m-linux_aarch64.whl
pip install --force-reinstall torch-1.9.0-cp37-cp37m-linux_aarch64.whl
```

## gunicorn activate
```
gunicorn flask_app:app -b 0.0.0.0:5002 -w 3 --timeout 300
```

