import ctypes
from PIL import Image
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from customtkinter import filedialog
import json
import os
import sys
import urllib.request
import urllib.error
import re
import threading
import socket
import webbrowser
import time

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ─── Renk Paleti ──────────────────────────────────────────────────────────────
TITLEBAR_BG   = ("#d8dce3", "#0a0a12")
ACCENT        = ("#5865F2", "#5865F2")
ACCENT_HOVER  = ("#4752C4", "#4752C4")
SUCCESS       = ("#1f6b2e", "#3ba55c")
SUCCESS_HVR   = ("#164d20", "#2d8a47")
DANGER        = ("#c0392b", "#ed4245")
DANGER_HVR    = ("#922b21", "#c03537")
WARN_COLOR    = ("#b7770d", "#faa81a")
SIDEBAR_BG    = ("#d8dce3", "#0f0f1a")
CARD_BG       = ("#eef0f3", "#161625")
SURFACE       = ("#ffffff", "#1e1e30")
SURFACE2      = ("#e5e8ed", "#252538")
BORDER        = ("#c8ccd2", "#2e2e48")
TXT_PRI       = ("#050507", "#eaeaf6")
TXT_SEC       = ("#4a4f5a", "#8f91b0")
TXT_MUTED     = ("#767b85", "#4f5170")

_APP_DATA_DIR = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "WARPConfig")
os.makedirs(_APP_DATA_DIR, exist_ok=True)
CONFIG_FILE = os.path.join(_APP_DATA_DIR, "warp_config.json")

DEFAULT_CATEGORIES = {
    "Custom": {"entries": []},
    "Discord": {"entries": [
        "34.0.240.0/20", "34.124.0.0/14", "35.186.224.24", "35.186.224.45",
        "35.207.192.0/18", "35.213.0.0/17", "35.213.128.0/18", "35.213.192.0/18",
        "35.214.128.0/17", "35.215.128.0/18", "35.215.192.0/18", "66.22.196.0/22",
        "66.22.200.0/22", "66.22.204.0/22", "66.22.208.0/22", "66.22.212.0/22",
        "66.22.216.0/23", "66.22.218.0/23", "66.22.220.0/23", "66.22.222.0/23",
        "66.22.224.0/23", "66.22.226.0/23", "66.22.230.0/24", "66.22.231.0/24",
        "66.22.232.0/24", "66.22.233.0/24", "66.22.234.0/24", "66.22.235.0/24",
        "66.22.236.0/24", "66.22.237.0/24", "66.22.238.0/24", "66.22.239.0/24",
        "66.22.240.0/24", "66.22.241.0/24", "66.22.242.0/24", "66.22.243.0/24",
        "66.22.243.155/32", "66.22.244.0/24", "66.22.244.37/32", "66.22.245.0/24",
        "66.22.246.0/24", "66.22.247.0/24", "66.22.248.0/24", "104.16.51.111",
        "104.18.0.0/20", "104.18.48.115", "162.159.128.0/19", "162.159.128.0/25",
        "162.159.128.233/32", "162.159.128.234/31", "162.159.128.236/30",
        "162.159.128.240/28", "162.159.129.0/24", "162.159.129.233/32",
        "162.159.130.0/23", "162.159.130.233/32", "162.159.130.234/32",
        "162.159.132.0/22", "162.159.133.233/32", "162.159.133.234/32",
        "162.159.134.233/32", "162.159.134.234/32", "162.159.135.232/32",
        "162.159.135.233/32", "162.159.135.234/32", "162.159.136.0/23",
        "162.159.136.232/32", "162.159.136.234/32", "162.159.137.232/32",
        "162.159.138.0/25", "162.159.138.128/26", "162.159.138.192/27",
        "162.159.138.224/29", "162.159.138.232/32", "198.244.231.90/32",
        "airhorn.solutions", "airhornbot.com", "bigbeans.solutions", "*.bigbeans.solutions",
        "daveprotocol.com", "*.daveprotocol.com", "dfr.gg", "dis.gd", "*.dis.gd",
        "discord.co", "*.discord.co", "discord.com", "*.discord.com", "discord.design",
        "*.discord.design", "discord.dev", "*.discord.dev", "discord.fr", "*.discord.fr",
        "discord.gg", "*.discord.gg", "discord.gift", "*.discord.gift", "discord.gifts",
        "*.discord.gifts", "discord.media", "*.discord.media", "discord.new", "*.discord.new",
        "discord.store", "*.discord.store", "discord.tools", "*.discord.tools",
        "discord-activities.com", "*.discord-activities.com", "discord-attachments-uploads-prd.storage.googleapis.com",
        "discordactivities.com", "*.discordactivities.com", "discordapp.com", "*.discordapp.com",
        "discordapp.io", "*.discordapp.io", "discordapp.net", "*.discordapp.net",
        "discordcdn.com", "*.discordcdn.com", "discordmerch.com", "*.discordmerch.com",
        "discordpartygames.com", "*.discordpartygames.com", "discordsays.com", "*.discordsays.com",
        "discordsez.com", "*.discordsez.com", "discordstatus.com", "*.discordstatus.com",
        "gateway.discord.gg", "i.dis.gd", "remote-auth-gateway.discord.gg",
        "watchanimeattheoffice.com", "*.watchanimeattheoffice.com"
    ]},
    "Roblox": {"entries": [
        "roblox.com", "*.roblox.com", "rbxcdn.com", "*.rbxcdn.com",
        "robloxlabs.com", "*.robloxlabs.com",
    ]},
    "Twitch": {"entries": [
        "twitch.tv", "*.twitch.tv", "ttvnw.net", "*.ttvnw.net", "jtvnw.net", "*.jtvnw.net",
    ]},
    "Instagram": {"entries": [
        "instagram.com", "*.instagram.com", "cdninstagram.com", "*.cdninstagram.com",
    ]},
}

