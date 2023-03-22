import PySimpleGUI as sg
import search_engine

sg.theme('Reddit')

# Define the window layout
layout = [
    [sg.Text('Search Engine', font=('Helvetica', 20))],
    [sg.Text('Enter your query:')],
    [sg.InputText()],
    [sg.Button('Search')],
    [sg.Text('Results:', font=('Helvetica', 14))],
    [sg.Listbox(values=[], size=(60, 15), font=('Helvetica', 12), key='results')]
]

# Create the window
window = sg.Window('Search Engine', layout, size=(800, 600))

# Event loop
while True:
    event, values = window.read()
    print(event, values)

    # Close the window if the user clicks the X button or presses Esc
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

    # If the user clicks the Search button, send a request to the search engine backend
    if event == 'Search':
        query = values[0]
        # TODO: Send a POST request to the search engine backend with the query and get the results
        # results = ['Result 1', 'Result 2', 'Result 3']
        results = search_engine.search(query)
        window['results'].update(values=results)

# Close the window
window.close()
