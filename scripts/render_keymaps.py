#!/usr/bin/env python3
import json
import math
import os
import cairo

# Theme colors
COLORS = {
    'bg': (0.09, 0.10, 0.14),           # #171923
    'card_bg': (0.12, 0.14, 0.20),      # #1f2333
    'key_default': (0.18, 0.20, 0.28),  # #2e3447
    'key_border': (0.26, 0.29, 0.40),   # #424a66
    
    # Text colors
    'text_main': (0.95, 0.96, 0.98),
    'text_sub': (0.60, 0.65, 0.78),
    'text_trans': (0.30, 0.33, 0.45),
    'trans_key': (0.13, 0.15, 0.21),
    'trans_border': (0.18, 0.20, 0.28),
    
    # Category highlights
    'alpha': (0.20, 0.23, 0.32),
    'mod': (0.25, 0.22, 0.38),          # purple-blue
    'mod_border': (0.45, 0.38, 0.70),
    'mod_tap': (0.22, 0.28, 0.38),
    'mod_tap_border': (0.35, 0.50, 0.75),
    'nav': (0.18, 0.30, 0.30),          # teal
    'nav_border': (0.28, 0.55, 0.55),
    'symbol': (0.28, 0.25, 0.20),       # amber
    'symbol_border': (0.60, 0.50, 0.25),
    'fn': (0.22, 0.28, 0.22),           # muted green
    'fn_border': (0.35, 0.55, 0.35),
    'layer': (0.35, 0.20, 0.18),        # orange/coral
    'layer_border': (0.75, 0.40, 0.25),
    'special': (0.28, 0.20, 0.30),      # magenta
    'special_border': (0.60, 0.35, 0.65),
    'num': (0.18, 0.26, 0.35),          # blue
    'num_border': (0.30, 0.50, 0.75),
    'bt': (0.15, 0.25, 0.40),           # deep blue
    'bt_border': (0.30, 0.55, 0.90),
    'rgb': (0.35, 0.18, 0.28),          # pink
    'rgb_border': (0.75, 0.35, 0.60),
    'sys': (0.35, 0.18, 0.18),          # red
    'sys_border': (0.75, 0.30, 0.30),
    'space': (0.22, 0.25, 0.35),
    'space_border': (0.40, 0.45, 0.65),
    'encoder': (0.20, 0.32, 0.28),      # emerald
    'encoder_border': (0.30, 0.65, 0.55),
}

