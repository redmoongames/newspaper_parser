import requests
import os
from pathlib import Path

def main():
    file_name = '/var/data/scans/public/6322AD5C-5547-45A2-B3D9-8AE9BDF672E0/0/441313_doc1.tiff_files'
    zoom = 13
    folder_name = 'red_star'
    
    create_directory(folder_name)
    output_file_path = get_directory_path(folder_name) + '/0_0.jpg'
    
    source_url = get_url(file_name, 0, 0, zoom)
    
    save_image(source_url, output_file_path)
    print('complete!')
    
    
def get_directory_path(name):
    file_path = os.path.realpath(__file__)
    directory_path = os.path.dirname(file_path)
    full_path = directory_path + '/' + str(name)
    return full_path


def create_directory(name):
    full_path = get_directory_path(name)
    Path(full_path).mkdir(parents=True, exist_ok=True)


def save_image(url, file_name):
    
    with open(file_name, 'wb') as handle:
        response = requests.get(url, stream=True)
        
        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)



def get_url(file_name, x_pos, y_pos, zoom = 13):
    
    base_url = 'http://content.prlib.ru/fcgi-bin/iipsrv.fcgi'
    image_name = str(x_pos) + '_' + str(y_pos) + '.jpg'
    url = base_url + '?DeepZoom=' + str(file_name) + '/' + str(zoom) + '/' + image_name
    return url




main()