import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import shutil
import threading
import sys
from datetime import datetime

# Unified 6-digit hex palette system
THEME_PALETTES = {
    "Night Blue": {
        "Background": "#0f172a",
        "Sidebar": "#1e293b",
        "Accent": "#38bdf8",
        "Text": "#f1f5f9",
        "Border": "#334155",
        "Hover": "#245fa8"
    },
    "Forest Green": {
        "Background": "#062016",
        "Sidebar": "#0a3121",
        "Accent": "#2ecc71",
        "Text": "#ecf0f1",
        "Border": "#196247",
        "Hover": "#38d39f"
    },
    "Soft Gray": {
        "Background": "#f8fafc",
        "Sidebar": "#f1f5f9",
        "Accent": "#64748b",
        "Text": "#1e293b",
        "Border": "#e2e8f0",
        "Hover": "#cbd5e1"
    },
    "Royal Purple": {
        "Background": "#1a1033",
        "Sidebar": "#26174d",
        "Accent": "#a855f7",
        "Text": "#faf5ff",
        "Border": "#643ebc",
        "Hover": "#d6a9fb"
    }
}

CONFIG_FILE = "config.json"

ICON_UNICODES = {
    "dashboard": "\uf0e4",
    "organize": "\uf187",
    "report": "\uf201",
    "settings": "\u2699",
    "folder": "\uf07b",
    "sparkle": "\uf005",
    "archive": "\uf187"
}

LANGUAGES = {
    "en": {
        "Dashboard": "Dashboard",
        "Organize Files": "Organize Files",
        "View Reports": "View Reports",
        "Settings": "Settings",
        "Select Folder": "Select Folder",
        "Start Organizing": "Start Organizing",
        "AI Search...": "AI Search...",
        "AI Suggestion:": "AI Suggestion:",
        "Move": "Move",
        "Status Ready": "Status: Ready",
        "Status Moving": "Status: Organizing files...",
        "Status Finished": "Status: Finished",
        "Language": "Language",
        "Theme": "Theme",
        "Night Blue": "Night Blue",
        "Forest Green": "Forest Green",
        "Soft Gray": "Soft Gray",
        "Royal Purple": "Royal Purple",
        "English": "English",
        "Arabic": "Arabic",
        "Spanish": "Español",
        "File Organization System": "File Organization System",
        "Please select a folder first.": "Please select a folder first.",
        "Progress": "Progress",
        "Done!": "Done!",
        "Reports will appear here.": "Reports will appear here.",
        "Step1": "Pick your messy folder",
        "Step2": "We'll create a beautifully organized archive for your files.",
        "Step3": "Press Start Organizing and relax.",
        "Welcome": "Welcome! Please choose your language:"
    },
    "ar": {
        "Dashboard": "لوحة التحكم",
        "Organize Files": "تنظيم الملفات",
        "View Reports": "عرض التقارير",
        "Settings": "الإعدادات",
        "Select Folder": "اختر المجلد",
        "Start Organizing": "ابدأ التنظيم",
        "AI Search...": "بحث الذكاء الاصطناعي...",
        "AI Suggestion:": "اقتراح الذكاء الاصطناعي:",
        "Move": "ابدأ التنظيم",
        "Status Ready": "الحالة: جاهز",
        "Status Moving": "الحالة: جاري تنظيم الملفات...",
        "Status Finished": "الحالة: اكتمل التنظيم",
        "Language": "اللغة",
        "Theme": "المظهر",
        "Night Blue": "أزرق ليلي",
        "Forest Green": "أخضر غابة",
        "Soft Gray": "رمادي فاتح",
        "Royal Purple": "أرجواني ملكي",
        "English": "الإنجليزية",
        "Arabic": "العربية",
        "Spanish": "الإسبانية",
        "File Organization System": "نظام تنظيم الملفات",
        "Please select a folder first.": "يرجى اختيار مجلد أولاً.",
        "Progress": "التقدم",
        "Done!": "تم!",
        "Reports will appear here.": "ستظهر التقارير هنا.",
        "Step1": "اختر مجلد الفوضى لديك",
        "Step2": "سننشئ لك أرشيفًا منظمًا بشكل جميل!",
        "Step3": "اضغط ابدأ التنظيم واسترخ.",
        "Welcome": "مرحبًا! اختر لغتك:"
    },
    "es": {
        "Dashboard": "Panel",
        "Organize Files": "Organizar archivos",
        "View Reports": "Ver informes",
        "Settings": "Configuración",
        "Select Folder": "Seleccionar carpeta",
        "Start Organizing": "Comenzar a organizar",
        "AI Search...": "Buscar con IA...",
        "AI Suggestion:": "Sugerencia de IA:",
        "Move": "Comenzar a organizar",
        "Status Ready": "Estado: Listo",
        "Status Moving": "Estado: Organizando archivos...",
        "Status Finished": "Estado: Terminado",
        "Language": "Idioma",
        "Theme": "Tema",
        "Night Blue": "Azul Noche",
        "Forest Green": "Verde Bosque",
        "Soft Gray": "Gris Suave",
        "Royal Purple": "Púrpura Real",
        "English": "Inglés",
        "Arabic": "Árabe",
        "Spanish": "Español",
        "File Organization System": "Sistema de organización de archivos",
        "Please select a folder first.": "Por favor seleccione una carpeta primero.",
        "Progress": "Progreso",
        "Done!": "¡Hecho!",
        "Reports will appear here.": "Los informes aparecerán aquí.",
        "Step1": "Elige tu carpeta desordenada",
        "Step2": "Creamos un archivo bellamente organizado para tus archivos.",
        "Step3": "Presiona Comenzar a organizar y relájate.",
        "Welcome": "¡Bienvenido! Por favor, elige tu idioma:"
    }
}

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8-sig") as f:
        json.dump(config, f, ensure_ascii=False)