CORNE_LAYERS = [
    {
        'id': 'corne_layer_0_qwerty',
        'title': 'Corne Choc Pro — Layer 0: QWERTY (Base)',
        'subtitle': '46-key layout with Rotary Encoders, German Alt-Gr shortcuts & Mod-Taps',
        'footer': 'Sensors: Left 1 = Vol Down/Up | Left 2 = PgUp/PgDn | Right 1 = Prev/Next Track | Right 2 = Brightness Down/Up',
        'keys': [
            # Row 0 (14 keys)
            ("ESC", "", "nav"), ("Q", "", "alpha"), ("W", "", "alpha"), ("E", "", "alpha"), ("R", "", "alpha"), ("T", "", "alpha"),
            ("VOL+", "🔊", "encoder"), ("PG UP", "⇞", "nav"),
            ("Y", "", "alpha"), ("U", "", "alpha"), ("I", "", "alpha"), ("O", "", "alpha"), ("P", "", "alpha"), ("BSPC", "⌫", "nav"),
            # Row 1 (14 keys)
            ("TAB", "⇥", "mod"), ("A", "", "alpha"), ("S", "", "alpha"), ("D", "", "alpha"), ("F", "", "alpha"), ("G", "", "alpha"),
            ("VOL-", "Hold: MUTE", "encoder"), ("PG DN", "⇟", "nav"),
            ("H", "", "alpha"), ("J", "", "alpha"), ("K", "", "alpha"), ("L", "", "alpha"), (";", ":", "alpha"), ("'", "Hold: `", "mod_tap"),
            # Row 2 (12 keys)
            ("SHIFT", "⇧", "mod"), ("Z", "", "alpha"), ("X", "", "alpha"), ("C", "", "alpha"), ("V", "", "alpha"), ("B", "", "alpha"),
            ("N", "", "alpha"), ("M", "", "alpha"), (",", "<", "alpha"), (".", ">", "alpha"), ("/", "?", "alpha"), ("RSHIFT", "⇧", "mod"),
            # Thumbs (6 keys)
            ("CTRL", "⌃", "mod"), ("NUM", "Hold: L1", "layer"), ("SPACE", "␣", "space"),
            ("RET", "Hold: ⌘+⏎", "mod_tap"), ("SYM", "Hold: L2", "layer"), ("GUI", "⌘", "mod")
        ]
    },
    {
        'id': 'corne_layer_1_number',
        'title': 'Corne Choc Pro — Layer 1: NUMBER & NAVIGATION (Lower)',
        'subtitle': 'Activated by holding Left Thumb [NUM]. Alt-Gr shortcuts, Braces, Alt+Tab & Arrow keys',
        'footer': '',
        'keys': [
            # Row 0
            ("", "▽", "trans"), ("@", "⌥+Q", "special"), ("", "▽", "trans"), ("(", "Hold: € [⌥+E]", "special"), (")", "", "special"), ("⌃↑", "Hold: [ [⌥+5]", "special"),
            ("", "▽", "trans"), ("", "▽", "trans"),
            ("Y", "⌥+Y", "special"), ("", "▽", "trans"), ("", "▽", "trans"), ("", "▽", "trans"), ("P", "⌥+P", "special"), ("DEL", "⌦", "nav"),
            # Row 1
            ("", "▽", "trans"), ("", "▽", "trans"), ("ß", "⌥+S", "special"), ("{", "", "special"), ("}", "", "special"), ("", "▽", "trans"),
            ("ALT+TAB", "⌥+⇥", "nav"), ("", "▽", "trans"),
            ("LEFT", "←", "nav"), ("DOWN", "↓", "nav"), ("UP", "↑", "nav"), ("RIGHT", "→", "nav"), ("", "▽", "trans"), ("", "▽", "trans"),
            # Row 2
            ("", "▽", "trans"), ("", "▽", "trans"), ("", "▽", "trans"), ("[", "", "special"), ("]", "", "special"), ("", "▽", "trans"),
            ("", "▽", "trans"), ("", "▽", "trans"), ("", "▽", "trans"), ("", "▽", "trans"), ("", "▽", "trans"), ("", "▽", "trans"),
            # Thumbs
            ("CTRL", "", "mod"), ("", "▽ [L1]", "trans"), ("SPACE", "", "space"),
            ("ENTER", "", "nav"), ("", "▽ [L2]", "trans"), ("GUI", "⌘", "mod")
        ]
    },
    {
        'id': 'corne_layer_2_symbol',
        'title': 'Corne Choc Pro — Layer 2: SYMBOL & FUNCTION (Raise)',
        'subtitle': 'Activated by holding Right Thumb [SYM]. Top row symbols, Function keys F1–F12 & Modifiers',
        'footer': '',
        'keys': [
            # Row 0
            ("", "▽", "trans"), ("!", "", "symbol"), ("@", "", "symbol"), ("#", "", "symbol"), ("$", "", "symbol"), ("%", "", "symbol"),
            ("", "▽", "trans"), ("RCTRL", "⌃", "mod"),
            ("^", "", "symbol"), ("&", "", "symbol"), ("*", "", "symbol"), ("(", "", "symbol"), (")", "", "symbol"), ("BSPC", "⌫", "nav"),
            # Row 1
            ("F1", "", "fn"), ("F2", "", "fn"), ("F3", "", "fn"), ("F4", "", "fn"), ("F5", "", "fn"), ("F6", "", "fn"),
            ("LALT", "⌥", "mod"), ("RALT", "⌥", "mod"),
            ("-", "", "symbol"), ("=", "", "symbol"), ("", "▽", "trans"), ("", "▽", "trans"), ("\\", "", "symbol"), ("`", "", "symbol"),
            # Row 2
            ("F7", "", "fn"), ("F8", "", "fn"), ("F9", "", "fn"), ("F10", "", "fn"), ("F11", "", "fn"), ("F12", "", "fn"),
            ("_", "", "symbol"), ("+", "", "symbol"), ("", "▽", "trans"), ("", "▽", "trans"), ("|", "", "symbol"), ("~", "", "symbol"),
            # Thumbs
            ("GUI", "⌘", "mod"), ("", "▽ [L1]", "trans"), ("SPACE", "", "space"),
            ("RET", "⏎", "nav"), ("", "▽ [L2]", "trans"), ("ALT", "⌥", "mod")
        ]
    },
    {
        'id': 'corne_layer_3_extra',
        'title': 'Corne Choc Pro — Layer 3: EXTRA 1 (Numpad + Bluetooth / RGB)',
        'subtitle': 'Activated automatically by holding BOTH Thumbs [NUM + SYM]',
        'footer': '',
        'keys': [
            # Row 0
            ("", "▽", "trans"), ("", "▽", "trans"), ("", "▽", "trans"), ("", "▽", "trans"), ("", "▽", "trans"), ("", "▽", "trans"),
            ("", "▽", "trans"), ("", "▽", "trans"),
            ("", "▽", "trans"), ("7", "", "num"), ("8", "", "num"), ("9", "", "num"), ("", "▽", "trans"), ("", "▽", "trans"),
            # Row 1
            ("", "▽", "trans"), ("BT 1", "Profile 0", "bt"), ("BT 2", "Profile 1", "bt"), ("BT 3", "Profile 2", "bt"), ("BT 4", "Profile 3", "bt"), ("BT 5", "Profile 4", "bt"),
            ("", "▽", "trans"), ("", "▽", "trans"),
            ("", "▽", "trans"), ("4", "", "num"), ("5", "", "num"), ("6", "", "num"), ("0", "", "num"), ("", "▽", "trans"),
            # Row 2
            ("", "▽", "trans"), ("BT CLR", "Clear Prof", "bt"), ("RGB TOG", "Power", "rgb"), ("RGB EFF", "Effect", "rgb"), ("BOOT", "Flashing", "sys"), ("UNLOCK", "Studio", "sys"),
            ("", "▽", "trans"), ("1", "", "num"), ("2", "", "num"), ("3", "", "num"), ("", "▽", "trans"), ("", "▽", "trans"),
            # Thumbs
            ("", "▽", "trans"), ("", "▽ [Active]", "trans"), ("", "▽", "trans"),
            ("", "▽", "trans"), ("", "▽ [Active]", "trans"), ("", "▽", "trans")
        ]
    }
]

