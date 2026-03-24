#!/usr/bin/env python

from tkinter import *
from tkinter import scrolledtext, messagebox
import subprocess
import os
import threading

class SQLMapGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLMap 自动注入工具")
        self.root.geometry("800x700")
        
        # 设置SQLMap路径
        self.sqlmap_path = os.path.join(os.path.dirname(__file__), "sqlmapproject-sqlmap-8f75402", "sqlmap.py")
        
        # 创建主框架
        main_frame = Frame(root, padx=10, pady=10)
        main_frame.pack(fill=BOTH, expand=True)
        
        # URL输入区域
        url_frame = Frame(main_frame)
        url_frame.pack(fill=X, pady=10)
        
        Label(url_frame, text="目标URL:", font=("Arial", 12)).pack(side=LEFT, padx=5)
        
        self.url_entry = Entry(url_frame, font=("Arial", 12), width=60)
        self.url_entry.pack(side=LEFT, fill=X, expand=True, padx=5)
        
        # 请求类型选择
        request_frame = Frame(main_frame)
        request_frame.pack(fill=X, pady=10)
        
        Label(request_frame, text="请求类型:", font=("Arial", 12)).pack(side=LEFT, padx=5)
        
        self.request_type = StringVar(value="GET")
        Radiobutton(request_frame, text="GET", variable=self.request_type, value="GET", font=("Arial", 10)).pack(side=LEFT, padx=10)
        Radiobutton(request_frame, text="POST", variable=self.request_type, value="POST", font=("Arial", 10)).pack(side=LEFT, padx=10)
        
        # POST数据输入
        post_frame = Frame(main_frame)
        post_frame.pack(fill=X, pady=10)
        
        Label(post_frame, text="POST数据:", font=("Arial", 12)).pack(anchor=W, padx=5, pady=5)
        
        self.post_entry = Entry(post_frame, font=("Arial", 12), width=80)
        self.post_entry.pack(fill=X, padx=5)
        self.post_entry.insert(0, "id=1")  # 默认值
        
        # 注入按钮
        button_frame = Frame(main_frame)
        button_frame.pack(fill=X, pady=10)
        
        inject_button = Button(button_frame, text="开始注入", font=("Arial", 12), command=self.start_injection)
        inject_button.pack(side=LEFT, padx=5)
        
        # 结果显示区域
        result_frame = Frame(main_frame)
        result_frame.pack(fill=BOTH, expand=True, pady=10)
        
        Label(result_frame, text="注入结果:", font=("Arial", 12)).pack(anchor=W, padx=5, pady=5)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, font=("Consolas", 10), wrap=WORD)
        self.result_text.pack(fill=BOTH, expand=True, padx=5)
        
        # 状态标签
        self.status_label = Label(main_frame, text="就绪", font=("Arial", 12), fg="green")
        self.status_label.pack(anchor=W, padx=5, pady=5)
        
    def start_injection(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("错误", "请输入目标URL")
            return
        
        # 清空结果区域
        self.result_text.delete(1.0, END)
        
        # 更新状态
        self.status_label.config(text="正在注入...", fg="blue")
        
        # 获取请求类型和POST数据
        request_type = self.request_type.get()
        post_data = self.post_entry.get().strip() if request_type == "POST" else None
        
        # 在新线程中执行注入，避免阻塞界面
        thread = threading.Thread(target=self.run_injection, args=(url, request_type, post_data))
        thread.daemon = True
        thread.start()
    
    def run_injection(self, url, request_type, post_data):
        # 构建SQLMap命令
        cmd = [
            "python",
            self.sqlmap_path,
            "-u", url,
            "--batch",  # 自动回答所有问题
            "--dump",   # 尝试转储数据库内容
            "-v", "1",   # 详细级别
            "--level=5", # 提高检测级别
            "--risk=3"   # 提高风险级别，增加检测能力
        ]
        
        # 添加POST数据
        if request_type == "POST" and post_data:
            cmd.extend(["--data", post_data])
        
        # 添加自动参数检测
        cmd.append("--forms")  # 自动检测表单
        cmd.append("--crawl=2")  # 爬取深度为2，寻找更多注入点
        
        try:
            # 执行命令并捕获输出
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=os.path.dirname(self.sqlmap_path)
            )
            
            # 实时显示输出
            for line in process.stdout:
                self.result_text.insert(END, line)
                self.result_text.see(END)
            
            process.wait()
            
            if process.returncode == 0:
                self.status_label.config(text="注入完成", fg="green")
                messagebox.showinfo("成功", "SQL注入完成！")
            else:
                self.status_label.config(text="注入失败", fg="red")
                messagebox.showerror("失败", "SQL注入失败，请检查URL是否正确")
        except Exception as e:
            self.status_label.config(text="错误", fg="red")
            messagebox.showerror("错误", f"执行注入时出错: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    app = SQLMapGUI(root)
    root.mainloop()
