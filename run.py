import base64
from flask import Flask, request, jsonify
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

app = Flask(__name__)

def plt_chinese():
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] # 修改中文字體
    plt.rcParams['axes.unicode_minus'] = False # 顯示負號

def plot_gauge(total_score):
    total_score = max(-1000, min(total_score, 1000))
    plt_chinese()
    min_value = -1000
    max_value = 1000
    
    # 設置漸層顏色
    colors = ['#4d8cb3', '#b3e033', '#ffb84d', '#e64d1a']
    cmap = mcolors.LinearSegmentedColormap.from_list('custom_cmap', colors)
    
    # 創建從-1000到1000的數據範圍
    x = np.linspace(-1000, 1000, 1000)
    y = np.zeros_like(x)
    
    # 繪製漸層色
    plt.figure(figsize=(8, 2))
    plt.imshow([x], cmap=cmap, aspect='auto', extent=[min_value, max_value, 0, 1])
    
    # 標註 total_score 的位置
    plt.axvline(x=total_score, color='black', linestyle=':')
    
    # 隱藏刻度
    plt.xticks([]) 
    plt.yticks([]) 
    
    # 標題
    plt.title('情緒溫度計')
    
    # 顯示當前情緒
    if -1000 <= total_score < -500:
        emotion_label = "負面情緒"
    elif -500 <= total_score < -200:
        emotion_label = "複雜情緒"
    elif -200 <= total_score < 200:
        emotion_label = "中性情緒"
    elif 200 <= total_score < 500:
        emotion_label = "正向情緒"
    else:
        emotion_label = "積極情緒"
    
    # plt.text(total_score, -0.1, f'當前情緒：{emotion_label}', ha='center')
    
    plt.savefig('gauge_plot.png')  # 將圖片保存到文件中
    plt.close()  # 關閉圖形窗口

@app.route('/linebot', methods=['POST'])
def calculate():
    data = request.json  # 接收從用戶端發送的 JSON 數據
    total_score = data['total_score']  # 從 JSON 數據中獲取 total_score
    plot_gauge(total_score)  # 使用 total_score 調用 plot_gauge 函式繪製情緒溫度計
    
    # 讀取繪製的圖片並轉換為 base64 字串
    with open('gauge_plot.png', 'rb') as img_file:
        img_data = img_file.read()
        img_base64 = base64.b64encode(img_data).decode('utf-8')
    
    return jsonify({'image_base64': img_base64})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
