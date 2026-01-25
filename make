export APP_ENV=test

python setup.py clean --all
python setup.py bdist_wheel
python setup.py clean --all
