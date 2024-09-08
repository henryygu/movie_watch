import tkinter as tk
from tkinter import filedialog, messagebox
from simplejustwatchapi.justwatch import search
import pandas as pd

# Global variables to store the selected file path and DataFrame
file_path = None
df_titles = None

# Function to convert offers to a DataFrame
def offers_to_dataframe(media_entries):
    rows = []
    for entry in media_entries:
        title = entry.title  # Access title attribute
        for offer in entry.offers:  # Access offers attribute
            row = {
                'Title': title,
                'Platform': offer.package.name,
                'URL': offer.url,
                'Monetization Type': offer.monetization_type,
                'Presentation Type': offer.presentation_type,
            }
            rows.append(row)
    return pd.DataFrame(rows)

# Function to process the Excel file
def process_file():
    global df_titles
    if not file_path or df_titles is None:
        messagebox.showerror("Error", "No file selected or file is not loaded properly.")
        return

    # Get the selected column
    column_name = column_var.get()
    if column_name not in df_titles.columns:
        messagebox.showerror("Error", "Selected column not found in the Excel file")
        return

    # Initialize an empty DataFrame to store all results
    all_results = pd.DataFrame()

    # Iterate over each title in the selected column and perform the search
    for title in df_titles[column_name]:
        results = search(title, "GB", "en", 5, True)
        df = offers_to_dataframe(results)
        all_results = pd.concat([all_results, df], ignore_index=True)

    # Save the combined results to a new Excel file
    save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx")])
    if save_path:
        all_results.to_excel(save_path, index=False)
        messagebox.showinfo("Success", f"Results saved to {save_path}")

# Function to select the file and load columns
def select_file():
    global file_path, df_titles
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        df_titles = pd.read_excel(file_path)
        column_var.set("Select Column")
        column_dropdown['menu'].delete(0, 'end')
        for col in df_titles.columns:
            column_dropdown['menu'].add_command(label=col, command=tk._setit(column_var, col))

# Set up the GUI
root = tk.Tk()
root.title("JustWatch Offer Search")

# Instructions Label
tk.Label(root, text="Select the Excel file and the column to search for titles:").pack(pady=10)

# Button to select the Excel file
file_button = tk.Button(root, text="Select Excel File", command=select_file)
file_button.pack(pady=5)

# Dropdown to select the column
column_var = tk.StringVar(root)
column_var.set("Select Column")
column_dropdown = tk.OptionMenu(root, column_var, "Select Column")
column_dropdown.pack(pady=5)

# Button to process the file
process_button = tk.Button(root, text="Process File", command=process_file)
process_button.pack(pady=20)

# Run the GUI
root.mainloop()