def rounded_rect(ctx, x, y, w, h, r):
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi/2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi/2)
    ctx.arc(x + r, y + h - r, r, math.pi/2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3*math.pi/2)
    ctx.close_path()

def render_single_layer(layout_data, layer, output_base, scale=64, pad_x=40, pad_y=110):
    unit = scale
    kw = 54
    base_kh = 54
    kr = 8
    
    max_x = max(k['x'] for k in layout_data) + 1.0
    max_y = max(k['y'] + k.get('h', 1.0) - 1.0 for k in layout_data) + 1.0
    
    extra_footer_h = 32 if layer.get('footer') else 0
    w = int(max_x * unit + pad_x * 2)
    h = int(max_y * unit + pad_y + 40 + extra_footer_h)
    
    for fmt in ['png', 'svg']:
        if fmt == 'png':
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        else:
            surface = cairo.SVGSurface(f"{output_base}.svg", w, h)
            
        ctx = cairo.Context(surface)
        ctx.set_source_rgb(*COLORS['bg'])
        ctx.paint()
        
        # Header banner card
        rounded_rect(ctx, 20, 16, w - 40, 72, 12)
        ctx.set_source_rgb(*COLORS['card_bg'])
        ctx.fill_preserve()
        ctx.set_source_rgb(*COLORS['key_border'])
        ctx.set_line_width(1.5)
        ctx.stroke()
        
        # Title text
        ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(24)
        ctx.set_source_rgb(*COLORS['text_main'])
        ctx.move_to(40, 48)
        ctx.show_text(layer['title'])
        
        # Subtitle text
        ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(14)
        ctx.set_source_rgb(*COLORS['text_sub'])
        ctx.move_to(40, 72)
        ctx.show_text(layer['subtitle'])
        
        # Draw keys
        for idx, (kdef, key_info) in enumerate(zip(layout_data, layer['keys'])):
            main_text, sub_text, cat = key_info
            kh = int(base_kh * kdef.get('h', 1.0))
            
            ctx.save()
            
            if 'r' in kdef:
                rot = kdef['r']
                rx = kdef['rx'] * unit + pad_x
                ry = kdef['ry'] * unit + pad_y
                ctx.translate(rx, ry)
                ctx.rotate(math.radians(rot))
                ctx.translate(-rx, -ry)
            
            kx = kdef['x'] * unit + pad_x
            ky = kdef['y'] * unit + pad_y
            
            # Key shadow
            rounded_rect(ctx, kx + 1, ky + 3, kw, kh, kr)
            ctx.set_source_rgba(0, 0, 0, 0.4)
            ctx.fill()
            
            # Key body
            rounded_rect(ctx, kx, ky, kw, kh, kr)
            
            if cat == 'trans':
                ctx.set_source_rgb(*COLORS['trans_key'])
                ctx.fill_preserve()
                ctx.set_source_rgb(*COLORS['trans_border'])
                ctx.set_line_width(1)
                ctx.stroke()
            else:
                body_col = COLORS.get(cat, COLORS['key_default'])
                border_col = COLORS.get(f"{cat}_border", COLORS['key_border'])
                ctx.set_source_rgb(*body_col)
                ctx.fill_preserve()
                ctx.set_source_rgb(*border_col)
                ctx.set_line_width(1.5)
                ctx.stroke()
                
            rounded_rect(ctx, kx + 2, ky + 2, kw - 4, kh - 4, kr - 2)
            ctx.set_source_rgba(1, 1, 1, 0.04)
            ctx.fill()
            
            # Text rendering
            if cat == 'trans':
                ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                ctx.set_font_size(10)
                ctx.set_source_rgb(*COLORS['text_trans'])
                ext = ctx.text_extents(sub_text if sub_text else "▽")
                ctx.move_to(kx + (kw - ext.width) / 2 - ext.x_bearing, ky + (kh + ext.height) / 2)
                ctx.show_text(sub_text if sub_text else "▽")
            else:
                if sub_text:
                    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                    ctx.set_font_size(12 if len(main_text) > 4 else (15 if len(main_text) <= 2 else 13))
                    ctx.set_source_rgb(*COLORS['text_main'])
                    ext = ctx.text_extents(main_text)
                    ctx.move_to(kx + (kw - ext.width) / 2 - ext.x_bearing, ky + (24 if kh <= 54 else 34))
                    ctx.show_text(main_text)
                    
                    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                    ctx.set_font_size(9 if len(sub_text) > 6 else 10)
                    ctx.set_source_rgb(*COLORS['text_sub'])
                    ext = ctx.text_extents(sub_text)
                    ctx.move_to(kx + (kw - ext.width) / 2 - ext.x_bearing, ky + (43 if kh <= 54 else 55))
                    ctx.show_text(sub_text)
                else:
                    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                    font_size = 11 if len(main_text) >= 6 else (13 if len(main_text) >= 4 else 17)
                    ctx.set_font_size(font_size)
                    ctx.set_source_rgb(*COLORS['text_main'])
                    ext = ctx.text_extents(main_text)
                    ctx.move_to(kx + (kw - ext.width) / 2 - ext.x_bearing, ky + (kh + ext.height) / 2)
                    ctx.show_text(main_text)
            
            ctx.restore()
            
        # Optional footer banner
        if layer.get('footer'):
            fy = h - 36
            rounded_rect(ctx, 20, fy, w - 40, 26, 6)
            ctx.set_source_rgb(*COLORS['card_bg'])
            ctx.fill_preserve()
            ctx.set_source_rgb(*COLORS['encoder_border'])
            ctx.set_line_width(1)
            ctx.stroke()
            
            ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(11)
            ctx.set_source_rgb(*COLORS['text_sub'])
            ext = ctx.text_extents(layer['footer'])
            ctx.move_to(32, fy + 17)
            ctx.show_text(layer['footer'])
            
        if fmt == 'png':
            surface.write_to_png(f"{output_base}.png")
        surface.finish()

