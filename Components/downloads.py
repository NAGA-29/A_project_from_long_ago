import urllib.request, urllib.error

class downloads:

    # 画像の保存先
    IMG_DIR = './images/'
    # -------------------- メソッド -----------------------
    # 画像のダウンロード
    def download(self,image_url):
        url_orig = '%s:orig' % image_url
        path = self.IMG_DIR + image_url.split('/')[-1]
        try:
            response = urllib.request.urlopen(url=url_orig)
            with open(path, "wb") as f:
                f.write(response.read())
            print('Image Download OK ' + image_url)
        except Exception as e:
            self.error_catch(e)

    # 動画のダウンロード
    def downloadVideo(self,video_url):
        remake_name = video_url.split('/')[-1]
        path = self.IMG_DIR + remake_name.split('?')[0]
        try:
            response = urllib.request.urlopen(url=video_url)
            with open(path, "wb") as f:
                f.write(response.read())
            print('Video Download OK ' + video_url)
        except Exception as e:
            self.error_catch(e)

    def error_catch(error):
        """エラー処理
        """
        print("NG ", error)