def show_welcome_select_language():
    root = tk.Tk()
    root.withdraw()
    window = tk.Toplevel()
    window.title("Welcome — File Organizer")
    window.geometry("420x280")
    window.configure(bg="#eaf0f9")
    window.grab_set()
    selected_lang = {'value': None}
    def select(lang_code):
        selected_lang['value'] = lang_code
        window.destroy()
    btn_font = ("Segoe UI", 18, "bold")
    info = tk.Label(window, text=LANGUAGES["en"]["Welcome"], font=("Segoe UI", 14, "bold"), bg="#eaf0f9")
    info.pack(pady=(24,18))
    btn_ar = tk.Button(window, text="العربية", font=btn_font, bg="#1e293b", fg="#f1f5f9", width=20, height=2, bd=0, command=lambda: select("ar"))
    btn_en = tk.Button(window, text="English", font=btn_font, bg="#1e293b", fg="#f1f5f9", width=20, height=2, bd=0, command=lambda: select("en"))
    btn_es = tk.Button(window, text="Español", font=btn_font, bg="#1e293b", fg="#f1f5f9", width=20, height=2, bd=0, command=lambda: select("es"))
    btn_ar.pack(pady=6)
    btn_en.pack(pady=6)
    btn_es.pack(pady=6)
    window.protocol("WM_DELETE_WINDOW", window.destroy)
    window.wait_window()
    try: root.destroy()
    except: pass
    return selected_lang["value"]

def load_config():
    if not os.path.exists(CONFIG_FILE):
        lang = show_welcome_select_language()
        if lang is None:
            sys.exit(0)
        config = {"language": lang, "theme": "Night Blue"}
        save_config(config)
        return config
    with open(CONFIG_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)

