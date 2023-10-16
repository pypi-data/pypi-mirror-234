cd tests
python3 test_database.py
cd ..
rm -rf dist/*
python3 -m build
python3 -m twine upload dist/*
