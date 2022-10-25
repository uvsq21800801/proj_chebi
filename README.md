# proj_chebi

# test_libchebi.py:
This file shows basic usage of libchebi. the comments on it are self explanatory.
To install libcheby
```
pip install libChEBIpy
```

# extract_to_db.py:
Take ChEBI_lite_3star.sdf and parse it information using [parsing not coded yet], then send every entity into a local database so it can be accessed easily.

Can be modified to Asks for the name of the .sdf to create the db.

Run to unpack the zip file
```
gzip -d ChEBI_lite_3star.sdf.gz
```