class Translator:
    def __init__(self, config=None):
        if config is None:
            config = load_config()
        self.config = config
        self.language = self.config.get("language", "en")
    def t(self, text):
        lang_dict = LANGUAGES.get(self.language, LANGUAGES["en"])
        return lang_dict.get(text, text)
    def set_language(self, lang):
        self.language = lang
        self.config["language"] = lang
        save_config(self.config)

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, app, translator):
        super().__init__(master)
        self.app = app
        self.translator = translator
        self.selected_idx = 0
        self.palette = self.app.palette
        self.build_ui()
        # Ensure sidebar can't shrink too much
        self.grid_propagate(False)
    def build_ui(self):
        for child in self.winfo_children():
            child.destroy()
        self.palette = self.app.palette
        right = self.translator.language == "ar"
        items = [
            (ICON_UNICODES["dashboard"], "Dashboard", self.on_dashboard),
            (ICON_UNICODES["organize"], "Organize Files", self.on_organize),
            (ICON_UNICODES["report"], "View Reports", self.on_reports)
        ]
        for i, (icon, label, command) in enumerate(items):
            txt = f"{self.translator.t(label)}  {icon}" if right else f"{icon}  {self.translator.t(label)}"
            anchor = "e" if right else "w"
            text_color = self.palette["Accent"] if i == self.selected_idx else self.palette["Text"]
            border_color = self.palette["Accent"] if i == self.selected_idx else self.palette["Sidebar"]
            btn = ctk.CTkButton(
                self, text=txt,
                font=ctk.CTkFont('FontAwesome', 16),
                anchor=anchor,
                fg_color="transparent",
                text_color=text_color,
                corner_radius=12,
                border_width=4 if i == self.selected_idx else 0,
                border_color=border_color,
                hover_color=self.palette["Hover"],
                height=48,
                command=lambda idx=i, fn=command: self.on_select(idx, fn)
            )
            pady = (10, 8) if i == 0 else (0,8)
            btn.grid(row=i, column=0, sticky="ew", padx=(10,10), pady=pady)
        self.grid_rowconfigure(len(items), weight=1)
        gear_txt = f"{self.translator.t('Settings')}  {ICON_UNICODES['settings']}" if right else f"{ICON_UNICODES['settings']}  {self.translator.t('Settings')}"
        gear_btn = ctk.CTkButton(
            self, text=gear_txt, anchor=anchor,
            font=ctk.CTkFont('Segoe UI', 16),
            fg_color="transparent", corner_radius=12,
            height=44, text_color=self.palette["Accent"], hover_color=self.palette["Hover"],
            border_width=0, command=self.app.open_settings
        )
        gear_btn.grid(row=len(items)+1, column=0, sticky="ew", padx=(10,10), pady=(0,18))
        self.configure(fg_color=self.palette["Sidebar"])
        # Responsive sidebar: NO window sizing/minsize here!
        self.update_idletasks()
        # Removed: self.minsize(180, min(220, self.winfo_height()))
    def on_select(self, idx, fn):
        self.selected_idx = idx
        self.build_ui()
        fn()
    def refresh_language(self):
        self.build_ui()
    def update_theme(self):
        self.build_ui()
    def on_dashboard(self): self.app.set_page("dashboard")
    def on_organize(self): self.app.set_page("organize")
    def on_reports(self): self.app.set_page("reports")

class StatusBar(ctk.CTkFrame):
    def __init__(self, master, app, translator):
        super().__init__(master)
        self.app = app
        self.translator = translator
        self.palette = self.app.palette
        right = self.translator.language == "ar"
        anchor = "e" if right else "w"
        self.text = ctk.CTkLabel(self, text=self.translator.t("Status Ready"),
            anchor=anchor, text_color=self.palette["Accent"], font=ctk.CTkFont("Segoe UI", 12))
        self.text.pack(side="right" if right else "left", padx=12)
        self.configure(height=28, fg_color=self.palette["Sidebar"])
    def set_status(self, msg):
        self.text.configure(text=msg)
    def refresh_language(self):
        right = self.translator.language == "ar"
        anchor = "e" if right else "w"
        self.text.configure(anchor=anchor, text=self.translator.t("Status Ready"), text_color=self.palette["Accent"])
        self.text.pack_configure(side="right" if right else "left")
        self.configure(fg_color=self.palette["Sidebar"])

