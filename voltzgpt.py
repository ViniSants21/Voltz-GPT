import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import random

# --- Configurações Globais e Temas ---
THEMES = {
    "light": {
        "bg_main": "#f5f5f5", "bg_sec": "#ffffff", "fg_main": "#000000",
        "entry_bg": "#ffffff", "msg_user_bg": "#dcf8c6", "msg_bot_bg": "#e9e9eb",
        "btn_bg": "#e0e0e0", "accent": "#0078d7"
    },
    "dark": {
        "bg_main": "#121212", "bg_sec": "#1e1e1e", "fg_main": "#ffffff",
        "entry_bg": "#2d2d2d", "msg_user_bg": "#005c4b", "msg_bot_bg": "#2d2d2d",
        "btn_bg": "#333333", "accent": "#0078d7"
    }
}

# Simulação de base de conhecimento de TI
IT_RESPONSES = {
    "python": (
        "Python é uma linguagem de programação poderosa e de fácil aprendizado. "
        "Ela é muito usada em automação, análise de dados, desenvolvimento web, inteligência artificial e cibersegurança. "
        "Sua sintaxe simples e vasta quantidade de bibliotecas, como pandas, Django e TensorFlow, a tornam ideal tanto para iniciantes quanto para profissionais."
    ),

    "java": (
        "Java é uma linguagem orientada a objetos amplamente usada em aplicações corporativas, sistemas Android e back-end. "
        "É conhecida pela portabilidade — o código escrito em Java pode rodar em qualquer sistema que tenha a JVM (Java Virtual Machine). "
        "Frameworks populares como Spring e Hibernate tornam o desenvolvimento mais ágil e robusto."
    ),

    "html": (
        "HTML (HyperText Markup Language) é a linguagem base da web, usada para estruturar páginas e conteúdos na internet. "
        "Ela define elementos como títulos, parágrafos, links, imagens e tabelas. "
        "Apesar de simples, é essencial para qualquer desenvolvedor web, servindo como fundação para o uso de CSS e JavaScript."
    ),

    "css": (
        "CSS (Cascading Style Sheets) é usado para estilizar páginas HTML, controlando cores, fontes, tamanhos e layout. "
        "Com ele, é possível criar interfaces modernas e responsivas. "
        "Frameworks como Bootstrap e Tailwind CSS aceleram o design e garantem compatibilidade entre dispositivos."
    ),

    "javascript": (
        "JavaScript é a linguagem da web responsável pela interatividade das páginas. "
        "Permite criar animações, validações de formulários e comunicação com servidores sem recarregar a página. "
        "Com o Node.js, também pode ser usado no back-end, e frameworks como React, Vue e Angular dominam o desenvolvimento moderno."
    ),

    "banco de dados": (
        "Bancos de dados armazenam e organizam informações de forma estruturada. "
        "Os principais tipos são os relacionais, como MySQL e PostgreSQL, e os não relacionais, como MongoDB. "
        "Consultas são feitas com linguagens como SQL, que permite buscar, inserir e alterar dados com precisão."
    ),

    "inteligência artificial": (
        "Inteligência Artificial (IA) é o campo da computação que busca criar sistemas capazes de aprender e tomar decisões. "
        "Ela abrange aprendizado de máquina, visão computacional, processamento de linguagem natural e redes neurais. "
        "Ferramentas como TensorFlow e PyTorch são amplamente usadas nesse setor, revolucionando áreas como saúde, finanças e automação."
    ),

    "c": (
        "C é uma das linguagens de programação mais antigas e influentes da história. "
        "Ela é usada em sistemas operacionais, drivers e softwares que exigem alto desempenho. "
        "Por ser de baixo nível, dá ao programador controle direto sobre a memória e o hardware, sendo ideal para quem quer entender o funcionamento interno dos computadores."
    ),

    "c++": (
        "C++ é uma evolução da linguagem C, adicionando suporte à programação orientada a objetos. "
        "É muito usada em jogos, aplicações de alto desempenho e softwares de engenharia. "
        "Sua flexibilidade e velocidade a tornam uma escolha comum para sistemas complexos e desenvolvimento de engines gráficas."
    ),

    "php": (
        "PHP é uma linguagem voltada ao desenvolvimento web, muito usada em sites dinâmicos e sistemas de gerenciamento de conteúdo como WordPress. "
        "Ela roda no servidor e é facilmente integrada com HTML e bancos de dados MySQL. "
        "Apesar da concorrência moderna, continua popular por sua simplicidade e ampla compatibilidade com hospedagens."
    ),

    "redes": (
        "Redes de computadores são sistemas que permitem a comunicação e o compartilhamento de dados entre dispositivos. "
        "Conceitos fundamentais incluem IP (identificação de dispositivos), DNS (tradução de nomes de domínio), DHCP (atribuição automática de endereços IP) e o modelo OSI, "
        "que organiza as camadas de comunicação — da física até a aplicação. Conhecer esses princípios é essencial para administrar e proteger uma rede."
    ),

    "hardware": (
        "Hardware é o conjunto de componentes físicos de um computador, como processador (CPU), memória RAM, placa-mãe, disco rígido (HD ou SSD) e periféricos. "
        "A performance do sistema depende do equilíbrio entre esses elementos. "
        "Por exemplo, uma CPU potente sem RAM suficiente causará gargalos, enquanto um SSD acelera o carregamento de dados e o tempo de inicialização do sistema."
    ),

    "segurança": (
        "Segurança da informação é o conjunto de práticas e tecnologias voltadas à proteção de dados contra acessos indevidos, alterações ou destruições. "
        "Ela se baseia nos pilares de confidencialidade, integridade e disponibilidade. "
        "Boas práticas incluem o uso de senhas fortes, autenticação de dois fatores, criptografia de dados, backups regulares e atualização constante de sistemas."
    ),

    "linux": (
        "Linux é um sistema operacional de código aberto amplamente usado em servidores, dispositivos embarcados e ambientes de desenvolvimento. "
        "Sua principal vantagem é a estabilidade, segurança e liberdade de personalização. "
        "Distribuições populares incluem Ubuntu, Debian, Fedora e Arch Linux. "
        "Além disso, o terminal do Linux oferece um controle avançado sobre o sistema, ideal para administradores e desenvolvedores."
    ),

    "padrão": (
        "Interessante! Posso conversar sobre diversos assuntos de tecnologia da informação: Python, Java, C, C++, PHP, HTML, CSS, JavaScript, Bancos de Dados, Linux, Segurança e muito mais. "
        "Escolha um tema e posso te explicar de forma técnica ou resumida, como preferir."
    )
}



