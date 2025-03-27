import tkinter as tk
from tkinter import messagebox, Menu
from tkinter import ttk
import os

# --- הגדרת פלטת צבעים וגופנים ---
BG_MAIN      = "#f9f9f9"         # רקע חלון ראשי – בהיר
FRAME_BG     = "#ffffff"         # רקע מסגרות – לבן
BANNER_BG    = "#2196F3"         # רקע Banner – כחול
BANNER_FG    = "#ffffff"         # טקסט Banner – לבן
NOTE_FONT    = ("Segoe UI", 10, "bold", "underline")
LABEL_FONT   = ("Segoe UI", 10)
BUTTON_FONT  = ("Segoe UI", 10)
TITLE_FONT   = ("Segoe UI", 16, "bold")
SUBTITLE_FONT= ("Segoe UI", 12, "bold")

# --------------------------------------------------
# הסתרת חלון ה-DOS (Console) במערכות Windows
if os.name == "nt":
    import ctypes
    whnd = ctypes.windll.kernel32.GetConsoleWindow()
    if whnd != 0:
        ctypes.windll.user32.ShowWindow(whnd, 0)
        ctypes.windll.kernel32.FreeConsole()

# --------------------------------------------------
# ניצור מופע Tk אחד בלבד – לכל הקוד
root = tk.Tk()
root.title("מחשבון פוזיציות")
root.geometry("600x850")
root.minsize(600, 850)
root.resizable(True, True)
root.configure(bg=BG_MAIN)

# --------------------------------------------------
# הגדרות נגישות מתקדמות – הדגשת שדות בפוקוס (קו כחול)
root.option_add('*Entry.focusHighlightColor', 'blue')
root.option_add('*Entry.focusHighlightThickness', 2)
# ברירת מחדל ליישור לימין עבור תוויות
root.option_add('*Label.anchor', 'e')
root.option_add('*Label.justify', 'right')
root.option_add('*Button.anchor', 'center')

# --------------------------------------------------
def validate_positive(value, field_name):
    if value <= 0:
        raise ValueError(f"{field_name} חייב להיות מספר חיובי וגדול מ-0.")

class CreateToolTip(object):
    def __init__(self, widget, text='מידע'):
        self.waittime = 500
        self.wraplength = 200
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()
    def leave(self, event=None):
        self.unschedule()
        self.hidetip()
    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)
    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
    def showtip(self, event=None):
        x = self.widget.winfo_pointerx() + 10
        y = self.widget.winfo_pointery() + 10
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         wraplength=self.wraplength, font=("Segoe UI", 9))
        label.pack(ipadx=1)
    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="הזן ערך...", color='grey', *args, **kwargs):
        kwargs.setdefault('justify', 'right')
        super().__init__(master, *args, **kwargs)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg'] if 'fg' in kwargs else 'black'
        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)
        self.put_placeholder()

    def put_placeholder(self):
        if not self.get():
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete(0, 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

def get_float(entry, field_name, default=None):
    value = entry.get().strip().replace(',', '.')
    if value == entry.placeholder or value == "":
        if default is not None:
            return default
        else:
            raise ValueError(f"יש למלא את '{field_name}'")
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"'{field_name}' חייב להיות מספר תקין.")

def get_int(entry, field_name, default=None):
    value = entry.get().strip().replace(',', '.')
    if value == entry.placeholder or value == "":
        if default is not None:
            return default
        else:
            raise ValueError(f"יש למלא את '{field_name}'")
    try:
        val = float(value)
        if not val.is_integer():
            raise ValueError(f"'{field_name}' חייב להיות מספר שלם")
        return int(val)
    except ValueError:
        raise ValueError(f"'{field_name}' חייב להיות מספר תקין ושלם.")