class ProgressBar(ctk.CTkFrame):
    def __init__(self, master, app, translator):
        super().__init__(master)
        self.app = app
        self.translator = translator
        self.palette = self.app.palette
        right = self.translator.language == "ar"
        anchor = "e" if right else "w"
        self.label = ctk.CTkLabel(self, text=f"{self.translator.t('Progress')}:", font=ctk.CTkFont('Segoe UI', 12),
                                  anchor=anchor, text_color=self.palette["Accent"])
        self.bar = ctk.CTkProgressBar(self, orientation="horizontal", height=10, width=210,
                                      progress_color=self.palette["Accent"], fg_color=self.palette["Border"])
        if right:
            self.label.pack(side="right", padx=12)
            self.bar.pack(side="right", padx=8, pady=8)
        else:
            self.label.pack(side="left", padx=12)
            self.bar.pack(side="left", padx=8, pady=8)
        self.pack_propagate(0)
        self.set(0)
        self.configure(fg_color="transparent")
    def set(self, val): self.bar.set(val)
    def refresh_language(self):
        self.label.configure(text=f"{self.translator.t('Progress')}:",
                             text_color=self.palette["Accent"])
        self.bar.configure(progress_color=self.palette["Accent"], fg_color=self.palette["Border"])

class DashboardPage(ctk.CTkFrame):
    def __init__(self, master, app, translator):
        super().__init__(master, fg_color=app.palette["Background"])
        self.app = app
        self.translator = translator
        self.bigicons_font = ctk.CTkFont('FontAwesome', 48)
        self.build_infographic()
    def build_infographic(self):
        for w in self.winfo_children():
            w.destroy()
        pal = self.app.palette
        right = self.translator.language == "ar"
        bigframe = ctk.CTkFrame(self, fg_color=pal["Sidebar"], corner_radius=18, border_color=pal["Border"], border_width=2)
        bigframe.pack(expand=True, pady=36, padx=60, fill="both")
        steps = [
            (ICON_UNICODES["folder"], self.translator.t("Step1")),
            (ICON_UNICODES["archive"], self.translator.t("Step2")),
            (ICON_UNICODES["sparkle"], self.translator.t("Step3"))
        ]
        for i, (icon, txt) in enumerate(steps):
            row = ctk.CTkFrame(bigframe, fg_color="transparent")
            row.pack(pady=(18,7), padx=32)
            ic = ctk.CTkLabel(row, text=icon, font=self.bigicons_font, text_color=pal["Accent"])
            ic.pack(side="left" if not right else "right", padx=(0,18) if not right else (18,0))
            desc = ctk.CTkLabel(row, text=txt, font=ctk.CTkFont('Segoe UI Semibold', 21),
                                text_color=pal["Text"], anchor=("e" if right else "w"))
            desc.pack(side="left" if not right else "right")
    def refresh_language(self):
        self.build_infographic()

