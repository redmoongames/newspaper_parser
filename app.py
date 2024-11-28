import threading
import time
import requests
import os
from pathlib import Path


def create_directory(directory_path) -> None:
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def make_max_length(number, max_length) -> str:
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


class ParsingStrategy:
    def get_download_link(self, archive_id: str, unit_number:int = 0) -> str:
        raise NotImplementedError()


class TwoAxisStrategy(ParsingStrategy):
    def __init__(self, zoom: int = 5):
        self.width = 1
        if zoom == 1:
            self.width = 1
        elif zoom == 2:
            self.width = 2
        elif zoom == 3:
            self.width = 4
        elif zoom == 4:
            self.width = 7
        elif zoom == 5:
            self.width = 10
        self.zoom = zoom
        self.base_url = 'https://content.prlib.ru/fcgi-bin/iipsrv.fcgi'


    def get_download_link(self, archive_id: str, unit_number:int = 0) -> str:
        if unit_number < 0:
            raise ValueError('width must be greater or equal than 0')
        y_position = unit_number // self.width
        x_position = unit_number % self.width
        full_name = str(x_position) + '_' + str(y_position) + '.jpg'
        url = self.base_url + '?DeepZoom=' + str(archive_id) + '/' + str(self.zoom + 8) + '/' + full_name
        print(url)
        return url


class OneLineStrategy(ParsingStrategy):
    def __init__(self, zoom=5):
        if zoom <= 0:
            raise ValueError('zoom must be greater than 0')
        self.zoom = zoom
        self.base_url = 'https://content.prlib.ru/fcgi-bin/iipsrv.fcgi'

    def get_download_link(self, archive_id: str, unit_number:int = 0) -> str:
        url = self.base_url + '?FIF=' + str(archive_id) + '&JTL=' + str(self.zoom) + ',' + str(unit_number) + '&CVT=JPEG'
        return url


class DownloadLinkParser:
    def __init__(self, strategy: ParsingStrategy) -> None:
        self.strategy = strategy

    def get_download_link(self, archive_id: str, unit_number: int) -> str:
        return self.strategy.get_download_link(archive_id, unit_number)


def save_image(source_url, output_file_path) -> None:
    response = requests.get(source_url, stream=True)
    if not response.ok:
        raise ConnectionError(str(response))
    with open(output_file_path, 'wb') as handle:
        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)


def download_newspaper_unit(download_link: str, file_name: str, output_folder) -> None:
    create_directory(output_folder)
    output_file = os.path.join(output_folder, file_name)
    if not os.path.isfile(output_file):
        try:
            save_image(download_link, output_file)
        except Exception as e:
            print('DOWNLOAD FAIL: ' + download_link + '\nERROR: ' + str(e))


def download_newspaper(link_parser: DownloadLinkParser, archive_id:str, output_folder: str, max_image_units: int = 250) -> None:
    for i in range(max_image_units):
        download_link = link_parser.get_download_link(archive_id, i)
        file_name = str(make_max_length(i, 4)) + '.jpg'
        threading.Thread(target=download_newspaper_unit, args=(download_link, file_name, output_folder), daemon=False).start()


def download_red_star(output_folder: str, zoom: int) -> None:
    all_archive_id = []
    all_archive_id.append(('/var/data/scans/public/8289540E-9AA0-47DB-A58B-4E36DD677695/0/441302_doc1.tiff', '1'))
    all_archive_id.append(('/var/data/scans/public/8289540E-9AA0-47DB-A58B-4E36DD677695/0/441303_doc1.tiff', '2'))
    all_archive_id.append(('/var/data/scans/public/8289540E-9AA0-47DB-A58B-4E36DD677695/0/441304_doc1.tiff', '3'))
    all_archive_id.append(('/var/data/scans/public/8289540E-9AA0-47DB-A58B-4E36DD677695/0/441305_doc1.tiff', '4'))
    max_image_units = 250
    parse_strategy = OneLineStrategy(zoom)
    link_parser = DownloadLinkParser(parse_strategy)
    for archive_pair in all_archive_id:
        archive_id = archive_pair[0]
        page_number = archive_pair[1]
        download_newspaper(link_parser, archive_id, output_folder + '/' + page_number, max_image_units)


def download_komsomol_pravda_13(output_folder: str, zoom: int) -> None:
    all_archive_id = []
    'https://content.prlib.ru/fcgi-bin/iipsrv.fcgi?DeepZoom=/var/data/scans/public/6322AD5C-5547-45A2-B3D9-8AE9BDF672E0/0/441313_doc1.tiff_files/13/1_0.jpg'
    all_archive_id.append(('/var/data/scans/public/6322AD5C-5547-45A2-B3D9-8AE9BDF672E0/0/441313_doc1.tiff_files', '1'))
    all_archive_id.append(('/var/data/scans/public/6322AD5C-5547-45A2-B3D9-8AE9BDF672E0/0/441314_doc1.tiff_files', '2'))
    all_archive_id.append(('/var/data/scans/public/6322AD5C-5547-45A2-B3D9-8AE9BDF672E0/0/441315_doc1.tiff_files', '3'))
    all_archive_id.append(('/var/data/scans/public/6322AD5C-5547-45A2-B3D9-8AE9BDF672E0/0/441316_doc1.tiff_files', '4'))
    max_image_units = 300

    parse_strategy = TwoAxisStrategy(zoom)

    link_parser = DownloadLinkParser(parse_strategy)
    for archive_pair in all_archive_id:
        archive_id = archive_pair[0]
        page_number = archive_pair[1]
        download_newspaper(link_parser, archive_id, output_folder + '/' + page_number, max_image_units)


def download_komsomol_pravda_15(output_folder: str, zoom: int) -> None:
    all_archive_id = []
    all_archive_id.append(('/var/data/scans/public/279A411B-D05E-4EE6-A9B4-F06E9B547435/0/444878_doc1.tiff_files', '1'))
    all_archive_id.append(('/var/data/scans/public/279A411B-D05E-4EE6-A9B4-F06E9B547435/0/444879_doc1.tiff_files', '2'))
    all_archive_id.append(('/var/data/scans/public/279A411B-D05E-4EE6-A9B4-F06E9B547435/0/444880_doc1.tiff_files', '3'))
    all_archive_id.append(('/var/data/scans/public/279A411B-D05E-4EE6-A9B4-F06E9B547435/0/444881_doc1.tiff_files', '4'))
    all_archive_id.append(('/var/data/scans/public/279A411B-D05E-4EE6-A9B4-F06E9B547435/0/444882_doc1.tiff_files', '5'))
    all_archive_id.append(('/var/data/scans/public/279A411B-D05E-4EE6-A9B4-F06E9B547435/0/444883_doc1.tiff_files', '6'))
    max_image_units = 300

    parse_strategy = TwoAxisStrategy(zoom)

    link_parser = DownloadLinkParser(parse_strategy)
    for archive_pair in all_archive_id:
        archive_id = archive_pair[0]
        page_number = archive_pair[1]
        download_newspaper(link_parser, archive_id, output_folder + '/' + page_number, max_image_units)


def main() -> None:
    download_komsomol_pravda_15('/Users/saha1506/Desktop/komsomol_pravda_15/zoom_4', 4)
    # download_red_star('/Users/saha1506/Desktop/red_star/zoom_5', 5)


if __name__ == '__main__':
    main()

