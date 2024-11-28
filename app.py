import requests
import os
from pathlib import Path


def main():

    all_archive_id = []
    all_archive_id.append('/var/data/scans/public/8289540E-9AA0-47DB-A58B-4E36DD677695/0/441302_doc1.tiff')
    all_archive_id.append('/var/data/scans/public/8289540E-9AA0-47DB-A58B-4E36DD677695/0/441303_doc1.tiff')
    all_archive_id.append('/var/data/scans/public/8289540E-9AA0-47DB-A58B-4E36DD677695/0/441304_doc1.tiff')
    all_archive_id.append('/var/data/scans/public/8289540E-9AA0-47DB-A58B-4E36DD677695/0/441305_doc1.tiff')

    newspaper_name = 'red_star'
    current_directory = os.path.dirname(os.path.realpath(__file__))
    output_folder = os.path.join(current_directory, newspaper_name)

    max_image_units = 250

    zoom = 5

    download_newspaper(all_archive_id, output_folder, max_image_units, zoom)

def download_newspaper(all_archive_id, output_folder, max_image_units, zoom):

    page_index = 0

    for archive_id in all_archive_id:

        print('Downloading ' + archive_id + '...')

        page_output_folder = os.path.join(output_folder, str(page_index))
        download_page(archive_id, page_output_folder, max_image_units, zoom)
        page_index += 1


def download_page(archive_id, output_folder, max_image_units, zoom=5):

    for i in range(max_image_units):

        create_directory(output_folder)

        file_name = str(make_max_length(i, 4)) + '.jpg'
        output_file = os.path.join(output_folder, file_name)

        if not os.path.isfile(output_file):
            try:
                source_url = get_url(archive_id, i, zoom)
                print('LOADING: ' + source_url)
                save_image(source_url, output_file)
                print('COMPLETE!')
            except Exception as e:
                print('ERROR: ' + str(e))



def create_directory(directory_path):
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def save_image(source_url, output_file_path):

    response = requests.get(source_url, stream=True)

    if not response.ok:
        raise ConnectionError(str(response))

    with open(output_file_path, 'wb') as handle:
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)


def get_url(file_name, image_unit, zoom = 13):
    
    base_url = 'https://content.prlib.ru/fcgi-bin/iipsrv.fcgi'
    url = base_url + '?FIF=' + str(file_name) + '&JTL=' + str(zoom) + ',' + str(image_unit) + '&CVT=JPEG'
    return url


def make_max_length(number, max_length):
    max_number = pow(10, max_length)
    if number > max_number:
        print('ERROR: ' + str(number) + ' is too big. Max number is ' + str(max_number))
        raise ValueError('number must be less than the maximum length')
    return_value = ''
    current_length = len(str(number))
    for i in range(max_length - current_length):
        return_value += '0'
    return_value += str(number)

    return return_value


if __name__ == '__main__':
    main()