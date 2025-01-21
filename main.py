import tkinter as tk
import random

#define the templates
arpeggios = [
    "C Major", "C Minor", "C# Major", "C# Minor",
    "D Major", "D Minor", "Eb Major", "Eb Minor",
    "E Major", "E Minor", "F Major", "F Minor",
    "F# Major", "F# Minor", "G Major", "G Minor",
    "Ab Major", "Ab Minor", "A Major", "A Minor",
    "Bb Major", "Bb Minor", "B Major", "B Minor"
]

scales = [
    f"{tone} {scale_type}"
    for tone in ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    for scale_type in ["Major", "Minor", "Harmonic", "Melodic"]
]

bar_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]

inversions = ["root", "1st", "2nd"]

# create a dictionary to map template names to their respective lists
templates = {
    "Arpeggios": arpeggios,
    "Scales": scales,
    "Bar Numbers": bar_numbers,
    "Inversions": inversions
}

# store the original state of the templates
original_templates = {key: value[:] for key, value in templates.items()}

#open main window
root = tk.Tk()
root.geometry("300x400")
root.title("Randomizzer")

#add label to choose template
label = tk.Label(root, text="Choose a template:")
label.pack(pady=10)

#add frame to hold dropdown menu and edit button
frame = tk.Frame(root)
frame.pack(pady=10)

# define the clicked variable
clicked = tk.StringVar()
clicked.set("Arpeggios")

# add dropdown menu
drop = tk.OptionMenu(frame, clicked, *templates.keys())
drop.pack(side="left", padx=5)

# function to update the dropdown menu
def update_dropdown():
    menu = drop["menu"]
    menu.delete(0, "end")
    for key in templates.keys():
        menu.add_command(label=key, command=tk._setit(clicked, key))

# define the edit_templates function
def edit_templates():
    edit_window = tk.Toplevel(root)
    edit_window.geometry("300x400")
    edit_window.title("Edit Template")

    # add text box
    text = tk.Text(edit_window, height=10, width=30)
    text.pack(pady=10)

    # populate the text box with the current template items
    sorted_items = sorted(templates[clicked.get()], key=lambda x: (x.isdigit(), int(x) if x.isdigit() else x))
    text.delete("1.0", "end")
    text.insert("1.0", "\n".join(sorted_items))

    # add button to save the templates
    def save_templates():
        if clicked.get() == "Bar Numbers":
            num_bars = bar_entry.get()
            if num_bars.isdigit():
                templates["Bar Numbers"] = [str(i) for i in range(1, int(num_bars) + 1)]
        else:
            text_content = text.get("1.0", "end-1c").split("\n")
            templates[clicked.get()][:] = [item for item in text_content if item]
        
        # Shuffle the list after saving changes
        random.shuffle(templates[clicked.get()])
        
        edit_window.destroy()

    save_button = tk.Button(edit_window, text="Save", command=save_templates)
    save_button.pack(pady=10)

    # add dropdown menu and delete button for deleting specific types
    if clicked.get() in ["Arpeggios", "Scales"]:
        delete_frame = tk.Frame(edit_window)
        delete_frame.pack(pady=10)

        delete_type = tk.StringVar()
        delete_type.set("Major")

        if clicked.get() == "Arpeggios":
            delete_options = ["Major", "Minor"]
        elif clicked.get() == "Scales":
            delete_options = ["Major", "Minor", "Harmonic", "Melodic"]

        delete_menu = tk.OptionMenu(delete_frame, delete_type, *delete_options)
        delete_menu.pack(side="left", padx=5)

        def delete_selected():
            current_template = templates[clicked.get()]
            updated_template = [item for item in current_template if not item.endswith(delete_type.get())]
            templates[clicked.get()][:] = updated_template
            sorted_items = sorted(updated_template, key=lambda x: (x.isdigit(), int(x) if x.isdigit() else x))
            text.delete("1.0", "end")
            text.insert("1.0", "\n".join(sorted_items))

        delete_button = tk.Button(delete_frame, text="Delete", command=delete_selected)
        delete_button.pack(side="left", padx=5)

    # add entry for number of bars if "Bar Numbers" is selected
    if clicked.get() == "Bar Numbers":
        bar_label = tk.Label(edit_window, text="Enter the number of bars:")
        bar_label.pack(pady=10)
        bar_entry = tk.Entry(edit_window)
        bar_entry.pack(pady=10)

        def update_bars(event):
            num_bars = bar_entry.get()
            if num_bars.isdigit():
                updated_bars = [str(i) for i in range(1, int(num_bars) + 1)]
                templates["Bar Numbers"] = updated_bars
                sorted_items = sorted(updated_bars, key=lambda x: (x.isdigit(), int(x) if x.isdigit() else x))
                text.delete("1.0", "end")
                text.insert("1.0", "\n".join(sorted_items))

        bar_entry.bind("<Return>", update_bars)

    # add button to delete the custom list if editing a custom list
    if clicked.get() not in ["Arpeggios", "Scales", "Bar Numbers", "Inversions"]:
        def delete_list():
            del templates[clicked.get()]
            update_dropdown()
            edit_window.destroy()

        delete_list_button = tk.Button(edit_window, text="Delete List", command=delete_list)
        delete_list_button.pack(pady=10)

    # add reset button to restore the content of the current template to original list components
    def reset():
        templates[clicked.get()] = original_templates[clicked.get()][:]
        sorted_items = sorted(templates[clicked.get()], key=lambda x: (x.isdigit(), int(x) if x.isdigit() else x))
        text.delete("1.0", "end")
        text.insert("1.0", "\n".join(sorted_items))

    reset_button = tk.Button(edit_window, text="Reset", command=reset)
    reset_button.pack(pady=10)

    # set protocol handler for window close event to discard changes
    def on_close():
        # restore the original state of the templates
        for key in templates:
            templates[key][:] = original_templates[key]
        edit_window.destroy()

    edit_window.protocol("WM_DELETE_WINDOW", on_close)

