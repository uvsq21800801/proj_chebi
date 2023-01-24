python3 Parsing.py
python3 database.py
python3 dl_nauty.py

tar xvzf nauty2_8_6.tar.gz
cd nauty2_8_6
./configure
make
cd ..

python3 interface_u.py

bash appel_sparce_c.sh