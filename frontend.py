import PySimpleGUI as sg
import json
import search_engine

sg.theme('Reddit')
font = ('Courier New', 11)

headings = ['Body', 'Post Title', 'Subreddit', 'URL']
data = []   # Empty data
col_widths = list(map(lambda x:len(x)+2, headings)) # find the widths of columns in character.
max_col_width = len('ParameterNameToLongToFitIntoAColumn')+2  # Set max midth of all columns of data to show

# Define the window layout
layout = [
    [sg.Text('Search Engine', font=('Helvetica', 20))],
    [sg.Text('Enter your query:')],
    [sg.InputText(size=(200, 1))],
    [sg.Button('Search')],
    [sg.Text('Results:', font=('Helvetica', 14))],
    # [sg.Listbox(values=[], size=(60, 15), font=('Helvetica', 12), key='results')],
    [sg.Table(
        values=data,                # Empty data must be with auto_size_columns=False
        headings=headings,
        auto_size_columns=False,    # For empty data
        vertical_scroll_only=False, # Required if column widths changed and width of table not changed
        hide_vertical_scroll=True,  # Not required if no more rows of data
        def_col_width=20,
        num_rows=10,
        col_widths=col_widths,      # Define each column width as len(string)+2
        font=font,                  # Use monospaced font for correct width
        key='-TABLE-')]
]

# Create the window
window = sg.Window('Reddit University Search Engine', layout, finalize=True, size=(1000, 800))

char_width = sg.Text.char_width_in_pixels(font)     # Get character width in pixel
table = window['-TABLE-']
table_widget = table.Widget
table.expand(expand_x=True, expand_y=True)          # Expand table in both directions of 'x' and 'y'
for cid in headings:
    table_widget.column(cid, stretch=True)          # Set column stretchable when window resize

# Event loop
while True:
    event, values = window.read()
    # print(event, values)

    # Close the window if the user clicks the X button or presses Esc
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    # If the user clicks the Search button, send a request to the search engine backend
    if event == 'Search':
        query = values[0]
        results = search_engine.search(query)

        table_data = []
        for row in results:
            table_data.append([row['Comment_Body'], row['Post_Title'], row['Subreddit'], row['URL']])
        # window['-TABLE-'].update(values=table_data, visible=True)
        # window['table'].set_size((200, 50))

        all_data = [headings] + table_data    
        # Find width in pixel and 2 extra characters for each column
        col_widths = [min([max(map(len, columns))+2, max_col_width])*char_width for columns in zip(*all_data)]
        table.update(values=table_data)                   # update all new data
        # Redraw table to update new size of table if horizontal scrollbar not used, care if widget too large to fit your window or screen.
        table_widget.pack_forget()
        for cid, width in zip(headings, col_widths):    # Set width for each column
            table_widget.column(cid, width=width)
        # table_widget.column('Subreddit', width=5)
        table_widget.pack(side='left', fill='both', expand=True)    # Redraw table



# Close the window
window.close()