def custom_warning(message):
    warn_win = tk.Toplevel(root)
    warn_win.title("אזהרה")
    warn_win.configure(bg="#ffecec")
    warn_win.update_idletasks()
    width = warn_win.winfo_reqwidth()
    height = warn_win.winfo_reqheight()
    screen_width = warn_win.winfo_screenwidth()
    screen_height = warn_win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    warn_win.geometry(f"+{x}+{y}")
    lbl_title = tk.Label(
        warn_win, text="אזהרה", fg="red",
        font=("Segoe UI", 12, "bold", "underline"), bg="#ffecec",
        justify="right", anchor="e"
    )
    lbl_title.pack(padx=20, pady=5)
    lbl_msg = tk.Label(
        warn_win, text=message, bg="#ffecec",
        font=("Segoe UI", 10), justify="right", anchor="e"
    )
    lbl_msg.pack(padx=20, pady=5)
    btn_ok = tk.Button(warn_win, text="אישור", command=warn_win.destroy, font=BUTTON_FONT)
    btn_ok.pack(pady=10)
    warn_win.grab_set()
    warn_win.focus_force()
    warn_win.wait_window()

def calculate_profit():
    errors = []
    try:
        entry_price = get_float(profit_entry_price_entry, "שווי המטבע הנוכחי ($)")
        validate_positive(entry_price, "שווי המטבע")
    except ValueError as e:
        errors.append(str(e))
    try:
        investment = get_float(profit_investment_entry, "סכום השקעה ($)")
        validate_positive(investment, "סכום השקעה")
    except ValueError as e:
        errors.append(str(e))
    try:
        target_price = get_float(profit_target_price_entry, "ערך יעד ($)")
        validate_positive(target_price, "ערך יעד")
    except ValueError as e:
        errors.append(str(e))
    try:
        leverage = get_int(profit_leverage_entry, "מינוף", default=1)
        validate_positive(leverage, "מינוף")
    except ValueError as e:
        errors.append(str(e))
    try:
        fee_percentage = get_float(profit_fee_entry, "עמלות (%)", default=0.12)
        if fee_percentage < 0:
            raise ValueError("עמלות חייבות להיות חיוביות או 0.")
    except ValueError as e:
        errors.append(str(e))
        
    if errors:
        messagebox.showerror("קלט לא תקין", "\n".join(errors))
        return

    position_type = profit_position_var.get()
    quantity = (investment * leverage) / entry_price

    if position_type == "long":
        profit = (target_price - entry_price) * quantity
    else:  # short
        profit = (entry_price - target_price) * quantity

    fee = (investment * leverage) * (fee_percentage / 100)
    net_profit = profit - fee
    profit_percentage = (net_profit / (investment * leverage)) * 100

    if net_profit >= 0:
        profit_result_label.config(text=f"רווח: ${net_profit:.6f}", fg="green")
    else:
        profit_result_label.config(text=f"הפסד: ${net_profit:.6f}", fg="red")

    profit_detail_label.config(
        text=(
            f"כמות מטבעות: {quantity:.6f}\n"
            f"אחוז רווח: {profit_percentage:.6f}%\n"
            f"עמלות: ${fee:.6f}"
        )
    )