def render_stacked_layers(layout_data, layers, output_base, scale=64, pad_x=40):
    unit = scale
    kw = 54
    base_kh = 54
    kr = 8
    
    layer_h = int(5.4 * unit + 100)
    max_x = max(k['x'] for k in layout_data) + 1.0
    w = int(max_x * unit + pad_x * 2)
    total_h = layer_h * len(layers) + 60
    
    for fmt in ['png', 'svg']:
        if fmt == 'png':
            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, total_h)
        else:
            surface = cairo.SVGSurface(f"{output_base}.svg", w, total_h)
            
        ctx = cairo.Context(surface)
        ctx.set_source_rgb(*COLORS['bg'])
        ctx.paint()
        
        for l_idx, layer in enumerate(layers):
            offset_y = l_idx * layer_h + 30
            
            rounded_rect(ctx, 20, offset_y, w - 40, 64, 10)
            ctx.set_source_rgb(*COLORS['card_bg'])
            ctx.fill_preserve()
            ctx.set_source_rgb(*COLORS['key_border'])
            ctx.set_line_width(1.2)
            ctx.stroke()
            
            ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
            ctx.set_font_size(20)
            ctx.set_source_rgb(*COLORS['text_main'])
            ctx.move_to(40, offset_y + 28)
            ctx.show_text(layer['title'])
            
            ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            ctx.set_font_size(12)
            ctx.set_source_rgb(*COLORS['text_sub'])
            ctx.move_to(40, offset_y + 50)
            ctx.show_text(layer['subtitle'])
            
            pad_y = offset_y + 85
            
            for idx, (kdef, key_info) in enumerate(zip(layout_data, layer['keys'])):
                main_text, sub_text, cat = key_info
                kh = int(base_kh * kdef.get('h', 1.0))
                
                ctx.save()
                
                if 'r' in kdef:
                    rot = kdef['r']
                    rx = kdef['rx'] * unit + pad_x
                    ry = kdef['ry'] * unit + pad_y
                    ctx.translate(rx, ry)
                    ctx.rotate(math.radians(rot))
                    ctx.translate(-rx, -ry)
                
                kx = kdef['x'] * unit + pad_x
                ky = kdef['y'] * unit + pad_y
                
                rounded_rect(ctx, kx + 1, ky + 3, kw, kh, kr)
                ctx.set_source_rgba(0, 0, 0, 0.4)
                ctx.fill()
                
                rounded_rect(ctx, kx, ky, kw, kh, kr)
                if cat == 'trans':
                    ctx.set_source_rgb(*COLORS['trans_key'])
                    ctx.fill_preserve()
                    ctx.set_source_rgb(*COLORS['trans_border'])
                    ctx.set_line_width(1)
                    ctx.stroke()
                else:
                    body_col = COLORS.get(cat, COLORS['key_default'])
                    border_col = COLORS.get(f"{cat}_border", COLORS['key_border'])
                    ctx.set_source_rgb(*body_col)
                    ctx.fill_preserve()
                    ctx.set_source_rgb(*border_col)
                    ctx.set_line_width(1.5)
                    ctx.stroke()
                    
                rounded_rect(ctx, kx + 2, ky + 2, kw - 4, kh - 4, kr - 2)
                ctx.set_source_rgba(1, 1, 1, 0.04)
                ctx.fill()
                
                if cat == 'trans':
                    ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                    ctx.set_font_size(10)
                    ctx.set_source_rgb(*COLORS['text_trans'])
                    ext = ctx.text_extents(sub_text if sub_text else "▽")
                    ctx.move_to(kx + (kw - ext.width) / 2 - ext.x_bearing, ky + (kh + ext.height) / 2)
                    ctx.show_text(sub_text if sub_text else "▽")
                else:
                    if sub_text:
                        ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                        ctx.set_font_size(12 if len(main_text) > 4 else (15 if len(main_text) <= 2 else 13))
                        ctx.set_source_rgb(*COLORS['text_main'])
                        ext = ctx.text_extents(main_text)
                        ctx.move_to(kx + (kw - ext.width) / 2 - ext.x_bearing, ky + (24 if kh <= 54 else 34))
                        ctx.show_text(main_text)
                        
                        ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
                        ctx.set_font_size(9 if len(sub_text) > 6 else 10)
                        ctx.set_source_rgb(*COLORS['text_sub'])
                        ext = ctx.text_extents(sub_text)
                        ctx.move_to(kx + (kw - ext.width) / 2 - ext.x_bearing, ky + (43 if kh <= 54 else 55))
                        ctx.show_text(sub_text)
                    else:
                        ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                        font_size = 11 if len(main_text) >= 6 else (13 if len(main_text) >= 4 else 17)
                        ctx.set_font_size(font_size)
                        ctx.set_source_rgb(*COLORS['text_main'])
                        ext = ctx.text_extents(main_text)
                        ctx.move_to(kx + (kw - ext.width) / 2 - ext.x_bearing, ky + (kh + ext.height) / 2)
                        ctx.show_text(main_text)
                
                ctx.restore()
                
            # Layer footer in stacked mode
            if layer.get('footer'):
                fy = offset_y + layer_h - 26
                ctx.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
                ctx.set_font_size(11)
                ctx.set_source_rgb(*COLORS['text_sub'])
                ctx.move_to(40, fy)
                ctx.show_text(layer['footer'])
                
        if fmt == 'png':
            surface.write_to_png(f"{output_base}.png")
        surface.finish()

def main():
    os.makedirs('docs/keymaps', exist_ok=True)
    
    # 1. Render Corne Choc Pro
    with open('config/corne_choc_pro.json') as f:
        corne_layout = json.load(f)['layouts']['default_layout']['layout']
        
    print("Rendering Corne Choc Pro keymaps...")
    for l in CORNE_LAYERS:
        print(f"  Rendering {l['id']}...")
        render_single_layer(corne_layout, l, f"docs/keymaps/{l['id']}")
    print("  Rendering corne_all_layers...")
    render_stacked_layers(corne_layout, CORNE_LAYERS, "docs/keymaps/corne_all_layers")
    
    print("All Corne graphics generated successfully!")

if __name__ == '__main__':
    main()