class ReportsPage(ctk.CTkFrame):
    def __init__(self, master, app, translator, get_logs_func=None):
        super().__init__(master, fg_color=app.palette["Background"])
        self.app = app
        self.translator = translator
        self.get_logs_func = get_logs_func
        pal = self.app.palette
        right = self.translator.language == "ar"
        anchor = "e" if right else "w"
        self.label = ctk.CTkLabel(
            self,
            text=self.translator.t("View Reports"),
            font=ctk.CTkFont('Segoe UI Bold', 21),
            text_color=pal["Accent"],
            anchor=anchor
        )
        self.label.pack(pady=24)
        self.report_area = ctk.CTkTextbox(
            self, height=280, font=ctk.CTkFont("Consolas", 14),
            fg_color=pal["Sidebar"], text_color=pal["Text"],
            border_color=pal["Border"], border_width=1, wrap="word", state="disabled"
        )
        self.report_area.pack(fill="both", expand=True, padx=18, pady=18)
        self.refresh_report_content()
    def refresh_report_content(self):
        pal = self.app.palette
        self.report_area.configure(state="normal")
        self.report_area.delete("1.0", "end")
        logs = []
        if self.get_logs_func is not None:
            logs = self.get_logs_func()
        if not logs:
            self.report_area.insert("end", f"{self.translator.t('Reports will appear here.')}")
        else:
            # direct text insertion, no tags, no justify
            self.report_area.insert("end", "\n".join(str(ln) for ln in logs))
        self.report_area.configure(state="disabled")
        self.report_area.configure(fg_color=pal["Sidebar"], border_color=pal["Border"], text_color=pal["Text"])
    def refresh_language(self):
        pal = self.app.palette
        self.label.configure(text=self.translator.t("View Reports"), text_color=pal["Accent"])
        self.report_area.configure(fg_color=pal["Sidebar"], border_color=pal["Border"], text_color=pal["Text"])
        self.refresh_report_content()

