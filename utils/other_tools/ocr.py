import time
import cv2
from PIL import Image
import easyocr
from utils.logging_tool.log_control import INFO, ERROR, WARNING


class OCRProcessor:
    def __init__(self):
        """
        初始化 PaddleOCR使用优化参数
        """
        self.ocr = easyocr.Reader(["ch_sim", "en"], gpu=False)

    def recognize_text(self, image_path=None, roi=None):
        """
        识别图片中的文本（支持智能 ROI 处理）
        :param image_path: 图片路径
        :param roi: (x1, y1, x2, y2) 支持以下特殊值场景：
                    - (0,0,0,0): 识别整个图片
                    - (x, y, 0, 0): 从(x,y)到右下角
                    - (0,0,w,h): 从左上角到指定宽高
        :return: 识别到的文本列表
        """
        if not image_path:
            raise ValueError("❌ 请输入正确的 `image_path`！")

        # 读取图片并获取尺寸
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"❌ 图片无法加载: {image_path}")
        height, width = image.shape[:2]
        start_time = time.perf_counter()
        # 智能处理 ROI 区域
        if roi is None:
            roi = (0, 0, width, height)  # 默认全屏
        else:
            x1, y1, x2, y2 = roi

            # 处理特殊值逻辑
            x2 = width if x2 <= 0 else x2
            y2 = height if y2 <= 0 else y2

            # 坐标排序确保 x1 < x2, y1 < y2
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])

            # 边界约束
            x1 = max(0, min(x1, width))
            x2 = max(0, min(x2, width))
            y1 = max(0, min(y1, height))
            y2 = max(0, min(y2, height))

            roi = (x1, y1, x2, y2)

        # 执行裁剪
        cropped_image = image[roi[1] : roi[3], roi[0] : roi[2]]

        # OCR 识别

        result = self.ocr.readtext(cropped_image, detail=0)
        # 检查 OCR 返回结果是否有效
        if result == [None]:
            WARNING.logger.warning("OCR 识别未返回任何结果。")
            # print("OCR 识别未返回任何结果。")
            return []
        result_text = ",".join(result)
        # 日志记录
        INFO.logger.info(f"⏳ OCR 识别耗时: {time.perf_counter() - start_time:.2f}秒")
        INFO.logger.info(f"📝 识别区域: {roi} | 结果: {result_text}")
        # print(f"⏳ OCR 识别耗时: {time.perf_counter() - start_time:.2f}秒")
        # print(f"📝 识别区域: {roi} | 结果: {result_text}")
        return result_text


if __name__ == "__main__":
    # 测试用例
    ocr = OCRProcessor()
    image_path = r"D:\LzyPro\android\test_pictures\login_success.png"

    # 场景1: 识别整个图片
    print("场景1:", ocr.recognize_text(image_path, roi=(0, 0, 0, 0)))

    # 场景2: 从(55,300)到右下角
    print("场景2:", ocr.recognize_text(image_path, roi=(55, 300, 0, 0)))

    # 场景3: 识别(0,0)到(55,300)
    print("场景3:", ocr.recognize_text(image_path, roi=(0, 0, 55, 300)))
    res = [None]
    print(res)
    print(res == [None])
    print(not res)