# add edit button to frame
edit_button = tk.Button(frame, text="Edit", command=edit_templates)
edit_button.pack(side="left", padx=5)

# define the create_custom_list function
def create_custom_list():
    custom_window = tk.Toplevel(root)
    custom_window.geometry("300x400")
    custom_window.title("Create Custom List")

    # add text box
    custom_text = tk.Text(custom_window, height=10, width=30)
    custom_text.pack(pady=10)

    # add button to save the custom list
    def save_custom_list():
        custom_list_name = custom_entry.get()
        custom_list_content = custom_text.get("1.0", "end-1c").split("\n")
        templates[custom_list_name] = [item for item in custom_list_content if item]
        original_templates[custom_list_name] = templates[custom_list_name][:]
        update_dropdown()  # Update the dropdown menu with the new list
        custom_window.destroy()

    custom_entry = tk.Entry(custom_window)
    custom_entry.pack(pady=10)
    custom_entry.insert(0, "Enter list name")

    save_custom_button = tk.Button(custom_window, text="Save", command=save_custom_list)
    save_custom_button.pack(pady=10)

# add button to create custom list
create_custom_button = tk.Button(root, text="Create Custom List", command=create_custom_list)
create_custom_button.pack(side="bottom", pady=10)

# add function to generate the random template with no repeats
previous_results = []

def generate():
    global previous_results
    choices = []
    if clicked.get() == "Arpeggios":
        choices = [item for item in arpeggios if item != previous_results[-1]] if previous_results else arpeggios
    elif clicked.get() == "Scales":
        choices = [item for item in scales if item != previous_results[-1]] if previous_results else scales
    elif clicked.get() == "Bar Numbers":
        choices = [item for item in templates["Bar Numbers"] if item != previous_results[-1]] if previous_results else templates["Bar Numbers"]
    elif clicked.get() == "Inversions":
        choices = [item for item in templates["Inversions"] if item != previous_results[-1]] if previous_results else templates["Inversions"]
    else:
        choices = [item for item in templates[clicked.get()] if item != previous_results[-1]] if previous_results else templates[clicked.get()]
    
    if not choices:
        choices = templates[clicked.get()]

    result = random.choice(choices)
    previous_results.append(result)
    if len(previous_results) > 7:
        previous_results.pop(0)
    result_label_no_repeats.config(text=result)
    result_label_no_repeats.pack(pady=10)

# add button
button = tk.Button(root, text="Generate", command=generate)
button.pack(pady=10)

# add result label
result_label_no_repeats = tk.Label(root, text="")

# create a key bind to generate the random template with no repeats
root.bind("<Return>", lambda event: generate())

# run the main window
root.mainloop()
