import os
import json
import re
import tkinter as tk
from tkinter import messagebox, ttk
class Player:
    def __init__(self, username, password, security_question, security_answer,
                 classic_time=None, classic_score=None, classic_rank=None,
                 max_level=None, stars=None, total_stars=0, achievements=None):
        self.username = username
        self.password = password
        self.security_question = security_question
        self.security_answer = security_answer
        self.score = {
            "classic": {
                "time": classic_time,
                "score": classic_score,
                "rank": classic_rank
            },
            "level_mode": {
                "max_level": max_level,
                "stars": stars if stars else {str(i): None for i in range(1, 6)},
                "total_stars": total_stars
            }
        }
        self.achievements = achievements if achievements else {}

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "security_question": self.security_question,
            "security_answer": self.security_answer,
            "score": self.score,
            "achievements": self.achievements
        }

    @staticmethod
    def from_dict(data):
        score = data.get("score", {})
        level_mode = score.get("level_mode", {})
        return Player(
            username=data["username"],
            password=data["password"],
            security_question=data["security_question"],
            security_answer=data["security_answer"],
            classic_time=score.get("classic", {}).get("time"),
            classic_score=score.get("classic", {}).get("score"),
            classic_rank=score.get("classic", {}).get("rank"),
            max_level=level_mode.get("max_level"),
            stars=level_mode.get("stars", {str(i): None for i in range(1, 6)}),
            total_stars=level_mode.get("total_stars", 0),
            achievements=data.get("achievements", {})
        )


