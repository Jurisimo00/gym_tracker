import PySimpleGUI as sg 

def createStartWindow():
    sg.theme("LightGrey")

    # Define the window layout
    layout = [
        [sg.Text("Start Window", size=(60, 1), justification="center")],
        [sg.Text("Select the exercise to analise", key="-OUTPUT-")],
        [sg.Button("Squat", size=(10, 1)),
         sg.Button("Deadlift", size=(10, 1)),
         sg.Button("Neck", size=(10, 1))]
    ]

    # Create the window and show it without the plot
    window = sg.Window("Stats", layout, location=(800, 400))
    return window

def messageWindow():
    sg.theme("LightGrey")

    # Define the window layout
    layout = [
        [sg.Text("Select body part to track", key="-OUTPUT-")]
    ]
    # Create the window and show it without the plot
    window = sg.Window("Start", layout, location=(800, 400))
    return window

def createWIndow():
    sg.theme("LightGrey")

    # Define the window layout
    layout = [
        [sg.Image(filename="", key="-IMAGE-"),
            sg.Image(filename="", key="-SKELETON-")],
        [sg.Text("Reps"), sg.Text("",key="-REPS-")],
        [sg.Text("Left knee angle", justification="right"), sg.Text("",key="-LEFT_KNEE-", justification="right")],
        [sg.Text("Right knee angle", justification="right"), sg.Text("",key="-RIGHT_KNEE-", justification="right")],
        [sg.Text("Left elbow angle", justification="right"), sg.Text("",key="-LEFT_ELBOW-", justification="right")],
        [sg.Text("Right elbow angle", justification="right"), sg.Text("",key="-RIGHT_ELBOW-", justification="right")],
        [sg.Button("Exit", size=(10, 1))],
        
    ]

    # Create the window and show it without the plot
    window = sg.Window("", layout, location=(800, 400))
    return window

def createSelectionInputWindow():
    sg.theme("LightGrey")

    # Define the window layout
    layout = [
        [sg.Text("Select video or webcam", size=(60, 1), justification="center")],
        [sg.Text("Select which input video you want to use")],
        [sg.Button("Webcam", size=(10, 1)), sg.Checkbox('Record video', default=False, key="-RECORD-")],
        [sg.Text("Upload video from file system"),
          sg.Input(),
        sg.FileBrowse(key="-IN-")],
         [sg.Button("Submit", size=(10,1))]
    ] 
    # Create the window and show it without the plot
    window = sg.Window("Selection", layout, location=(800, 400))
    return window   
