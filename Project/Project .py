import pygame
import pygame.gfxdraw
import numpy as np
import sys
import time
import math
import json
import re
from datetime import datetime

# Initialize Pygame
pygame.init()
pygame.font.init()

# Setup Virtual Screen (Scalable)
import os
os.environ['SDL_VIDEO_CENTERED'] = '1'
V_WIDTH, V_HEIGHT = 1920, 1080
initial_w, initial_h = 1280, 720
screen = pygame.display.set_mode((initial_w, initial_h), pygame.RESIZABLE | pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption("InventoryPro - Automated Inventory & Vendor Billing Ecosystem")
clock = pygame.time.Clock()

# --- THEME & CONSTANTS ---
BG_COLOR = (15, 15, 35)       # #0f0f23
CARD_COLOR = (30, 30, 63)     # #1e1e3f
ACCENT_COLOR = (0, 212, 255)  # #00d4ff
ALERT_COLOR = (255, 107, 107) # #ff6b6b
SUCCESS_COLOR = (46, 204, 113) # #2ecc71
TEXT_PRIMARY = (255, 255, 255)
TEXT_SECONDARY = (180, 180, 200)
BORDER_COLOR = (60, 60, 90)
HOVER_GLOW = (0, 255, 255)

# Fonts
try:
    FONT_HUGE = pygame.font.SysFont('segoeui', 64, bold=True)
    FONT_LARGE = pygame.font.SysFont('segoeui', 36, bold=True)
    FONT_MED = pygame.font.SysFont('segoeui', 24, bold=True)
    FONT_REG = pygame.font.SysFont('segoeui', 20)
    FONT_SMALL = pygame.font.SysFont('segoeui', 16)
except:
    FONT_HUGE = pygame.font.Font(None, 64)
    FONT_LARGE = pygame.font.Font(None, 36)
    FONT_MED = pygame.font.Font(None, 24)
    FONT_REG = pygame.font.Font(None, 20)
    FONT_SMALL = pygame.font.Font(None, 16)

# --- DATA STORES ---
np.random.seed(42)

# Dummy Vendors
vendors_data = [
    {"vendor_id": "V001", "name": "TechCorp Logistics", "contact": "John Doe", "email": "john@techcorp.com", "assoc_year": 2021, "total_purchases": 1500000.0},
    {"vendor_id": "V002", "name": "Global Electronics", "contact": "Jane Smith", "email": "jane@globalelec.com", "assoc_year": 2019, "total_purchases": 3200000.0},
    {"vendor_id": "V003", "name": "Prime Office Supplies", "contact": "Alan Wake", "email": "alan@primeoffice.com", "assoc_year": 2023, "total_purchases": 450000.0},
    {"vendor_id": "V004", "name": "NexGen Hardware", "contact": "Sarah Connor", "email": "sarah@nexgen.com", "assoc_year": 2020, "total_purchases": 2100000.0},
    {"vendor_id": "V005", "name": "Alpha Traders", "contact": "Mike Ross", "email": "mike@alpha.com", "assoc_year": 2024, "total_purchases": 120000.0},
]

# Dummy Items
items_data = [
    {"item_id": "I001", "name": "ThinkPad Carbon X1", "qty": 45, "price": 145000.0, "threshold": 10},
    {"item_id": "I002", "name": "Dell UltraSharp 27\"", "qty": 8, "price": 42000.0, "threshold": 15},
    {"item_id": "I003", "name": "Logitech MX Master 3", "qty": 120, "price": 8500.0, "threshold": 20},
    {"item_id": "I004", "name": "Keychron K8 Pro", "qty": 35, "price": 11000.0, "threshold": 10},
    {"item_id": "I005", "name": "ErgoChair Pro", "qty": 12, "price": 35000.0, "threshold": 15},
    {"item_id": "I006", "name": "Standing Desk 60\"", "qty": 5, "price": 28000.0, "threshold": 10},
    {"item_id": "I007", "name": "USB-C Hub Pro", "qty": 200, "price": 3500.0, "threshold": 50},
    {"item_id": "I008", "name": "Cat6 Ethernet Cable (10m)", "qty": 350, "price": 800.0, "threshold": 100},
    {"item_id": "I009", "name": "APC UPS 1500VA", "qty": 18, "price": 16500.0, "threshold": 20},
    {"item_id": "I010", "name": "Samsung 2TB NVMe SSD", "qty": 42, "price": 18000.0, "threshold": 15},
]

# --- UTILS / MATH ---
def lerp(a, b, t):
    return a + (b - a) * t

def format_inr(amount):
    s, *d = str(round(amount, 2)).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return f"₹ {r}{d[0]}{d[1].ljust(2, '0')}"

def ease_out_cubic(x):
    return 1 - pow(1 - x, 3)

def draw_rect_alpha(surface, color, rect, border_radius=0):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=border_radius)
    surface.blit(shape_surf, rect)

