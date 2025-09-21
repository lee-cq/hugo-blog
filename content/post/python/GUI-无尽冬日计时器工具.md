---
title: "无尽冬日计时器工具"
author: "Li, Caleb Chaoqun"
date: "2025-08-20"
description: "数据库表结构对比小工"
typora-copy-images-to: ""
tags:
  - "Python"
  - "MySQL"
  - "MsSQL"
---

> 使用Python创建的一个具有固定项目的倒计时工具。

1. 固定项目有：
    第一列：建一、建二、盾兵、矛兵、射手、科技、捐献, 仓库
    第二列：行军一、行军二、行军三、行军四、行军五
    1. 浮窗1：这些项目显示在浮窗中，大小需要保证99时59分59秒的长度能够正确显示，浮窗透明，倒计时未到期的项目行显示绿色；剩余2分钟内显示黄色；到期后项目行显示红色并开始正计时，浮动在所有窗口的前面；
    2. 浮窗2： 一个30*30的正方形半透明浮窗，所有队列大于2min时显示绿等，存在小与2分钟的队列时黄灯，存在超期的项目显示红灯；
3. 将配置保存在零时目录中，启动后先从零时目录加载之前的配置,在每次点击应用后保存，过程数据无需保存；
4. 程序通过托盘运行在后台，通过托盘图标可以打开配置剩余时间的界面，也可以双击浮窗打开设计界面；
5. 设置时间的界面每个项目后面分别允许输入时，分，秒，并通过应用按钮应用并更新该项目的倒计时，更新后的配置时间显示在对应的输入框中。
6. 使用全局快捷键 Ctrl+Shift+Q 控制在2个浮窗和隐藏3个状态中切换，允许在设置中更改快捷键，整合在倒计时配置界面；
7. 使用全局快捷键 Ctrl+Shift+S 快速打开设置窗口，允许在设置中更改快捷键，整合在倒计时配置界面；
8. 在任务到期后发出一个通知，并在设置界面中添加一个选项，是否启用通知;
9. 在控制台上打印关键关键位置的日志，便于排查和理解程序运行状态。


