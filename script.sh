python3 Parsing.py
python3 database.py
python3 dl_nauty.py

tar xvzf nauty2_8_6.tar.gz
cd nauty2_8_6
./configure
make
cd ..

gcc -o sparse_run Sparse.c nauty2_8_6/nausparse.h nauty2_8_6/nauty.a

python3 pyqt5_window.py