# ─── Ana Uygulama ──────────────────────────────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WARP Configurator")
        self.geometry("1060x720")
        self.minsize(920, 620)
        self.configure(fg_color=SIDEBAR_BG)

        # ── Custom title bar (Windows chrome'u kaldır) ────────────────────────
        self.overrideredirect(True)
        self._drag_x = self._drag_y = 0
        self.bind("<Map>", self._on_map_restore)
        self.after(200, self._set_appwindow)

        icon_path = resource_path("icon.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # ── Config ──────────────────────────────────────────────────────────
        self.config_data = {
            "api_token": "",
            "account_id": "",
            "theme": "Dark",
            "tunnel_protocol": "masque",
            "categories": {k: {"entries": list(v["entries"])} for k, v in DEFAULT_CATEGORIES.items()},
            "current_category": "Custom",
        }
        self._initializing = True
        self.load_config()
        ctk.set_appearance_mode("Dark")

        # ── Layout: row 0 = titlebar, row 1 = content ───────────────────────
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._build_titlebar()
        self._build_sidebar()
        self._build_main_area()
        self._navigate("routes")

        # ── Veri kaybı fix: select_profile ÖNCE, _initializing=False SONRA ──
        self.select_profile(self.config_data.get("current_category", "Custom"))
        self._initializing = False  # select_profile bittikten SONRA aktif

        # ── Live sync ────────────────────────────────────────────────────────
        self._live_sync_running = True
        self._start_live_sync()

    # ── Custom Title Bar ──────────────────────────────────────────────────────

    def _set_appwindow(self):
        """overrideredirect(True) aktifken görev çubuğunda (taskbar) ikonun çıkmasını sağlar."""
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -20) # GWL_EXSTYLE
        style = style & ~0x00000080 # Remove WS_EX_TOOLWINDOW
        style = style | 0x00040000  # Add WS_EX_APPWINDOW
        ctypes.windll.user32.SetWindowLongW(hwnd, -20, style)
        self.withdraw()
        self.deiconify()

    def _build_titlebar(self):
        tb = ctk.CTkFrame(self, height=44, corner_radius=0, fg_color=TITLEBAR_BG)
        tb.grid(row=0, column=0, columnspan=2, sticky="ew")
        tb.grid_propagate(False)
        tb.grid_columnconfigure(1, weight=1)

        # Logo Text
        logo = ctk.CTkFrame(tb, fg_color="transparent")
        logo.grid(row=0, column=0, padx=(16, 0), sticky="w")
        ctk.CTkLabel(logo, text="⚡", font=ctk.CTkFont(size=18)).pack(side="left")
        ctk.CTkLabel(logo, text=" WARP", font=ctk.CTkFont(size=15, weight="bold"), text_color=TXT_PRI).pack(side="left")
        ctk.CTkLabel(logo, text="Config", font=ctk.CTkFont(size=15), text_color=ACCENT).pack(side="left")
        ctk.CTkLabel(logo, text="  v2.3", font=ctk.CTkFont(size=11), text_color=TXT_MUTED).pack(side="left")

        # Drag binding
        for w in [tb, logo]:
            w.bind("<Button-1>",   self._start_drag)
            w.bind("<B1-Motion>",  self._do_drag)

        # Window controls
        ctrl = ctk.CTkFrame(tb, fg_color="transparent")
        ctrl.grid(row=0, column=2, sticky="e")

        for text, cmd, hover in [
            ("─",  self._minimize,  ("#c8ccd2", "#1e1e30")),
            ("✕",  self._on_close,  ("#e81123", "#8b1a1a")),
        ]:
            btn = ctk.CTkButton(
                ctrl, text=text, width=50, height=44, corner_radius=0,
                font=ctk.CTkFont(size=16), fg_color="transparent",
                hover_color=hover, text_color=TXT_SEC,
                command=cmd,
            )
            btn.pack(side="left")

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _do_drag(self, event):
        x = self.winfo_x() + (event.x - self._drag_x)
        y = self.winfo_y() + (event.y - self._drag_y)
        self.geometry(f"+{x}+{y}")

    def _minimize(self):
        self.overrideredirect(False)
        self.iconify()

    def _on_map_restore(self, event):
        """Minimize'dan geri dönünce custom titlebar'ı yeniden uygula."""
        if self.state() == "normal":
            self.overrideredirect(True)

    def _on_close(self):
        """Uygulama kapanmadan önce her zaman kaydet."""
        self._live_sync_running = False
        self.save_current_data()
        self.save_config()
        self.destroy()

    # ── Live Sync (Cloudflare → Uygulama) ────────────────────────────────────

    def _start_live_sync(self):
        """Her 45 saniyede Cloudflare'den tünel protokolü ve split tunnel modunu çeker."""
        def _loop():
            while self._live_sync_running:
                time.sleep(45)
                if not self._live_sync_running:
                    break
                try:
                    token = self.config_data.get("api_token", "").strip()
                    acc   = self.config_data.get("account_id", "").strip()
                    if not token or not acc:
                        continue
                    res = self.api_request("GET", "/devices/policy")
                    result = res.get("result", {})
                    if not isinstance(result, dict):
                        continue
                    remote_proto = result.get("tunnel_protocol", "")
                    remote_match = result.get("match", "")
                    if remote_proto:
                        self.after(0, lambda p=remote_proto: self._sync_protocol_ui(p))
                    if remote_match:
                        self.after(0, lambda m=remote_match: self._sync_split_tunnel_ui(m))
                except Exception:
                    pass
        threading.Thread(target=_loop, daemon=True).start()

    def _sync_protocol_ui(self, proto):
        """Cloudflare'den gelen protokolü UI'a yansıt."""
        if hasattr(self, "protocol_var"):
            current = self.protocol_var.get()
            if current != proto:
                self.protocol_var.set(proto)
                self.config_data["tunnel_protocol"] = proto
                self.save_config()

    def _sync_split_tunnel_ui(self, match):
        """Cloudflare'den gelen split tunnel modunu UI'a yansıt."""
        if hasattr(self, "split_tunnel_var"):
            # Cloudflare "match" değeri: "include" veya "exclude"
            mode = "include" if "include" in match.lower() else "exclude"
            current = self.split_tunnel_var.get()
            if current != mode:
                self.split_tunnel_var.set(mode)
                self.config_data["split_tunnel_mode"] = mode
                self.save_config()

    def ask_confirm(self, title, message, on_confirm):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.transient(self)
        dialog.grab_set()
        
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        ctk.CTkLabel(dialog, text=title, font=ctk.CTkFont(size=18, weight="bold"), text_color=TXT_PRI).pack(pady=(20, 10))
        ctk.CTkLabel(dialog, text=message, font=ctk.CTkFont(size=14), text_color=TXT_SEC, wraplength=350).pack(pady=(0, 20))
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        def _yes():
            dialog.destroy()
            on_confirm()
            
        def _no():
            dialog.destroy()
            
        ctk.CTkButton(btn_frame, text="İptal", fg_color=SURFACE, hover_color=SURFACE2, text_color=TXT_PRI, command=_no, width=100).pack(side="left", expand=True, padx=10)
        ctk.CTkButton(btn_frame, text="Evet", fg_color=DANGER, hover_color=DANGER_HVR, command=_yes, width=100).pack(side="right", expand=True, padx=10)

    def _show_modal(self, title, message, level="info", action_text=None, action_cmd=None):
        """Temiz, minimal in-app dialog. Windows popup yok, kod yok."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("")
        dialog.geometry("420x220")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width()  - 420) // 2
        y = self.winfo_rooty() + (self.winfo_height() - 220) // 2
        dialog.geometry(f"+{x}+{y}")

        icon = {"info": "ℹ️", "success": "✅", "error": "❌", "warn": "⚠️"}.get(level, "ℹ️")
        accent = {"info": ACCENT, "success": SUCCESS, "error": DANGER, "warn": WARN_COLOR}.get(level, ACCENT)

        ctk.CTkFrame(dialog, height=4, fg_color=accent, corner_radius=0).pack(fill="x")
        ctk.CTkLabel(dialog, text=f"{icon}  {title}", font=ctk.CTkFont(size=16, weight="bold"), text_color=TXT_PRI).pack(pady=(18, 6))
        ctk.CTkLabel(dialog, text=message, font=ctk.CTkFont(size=13), text_color=TXT_SEC, wraplength=360, justify="center").pack(pady=(0, 16))

        btn_row = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_row.pack(fill="x", padx=24, pady=(0, 18))
        if action_text and action_cmd:
            def _act():
                dialog.destroy()
                action_cmd()
            ctk.CTkButton(btn_row, text=action_text, fg_color=accent, hover_color=ACCENT_HOVER, height=36, command=_act).pack(side="left", expand=True, padx=(0,6))
        ctk.CTkButton(btn_row, text="Kapat", fg_color=SURFACE2, hover_color=BORDER, text_color=TXT_PRI, height=36, command=dialog.destroy).pack(side="right", expand=True)

    # ── Config ────────────────────────────────────────────────────────────────

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
            for key, val in saved.items():
                if key == "categories":
                    for cat_name, cat_data in val.items():
                        if cat_name in DEFAULT_CATEGORIES and cat_name != "Custom":
                            self.config_data["categories"][cat_name] = {"entries": list(DEFAULT_CATEGORIES[cat_name]["entries"])}
                        else:
                            self.config_data["categories"][cat_name] = cat_data
                else:
                    self.config_data[key] = val
                    
            if "Custom" not in self.config_data["categories"]:
                self.config_data["categories"]["Custom"] = {"entries": []}
            
            # Add missing default categories
            for def_cat, def_data in DEFAULT_CATEGORIES.items():
                if def_cat not in self.config_data["categories"]:
                    self.config_data["categories"][def_cat] = {"entries": list(def_data["entries"])}
                else:
                    # Force refresh predefined categories
                    self.config_data["categories"][def_cat]["entries"] = list(def_data["entries"])

        except Exception:
            pass

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    # ── API ───────────────────────────────────────────────────────────────────

    def api_request(self, method, endpoint, data=None):
        token = self.config_data.get("api_token", "").strip()
        acc   = self.config_data.get("account_id", "").strip()
        if not token or not acc:
            raise ValueError("API Token veya Account ID eksik.")
        url     = f"https://api.cloudflare.com/client/v4/accounts/{acc}{endpoint}"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        req     = urllib.request.Request(url, headers=headers, method=method)
        if data is not None:
            req.data = json.dumps(data).encode("utf-8")
        try:
            resp = urllib.request.urlopen(req, timeout=20)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")
            # Sadece JSON parse hatasını yakala, diğer istisnaları geçir
            try:
                err_json = json.loads(body)
                errs = err_json.get("errors", [])
                if errs:
                    err_msg = "\n".join([f"Kod {err.get('code', '?')}: {err.get('message', '')}" for err in errs])
                    raise ValueError(f"Cloudflare API Hatası:\n{err_msg}\n\nTam yanıt: {body[:500]}")
            except json.JSONDecodeError:
                pass
            raise ValueError(f"HTTP {e.code}: {body[:500]}")
        except urllib.error.URLError as e:
            raise ValueError(f"Bağlantı hatası: {e.reason}")

    def get_default_policy_id(self):
        """Default politikanin ID'sini dondurur. Cloudflare /devices/policy tek bir obje dondurur."""
        res = self.api_request("GET", "/devices/policy")
        result = res.get("result")
        if not result or not isinstance(result, dict):
            raise ValueError(
                f"Beklenmeyen API yanıtı. 'result': {result}\n\n"
                "Cloudflare Zero Trust → Settings → WARP Client → Device profiles "
                "bölümünde Default profil mevcut olmalı."
            )
        return result.get("policy_id") or result.get("id")

    # ── Text Cleaning Helper ──────────────────────────────────────────────────

    def extract_valid_entries(self, text):
        import re
        # IP/CIDR arama: 1.1.1.1 veya 1.1.1.1/32
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b', text)
        # Domain arama: test.com veya *.test.com
        domains = re.findall(r'(?<![a-zA-Z0-9-])(?:\*\.)?(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b', text)
        
        res = []
        for x in ips + domains:
            x_clean = x.strip()
            if x_clean and x_clean not in res:
                res.append(x_clean)
        return res

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=230, corner_radius=0, fg_color=SIDEBAR_BG)
        sb.grid(row=1, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_rowconfigure(1, weight=1)

        # Resimli Logo
        logo = ctk.CTkFrame(sb, fg_color="transparent")
        logo.grid(row=0, column=0, sticky="ew", padx=20, pady=(28, 24))
        
        logo_path = resource_path("logo_full.png")
        if os.path.exists(logo_path):
            try:
                logo_img = ctk.CTkImage(
                    light_image=Image.open(logo_path),
                    dark_image=Image.open(logo_path),
                    size=(180, 80)
                )
                ctk.CTkLabel(logo, image=logo_img, text="").pack()
            except Exception:
                ctk.CTkLabel(logo, text="⚡", font=ctk.CTkFont(size=26)).pack(side="left")
                ctk.CTkLabel(logo, text=" WARP", font=ctk.CTkFont(size=20, weight="bold"), text_color=TXT_PRI).pack(side="left")
                ctk.CTkLabel(logo, text="Config", font=ctk.CTkFont(size=20), text_color=ACCENT).pack(side="left")
        else:
            ctk.CTkLabel(logo, text="⚡", font=ctk.CTkFont(size=26)).pack(side="left")
            ctk.CTkLabel(logo, text=" WARP", font=ctk.CTkFont(size=20, weight="bold"), text_color=TXT_PRI).pack(side="left")
            ctk.CTkLabel(logo, text="Config", font=ctk.CTkFont(size=20), text_color=ACCENT).pack(side="left")


        # Nav
        nav_area = ctk.CTkFrame(sb, fg_color="transparent")
        nav_area.grid(row=1, column=0, sticky="nsew", padx=10)

        self.nav_buttons = {}
        nav_items = [
            ("routes",   "🔀", "Yönlendirme"),
            ("settings", "⚙️", "API & Protokol"),
            ("devices",  "💻", "Cihazlar"),
            ("guide",    "📋", "Kurulum"),
        ]
        for page, icon, label in nav_items:
            btn = ctk.CTkButton(
                nav_area, text=f"  {icon}  {label}", anchor="w",
                height=44, corner_radius=10, font=ctk.CTkFont(size=14),
                fg_color="transparent", hover_color=SURFACE2, text_color=TXT_SEC,
                command=lambda p=page: self._navigate(p),
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[page] = btn

        # Bottom
        bottom = ctk.CTkFrame(sb, fg_color="transparent")
        bottom.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 18))

        ctk.CTkLabel(bottom, text="v2.3", font=ctk.CTkFont(size=11), text_color=TXT_MUTED).pack(pady=(0, 10))

    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_area.grid(row=1, column=1, sticky="nsew")
        self.main_area.grid_rowconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        self.pages = {}
        for page_name in ["routes", "settings", "devices", "guide"]:
            frame = ctk.CTkFrame(self.main_area, corner_radius=0, fg_color=CARD_BG)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[page_name] = frame

        self._build_routes_page(self.pages["routes"])
        self._build_settings_page(self.pages["settings"])
        self._build_devices_page(self.pages["devices"])
        self._build_guide_page(self.pages["guide"])

    def _navigate(self, page):
        for p, btn in self.nav_buttons.items():
            if p == page:
                btn.configure(fg_color=SURFACE2, text_color=TXT_PRI)
            else:
                btn.configure(fg_color="transparent", text_color=TXT_SEC)

        self.current_page = page
        self.pages[page].tkraise()



    # ── Yönlendirme Sayfası ───────────────────────────────────────────────────

    def _build_routes_page(self, page):
        page.grid_columnconfigure(0, weight=0)
        page.grid_columnconfigure(1, weight=1)
        page.grid_rowconfigure(0, weight=1)

        # ── Sol panel (Kategoriler) ────────────────────────────────────────────
        cat_panel = ctk.CTkFrame(page, width=250, fg_color=SIDEBAR_BG, corner_radius=0)
        cat_panel.grid(row=0, column=0, sticky="nsew")
        cat_panel.grid_propagate(False)
        cat_panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            cat_panel, text="KATEGORİLER",
            font=ctk.CTkFont(size=11, weight="bold"), text_color=TXT_MUTED
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(20, 10))

        self.cat_scroll = ctk.CTkScrollableFrame(cat_panel, fg_color="transparent")
        self.cat_scroll.grid(row=1, column=0, sticky="nsew", padx=6)

        # Yeni kategori ekle
        ctk.CTkFrame(cat_panel, height=1, fg_color=BORDER).grid(row=2, column=0, sticky="ew", padx=10, pady=(6, 0))
        add_row = ctk.CTkFrame(cat_panel, fg_color="transparent")
        add_row.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

        self.new_cat_entry = ctk.CTkEntry(
            add_row, placeholder_text="Yeni kategori...",
            height=36, font=ctk.CTkFont(size=13),
            fg_color=SURFACE, border_color=BORDER, border_width=1,
        )
        self.new_cat_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
        self.new_cat_entry.bind("<Return>", lambda e: self.add_profile())

        ctk.CTkButton(
            add_row, text="+", width=36, height=36,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            command=self.add_profile,
        ).pack(side="right")

        # ── Sağ panel (Editör) ────────────────────────────────────────────────
        editor = ctk.CTkFrame(page, fg_color=CARD_BG, corner_radius=0)
        editor.grid(row=0, column=1, sticky="nsew")
        editor.grid_rowconfigure(2, weight=1)
        editor.grid_columnconfigure(0, weight=1)

        # Başlık satırı
        hdr = ctk.CTkFrame(editor, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", padx=26, pady=(24, 0))

        self.prof_title_lbl = ctk.CTkLabel(
            hdr, text="Custom", font=ctk.CTkFont(size=21, weight="bold"), text_color=TXT_PRI
        )
        self.prof_title_lbl.pack(side="left")

        self.entry_count_lbl = ctk.CTkLabel(
            hdr, text="0 kural", font=ctk.CTkFont(size=13), text_color=TXT_MUTED
        )
        self.entry_count_lbl.pack(side="left", padx=(10, 0), pady=(4, 0))

        # Hızlı ekle araç çubuğu
        toolbar = ctk.CTkFrame(editor, fg_color=SURFACE, corner_radius=10)
        toolbar.grid(row=1, column=0, sticky="ew", padx=26, pady=14)
        
        # Üst kısım: Hızlı ekle
        top_tool = ctk.CTkFrame(toolbar, fg_color="transparent")
        top_tool.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(top_tool, text="Hızlı Ekle", font=ctk.CTkFont(size=13, weight="bold"), text_color=TXT_SEC).pack(side="left", padx=(6, 10))
        self.qa_entry = ctk.CTkEntry(top_tool, placeholder_text="domain.com veya 1.2.3.4/24", height=36, fg_color=CARD_BG, border_width=1, border_color=BORDER, font=ctk.CTkFont(size=13))
        self.qa_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.qa_entry.bind("<Return>", lambda e: self.quick_add())
        ctk.CTkButton(top_tool, text="Ekle →", height=36, width=84, font=ctk.CTkFont(size=13, weight="bold"), fg_color=ACCENT, hover_color=ACCENT_HOVER, command=self.quick_add).pack(side="left", padx=(0, 6))

        # Alt kısım: Araçlar
        bot_tool = ctk.CTkFrame(toolbar, fg_color="transparent")
        bot_tool.pack(fill="x", padx=10, pady=(5, 10))

        ctk.CTkButton(bot_tool, text="⬇️ İçe Aktar", width=90, height=30, font=ctk.CTkFont(size=12), fg_color=SURFACE2, hover_color=BORDER, text_color=TXT_PRI, command=self.import_list).pack(side="left", padx=(6, 5))
        ctk.CTkButton(bot_tool, text="⬆️ Dışa Aktar", width=90, height=30, font=ctk.CTkFont(size=12), fg_color=SURFACE2, hover_color=BORDER, text_color=TXT_PRI, command=self.export_list).pack(side="left", padx=5)
        
        ctk.CTkButton(bot_tool, text="🔍 İlişkili Adresleri Bul", width=150, height=30, font=ctk.CTkFont(size=12), fg_color=SURFACE2, hover_color=BORDER, text_color=TXT_PRI, command=self.deep_scan_domain).pack(side="right", padx=5)

        # Metin kutusu
        self.entries_text = ctk.CTkTextbox(
            editor, font=ctk.CTkFont(family="Consolas", size=13),
            fg_color=SURFACE, text_color=TXT_PRI,
            border_width=1, border_color=BORDER, corner_radius=10,
        )
        self.entries_text.grid(row=2, column=0, sticky="nsew", padx=26, pady=(0, 12))
        self.entries_text.bind("<KeyRelease>", lambda e: self._update_count())
        self.entries_text.bind("<<Paste>>", self._on_paste)

        # Alt satır: Uygula butonu + durum mesajı
        bottom_bar = ctk.CTkFrame(editor, fg_color="transparent")
        bottom_bar.grid(row=3, column=0, sticky="ew", padx=26, pady=(0, 20))
        bottom_bar.grid_columnconfigure(0, weight=1)

        self.apply_btn = ctk.CTkButton(
            bottom_bar, text="⚡  Tüm Kategorileri WARP'a Uygula",
            height=50, font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=SUCCESS, hover_color=SUCCESS_HVR, corner_radius=10,
            command=self.apply_to_warp,
        )
        self.apply_btn.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.status_lbl = ctk.CTkLabel(
            bottom_bar, text="Not: Mevcut tüm kategorilerdeki IP ve domainler Cloudflare ile senkronize edilir.", font=ctk.CTkFont(size=12), text_color=TXT_MUTED
        )
        self.status_lbl.grid(row=1, column=0, sticky="w")

        self.refresh_profiles()

    def _on_paste(self, event):
        self.after(50, self.clean_entries_text)

    def clean_entries_text(self):
        current = self.entries_text.get("1.0", tk.END)
        cleaned = self.extract_valid_entries(current)
        self.entries_text.delete("1.0", tk.END)
        self.entries_text.insert(tk.END, "\n".join(cleaned))
        self._update_count()
        self._set_status("Metin içerisindeki geçersiz yazılar temizlendi.", "success")

    def import_list(self):
        file_path = filedialog.askopenfilename(title="Liste Seç", filetypes=[("Text ve JSON", "*.txt *.json"), ("Tüm Dosyalar", "*.*")])
        if not file_path:
            return
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            new_entries = ""
            if file_path.endswith(".json"):
                try:
                    data = json.loads(content)
                    if isinstance(data, list):
                        new_entries = "\n".join(str(i) for i in data)
                    elif isinstance(data, dict):
                        new_entries = json.dumps(data)
                except Exception:
                    new_entries = content
            else:
                new_entries = content
                
            valid_new = self.extract_valid_entries(new_entries)
            if not valid_new:
                self._show_modal("Geçersiz Dosya", "Dosya içerisinde geçerli bir IP veya domain bulunamadı.", "warn")
                return

            cat_name = os.path.splitext(os.path.basename(file_path))[0] or "Imported"

            # Mevcut kategori verisi varsa ÖNCE kaydet, SONRA güncelle
            if cat_name == self.config_data.get("current_category"):
                # Aynı kategorideyiz: entries_text'i direkt güncelle
                self.config_data["categories"][cat_name] = {"entries": valid_new}
                self.entries_text.delete("1.0", tk.END)
                self.entries_text.insert(tk.END, "\n".join(valid_new))
                self._update_count()
            else:
                # Farklı kategori: save_current_data'yı çağırmadan veriyi yaz
                self.config_data["categories"][cat_name] = {"entries": valid_new}
                # Şimdi güvenle geçiş yapabiliriz
                self.config_data["current_category"] = cat_name
                self.entries_text.delete("1.0", tk.END)
                self.entries_text.insert(tk.END, "\n".join(valid_new))
                self._update_count()
                self.refresh_profiles()

            self.save_config()
            self._set_status(f"'{cat_name}' kategorisi güncellendi — {len(valid_new)} adres", "success")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya okunurken hata oluştu: {e}")

    def export_list(self):
        file_path = filedialog.asksaveasfilename(
            title="Listeyi Kaydet", 
            defaultextension=".txt", 
            filetypes=[("Text file", "*.txt"), ("JSON file", "*.json")]
        )
        if not file_path:
            return
            
        try:
            current = self.entries_text.get("1.0", tk.END)
            valid_current = self.extract_valid_entries(current)
            
            with open(file_path, "w", encoding="utf-8") as f:
                if file_path.endswith(".json"):
                    json.dump(valid_current, f, indent=4)
                else:
                    f.write("\n".join(valid_current))
            messagebox.showinfo("Başarılı", "Liste başarıyla dışa aktarıldı.")
        except Exception as e:
            messagebox.showerror("Hata", f"Dışa aktarma hatası: {e}")

    def deep_scan_domain(self):
        dialog = ctk.CTkInputDialog(text="Tarancak domaini girin (örn. youtube.com):", title="İlişkili Adresleri Bul")
        domain = dialog.get_input()
        if not domain:
            return
        domain = domain.strip()
        # Clean protocol or path if user pasted a link
        if "://" in domain:
            domain = domain.split("://")[-1].split("/")[0]
            
        def _scan():
            self.after(0, lambda: self._set_status(f"{domain} için ilişkili adresler HackerTarget üzerinden aranıyor...", "info"))
            try:
                url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                resp = urllib.request.urlopen(req, timeout=15)
                data = resp.read().decode("utf-8")
                
                lines = data.splitlines()
                if not lines or "error" in data.lower() or "no records" in data.lower():
                    self.after(0, lambda: messagebox.showinfo("Bulunamadı", "İlişkili kayıt bulunamadı veya API limiti aşıldı."))
                    self.after(0, lambda: self._set_status("Tarama başarısız veya sonuç yok.", "error"))
                    return
                
                found = []
                for line in lines:
                    parts = line.split(",")
                    if len(parts) == 2:
                        found.append(parts[0].strip())
                        found.append(parts[1].strip() + "/32")
                        
                self.after(0, lambda: self._add_fetched_lines(found))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Hata", f"Tarama hatası: {e}"))
                self.after(0, lambda: self._set_status("Tarama sırasında hata oluştu.", "error"))
                
        threading.Thread(target=_scan, daemon=True).start()

    def _add_fetched_lines(self, lines):
        text = "\n".join(lines)
        valid_new = self.extract_valid_entries(text)
        
        current = self.entries_text.get("1.0", tk.END)
        valid_current = self.extract_valid_entries(current)
        
        added = 0
        for v in valid_new:
            if v not in valid_current:
                valid_current.append(v)
                added += 1
                
        self.entries_text.delete("1.0", tk.END)
        self.entries_text.insert(tk.END, "\n".join(valid_current))
        self._update_count()
        self._set_status(f"{added} yeni ilişkili adres eklendi.", "success")

    def _update_count(self):
        if not hasattr(self, "entries_text") or not hasattr(self, "entry_count_lbl"):
            return
        lines = self.entries_text.get("1.0", tk.END)
        count = len([l for l in lines.split("\n") if l.strip()])
        self.entry_count_lbl.configure(text=f"{count} kural")

        # Baslangic asamasinda kaydetme (entries_text henuz dolu degil)
        if getattr(self, "_initializing", True):
            return

        # Otomatik kaydet
        cat = self.config_data.get("current_category")
        if cat and cat in self.config_data["categories"]:
            entries = [e.strip() for e in lines.split("\n") if e.strip()]
            self.config_data["categories"][cat]["entries"] = entries
            self.save_config()

    def refresh_profiles(self):
        if not hasattr(self, "cat_scroll"):
            return
        for w in self.cat_scroll.winfo_children():
            w.destroy()

        cats = list(self.config_data["categories"].keys())
        if "Custom" in cats:
            cats.remove("Custom")
            cats.insert(0, "Custom")

        for cat in cats:
            self._make_cat_row(cat, cat == self.config_data.get("current_category"))

    def _make_cat_row(self, cat, is_active):
        row = ctk.CTkFrame(
            self.cat_scroll,
            fg_color=SURFACE2 if is_active else "transparent",
            corner_radius=8, height=38,
        )
        row.pack(fill="x", pady=2)
        row.pack_propagate(False)

        name_btn = ctk.CTkButton(
            row, text=cat, anchor="w",
            font=ctk.CTkFont(size=13, weight="bold" if is_active else "normal"),
            fg_color="transparent", hover_color=SURFACE2,
            text_color=TXT_PRI if is_active else TXT_SEC,
            command=lambda c=cat: self.select_profile(c),
        )
        name_btn.pack(side="left", fill="both", expand=True, padx=(8, 0))

        if cat != "Custom":
            del_btn = ctk.CTkButton(
                row, text="✕", width=28, height=28,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="transparent", hover_color=DANGER,
                text_color=TXT_MUTED,
                command=lambda c=cat: self.delete_profile(c),
            )
            del_btn.pack(side="right", padx=5)

    def save_current_data(self):
        if not hasattr(self, "entries_text"):
            return
        # Baslangic asamasinda bos entries_text ile mevcut veriyi silme
        if getattr(self, "_initializing", True):
            return
        cat = self.config_data.get("current_category")
        if not cat or cat not in self.config_data["categories"]:
            return
        text    = self.entries_text.get("1.0", tk.END)
        entries = [e.strip() for e in text.split("\n") if e.strip()]
        self.config_data["categories"][cat]["entries"] = entries

    def select_profile(self, cat):
        self.save_current_data()
        self.config_data["current_category"] = cat

        if hasattr(self, "prof_title_lbl"):
            self.prof_title_lbl.configure(text=cat)

        entries = self.config_data["categories"].get(cat, {}).get("entries", [])
        if hasattr(self, "entries_text"):
            self.entries_text.delete("1.0", tk.END)
            self.entries_text.insert(tk.END, "\n".join(entries))
            self._update_count()

        self.refresh_profiles()
        self.save_config()

    def add_profile(self):
        new_cat = self.new_cat_entry.get().strip()
        if not new_cat:
            return
        if new_cat in self.config_data["categories"]:
            self._set_status(f"'{new_cat}' zaten mevcut.", "warn")
            return
        self.save_current_data()
        self.config_data["categories"][new_cat] = {"entries": []}
        self.new_cat_entry.delete(0, tk.END)
        self.select_profile(new_cat)

    def delete_profile(self, cat):
        if cat == "Custom":
            return
        
        def _do_delete():
            del self.config_data["categories"][cat]
            if self.config_data.get("current_category") == cat:
                self.config_data["current_category"] = "Custom"
                if hasattr(self, "prof_title_lbl"):
                    self.prof_title_lbl.configure(text="Custom")
                entries = self.config_data["categories"]["Custom"].get("entries", [])
                if hasattr(self, "entries_text"):
                    self.entries_text.delete("1.0", tk.END)
                    self.entries_text.insert(tk.END, "\n".join(entries))
                    self._update_count()
            self.refresh_profiles()
            self.save_config()
            self._set_status(f"'{cat}' silindi.", "success")

        self.ask_confirm("Kategoriyi Sil", f"'{cat}' kategorisini silmek istediğinize emin misiniz?", _do_delete)

    def quick_add(self):
        val = self.qa_entry.get().strip()
        if not val:
            return
        
        valid = self.extract_valid_entries(val)
        if not valid:
            self._set_status("Geçerli bir IP veya Domain girilmedi.", "error")
            return
            
        current = self.entries_text.get("1.0", tk.END)
        valid_current = self.extract_valid_entries(current)
        
        added = 0
        for v in valid:
            if v not in valid_current:
                valid_current.append(v)
                added += 1
                
        self.entries_text.delete("1.0", tk.END)
        self.entries_text.insert(tk.END, "\n".join(valid_current))
        self.qa_entry.delete(0, tk.END)
        self._update_count()
        
        if added > 0:
            self._set_status(f"{added} kayıt eklendi.", "success")
        else:
            self._set_status("Girilen kayıt zaten listede mevcut.", "warn")

    def apply_to_warp(self):
        self.clean_entries_text()
        self.save_current_data()

        token = self.config_data.get("api_token", "").strip()
        acc   = self.config_data.get("account_id", "").strip()
        if not token or not acc:
            self._navigate("settings")
            messagebox.showerror("Hata", "Lütfen önce API Token ve Account ID bilgilerinizi girin.")
            return

        all_entries = []
        for cat_data in self.config_data["categories"].values():
            for e in cat_data.get("entries", []):
                if e not in all_entries:
                    all_entries.append(e)

        if not all_entries:
            if not messagebox.askyesno("Uyarı", "Gönderilecek liste tamamen boş.\nBu işlem Cloudflare üzerindeki TÜM kayıtları silecek. Onaylıyor musunuz?"):
                return

        self.apply_btn.configure(state="disabled", text="⏳  Gönderiliyor...")
        self._set_status("Tüm kategoriler Cloudflare'e eşitleniyor...", "info")
        self.update()

        def _worker():
            try:
                # Default policy icin ID'ye gerek yok, direkt /devices/policy/include kullan
                ip_pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}(/\d{1,2})?$")
                body = []
                for e in all_entries:
                    if ip_pattern.match(e):
                        if "/" not in e:
                            e += "/32"
                        body.append({"address": e, "description": "WARPConfig"})
                    else:
                        body.append({"host": e, "description": "WARPConfig"})

                res = self.api_request("PUT", "/devices/policy/include", body)
                self.after(0, lambda: self._on_apply_done(res, len(body)))
            except Exception as ex:
                self.after(0, lambda err=str(ex): self._on_apply_error(err))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_apply_done(self, res, count):
        self.apply_btn.configure(state="normal", text="⚡  Tüm Kategorileri WARP'a Uygula")
        if res.get("success"):
            self._set_status(f"✓  Tüm listeler Cloudflare ile senkronize edildi! ({count} kayıt)", "success")
            messagebox.showinfo(
                "Başarılı",
                f"Toplam {count} kural Zero Trust'a eklendi/güncellendi!\n\n"
                "Uygulamada olan listeleriniz Cloudflare ile birebir eşitlendi.\n"
                "Değişikliklerin aktif olması için WARP istemcisini kapatıp yeniden açın.",
            )
        else:
            errs = res.get("errors", [])
            if errs:
                err_msg = "\n".join([f"Kodu: {e.get('code', 'Bilinmiyor')} - {e.get('message', '')}" for e in errs])
            else:
                err_msg = "Bilinmeyen API Hatası"
            self._set_status("API hatası oluştu.", "error")
            messagebox.showerror("API Hatası", err_msg)

    def _on_apply_error(self, msg):
        self.apply_btn.configure(state="normal", text="⚡  Tüm Kategorileri WARP'a Uygula")
        self._set_status(f"Hata: {msg[:80]}", "error")
        self._show_modal("Hata", msg[:300], "error")

    def _set_status(self, msg, level="info"):
        if not hasattr(self, "status_lbl"):
            return
        color = {
            "success": SUCCESS,
            "error":   DANGER,
            "warn":    WARN_COLOR,
            "info":    TXT_MUTED,
        }.get(level, TXT_MUTED)
        self.status_lbl.configure(text=msg, text_color=color)

    # ── Ayarlar Sayfası ───────────────────────────────────────────────────────

    def _build_settings_page(self, page):
        scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=32, pady=24)

        ctk.CTkLabel(
            scroll, text="API & Protokol Ayarları",
            font=ctk.CTkFont(size=22, weight="bold"), text_color=TXT_PRI,
        ).pack(anchor="w", pady=(0, 22))

        self._card(scroll, "🔑  API Yapılandırması",       self._section_api)
        self._card(scroll, "🚀  Hızlı Kurulum",            self._section_quick_setup)
        self._card(scroll, "🔗  Tünel Protokolü",           self._section_proto)
        self._card(scroll, "⛶  Split Tunnel Modu",          self._section_split_tunnel)

    def _card(self, parent, title, build_fn):
        card = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=14)
        card.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(
            card, text=title, font=ctk.CTkFont(size=15, weight="bold"), text_color=TXT_PRI
        ).pack(anchor="w", padx=22, pady=(18, 12))
        ctk.CTkFrame(card, height=1, fg_color=BORDER).pack(fill="x", padx=22)
        build_fn(card)
        ctk.CTkFrame(card, height=4, fg_color="transparent").pack()

    def _section_api(self, parent):
        self.token_entry = ctk.CTkEntry(
            parent, placeholder_text="Cloudflare API Token",
            show="*", height=40, fg_color=CARD_BG, border_color=BORDER,
            font=ctk.CTkFont(size=13),
        )
        self.token_entry.pack(fill="x", padx=22, pady=(16, 8))
        if self.config_data.get("api_token"):
            self.token_entry.insert(0, self.config_data["api_token"])

        self.acc_entry = ctk.CTkEntry(
            parent, placeholder_text="Cloudflare Account ID",
            height=40, fg_color=CARD_BG, border_color=BORDER,
            font=ctk.CTkFont(size=13),
        )
        self.acc_entry.pack(fill="x", padx=22, pady=(0, 16))
        if self.config_data.get("account_id"):
            self.acc_entry.insert(0, self.config_data["account_id"])

        btn_row = ctk.CTkFrame(parent, fg_color="transparent")
        btn_row.pack(anchor="w", padx=22, pady=(0, 18))

        ctk.CTkButton(
            btn_row, text="Kaydet", width=110, height=38,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.save_api_credentials,
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            btn_row, text="🔌 Bağlantıyı Test Et", width=180, height=38,
            fg_color=SURFACE2, hover_color=BORDER, text_color=TXT_PRI, corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.test_connection,
        ).pack(side="left")

    def _section_proto(self, parent):
        ctk.CTkLabel(
            parent,
            text="Superonline / Vodafone gibi ISP'lerde Discord engelini aşmak için MASQUE seçin.\n"
                 "MASQUE, 443 portunu kullandığından engellenemez.",
            font=ctk.CTkFont(size=13), text_color=TXT_SEC,
            wraplength=520, justify="left",
        ).pack(anchor="w", padx=22, pady=(14, 12))

        self.protocol_var = ctk.StringVar(value=self.config_data.get("tunnel_protocol", "masque"))

        for val, label, desc in [
            ("masque",    "MASQUE",    "Önerilen · 443 portunu kullanır · Engellenmez"),
            ("wireguard", "WireGuard", "Standart · Bazı ISP'lerde engellenebilir"),
        ]:
            row = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=8)
            row.pack(fill="x", padx=22, pady=4)
            ctk.CTkRadioButton(
                row, text=f"  {label}", variable=self.protocol_var, value=val,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=ACCENT, hover_color=ACCENT_HOVER,
                radiobutton_width=18, radiobutton_height=18,
            ).pack(side="left", padx=16, pady=14)
            ctk.CTkLabel(
                row, text=desc, font=ctk.CTkFont(size=12), text_color=TXT_MUTED
            ).pack(side="left")

        ctk.CTkButton(
            parent, text="Protokolü Uygula", width=160, height=38,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.apply_protocol,
        ).pack(anchor="w", padx=22, pady=(14, 18))

    def _section_split_tunnel(self, parent):
        ctk.CTkLabel(
            parent,
            text="Split Tunnel modu, WARP trafiğinin nasıl yönlendirileceğini belirler.\n"
                 "Include: Sadece listedeki IP/domain'ler WARP'tan geçer (Önerilen - Discord, Roblox vb.)\n"
                 "Exclude: Listedeki IP/domain'ler WARP'tan geçmez, diğerleri geçer.",
            font=ctk.CTkFont(size=13), text_color=TXT_SEC,
            wraplength=520, justify="left",
        ).pack(anchor="w", padx=22, pady=(14, 12))

        self.split_tunnel_var = ctk.StringVar(value=self.config_data.get("split_tunnel_mode", "include"))

        modes = [
            ("include", "Include Modu",  "⭐ Önerilen · Sadece belirlediğin IP/domain'ler WARP'tan geçer"),
            ("exclude", "Exclude Modu",  "Listendeki IP/domain'ler WARP'ı atlar, diğerleri geçer"),
        ]
        for val, label, desc in modes:
            row = ctk.CTkFrame(parent, fg_color=CARD_BG, corner_radius=8)
            row.pack(fill="x", padx=22, pady=4)
            ctk.CTkRadioButton(
                row, text=f"  {label}", variable=self.split_tunnel_var, value=val,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=ACCENT, hover_color=ACCENT_HOVER,
                radiobutton_width=18, radiobutton_height=18,
            ).pack(side="left", padx=16, pady=14)
            ctk.CTkLabel(
                row, text=desc, font=ctk.CTkFont(size=12), text_color=TXT_MUTED
            ).pack(side="left")

        ctk.CTkButton(
            parent, text="Split Tunnel Modunu Uygula", width=220, height=38,
            fg_color=ACCENT, hover_color=ACCENT_HOVER, corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.apply_split_tunnel,
        ).pack(anchor="w", padx=22, pady=(14, 18))
    def save_api_credentials(self, silent=False):
        self.config_data["api_token"] = self.token_entry.get().strip()
        self.config_data["account_id"] = self.acc_entry.get().strip()
        self.save_config()
        if not silent:
            self._show_modal("Kaydedildi", "API bilgileri başarıyla kaydedildi.", "success")

    def test_connection(self):
        self.save_api_credentials(silent=True)

        token = self.config_data.get("api_token", "").strip()
        acc   = self.config_data.get("account_id", "").strip()
        if not token or not acc:
            messagebox.showerror("Eksik Bilgi", "Lütfen önce API Token ve Account ID girin.")
            return

        def _test():
            results = []

            try:
                results.append("── Default Cihaz Politikası (/devices/policy) ──")
                res2 = self.api_request("GET", "/devices/policy")
                results.append(f"Başarı: {res2.get('success')}")
                policy = res2.get("result", {})
                if isinstance(policy, dict):
                    results.append(f"Politika Adı: {policy.get('name', 'Bulunamadı')}")
                    results.append(f"Politika ID: {policy.get('policy_id') or policy.get('id', 'Bulunamadı')}")
                    results.append(f"Tunnel Protokol: {policy.get('tunnel_protocol', 'Bilinmiyor')}")
                    results.append(f"Split Tunnel Modu: {policy.get('match', 'Bilinmiyor')}")
                    results.append("")
                    results.append("✔️ Include endpoint'i kullanılabilir: /devices/policy/include")
                else:
                    results.append(f"Beklenmeyen veri tipi: {type(policy)} - {str(policy)[:200]}")
            except Exception as e:
                results.append(f"HATA: {e}")

            results.append("")
            try:
                results.append("── Mevcut Include Listesi (/devices/policy/include) ──")
                res3 = self.api_request("GET", "/devices/policy/include")
                results.append(f"Başarı: {res3.get('success')}")
                includes = res3.get("result", []) or []
                results.append(f"Mevcut kural sayısı: {len(includes)}")
                if includes:
                    for item in includes[:5]:
                        if isinstance(item, dict):
                            results.append(f"  - {item.get('address') or item.get('host', '?')}")
                    if len(includes) > 5:
                        results.append(f"  ... ve {len(includes)-5} kural daha")
            except Exception as e:
                results.append(f"HATA: {e}")

            self.after(0, lambda: self._show_test_result("\n".join(results)))

        threading.Thread(target=_test, daemon=True).start()

    def _show_test_result(self, text):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Bağlantı Test Sonucu")
        dialog.geometry("620x420")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        ctk.CTkLabel(dialog, text="API Bağlantı Testi", font=ctk.CTkFont(size=17, weight="bold"), text_color=TXT_PRI).pack(pady=(18, 8))
        tb = ctk.CTkTextbox(dialog, font=ctk.CTkFont(family="Consolas", size=12), fg_color=SURFACE, text_color=TXT_PRI, border_width=1, border_color=BORDER)
        tb.pack(fill="both", expand=True, padx=18, pady=(0, 12))
        tb.insert("0.0", text)
        tb.configure(state="disabled")
        ctk.CTkButton(dialog, text="Kapat", command=dialog.destroy, fg_color=ACCENT, hover_color=ACCENT_HOVER, width=100).pack(pady=(0, 16))

    def apply_protocol(self):
        self.save_api_credentials(silent=True)
        proto = self.protocol_var.get()
        self.config_data["tunnel_protocol"] = proto
        self.save_config()
        try:
            # Default policy için ID olmadan direkt PATCH /devices/policy kullanılır
            res = self.api_request("PATCH", "/devices/policy", {"tunnel_protocol": proto})
            if res.get("success"):
                messagebox.showinfo("Başarılı", f"Protokol '{proto.upper()}' olarak değiştirildi!\n\nDeğişikliğin aktif olması için WARP istemcisini kapatıp yeniden açın.")
            else:
                errs = res.get("errors", [])
                err_msg = "\n".join([f"Kod {e.get('code','?')}: {e.get('message','')}" for e in errs]) if errs else str(res)
                messagebox.showerror("Hata", err_msg)
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    def apply_split_tunnel(self):
        self.save_api_credentials(silent=True)
        self.save_current_data()
        mode = self.split_tunnel_var.get()
        self.config_data["split_tunnel_mode"] = mode
        self.save_config()

        # Uygulamadaki TÜM kategorilerden entry listesini oluştur
        ip_pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}(/\d{1,2})?$")
        all_entries = []
        for cat_data in self.config_data["categories"].values():
            for e in cat_data.get("entries", []):
                if e not in all_entries:
                    all_entries.append(e)

        body = []
        for e in all_entries:
            if ip_pattern.match(e):
                if "/" not in e:
                    e += "/32"
                body.append({"address": e, "description": "WARPConfig"})
            else:
                body.append({"host": e, "description": "WARPConfig"})

        if not body:
            messagebox.showwarning(
                "Liste Boş",
                "Hiç IP veya domain eklenmemiş.\n\n"
                "Önce Yönlendirme sekmesinden en az bir IP veya domain ekleyin,\n"
                "ardından Split Tunnel modunu değiştirin."
            )
            return

        def _worker():
            try:
                if mode == "include":
                    # Include: uygulama listesini include'a yaz, exclude'u sıfırla
                    self.api_request("PUT", "/devices/policy/include", body)
                    self.api_request("PUT", "/devices/policy/exclude", [])
                    mode_label = "Include — Sadece belirlediğin IP/domain'ler WARP'tan geçer"
                else:
                    # Exclude: uygulama listesini exclude'a yaz, include'u sıfırla
                    self.api_request("PUT", "/devices/policy/exclude", body)
                    self.api_request("PUT", "/devices/policy/include", body)  # Include da dolu olsun, Cloudflare reddetmesin
                    mode_label = "Exclude — Belirlediğin IP/domain'ler WARP'ı atlar, diğerleri geçer"

                self.after(0, lambda: messagebox.showinfo(
                    "Başarılı",
                    f"Split Tunnel modu değiştirildi:\n{mode_label}\n\n"
                    f"Toplam {len(body)} kural uygulandı.\n"
                    "Değişikliğin aktif olması için WARP istemcisini kapatıp yeniden açın."
                ))
            except Exception as e:
                self.after(0, lambda err=str(e): messagebox.showerror("Hata", err))

        threading.Thread(target=_worker, daemon=True).start()

    def _section_quick_setup(self, parent):
        info = ctk.CTkFrame(parent, fg_color=SURFACE2, corner_radius=8)
        info.pack(fill="x", padx=22, pady=(14, 12))
        ctk.CTkLabel(
            info,
            text="Bu buton şunları otomatik yapar:\n"
                 "  ✓  Cihaz profili MASQUE protokolüne ayarlanır\n"
                 "  ✓  Split Tunnel modu Include'a alınır\n"
                 "  ✓  Yönlendirme sekmesindeki tüm IP/domain'ler Cloudflare'e yüklenir\n"
                 "  ✓  Enrollment Access Policy oluşturulur (sonra 1 tık bağlama gerekir)",
            font=ctk.CTkFont(size=12), text_color=TXT_SEC, justify="left",
        ).pack(anchor="w", padx=14, pady=10)

        ctk.CTkButton(
            parent, text="🚀  Kurulumu Uygula",
            height=46, corner_radius=8,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER,
            command=self.run_quick_setup,
        ).pack(fill="x", padx=22, pady=(0, 18))


    def run_quick_setup(self):
        self.save_api_credentials(silent=True)

        token = self.config_data.get("api_token", "").strip()
        acc   = self.config_data.get("account_id", "").strip()
        if not token or not acc:
            self._show_modal("Eksik Bilgi", "Lütfen önce API Token ve Account ID'yi Ayarlar'a girin.", "error")
            return

        # IP/domain kontrolü
        ip_pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}(/\d{1,2})?$")
        all_entries = []
        for cat_data in self.config_data["categories"].values():
            for e in cat_data.get("entries", []):
                if e not in all_entries:
                    all_entries.append(e)

        if not all_entries:
            self._show_modal(
                "Önce IP/Domain Ekle",
                "Henüz hiç IP veya domain eklenmemiş.\n\n"
                "Yönlendirme sekmesine gidip en az bir kategori için\n"
                "IP veya domain listesi ekle, sonra tekrar dene.",
                "warn",
                action_text="Yönlendirme'ye Git",
                action_cmd=lambda: self._navigate("routes"),
            )
            return

        body_list = []
        for e in all_entries:
            if ip_pattern.match(e):
                if "/" not in e:
                    e += "/32"
                body_list.append({"address": e, "description": "WARPConfig"})
            else:
                body_list.append({"host": e, "description": "WARPConfig"})

        results = []


        def _worker():
            # --- Adim 1: 'email' Access Policy olustur veya ID'sini bul ---
            access_policy_id = None
            try:
                pol_payload = {
                    "name": "email",
                    "decision": "allow",
                    "include": [{"email_domain": {"domain": "gmail.com"}}],
                    "session_duration": "0s",
                }
                res_create = self.api_request("POST", "/access/policies", pol_payload)
                if res_create.get("success"):
                    access_policy_id = res_create["result"]["id"]
                    results.append(f"✅ Access Policy oluşturuldu (ID: {access_policy_id})")
                else:
                    # Zaten varsa mevcut listede ara
                    res_list = self.api_request("GET", "/access/policies")
                    for p in (res_list.get("result") or []):
                        if isinstance(p, dict) and p.get("name") == "email":
                            access_policy_id = p["id"]
                            results.append(f"✅ Mevcut 'email' policy bulundu (ID: {access_policy_id})")
                            break
                    if not access_policy_id:
                        results.append(f"⚠️ Policy oluşturulamadı: {res_create.get('errors')}")
            except Exception as e:
                results.append(f"⚠️ Access Policy hatası: {e}")

            # --- Adim 2: Policy'yi Device Enrollment'a bagla ---
            # UI'daki "Select existing policies → Confirm" işleminin API karşılığı:
            # Policy ID referansı ile enrollment endpoint'e gönder
            enrollment_ok = False

            if access_policy_id:
                endpoints_to_try = [
                    # Sadece ID referansı ile (UI'nın yaptığı şey)
                    ("PUT", "/devices/policy/enrollment", [{"id": access_policy_id}]),
                    # Device policy ID'siyle
                    ("PUT", f"/devices/policy/enrollment_rules", [{"id": access_policy_id}]),
                    # Access app policy link
                    ("POST", "/access/apps/warp-enrollment/policies", {
                        "policy_id": access_policy_id,
                        "precedence": 1,
                    }),
                ]
                # Önce device policy ID'sini al
                try:
                    dp_res = self.api_request("GET", "/devices/policy")
                    dp_id = (dp_res.get("result") or {}).get("policy_id") or (dp_res.get("result") or {}).get("id")
                    if dp_id:
                        endpoints_to_try.insert(0, ("PUT", f"/devices/policy/{dp_id}/enrollment_rules", [{"id": access_policy_id}]))
                except Exception:
                    pass

                for method, ep, payload in endpoints_to_try:
                    if enrollment_ok:
                        break
                    try:
                        r = self.api_request(method, ep, payload)
                        if r.get("success"):
                            results.append(f"✅ Enrollment bağlandı ({ep})")
                            enrollment_ok = True
                        else:
                            errs = r.get("errors", [])
                            if any("already" in str(e).lower() or "exist" in str(e).lower() for e in errs):
                                results.append(f"✅ Enrollment zaten mevcut ({ep})")
                                enrollment_ok = True
                    except Exception:
                        pass

            if not enrollment_ok:
                results.append("")
                results.append("⚠️ Enrollment otomatik yapılamadı — 1 Manuel adım:")
                results.append("  Cloudflare → Team & Resources → Devices →")
                results.append("  Device enrollment permissions → Select existing policies")
                results.append(f"  → 'email' seçin → Confirm")



            # --- Adim 3: MASQUE protokolünü ayarla ---
            try:
                res3 = self.api_request("PATCH", "/devices/policy", {"tunnel_protocol": "masque"})
                if res3.get("success"):
                    results.append("✅ Tünel protokolü MASQUE olarak ayarlandı.")
                else:
                    results.append(f"⚠️ Protokol ayarlanamadı: {res3.get('errors')}")
            except Exception as e:
                results.append(f"❌ Protokol hatası: {e}")

            # --- Adim 4: Include listesini uygula ---
            if body_list:
                try:
                    res4 = self.api_request("PUT", "/devices/policy/include", body_list)
                    if res4.get("success"):
                        results.append(f"✅ Include listesi uygulandı ({len(body_list)} kural).")
                    else:
                        results.append(f"⚠️ Include listesi hatası: {res4.get('errors')}")
                except Exception as e:
                    results.append(f"❌ Include listesi oluşturulamadı: {e}")
            else:
                results.append("⚠️ Uygulama listesi boş — İP/domain ekleyip tekrar çalıştırın.")

            summary = "\n".join(results)
            self.after(0, lambda: self._show_setup_result(summary))

        threading.Thread(target=_worker, daemon=True).start()


    def _show_setup_result(self, summary):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Kurulum Sonucu")
        dialog.geometry("580x460")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        x = self.winfo_rootx() + (self.winfo_width() - dialog.winfo_width()) // 2
        y = self.winfo_rooty() + (self.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")

        ctk.CTkLabel(dialog, text="🚀  Kurulum Tamamlandı", font=ctk.CTkFont(size=17, weight="bold"), text_color=TXT_PRI).pack(pady=(18, 4))
        ctk.CTkLabel(dialog, text="Yapılan işlemler:", font=ctk.CTkFont(size=12), text_color=TXT_MUTED).pack()

        tb = ctk.CTkTextbox(dialog, font=ctk.CTkFont(family="Consolas", size=13), fg_color=SURFACE, text_color=TXT_PRI, border_width=1, border_color=BORDER, corner_radius=8)
        tb.pack(fill="both", expand=True, padx=18, pady=(8, 0))
        tb.insert("0.0", summary)
        tb.configure(state="disabled")

        enrollment_failed = "Enrollment otomatik yapılamadı" in summary or "⚠️ Enrollment" in summary
        if enrollment_failed:
            note = ctk.CTkFrame(dialog, fg_color="#2a1f00", corner_radius=8)
            note.pack(fill="x", padx=18, pady=(8, 0))
            ctk.CTkLabel(
                note,
                text="⚠️  Son 1 adım kaldı: Enrollment policy'yi bağla",
                font=ctk.CTkFont(size=13, weight="bold"), text_color="#ffcc44",
            ).pack(anchor="w", padx=14, pady=(8, 2))
            ctk.CTkLabel(
                note,
                text="Aşağıdaki butona tıkla → \"Select existing policies\" → \"email\" seç → \"Confirm\"",
                font=ctk.CTkFont(size=12), text_color=TXT_SEC,
            ).pack(anchor="w", padx=14, pady=(0, 8))

            account_id = self.config_data.get("account_id", "")
            enroll_url = (
                f"https://dash.cloudflare.com/{account_id}/one/team-resources/devices/edit?tab=rules"
                if account_id else "https://dash.cloudflare.com/"
            )

            ctk.CTkButton(
                note,
                text="🌐  Enrollment Sayfasını Aç",
                height=38, corner_radius=8,
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color="#f6821f", hover_color="#d4691a",
                command=lambda u=enroll_url: webbrowser.open(u),
            ).pack(fill="x", padx=14, pady=(0, 12))

        btn_row = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_row.pack(fill="x", padx=18, pady=(8, 14))
        ctk.CTkButton(btn_row, text="Kapat", command=dialog.destroy, fg_color=ACCENT, hover_color=ACCENT_HOVER, width=100).pack(side="right")

    # ── Cihazlar Sayfası ──────────────────────────────────────────────────────

    def _build_devices_page(self, page):
        top = ctk.CTkFrame(page, fg_color="transparent")
        top.pack(fill="x", padx=30, pady=(26, 16))
        ctk.CTkLabel(
            top, text="Bağlı Cihazlar",
            font=ctk.CTkFont(size=22, weight="bold"), text_color=TXT_PRI,
        ).pack(side="left")
        ctk.CTkButton(
            top, text="🔄  Yenile", width=110, height=38,
            fg_color=SURFACE, hover_color=SURFACE2,
            font=ctk.CTkFont(size=13), text_color=TXT_PRI,
            command=self.refresh_devices,
        ).pack(side="right")

        self.devices_scroll = ctk.CTkScrollableFrame(page, fg_color="transparent")
        self.devices_scroll.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        ctk.CTkLabel(
            self.devices_scroll,
            text="Cihazları görmek için Yenile butonuna basın.",
            font=ctk.CTkFont(size=14), text_color=TXT_MUTED,
        ).pack(pady=50)

    def refresh_devices(self):
        for w in self.devices_scroll.winfo_children():
            w.destroy()
        try:
            res     = self.api_request("GET", "/devices")
            devices = res.get("result", [])
            if not devices:
                ctk.CTkLabel(
                    self.devices_scroll,
                    text="Bağlı cihaz bulunamadı.", font=ctk.CTkFont(size=14), text_color=TXT_MUTED
                ).pack(pady=50)
                return
            for dev in devices:
                card = ctk.CTkFrame(self.devices_scroll, fg_color=SURFACE, corner_radius=10)
                card.pack(fill="x", pady=5)

                info = ctk.CTkFrame(card, fg_color="transparent")
                info.pack(side="left", padx=18, pady=14)

                name   = dev.get("name", "Bilinmeyen Cihaz")
                email  = dev.get("user", {}).get("email", "Bilinmeyen Kullanıcı")
                ip     = dev.get("ip", "IP Yok")
                dev_id = dev.get("id")

                ctk.CTkLabel(info, text=name, font=ctk.CTkFont(size=14, weight="bold"), text_color=TXT_PRI).pack(anchor="w")
                ctk.CTkLabel(info, text=f"{email}  ·  {ip}", font=ctk.CTkFont(size=12), text_color=TXT_SEC).pack(anchor="w")

                ctk.CTkButton(
                    card, text="Bağlantıyı Kes", width=140, height=36,
                    fg_color="transparent", border_width=1, border_color=DANGER,
                    text_color=DANGER, hover_color=DANGER, corner_radius=8,
                    font=ctk.CTkFont(size=13),
                    command=lambda d=dev_id: self.revoke_device(d),
                ).pack(side="right", padx=16)
        except Exception as e:
            ctk.CTkLabel(self.devices_scroll, text=f"Hata: {e}", text_color=DANGER).pack(pady=20)

    def revoke_device(self, dev_id):
        def _do_revoke():
            try:
                self.api_request("POST", f"/devices/{dev_id}/revoke")
                messagebox.showinfo("Başarılı", "Cihaz bağlantısı kesildi.")
                self.refresh_devices()
            except Exception as e:
                messagebox.showerror("Hata", str(e))
                
        self.ask_confirm("Cihaz Bağlantısını Kes", "Bu cihazın WARP bağlantısı kalıcı olarak kesilecek.\nOnaylıyor musunuz?", _do_revoke)

    # ── Kurulum Sayfası ────────────────────────────────────────────────────────

    def _build_guide_page(self, page):
        ctk.CTkLabel(
            page, text="Kurulum Rehberi",
            font=ctk.CTkFont(size=22, weight="bold"), text_color=TXT_PRI,
        ).pack(anchor="w", padx=30, pady=(26, 12))

        tb = ctk.CTkTextbox(page, wrap="word", font=ctk.CTkFont(size=14), fg_color=SURFACE, border_width=0, corner_radius=0)
        tb.pack(fill="both", expand=True, padx=30, pady=(0, 24))

        guide_tr = """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 WARP Configurator – Kurulum Rehberi
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Bu uygulama Cloudflare WARP'i istediğin IP ve domain'ler üzerinden
tunnel yapacak şekilde otomatik yapılandırır. ISP'nin engellediği
servislere (Discord, Roblox vb.) kolayca erişim sağlar.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADIM 1 – Cloudflare Zero Trust Hesabı Aç
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. cloudflare.com adresine gidip Google hesabınla kayıt ol.
2. Sol menüden "Zero Trust"'a tıkla.
3. "Takım adı" (team name) istenir — benzersiz bir isim yaz.
   └─ Bu ismi WARP client'ta giriş yaparken kullanacaksın!
4. Plan seçiminde en soldaki FREE seçeneğini seç.
5. Kart bilgisi istenir — sanal kart girebilirsin, ücret alınmaz.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADIM 2 – API Token ve Account ID Al
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

API Token:
1. dash.cloudflare.com → Sağ üst profil → My Profile → API Tokens
2. Create Token → Create Custom Token
3. İsim: WarpConfig  |  İzin: Account → Zero Trust → Edit
4. Continue to summary → Create Token → Kopyala ve kaydet!

Account ID:
  dash.cloudflare.com ana sayfasında sol altta ya da URL'de görünür.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADIM 3 – IP / Domain Listesi Ekle  (Kurulumdan ÖNCE yap!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  Kurulum butonu IP/domain olmadan çalışmaz!

1. Sol menüden "Yönlendirme" sekmesine geç.
2. İstediğin kategoriyi seç (Discord, Roblox vb.)
3. Sağ taraftaki alana IP'leri veya domain'leri yapıştır.
   └─ Kopyaladığın metinden sadece geçerli IP/domain'ler alınır.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADIM 4 – Hızlı Kurulumu Çalıştır
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. "API & Protokol" sekmesine git → Token ve ID'yi gir → Kaydet.
2. "Hızlı Kurulum" bölümündeki "🚀 Kurulumu Uygula" butonuna bas.
   → MASQUE protokolü ayarlanır
   → Include modu aktif edilir
   → Listeler Cloudflare'e yüklenir
   → Enrollment policy oluşturulur

3. Sonuç penceresinde "🌐 Enrollment Sayfasını Aç" butonuna tıkla.
4. "Select existing policies" → "email" seç → "Confirm" tıkla.
   ✓ Bitti! Enrollment tamamlandı.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADIM 5 – WARP Client Kur ve Bağlan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. one.one.one.one/warp adresinden WARP client'i indirip kur.
2. WARP → Settings → Account → Login with Cloudflare Zero Trust
3. Organizasyon adı = ADIM 1'de yazdığın takım adı.
4. Gmail ile giriş yap → WARP'i Connect et.
5. Disconnect → Connect yap (kuralların yüklenmesi için).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sık Karşılaşılan Hatalar
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✖ "Enrollment request is invalid"
  └─ ADIM 4'teki "Enrollment Sayfasını Aç" adımını atlamışsın.

✖ "API hatası: 403 / Unauthorized"
  └─ API Token'a "Zero Trust → Edit" izni verilmemiş. Yeniden oluştur.

✖ WARP bağlanıyor ama site açılmıyor
  └─ WARP'i disconnect edip connect et.
     Ayarlar → Tünel Protokolü'nün MASQUE olduğunu kontrol et.

✖ "Önce IP/Domain Ekle" uyarısı
  └─ ADIM 3'ü atlamışsın. Yönlendirme sekmesine git ve liste ekle.
"""
        tb.insert("0.0", guide_tr)
        tb.configure(state="disabled")



# ── Giriş Noktası ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()
