from PIL import Image
import cv2

class PhotoFabrication:
    # 画像の読込先
    LIVE_TMB_IMG_DIR = ''
    # トリミング済み画像の保存場所
    IMG_TRIM_DIR = ''
    '''
    Initial Setting
    '''
    def __init__(self,tmb_img_dir,img_trim_dir):
        # 画像の読込先
        self.LIVE_TMB_IMG_DIR = tmb_img_dir
        # トリミング済み画像の保存場所
        self.IMG_TRIM_DIR = img_trim_dir

    '''
    画像トリミング
    param img_url:画像url
    '''
    def imgTrim(self,img_url:str):
        img_name = img_url.split('/')[-2] + '.jpg'
        FILE_NAME = self.LIVE_TMB_IMG_DIR + img_name
        img = Image.open(FILE_NAME) #画像の読み込み
        img2 = img.crop(box=(0,45,480,315)) #画像の切り抜き
        img2.save(self.IMG_TRIM_DIR + img_name) #切り抜いた画像を保存


    def get_concat_v(self, oldImg, newImg):
        '''
        画像連結加工
        '''
        im1 = Image.open(oldImg)
        im2 = Image.open(newImg)
        dst = Image.new('RGB', (im1.width, im1.height + im2.height))
        dst.paste(im1, (0, 0))
        dst.paste(im2, (0, im1.height))
        return dst


    def imgTrim_Linking(self, top_path:str, bottom_path:str, save_path:str):
        '''
        画像トリミング & 画像連結
        param img_url:画像url
        '''
        # img_name = img_url.split('/')[-2] + '.jpg'
        # FILE_NAME = '../live_temporary_image/'+ img_name
        img = Image.open(top_path) #画像の読み込み
        top = img.crop(box=(0,45,480,315)) #画像の切り抜き

        bottom = Image.open(bottom_path)
        dst = Image.new('RGB', (top.width, top.height + bottom.height))
        dst.paste(bottom, (0, 0))
        dst.paste(top, (0, top.height))
        dst.save(save_path) #切り抜いた画像を保存
        img = cv2.imread(save_path)
        cv2.arrowedLine(img,
                        pt1=(240, 250), 
                        pt2=(240, 290), 
                        color=(255, 255, 0),
                        thickness=4,
                        line_type=cv2.LINE_4,
                        shift=0,
                        tipLength=0.5)
        cv2.imwrite(save_path, img)