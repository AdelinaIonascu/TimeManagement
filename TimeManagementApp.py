import PySimpleGUI as sg
from datetime import datetime

# Funcție pentru citirea sarcinilor din fișier
def read_tasks_from_file(filename):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []  # Dacă fișierul nu există, întoarcem o listă goală

# Funcție pentru salvarea sarcinilor în fișier
def write_tasks_to_file(filename, tasks):
    with open(filename, "w") as file:
        file.writelines(f"{task}\n" for task in tasks)

# Funcție pentru crearea interfeței
def create_window():
    # Setăm o temă personalizată
    sg.theme("DarkTeal9")

    # Fonturi și culori
    font_title = ("Trebuchet MS", 22, "bold")  # Font modern pentru titlu
    font_main = ("Calibri", 12, "bold")  # Font elegant pentru textul principal
    button_color = ("white", "#5D3FD3")  # Text alb, fundal mov
    listbox_color = {"text_color": "black", "background_color": "#B0E0E6"}  # Turcoaz deschis pentru listă
    bg_color = "#4682B4"  # Albastru oțel pentru fundal
    text_color = "#D8BFD8"  # Mov pal pentru text

    # Layout-ul aplicației
    layout = [
        [sg.Text("Gestiune Sarcini", font=font_title, justification="center", expand_x=True, text_color=text_color, background_color=bg_color)],
        [sg.HorizontalSeparator(color="#5D3FD3")],  # Linie separatoare în mov închis
        [sg.Text("Adaugă o nouă sarcină:", font=font_main, text_color=text_color, background_color=bg_color),
         sg.InputText(key="task_input", font=font_main, expand_x=True, background_color="#E0FFFF", text_color="#333333")],

        [sg.Button("Adaugă", font=font_main, size=(15, 1), button_color=button_color, border_width=0, pad=(5, 10)),
         sg.Button("Șterge", font=font_main, size=(15, 1), button_color=button_color, border_width=0, pad=(5, 10)),
         sg.Button("Editare", font=font_main, size=(15, 1), button_color=button_color, border_width=0, pad=(5, 10)),
         sg.Button("Ieșire", font=font_main, size=(15, 1), button_color=("white", "#DC143C"), border_width=0, pad=(5, 10))],

        [sg.Text("Lista Sarcinilor:", font=font_main, text_color=text_color, background_color=bg_color)],
        [sg.Listbox(values=[], size=(50, 10), key="task_list", font=font_main, **listbox_color, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],

        [sg.Button("Marchează ca finalizată", font=font_main, size=(20, 1), button_color=("white", "#20B2AA"), border_width=0, pad=(5, 10)),
         sg.Button("Data Limită", font=font_main, size=(15, 1), button_color=("white", "#5D3FD3"), border_width=0, pad=(5, 10)),
         sg.Button("Status", font=font_main, size=(15, 1), button_color=("white", "#5D3FD3"), border_width=0, pad=(5, 10))]
    ]

    # Creăm fereastra cu fundal personalizat
    window = sg.Window("Aplicație Gestiune Timp", layout, finalize=True, background_color=bg_color)
    return window

# Funcția principală
def main():
    filename = "sarcini.txt"
    tasks = read_tasks_from_file(filename)  # Citim sarcinile existente din fișier

    window = create_window()
    window["task_list"].update(tasks)  # Populăm lista inițială cu sarcinile citite

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Ieșire":
            break

        # Adăugarea unei sarcini noi
        if event == "Adaugă":
            task = values["task_input"].strip()
            if task:  # Adăugăm sarcina doar dacă nu este goală
                tasks.append(task)
                window["task_list"].update(tasks)
                write_tasks_to_file(filename, tasks)
                window["task_input"].update("")  # Golim input-ul

        # Ștergerea unei sarcini selectate
        if event == "Șterge":
            selected_task = values["task_list"]
            if selected_task:
                task_to_remove = selected_task[0]
                tasks.remove(task_to_remove)
                window["task_list"].update(tasks)
                write_tasks_to_file(filename, tasks)

        # Editarea unei sarcini
        if event == "Editare":
            selected_task = values["task_list"]
            if selected_task:
                task_to_edit = selected_task[0]
                # Obținem noua valoare de la utilizator
                new_task = sg.popup_get_text("Editează sarcina:", default_text=task_to_edit, background_color="#E0FFFF", text_color="#333333")
                if new_task:  # Actualizăm doar dacă noua valoare nu este goală
                    index = tasks.index(task_to_edit)
                    tasks[index] = new_task
                    window["task_list"].update(tasks)
                    write_tasks_to_file(filename, tasks)

        # Marchează sarcina ca finalizată
        if event == "Marchează ca finalizată":
            selected_task = values["task_list"]
            if selected_task:
                task_to_mark = selected_task[0]
                index = tasks.index(task_to_mark)
                tasks[index] = f"[Finalizat] {task_to_mark}"
                window["task_list"].update(tasks)
                write_tasks_to_file(filename, tasks)

        # Adăugarea unei date limită
        if event == "Data Limită":
            selected_task = values["task_list"]
            if selected_task:
                task_to_update = selected_task[0]
                deadline = sg.popup_get_date(title="Selectați Data Limită")
                if deadline:
                    formatted_deadline = datetime(deadline[2], deadline[0], deadline[1]).strftime("%d-%m-%Y")
                    index = tasks.index(task_to_update)
                    tasks[index] = f"{task_to_update} (Deadline: {formatted_deadline})"
                    window["task_list"].update(tasks)
                    write_tasks_to_file(filename, tasks)

        # Setarea statusului unei sarcini
        if event == "Status":
            selected_task = values["task_list"]
            if selected_task:
                task_to_update = selected_task[0]
                status = sg.popup_get_text("Introduceți Statusul sarcinii (e.g., În progres, Blocat):", background_color="#E0FFFF", text_color="#333333")
                if status:
                    index = tasks.index(task_to_update)
                    tasks[index] = f"{task_to_update} [Status: {status}]"
                    window["task_list"].update(tasks)
                    write_tasks_to_file(filename, tasks)

    window.close()

if __name__ == "__main__":
    main()