def calculate_strategy():
    """
    חישוב יעדים ואסטרטגיה לפי Take Profit by ROI.
    כאן, מחיר היעד לכל יעד מחושב על בסיס:
      PNL_target = investment * (ROI_target/100)
      Quantity = (investment * leverage)/ entry_price
    עבור פוזיציית Long: target = entry_price + (PNL_target/Quantity)
    ועבור Short: target = entry_price - (PNL_target/Quantity)
    """
    errors = []
    try:
        entry_price = get_float(strategy_entry_price_entry, "מחיר כניסה למטבע ($)")
        validate_positive(entry_price, "מחיר כניסה")
    except ValueError as e:
        errors.append(str(e))
    try:
        available_capital = get_float(strategy_available_capital_entry, "כסף זמין למסחר ($)")
        validate_positive(available_capital, "כסף זמין למסחר")
    except ValueError as e:
        errors.append(str(e))
    try:
        investment = get_float(strategy_investment_entry, "סכום השקעה ($)")
        validate_positive(investment, "סכום השקעה")
    except ValueError as e:
        errors.append(str(e))
    try:
        leverage = get_int(strategy_leverage_entry, "מינוף", default=1)
        validate_positive(leverage, "מינוף")
    except ValueError as e:
        errors.append(str(e))
    try:
        fee_percentage = get_float(strategy_fee_entry, "עמלות (%)", default=0.12)
        if fee_percentage < 0:
            raise ValueError("עמלות חייבות להיות חיוביות או 0.")
    except ValueError as e:
        errors.append(str(e))
        
    if errors:
        messagebox.showerror("קלט לא תקין", "\n".join(errors))
        return

    position_type = strategy_position_var.get()
    max_investment = available_capital * 0.75
    if investment > max_investment:
        custom_warning(
            f"סכום ההשקעה גדול מ-75% מהכסף הזמין.\n"
            f"נשתמש בערך {max_investment:.6f} במקום {investment:.6f}."
        )
        investment = max_investment

    quantity = (investment * leverage) / entry_price

    # הגדרת יעדי ROI רצויים (באחוזים)
    roi_target1 = 12.5
    roi_target2 = 25.0
    roi_target3 = 42.5

    # חישוב הרווח הרצוי (PNL) לכל יעד, על בסיס הסכום שהבורסה מחשיבה כמרג'ין (investment)
    pnl_target1 = investment * (roi_target1 / 100)
    pnl_target2 = investment * (roi_target2 / 100)
    pnl_target3 = investment * (roi_target3 / 100)

    if position_type == "long":
        stop_loss = entry_price * (1 - 0.15)
        target1 = entry_price + (pnl_target1 / quantity)
        target2 = entry_price + (pnl_target2 / quantity)
        target3 = entry_price + (pnl_target3 / quantity)
    else:
        stop_loss = entry_price * (1 + 0.15)
        target1 = entry_price - (pnl_target1 / quantity)
        target2 = entry_price - (pnl_target2 / quantity)
        target3 = entry_price - (pnl_target3 / quantity)

    # המשך חישוב הרווחים והעמלות כפי שהיה:
    fraction1 = 0.25
    fraction2 = 0.25
    fraction3 = 0.50

    if position_type == "long":
        partial_profit1 = fraction1 * (target1 - entry_price) * quantity
        partial_profit2 = fraction2 * (target2 - entry_price) * quantity
        partial_profit3 = fraction3 * (target3 - entry_price) * quantity
    else:
        partial_profit1 = fraction1 * (entry_price - target1) * quantity
        partial_profit2 = fraction2 * (entry_price - target2) * quantity
        partial_profit3 = fraction3 * (entry_price - target3) * quantity

    total_profit = partial_profit1 + partial_profit2 + partial_profit3

    fee_total = (investment * leverage) * (fee_percentage / 100)
    fee1 = fee_total * fraction1
    fee2 = fee_total * fraction2
    fee3 = fee_total * fraction3

    roi_net_target1 = ((partial_profit1 - fee1) / (investment * leverage * fraction1)) * 100
    roi_net_target2 = ((partial_profit2 - fee2) / (investment * leverage * fraction2)) * 100
    roi_net_target3 = ((partial_profit3 - fee3) / (investment * leverage * fraction3)) * 100

    net_profit = total_profit - fee_total

    line1 = (
        f"כמות מטבעות: {quantity:.6f}\n"
        f"סכום השקעה בשימוש: ${investment:.6f} ({(investment/available_capital)*100:.6f}% מהכסף הזמין)\n"
        f"סטופ לוס: ${stop_loss:.6f} - 15% הפסד מקסימום\n"
    )
    line2 = (
        f"לסגור 25% מהעסקה - (ROI נטו: {roi_target1:.6f}%)- יעד 1 \n"
        f"  מחיר יעד: ${target1:.6f}\n"
        f"  כמות מטבעות לסגירה: {quantity * fraction1:.6f}\n"
        f"  רווח בפועל (לפני עמלות): ${partial_profit1:.6f}\n"
    )
    line3 = (
        f"לסגור 25% מהעסקה - (ROI נטו: {roi_target2:.6f}%)- יעד 2 \n"
        f"  מחיר יעד: ${target2:.6f}\n"
        f"  כמות מטבעות לסגירה: {quantity * fraction2:.6f}\n"
        f"  רווח בפועל (לפני עמלות): ${partial_profit2:.6f}\n"
    )
    line4 = (
        f"לסגור 50% מהעסקה - (ROI נטו: {roi_target3:.6f}%)- יעד 3 \n"
        f"  מחיר יעד: ${target3:.6f}\n"
        f"  כמות מטבעות לסגירה: {quantity * fraction3:.6f}\n"
        f"  רווח בפועל (לפני עמלות): ${partial_profit3:.6f}\n"
    )
    line5 = (
        f"סה\"כ רווח צפוי (לפני עמלות): ${total_profit:.6f}\n"
        f"עלות עמלות לפתיחה וסגירה: ${fee_total:.6f}\n"
        f"סה\"כ רווח נטו (לאחר עמלות): ${net_profit:.6f}"
    )

    result_text = "\n".join([line1, line2, line3, line4, line5])
    
    strategy_note_label.config(
        text="לאחר השגת יעד 1, עדכן את הסטופ לוס לנקודת הכניסה (סיכון אפס).",
        fg="red", font=NOTE_FONT
    )
    
    strategy_result_label.config(
        text=result_text,
        wraplength=0,
        justify="center",
        anchor="center"
    )

