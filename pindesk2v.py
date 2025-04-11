import tkinter as tk
from tkinter import filedialog, colorchooser, simpledialog, messagebox
import json

class DesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zaawansowany Program do Projektowania Budynków")
        self.create_menu()
        self.create_canvas()
        self.create_tools()
        self.current_color = 'black'
        self.current_layer = 'Layer 1'
        self.layers = {'Layer 1': []}
        self.line_width = 2
        self.scale_factor = 1.0

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Nowy", command=self.new_project)
        file_menu.add_command(label="Otwórz", command=self.open_project)
        file_menu.add_command(label="Zapisz", command=self.save_project)
        file_menu.add_command(label="Zapisz jako PNG", command=self.save_as_png)
        file_menu.add_separator()
        file_menu.add_command(label="Wyjście", command=self.root.quit)
        menu_bar.add_cascade(label="Plik", menu=file_menu)
        self.root.config(menu=menu_bar)

    def create_canvas(self):
        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.grid(row=0, column=1, sticky="nsew")

        self.canvas = tk.Canvas(self.canvas_frame, bg="white", width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset_coords)

        self.scroll_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.pack(side="bottom", fill="x")
        self.scroll_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side="right", fill="y")

        self.canvas.configure(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        self.draw_grid()

    def draw_grid(self):
        for i in range(0, 800, 20):
            self.canvas.create_line([(i, 0), (i, 600)], tag='grid_line', fill='gray')
        for i in range(0, 600, 20):
            self.canvas.create_line([(0, i), (800, i)], tag='grid_line', fill='gray')

    def create_tools(self):
        tool_frame = tk.Frame(self.root, bd=2, relief="ridge")
        tool_frame.grid(row=0, column=0, sticky="ns")

        self.scale_label = tk.Label(tool_frame, text="Skala: 1:100")
        self.scale_label.pack(pady=5)

        self.draw_line_btn = tk.Button(tool_frame, text="Rysuj Linię", command=self.select_line_tool)
        self.draw_line_btn.pack(pady=5)

        self.draw_rect_btn = tk.Button(tool_frame, text="Rysuj Prostokąt", command=self.select_rect_tool)
        self.draw_rect_btn.pack(pady=5)

        self.draw_circle_btn = tk.Button(tool_frame, text="Rysuj Okrąg", command=self.select_circle_tool)
        self.draw_circle_btn.pack(pady=5)

        self.draw_polygon_btn = tk.Button(tool_frame, text="Rysuj Wielokąt", command=self.select_polygon_tool)
        self.draw_polygon_btn.pack(pady=5)

        self.text_btn = tk.Button(tool_frame, text="Dodaj Tekst", command=self.add_text)
        self.text_btn.pack(pady=5)

        self.color_btn = tk.Button(tool_frame, text="Wybierz Kolor", command=self.choose_color)
        self.color_btn.pack(pady=5)

        self.line_width_btn = tk.Button(tool_frame, text="Grubość Linii", command=self.choose_line_width)
        self.line_width_btn.pack(pady=5)

        self.layer_btn = tk.Button(tool_frame, text="Zarządzaj Warstwami", command=self.manage_layers)
        self.layer_btn.pack(pady=5)

        self.scale_btn = tk.Button(tool_frame, text="Skalowanie", command=self.set_scale)
        self.scale_btn.pack(pady=5)

        self.rotate_btn = tk.Button(tool_frame, text="Obracanie", command=self.rotate_element)
        self.rotate_btn.pack(pady=5)

        self.selected_tool = None

    def select_line_tool(self):
        self.selected_tool = "line"

    def select_rect_tool(self):
        self.selected_tool = "rect"

    def select_circle_tool(self):
        self.selected_tool = "circle"

    def select_polygon_tool(self):
        self.selected_tool = "polygon"
        self.polygon_coords = []

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Wybierz Kolor")[1]
        if color_code:
            self.current_color = color_code

    def choose_line_width(self):
        width = simpledialog.askinteger("Grubość Linii", "Podaj grubość linii (1-10):", minvalue=1, maxvalue=10)
        if width:
            self.line_width = width

    def set_scale(self):
        scale = simpledialog.askfloat("Skalowanie", "Podaj skalę (np. 1.5 dla 150%):", minvalue=0.1)
        if scale:
            self.scale_factor = scale
            self.canvas.scale("all", 0, 0, scale, scale)

    def rotate_element(self):
        angle = simpledialog.askfloat("Obracanie", "Podaj kąt w stopniach:", minvalue=0)
        if angle:
            self.canvas.delete("all")
            for layer, items in self.layers.items():
                for item in items:
                    coords = self.rotate_coords(item['coords'], angle)
                    item['coords'] = coords
                    self.draw_item(item, layer)
            self.draw_grid()

    def rotate_coords(self, coords, angle):
        from math import radians, cos, sin
        angle = radians(angle)
        new_coords = []
        for i in range(0, len(coords), 2):
            x, y = coords[i], coords[i+1]
            new_x = x * cos(angle) - y * sin(angle)
            new_y = x * sin(angle) + y * cos(angle)
            new_coords.extend([new_x, new_y])
        return new_coords

    def manage_layers(self):
        layers_window = tk.Toplevel(self.root)
        layers_window.title("Zarządzaj Warstwami")
        tk.Label(layers_window, text="Aktualna Warstwa:").pack(pady=5)
        layer_var = tk.StringVar(value=self.current_layer)
        layer_menu = tk.OptionMenu(layers_window, layer_var, *self.layers.keys())
        layer_menu.pack(pady=5)

        def set_layer():
            self.current_layer = layer_var.get()
            layers_window.destroy()

        def add_layer():
            new_layer = simpledialog.askstring("Nowa Warstwa", "Nazwa nowej warstwy:")
            if new_layer and new_layer not in self.layers:
                self.layers[new_layer] = []
                layer_var.set(new_layer)
                layer_menu["menu"].add_command(label=new_layer, command=tk._setit(layer_var, new_layer))
        
        def delete_layer():
            if len(self.layers) > 1:
                del self.layers[self.current_layer]
                self.current_layer = list(self.layers.keys())[0]
                layer_var.set(self.current_layer)
                layer_menu["menu"].delete(0, "end")
                for layer in self.layers.keys():
                    layer_menu["menu"].add_command(label=layer, command=tk._setit(layer_var, layer))
            else:
                messagebox.showwarning("Ostrzeżenie", "Musi istnieć przynajmniej jedna warstwa.")
        
        tk.Button(layers_window, text="Ustaw Warstwę", command=set_layer).pack(pady=5)
        tk.Button(layers_window, text="Dodaj Warstwę", command=add_layer).pack(pady=5)
        tk.Button(layers_window, text="Usuń Warstwę", command=delete_layer).pack(pady=5)

    def add_text(self):
        text = simpledialog.askstring("Dodaj Tekst", "Wprowadź tekst:")
        if text:
            self.canvas.create_text(400, 300, text=text, fill=self.current_color, tags=self.current_layer)

    def draw(self, event):
        if self.start_x is None or self.start_y is None:
            self.start_x = event.x
            self.start_y = event.y
            return

        if self.selected_tool == "line":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.current_color, width=self.line_width, tags=self.current_layer)
        elif self.selected_tool == "rect":
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.current_color, width=self.line)
