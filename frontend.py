import PySimpleGUI as sg
import search_engine

sg.theme('Reddit')
font = ('Courier New', 11)

# headings = ['Content', 'Subreddit', 'URL']
# data = []   # Empty data
# col_widths = list(map(lambda x:len(x)+2, headings)) # find the widths of columns in character.
# max_col_width = 100  # Set max midth of all columns of data to show

# Define the window layout
layout = [
    [sg.Text('Reddit University Search Engine', font=('Helvetica', 20))],
    [sg.Text('Enter your query:')],
    [sg.InputText(key='-QUERY-', size=(200, 1))],
    [sg.Button('Search')],
    [sg.Text(font=('Helvetica', 12), visible=False, key='-RECOMMENDATION-'), sg.Button('Search with recommendation', visible=False, key='-RECOMMENDATION-BUTTON-')],
    [sg.Text(font=('Helvetica', 14), visible=False, key='-RESULTS-TITLE-')],
    # [sg.Text('Results:', font=('Helvetica', 14))],
    # [sg.Listbox(values=[], size=(60, 15), font=('Helvetica', 12), key='results')],
    # [sg.Table(
    #     values=data,                # Empty data must be with auto_size_columns=False
    #     headings=headings,
    #     auto_size_columns=True,    # For empty data
    #     vertical_scroll_only=False, # Required if column widths changed and width of table not changed
    #     hide_vertical_scroll=True,  # Not required if no more rows of data
    #     def_col_width=20,
    #     num_rows=10,
    #     # col_widths=col_widths,      # Define each column width as len(string)+2
    #     font=font,                  # Use monospaced font for correct width
    #     key='-TABLE-')],
        [sg.Multiline(size=(200, 80), key='-RESULTS-')]
]

# Create the window
window = sg.Window('Reddit University Search Engine', layout, finalize=True, size=(1000, 800),resizable=True)

# char_width = sg.Text.char_width_in_pixels(font)     # Get character width in pixel
# table = window['-TABLE-']
# table_widget = table.Widget
# table.expand(expand_x=True, expand_y=True)          # Expand table in both directions of 'x' and 'y'
# for cid in headings:
#     table_widget.column(cid, stretch=True)          # Set column stretchable when window resize
# table_widget.column('Content', width=100)
# table_widget.column('Subreddit', width=5)
# table_widget.column('URL', width=50)

# Event loop
while True:
    event, values = window.read()
    # print(event, values)

    # Close the window if the user clicks the X button or presses Esc
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    # If the user clicks the Search button, send a request to the search engine backend
    if event == 'Search':
        query = values['-QUERY-']
        results, recommendation = search_engine.search(query)

        content = ''
        content += '1'+'-'*250 + '\n'
        # table_data = []
        num = 2
        for row in results:
            title = row['Post_Title'][0]
            body = row['Comment_Body'][0]

            
            content += 'Title:\n' + title + '\nContent:\n\n'
            for i in range(0, len(body), 190):
                content += body[i:i+190] + '\n'
            

            content += '\nSubreddit:\n' + row['Subreddit'][0] + '\n\n'
            content += 'Bow_Clus_Label:\n' + str(row['Bow_Clus_Label'][0]) + '\n\n'
            content += 'URL:\n' + row['URL'][0] + '\n'
            content += str(num)+'-'*250 + '\n'
            num+=1

            # table_data.append([content, row['Subreddit'], row['URL']])

        # all_data = [headings] + table_data    
        # # Find width in pixel and 2 extra characters for each column
        # # col_widths = [min([max(map(len, columns))+2, max_col_width])*char_width for columns in zip(*all_data)]
        # table.update(values=table_data)                   # update all new data
        # # Redraw table to update new size of table if horizontal scrollbar not used, care if widget too large to fit your window or screen.
        # table_widget.pack_forget()
        # # for cid, width in zip(headings, col_widths):    # Set width for each column
        # #     table_widget.column(cid, width=width)
        # table_widget.column('Content', width=100)
        # table_widget.column('Subreddit', width=5)
        # table_widget.column('URL', width=50)
        # # table_widget.column('Subreddit', width=5)
        # table_widget.pack(side='left', fill='both', expand=True)    # Redraw table
        window['-RESULTS-'].update(content)
        window['-RESULTS-TITLE-'].update('Showing results for: ' + query, visible=True)
        if query != recommendation:
            window['-RECOMMENDATION-'].update('Search instead for: ' + recommendation, visible=True)
            window['-RECOMMENDATION-BUTTON-'].update(visible=True)

    if event == '-RECOMMENDATION-BUTTON-':
        window['-QUERY-'].update(recommendation)
        window.write_event_value('Search', None)


# Close the window
window.close()
