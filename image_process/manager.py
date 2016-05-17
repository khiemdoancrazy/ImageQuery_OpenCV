
import os
import imghdr
import cv2
from .image import Image
from .database import Database


class Manager:

    def __init__(self):
        self.__database = Database()
        self.__images = []
        self.__distances = []

    def load_image_folder(self, folder_path):
        self.__images = []
        for item in os.listdir(folder_path):
            file_path = os.path.join(folder_path, item)
            if imghdr.what(file_path) is not None:          # xác định xem file đầu vào có phải là file ảnh không
                image = Image()
                if len(item) < 7:
                    image.set_category('0')
                else:
                    image.set_category(item[0])
                image.read(file_path)
                self.__images.append(image)
                print('Cat: ', image.get_category(), ' - ', image.get_file_path())

    def set_database(self, path):
        self.__database.set_path(path)

    def save_database(self):
        self.__database.erase()
        self.__database.saves(self.__images)

    def load_database(self):
        self.__images = []
        self.__images = self.__database.loads()

    def query_image(self, file_path):
        if imghdr.what(file_path) is not None:          # xác định xem file đầu vào có phải là file ảnh không
            image = Image()
            image.read(file_path)
            self.__distances = []
            for img in self.__images:
                d = image.calc_distance(img, cv2.HISTCMP_CHISQR)
                self.__distances.append(d)

            # sắp xếp kết quả
            # cùng lúc sắp xếp 2 list __distances và images theo __distances
            combined = zip(self.__distances, self.__images)
            z = sorted(combined)
            self.__distances, self.__images = zip(*z)

            i = 0
            for d in self.__distances:
                print('khoang cach ', i, ': ', d, " - ", self.__images[i].get_file_path())
                i += 1

    def get_image(self):
        print('get image: ')

    def next_image(self):
        print('next image')

    def back_image(self):
        print('back image')
