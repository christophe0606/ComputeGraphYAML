ECHO OFF

ECHO "A"
python exportyaml.py a
dot -Tpng -o ga\test.png ga\test.dot

ECHO "B"
python exportyaml.py b
dot -Tpng -o gb\test.png gb\test.dot

ECHO "C"
python exportyaml.py c
dot -Tpng -o gctest\test.png gctest\test.dot

ECHO "D"
python exportyaml.py d
dot -Tpng -o gd\test.png gd\test.dot

ECHO "E"
python exportyaml.py e
dot -Tpng -o ge\test.png ge\test.dot

ECHO "F"
python exportyaml.py f
dot -Tpng -o gf\test.png gf\test.dot

ECHO "G"
python exportyaml.py g
dot -Tpng -o gg\test.png gg\test.dot

ECHO "H"
python exportyaml.py h
dot -Tpng -o gh\test.png gh\test.dot

ECHO "I"
python exportyaml.py i
dot -Tpng -o gi\test.png gi\test.dot

ECHO "J"
python exportyaml.py j
dot -Tpng -o gj\test.png gj\test.dot

ECHO "K"
python exportyaml.py k
dot -Tpng -o gk\test.png gk\test.dot

ECHO "L"
python exportyaml.py l
dot -Tpng -o gl\test.png gl\test.dot

ECHO "M"
python exportyaml.py m
dot -Tpng -o gm\test.png gm\test.dot