def reset_fields(frame):
    for child in frame.winfo_children():
        if isinstance(child, tk.Entry):
            child.delete(0, tk.END)
            if hasattr(child, 'put_placeholder'):
                child.put_placeholder()
    if frame == strategy_inputs_frame:
        strategy_note_label.config(text="", fg="red", font=("Segoe UI", 10))

def create_context_menu(widget):
    menu = Menu(root, tearoff=0)
    menu.add_command(label="גזור", command=lambda: cut_text(widget))
    menu.add_command(label="העתק", command=lambda: copy_text(widget))
    menu.add_command(label="הדבק", command=lambda: paste_text(widget))
    return menu

def show_context_menu(event, widget):
    menu = create_context_menu(widget)
    menu.post(event.x_root, event.y_root)

def cut_text(widget):
    try:
        root.clipboard_clear()
        root.clipboard_append(widget.selection_get())
        widget.delete(0, tk.SEL_FIRST, tk.SEL_LAST)
    except tk.TclError:
        pass

def copy_text(widget):
    try:
        root.clipboard_clear()
        root.clipboard_append(widget.selection_get())
    except tk.TclError:
        pass

def paste_text(widget):
    try:
        widget.insert(tk.INSERT, root.clipboard_get())
    except tk.TclError:
        pass

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky="nsew")

# ---------- טאב רווח/הפסד ----------
profit_tab = ttk.Frame(notebook)
notebook.add(profit_tab, text="חישוב רווח/הפסד")

banner_profit = tk.Label(profit_tab, text="מחשבון רווח/הפסד", 
                         font=TITLE_FONT, bg=BANNER_BG, fg=BANNER_FG,
                         padx=10, pady=10, anchor="center", justify="center")
banner_profit.pack(fill="x")

profit_main = tk.Frame(profit_tab, bg=FRAME_BG)
profit_main.pack(expand=True, fill="both", padx=20, pady=20)

tk.Label(
    profit_main,
    text="הזן את הנתונים לחישוב רווח/הפסד",
    font=SUBTITLE_FONT,
    bg=FRAME_BG, justify="center", anchor="center"
).grid(row=0, column=0, columnspan=2, pady=10)

