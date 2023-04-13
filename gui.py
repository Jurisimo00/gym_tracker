import PySimpleGUI as sg 

def createStartWindow():
    sg.theme("LightGrey")

    # Define the window layout
    layout = [
        [sg.Text("Start WIndow", size=(60, 1), justification="center")],
        [sg.Text("Select the exercise to analise", key="-OUTPUT-")],
        [sg.Button("Squat", size=(10, 1)),
         sg.Button("Deadlift", size=(10, 1)),
         sg.Button("Neck", size=(10, 1))]
    ]

    # Create the window and show it without the plot
    window = sg.Window("OpenCV Integration", layout, location=(800, 400))
    return window

def createWIndow():
    sg.theme("LightGrey")

    # Define the window layout
    layout = [
        [sg.Image(filename="", key="-IMAGE-"),
            sg.Image(filename="", key="-SKELETON-")],
        [sg.Text("Output", key="-OUTPUT-")],
        [sg.Text("Reps"), sg.Text("",key="-REPS-")],
        [sg.Text("Left knee angle", justification="right"), sg.Text("",key="-LEFT_KNEE-", justification="right")],
        [sg.Text("Right knee angle", justification="right"), sg.Text("",key="-RIGHT_KNEE-", justification="right")],
        [sg.Text("Left elbow angle", justification="right"), sg.Text("",key="-LEFT_ELBOW-", justification="right")],
        [sg.Text("Right elbow angle", justification="right"), sg.Text("",key="-RIGHT_ELBOW-", justification="right")],
        [sg.Button("Exit", size=(10, 1))],
        
    ]

    # Create the window and show it without the plot
    window = sg.Window("OpenCV Integration", layout, location=(800, 400))
    return window
