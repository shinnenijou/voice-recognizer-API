import ttkbootstrap as ttk

from res.scripts.config import CONST

def set_style():
    ttk.Style().configure('TLabelframe.Label', font=CONST.GLOBAL_FONT)
    ttk.Style().configure('TButton', font=CONST.GLOBAL_FONT)
    ttk.Style().configure('TEntry', font=CONST.GLOBAL_FONT)
    ttk.Style().configure('TLabel', font=CONST.GLOBAL_FONT)
    ttk.Style().configure('TRadiobutton', font=CONST.GLOBAL_FONT)

