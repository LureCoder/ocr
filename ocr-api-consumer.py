import requests
import base64
import os

def call_ocr_api(image_path):
    # 检查文件是否存在
    if not os.path.exists(image_path):
        print(f"文件 {image_path} 不存在。")
        return

    # 读取图片文件
    with open(image_path, 'rb') as file:
        image_data = file.read()

    # 将图片数据编码为 base64
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    # 发送 POST 请求
    url = 'http://127.0.0.1:5001/ocr'
    data = {'image': image_base64}
    print(f"发送的数据: {data}")
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()
        if 'text' in result:
            print("识别结果：")
            for line in result['text']:
                print(line)
        elif 'error' in result:
            print(f"调用 API 出错：{result['error']}")
    except requests.RequestException as e:
        print(f"请求出错：{e}")
    except ValueError as e:
        print(f"解析响应出错：{e}")


if __name__ == "__main__":
    # 替换为你要识别的图片路径
    image_path = 'C:\\Users\\lchua\\Pictures\\210730tr5ozvvmir58yrri.png'
    call_ocr_api(image_path)
    