# --- PARTICLES & ANIMATIONS ---
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed, size, life):
        super().__init__()
        self.x, self.y = x, y
        self.color = color
        self.vx, self.vy = speed
        self.size = size
        self.life = life
        self.max_life = life
        
    def update(self, dt):
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.life -= dt
        
    def draw(self, surface):
        if self.life > 0:
            alpha = max(0, int((self.life / self.max_life) * 255))
            c = (*self.color[:3], alpha)
            surf = pygame.Surface((int(self.size*2), int(self.size*2)), pygame.SRCALPHA)
            pygame.draw.circle(surf, c, (int(self.size), int(self.size)), int(self.size))
            surface.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def emit(self, x, y, color, count=20, speed=5.0):
        for _ in range(count):
            angle = np.random.uniform(0, 2 * math.pi)
            s = np.random.uniform(1.0, speed)
            sz = np.random.uniform(2.0, 6.0)
            life = np.random.uniform(0.5, 1.5)
            self.particles.append(Particle(x, y, color, (math.cos(angle)*s, math.sin(angle)*s), sz, life))
            
    def update(self, dt):
        [p.update(dt) for p in self.particles]
        self.particles = [p for p in self.particles if p.life > 0]
        
    def draw(self, surface):
        [p.draw(surface) for p in self.particles]

particles = ParticleSystem()