profit_position_var = tk.StringVar(value="long")
position_frame_profit = tk.Frame(profit_main, bg=FRAME_BG)
position_frame_profit.grid(row=1, column=0, columnspan=2, pady=5)
tk.Label(position_frame_profit, text="סוג פוזיציה:", bg=FRAME_BG).grid(row=0, column=0, padx=5)
tk.Radiobutton(position_frame_profit, text="Long", variable=profit_position_var, value="long", bg=FRAME_BG)\
    .grid(row=0, column=1, padx=5)
tk.Radiobutton(position_frame_profit, text="Short", variable=profit_position_var, value="short", bg=FRAME_BG)\
    .grid(row=0, column=2, padx=5)

profit_inputs_frame = tk.Frame(profit_main, bg=FRAME_BG)
profit_inputs_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")
for i in range(2):
    profit_inputs_frame.grid_columnconfigure(i, weight=1)

def add_profit_field(frame, label_text, tooltip_text, placeholder_text, row):
    tk.Label(frame, text=label_text, bg=FRAME_BG)\
        .grid(row=row, column=0, sticky="ew", padx=5, pady=2)
    entry = PlaceholderEntry(frame, placeholder=placeholder_text)
    entry.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
    entry.bind("<Button-3>", lambda e, w=entry: show_context_menu(e, w))
    CreateToolTip(entry, tooltip_text)
    return entry

profit_entry_price_entry = add_profit_field(profit_inputs_frame, "שווי המטבע הנוכחי ($):", 
                                            "הזן את מחיר המטבע הנוכחי", "למשל: 50000", 0)
profit_investment_entry = add_profit_field(profit_inputs_frame, "סכום השקעה ($):", 
                                           "הזן את סכום ההשקעה שלך", "למשל: 1000", 1)
profit_target_price_entry = add_profit_field(profit_inputs_frame, "ערך יעד ($):", 
                                             "הזן את מחיר היעד לסגירת העסקה", "למשל: 55000", 2)
profit_leverage_entry = add_profit_field(profit_inputs_frame, "מינוף (מספר שלם, ברירת מחדל: 1):", 
                                         "הזן את המינוף (מספר שלם בלבד)", "למשל: 1", 3)
profit_fee_entry = add_profit_field(profit_inputs_frame, "עמלות (%) (ברירת מחדל: 0.12 אחוז):", 
                                    "הזן את אחוז העמלות", "למשל: 0", 4)

profit_button_frame = tk.Frame(profit_main, bg=FRAME_BG)
profit_button_frame.grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(profit_button_frame, text="חשב רווח/הפסד", command=calculate_profit, font=BUTTON_FONT)\
    .grid(row=0, column=0, padx=10)
tk.Button(profit_button_frame, text="אפס שדות", command=lambda: reset_fields(profit_inputs_frame), font=BUTTON_FONT)\
    .grid(row=0, column=1, padx=10)

profit_result_label = tk.Label(profit_main, text="", font=("Segoe UI", 12, "bold"),
                               bg=FRAME_BG, justify="center", anchor="center")
profit_result_label.grid(row=4, column=0, columnspan=2, pady=5)

profit_detail_label = tk.Label(profit_main, text="", fg="black",
                               bg=FRAME_BG, justify="center", anchor="center")
profit_detail_label.grid(row=5, column=0, columnspan=2, pady=5)

profit_main.bind("<Return>", lambda event: calculate_profit())
profit_main.bind("<Control-r>", lambda event: reset_fields(profit_inputs_frame))

# ---------- טאב אסטרטגיה ויעדים ----------
strategy_tab = ttk.Frame(notebook)
notebook.add(strategy_tab, text="יעדים ואסטרטגיה")

banner_strategy = tk.Label(strategy_tab, text="מחשבון יעדים ואסטרטגיה", 
                           font=TITLE_FONT, bg=BANNER_BG, fg=BANNER_FG,
                           padx=10, pady=10, anchor="center", justify="center")