class OrganizeFilesPage(ctk.CTkFrame):
    def __init__(self, master, app, translator, status_bar, progress_bar, add_log_callback=None, update_reports_callback=None):
        super().__init__(master, fg_color=app.palette["Background"])
        self.app = app
        self.translator = translator
        self.status_bar = status_bar
        self.progress_bar = progress_bar
        self.add_log_callback = add_log_callback
        self.update_reports_callback = update_reports_callback
        self.palette = self.app.palette
        self.selected_folder = tk.StringVar()
        self.folder_btn = None
        self.folder_label = None
        self.move_btn = None
        self.build_ui()
    def build_ui(self):
        for w in self.winfo_children():
            w.destroy()
        pal = self.palette = self.app.palette
        right = self.translator.language == "ar"
        self.folder_frame = ctk.CTkFrame(self, fg_color=pal["Sidebar"], border_color=pal["Border"], border_width=1)
        self.folder_frame.pack(fill="x", padx=60, pady=(50, 14))
        label_kwargs = {"wraplength": 420, "font": ctk.CTkFont('Segoe UI', 15), "text_color":pal["Text"]}
        btn_kwargs = {"height":40, "corner_radius":12, "border_width":1, "border_color":pal["Accent"], "fg_color":"transparent",
                      "text_color":pal["Text"], "hover_color":pal["Hover"], "font":ctk.CTkFont("Segoe UI", 15)}
        if right:
            self.folder_label = ctk.CTkLabel(self.folder_frame, text="", anchor="e", **label_kwargs)
            self.folder_label.pack(side="right", fill="x", expand=True, padx=(0,10))
            self.folder_btn = ctk.CTkButton(self.folder_frame, text=self.translator.t("Select Folder"), command=self.select_folder, **btn_kwargs)
            self.folder_btn.pack(side="right", padx=(10,0), pady=8)
        else:
            self.folder_btn = ctk.CTkButton(self.folder_frame, text=self.translator.t("Select Folder"), command=self.select_folder, **btn_kwargs)
            self.folder_btn.pack(side="left", padx=(0,10), pady=8)
            self.folder_label = ctk.CTkLabel(self.folder_frame, text="", anchor="w", **label_kwargs)
            self.folder_label.pack(side="left", fill="x", expand=True, padx=(10,0))
        # Single, large, professional "Start Organizing" button
        move_btn_kwargs = dict(
            text=self.translator.t("Start Organizing"),
            height=80,
            fg_color=pal["Accent"],
            hover_color=pal["Hover"],
            font=ctk.CTkFont("Segoe UI Bold",28),
            corner_radius=16,
            border_width=1,
            border_color=pal["Accent"],
            text_color=pal["Text"],
            command=self.organize_files,
        )
        self.move_btn = ctk.CTkButton(self, **move_btn_kwargs)
        self.move_btn.pack(padx=110, pady=(34,30), anchor="center", expand=True)
        # Set label if folder was chosen previously
        if self.selected_folder.get():
            self.folder_label.configure(text=self.selected_folder.get())
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder.set(folder)
            self.folder_label.configure(text=folder)
    def organize_files(self):
        folder = self.selected_folder.get()
        if not folder:
            messagebox.showerror(self.translator.t("Organize Files"), self.translator.t("Please select a folder first."))
            return
        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        if not files:
            messagebox.showinfo(self.translator.t("Organize Files"), "No files found in the folder.")
            return
        total = len(files)
        self.status_bar.set_status(self.translator.t("Status Moving"))
        self.progress_bar.set(0)
        def do_organize():
            dt = datetime.now().strftime('%d_%b')
            master_folder = os.path.join(folder, f"Organized_Archive_{dt}")
            if not os.path.exists(master_folder):
                os.makedirs(master_folder)
            folders = {
                "Photos_Gallery": ['jpg','jpeg','png','gif','bmp'],
                "Videos_Hub": ['mp4','avi','mkv','mov','mpeg'],
                "Audio_Studio": ['mp3','wav','flac','ogg','aac'],
                "Documents_Archive": ['pdf','docx','txt','xlsx','pptx','doc'],
                "Compressed_Backups": ['zip','rar','tar','gz','7z']
            }
            for sub in folders:
                path = os.path.join(master_folder, sub)
                if not os.path.exists(path):
                    os.makedirs(path)
            others_path = os.path.join(master_folder, "Others")
            if not os.path.exists(others_path): os.makedirs(others_path)
            count = {k:0 for k in folders}
            count["Others"] = 0
            for idx, filename in enumerate(files):
                try:
                    ext = os.path.splitext(filename)[1][1:].lower()
                    found = False
                    for group, exts in folders.items():
                        if ext in exts:
                            dest_folder = os.path.join(master_folder, group)
                            found = True
                            break
                    if not found:
                        dest_folder = others_path
                    basename, extension = os.path.splitext(filename)
                    destfile = os.path.join(dest_folder, filename)
                    ctr = 1
                    while os.path.exists(destfile):
                        destfile = os.path.join(dest_folder, f"{basename}_{ctr}{extension}")
                        ctr += 1
                    shutil.move(os.path.join(folder, filename), destfile)
                    key = group if found else "Others"
                    count[key] += 1
                    now = datetime.now()
                    dtstamp = now.strftime('%Y-%m-%d %H:%M:%S')
                    log_str = f"[{dtstamp}] - {filename} → /{os.path.relpath(destfile, folder)}"
                    if self.add_log_callback: self.add_log_callback(log_str)
                except Exception as ex:
                    now = datetime.now()
                    dtstamp = now.strftime('%Y-%m-%d %H:%M:%S')
                    log_str = f"[{dtstamp}] - ERROR: Could not move {filename}: {ex}"
                    if self.add_log_callback: self.add_log_callback(log_str)
                self.progress_bar.set((idx+1)/total)
            self.status_bar.set_status(self.translator.t("Status Finished"))
            parts = []
            for key in folders:
                if count[key]:
                    parts.append(f"{count[key]} {key.replace('_',' ')}")
            if count["Others"]:
                parts.append(f"{count['Others']} Others")
            summary = self.translator.t("Done!") + " " + (", ".join(parts) if self.translator.language != "ar" else "، ".join(parts))
            messagebox.showinfo(self.translator.t("Organize Files"), summary)
            self.progress_bar.set(1.0)
            if self.update_reports_callback:
                self.update_reports_callback()
        threading.Thread(target=do_organize, daemon=True).start()
    def refresh_language(self):
        self.palette = self.app.palette
        self.build_ui()

