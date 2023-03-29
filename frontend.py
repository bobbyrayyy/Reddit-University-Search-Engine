import PySimpleGUI as sg
import search_engine

sg.theme('Reddit')
font = ('Courier New', 11)

# Define the window layout
layout = [
    [sg.Text('Reddit University Search Engine', font=('Helvetica', 20))],
    [sg.Text('Enter your query:')],
    [sg.InputText(key='-QUERY-', size=(200, 1))],
    [sg.Button('Search')],
    [sg.Text(font=('Helvetica', 12), visible=False, key='-RECOMMENDATION-'), sg.Button('Search with recommendation', visible=False, key='-RECOMMENDATION-BUTTON-')],
    [sg.Text(font=('Helvetica', 14), visible=False, key='-RESULTS-TITLE-')],
    [sg.Multiline(size=(200, 80), key='-RESULTS-')]
]

# Create the window
window = sg.Window('Reddit University Search Engine', layout, finalize=True, size=(1000, 800),resizable=True)

# Event loop
while True:
    event, values = window.read()

    # Close the window if the user clicks the X button or presses Esc
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    # If the user clicks the Search button, send a request to the search engine backend
    if event == 'Search':
        query = values['-QUERY-']
        results, recommendation = search_engine.search(query)

        content = ''
        content += '1'+'-'*250 + '\n'
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