banner_strategy.pack(fill="x")

strategy_main = tk.Frame(strategy_tab, bg=FRAME_BG)
strategy_main.pack(expand=True, fill="both", padx=20, pady=20)

tk.Label(
    strategy_main,
    text="הזן את הנתונים לחישוב יעדים ואסטרטגיה",
    font=SUBTITLE_FONT,
    bg=FRAME_BG, justify="center", anchor="center"
).grid(row=0, column=0, columnspan=2, pady=10)

strategy_position_var = tk.StringVar(value="long")
position_frame_strategy = tk.Frame(strategy_main, bg=FRAME_BG)
position_frame_strategy.grid(row=1, column=0, columnspan=2, pady=5)
tk.Label(position_frame_strategy, text="סוג פוזיציה:", bg=FRAME_BG)\
    .grid(row=0, column=0, padx=5)
tk.Radiobutton(position_frame_strategy, text="Long", variable=strategy_position_var, 
               value="long", bg=FRAME_BG)\
    .grid(row=0, column=1, padx=5)
tk.Radiobutton(position_frame_strategy, text="Short", variable=strategy_position_var, 
               value="short", bg=FRAME_BG)\
    .grid(row=0, column=2, padx=5)

strategy_inputs_frame = tk.Frame(strategy_main, bg=FRAME_BG)
strategy_inputs_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")
for i in range(2):
    strategy_inputs_frame.grid_columnconfigure(i, weight=1)

def add_strategy_field(frame, label_text, tooltip_text, placeholder_text, row):
    tk.Label(frame, text=label_text, bg=FRAME_BG)\
        .grid(row=row, column=0, sticky="ew", padx=5, pady=2)
    entry = PlaceholderEntry(frame, placeholder=placeholder_text)
    entry.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
    entry.bind("<Button-3>", lambda e, w=entry: show_context_menu(e, w))
    CreateToolTip(entry, tooltip_text)
    return entry

strategy_entry_price_entry = add_strategy_field(strategy_inputs_frame, "מחיר כניסה למטבע ($):", 
                                                "הזן את מחיר הכניסה לעסקה", "למשל: 3000", 0)
strategy_available_capital_entry = add_strategy_field(strategy_inputs_frame, "כסף זמין למסחר ($):", 
                                                      "הזן את הסכום הכולל שברשותך למסחר", "למשל: 5000", 1)
strategy_investment_entry = add_strategy_field(strategy_inputs_frame, "סכום השקעה ($):", 
                                               "הזן את סכום ההשקעה (לא יעלה על 75% מהכסף הזמין)", "למשל: 1000", 2)
strategy_leverage_entry = add_strategy_field(strategy_inputs_frame, "מינוף (מספר שלם, ברירת מחדל: 1):", 
                                             "הזן את המינוף (חובה מספר שלם)", "למשל: 1", 3)
strategy_fee_entry = add_strategy_field(strategy_inputs_frame, "עמלות (%) (ברירת מחדל: 0.12 אחוז):", 
                                        "הזן את אחוז העמלות", "למשל: 0.12", 4)

strategy_button_frame = tk.Frame(strategy_main, bg=FRAME_BG)
strategy_button_frame.grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(strategy_button_frame, text="חשב יעדים ואסטרטגיה", command=calculate_strategy, font=BUTTON_FONT)\
    .grid(row=0, column=0, padx=10)
tk.Button(strategy_button_frame, text="אפס שדות", command=lambda: reset_fields(strategy_inputs_frame), font=BUTTON_FONT)\
    .grid(row=0, column=1, padx=10)

strategy_result_label = tk.Label(strategy_main, text="", fg="blue",
                                 font=("Segoe UI", 10, "bold"), bg=FRAME_BG,
                                 justify="center", anchor="center", wraplength=550)