class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        # ALTERAÇÃO 1: Título da janela atualizado
        self.title("Voltz GPT - Assistente TI")
        self.geometry("900x700")
        self.current_theme = "light"
        self.user = None
        
        self.configure_styles()
        self.show_login_screen()

    def configure_styles(self):
        """Configura os estilos iniciais (ttk)."""
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.update_theme_styles()

    def update_theme_styles(self):
        """Atualiza as cores do estilo ttk com base no tema atual."""
        theme = THEMES[self.current_theme]
        self.configure(bg=theme["bg_main"])
        
        # Estilos gerais
        self.style.configure("TFrame", background=theme["bg_main"])
        self.style.configure("TLabel", background=theme["bg_main"], foreground=theme["fg_main"], font=("Helvetica", 11))
        self.style.configure("TButton", background=theme["btn_bg"], foreground=theme["fg_main"], font=("Helvetica", 10), borderwidth=1)
        self.style.map("TButton", background=[("active", theme["accent"])], foreground=[("active", "white")])
        
        # Estilos específicos
        self.style.configure("Login.TFrame", background=theme["bg_sec"], relief="raised")
        self.style.configure("Chat.TFrame", background=theme["bg_sec"])
        self.style.configure("MsgBox.TFrame", background=theme["bg_sec"])

    def show_login_screen(self):
        """Exibe a tela de login."""
        self.clear_window()
        
        login_frame = ttk.Frame(self, style="Login.TFrame", padding=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        theme = THEMES[self.current_theme]
        # ALTERAÇÃO 2: Título do login atualizado
        ttk.Label(login_frame, text="Voltz GPT Login", font=("Helvetica", 20, "bold"), background=theme["bg_sec"]).pack(pady=(0, 20))
        
        ttk.Label(login_frame, text="Usuário (admin):", background=theme["bg_sec"]).pack(anchor="w")
        self.user_entry = ttk.Entry(login_frame, font=("Helvetica", 12))
        self.user_entry.pack(fill="x", pady=(0, 15))
        
        ttk.Label(login_frame, text="Senha (1234):", background=theme["bg_sec"]).pack(anchor="w")
        self.pass_entry = ttk.Entry(login_frame, show="*", font=("Helvetica", 12))
        self.pass_entry.pack(fill="x", pady=(0, 20))
        
        login_btn = ttk.Button(login_frame, text="ENTRAR", command=self.validate_login)
        login_btn.pack(fill="x", ipady=5)

    def validate_login(self):
        """Valida as credenciais."""
        user = self.user_entry.get()
        password = self.pass_entry.get()
        
        if user == "admin" and password == "1234":
            self.user = user
            self.show_chat_screen()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos!")

    def show_chat_screen(self):
        """Exibe a tela principal do chat."""
        self.clear_window()
        theme = THEMES[self.current_theme]
        
        # === Cabeçalho ===
        header = ttk.Frame(self, padding=10)
        header.pack(fill="x")
        
        # Avatar do usuário atual (canto esquerdo)
        user_icon_canvas = tk.Canvas(header, width=40, height=40, bg=theme["bg_main"], highlightthickness=0)
        user_icon_canvas.create_oval(2, 2, 38, 38, fill=theme["accent"], outline="")
        user_icon_canvas.create_text(20, 20, text=self.user[0].upper(), fill="white", font=("Helvetica", 14, "bold"))
        user_icon_canvas.pack(side="left")
        
        ttk.Label(header, text=f" Olá, {self.user}!", font=("Helvetica", 14)).pack(side="left", padx=10)
        
        btn_theme = ttk.Button(header, text="🌗 Tema", command=self.toggle_theme, width=8)
        btn_theme.pack(side="right")
        
        # === Área de Chat (Scroll) ===
        chat_container = ttk.Frame(self)
        chat_container.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.chat_canvas = tk.Canvas(chat_container, bg=theme["bg_sec"], highlightthickness=0)
        self.chat_scrollbar = ttk.Scrollbar(chat_container, orient="vertical", command=self.chat_canvas.yview)
        
        self.chat_inner_frame = ttk.Frame(self.chat_canvas, style="Chat.TFrame")
        self.chat_canvas.create_window((0, 0), window=self.chat_inner_frame, anchor="nw", tags="inner_frame")
        
        self.chat_canvas.configure(yscrollcommand=self.chat_scrollbar.set)
        
        self.chat_scrollbar.pack(side="right", fill="y")
        self.chat_canvas.pack(side="left", fill="both", expand=True)
        
        self.chat_inner_frame.bind("<Configure>", lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.bind("<Configure>", self.on_canvas_configure)
        
        # === Rodapé (Entrada de Texto) ===
        footer = ttk.Frame(self, padding=10)
        footer.pack(fill="x")
        
        self.msg_entry = tk.Entry(footer, font=("Helvetica", 12), bd=0, bg=theme["entry_bg"], fg=theme["fg_main"], relief="flat")
        self.msg_entry.pack(side="left", fill="both", expand=True, padx=(0, 10), ipady=8)
        self.msg_entry.bind("<Return>", lambda e: self.send_message())
        
        btn_send = ttk.Button(footer, text="Enviar ➤", command=self.send_message)
        btn_send.pack(side="right", padx=5)
        
        btn_clear = ttk.Button(footer, text="Limpar", command=self.clear_chat)
        btn_clear.pack(side="right")

    def on_canvas_configure(self, event):
        """Ajusta a largura do frame interno do chat."""
        self.chat_canvas.itemconfig("inner_frame", width=event.width)

    def send_message(self):
        """Envia a mensagem do usuário e inicia a resposta da IA."""
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        
        self.msg_entry.delete(0, "end")
        self.add_message(self.user, msg, is_user=True)
        
        # Thread para simular processamento da IA sem travar a UI
        threading.Thread(target=self.process_ai_response, args=(msg,), daemon=True).start()

    def process_ai_response(self, user_msg):
        """Simula o pensamento da IA e devolve a resposta."""
        time.sleep(1.5)  # Simulação de atraso/thinking
        
        response = IT_RESPONSES["padrão"]
        msg_lower = user_msg.lower()
        
        for key, value in IT_RESPONSES.items():
            if key in msg_lower:
                response = value
                break
        
        # ALTERAÇÃO 3: Nome da IA que responde foi atualizado
        self.after(0, lambda: self.add_message("Voltz GPT", response, is_user=False))

    def add_message(self, sender, text, is_user=True):
        """Adiciona uma mensagem visualmente à tela de chat."""
        theme = THEMES[self.current_theme]
        bg_color = theme["msg_user_bg"] if is_user else theme["msg_bot_bg"]
        align = "e" if is_user else "w" # east (direita) ou west (esquerda)
        
        msg_container = tk.Frame(self.chat_inner_frame, bg=theme["bg_sec"])
        msg_container.pack(fill="x", pady=5, padx=10)
        
        # Frame wrapper para alinhamento
        wrapper = tk.Frame(msg_container, bg=theme["bg_sec"])
        wrapper.pack(anchor=align)
        
        # Avatar
        avatar_color = theme["accent"] if is_user else "#e74c3c"
        initial = sender[0].upper()
        
        avatar = tk.Canvas(wrapper, width=35, height=35, bg=theme["bg_sec"], highlightthickness=0)
        avatar.create_oval(2, 2, 33, 33, fill=avatar_color, outline="")
        avatar.create_text(17, 17, text=initial, fill="white", font=("Helvetica", 10, "bold"))
        
        # Conteúdo da mensagem
        msg_frame = tk.LabelFrame(wrapper, text=f" {sender} ", bg=bg_color, fg=theme["fg_main"], bd=0, font=("Helvetica", 9, "bold"))
        msg_label = tk.Label(msg_frame, text=text, bg=bg_color, fg=theme["fg_main"], font=("Helvetica", 11), wraplength=400, justify="left", padx=10, pady=5)
        msg_label.pack()
        
        if is_user:
            msg_frame.pack(side="right", padx=5)
            avatar.pack(side="right")
        else:
            avatar.pack(side="left")
            msg_frame.pack(side="left", padx=5)
            
        # Scroll automático para o final
        self.chat_canvas.update_idletasks()
        self.chat_canvas.yview_moveto(1.0)

    def clear_chat(self):
        """Limpa a conversa."""
        for widget in self.chat_inner_frame.winfo_children():
            widget.destroy()

    def toggle_theme(self):
        """Alterna entre modos claro e escuro."""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.update_theme_styles()
        # Recria a tela atual para aplicar cores
        if getattr(self, 'user', None):
             # Salva o histórico atual para restaurar (opcional avançado)
             # Por simplicidade, recarregamos a estrutura limpa
             self.show_chat_screen()
             self.clear_chat() # Limpa pois mudou a cor dos widgets antigos
             messagebox.showinfo("Tema Alterado", "O tema foi alterado. O chat foi limpo para aplicar os novos estilos.")
        else:
            self.show_login_screen()

    def clear_window(self):
        """Remove todos os widgets da janela."""
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()