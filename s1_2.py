from flask import Flask, request, render_template
import tkinter as tk
import threading
import queue

app = Flask(__name__)
text_queue = queue.Queue()
current_thread = None

def show_gui():
    root = tk.Tk()
    root.attributes('-alpha', 0.7)
    root.configure(bg='black')
    root.overrideredirect(True)  # 消除边框和标题栏
    root.attributes('-topmost', True)  # 窗口始终在前
    text_var = tk.StringVar()
    font_style = "System"
    font_size = 170
    label = tk.Label(root, textvariable=text_var, font=(font_style, font_size), fg='white', bg='black')
    label.pack(expand='yes', fill='both')
    while True:
        if not text_queue.empty():
            text = text_queue.get()
            text_var.set(text)
        root.update_idletasks()
        root.update()

@app.route('/', methods=['GET', 'POST'])
def home():
    global current_thread
    if request.method == 'POST':
        text = request.form.get('text')
        text_queue.put(text)
        if current_thread and current_thread.is_alive():
            return render_template('index.html')
        current_thread = threading.Thread(target=show_gui)
        current_thread.start()  # 在新的线程中运行show_gui函数
        return render_template('index.html')
    return render_template('index.html')  # 返回输入页面

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000, debug=False)
