import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import requests
from typing import Optional


class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Analyzer 🔍")
        self.root.geometry("1200x800")
        self.root.minsize(900, 650)

        # Современная цветовая палитра с градиентами
        self.bg_primary = "#0f0f23"
        self.bg_secondary = "#1a1a2e"
        self.bg_tertiary = "#16213e"
        self.accent_blue = "#4a9eff"
        self.accent_purple = "#a855f7"
        self.accent_cyan = "#06b6d4"
        self.fg_primary = "#e2e8f0"
        self.fg_secondary = "#94a3b8"
        self.success_green = "#10b981"
        self.error_red = "#ef4444"
        self.warning_yellow = "#f59e0b"

        self.config_file = "config.json"
        self.api_key = self.load_api_key()

        if not self.api_key:
            self.request_api_key()

        self.setup_ui()

    def load_api_key(self) -> Optional[str]:
        """Загрузка API ключа из config.json"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('api_key')
            except Exception:
                return None
        return None

    def save_api_key(self, api_key: str):
        """Сохранение API ключа в config.json"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump({'api_key': api_key}, f)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить ключ: {e}")

    def request_api_key(self):
        """Диалоговое окно для ввода API ключа"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔑 API Configuration")
        dialog.geometry("500x250")
        dialog.resizable(False, False)
        dialog.configure(bg=self.bg_secondary)
        dialog.transient(self.root)
        dialog.grab_set()

        # Заголовок
        header_frame = tk.Frame(dialog, bg=self.bg_primary, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🔑 OpenRouter API Key",
            bg=self.bg_primary,
            fg=self.accent_blue,
            font=("Segoe UI", 14, "bold")
        ).pack(pady=15)

        # Основной контент
        content_frame = tk.Frame(dialog, bg=self.bg_secondary)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        tk.Label(
            content_frame,
            text="Введите ваш API ключ от OpenRouter:",
            bg=self.bg_secondary,
            fg=self.fg_primary,
            font=("Segoe UI", 10)
        ).pack(pady=(0, 10))

        # Поле ввода с современным стилем
        key_frame = tk.Frame(content_frame, bg=self.bg_tertiary, highlightbackground=self.accent_blue,
                             highlightthickness=2)
        key_frame.pack(fill=tk.X, pady=5)

        key_entry = tk.Entry(
            key_frame,
            font=("Consolas", 10),
            bg=self.bg_tertiary,
            fg=self.fg_primary,
            insertbackground=self.accent_cyan,
            relief=tk.FLAT,
            show="●"
        )
        key_entry.pack(fill=tk.X, padx=10, pady=8)
        key_entry.focus()

        def save_key():
            key = key_entry.get().strip()
            if key:
                self.api_key = key
                self.save_api_key(key)
                dialog.destroy()
            else:
                messagebox.showwarning("⚠️ Предупреждение", "Ключ не может быть пустым!")

        def on_cancel():
            if not self.api_key:
                self.root.destroy()
            dialog.destroy()

        # Кнопки
        btn_frame = tk.Frame(content_frame, bg=self.bg_secondary)
        btn_frame.pack(pady=15)

        save_btn = tk.Button(
            btn_frame,
            text="✓ Сохранить",
            command=save_key,
            bg=self.accent_blue,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            activebackground=self.accent_purple
        )
        save_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="✕ Отмена",
            command=on_cancel,
            bg=self.bg_tertiary,
            fg=self.fg_secondary,
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            padx=30,
            pady=10,
            cursor="hand2",
            activebackground=self.error_red
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

        key_entry.bind('<Return>', lambda e: save_key())
        dialog.protocol("WM_DELETE_WINDOW", on_cancel)

        self.root.wait_window(dialog)

    def setup_ui(self):
        """Настройка интерфейса"""
        self.root.configure(bg=self.bg_primary)

        # Создаем главный контейнер с отступами
        main_container = tk.Frame(self.root, bg=self.bg_primary)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # ============ HEADER ============
        header_frame = tk.Frame(main_container, bg=self.bg_secondary, height=70)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        header_frame.pack_propagate(False)

        # Заголовок с градиентным эффектом (имитация)
        title_frame = tk.Frame(header_frame, bg=self.bg_secondary)
        title_frame.pack(expand=True)

        tk.Label(
            title_frame,
            text="🔍 Python Code Analyzer",
            bg=self.bg_secondary,
            fg=self.accent_blue,
            font=("Segoe UI", 22, "bold")
        ).pack(side=tk.LEFT, padx=5)

        tk.Label(
            title_frame,
            text="AI-Powered",
            bg=self.bg_secondary,
            fg=self.accent_purple,
            font=("Segoe UI", 13, "italic")
        ).pack(side=tk.LEFT)

        # ============ CONTROL PANEL ============
        control_frame = tk.Frame(main_container, bg=self.bg_secondary, height=60)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        control_frame.pack_propagate(False)

        # Внутренние отступы для панели управления
        control_inner = tk.Frame(control_frame, bg=self.bg_secondary)
        control_inner.pack(expand=True)

        # Тип анализа с иконкой
        analysis_label = tk.Label(
            control_inner,
            text="📊 Тип анализа:",
            bg=self.bg_secondary,
            fg=self.accent_cyan,
            font=("Segoe UI", 11, "bold")
        )
        analysis_label.pack(side=tk.LEFT, padx=(20, 10))

        # Стилизованный Combobox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Custom.TCombobox',
            fieldbackground=self.bg_tertiary,
            background=self.bg_tertiary,
            foreground=self.fg_primary,
            arrowcolor=self.accent_blue,
            borderwidth=0
        )

        self.analysis_type = ttk.Combobox(
            control_inner,
            values=[
                "🔍 Полный аудит (ошибки, PEP 8, оптимизация)",
                "🐛 Только баги и ошибки",
                "📏 Проверка PEP 8 стандарта",
                "📖 Объяснение работы кода"
            ],
            state="readonly",
            width=42,
            font=("Segoe UI", 10),
            style='Custom.TCombobox'
        )
        self.analysis_type.current(0)
        self.analysis_type.pack(side=tk.LEFT, padx=10)

        # Модель скрыта, используется только Mistral
        self.model_choice_value = "mistralai/mistral-7b-instruct:free"

        # Индикатор модели
        model_label = tk.Label(
            control_inner,
            text="⚡ Mistral 7B",
            bg=self.bg_secondary,
            fg=self.success_green,
            font=("Segoe UI", 10, "bold")
        )
        model_label.pack(side=tk.RIGHT, padx=20)

        # ============ INPUT SECTION ============
        input_section = tk.Frame(main_container, bg=self.bg_primary, height=250)
        input_section.pack(fill=tk.X, pady=(0, 15))
        input_section.pack_propagate(False)

        # Заголовок секции
        input_header = tk.Frame(input_section, bg=self.bg_primary, height=35)
        input_header.pack(fill=tk.X, pady=(0, 5))
        input_header.pack_propagate(False)

        tk.Label(
            input_header,
            text="💻 Введите Python код",
            bg=self.bg_primary,
            fg=self.fg_primary,
            font=("Segoe UI", 12, "bold")
        ).pack(side=tk.LEFT, pady=5)

        # Кнопки быстрых действий
        quick_buttons = tk.Frame(input_header, bg=self.bg_primary)
        quick_buttons.pack(side=tk.RIGHT, pady=5)

        paste_btn = tk.Button(
            quick_buttons,
            text="📋 Вставить",
            command=self.paste_code,
            bg=self.bg_tertiary,
            fg=self.accent_cyan,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=5,
            cursor="hand2",
            activebackground=self.bg_secondary
        )
        paste_btn.pack(side=tk.LEFT, padx=3)

        example_btn = tk.Button(
            quick_buttons,
            text="📄 Пример",
            command=self.load_example_code,
            bg=self.bg_tertiary,
            fg=self.accent_purple,
            font=("Segoe UI", 9, "bold"),
            relief=tk.FLAT,
            padx=12,
            pady=5,
            cursor="hand2",
            activebackground=self.bg_secondary
        )
        example_btn.pack(side=tk.LEFT, padx=3)

        # Поле ввода кода с эффектом свечения
        input_frame = tk.Frame(
            input_section,
            bg=self.bg_tertiary,
            highlightbackground=self.accent_blue,
            highlightthickness=2
        )
        input_frame.pack(fill=tk.BOTH, expand=True)

        self.code_input = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.NONE,
            bg=self.bg_tertiary,
            fg=self.fg_primary,
            insertbackground=self.accent_cyan,
            font=("Consolas", 10),
            relief=tk.FLAT,
            padx=12,
            pady=12,
            undo=True,
            maxundo=-1,
            selectbackground=self.accent_purple,
            selectforeground="white"
        )
        self.code_input.pack(fill=tk.BOTH, expand=True)

        # Контекстное меню
        self.create_context_menu()

        # ============ ANALYZE BUTTON ============
        analyze_frame = tk.Frame(main_container, bg=self.bg_primary, height=60)
        analyze_frame.pack(fill=tk.X, pady=10)
        analyze_frame.pack_propagate(False)

        analyze_btn = tk.Button(
            analyze_frame,
            text="🚀 АНАЛИЗИРОВАТЬ КОД",
            command=self.analyze_code,
            bg=self.accent_blue,
            fg="white",
            font=("Segoe UI", 12, "bold"),
            relief=tk.FLAT,
            padx=40,
            pady=12,
            cursor="hand2",
            activebackground=self.accent_purple
        )
        analyze_btn.pack(expand=True)

        # Эффект при наведении
        def on_enter(e):
            analyze_btn['bg'] = self.accent_purple

        def on_leave(e):
            analyze_btn['bg'] = self.accent_blue

        analyze_btn.bind("<Enter>", on_enter)
        analyze_btn.bind("<Leave>", on_leave)

        # ============ OUTPUT SECTION ============
        output_section = tk.Frame(main_container, bg=self.bg_primary)
        output_section.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Заголовок результата
        output_header = tk.Frame(output_section, bg=self.bg_primary, height=35)
        output_header.pack(fill=tk.X, pady=(0, 5))
        output_header.pack_propagate(False)

        tk.Label(
            output_header,
            text="📊 Результат анализа",
            bg=self.bg_primary,
            fg=self.fg_primary,
            font=("Segoe UI", 12, "bold")
        ).pack(side=tk.LEFT, pady=5)

        # Статус индикатор
        self.status_label = tk.Label(
            output_header,
            text="",
            bg=self.bg_primary,
            fg=self.success_green,
            font=("Segoe UI", 10, "bold")
        )
        self.status_label.pack(side=tk.RIGHT, pady=5)

        # Поле вывода
        output_frame = tk.Frame(
            output_section,
            bg=self.bg_tertiary,
            highlightbackground=self.accent_cyan,
            highlightthickness=2
        )
        output_frame.pack(fill=tk.BOTH, expand=True)

        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            bg=self.bg_tertiary,
            fg="#ffffff",
            font=("Consolas", 10),
            relief=tk.FLAT,
            padx=15,
            pady=15,
            state=tk.DISABLED,
            selectbackground=self.accent_blue,
            selectforeground="white"
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # ============ BOTTOM ACTIONS ============
        bottom_frame = tk.Frame(main_container, bg=self.bg_primary, height=50)
        bottom_frame.pack(fill=tk.X)
        bottom_frame.pack_propagate(False)

        # Левая группа кнопок
        left_buttons = tk.Frame(bottom_frame, bg=self.bg_primary)
        left_buttons.pack(side=tk.LEFT, pady=5)

        copy_btn = tk.Button(
            left_buttons,
            text="📋 Скопировать",
            command=self.copy_report,
            bg=self.bg_secondary,
            fg=self.accent_cyan,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=18,
            pady=8,
            cursor="hand2",
            activebackground=self.bg_tertiary
        )
        copy_btn.pack(side=tk.LEFT, padx=(0, 8))

        clear_btn = tk.Button(
            left_buttons,
            text="🗑️ Очистить",
            command=self.clear_all,
            bg=self.bg_secondary,
            fg=self.warning_yellow,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=18,
            pady=8,
            cursor="hand2",
            activebackground=self.bg_tertiary
        )
        clear_btn.pack(side=tk.LEFT)

        # Правая группа кнопок
        right_buttons = tk.Frame(bottom_frame, bg=self.bg_primary)
        right_buttons.pack(side=tk.RIGHT, pady=5)

        key_btn = tk.Button(
            right_buttons,
            text="🔑 API Ключ",
            command=self.request_api_key,
            bg=self.bg_secondary,
            fg=self.accent_purple,
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            padx=18,
            pady=8,
            cursor="hand2",
            activebackground=self.bg_tertiary
        )
        key_btn.pack()

        # Привязка горячих клавиш
        self.code_input.bind('<Control-v>', lambda e: self.paste_code())
        self.code_input.bind('<Control-V>', lambda e: self.paste_code())

    def create_context_menu(self):
        """Создание контекстного меню"""
        self.context_menu = tk.Menu(
            self.code_input,
            tearoff=0,
            bg=self.bg_tertiary,
            fg=self.fg_primary,
            activebackground=self.accent_blue,
            activeforeground="white",
            font=("Segoe UI", 9)
        )
        self.context_menu.add_command(label="📋 Вставить", command=self.paste_code)
        self.context_menu.add_command(label="📄 Копировать", command=lambda: self.code_input.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="✂️ Вырезать", command=lambda: self.code_input.event_generate("<<Cut>>"))
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🗑️ Очистить", command=lambda: self.code_input.delete("1.0", tk.END))

        self.code_input.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        """Показать контекстное меню"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def paste_code(self):
        """Вставка кода из буфера обмена"""
        try:
            clipboard_content = self.root.clipboard_get()
            self.code_input.insert(tk.INSERT, clipboard_content)
            return "break"  # Предотвращаем двойную вставку
        except tk.TclError:
            messagebox.showwarning("Предупреждение", "Буфер обмена пуст!")

    def load_example_code(self):
        """Загрузка примера кода с ошибками"""
        example_code = """# Калькулятор с ошибками для тестирования

def calculate_average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total / len(numbers)  # Деление на ноль не проверяется

def find_Maximum(List):  # Нарушение PEP 8
    max=List[0]  # Нет пробелов
    for i in List:
        if i>max:
            max=i
    return max

class userProfile:  # Неправильное имя класса
    def __init__(self,name,age):
        self.name=name
        self.age=age

    def is_adult(self):
        if self.age >= 18
            return True  # Отсутствует двоеточие
        else:
            return False

def divide_numbers(a, b):
    result = a / b  # Деление на ноль
    return result

# Главная функция
if __name__ == '__main__':
    numbers = [1, 2, 3, 4, 5]
    avg = calculate_average(numbers)
    print(f"Average: {avg}")

    empty_list = []
    max_val = find_Maximum(empty_list)  # Ошибка

    result = divide_numbers(10, 0)  # Деление на ноль
    print(result)"""

        self.code_input.delete("1.0", tk.END)
        self.code_input.insert("1.0", example_code)
        messagebox.showinfo("Успех", "Пример кода загружен!")

    def get_prompt(self, code: str, analysis_type: str) -> str:
        """Генерация промпта в зависимости от типа анализа"""
        prompts = {
            "Полный аудит (ошибки, PEP 8, оптимизация, объяснение)": f"""Проведи полный аудит следующего Python кода:

```python
{code}
```

Проанализируй код по следующим аспектам:
1. **Ошибки и баги**: Найди потенциальные ошибки, исключения, логические проблемы
2. **PEP 8**: Проверь соответствие стандарту PEP 8 (отступы, именование, длина строк)
3. **Оптимизация**: Предложи улучшения производительности и эффективности
4. **Объяснение**: Кратко опиши, что делает этот код

Ответ структурируй по разделам с примерами и рекомендациями.""",

            "Только баги": f"""Найди все потенциальные ошибки и баги в этом Python коде:

```python
{code}
```

Укажи:
- Синтаксические ошибки
- Логические ошибки
- Потенциальные исключения
- Проблемы с типами данных
- Другие проблемы, которые могут привести к сбоям

Для каждой ошибки предложи исправление.""",

            "PEP 8": f"""Проверь соответствие этого Python кода стандарту PEP 8:

```python
{code}
```

Проверь:
- Именование переменных, функций, классов
- Отступы и пробелы
- Длину строк
- Импорты
- Комментарии и docstrings
- Другие стилистические аспекты

Для каждого нарушения предложи исправленный вариант.""",

            "Объяснение кода": f"""Подробно объясни, что делает этот Python код:

```python
{code}
```

Опиши:
- Общую цель и назначение кода
- Как работает каждая часть
- Используемые алгоритмы и подходы
- Зависимости и внешние библиотеки (если есть)
- Возможные варианты использования

Объясняй простым языком, как для начинающего разработчика."""
        }

        return prompts.get(analysis_type, prompts["Полный аудит (ошибки, PEP 8, оптимизация, объяснение)"])

    def analyze_code(self):
        """Отправка кода на анализ через OpenRouter API"""
        code = self.code_input.get("1.0", tk.END).strip()

        if not code:
            messagebox.showwarning("Предупреждение", "Введите код для анализа!")
            return

        if not self.api_key:
            messagebox.showerror("Ошибка", "API ключ не установлен!")
            self.request_api_key()
            return

        analysis_type = self.analysis_type.get()
        model = self.model_choice_value

        # Показываем процесс анализа
        self.status_label.config(text="⏳ Анализ...", fg=self.warning_yellow)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "⏳ Отправка кода на анализ...\n\n")
        self.output_text.insert(tk.END, "Пожалуйста, подождите. Это может занять несколько секунд.\n")
        self.output_text.config(state=tk.DISABLED)
        self.root.update()

        try:
            prompt = self.get_prompt(code, analysis_type)

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "https://github.com/username/code-analyzer",
                "X-Title": "Python Code Analyzer",
                "Content-Type": "application/json"
            }

            data = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=90
            )

            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']

                self.status_label.config(text="✅ Готово", fg=self.success_green)
                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete("1.0", tk.END)

                # Красивый заголовок отчёта
                self.output_text.insert(tk.END, "╔" + "═" * 78 + "╗\n", "header")
                self.output_text.insert(tk.END, "║" + " " * 20 + "РЕЗУЛЬТАТ АНАЛИЗА" + " " * 41 + "║\n", "header")
                self.output_text.insert(tk.END, "╚" + "═" * 78 + "╝\n\n", "header")

                self.output_text.insert(tk.END, f"📊 Тип: ", "bold")
                self.output_text.insert(tk.END, f"{analysis_type}\n")
                self.output_text.insert(tk.END, f"⚡ Модель: ", "bold")
                self.output_text.insert(tk.END, "Mistral 7B Instruct\n")
                self.output_text.insert(tk.END, "─" * 80 + "\n\n")

                self.output_text.insert(tk.END, content)

                # Стили для текста
                self.output_text.tag_config("header", foreground=self.accent_cyan)
                self.output_text.tag_config("bold", foreground=self.accent_purple, font=("Consolas", 10, "bold"))

                self.output_text.config(state=tk.DISABLED)
            else:
                self.status_label.config(text="❌ Ошибка", fg=self.error_red)
                error_msg = f"❌ ОШИБКА API: {response.status_code}\n\n"

                try:
                    error_json = response.json()
                    if 'error' in error_json:
                        error_msg += f"Сообщение: {error_json['error'].get('message', 'Неизвестная ошибка')}\n"
                except:
                    error_msg += response.text

                if response.status_code == 401:
                    error_msg = "❌ Неверный API ключ.\n\n"
                    error_msg += "Проверьте ключ и попробуйте снова.\n"
                    error_msg += "Нажмите '🔑 API Ключ' для изменения."
                elif response.status_code == 404:
                    error_msg = f"❌ Модель недоступна.\n\n"
                    error_msg += "Попробуйте позже или обратитесь в поддержку OpenRouter."
                elif response.status_code == 402:
                    error_msg = "❌ Недостаточно средств на балансе OpenRouter.\n\n"
                    error_msg += "Пополните баланс на сайте openrouter.ai"

                self.output_text.config(state=tk.NORMAL)
                self.output_text.delete("1.0", tk.END)
                self.output_text.insert(tk.END, error_msg)
                self.output_text.config(state=tk.DISABLED)

        except requests.exceptions.Timeout:
            self.status_label.config(text="❌ Timeout", fg=self.error_red)
            messagebox.showerror("⏱️ Ошибка", "Превышено время ожидания ответа от сервера.")
        except requests.exceptions.ConnectionError:
            self.status_label.config(text="❌ Нет связи", fg=self.error_red)
            messagebox.showerror("🌐 Ошибка", "Ошибка подключения к интернету.")
        except Exception as e:
            self.status_label.config(text="❌ Ошибка", fg=self.error_red)
            messagebox.showerror("⚠️ Ошибка", f"Произошла ошибка: {str(e)}")

    def copy_report(self):
        """Копирование отчёта в буфер обмена"""
        report = self.output_text.get("1.0", tk.END).strip()
        if report:
            self.root.clipboard_clear()
            self.root.clipboard_append(report)
            messagebox.showinfo("Успех", "Отчёт скопирован в буфер обмена!")
        else:
            messagebox.showwarning("Предупреждение", "Нет отчёта для копирования!")

    def clear_all(self):
        """Очистка всех полей"""
        self.code_input.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = CodeAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()