class SettingsPage(ctk.CTkFrame):
    def __init__(self, master, app, translator):
        super().__init__(master, fg_color=app.palette["Background"])
        self.app = app
        self.translator = translator
        self.palette = self.app.palette
        self.build_ui()
    def build_ui(self):
        for w in self.winfo_children():
            w.destroy()
        pal = self.app.palette
        right = self.translator.language == "ar"
        anchor = "e" if right else "w"
        title = ctk.CTkLabel(self, text=self.translator.t("Settings"),
                             font=ctk.CTkFont('Segoe UI Bold', 24),
                             text_color=pal["Accent"], anchor=anchor)
        title.pack(pady=24)
        lang_label = ctk.CTkLabel(self, text=self.translator.t("Language"),
                                  font=ctk.CTkFont("Segoe UI", 15),
                                  text_color=pal["Accent"], anchor=anchor)
        lang_label.pack(pady=(10,5), anchor=anchor)
        lang_frame = ctk.CTkFrame(self, fg_color="transparent")
        lang_frame.pack(pady=2, anchor=anchor)
        langs = [("en", LANGUAGES["en"]["English"]), ("ar", LANGUAGES["ar"]["Arabic"]), ("es", LANGUAGES["es"]["Spanish"])]
        for code, name in (reversed(langs) if right else langs):
            btn = ctk.CTkButton(lang_frame, text=name, width=140, height=38,
                                command=lambda c=code: self.change_lang(c),
                                fg_color="transparent",
                                text_color=pal["Text"],
                                hover_color=pal["Hover"],
                                border_color=pal["Accent"],
                                border_width=1,
                                corner_radius=12,
                                font=ctk.CTkFont("Segoe UI", 15),
                                anchor=anchor)
            btn.pack(side="right" if right else "left", padx=10)
        theme_label = ctk.CTkLabel(self, text=self.translator.t("Theme"),
                                   font=ctk.CTkFont("Segoe UI", 15),
                                   text_color=pal["Accent"], anchor=anchor)
        theme_label.pack(pady=(28,5), anchor=anchor)
        theme_var = tk.StringVar(value=self.app.theme)
        theme_menu = ctk.CTkOptionMenu(
            self, variable=theme_var,
            values=list(THEME_PALETTES.keys()),
            command=self.change_theme,
            fg_color=pal["Sidebar"], text_color=pal["Text"], width=200,
            button_color=pal["Accent"], button_hover_color=pal["Hover"],
            font=ctk.CTkFont("Segoe UI", 15)
        )
        theme_menu.pack(pady=(0, 22), anchor=anchor)
        theme_var.set(self.app.theme)
    def change_lang(self, lang_code):
        self.app.translator.set_language(lang_code)
        self.app.config["language"] = lang_code
        save_config(self.app.config)
        self.app.refresh_language()
    def change_theme(self, theme_name):
        self.app.change_theme(theme_name)
    def refresh_language(self):
        self.palette = self.app.palette
        self.build_ui()

