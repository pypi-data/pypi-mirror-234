Create pypi package and upload:
1. python3 -m build
2. python3 -m twine upload --repository testpypi dist/* 


Production:
python3 -m twine upload dist/*
