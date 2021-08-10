import imagehash
import numpy
import shutil
from PIL import Image, ImageFilter
import os

from pprint import pprint

from pyasn1.type.univ import Boolean

class ImageProcessing: 
    # 画像の一時保存先
    _LIVE_TMB_TMP_DIR = ''
    # 画像の保存先
    _LIVE_TMB_IMG_DIR = ''
    _OTHER_TMB_TMP_DIR = './other_temporary_image/'

    _TMB_TMP_FilePath = ''
    _TMB_IMG_FilePath = ''
    _OTHER_TMP_FilePath = ''



    def __init__(self, file_path:str, TMP_DIR = './live_temporary_image/', IMG_DIR = './live_thumbnail_image/'):
        self._LIVE_TMB_TMP_DIR = TMP_DIR
        self._LIVE_TMB_IMG_DIR = IMG_DIR
        self._TMB_TMP_FilePath = self._LIVE_TMB_TMP_DIR + file_path.split('/')[-2] + '.jpg'
        self._TMB_IMG_FilePath = self._LIVE_TMB_IMG_DIR + file_path.split('/')[-2] + '.jpg'
        self._OTHER_TMP_FilePath = self._OTHER_TMB_TMP_DIR + file_path.split('/')[-2] + '.jpg'

    """
    画像比較メソッド
    @return result:Boolean
    """
    def imageComparison_hash(self) ->Boolean:
        try:
            # print(self._TMB_IMG_FilePath)
            # print(self._TMB_TMP_FilePath)
            hash_A = imagehash.average_hash(Image.open(self._TMB_IMG_FilePath))
            hash_B = imagehash.average_hash(Image.open(self._TMB_TMP_FilePath))
            num_difference = hash_A - hash_B
            # print(hash_A)
            # print(hash_B)
            
            if(num_difference == 0):
                result = True
            else:
                result = False
            return result
        except FileNotFoundError as e:
            pprint(e)
            print('アウチ')


    """
    画像比較メソッド
    @return result:Boolean
    """
    def imageComparison_hash_other(self) ->Boolean:
        try:
            hash_A = imagehash.average_hash(Image.open(self._TMB_IMG_FilePath))
            hash_B = imagehash.average_hash(Image.open(self._OTHER_TMP_FilePath))
            num_difference = hash_A - hash_B
            
            if(num_difference == 0):
                result = True
            else:
                result = False
            return result
        except FileNotFoundError as e:
            pprint(e)


    # def readImage():
    #     im1 = Image.open('./Trim_Images/IMG_6D3F3ABB2313-1.jpg')
    #     im2 = Image.open('./Trim_Images/VW6SVPIiIvU.jpg')

    # def get_concat_h(im1, im2):
    #     dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    #     dst.paste(im1, (0, 0))
    #     dst.paste(im2, (im1.width, 0))
    #     return dst

    # def get_concat_v(im1, im2):
    #     dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    #     dst.paste(im1, (0, 0))
    #     dst.paste(im2, (0, im1.height))
    #     return dst

    # # get_concat_h(im1, im2).save('renketu_test.jpg')
    # get_concat_v(im1, im2).save('renketu_test.jpg')



    # print(os.path.getsize('./dirA/El29sxsXYAMBOvJ.jpg'))

    # hash_1a = imagehash.average_hash(Image.open('./dirA/El29sxsXYAMBOvJ.jpg'))
    # hash_1p = imagehash.phash(Image.open('./dirA/El29sxsXYAMBOvJ.jpg'))
    # hash_1d = imagehash.dhash(Image.open('./dirA/El29sxsXYAMBOvJ.jpg'))
    # hash_1w = imagehash.whash(Image.open('./dirA/El29sxsXYAMBOvJ.jpg'))

    # hash_2a = imagehash.average_hash(Image.open('./dirB/El29sxsXYAMBOvJ.jpg'))
    # hash_2p = imagehash.phash(Image.open('./dirB/El29sxsXYAMBOvJ.jpg'))
    # hash_2d = imagehash.dhash(Image.open('./dirB/El29sxsXYAMBOvJ.jpg'))
    # hash_2w = imagehash.whash(Image.open('./dirB/El29sxsXYAMBOvJ.jpg'))

    # print('ahash : ', hash_2a - hash_1a)
    # print('phash : ', hash_2p-hash_1p)
    # print('dhash : ', hash_2d-hash_1d)
    # print('whash : ', hash_2w-hash_1w)

    # shutil.move('./dirA/El29sxsXYAMBOvJ.jpg', './dirB/')