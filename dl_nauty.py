import os
import requests

# récupération du chemin de l'utilisateur
current_path = os.path.abspath("dl_nauty.py")
path_len = len(current_path)
len_to_delete = len("dl_nauty.py")
lib_path = current_path[:path_len-len_to_delete]

url = 'http://users.cecs.anu.edu.au/~bdm/nauty/nauty2_8_6.tar.gz'

# Le dataset ne sera téléchargé que si il n'a toujours pas
# encore été téléchargé
if not os.path.exists(os.path.join(lib_path, 'nauty2_8_6.tar.gz')):
    
    print('téléchargement de nauty')

    # récupération du .tar.gz
    r = requests.get(url)
    path_file = os.path.join(lib_path, 'nauty2_8_6.tar.gz')  
    with open(path_file, 'wb') as f:
        f.write(r.content)

    