```python
"""
使用Python创建一个具有固定项目的倒计时工具。
1. 固定项目有：
    第一列：建一、建二、盾兵、矛兵、射手、科技、捐献, 仓库
    第二列：行军一、行军二、行军三、行军四、行军五
2.1 浮窗1：这些项目显示在浮窗中，大小需要保证99时59分59秒的长度能够正确显示，浮窗透明，倒计时未到期的项目行显示绿色；剩余2分钟内显示黄色；到期后项目行显示红色并开始正计时，浮动在所有窗口的前面；
2.2 浮窗2： 一个30*30的正方形半透明浮窗，所有队列大于2min时显示绿等，存在小与2分钟的队列时黄灯，存在超期的项目显示红灯；
3. 将配置保存在零时目录中，启动后先从零时目录加载之前的配置,在每次点击应用后保存，过程数据无需保存；
4. 程序通过托盘运行在后台，通过托盘图标可以打开配置剩余时间的界面，也可以双击浮窗打开设计界面；
5. 设置时间的界面每个项目后面分别允许输入时，分，秒，并通过应用按钮应用并更新该项目的倒计时，更新后的配置时间显示在对应的输入框中。
6. 使用全局快捷键 Ctrl+Shift+Q 控制在2个浮窗和隐藏3个状态中切换，允许在设置中更改快捷键，整合在倒计时配置界面；
7. 使用全局快捷键 Ctrl+Shift+S 快速打开设置窗口，允许在设置中更改快捷键，整合在倒计时配置界面；
8. 在任务到期后发出一个通知，并在设置界面中添加一个选项，是否启用通知;
9. 在控制台上打印关键关键位置的日志，便于排查和理解程序运行状态。

pip install pystray pillow

"""
import tkinter as tk
from tkinter import ttk, messagebox
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import datetime
import time
import threading
import re
import tempfile
import os
import json
import logging
from plyer import notification
import keyboard

# 配置日志输出
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

class ProjectCountdownApp:
    def __init__(self):
        logging.info("启动项目倒计时工具")
        
        # 固定项目列表
        self.projects = {
            "建一": None,
            "建二": None,
            "盾兵": None,
            "矛兵": None,
            "射手": None,
            "科技": None,
            "捐献": None,
            "仓库": None,
            "行军一": None,
            "行军二": None,
            "行军三": None,
            "行军四": None,
            "行军五": None
        }
        
        # 存储设置的原始时间（小时、分钟、秒）
        self.original_times = {project: (0, 0, 0) for project in self.projects.keys()}
        
        # 存储已到期项目的正计时开始时间
        self.elapsed_start = {project: None for project in self.projects.keys()}
        
        # 记录项目是否已发送过通知
        self.notification_sent = {project: False for project in self.projects.keys()}
        
        # 快捷键配置
        self.hotkeys = {
            'toggle_windows': 'ctrl+shift+q',  # 切换浮窗状态
            'open_settings': 'ctrl+shift+s'     # 打开设置窗口
        }
        
        # 存储快捷键ID
        self.hotkey_ids = {}
        
        # 通知设置
        self.notification_enabled = True
        
        # 浮窗状态：0-显示浮窗1，1-显示浮窗2，2-都隐藏
        self.window_state = 0
        
        # 临时文件路径
        self.temp_file = os.path.join(tempfile.gettempdir(), "project_countdown_config.json")
        logging.info(f"配置文件路径: {self.temp_file}")
        
        # 尝试加载配置
        self.load_config()
        
        # 创建主窗口（隐藏）
        self.root = tk.Tk()
        self.root.withdraw()
        
        # 创建两个浮窗
        self.create_overlay1()  # 浮窗1：详细倒计时
        self.create_overlay2()  # 浮窗2：状态指示
        
        # 初始化浮窗状态
        self.update_window_state()
        
        # 创建系统托盘
        self.create_system_tray()
        
        # 绑定全局快捷键
        self.bind_global_hotkeys()
        
        # 启动倒计时更新线程
        self.update_thread = threading.Thread(target=self.update_countdowns, daemon=True)
        self.update_thread.start()
        logging.info("倒计时更新线程已启动")
        
        # 启动配置保存线程
        self.save_thread = threading.Thread(target=self.periodic_save, daemon=True)
        self.save_thread.start()
        logging.info("配置保存线程已启动")
    
    def bind_global_hotkeys(self):
        """绑定全局快捷键"""
        try:
            self.unbind_all_hotkeys()
            
            # 绑定切换浮窗状态快捷键
            if self.is_valid_hotkey(self.hotkeys['toggle_windows']):
                hotkey_id = keyboard.add_hotkey(
                    self.hotkeys['toggle_windows'], 
                    self.cycle_window_state
                )
                self.hotkey_ids['toggle_windows'] = hotkey_id
                logging.info(f"已绑定切换浮窗快捷键: {self.hotkeys['toggle_windows']}")
            else:
                logging.error(f"无效的快捷键格式: {self.hotkeys['toggle_windows']}，使用默认值")
                self.hotkeys['toggle_windows'] = 'ctrl+shift+q'
                self.bind_global_hotkeys()
            
            # 绑定打开设置窗口快捷键
            if self.is_valid_hotkey(self.hotkeys['open_settings']):
                hotkey_id = keyboard.add_hotkey(
                    self.hotkeys['open_settings'], 
                    self.open_config_window
                )
                self.hotkey_ids['open_settings'] = hotkey_id
                logging.info(f"已绑定打开设置窗口快捷键: {self.hotkeys['open_settings']}")
            else:
                logging.error(f"无效的快捷键格式: {self.hotkeys['open_settings']}，使用默认值")
                self.hotkeys['open_settings'] = 'ctrl+shift+s'
                self.bind_global_hotkeys()
                
        except Exception as e:
            logging.error(f"绑定快捷键失败: {str(e)}")
    
    def is_valid_hotkey(self, hotkey):
        """验证快捷键格式是否有效"""
        try:
            keyboard.parse_hotkey(hotkey)
            return True
        except:
            return False
    
    def unbind_all_hotkeys(self):
        """解除所有快捷键绑定"""
        try:
            for action, hotkey_id in self.hotkey_ids.items():
                if hotkey_id:
                    keyboard.remove_hotkey(hotkey_id)
            self.hotkey_ids.clear()
        except Exception as e:
            logging.warning(f"解除快捷键绑定时出错: {str(e)}")
            try:
                keyboard.unhook_all_hotkeys()
            except:
                pass
    
    def cycle_window_state(self):
        """循环切换浮窗状态：浮窗1→浮窗2→隐藏→浮窗1..."""
        self.window_state = (self.window_state + 1) % 3
        self.update_window_state()
        state_names = ["显示浮窗1", "显示浮窗2", "隐藏所有浮窗"]
        logging.info(f"浮窗状态切换为: {state_names[self.window_state]}")
    
    def update_window_state(self):
        """根据当前状态更新浮窗显示"""
        if self.window_state == 0:  # 显示浮窗1
            self.overlay1.deiconify()
            self.overlay2.withdraw()
        elif self.window_state == 1:  # 显示浮窗2
            self.overlay1.withdraw()
            self.overlay2.deiconify()
        else:  # 都隐藏
            self.overlay1.withdraw()
            self.overlay2.withdraw()
    
    def create_overlay1(self):
        """创建浮窗1（显示所有项目详细倒计时）"""
        self.overlay1 = tk.Toplevel(self.root)
        self.overlay1.overrideredirect(True)  # 无边框
        self.overlay1.attributes('-alpha', 0.8)  # 透明度
        self.overlay1.attributes('-topmost', True)  # 始终在最前面
        self.overlay1.configure(bg='black')
        
        # 双击浮窗打开配置界面
        self.overlay1.bind("<Double-Button-1>", lambda e: self.open_config_window())
        
        # 创建两列布局
        frame1 = tk.Frame(self.overlay1, bg='black')
        frame1.pack(side=tk.LEFT, padx=5, pady=5)
        
        frame2 = tk.Frame(self.overlay1, bg='black')
        frame2.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 项目标签字典
        self.labels = {}
        
        # 第一列项目
        column1 = ["建一", "建二", "盾兵", "矛兵", "射手", "科技", "捐献", "仓库"]
        for i, project in enumerate(column1):
            frame = tk.Frame(frame1, bg='black')
            frame.grid(row=i, column=0, sticky='w', pady=2)
            
            label = tk.Label(frame, text=f"{project}: ", bg='black', 
                           fg='white', font=('SimHei', 10, 'bold'))
            label.pack(side=tk.LEFT)
            
            # 确保能显示"99时59分59秒"
            time_label = tk.Label(frame, text="未设置", bg='black', 
                               fg='gray', font=('SimHei', 10), width=12)
            time_label.pack(side=tk.LEFT)
            
            self.labels[project] = frame, time_label
        
        # 第二列项目
        column2 = ["行军一", "行军二", "行军三", "行军四", "行军五"]
        for i, project in enumerate(column2):
            frame = tk.Frame(frame2, bg='black')
            frame.grid(row=i, column=0, sticky='w', pady=2)
            
            label = tk.Label(frame, text=f"{project}: ", bg='black', 
                           fg='white', font=('SimHei', 10, 'bold'))
            label.pack(side=tk.LEFT)
            
            time_label = tk.Label(frame, text="未设置", bg='black', 
                               fg='gray', font=('SimHei', 10), width=12)
            time_label.pack(side=tk.LEFT)
            
            self.labels[project] = frame, time_label
        
        # 调整窗口大小
        self.overlay1.update_idletasks()
        width = self.overlay1.winfo_width()
        height = self.overlay1.winfo_height()
        self.overlay1.geometry(f"{width}x{height}+100+100")
        
        # 允许拖动窗口
        self.overlay1.bind("<Button-1>", self.start_drag_overlay1)
        self.overlay1.bind("<B1-Motion>", self.on_drag_overlay1)
        
        logging.info("浮窗1创建完成")
    
    def create_overlay2(self):
        """创建浮窗2（20*20正方形半透明状态指示）"""
        self.overlay2 = tk.Toplevel(self.root)
        self.overlay2.overrideredirect(True)  # 无边框
        self.overlay2.attributes('-alpha', 0.9)  # 半透明
        self.overlay2.attributes('-topmost', True)  # 始终在最前面
        self.overlay2.geometry("30x30+300+200")  # 20*20大小，位置错开
        
        # 状态指示标签
        self.indicator = tk.Label(self.overlay2, bg='gray')
        self.indicator.pack(fill=tk.BOTH, expand=True)
        
        # 双击浮窗打开配置界面
        self.overlay2.bind("<Double-Button-1>", lambda e: self.open_config_window())
        
        # 允许拖动窗口
        self.overlay2.bind("<Button-1>", self.start_drag_overlay2)
        self.overlay2.bind("<B1-Motion>", self.on_drag_overlay2)
        
        logging.info("浮窗2创建完成")
    
    def start_drag_overlay1(self, event):
        """开始拖动浮窗1"""
        self.x1 = event.x
        self.y1 = event.y
    
    def on_drag_overlay1(self, event):
        """拖动浮窗1时更新位置"""
        x = self.overlay1.winfo_x() + event.x - self.x1
        y = self.overlay1.winfo_y() + event.y - self.y1
        self.overlay1.geometry(f"+{x}+{y}")
        logging.debug(f"浮窗1位置更新: x={x}, y={y}")
    
    def start_drag_overlay2(self, event):
        """开始拖动浮窗2"""
        self.x2 = event.x
        self.y2 = event.y
    
    def on_drag_overlay2(self, event):
        """拖动浮窗2时更新位置"""
        x = self.overlay2.winfo_x() + event.x - self.x2
        y = self.overlay2.winfo_y() + event.y - self.y2
        self.overlay2.geometry(f"+{x}+{y}")
        logging.debug(f"浮窗2位置更新: x={x}, y={y}")
    
    def create_system_tray(self):
        """创建系统托盘图标和菜单"""
        try:
            # 创建简单图标
            image = Image.new('RGB', (64, 64), color='blue')
            draw = ImageDraw.Draw(image)
            draw.text((10, 20), "倒", font_size=20, fill='white')
            
            # 创建菜单
            menu = (
                item('显示浮窗1', lambda icon, item: self.set_window_state(0)),
                item('显示浮窗2', lambda icon, item: self.set_window_state(1)),
                item('隐藏所有', lambda icon, item: self.set_window_state(2)),
                item('设置倒计时', lambda icon, item: self.open_config_window()),
                item('退出', lambda icon, item: self.exit_app())
            )
            
            # 创建托盘图标
            self.tray = pystray.Icon("project_countdown", image, "项目倒计时", menu)
            logging.info("系统托盘创建完成")
            
            # 在单独线程中运行托盘
            threading.Thread(target=self.tray.run, daemon=True).start()
        except Exception as e:
            logging.error(f"创建系统托盘失败: {str(e)}")
    
    def set_window_state(self, state):
        """设置浮窗状态"""
        self.window_state = state
        self.update_window_state()
    
    def open_config_window(self, *args):
        """打开配置窗口"""
        logging.info("打开配置窗口")
        
        # 确保浮窗1可见
        self.set_window_state(0)
        
        # 如果窗口已存在则激活它
        if hasattr(self, 'config_window') and isinstance(self.config_window, tk.Toplevel) and self.config_window.winfo_exists():
            self.config_window.lift()
            return
        
        # 创建配置窗口
        self.config_window = tk.Toplevel(self.overlay1)
        self.config_window.title("设置倒计时与快捷键")
        self.config_window.geometry("700x650")
        self.config_window.attributes('-topmost', True)
        
        # 创建带滚动条的主框架
        main_frame = ttk.Frame(self.config_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建笔记本控件（标签页）
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 倒计时设置标签页
        countdown_frame = ttk.Frame(notebook)
        notebook.add(countdown_frame, text="倒计时设置")
        
        # 快捷键设置标签页
        hotkey_frame = ttk.Frame(notebook)
        notebook.add(hotkey_frame, text="快捷键设置")
        
        # 通知设置标签页
        notify_frame = ttk.Frame(notebook)
        notebook.add(notify_frame, text="通知设置")
        
        # ============== 倒计时设置标签页内容 ==============
        canvas = tk.Canvas(countdown_frame)
        scrollbar = ttk.Scrollbar(countdown_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 存储输入框引用
        self.time_entries = {}
        
        # 添加所有项目的输入框
        for i, project in enumerate(self.projects.keys()):
            row_frame = ttk.Frame(scrollable_frame)
            row_frame.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
            
            ttk.Label(row_frame, text=project, width=10).grid(row=0, column=0, padx=5)
            
            hour_entry = ttk.Entry(row_frame, width=5)
            hour_entry.grid(row=0, column=1, padx=2)
            ttk.Label(row_frame, text="时").grid(row=0, column=2)
            
            min_entry = ttk.Entry(row_frame, width=5)
            min_entry.grid(row=0, column=3, padx=2)
            ttk.Label(row_frame, text="分").grid(row=0, column=4)
            
            sec_entry = ttk.Entry(row_frame, width=5)
            sec_entry.grid(row=0, column=5, padx=2)
            ttk.Label(row_frame, text="秒").grid(row=0, column=6)
            
            apply_btn = ttk.Button(row_frame, text="应用", 
                                 command=lambda p=project, h=hour_entry, m=min_entry, s=sec_entry: 
                                 self.apply_time(p, h, m, s))
            apply_btn.grid(row=0, column=7, padx=10)
            
            clear_btn = ttk.Button(row_frame, text="清除",
                                 command=lambda p=project, h=hour_entry, m=min_entry, s=sec_entry: 
                                 self.clear_time(p, h, m, s))
            clear_btn.grid(row=0, column=8, padx=5)
            
            self.time_entries[project] = (hour_entry, min_entry, sec_entry)
            
            # 填充已设置的时间
            hours, mins, secs = self.original_times[project]
            if hours > 0:
                hour_entry.insert(0, str(hours))
            if mins > 0:
                min_entry.insert(0, str(mins))
            if secs > 0:
                sec_entry.insert(0, str(secs))
        
        # ============== 快捷键设置标签页内容 ==============
        ttk.Label(hotkey_frame, text="请使用以下格式: ctrl+shift+q 或 alt+s", font=('SimHei', 10, 'bold')).pack(pady=20)
        
        frame1 = ttk.Frame(hotkey_frame)
        frame1.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(frame1, text="切换浮窗状态:", width=20).pack(side=tk.LEFT)
        self.toggle_hotkey_var = tk.StringVar(value=self.hotkeys['toggle_windows'])
        ttk.Entry(frame1, textvariable=self.toggle_hotkey_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(frame1, text="应用", command=lambda: self.update_hotkey('toggle_windows', self.toggle_hotkey_var.get())).pack(side=tk.LEFT, padx=5)
        
        frame2 = ttk.Frame(hotkey_frame)
        frame2.pack(fill=tk.X, padx=20, pady=10)
        
        ttk.Label(frame2, text="打开设置窗口:", width=20).pack(side=tk.LEFT)
        self.settings_hotkey_var = tk.StringVar(value=self.hotkeys['open_settings'])
        ttk.Entry(frame2, textvariable=self.settings_hotkey_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        ttk.Button(frame2, text="应用", command=lambda: self.update_hotkey('open_settings', self.settings_hotkey_var.get())).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(hotkey_frame, text="支持的修饰键: ctrl, shift, alt；使用+连接；字母为小写", foreground="gray").pack(pady=20)
        
        # ============== 通知设置标签页内容 ==============
        ttk.Label(notify_frame, text="通知设置", font=('SimHei', 12, 'bold')).pack(pady=20)
        
        self.notify_var = tk.BooleanVar(value=self.notification_enabled)
        notify_check = ttk.Checkbutton(
            notify_frame, 
            text="任务到期时启用通知", 
            variable=self.notify_var,
            command=self.update_notification_setting
        )
        notify_check.pack(anchor=tk.W, padx=20, pady=10)
    
    def update_notification_setting(self):
        """更新通知设置"""
        self.notification_enabled = self.notify_var.get()
        logging.info(f"通知设置已更新: {'启用' if self.notification_enabled else '禁用'}")
    
    def update_hotkey(self, action, new_hotkey):
        """更新快捷键设置"""
        try:
            if not re.match(r'^((ctrl|shift|alt)\+)*[a-z]$', new_hotkey, re.IGNORECASE):
                messagebox.showerror("输入错误", "请输入有效的快捷键格式，例如: ctrl+shift+q")
                return
            
            new_hotkey = new_hotkey.lower()
            
            if not self.is_valid_hotkey(new_hotkey):
                messagebox.showerror("输入错误", f"快捷键 '{new_hotkey}' 无效，请尝试其他组合")
                return
            
            self.hotkeys[action] = new_hotkey
            self.bind_global_hotkeys()
            
            logging.info(f"快捷键已更新: {action} -> {self.hotkeys[action]}")
            messagebox.showinfo("成功", f"快捷键已更新为: {self.hotkeys[action]}")
        except Exception as e:
            logging.error(f"更新快捷键失败: {str(e)}")
            messagebox.showerror("错误", f"更新快捷键失败: {str(e)}")
    
    def apply_time(self, project, hour_entry, min_entry, sec_entry):
        """应用设置的时间"""
        try:
            hours = int(hour_entry.get() or 0)
            mins = int(min_entry.get() or 0)
            secs = int(sec_entry.get() or 0)
            
            if hours < 0 or hours > 99 or mins < 0 or mins >= 60 or secs < 0 or secs >= 60:
                messagebox.showerror("输入错误", "请输入有效的时间值！\n小时0-99，分钟和秒0-59")
                return
            
            total_seconds = hours * 3600 + mins * 60 + secs
            
            if total_seconds <= 0:
                messagebox.showinfo("提示", "时间必须大于0")
                return
            
            end_time = datetime.datetime.now() + datetime.timedelta(seconds=total_seconds)
            self.projects[project] = end_time
            self.elapsed_start[project] = None
            self.notification_sent[project] = False  # 重置通知状态
            
            self.original_times[project] = (hours, mins, secs)
            
            # 更新输入框显示
            hour_entry.delete(0, tk.END)
            min_entry.delete(0, tk.END)
            sec_entry.delete(0, tk.END)
            hour_entry.insert(0, str(hours))
            min_entry.insert(0, str(mins))
            sec_entry.insert(0, str(secs))
            
            logging.info(f"项目 [{project}] 倒计时已设置: {hours}时{mins}分{secs}秒")
            
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")
        except Exception as e:
            logging.error(f"应用时间设置失败: {str(e)}")
    
    def clear_time(self, project, hour_entry, min_entry, sec_entry):
        """清除项目的倒计时"""
        self.projects[project] = None
        self.original_times[project] = (0, 0, 0)
        self.elapsed_start[project] = None
        self.notification_sent[project] = False
        
        # 清除输入框
        hour_entry.delete(0, tk.END)
        min_entry.delete(0, tk.END)
        sec_entry.delete(0, tk.END)
        
        logging.info(f"项目 [{project}] 倒计时已清除")
    
    def calculate_time_status(self, project):
        """计算项目的时间状态：剩余时间或已过时间"""
        end_time = self.projects.get(project)
        if end_time is None:
            return ("未设置", None)
            
        now = datetime.datetime.now()
        
        if end_time < now:
            # 如果是刚到期，记录正计时开始时间
            if self.elapsed_start[project] is None:
                self.elapsed_start[project] = now
                logging.info(f"项目 [{project}] 已到期")
            
            # 计算已过时间
            elapsed = now - self.elapsed_start[project]
            return ("elapsed", int(elapsed.total_seconds()))
        else:
            # 计算剩余时间
            remaining = end_time - now
            return ("remaining", int(remaining.total_seconds()))
    
    def check_for_expired_projects(self):
        """检查是否有超期项目"""
        for project in self.projects:
            status, _ = self.calculate_time_status(project)
            if status == "elapsed":
                return True
        return False
    
    def get_min_remaining_time(self):
        """获取所有项目中最小的剩余时间（秒）"""
        min_remaining = None
        for project in self.projects:
            status, seconds = self.calculate_time_status(project)
            if status == "remaining" and seconds is not None:
                if min_remaining is None or seconds < min_remaining:
                    min_remaining = seconds
        return min_remaining
    
    def update_overlay2_color(self):
        """根据项目状态更新浮窗2颜色"""
        # 浮窗2颜色逻辑：
        # 1. 存在超期项目 → 红色
        # 2. 无超期但存在≤2分钟的项目 → 黄色
        # 3. 所有项目>2分钟 → 绿色
        # 4. 无有效项目 → 灰色
        
        if self.check_for_expired_projects():
            self.indicator.configure(bg='red')
        else:
            min_remaining = self.get_min_remaining_time()
            if min_remaining is None:
                self.indicator.configure(bg='gray')
            elif min_remaining > 120:  # >2分钟
                self.indicator.configure(bg='green')
            elif 0 < min_remaining <= 120:  # ≤2分钟
                self.indicator.configure(bg='yellow')
            else:  # ≤2分钟但>0
                self.indicator.configure(bg='yellow')
    
    def send_notification(self, project):
        """发送系统通知"""
        if not self.notification_enabled or self.notification_sent[project]:
            return
            
        try:
            notification.notify(
                title="项目倒计时",
                message=f"项目 '{project}' 已到期！",
                timeout=10
            )
            self.notification_sent[project] = True
            logging.info(f"已发送项目 [{project}] 到期通知")
        except Exception as e:
            logging.error(f"发送通知失败: {str(e)}")
    
    def format_time(self, status, seconds):
        """格式化时间显示"""
        if status != "remaining" and status != "elapsed":
            return "未设置"
            
        days = seconds // 86400
        seconds %= 86400
        
        hours = seconds // 3600
        seconds %= 3600
        
        mins = seconds // 60
        secs = seconds % 60
        
        if days > 0:
            return f"{days}天{hours}时{mins}分{secs}秒"
        else:
            return f"{hours:02d}时{mins:02d}分{secs:02d}秒"
    
    def update_countdowns(self):
        """更新所有项目的倒计时显示，每秒更新一次"""
        while True:
            try:
                # 更新浮窗1项目状态
                for project, (row_frame, time_label) in self.labels.items():
                    status, seconds = self.calculate_time_status(project)
                    
                    # 如果项目刚到期且需要通知，发送通知
                    if status == "elapsed" and seconds <= 1 and not self.notification_sent[project]:
                        self.send_notification(project)
                    
                    time_str = self.format_time(status, seconds)
                    
                    # 设置颜色
                    if status == "remaining":
                        if seconds > 120:  # >2分钟
                            color = "green"
                        else:  # ≤2分钟
                            color = "yellow"
                    elif status == "elapsed":
                        color = "red"
                    else:
                        color = "gray"
                    
                    # 更新UI
                    self.overlay1.after(0, lambda rf=row_frame: rf.configure(bg='black'))
                    self.overlay1.after(0, lambda tl=time_label, t=time_str, c=color: 
                                     tl.config(text=t, fg=c))
                
                # 更新浮窗2颜色
                self.root.after(0, self.update_overlay2_color)
                
                time.sleep(1)
            except Exception as e:
                logging.error(f"更新倒计时时出错: {str(e)}")
                time.sleep(1)
    
    def save_config(self):
        """保存配置到临时文件"""
        try:
            data = {
                "projects": {},
                "original_times": {},
                "hotkeys": self.hotkeys,
                "notification_enabled": self.notification_enabled
            }
            
            # 保存项目结束时间
            for project, end_time in self.projects.items():
                if end_time is not None and end_time > datetime.datetime.now():
                    data["projects"][project] = end_time.isoformat()
            
            # 保存原始时间设置
            for project, (h, m, s) in self.original_times.items():
                if h > 0 or m > 0 or s > 0:
                    data["original_times"][project] = (h, m, s)
            
            # 写入临时文件
            with open(self.temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logging.debug("配置已保存")
        except Exception as e:
            logging.error(f"保存配置失败: {str(e)}")
    
    def load_config(self):
        """从临时文件加载配置"""
        if not os.path.exists(self.temp_file):
            logging.info("没有找到配置文件，使用默认配置")
            return
            
        try:
            with open(self.temp_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # 加载项目结束时间
            if "projects" in data:
                for project, time_str in data["projects"].items():
                    if project in self.projects:
                        end_time = datetime.datetime.fromisoformat(time_str)
                        # 只加载未来的时间
                        if end_time > datetime.datetime.now():
                            self.projects[project] = end_time
                            logging.debug(f"已加载项目 [{project}] 的倒计时配置")
            
            # 加载原始时间设置
            if "original_times" in data:
                for project, (h, m, s) in data["original_times"].items():
                    if project in self.original_times:
                        self.original_times[project] = (h, m, s)
            
            # 加载快捷键设置
            if "hotkeys" in data:
                for action, hotkey in data["hotkeys"].items():
                    if action in self.hotkeys and self.is_valid_hotkey(hotkey):
                        self.hotkeys[action] = hotkey
            
            # 加载通知设置
            if "notification_enabled" in data:
                self.notification_enabled = data["notification_enabled"]
            
            logging.info("配置加载完成")
                
        except Exception as e:
            logging.error(f"加载配置失败: {str(e)}")
            try:
                os.remove(self.temp_file)
                logging.info("已删除损坏的配置文件")
            except:
                pass
    
    def periodic_save(self):
        """定期保存配置，每30秒一次"""
        while True:
            self.save_config()
            time.sleep(30)
    
    def exit_app(self):
        """退出应用程序"""
        logging.info("准备退出程序")
        
        # 退出前保存一次配置
        self.save_config()
        
        # 停止托盘
        self.tray.stop()
        
        # 关闭配置窗口
        if hasattr(self, 'config_window') and isinstance(self.config_window, tk.Toplevel) and self.config_window.winfo_exists():
            self.config_window.destroy()
        
        # 关闭浮窗和主窗口
        self.overlay1.destroy()
        self.overlay2.destroy()
        self.root.destroy()
        
        # 停止全局快捷键监听
        try:
            keyboard.unhook_all()
        except:
            pass
        
        logging.info("程序已退出")
        os._exit(0)

if __name__ == "__main__":
    try:
        app = ProjectCountdownApp()
        app.root.mainloop()
    except Exception as e:
        logging.critical(f"程序运行出错: {str(e)}", exc_info=True)
        os._exit(1)
```