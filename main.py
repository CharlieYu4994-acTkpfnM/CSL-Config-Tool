import tkinter, tkinter.filedialog, tkinter.messagebox
from tkinter import ttk
import json, copy

legacy_load_template = {
    "name": None,
    "type": "Legacy",
    "cape": None,
    "elytra": None,
    "skin": None,
    "checkPNG": True,
    "model": "auto"
}

default_loadlist = [{
    "name": "LittleSkin",
    "type": "CustomSkinAPI",
    "root": "https://mcskin.littleservice.cn/csl/"
    },
    {
    "name": "Mojang",
    "type": "MojangAPI"
    }]

load_template = {
    "name": None,
    "type": None,
    "root": None,
}

cfg_template = {
    "loadlist": [],
    "enableDynamicSkull": True,
    "enableTransparentSkin": True,
    "ignoreHttpsCertificate": False,
    "forceLoadAllTextures": False,
    "enableCape": True,
    "cacheExpiry": 10,
    "enableUpdateSkull": False,
    "enableLocalProfileCache": False,
    "enableCacheAutoClean": False
}

load_type = ["MojangAPI", "CustomSkinAPI", "UniSkinAPI"]


def load_cfg(path):
    with open(path, 'rb') as f:
        result = json.loads(f.read(1048576).decode())
    if type(result) == dict:
        if result.__contains__('loadlist'):
            return True, result
        else: return False, ''
    else: return False, ''

class detail_window(tkinter.Toplevel):
    cfg = {}
    def __init__(self, cfg):
        super().__init__()
        displayh = self.winfo_screenheight() // 2
        dispalyw = self.winfo_screenwidth() // 2
        self.cfg = cfg
        self.geometry(f'400x320+{dispalyw-200}+{displayh-200}')
        self.title('Detail')
        self.focus_set()
        self.grab_set()
        self.setupUI()

        if self.cfg['type'] == 'legacy':
            self.type_cbx['state'] = 'disabled'
            self.name_entry.insert('0', self.cfg['name'])
            self.root_entry.insert('0', self.cfg[''])
        else:
            self.skin_entry['state'] = 'disabled'
            self.cape_entry['state'] = 'disabled'
            self.elytra_entry['state'] = 'disabled'
            self.png_chb['state'] = 'disabled'
    
    def setupUI(self):
        topbox = ttk.Frame(self)
        ttk.Label(topbox, text='配置名称: ').grid(column=0, row=0, columnspan=1)
        self.name_entry = ttk.Entry(topbox, width=32)
        self.name_entry.grid(column=1, row=0, columnspan=4, pady=8)
        ttk.Label(topbox, text='API 链接: ').grid(column=0, row=1, columnspan=1)
        self.root_entry = ttk.Entry(topbox, width=32)
        self.root_entry.grid(column=1, row=1, columnspan=4, pady=8)
        ttk.Label(topbox, text='皮肤链接: ').grid(column=0, row=2, columnspan=1)
        self.skin_entry = ttk.Entry(topbox, width=32)
        self.skin_entry.grid(column=1, row=2, columnspan=4, pady=8)
        ttk.Label(topbox, text='披风链接: ').grid(column=0, row=3, columnspan=1)
        self.cape_entry = ttk.Entry(topbox, width=32)
        self.cape_entry.grid(column=1, row=3, columnspan=4, pady=8)
        ttk.Label(topbox, text='鞘翅链接: ').grid(column=0, row=4, columnspan=1)
        self.elytra_entry = ttk.Entry(topbox, width=32)
        self.elytra_entry.grid(column=1, row=4, columnspan=4, pady=8)
        ttk.Label(topbox, text='加载类型: ').grid(column=0, row=5, columnspan=1)
        self.type_cbx = ttk.Combobox(topbox, width=16)
        self.type_cbx.grid(column=1, row=5, columnspan=3, pady=8)
        self.png_chb = tkinter.Checkbutton(topbox, text='png 检查')
        self.png_chb.grid(column=4, row=5, columnspan=1, pady=8)
        topbox.grid(column=0, row=0, pady=4, padx=15)

        buttombox = ttk.Frame(self)
        ttk.Button(buttombox, text='确定', width=18).grid(column=0, row=0, padx=8)
        ttk.Button(buttombox, text='取消', width=18).grid(column=1, row=0, padx=8)
        buttombox.grid(column=0, row=1, pady=4, padx=10)



