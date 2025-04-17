import os
from time import sleep
import numpy as np
from matplotlib import pyplot as plt
import cv2
import ddddocr
from PIL import Image
import pytesseract


def test(n):
    filepath = f"./code/vcode{n}.png"
    # opencv读取文件
    im = cv2.imread(filepath)
    # 显示图片
    # plt.imshow(im[:,:,[2,1,0]])
    # plt.show()

    # 将图片转成灰度图
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # 显示图片
    # plt.imshow(im_gray,cmap="gray")
    # plt.show()

    # 将图片做二值化处理，与之设定为127，像素值大约127的置为0，小于127的置为255
    ret, im_inv = cv2.threshold(im_gray, 240, 255, cv2.THRESH_BINARY_INV)
    # 显示图片
    # plt.imshow(im_inv, cmap="gray")
    # plt.show()

    # 构建卷积核的数据集，实现模糊成像的效果
    kernel = 1 / 16 * np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    # 使用高斯模糊对图片进行降噪
    im_blur = cv2.filter2D(im_inv, -1, kernel)
    # 显示图片
    # plt.imshow(im_blur,cmap="gray")
    # plt.show()

    # 将图片做二值化处理，阈值设定为185，将像素值大于185的置为0，小于185的置为255
    ret, im_res = cv2.threshold(im_blur, 210, 255, cv2.THRESH_BINARY)
    # 显示图片
    plt.imshow(im_res, cmap="gray")
    plt.show()
    cv2.imwrite("test.png", im_res)
    # ocr = ddddocr.DdddOcr(old=True)
    # with open('test.png', 'rb') as f:
    #     image = f.read()
    # res = ocr.classification(image)
    # ocr = ddddocr.DdddOcr(old=True)
    # with open(filepath, 'rb') as f:
    #     image = f.read()
    # re = ocr.classification(image)

    print(f"{n}".center(20, "="))
    # print(re.center(20,'_'))
    # print(res.center(20,'-'))
    # image = Image.open('test.png')
    # img_str = pytesseract.image_to_string(image)
    # print(img_str.center(20,'^'))
    # print('\n')


def test1(n):
    import cv2 as cv

    # 对存储的验证码进行均值迁移去噪声，然后二值化处理，最终覆盖源文件，进行存储
    # 原图
    src_file = f"./code/vcode{n}.png"
    # 去噪图
    blurred_file = "t02_blurred.png"
    # 灰度图
    gray_file = "t03_gray.png"
    # 二值化图
    binary_file = "t04_binary.png"

    # 文件读取
    image = cv.imread(src_file)
    # cv.imwrite("复制图像", image)
    # 均值迁移去噪
    blurred = cv.pyrMeanShiftFiltering(image, 5, 70)
    # 保存文件
    cv.imwrite(blurred_file, blurred)

    image = cv.imread(blurred_file)
    blurred = cv.pyrMeanShiftFiltering(image, 1, 90)
    cv.imwrite("t02_blurred1.png", blurred)

    image = cv.imread(blurred_file)
    blurred = cv.pyrMeanShiftFiltering(image, 1, 50)
    cv.imwrite("t02_blurred2.png", blurred)

    image = cv.imread(blurred_file)
    blurred = cv.pyrMeanShiftFiltering(image, 1, 40)
    cv.imwrite("t02_blurred3.png", blurred)
    # 灰度图
    gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
    # 保存文件
    cv.imwrite(gray_file, gray)
    # 二值化处理
    t, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    # t为获取的阈值
    # print(t)
    # 保存文件
    cv.imwrite(binary_file, binary)

    # 使用 PIL 打开图像转化为图像对象，并使用 pytesseract 进行图像识别验证码
    file_name = "t04_binary.png"
    image = Image.open(file_name)
    img_str = pytesseract.image_to_string(image)

    # print(img_str)

    ocr = ddddocr.DdddOcr(old=True)
    with open(src_file, "rb") as f:
        image = f.read()
    re = ocr.classification(image)

    ocr = ddddocr.DdddOcr(old=True)
    with open(file_name, "rb") as f:
        image = f.read()
    res = ocr.classification(image)
    print(f"{n}".center(20, "!"))
    print(f"{re}".center(20, "_"))
    print(f"{res}".center(20, "="))
    print(f"{img_str}".center(20, "-"))
    # print(res)


def fix_img(filepath):
    # sourcery skip: inline-immediately-returned-variable, merge-dict-assign
    # opencv读取文件
    im = cv2.imread(filepath)
    # 显示图片
    # plt.imshow(im[:,:,[2,1,0]])
    # plt.show()

    # 将图片转成灰度图
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # 显示图片
    # plt.imshow(im_gray,cmap="gray")
    # plt.show()

    # 将图片做二值化处理，与之设定为127，像素值大约127的置为0，小于127的置为255
    ret, im_inv = cv2.threshold(im_gray, 240, 255, cv2.THRESH_BINARY_INV)
    # 显示图片
    # plt.imshow(im_inv, cmap="gray")
    # plt.show()

    # 构建卷积核的数据集，实现模糊成像的效果
    kernel = 1 / 16 * np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    # 使用高斯模糊对图片进行降噪
    im_blur = cv2.filter2D(im_inv, -1, kernel)
    # 显示图片
    # plt.imshow(im_blur,cmap="gray")
    # plt.show()

    # 将图片做二值化处理，阈值设定为185，将像素值大于185的置为0，小于185的置为255
    ret, im_res = cv2.threshold(im_blur, 210, 255, cv2.THRESH_BINARY)
    # 显示图片
    # plt.imshow(im_res,cmap="gray")
    # plt.show()
    # cv2.imwrite('test.png', im_res)
    # 将观察到的四个字符在图片中所处的区域信息保存到字典中
    roi_dict = {}
    roi_dict[0] = im_res[10:50, 0:40]
    roi_dict[1] = im_res[10:50, 40:80]
    roi_dict[2] = im_res[10:50, 80:120]
    roi_dict[3] = im_res[10:50, 120:160]

    return roi_dict