class PlayerDataManager:
    def __init__(self, filename="player_data.json"):
        self.filename = filename
        self.players = self.load_data()

    def load_data(self):
        if not os.path.exists(self.filename):
            return {}
        with open(self.filename, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            return {
                username: Player.from_dict(data)
                for username, data in raw_data.items()
            }

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump({u: p.to_dict() for u, p in self.players.items()}, f, indent=2, ensure_ascii=False)

    def is_username_taken(self, username):
        return username in self.players

    def is_valid_password(self, password):
        return len(password) >= 8 and re.search(r"[A-Za-z]", password) and re.search(r"[0-9]", password)

    def register_player(self, username, password, confirm_password, question, answer):
        if self.is_username_taken(username):
            return False, "帳號已存在"
        if password != confirm_password:
            return False, "兩次密碼不一致"
        if not self.is_valid_password(password):
            return False, "密碼需至少8位，並包含英文字母與數字"

        self.players[username] = Player(username, password, question, answer)
        self.save_data()
        return True, "註冊成功"

    def verify_login(self, username, password):
        if username not in self.players:
            return False, "此帳號不存在，請先註冊"
        elif self.players[username].password != password:
            return False, "密碼錯誤，請重試"
        else:
            return True, self.players[username]
        
    def verify_security_answer(self, username, answer):
        if username in self.players and self.players[username].security_answer == answer:
            return True
        return False

    def reset_password(self, username, new_password):
        if username in self.players:
            self.players[username].password = new_password
            self.save_data()
            return True
        return False


    def update_classic_score(self, username, time=None, score=None, rank=None):
        if username in self.players:
            player = self.players[username]
        if time is not None:
            player.score["classic"]["time"] = time
        if score is not None:
            player.score["classic"]["score"] = score
        if rank is not None:
            player.score["classic"]["rank"] = rank
        self.save_data()

# UI 部分
manager = PlayerDataManager()
current_user = None

root = tk.Tk()
root.title("登入系統")
root.geometry("300x250")

def login():
    global current_user
    username = login_username.get().strip()
    password = login_password.get().strip()
    success, result = manager.verify_login(username, password)
    if success:
        current_user = username
        messagebox.showinfo("登入成功", f"歡迎回來，{username}！")
        root.destroy()
    else:
        messagebox.showerror("登入失敗", result)

def register():
    username = reg_username.get().strip()
    pw = reg_password.get().strip()
    confirm_pw = reg_confirm_password.get().strip()
    question = reg_question.get()
    answer = reg_answer.get().strip()
    success, msg = manager.register_player(username, pw, confirm_pw, question, answer)

    if success:
        messagebox.showinfo("註冊成功", msg)
        reg_window.destroy()
    else:
        messagebox.showerror("註冊失敗", msg)

def open_register_window():
    global reg_window, reg_username, reg_password, reg_confirm_password, reg_question, reg_answer
    reg_window = tk.Toplevel(root)
    reg_window.title("註冊")
    reg_window.geometry("300x300")

    tk.Label(reg_window, text="帳號：").pack()
    reg_username = tk.Entry(reg_window)
    reg_username.pack()

    tk.Label(reg_window, text="密碼：").pack()
    reg_password = tk.Entry(reg_window, show="*")
    reg_password.pack()

    tk.Label(reg_window, text="確認密碼：").pack()
    reg_confirm_password = tk.Entry(reg_window, show="*")
    reg_confirm_password.pack()

    tk.Label(reg_window, text="安全提問").pack()
    reg_question = ttk.Combobox(reg_window, values=["我的生日是什麼？", "我父親/母親的名字是？", "我使用的手機品牌是？"])
    reg_question.current(0)
    reg_question.pack()

    tk.Label(reg_window, text="答案：").pack()
    reg_answer = tk.Entry(reg_window)
    reg_answer.pack()

    tk.Label(reg_window, text="* 密碼需至少8位，包含英文字母與數字", fg="gray").pack(pady=5)
    tk.Button(reg_window, text="註冊", command=register).pack(pady=10)
    
def open_forgot_window():
    def check_account():
        user = fg_username.get().strip()
        if user not in manager.players:
            messagebox.showerror("錯誤", "帳號不存在")
            return
        fg_question.config(text=manager.players[user].security_question)
        fg_next_btn.config(state="normal")

    def reset_password():
        user = fg_username.get().strip()
        answer = fg_answer.get().strip()
        new_pw = fg_new_pw.get().strip()
        if not manager.is_valid_password(new_pw):
            messagebox.showerror("錯誤", "密碼格式不正確")
            return
        if manager.verify_security_answer(user, answer):
            manager.reset_password(user, new_pw)
            messagebox.showinfo("成功", "密碼已更新")
            forgot_window.destroy()
        else:
            messagebox.showerror("錯誤", "答案錯誤")

    forgot_window = tk.Toplevel(root)
    forgot_window.title("忘記密碼")
    forgot_window.geometry("300x300")

    tk.Label(forgot_window, text="帳號").pack()
    fg_username = tk.Entry(forgot_window)
    fg_username.pack()

    tk.Button(forgot_window, text="確認帳號", command=check_account).pack()

    fg_question = tk.Label(forgot_window, text="")
    fg_question.pack()

    tk.Label(forgot_window, text="答案").pack()
    fg_answer = tk.Entry(forgot_window)
    fg_answer.pack()

    tk.Label(forgot_window, text="新密碼").pack()
    fg_new_pw = tk.Entry(forgot_window)
    fg_new_pw.pack()

    fg_next_btn = tk.Button(forgot_window, text="重設密碼", state="disabled", command=reset_password)
    fg_next_btn.pack(pady=5)

# 主視窗內容

tk.Label(root, text="帳號：").pack()
login_username = tk.Entry(root)
login_username.pack()

tk.Label(root, text="密碼：").pack()
login_password = tk.Entry(root, show="*")
login_password.pack()

show_pw_var = tk.BooleanVar()
tk.Checkbutton(root, text="顯示密碼", variable=show_pw_var, command=lambda: login_password.config(show="" if show_pw_var.get() else "*")).pack()

tk.Button(root, text="登入", command=login).pack(pady=5)
tk.Button(root, text="註冊新帳號", command=open_register_window).pack()
tk.Button(root, text="忘記密碼", command=open_forgot_window).pack(pady=5)

root.mainloop()