class main(tkinter.Tk):
    loadlist = []
    cfg = {}

    def __init__(self):
        super().__init__()
        displayh = self.winfo_screenheight() // 2
        dispalyw = self.winfo_screenwidth() // 2
        self.geometry(f'312x350+{dispalyw-156}+{displayh-200}')
        self.title('CSL Config')
        self.protocol('WM_DELETE_WINDOW', lambda: self.close())
        self.resizable(0, 0)
        self.setupUI()
        self.bind('<Control-N>', lambda event: self.gen_new())
        self.bind('<Control-O>', lambda event: self.load_cfg())
        self.bind('<Control-S>', lambda event: self.save())
        self.cfg_lsb.bind('<Double-Button-1>', lambda event: self.detail())

    def setupUI(self):
        menu_bar = tkinter.Menu(self)

        file_menu = tkinter.Menu(menu_bar, tearoff=False)
        file_menu.add_command(label='新建', command=self.gen_new, accelerator='Ctrl+N')
        file_menu.add_command(label='打开', command=self.load_cfg, accelerator='Ctrl+O')
        file_menu.add_command(label='保存', command=self.save, accelerator='Ctrl+S')
        menu_bar.add_cascade(label='文件', menu=file_menu)

        help_menu = tkinter.Menu(menu_bar, tearoff=False)
        help_menu.add_command(label='关于')
        help_menu.add_command(label='帮助')
        menu_bar.add_cascade(label='帮助', menu=help_menu)

        self.config(menu=menu_bar)

        topbox = ttk.Frame(self)
        cfg_lsb_sb = ttk.Scrollbar(topbox)
        self.cfg_lsb = tkinter.Listbox(topbox, width=32, height=14, yscrollcommand=cfg_lsb_sb.set)
        self.cfg_lsb.grid(column=0, row=0)
        cfg_lsb_sb.config(command=self.cfg_lsb.yview)
        cfg_lsb_sb.grid(column=1, row=0, sticky='ns')
        topbox.grid(column=0, row=0)

        buttombox = ttk.Frame(self)
        ttk.Button(buttombox, width=8, text='上移', command=
                   lambda: self.move(is_up=True)).grid(column=0, row=0, padx=4)
        ttk.Button(buttombox, width=8, text='删除', command=
                   lambda: self.delete()).grid(column=1, row=0, padx=4)
        ttk.Button(buttombox, width=8, text='下移', command=
                   lambda: self.move(is_up=False)).grid(column=2, row=0, padx=4)
        buttombox.grid(column=0, row=1, pady=9)

    def create_newcfg(self):
        self.cfg = cfg_template.copy()
        self.cfg['loadlist'] = copy.deepcopy(default_loadlist)
    
    def load_cfg(self):
        path = tkinter.filedialog.askopenfilename(initialfile='CustomSkinLoader'
                    ,filetypes=[('JSON File', '*.json')], initialdir='./')
        if not path: return
        status, cfg_t = load_cfg(path)
        if not status: tkinter.messagebox.showerror('Error', '配置文件无效'); return
        self.cfg = copy.deepcopy(cfg_t)
        self.flush_list()

    def flush_list(self):
        self.loadlist = self.cfg['loadlist']
        self.cfg_lsb.delete('0', 'end')
        for stuff in self.loadlist:
            self.cfg_lsb.insert('end', stuff['name'])

    def lsb_swap(self, pos0, pos1):
        tmp0 = self.cfg_lsb.get(pos0)
        tmp1 = self.cfg_lsb.get(pos1)
        self.cfg_lsb.delete(pos0)
        self.cfg_lsb.insert(pos0, tmp1)
        self.cfg_lsb.delete(pos1)
        self.cfg_lsb.insert(pos1, tmp0)
        self.cfg_lsb.activate(pos1)
    
    def move(self, is_up=True):
        index0 = self.cfg_lsb.index('active')
        index1 = index0 - 1 if is_up else index0 + 1
        if index1 < 0 or index1 == self.cfg_lsb.size(): return
        self.lsb_swap(index0, index1)
        self.loadlist[index0], self.loadlist[index1] =\
            self.loadlist[index1], self.loadlist[index0]

    def save(self):
        path = tkinter.filedialog.asksaveasfilename(initialfile='CustomSkinLoader'
                    ,filetypes=[('JSON File', '*.json')], initialdir='./')
        if not path: return
        json.dump(self.cfg, open(path, "w"))
    
    def detail(self):
        cfg = self.loadlist[self.cfg_lsb.index('active')]
        window = detail_window(cfg)

    def delete(self):
        self.cfg_lsb.delete('active')

    def gen_new(self):
        self.create_newcfg()
        self.flush_list()

    def close(self):
        self.destroy()
        pass


if __name__ == "__main__":
    app = detail_window({'type': 'legcacy'})
    app.mainloop()