# --- UI COMPONENTS ---
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, callback, icon=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.callback = callback
        self.icon = icon
        self.hover_factor = 0
        self.scale_factor = 1.0
        self.is_clicked = False

    def update(self, dt, mouse_pos, mouse_clicked):
        hovering = self.rect.collidepoint(mouse_pos)
        target_hover = 1.0 if hovering else 0.0
        self.hover_factor = lerp(self.hover_factor, target_hover, dt * 10)
        
        if hovering and mouse_clicked:
            self.is_clicked = True
            self.scale_factor = 0.95
            
        if self.is_clicked and not pygame.mouse.get_pressed()[0]:
            if hovering:
                self.callback()
            self.is_clicked = False
            
        self.scale_factor = lerp(self.scale_factor, 1.0, dt * 15)

    def draw(self, surface):
        c = [lerp(self.color[i], self.hover_color[i], self.hover_factor) for i in range(3)]
        
        # Scaling effect
        w = int(self.rect.width * self.scale_factor)
        h = int(self.rect.height * self.scale_factor)
        cx = self.rect.x + (self.rect.width - w) // 2
        cy = self.rect.y + (self.rect.height - h) // 2
        
        # Glow
        if self.hover_factor > 0.05:
            glow_rect = pygame.Rect(cx-5, cy-5, w+10, h+10)
            draw_rect_alpha(surface, (*ACCENT_COLOR, int(50 * self.hover_factor)), glow_rect, 15)

        pygame.draw.rect(surface, c, (cx, cy, w, h), border_radius=10)
        
        # Text
        text_surf = FONT_MED.render(self.text, True, TEXT_PRIMARY)
        text_rect = text_surf.get_rect(center=(cx + w//2, cy + h//2))
        surface.blit(text_surf, text_rect)

class TextInput:
    def __init__(self, x, y, w, h, placeholder=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.placeholder = placeholder
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.type_filter = None # None, 'int', 'float'

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isprintable():
                if self.type_filter == 'int' and not event.unicode.isdigit(): return
                if self.type_filter == 'float' and not (event.unicode.isdigit() or event.unicode == '.'): return
                self.text += event.unicode
                
    def update(self, dt):
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= 0.5:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0
        else:
            self.cursor_visible = False

    def draw(self, surface):
        color = ACCENT_COLOR if self.active else BORDER_COLOR
        # Background
        pygame.draw.rect(surface, CARD_COLOR, self.rect, border_radius=8)
        # Border
        pygame.draw.rect(surface, color, self.rect, width=2, border_radius=8)
        
        val = self.text if self.text else (self.placeholder if not self.active else "")
        c = TEXT_PRIMARY if self.text else TEXT_SECONDARY
        text_surf = FONT_REG.render(val, True, c)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + self.rect.height//2 - text_surf.get_height()//2))
        
        if self.cursor_visible:
            cx = self.rect.x + 10 + FONT_REG.size(self.text)[0] + 2
            pygame.draw.line(surface, TEXT_PRIMARY, (cx, self.rect.y + 10), (cx, self.rect.bottom - 10), 2)

class TableRenderer:
    def __init__(self, x, y, w, h, headers, col_widths):
        self.rect = pygame.Rect(x, y, w, h)
        self.headers = headers
        self.col_widths = col_widths # list of relative weights
        self.scroll_y = 0
        self.target_scroll_y = 0
        self.row_height = 60
        self.is_dragging = False
        self.last_my = 0

    def update(self, dt, rows_count, mouse_pos=None, mouse_clicked=False, actions_callback=None):
        self.scroll_y = lerp(self.scroll_y, self.target_scroll_y, dt * 15)
        max_scroll = max(0, (rows_count + 1) * self.row_height - self.rect.height)
        
        if self.target_scroll_y < -max_scroll: self.target_scroll_y = -max_scroll
        if self.target_scroll_y > 0: self.target_scroll_y = 0
        
        if not mouse_pos: mouse_pos = pygame.mouse.get_pos()
        
        # Check clicks for row callbacks
        if mouse_clicked and self.rect.collidepoint(mouse_pos) and actions_callback:
            local_y = mouse_pos[1] - (self.rect.y + self.row_height + self.scroll_y)
            if local_y >= 0:
                idx = int(local_y // self.row_height)
                if idx < rows_count:
                    actions_callback(idx)

        if pygame.mouse.get_pressed()[0]:
            if self.rect.collidepoint(mouse_pos) and not self.is_dragging:
                self.is_dragging = True
                self.last_my = mouse_pos[1]
            elif self.is_dragging:
                dy = mouse_pos[1] - self.last_my
                self.target_scroll_y += dy
                self.last_my = mouse_pos[1]
        else:
            self.is_dragging = False

    def handle_wheel(self, y):
        self.target_scroll_y += y * 40
        
    def draw(self, surface, data, actions_callback=None):
        # Clip surface for scrolling items
        clip_rect = pygame.Rect(self.rect.x, self.rect.y + self.row_height, self.rect.width, self.rect.height - self.row_height)
        
        total_weight = sum(self.col_widths)
        actual_widths = [int(self.rect.width * (w / total_weight)) for w in self.col_widths]
        
        # Draw Headers Background
        pygame.draw.rect(surface, (20, 20, 45), (self.rect.x, self.rect.y, self.rect.width, self.row_height), border_top_left_radius=10, border_top_right_radius=10)
        
        curr_x = self.rect.x
        for i, h in enumerate(self.headers):
            text_surf = FONT_MED.render(h, True, ACCENT_COLOR)
            surface.blit(text_surf, (curr_x + 20, self.rect.y + 15))
            curr_x += actual_widths[i]

        surface.set_clip(clip_rect)
        
        y_offset = self.rect.y + self.row_height + self.scroll_y
        mouse_pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]
        
        for idx, row in enumerate(data):
            row_rect = pygame.Rect(self.rect.x, y_offset, self.rect.width, self.row_height)
            
            if row_rect.bottom > clip_rect.top and row_rect.top < clip_rect.bottom:
                bg = CARD_COLOR if idx % 2 == 0 else (35, 35, 70)
                hovering = row_rect.collidepoint(mouse_pos)
                if hovering: bg = (45, 45, 85)
                
                pygame.draw.rect(surface, bg, row_rect)
                pygame.draw.line(surface, BORDER_COLOR, (row_rect.x, row_rect.bottom), (row_rect.right, row_rect.bottom))
                
                curr_x = self.rect.x
                for i, cell in enumerate(row):
                    # Value formatting based on type or tuple flags could be done here
                    color = TEXT_PRIMARY
                    if isinstance(cell, float) or isinstance(cell, int):
                        pass
                    
                    # Custom format logic injected via cell strings: "!C:R"
                    val = str(cell)
                    if val.startswith("!ALERT!"):
                        val = val.replace("!ALERT!", "")
                        color = ALERT_COLOR
                    elif val.startswith("!INR!"):
                        try:
                            val = format_inr(float(val.replace("!INR!", "")))
                        except: pass
                    elif val.startswith("!DELETE!"):
                        val = val.replace("!DELETE!", "")
                        color = ALERT_COLOR
                    
                    text_surf = FONT_REG.render(val, True, color)
                    surface.blit(text_surf, (curr_x + 20, y_offset + 18))
                    curr_x += actual_widths[i]

            y_offset += self.row_height
            
        surface.set_clip(None)

        # Container border
        pygame.draw.rect(surface, BORDER_COLOR, self.rect, width=2, border_radius=10)

class NotificationManager:
    def __init__(self):
        self.notes = []
        
    def add(self, msg, type="info"):
        self.notes.append({"msg": msg, "type": type, "life": 3.0, "max": 3.0, "y_off": 50})
        
    def update(self, dt):
        for n in self.notes:
            n['life'] -= dt
            n['y_off'] = lerp(n['y_off'], 0, dt * 10)
        self.notes = [n for n in self.notes if n['life'] > 0]
        
    def draw(self, surface):
        for i, n in enumerate(self.notes):
            alpha = min(255, int((n['life'] / 0.5) * 255)) if n['life'] < 0.5 else 255
            color = ALERT_COLOR if n['type'] == "error" else SUCCESS_COLOR if n['type'] == "success" else ACCENT_COLOR
            
            rect = pygame.Rect(V_WIDTH - 420, 20 + i*70 + n['y_off'], 400, 60)
            draw_rect_alpha(surface, (*CARD_COLOR, alpha), rect, 10)
            pygame.draw.rect(surface, (*color, alpha), rect, width=2, border_radius=10)
            
            surf = FONT_MED.render(n['msg'], True, (*TEXT_PRIMARY, alpha))
            surface.blit(surf, (rect.x + 20, rect.y + 15))


class Modal:
    def __init__(self, title, width, height):
        self.active = False
        self.title = title
        self.rect = pygame.Rect(V_WIDTH//2 - width//2, V_HEIGHT//2 - height//2, width, height)
        self.alpha = 0
        self.scale = 0.8
        self.inputs = {}
        self.buttons = []
        self.on_submit = None

    def open(self):
        self.active = True
        self.scale = 0.8
        self.alpha = 0
        self.inputs = {}
        self.buttons = []
        
    def add_input(self, key, x_off, y_off, w, h, placeholder, val=""):
        ti = TextInput(self.rect.x + x_off, self.rect.y + y_off, w, h, placeholder)
        ti.text = str(val)
        self.inputs[key] = ti
        
    def add_button(self, key, x_off, y_off, w, h, text, color, cb):
        def wrap():
            cb(self.inputs)
            self.active = False
        btn = Button(self.rect.x + x_off, self.rect.y + y_off, w, h, text, color, HOVER_GLOW, wrap)
        self.buttons.append(btn)
        
    def close(self):
        self.active = False

    def handle_event(self, event):
        if not self.active: return
        for ti in self.inputs.values(): ti.handle_event(event)

    def update(self, dt, mouse_pos, clicked):
        if not self.active: return
        self.alpha = lerp(self.alpha, 255, dt * 15)
        self.scale = lerp(self.scale, 1.0, dt * 15)
        for ti in self.inputs.values(): ti.update(dt)
        for btn in self.buttons: btn.update(dt, mouse_pos, clicked)
        
    def draw(self, surface):
        if not self.active: return
        
        # Overlay
        draw_rect_alpha(surface, (0,0,0, int(self.alpha * 0.6)), (0,0, V_WIDTH, V_HEIGHT))
        
        # Transform modal logic
        w = int(self.rect.width * self.scale)
        h = int(self.rect.height * self.scale)
        cx = self.rect.x + (self.rect.width - w) // 2
        cy = self.rect.y + (self.rect.height - h) // 2
        
        m_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(m_surf, (*CARD_COLOR, int(self.alpha)), m_surf.get_rect(), border_radius=15)
        pygame.draw.rect(m_surf, (*BORDER_COLOR, int(self.alpha)), m_surf.get_rect(), width=2, border_radius=15)
        
        # Title
        tsurf = FONT_LARGE.render(self.title, True, (*TEXT_PRIMARY, int(self.alpha)))
        m_surf.blit(tsurf, (30, 20))
        pygame.draw.line(m_surf, (*BORDER_COLOR, int(self.alpha)), (0, 70), (self.rect.width, 70), 2)
        
        # Render fields shifted by offset relative to modal surf
        for ti in self.inputs.values():
            trect = ti.rect.copy()
            ti.rect.x -= self.rect.x
            ti.rect.y -= self.rect.y
            ti.draw(m_surf)
            ti.rect = trect
            
        for btn in self.buttons:
            brect = btn.rect.copy()
            btn.rect.x -= self.rect.x
            btn.rect.y -= self.rect.y
            btn.draw(m_surf)
            btn.rect = brect
            
        # Blit scaled modal
        scaled = pygame.transform.smoothscale(m_surf, (w, h))
        surface.blit(scaled, (cx, cy))


# --- MAIN APPLICATION FRAMEWORK ---
class AppManager:
    def __init__(self):
        self.state = 'dashboard'
        self.sidebar_y = 0
        self.notifications = NotificationManager()
        self.modal = Modal("Add Item", 500, 600)
        
        # State Data Views
        self.views = {
            'dashboard': self.draw_dashboard,
            'inventory': self.draw_inventory,
            'vendors': self.draw_vendors,
            'search': self.draw_search,
            'report': self.draw_report
        }
        
        # Sidebar Setup
        self.nav_items = ['Dashboard', 'Inventory', 'Vendors', 'Search', 'Report']
        self.nav_hovers = [0.0] * len(self.nav_items)
        
        self.setup_ui_elements()
        self.check_low_stock()
        
    def setup_ui_elements(self):
        # Inventory Elements
        self.inv_table = TableRenderer(320, 150, 1550, 850, ["ID", "Name", "Qty", "Price", "Threshold", "Action"], [1, 3, 1, 2, 1, 1.5])
        self.btn_add_item = Button(1670, 70, 200, 50, "+ New Item", ACCENT_COLOR, (0, 255, 255), self.open_add_item_modal)
        
        # Vendors Elements
        self.ven_table = TableRenderer(320, 150, 1550, 850, ["ID", "Name", "Contact", "Since", "Total Purchases"], [1, 3, 2, 1, 2])
        self.btn_add_vendor = Button(1670, 70, 200, 50, "+ New Vendor", ACCENT_COLOR, (0, 255, 255), self.open_add_vendor_modal)
        
        # Search Element
        self.search_input = TextInput(320, 100, 1000, 60, "Type to search by Item ID or Name...")
        self.btn_search = Button(1350, 100, 150, 60, "Search", CARD_COLOR, ACCENT_COLOR, lambda: None)
        
        # Analytics state initialized lazily
        self.last_search_query = ""

    def save_data(self):
        # Simulate saving to text representation
        state_str = {"items": items_data, "vendors": vendors_data}
        try:
            with open("ecosystem_db.json", "w") as f:
                json.dump(state_str, f)
            self.notifications.add("Data Auto-Saved locally.", "success")
        except: pass

    def open_add_item_modal(self):
        self.modal = Modal("Add New Inventory Item", 500, 500)
        self.modal.open()
        self.modal.add_input('id', 50, 100, 400, 50, "Item ID (e.g., I011)")
        self.modal.add_input('name', 50, 170, 400, 50, "Item Name")
        self.modal.add_input('qty', 50, 240, 190, 50, "Quantity (int)")
        self.modal.inputs['qty'].type_filter = 'int'
        self.modal.add_input('price', 260, 240, 190, 50, "Price (float)")
        self.modal.inputs['price'].type_filter = 'float'
        self.modal.add_input('thresh', 50, 310, 400, 50, "Low Stock Threshold")
        self.modal.inputs['thresh'].type_filter = 'int'
        
        def save(inputs):
            try:
                id_text = inputs['id'].text.strip() or "I999"
                name_text = inputs['name'].text.strip() or "Unnamed Item"
                qty_text = inputs['qty'].text.strip() or "0"
                price_text = inputs['price'].text.strip() or "0"
                thresh_text = inputs['thresh'].text.strip() or "0"
                
                items_data.append({
                    "item_id": id_text,
                    "name": name_text,
                    "qty": int(qty_text),
                    "price": float(price_text),
                    "threshold": int(thresh_text)
                })
                particles.emit(V_WIDTH//2, V_HEIGHT//2, ACCENT_COLOR, 50, 8.0)
                self.notifications.add("Item successfully added!", "success")
                self.check_low_stock()
                self.save_data()
            except ValueError:
                self.notifications.add("Invalid input fields!", "error")
                
        self.modal.add_button('save', 50, 400, 190, 50, "Save", SUCCESS_COLOR, save)
        self.modal.add_button('cancel', 260, 400, 190, 50, "Cancel", ALERT_COLOR, lambda x: None)

    def prompt_delete_item(self, idx):
        if idx >= len(items_data): return
        item = items_data[idx]
        self.modal = Modal(f"Delete {item['item_id']}?", 500, 250)
        self.modal.open()
        
        def confirm(inputs):
            if idx < len(items_data):
                del items_data[idx]
                self.notifications.add("Item successfully deleted.", "success")
                self.save_data()
                self.check_low_stock()
                
        self.modal.add_button('confirm', 50, 120, 190, 50, "Confirm Delete", ALERT_COLOR, confirm)
        self.modal.add_button('cancel', 260, 120, 190, 50, "Cancel", (60, 60, 90), lambda x: None)

    def open_add_vendor_modal(self):
        self.modal = Modal("Add New Vendor", 500, 550)
        self.modal.open()
        self.modal.add_input('id', 50, 100, 400, 50, "Vendor ID")
        self.modal.add_input('name', 50, 170, 400, 50, "Vendor Name")
        self.modal.add_input('contact', 50, 240, 400, 50, "Contact Name")
        self.modal.add_input('email', 50, 310, 400, 50, "Email")
        
        def save(inputs):
            vendors_data.append({
                "vendor_id": inputs['id'].text.strip() or "V999",
                "name": inputs['name'].text.strip() or "Unnamed Vendor",
                "contact": inputs['contact'].text.strip() or "N/A",
                "email": inputs['email'].text.strip() or "N/A",
                "assoc_year": datetime.now().year,
                "total_purchases": 0.0
            })
            self.notifications.add("Vendor added!", "success")
            self.save_data()
            
        self.modal.add_button('save', 50, 430, 400, 50, "Save Vendor", ACCENT_COLOR, save)

    def check_low_stock(self):
        if not items_data: return
        dt = np.array([(item['qty'], item['threshold']) for item in items_data])
        low_stocks = np.sum(dt[:, 0] < dt[:, 1])
        if low_stocks > 0:
            particles.emit(100, 100, ALERT_COLOR, 30, 6.0)
            self.notifications.add(f"ALERT: {low_stocks} item(s) below threshold!", "error")

    def update(self, dt, mouse_pos, clicked):
        target_cursor = pygame.SYSTEM_CURSOR_ARROW
        particles.update(dt)
        self.notifications.update(dt)
        if self.modal.active:
            self.modal.update(dt, mouse_pos, clicked)
            for btn in self.modal.buttons:
                if btn.rect.collidepoint(mouse_pos): target_cursor = pygame.SYSTEM_CURSOR_HAND
            for ti in self.modal.inputs.values():
                if ti.rect.collidepoint(mouse_pos): target_cursor = pygame.SYSTEM_CURSOR_IBEAM
            pygame.mouse.set_cursor(target_cursor)
            return # Block updates to background
            
        # Sidebar interactions
        sidebar_rect = pygame.Rect(0, 0, 280, V_HEIGHT)
        for i, nav in enumerate(self.nav_items):
            rect = pygame.Rect(20, 150 + i*70, 240, 50)
            hovering = rect.collidepoint(mouse_pos)
            if hovering: target_cursor = pygame.SYSTEM_CURSOR_HAND
            self.nav_hovers[i] = lerp(self.nav_hovers[i], 1.0 if hovering else 0.0, dt*15)
            if hovering and clicked:
                if self.state != nav.lower():
                    self.state = nav.lower()
                    if self.state == 'report': self.generate_confetti()
        
        # State updates
        if self.state == 'inventory':
            self.btn_add_item.update(dt, mouse_pos, clicked)
            if self.btn_add_item.rect.collidepoint(mouse_pos): target_cursor = pygame.SYSTEM_CURSOR_HAND
            self.inv_table.update(dt, len(items_data), mouse_pos, clicked, self.prompt_delete_item)
            if self.inv_table.rect.collidepoint(mouse_pos):
                local_y = mouse_pos[1] - (self.inv_table.rect.y + self.inv_table.row_height + self.inv_table.scroll_y)
                if local_y >= 0 and int(local_y // self.inv_table.row_height) < len(items_data):
                    target_cursor = pygame.SYSTEM_CURSOR_HAND
        elif self.state == 'vendors':
            self.btn_add_vendor.update(dt, mouse_pos, clicked)
            if self.btn_add_vendor.rect.collidepoint(mouse_pos): target_cursor = pygame.SYSTEM_CURSOR_HAND
            self.ven_table.update(dt, len(vendors_data), mouse_pos, clicked)
        elif self.state == 'search':
            self.search_input.update(dt)
            if self.search_input.rect.collidepoint(mouse_pos): target_cursor = pygame.SYSTEM_CURSOR_IBEAM
            
        pygame.mouse.set_cursor(target_cursor)

    def generate_confetti(self):
        for _ in range(5):
            x = np.random.randint(300, V_WIDTH)
            particles.emit(x, V_HEIGHT, (np.random.randint(100, 255), np.random.randint(100, 255), np.random.randint(100, 255)), 20, 10)

    def handle_event(self, event):
        if self.modal.active:
            self.modal.handle_event(event)
            return
            
        if self.state == 'inventory' and event.type == pygame.MOUSEWHEEL:
            self.inv_table.handle_wheel(event.y)
        elif self.state == 'vendors' and event.type == pygame.MOUSEWHEEL:
            self.ven_table.handle_wheel(event.y)
        elif self.state == 'search':
            self.search_input.handle_event(event)
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.save_data()

    def draw_sidebar(self, surface):
        pygame.draw.rect(surface, CARD_COLOR, (0, 0, 280, V_HEIGHT))
        pygame.draw.line(surface, BORDER_COLOR, (280, 0), (280, V_HEIGHT), 2)
        
        # Logo
        logo = FONT_LARGE.render("InvPro", True, ACCENT_COLOR)
        surface.blit(logo, (80, 40))
        pygame.draw.circle(surface, ACCENT_COLOR, (45, 60), 15, 3)
        pygame.draw.circle(surface, ALERT_COLOR, (55, 70), 8)
        
        # Nav links
        for i, nav in enumerate(self.nav_items):
            is_active = self.state == nav.lower()
            rect = pygame.Rect(20, 150 + i*70, 240, 50)
            
            # Hover/Active background
            bg_alpha = int(self.nav_hovers[i] * 50) + (100 if is_active else 0)
            draw_rect_alpha(surface, (*ACCENT_COLOR, bg_alpha), rect, 10)
            
            # Text
            c = ACCENT_COLOR if is_active else TEXT_PRIMARY
            text = FONT_MED.render(nav, True, c)
            x_off = int(self.nav_hovers[i] * 10) + (10 if is_active else 0)
            surface.blit(text, (rect.x + 40 + x_off, rect.y + 10))
            
            if is_active:
                pygame.draw.rect(surface, ACCENT_COLOR, (rect.x-5, rect.y+10, 5, 30), border_radius=3)

    def draw_dashboard(self, surface):
        text = FONT_HUGE.render("Ecosystem Dashboard", True, TEXT_PRIMARY)
        surface.blit(text, (320, 50))
        
        # Stats Cards (Using Numpy)
        if items_data:
            qty_arr = np.array([i['qty'] for i in items_data])
            price_arr = np.array([i['price'] for i in items_data])
            thresh_arr = np.array([i['threshold'] for i in items_data])
            val_arr = qty_arr * price_arr
        else:
            qty_arr = price_arr = thresh_arr = val_arr = np.array([0])
            
        total_items = int(np.sum(qty_arr))
        total_value = float(np.sum(val_arr))
        low_stock = int(np.sum(qty_arr < thresh_arr))
        
        cards = [
            ("Total Stock Value", format_inr(total_value), ACCENT_COLOR),
            ("Total Stock Count", f"{total_items} Units", SUCCESS_COLOR),
            ("Low Stock Items", str(low_stock), ALERT_COLOR)
        ]
        
        for i, (title, val, col) in enumerate(cards):
            r = pygame.Rect(320 + i*420, 180, 380, 160)
            pygame.draw.rect(surface, CARD_COLOR, r, border_radius=15)
            pygame.draw.rect(surface, col, r, width=2, border_radius=15)
            surface.blit(FONT_MED.render(title, True, TEXT_SECONDARY), (r.x + 20, r.y + 20))
            surface.blit(FONT_LARGE.render(val, True, col), (r.x + 20, r.y + 80))
            
        # Draw Pie Chart background simulation
        pygame.draw.rect(surface, CARD_COLOR, (320, 380, 1220, 600), border_radius=15)
        surface.blit(FONT_LARGE.render("Stock Distribution by Value", True, TEXT_PRIMARY), (350, 410))
        
        if len(val_arr) > 1:
            total = float(np.sum(val_arr))
            if total > 0:
                angles = (val_arr / total) * 360
                start_a = 0
                cx, cy = 600, 680
                radius = 200
                
                for i, a in enumerate(angles):
                    end_a = start_a + a
                    color = (min(255, 50+i*30), min(255, 100+i*15), 255)
                    # Draw pie slice polygon
                    pts = [(cx, cy)]
                    for deg in range(int(start_a), int(end_a+2)):
                        rad = math.radians(deg)
                        pts.append((cx + math.cos(rad)*radius, cy + math.sin(rad)*radius))
                    if len(pts) > 2:
                        pygame.draw.polygon(surface, color, pts)
                        pygame.draw.polygon(surface, BG_COLOR, pts, 2)
                        
                    # Legend
                    if i < 8:
                        pygame.draw.rect(surface, color, (900, 500 + i*40, 20, 20))
                        surface.blit(FONT_REG.render(f"{items_data[i]['name'][:20]}... ({val_arr[i]/total*100:.1f}%)", True, TEXT_SECONDARY), (930, 500 + i*40))
                    start_a = end_a

    def draw_inventory(self, surface):
        surface.blit(FONT_HUGE.render("Inventory Management", True, TEXT_PRIMARY), (320, 50))
        self.btn_add_item.draw(surface)
        
        # Prepare Data
        t_data = []
        for i in items_data:
            qty_str = f"!ALERT!{i['qty']}" if i['qty'] < i['threshold'] else str(i['qty'])
            t_data.append([i['item_id'], i['name'], qty_str, f"!INR!{i['price']}", i['threshold'], "!DELETE![ DELETE ITEM ]"])
            
        self.inv_table.draw(surface, t_data)

    def draw_vendors(self, surface):
        surface.blit(FONT_HUGE.render("Vendor Register", True, TEXT_PRIMARY), (320, 50))
        self.btn_add_vendor.draw(surface)
        
        t_data = []
        for v in vendors_data:
            t_data.append([v['vendor_id'], v['name'], v['contact'], v['assoc_year'], f"!INR!{v['total_purchases']}"])
        self.ven_table.draw(surface, t_data)

    def draw_search(self, surface):
        surface.blit(FONT_HUGE.render("Universal Search", True, TEXT_PRIMARY), (320, 20))
        self.search_input.draw(surface)
        
        q = self.search_input.text.lower()
        if not q:
            surface.blit(FONT_LARGE.render("Enter query to search items & vendors...", True, TEXT_SECONDARY), (320, 200))
            return
            
        y_off = 200
        found = False
        
        # Search Items
        for item in items_data:
            if q in item['item_id'].lower() or q in item['name'].lower():
                found = True
                rect = pygame.Rect(320, y_off, 1200, 60)
                pygame.draw.rect(surface, CARD_COLOR, rect, border_radius=8)
                surface.blit(FONT_MED.render(f"ITEM: {item['item_id']} - {item['name']}", True, ACCENT_COLOR), (340, y_off+15))
                surface.blit(FONT_REG.render(f"Qty: {item['qty']} | Price: {format_inr(item['price'])}", True, TEXT_SECONDARY), (900, y_off+18))
                y_off += 70
                
        # Search Vendors
        for v in vendors_data:
            if q in v['vendor_id'].lower() or q in v['name'].lower() or q in v['contact'].lower():
                found = True
                rect = pygame.Rect(320, y_off, 1200, 60)
                pygame.draw.rect(surface, (45, 35, 60), rect, border_radius=8)
                surface.blit(FONT_MED.render(f"VENDOR: {v['vendor_id']} - {v['name']}", True, (255, 100, 255)), (340, y_off+15))
                surface.blit(FONT_REG.render(f"Contact: {v['contact']} | {v['email']}", True, TEXT_SECONDARY), (800, y_off+18))
                y_off += 70
                
        if not found:
            surface.blit(FONT_LARGE.render("No results found.", True, ALERT_COLOR), (320, 200))

    def draw_report(self, surface):
        # Numpy Analytics Calculation on demand
        qty_arr = np.array([i['qty'] for i in items_data]) if items_data else np.array([0])
        price_arr = np.array([i['price'] for i in items_data]) if items_data else np.array([0])
        t_arr = np.array([i['threshold'] for i in items_data]) if items_data else np.array([0])
        sales = np.sum(qty_arr * price_arr)
        avg_price = np.mean(price_arr) if len(price_arr)>0 else 0
        low_count = np.sum(qty_arr < t_arr)
        
        # Draw Report Modal background
        r = pygame.Rect(320, 80, 1500, 900)
        pygame.draw.rect(surface, CARD_COLOR, r, border_radius=20)
        pygame.draw.rect(surface, ACCENT_COLOR, r, width=3, border_radius=20)
        
        surface.blit(FONT_HUGE.render("Annual Purchase & Inventory Report", True, TEXT_PRIMARY), (360, 110))
        surface.blit(FONT_MED.render(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", True, TEXT_SECONDARY), (360, 180))
        pygame.draw.line(surface, BORDER_COLOR, (360, 220), (1750, 220), 2)
        
        # Summary Stats
        stats = [
            ("Total Portfolio Valuation", format_inr(sales), SUCCESS_COLOR),
            ("Average Unit Price", format_inr(avg_price), ACCENT_COLOR),
            ("At-Risk Items (Low Stock)", str(low_count), ALERT_COLOR)
        ]
        
        for i, (title, val, col) in enumerate(stats):
            sr = pygame.Rect(360 + i*480, 250, 450, 150)
            pygame.draw.rect(surface, (20,20,40), sr, border_radius=15)
            surface.blit(FONT_MED.render(title, True, TEXT_SECONDARY), (sr.x + 20, sr.y + 20))
            surface.blit(FONT_LARGE.render(val, True, col), (sr.x + 20, sr.y + 70))
            
        # Top Vendors Table
        surface.blit(FONT_LARGE.render("Top Vendors by Historical Volume", True, TEXT_PRIMARY), (360, 450))
        
        # Sort vendors using numpy indirect sort for showcase
        if vendors_data:
            v_names = np.array([v['name'] for v in vendors_data])
            v_purch = np.array([v['total_purchases'] for v in vendors_data])
            sorted_idx = np.argsort(v_purch)[::-1] # descending
            
            y_off = 510
            for i in range(min(5, len(sorted_idx))):
                idx = sorted_idx[i]
                pygame.draw.rect(surface, (25, 25, 50), (360, y_off, 1400, 60), border_radius=8)
                surface.blit(FONT_MED.render(f"#{i+1}  {v_names[idx]}", True, TEXT_PRIMARY), (380, y_off+15))
                surface.blit(FONT_LARGE.render(format_inr(v_purch[idx]), True, ACCENT_COLOR), (1450, y_off+10))
                # Bar chart inline
                bar_w = int((v_purch[idx] / np.max(v_purch)) * 600) if np.max(v_purch)>0 else 0
                pygame.draw.rect(surface, ACCENT_COLOR, (800, y_off+20, bar_w, 20), border_radius=10)
                y_off += 70

    def draw(self, surface):
        surface.fill(BG_COLOR)
        
        # Action Views
        self.views[self.state](surface)
        
        # Sidebar over everything else except modal/particles
        self.draw_sidebar(surface)
        
        particles.draw(surface)
        self.notifications.draw(surface)
        self.modal.draw(surface)


# --- MAIN GAME LOOP ---
def main():
    app = AppManager()
    
    virtual_surface = pygame.Surface((V_WIDTH, V_HEIGHT))
    running = True
    last_time = time.time()
    
    while running:
        dt = time.time() - last_time
        dt = min(dt, 0.1) # limit maximum delta
        last_time = time.time()
        
        # Real-to-virtual mouse transformation
        cw, ch = screen.get_size()
        scale_x = cw / V_WIDTH
        scale_y = ch / V_HEIGHT
        
        raw_mouse = pygame.mouse.get_pos()
        v_mouse_pos = (int(raw_mouse[0] / scale_x), int(raw_mouse[1] / scale_y))
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
            
            # Map event positions to virtual
            if hasattr(event, 'pos'):
                event.pos = (int(event.pos[0] / scale_x), int(event.pos[1] / scale_y))
                
            app.handle_event(event)

        app.update(dt, v_mouse_pos, mouse_clicked)
        app.draw(virtual_surface)
        
        # Scale to window
        scaled_surf = pygame.transform.smoothscale(virtual_surface, (cw, ch))
        screen.blit(scaled_surf, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
