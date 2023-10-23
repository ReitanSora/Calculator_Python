import tkinter as tk
from static import style


class Calculator(tk.Tk):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.geometry("375x600")
        self.resizable(False, False)
        self.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 3)
        }

        self.operators = {'/': "\u00F7", '*': "\u00D7", '-': '-', '+': '+'}

        self.init_frames()
        self.display_label()
        self.init_buttons()
        self.bind_keys()

    def init_frames(self):

        # display frame
        self.display_frame = tk.Frame(self,
                                      height=220,
                                      bg=style.BG_OSCURO)
        self.display_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # buttons frame
        self.button_frame = tk.Frame(self,
                                     bg=style.BG_OSCURO)
        self.button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        for x in range(1, 5):
            self.button_frame.rowconfigure(x, weight=1)
            self.button_frame.columnconfigure(x, weight=1)

    def init_buttons(self):
        # index to create operator's positions
        i = 0

        # digits
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.button_frame,
                               text=str(digit),
                               **style.BUTTON,
                               command=lambda x=digit: self.add_to_expression(x))
            button.grid(
                row=grid_value[0], column=grid_value[1], sticky=tk.NSEW, padx=2, pady=2)

        # operators
        for operator, symbol in self.operators.items():
            button = tk.Button(self.button_frame,
                               text=symbol, **style.BUTTON,
                               command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW, padx=2, pady=2)
            i += 1

        # clear
        button = tk.Button(self.button_frame, text='C', **style.BUTTON, command=self.clear)
        button.grid(row=4, column=1, sticky=tk.NSEW, padx=2, pady=2)

        # equals
        button = tk.Button(self.button_frame, text='=', **style.BUTTON, command=self.evaluate)
        button.grid(row=4, column=4, sticky=tk.NSEW, padx=2, pady=2)

        # percent
        button = tk.Button(self.button_frame, text='%', **style.BUTTON, command=self.percent)
        button.grid(row=0, column=1, sticky=tk.NSEW, padx=2, pady=2)

        # square
        button = tk.Button(self.button_frame, text='x \u00B2', **style.BUTTON, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW, padx=2, pady=2)

        # sqrt
        button = tk.Button(self.button_frame, text='\u221A x', **style.BUTTON, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW, padx=2, pady=2)

    def display_label(self):
        self.total_label = tk.Label(self.display_frame,
                                    text=self.total_expression,
                                    anchor=tk.E,
                                    **style.TOTAL_LABEL,)
        self.total_label.pack(expand=True, fill=tk.BOTH, padx=20)

        self.label = tk.Label(self.display_frame,
                              text=self.total_expression,
                              anchor=tk.E,
                              **style.LABEL,)
        self.label.pack(expand=True, fill=tk.BOTH, padx=20)

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operators.items():
            expression = expression.replace(operator, f'{symbol}')

        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_total_label()
        self.update_label()
        
    def evaluate(self):
        self.total_expression +=self.current_expression
        self.update_total_label()
        try:
            self.current_expression= str(eval(self.total_expression))
            self.total_expression = ""
        except Exception:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def square(self):
        self.current_expression = str(eval(f'{self.current_expression}**2'))
        self.update_label()
    
    def sqrt(self):
        self.current_expression = str(eval(f'{self.current_expression}**0.5'))
        self.update_label()
    
    def percent(self):
        self.current_expression = str(eval(f'{self.current_expression}/100'))
        self.update_label()

    def bind_keys(self):
        self.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.bind(str(key), lambda event, digit = key: self.add_to_expression(digit))
        
        for key in self.operators:
            self.bind(key, lambda event, operator= key: self.append_operator(operator))