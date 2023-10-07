import os
import sys
import re
from pathlib import Path
import shutil




search_folder_files = {'archives': ('ZIP', 'GZ', 'TAR'),
                         'video':('AVI', 'MP4', 'MOV', 'MKV'),
                           'audio': ('MP3', 'OGG', 'WAV', 'AMR'),
                             'documents':('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'),
                               'images':('JPEG', 'PNG', 'JPG', 'SVG')}

search_files = {'archives': [],
                   'video':[],
                      'audio': [],
                         'documents':[],
                            'images':[],
                               'unknown':[]}
extension_files = set()
unknow_ext_files = set()

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
TRANS = {}

for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()




def parse_folder(path, level = 1):   # обхід папок через модуль pathlib
    path = normalize(path, True)
    p = Path(path)
    movin_files(p)
        
    
    for f in p.iterdir():
        
        if f.is_dir() and  f.name not in search_files.keys():
            parse_folder((path +'\\'+ f.name), level+1)
                
def movin_files (folder_n):
    for f in folder_n.iterdir():
        if f.is_file():
            
            mov_fil = select_folder(f.name)
            
            f_name =  normalize(f.name)
           
            new_way = search_path + '\\' + str(mov_fil) + '\\' + f_name
            
            if mov_fil:
                if mov_fil != 'archives':
                      shutil.move(f, new_way) 
                else:
                    shutil.unpack_archive(f, new_way.rsplit('.')[-2])
                    Path(f).unlink()



 
def normalize(file_nam, fold = False):
    
    if fold:
        fold_name = file_nam.rsplit('\\', 1)[-1]
         
        fold_name = fold_name.translate(TRANS)
        fold_name = fold_name.replace(' ', '_')
        fold_name = re.sub(r"\W+", r'_', fold_name) 
        new_fold_name = file_nam.rsplit('\\', 1)[-2] + '\\' + fold_name 
        if file_nam == new_fold_name:
            return file_nam
        else:
             os.rename(file_nam, new_fold_name)
             return new_fold_name
         
    file_transl = file_nam.translate(TRANS)

    file_transl = file_transl.replace(' ', '_')
    
    fil_name = re.sub(r"\W+", r'_', file_transl[:file_transl.rfind('.')]) + '.' +  file_transl[file_transl.rfind('.')+1:]
    
    return fil_name


def select_folder(file_name):
    file_type = file_name.rsplit('.')[-1]
     
    for key,value  in search_folder_files.items():
         
        if re.search(file_type, str(value), flags  = re.IGNORECASE):
            search_files[key].append(file_name)
            extension_files.add(file_type)
            return key 
    unknow_ext_files.add(file_type)
    search_files['unknown'].append(file_name) 
    return 'unknown'

def del_empty_fold(path):
    for f in os.listdir(path):
        fo_n = os.path.join(path, f)
        if os.path.isdir(fo_n) and  f not in search_files.keys():
             del_empty_fold(fo_n)
             if not os.listdir(fo_n):
                 os.rmdir(fo_n)
             
def start ():
    global search_path
    try:
     
        search_path = sys.argv[1]
                    
        if os.path.exists(search_path):
        
            search_path = normalize(search_path, True)
                                    
            for key in search_files:
                if  os.path.isdir(search_path + '\\' + key):
                    continue
                else:
                    os.mkdir(search_path+'\\'+ key)
                    
                    
            parse_folder(search_path)

            del_empty_fold(search_path)

            print('Списки знайдених  файлів :', '\n') 
            
            for value in search_files.items():
                print (value)


            print ('Include extension : ', extension_files)
            print ('Unknown extension : ', unknow_ext_files)
            return
        else:
            print ('Incorrect Path > try again ')  
            return
        
    except:
        print ('Incorrect Path > try again ')
    
        
           






if __name__ == '__main__':
    
    start()
   