def cut_img(train_dir, cut_dir, suffix):
    # 浏览训练集图片样本的目录
    for root, dirs, files in os.walk(train_dir):
        for f in files:
            # 获取文件路径
            filepath = os.path.join(root, f)
            # 检查文件名后缀
            filesuffix = os.path.splitext(filepath)[1][1:]
            if filesuffix in suffix:
                # 通过特征工程处理图片并获取每个字符所在区域的信息
                roi_dict = fix_img(filepath)
                # 将图片按照获取到的每个字符所在区域的信息切割为不同的图片，分开保存
                for i in sorted(roi_dict.keys()):
                    cv2.imwrite(
                        "{0}/{1}_{2}.png".format(cut_dir, f.split(".")[0], f[i]),
                        roi_dict[i],
                    )

    # 关闭OpenCV的写操作
    cv2.waitKey(0)
    return True


def train_model(cut_dir, suffix):
    # 创建一个空的数据集存放验证码的图片信息
    samples = np.empty((0, 1600))
    # 创建一个控的标签列表
    labels = []

    # 浏览单个字符的图片训练集的目录
    for root, dirs, files in os.walk(cut_dir):
        for f in files:
            filepath = os.path.join(root, f)
            filesuffix = os.path.splitext(filepath)[1][1:]
            if filesuffix in suffix:
                filepath = os.path.join(root, f)
                # 读取图片的标签
                label = f.split(".")[0].split("_")[-1]
                labels.append(label)
                # 将验证码的图片信息存放到数据集中
                im = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
                # print(im.shape)
                sample = im.reshape((1, 1600)).astype(np.float32)
                samples = np.append(samples, sample, 0)
                samples = samples.astype(np.float32)
    # 将数据集与标签进行映射
    unique_labels = list(set(labels))
    unique_ids = list(range(len(unique_labels)))
    label_id_map = dict(zip(unique_labels, unique_ids))
    id_label_map = dict(zip(unique_ids, unique_labels))
    label_ids = list(map(lambda x: label_id_map[x], labels))
    label_ids = np.array(label_ids).reshape((-1, 1)).astype(np.float32)

    # 使用OpenCV自带的KNN相似度模型进行机器学习
    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, label_ids)

    # 返回训练好的模型，数据ID与标签的映射字典
    return {"model": model, "id_label_map": id_label_map}


def rek_img(model_dict, rek_dir, suffix):
    # 获取训练好的模型
    model = model_dict["model"]
    # 获取模型中的数据ID与标签的映射字典
    id_label_map = model_dict["id_label_map"]
    label_dict = {}
    result_str = ""
    # 浏览测试集图片的目录
    for root, dirs, files in os.walk(rek_dir):
        for f in files:
            filepath = os.path.join(root, f)
            filesuffix = os.path.splitext(filepath)[1][1:]
            if filesuffix in suffix:
                # 通过特征工程处理图片并获取每个字符所在区域的信息
                roi_dict = fix_img(filepath)
                # 对每个字符所在区域的信息进行处理
                for i in sorted(roi_dict.keys()):
                    # 将字符所在区域的信息转换为数据集格式
                    sample = roi_dict[i].reshape((1, 1600)).astype(np.float32)
                    # 通过训练好的模型匹配识别出最相似的数据集，并返回数据ID
                    ret, results, neighbours, distances = model.findNearest(sample, k=3)
                    # 通过数据ID查询出对应的标签，并写入到字典中
                    label_id = int(results[0, 0])
                    label = id_label_map[label_id]
                    label_dict[i] = label

                # 将标签字典中的值依次取出，显示为验证码图片中的四个字符
                result_str = "".join(str(v) for k, v in sorted(label_dict.items()))
                # 将测试集图片的文件名与识别出的字符以逗号分割存入到CSV中
                # with open(results_csv, "a+") as myfile:
                # myfile.write("{0},{1}\n".format(f,result_str))
    return result_str


if __name__ == "__main__":
    suffix = ["jpg", "png"]
    train_dir = "./vcode/train"
    cut_dir = "./vcode/cut_dir"
    # rek_dir = '../vcode/test'
    results_csv = "./results.csv"
    # print('INFO: Cutting images...')
    # cut_img(train_dir,cut_dir,suffix)
    # print('INFO: Training model...')
    # model_dict = train_model(cut_dir,suffix)
    # print('INFO: Recognizing images in directory {0}...'.format(rek_dir))
    # rek_img(model_dict,train_dir,suffix,results_csv)
    # print('INFO: See results in {0}'.format(results_csv))
    # model_dict = train_model("./vcode/cut_dir", ["png"])
    # code = rek_img(model_dict, "./vcode/test", ["png"])
    # if "x" in code and len(code) > 2:
    #     print(int(code[0] * int(code[2])))
    # else:
    #     print(eval(code[:3]))
