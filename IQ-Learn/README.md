# IQ Learn

To train the relevant model just run the `iq_train.py` file with correctly chosen config file.

To train another expert, just take the baseline code from training folder and modify the script.

## Installing packages

Install `requirements.txt` or simply run the command to install the relevant fixed packages. The code should work for python>=3.8

```
pip install "gym[box2d]" git+https://github.com/carlosluis/stable-baselines3@fix_tests "gym[mujoco]"
```

## Extra

Saviour https://stackoverflow.com/questions/75421424/cant-install-stable-baselines3extra and GPT -> installs stable baselines for newer versions of Python and Mujoco.
