# Documentation for Data availability plots at THAAO

# TODO:
- escludere dai plot valori mediati se sono basati da meno di x misure nel periodo considerato (medi mail di Daniela)

This Python script leverages the Tkinter library for creating graphical user interface (GUI) elements to allow users to
customize and generate plots related to instruments, field campaigns, and historical events. It also uses pandas for
handling time-related data and integrates with various plotting functions imported from an external module `plots`.

## Table of Contents

- [Function Documentation](#function-documentation)
    - [create_root](#create_root)
    - [update_instr_list](#update_instr_list)
    - [get_switch_input](#get_switch_input)
    - [set_date_params](#set_date_params)
    - [main](#main)
- [Main Execution Flow](#main-execution-flow)
- [External Dependencies](#external-dependencies)

## Function Documentation

### `create_root()`

This function creates a hidden Tkinter root window. The Tkinter root window is necessary to initialize the Tkinter event
loop, but it is immediately hidden as it is not needed for display.

**Returns:**

- A `Tk` root window instance (`root`).

### `update_instr_list()`

This function updates the list of instruments (`ts.instr_list`) based on the instrument categories selected in the
input. It checks the selected categories and adds the corresponding instruments from the predefined `ts.instr_sets`
dictionary.

**Parameters:**

- None (relies on `sw.switch_instr_list`).

### `get_switch_input(prompt, default=False)`

This function shows a simple yes/no input dialog to the user with a given prompt. The user’s choice is returned as a
boolean (`True` or `False`).

**Parameters:**

- `prompt`: A string message to be displayed in the dialog box.
- `default`: The default boolean value returned if the user cancels or doesn't provide an answer. Defaults to `False`.

**Returns:**

- `True` if the user selects "Yes", `False` if the user selects "No" or cancels.

### `set_date_params(start_prompt, end_prompt, date_type)`

This function prompts the user for start and end year values for a given date range. Based on the type of date range (
`rolling` or `cumulative`), it updates the corresponding `sw` global variables to reflect the start and end
dates.

**Parameters:**

- `start_prompt`: The prompt text for asking the user for the start year.
- `end_prompt`: The prompt text for asking the user for the end year.
- `date_type`: A string indicating the type of date range (`rolling` or `cumulative`).

**Returns:**

- None (updates global variables in `sw`).

### `main()`

This is the main execution function of the script, which initializes the Tkinter root window, displays dialog boxes for
user inputs, updates instrument lists, and sets parameters for plotting panels. The function will then call the plotting
functions based on the user's selections.

**Parameters:**

- None

**Returns:**

- None

**Execution Flow:**

1. Prompts the user to select instrument categories.
2. Prompts the user for inputs related to plotting options (rolling and cumulative panels).
3. Prompts for field campaigns and historical events display.
4. Displays the selected instruments.
5. Generates the plots based on the user's selections.

---

## Main Execution Flow

1. **Create Root Window:**  
   The Tkinter root window is created by calling the `create_root` function, and it remains hidden as it is only
   required for handling GUI dialogs.

2. **Instrument Selection:**  
   The user is prompted to input a category of instruments they would like to plot. This could include:
    - `thaao`
    - `legacy`
    - `hyso`  
      If the user chooses a category, the `update_instr_list` function updates the instrument list (`ts.instr_list`)
      accordingly.

3. **Panel Type Selection:**  
   The user is asked if they would like to plot rolling and cumulative panels:
    - **Rolling Panels**: If selected, the user provides window size (in months) and lag (in months), which are used to
      set the `sw.time_window_r` and `sw.time_freq_r` values, respectively.
    - **Cumulative Panels**: If selected, the user provides a lag (in months) and a date range for cumulative panels.

4. **Campaigns and Historical Events:**  
   The user is asked whether they want to include field campaigns and historical events in the plot. These selections
   are stored as boolean values in the `sw.switch_campaigns` and `sw.switch_history` variables.

5. **Display Selected Instruments:**  
   After all inputs are gathered, a message box is displayed to inform the user of the selected instruments.

6. **Generate Plots:**  
   Based on the selected options, the corresponding plotting functions are called to generate and save the plots:
    - `plot_panels('rolling')`
    - `plot_panels('cumulative')`

7. **Completion:**  
   The script finishes executing by printing "END" in the terminal.

---

## External Dependencies

The script relies on the following external libraries:

- **tkinter**: For creating GUI elements such as message boxes and input dialogs.
- **pandas**: For date handling and offset operations (i.e., `pd.DateOffset`).
- **plots**: A custom module that is expected to contain plotting-related functions (e.g., `plot_panels()`).

Additionally, the script references global variables from `sw` (settings or switches) and `ts` (instrument metadata and
lists).

---

## Notes

- The Tkinter window created by `create_root()` is kept hidden (`root.withdraw()`) since only pop-up windows are used
  for input.
- The use of message boxes (`messagebox.showinfo`) provides interactive feedback to the user.
- The `plot_panels()` function (imported from `plots`) is invoked based on user selections to generate the plots.