strategy_result_label.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

strategy_note_label = tk.Label(strategy_main, text="", bg=FRAME_BG,
                               justify="center", anchor="center")
strategy_note_label.grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

strategy_main.bind("<Return>", lambda event: calculate_strategy())
strategy_main.bind("<Control-r>", lambda event: reset_fields(strategy_inputs_frame))

# ---------- טאב "אודות" ----------
about_tab = ttk.Frame(notebook)
notebook.add(about_tab, text="אודות")

about_frame = tk.Frame(about_tab, bg="#f1f1f1")
about_frame.pack(expand=True, fill="both", padx=20, pady=20)

title_label = tk.Label(about_frame, 
    text="מחשבון פוזיציות", 
    font=("Segoe UI", 18, "bold", "underline"), 
    bg="#f1f1f1", fg="#333333",
    anchor="center", justify="center")
title_label.pack(pady=(10, 20))

desc_title = tk.Label(about_frame, 
    text="תיאור האפליקציה", 
    font=("Segoe UI", 14, "bold", "underline"), 
    bg="#f1f1f1", fg="#555555", 
    anchor="center", justify="center")
desc_title.pack(pady=(0, 5))

desc_text = (
    "מחשבון פוזיציות הוא כלי מקצועי לניהול עסקאות קריפטו, "
    "המיועד לסוחרים המעוניינים לקבל חישוב מדויק של רווחים והפסדים, "
    "לנהל יעדים ואסטרטגיה בצורה מסודרת, ולבצע ניתוחים מתקדמים. "
    "האפליקציה מציגה תוצאות ברורות ומספקת ממשק נגיש, אינטואיטיבי ומעוצב בהתאם לעקרונות עיצוב מודרני."
)
desc_label = tk.Label(about_frame, 
    text=desc_text, 
    font=("Segoe UI", 11), 
    bg="#f1f1f1", fg="#444444",
    wraplength=550, anchor="center", justify="center")
desc_label.pack(pady=(0, 20))

features_title = tk.Label(about_frame, 
    text="תכונות עיקריות", 
    font=("Segoe UI", 14, "bold", "underline"), 
    bg="#f1f1f1", fg="#555555", 
    anchor="center", justify="center")
features_title.pack(pady=(0, 5))

features_text = (
    "• חישוב רווח/הפסד מדויק\n"
    "• ניהול יעדים ואסטרטגיה עם חלוקה מדורגת\n"
    "• בדיקות קלט מתקדמות למניעת שגיאות\n"
    "• ממשק משתמש מודרני, נגיש ורספונסיבי\n"
    "• חלונות התראה מותאמים להמחשת נקודות קריטיות"
)
features_label = tk.Label(about_frame, 
    text=features_text, 
    font=("Segoe UI", 11), 
    bg="#f1f1f1", fg="#444444",
    anchor="center", justify="center")
features_label.pack(pady=(0, 20))

vision_title = tk.Label(about_frame, 
    text="חזון וקרדיטים", 
    font=("Segoe UI", 14, "bold", "underline"), 
    bg="#f1f1f1", fg="#555555", 
    anchor="center", justify="center")
vision_title.pack(pady=(0, 5))

vision_text = (
    "האפליקציה נועדה לשפר את ניהול העסקאות והערכת הסיכונים במסחר קריפטו, ולספק כלים מתקדמים לקבלת החלטות מושכלות.\n\n"
    "קרדיטים:\n"
    "תודה ענקית לצוות הפיתוח ולכל מי שתרם להצלחת הפרויקט. קרדיט ענק לשיתוף הפעולה, היצירתיות והמאמץ המשותף."
)
vision_label = tk.Label(about_frame, 
    text=vision_text, 
    font=("Segoe UI", 11), 
    bg="#f1f1f1", fg="#444444",
    wraplength=550, anchor="center", justify="center")
vision_label.pack(pady=(0, 10))

root.mainloop()
