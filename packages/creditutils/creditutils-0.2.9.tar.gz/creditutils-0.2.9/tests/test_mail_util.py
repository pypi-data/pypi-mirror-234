import unittest
import os
import tempfile
import shutil
from PIL import Image
import creditutils.img_util as img_util
import creditutils.file_util as file_util
from creditutils.mail_util import SenderLabel, SenderProcess


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass

# 生成图片列表
def get_img_list(img_dir, cnt=2):
    text_format = '测试图片0{}'
    file_path_format = 'img_0{}.png'

    imgs = list()
    butt = cnt + 1
    for index in range(1, butt):
        dst_path = os.path.join(img_dir, file_path_format.format(index))
        text = text_format.format(index)
        src_w = 720
        src_h = 1280
        img = Image.new('RGBA', (src_w, src_h))
        w = 400
        h = 100
        img_w, img_h = img.size
        x = round(img_w * 1 / 3)
        y = round(img_h / 3 + h / 2)
        font_size = 32
        fill = 'gray'
        outline = 'blue'
        result = img_util.add_text_to_image(img, (x, y), (w, h), text, font_size, fill, outline=outline, text_lines=1,
                                            angle=None)
        # result.show()
        result.save(dst_path)
        result.close()
        img_item = dict()
        img_item[SenderLabel.PATH_FLAG] = dst_path
        imgs.append(img_item)

    return imgs

# 生成图片列表
def get_file_list(file_dir, cnt=3):
    text_format = '测试文件0{}'
    file_path_format = 'file_0{}.txt'

    file_list = list()
    butt = cnt + 1
    for index in range(1, butt):
        dst_path = os.path.join(file_dir, file_path_format.format(index))
        text = text_format.format(index)
        file_util.write_to_file(dst_path, text, encoding='utf-8')
        file_item = dict()
        file_item[SenderLabel.PATH_FLAG] = dst_path
        file_item[SenderLabel.NAME_FLAG] = text
        file_list.append(file_item)

    return file_list

def test_send_mail():
    temp_dir_a = tempfile.mkdtemp()
    temp_dir_b = tempfile.mkdtemp()
    
    mail_host = "smtp.mxhichina.com"
    mail_port = 465
    # 发件人邮箱，自测需要调整为阿里云对应邮箱
    mail_sender = "what@company.com"
    # 邮箱密码，需要调整为正确的
    mail_passwd = "yourpassword"
    mail_name = '名字'
    
    subject = '纯粹只是测试'
    content = '''您好：
            这只是测试，请忽略此邮件信息！
    '''

    # 下面的邮箱和名称，也需要相应调整为正确的
    receivers = list()
    
    item1 = dict()
    item1[SenderLabel.EMAIL_FLAG] = 'zhangs@company.com'
    item1[SenderLabel.NAME_FLAG] = '张三'
    receivers.append(item1)

    item2 = dict()
    item2[SenderLabel.EMAIL_FLAG] = 'lis@company.com'
    item2[SenderLabel.NAME_FLAG] = '李四'
    receivers.append(item2)

    ccs = list()
    
    item3 = dict()
    item3[SenderLabel.EMAIL_FLAG] = 'wangw@company.com'
    item3[SenderLabel.NAME_FLAG] = '王五'
    ccs.append(item3)

    item4 = dict()
    item4[SenderLabel.EMAIL_FLAG] = 'zhaol@company.com'
    item4[SenderLabel.NAME_FLAG] = '赵六'
    ccs.append(item4)

    images = get_img_list(temp_dir_a)
    files = get_file_list(temp_dir_b)

    sender = SenderProcess(mail_host, mail_sender, mail_passwd, port=mail_port, name=mail_name)
    sender.send_mail(subject, content, receivers, ccs=ccs, images=images, files=files)

    # Clean up the directory yourself
    shutil.rmtree(temp_dir_a)
    shutil.rmtree(temp_dir_b)

def test_main():
    # src_dir = r'E:\test'
    # get_img_list(src_dir)
    test_send_mail()
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
#     unittest.main()

    test_main()