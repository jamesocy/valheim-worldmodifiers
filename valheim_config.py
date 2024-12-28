import json
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, colorchooser
import re

class ValheimServerConfig:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("英灵神殿服务器配置工具")
        self.window.geometry("500x800")
        self.window.resizable(False, False)

        # 加载配置
        self.config = self.load_config()
        
        # 初始化语言设置
        self.current_lang = 'cn'
        self.init_translations()
        
        # 创建主框架
        self.content_frame = ttk.Frame(self.window)
        self.content_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # 创建语言切换按钮
        self.lang_button = ttk.Button(
            self.window,
            text="English/中文",
            command=self.toggle_language,
            width=15
        )
        self.lang_button.place(relx=1.0, x=-10, y=5, anchor="ne")

        # 初始化界面
        self.init_ui()

    def init_ui(self):
        """初始化用户界面"""
        # 创建服务器名称编辑框架
        self.name_frame = ttk.LabelFrame(self.content_frame, text=self.get_text('server_name_frame'))
        self.name_frame.pack(fill="x", padx=5, pady=5)
        self.create_name_editor(self.name_frame)

        # 创建基本设置框架
        self.basic_frame = ttk.LabelFrame(self.content_frame, text=self.get_text('basic_settings_frame'))
        self.basic_frame.pack(fill="x", padx=5, pady=10)
        self.create_basic_settings(self.basic_frame)

        # 创建游戏设置框架
        self.game_frame = ttk.LabelFrame(self.content_frame, text=self.get_text('game_settings_frame'))
        self.game_frame.pack(fill="x", padx=5, pady=10)
        self.create_game_settings(self.game_frame)

        # 创建额外设置框架
        self.extra_frame = ttk.LabelFrame(self.content_frame, text=self.get_text('extra_settings_frame'))
        self.extra_frame.pack(fill="x", padx=5, pady=10)
        self.create_extra_settings(self.extra_frame)

    def get_text(self, key):
        """获取当前语言的文本"""
        return self.translations[self.current_lang].get(key, key)

    def init_translations(self):
        """初始化翻译"""
        self.translations = {
            'cn': {
                'window_title': "英灵神殿服务器配置工具",
                'server_name_frame': "服务器名称设置",
                'basic_settings_frame': "基本设置",
                'game_settings_frame': "游戏难度设置",
                'extra_settings_frame': "额外功能设置",
                'port_label': "端口号:",
                'world_name_label': "世界名称:",
                'password_label': "密码:",
                'public_label': "公开服务器:",
                'combat_label': "战斗难度:",
                'death_penalty_label': "死亡惩罚:",
                'resources_label': "资源数量:",
                'raids_label': "袭击频率:",
                'portals_label': "传送门设置:",
                'no_build_cost_label': "无建造消耗",
                'passive_mobs_label': "和平生物",
                'player_events_label': "玩家触发袭击",
                'no_map_label': "无地图",
                'save_button': "保存配置"
            },
            'en': {
                'window_title': "Valheim Server Configuration Tool",
                'server_name_frame': "Server Name",
                'basic_settings_frame': "Basic Settings",
                'game_settings_frame': "Game Settings",
                'extra_settings_frame': "Extra Settings",
                'port_label': "Port:",
                'world_name_label': "World Name:",
                'password_label': "Password:",
                'public_label': "Public Server:",
                'combat_label': "Combat:",
                'death_penalty_label': "Death Penalty:",
                'resources_label': "Resources:",
                'raids_label': "Raids:",
                'portals_label': "Portals:",
                'no_build_cost_label': "No Build Cost",
                'passive_mobs_label': "Passive Mobs",
                'player_events_label': "Player Events",
                'no_map_label': "No Map",
                'save_button': "Save Config"
            }
        }

    def load_config(self):
        """加载配置文件"""
        default_config = {
            "serverName": "Valheim Server",
            "port": "17741",
            "worldName": "MyWorld",
            "password": "123456",
            "public": True,
            "modifiers": {
                "Combat": "Normal",
                "DeathPenalty": "Normal",
                "Resources": "Normal",
                "Raids": "Normal",
                "Portals": "Normal"
            }
        }

        try:
            if os.path.exists('config.json'):
                with open('config.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default_config
        except:
            return default_config

    def save_config(self):
        """保存配置到文件"""
        config = {
            "serverName": self.text_input.get(),
            "port": self.vars["port"].get(),
            "worldName": self.vars["worldName"].get(),
            "password": self.vars["password"].get(),
            "public": self.vars["public"].get(),
            "modifiers": {
                modifier: self.cn_to_en_map[modifier][var.get()]
                if self.current_lang == 'cn' else var.get()
                for modifier, var in self.modifier_vars.items()
            },
            "extraSettings": {
                key: var.get()
                for key, var in self.extra_vars.items()
            }
        }

        # 保存配置文件
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

        # 生成批处理文件
        batch_content = f"""@echo off
set SteamAppId=892970

echo "Starting server PRESS CTRL-C to exit"

REM Tip: Make a local copy of this script to avoid it being overwritten by steam.
REM NOTE: Minimum password length is 5 characters & Password cant be in the server name.
REM NOTE: You need to make sure the ports 2456-2458 is being forwarded to your server through your local router & firewall.
valheim_server -nographics -batchmode -name "{config['serverName']}" -port {config['port']} -world "{config['worldName']}" -password "{config['password']}" -public {1 if config['public'] else 0} -modifier Combat {config['modifiers']['Combat'].lower()} -modifier DeathPenalty {config['modifiers']['DeathPenalty'].lower()} -modifier Resources {config['modifiers']['Resources'].lower()} -modifier Raids {config['modifiers']['Raids'].lower()} -modifier Portals {config['modifiers']['Portals'].lower()}{' -setkey playerevents' if config['extraSettings'].get('playerevents', False) else ''}{' -setkey nobuildcost' if config['extraSettings'].get('nobuildcost', False) else ''}{' -setkey passivemobs' if config['extraSettings'].get('passivemobs', False) else ''}{' -setkey nomap' if config['extraSettings'].get('nomap', False) else ''}
"""

        # 保存批处理文件
        with open('start_server.bat', 'w', encoding='utf-8') as f:
            f.write(batch_content)

    def run(self):
        """运行应用程序"""
        self.window.mainloop()

    def create_tooltip(self, widget, text):
        """为控件创建提示文本"""
        def enter(event):
            # 获取控件的位置
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20
            
            # 创建提示窗口
            self.tooltip = tk.Toplevel()
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
            
            # 添加提示文本
            label = ttk.Label(
                self.tooltip,
                text=text,
                justify='left',
                background="#ffffe0",
                relief='solid',
                borderwidth=1,
                font=("微软雅黑", 9)
            )
            label.pack()

        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
                delattr(self, 'tooltip')

        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)


    def create_name_editor(self, name_frame):
        """创建服务器名称编辑器"""
        # 编辑区域
        edit_frame = ttk.Frame(name_frame)
        edit_frame.pack(fill="x", padx=5, pady=5)

        self.text_input = ttk.Entry(
            edit_frame,
            width=40,
            font=('微软雅黑', 10)
        )
        self.text_input.pack(fill="x", padx=5)
        
        # 添加文本内容
        initial_text = self.config.get("serverName", "我的服务器")
        self.text_input.insert(0, initial_text)

    def toggle_language(self):
        """切换界面语言"""
        self.current_lang = 'en' if self.current_lang == 'cn' else 'cn'
        self.update_language()

    def update_language(self):
        """更新界面语言"""
        lang = self.translations[self.current_lang]
        
        # 更新窗口标题
        self.window.title(lang['window_title'])
        
        # 更新所有框架标题
        self.name_frame.configure(text=lang['server_name_frame'])
        self.basic_frame.configure(text=lang['basic_settings_frame'])
        self.game_frame.configure(text=lang['game_settings_frame'])
        self.extra_frame.configure(text=lang['extra_settings_frame'])

        # 更新基本设置标签
        for frame in self.basic_frame.winfo_children():
            for child in frame.winfo_children():
                if isinstance(child, ttk.Label):
                    current_text = child.cget('text')
                    if "端口号" in current_text or "Port" in current_text:
                        child.configure(text=lang['port_label'])
                    elif "世界名称" in current_text or "World Name" in current_text:
                        child.configure(text=lang['world_name_label'])
                    elif "密码" in current_text or "Password" in current_text:
                        child.configure(text=lang['password_label'])
                    elif "公开服务器" in current_text or "Public Server" in current_text:
                        child.configure(text=lang['public_label'])

        # 更新游戏设置
        label_keys = {
            "Combat": "combat_label",
            "DeathPenalty": "death_penalty_label",
            "Resources": "resources_label",
            "Raids": "raids_label",
            "Portals": "portals_label"
        }

        for modifier, combo in self.setting_combos.items():
            # 更新标签
            combo.master.winfo_children()[0].configure(text=lang[label_keys[modifier]])
            
            # 获取当前值
            current_value = combo.get()
            
            # 更新选项列表
            new_values = self.options_map[modifier][self.current_lang]
            combo.configure(values=new_values)
            
            # 更新当前选中值和说明文字
            if self.current_lang == 'en':
                if current_value in self.cn_to_en_map[modifier]:
                    new_value = self.cn_to_en_map[modifier][current_value]
                    combo.set(new_value)
                    self.setting_labels[modifier].configure(
                        text=self.tooltips[modifier][self.current_lang][new_value]
                    )
            else:
                for cn_val, en_val in self.cn_to_en_map[modifier].items():
                    if en_val == current_value:
                        combo.set(cn_val)
                        self.setting_labels[modifier].configure(
                            text=self.tooltips[modifier][self.current_lang][cn_val]
                        )
                        break

        # 更新额外设置
        extra_label_keys = {
            "nobuildcost": "no_build_cost_label",
            "passivemobs": "passive_mobs_label",
            "playerevents": "player_events_label",
            "nomap": "no_map_label"
        }

        for var_name, check in self.extra_checkbuttons.items():
            # 更新复选框文本
            check.configure(text=lang[extra_label_keys[var_name]])
            # 更新提示文本
            self.create_tooltip(check, self.extra_tooltips[var_name][self.current_lang])

        # 更新按钮文本
        for widget in self.window.winfo_children():
            if isinstance(widget, ttk.Frame):  # 检查按钮框架
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Button):
                        current_text = child.cget('text')
                        if "保存配置" in current_text or "Save Config" in current_text:
                            child.configure(text=lang['save_button'])

    def create_basic_settings(self, frame):
        """创建基本设置"""
        # 初始化变量字典
        self.vars = {}
        
        # 端口号
        port_frame = ttk.Frame(frame)
        port_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(port_frame, text=self.get_text('port_label'), width=15).pack(side="left")
        self.vars["port"] = tk.StringVar(value=self.config.get("port", "17741"))
        port_entry = ttk.Entry(port_frame, textvariable=self.vars["port"], width=25)
        port_entry.pack(side="left", padx=5)
        self.create_tooltip(port_entry, "默认为2456-2458，如果被占用请修改")
        
        # 世界名称
        world_frame = ttk.Frame(frame)
        world_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(world_frame, text=self.get_text('world_name_label'), width=15).pack(side="left")
        self.vars["worldName"] = tk.StringVar(value=self.config.get("worldName", "MyWorld"))
        world_entry = ttk.Entry(world_frame, textvariable=self.vars["worldName"], width=25)
        world_entry.pack(side="left", padx=5)
        self.create_tooltip(world_entry, "这将决定存档文件的名字")
        
        # 密码
        password_frame = ttk.Frame(frame)
        password_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(password_frame, text=self.get_text('password_label'), width=15).pack(side="left")
        self.vars["password"] = tk.StringVar(value=self.config.get("password", "123456"))
        password_entry = ttk.Entry(password_frame, textvariable=self.vars["password"], width=25)
        password_entry.pack(side="left", padx=5)
        self.create_tooltip(password_entry, "必须至少5个字符")
        
        # 公开服务器
        public_frame = ttk.Frame(frame)
        public_frame.pack(fill="x", padx=5, pady=5)
        ttk.Label(public_frame, text=self.get_text('public_label'), width=15).pack(side="left")
        self.vars["public"] = tk.BooleanVar(value=self.config.get("public", True))
        public_check = ttk.Checkbutton(public_frame, variable=self.vars["public"])
        public_check.pack(side="left", padx=5)
        self.create_tooltip(public_check, "是否在服务器列表中公开显示")

    def create_game_settings(self, frame):
        """创建游戏设置"""
        # 初始化修改器变量
        self.modifier_vars = {}
        
        # 中英文映射关系
        self.cn_to_en_map = {
            "Combat": {
                "非常简单": "veryeasy",
                "简单": "easy",
                "困难": "hard",
                "非常困难": "veryhard"
            },
            "DeathPenalty": {
                "休闲": "casual",
                "非常简单": "veryeasy",
                "简单": "easy",
                "困难": "hard",
                "硬核": "hardcore"
            },
            "Resources": {
                "最少(0.5x)": "muchless",
                "较少(0.75x)": "less",
                "较多(1.5x)": "more",
                "很多(2x)": "muchmore",
                "最多(3x)": "most"
            },
            "Raids": {
                "无": "none",
                "最少": "muchless",
                "较少": "less",
                "较多": "more",
                "最多": "muchmore"
            },
            "Portals": {
                "休闲": "casual",
                "困难": "hard",
                "非常困难": "veryhard"
            }
        }

        # 选项的中英文映射
        self.options_map = {
            "Combat": {
                "cn": ["非常简单", "简单", "困难", "非常困难"],
                "en": ["veryeasy", "easy", "hard", "veryhard"]
            },
            "DeathPenalty": {
                "cn": ["休闲", "非常简单", "简单", "困难", "硬核"],
                "en": ["casual", "veryeasy", "easy", "hard", "hardcore"]
            },
            "Resources": {
                "cn": ["最少(0.5x)", "较少(0.75x)", "较多(1.5x)", "很多(2x)", "最多(3x)"],
                "en": ["muchless", "less", "more", "muchmore", "most"]
            },
            "Raids": {
                "cn": ["无", "最少", "较少", "较多", "最多"],
                "en": ["none", "muchless", "less", "more", "muchmore"]
            },
            "Portals": {
                "cn": ["休闲", "困难", "非常困难"],
                "en": ["casual", "hard", "veryhard"]
            }
        }

        # 游戏设置提示文本
        self.tooltips = {
            "Combat": {
                "cn": {
                    "非常简单": "敌人非常弱小",
                    "简单": "敌人较弱",
                    "困难": "敌人较强",
                    "非常困难": "敌人非常强大"
                },
                "en": {
                    "veryeasy": "Enemies are very weak",
                    "easy": "Enemies are weaker",
                    "hard": "Enemies are stronger",
                    "veryhard": "Enemies are very powerful"
                }
            },
            "DeathPenalty": {
                "cn": {
                    "休闲": "死亡无惩罚",
                    "非常简单": "死亡惩罚很小",
                    "简单": "死亡惩罚较小",
                    "困难": "死亡惩罚较重",
                    "硬核": "死亡后丢失所有物品与技能"
                },
                "en": {
                    "casual": "No death penalty",
                    "veryeasy": "Very light death penalty",
                    "easy": "Light death penalty",
                    "hard": "Heavy death penalty",
                    "hardcore": "Lose all items and skills on death"
                }
            },
            "Resources": {
                "cn": {
                    "最少(0.5x)": "正常的资源生成量",
                    "较少(0.75x)": "较少的资源生成",
                    "较多(1.5x)": "更多的资源生成",
                    "很多(2x)": "大量的资源生成",
                    "最多(3x)": "极多的资源生成"
                },
                "en": {
                    "muchless": "Normal resource spawns",
                    "less": "Reduced resource spawns",
                    "more": "Increased resource spawns",
                    "muchmore": "Maximum resource spawns",
                    "most": "Maximum resource spawns"
                }
            },
            "Raids": {
                "cn": {
                    "无": "完全禁用袭击",
                    "最少": "较少的袭击",
                    "较少": "较少的袭击",
                    "较多": "更频繁的袭击",
                    "最多": "非常频繁的袭击"
                },
                "en": {
                    "none": "Raids disabled",
                    "muchless": "Reduced raid frequency",
                    "less": "Reduced raid frequency",
                    "more": "Increased raid frequency",
                    "muchmore": "Maximum raid frequency"
                }
            },
            "Portals": {
                "cn": {
                    "休闲": "可以携带矿石传送",
                    "困难": "正常的传送门规则",
                    "非常困难": "禁用传送门"
                },
                "en": {
                    "casual": "Allow ore teleportation",
                    "hard": "Normal portal rules",
                    "veryhard": "Portals disabled"
                }
            }
        }

        # 创建游戏设置控件
        settings = [
            ("combat_label", "Combat"),
            ("death_penalty_label", "DeathPenalty"),
            ("resources_label", "Resources"),
            ("raids_label", "Raids"),
            ("portals_label", "Portals")
        ]
        
        self.setting_combos = {}  # 存储所有下拉框的引用
        self.setting_labels = {}  # 存储说明文字标签的引用
        
        for label_key, modifier in settings:
            setting_frame = ttk.Frame(frame)
            setting_frame.pack(fill="x", padx=5, pady=5)
            
            # 添加设置标签
            ttk.Label(setting_frame, text=self.get_text(label_key), width=15).pack(side="left")
            
            # 添加下拉框
            var = tk.StringVar(value=self.options_map[modifier]["cn"][0])
            self.modifier_vars[modifier] = var
            combo = ttk.Combobox(
                setting_frame, 
                textvariable=var, 
                values=self.options_map[modifier]["cn"], 
                state="readonly", 
                width=25
            )
            combo.pack(side="left", padx=5)
            self.setting_combos[modifier] = combo
            
            # 添加说明文字标签
            desc_label = ttk.Label(
                setting_frame,
                text=self.tooltips[modifier][self.current_lang][self.options_map[modifier]["cn"][0]],
                width=30
            )
            desc_label.pack(side="left", padx=5)
            self.setting_labels[modifier] = desc_label
            
            # 更新说明文字的回调函数
            def create_update_description(combo, modifier, label):
                def update_description(event):
                    value = combo.get()
                    tooltips = self.tooltips[modifier][self.current_lang]
                    if value in tooltips:
                        label.configure(text=tooltips[value])
                return update_description
            
            combo.bind('<<ComboboxSelected>>', create_update_description(combo, modifier, desc_label))

    def create_extra_settings(self, frame):
        """创建额外设置"""
        # 初始化额外设置变量
        self.extra_vars = {}
        
        # 创建复选框
        self.extra_tooltips = {
            "nobuildcost": {
                "cn": "启用后建造不消耗材料",
                "en": "No resource cost for building when enabled"
            },
            "passivemobs": {
                "cn": "启用后生物不主动攻击",
                "en": "Creatures won't attack unless provoked"
            },
            "playerevents": {
                "cn": "启用后袭击由玩家触发",
                "en": "Raids are triggered by player actions"
            },
            "nomap": {
                "cn": "启用后禁用地图",
                "en": "Disables the map when enabled"
            }
        }
        
        settings = [
            ("no_build_cost_label", "nobuildcost"),
            ("passive_mobs_label", "passivemobs"),
            ("player_events_label", "playerevents"),
            ("no_map_label", "nomap")
        ]
        
        self.extra_checkbuttons = {}  # 存储复选框引用
        
        for label_key, var_name in settings:
            var = tk.BooleanVar(value=False)
            self.extra_vars[var_name] = var
            check = ttk.Checkbutton(
                frame,
                text=self.get_text(label_key),
                variable=var,
                padding=5
            )
            check.pack(fill="x", padx=10, pady=2)
            self.extra_checkbuttons[var_name] = check  # 保存复选框引用
            self.create_tooltip(check, self.extra_tooltips[var_name]["cn"])

        # 创建按钮框架
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=10)

        # 保存配置按钮
        save_button = ttk.Button(
            button_frame,
            text=self.get_text('save_button'),
            command=self.save_config,
            width=15
        )
        save_button.pack(side="left", padx=10)

if __name__ == "__main__":
    app = ValheimServerConfig()
    app.run() 