class FileOrganizerApp(ctk.CTk):
    def __init__(self):
        self.config = load_config()
        self.theme = self.config.get("theme", "Night Blue")
        self.palette = THEME_PALETTES.get(self.theme, THEME_PALETTES["Night Blue"])
        if self.theme == "Soft Gray":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
        super().__init__()
        self.title("File Organization System")
        self.geometry("940x600")
        self.resizable(True, True)
        self.state('zoomed')
        self.translator = Translator(self.config)
        self.history_logs = []

        # --- Begin grid layout configuration ---
        # Set up a grid with 2 columns and 3 rows (main+bars)
        self.grid_rowconfigure(0, weight=1)   # main area row grows
        self.grid_rowconfigure(1, weight=0)   # status bar fixed
        self.grid_rowconfigure(2, weight=0)   # progress bar fixed
        self.grid_columnconfigure(0, weight=0, minsize=180)  # Sidebar fixed width
        self.grid_columnconfigure(1, weight=1)  # Main content expands
        # --- End grid layout configuration ---

        # Sidebar - fixed width, sticky north/south
        self.sidebar = Sidebar(self, self, self.translator)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        self.sidebar.update_idletasks()
        # Removed: self.sidebar.minsize(180, 200)
        # Prevent column 0 from shrinking below min width
        self.grid_columnconfigure(0, minsize=180)

        # Main container frame - expands, sticky all sides
        self.container = ctk.CTkFrame(self, fg_color=self.palette["Background"])
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Status bar and progress bar, stick to bottom, span both columns
        self.status_bar = StatusBar(self, self, self.translator)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        self.progress_bar = ProgressBar(self, self, self.translator)
        self.progress_bar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=1)

        self.pages = {}
        self.suggestion = ""

        def get_history_logs(): return self.history_logs.copy()

        # Content frame fills all its space inside container using grid
        self.content_frame = ctk.CTkFrame(
            self.container,
            fg_color=self.palette["Sidebar"],
            corner_radius=18,
            border_width=1,
            border_color=self.palette["Border"]
        )
        self.content_frame.grid(row=0, column=0, sticky="nsew", padx=28, pady=14)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.current_page = None
        self.init_pages(get_history_logs)
        self.set_page("dashboard")
        self.refresh_ui_colors()

    def change_theme(self, theme_name):
        self.theme = theme_name
        self.palette = THEME_PALETTES.get(theme_name, THEME_PALETTES["Night Blue"])
        self.config["theme"] = theme_name
        save_config(self.config)
        if theme_name == "Soft Gray":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")
        self.refresh_ui_colors()
    def refresh_ui_colors(self):
        pal = self.palette
        self.configure(bg=pal["Background"])
        self.container.configure(fg_color=pal["Background"])
        self.sidebar.palette = pal
        self.sidebar.update_theme()
        self.status_bar.palette = pal
        self.status_bar.refresh_language()
        self.progress_bar.palette = pal
        self.progress_bar.refresh_language()
        self.content_frame.configure(fg_color=pal["Sidebar"], border_color=pal["Border"])
        for key, page in self.pages.items():
            if hasattr(page, "palette"):
                page.palette = pal
            if hasattr(page, "refresh_language"):
                page.refresh_language()
        if "reports" in self.pages:
            page = self.pages["reports"]
            page.refresh_report_content()
    def set_page(self, page):
        if self.current_page:
            # Always use grid_forget for pages
            if hasattr(self.current_page, "grid_forget"):
                self.current_page.grid_forget()
            elif hasattr(self.current_page, "pack_forget"):
                self.current_page.pack_forget()
        self.current_page = self.pages[page]
        # Page must fill the content_frame using sticky='nsew'
        self.current_page.grid(row=0, column=0, sticky="nsew")
        if hasattr(self.current_page, "refresh_language"):
            self.current_page.refresh_language()
        if page == "reports" and hasattr(self.current_page, "refresh_report_content"):
            self.current_page.refresh_report_content()
    def open_settings(self): self.set_page("settings")
    def add_history_log(self, text): self.history_logs.append(text)
    def update_reports_page(self):
        if "reports" in self.pages:
            page = self.pages["reports"]
            page.refresh_report_content()
    def init_pages(self, get_history_logs):
        self.pages = {
            "dashboard": DashboardPage(self.content_frame, self, self.translator),
            "organize": OrganizeFilesPage(
                self.content_frame, self, self.translator, self.status_bar, self.progress_bar,
                add_log_callback=self.add_history_log, update_reports_callback=self.update_reports_page
            ),
            "reports": ReportsPage(self.content_frame, self, self.translator, get_logs_func=get_history_logs),
            "settings": SettingsPage(self.content_frame, self, self.translator)
        }
    def refresh_language(self):
        self.translator.language = self.config.get("language", "en")
        self.refresh_ui_colors()
    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = FileOrganizerApp()
    app.run()
