import threading
import socket
import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

root = Tk()
root.title("Shareit")
root.geometry("540x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

filename = None  # Initialize filename globally

# Function to load images with PIL
def load_image(path, width, height):
    img = Image.open(path)
    img = img.resize((width, height), Image.Resampling.LANCZOS)  # Replace ANTIALIAS with LANCZOS
    return ImageTk.PhotoImage(img)

def select_file():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                           title='Select Image File',
                                           filetype=(('JPEG Files', '*.jpg'), ('All Files', '*.*')))
    # Display the file selected
    if filename:
        messagebox.showinfo("Selected File", f"File Selected: {filename}")

def sender():
    if filename:
        s = socket.socket()
        host = socket.gethostname()
        port = 8080
        s.bind((host, port))
        s.listen(1)
        print(f"Listening on {host}:{port} for incoming connections...")
        conn, addr = s.accept()
        
        def send_file():
            with open(filename, 'rb') as file:
                file_data = file.read(1024)
                while file_data:
                    conn.send(file_data)
                    file_data = file.read(1024)
            print("Data has been transmitted successfully.")
            conn.close()

        # Run file sending in a separate thread
        threading.Thread(target=send_file, daemon=True).start()
        
    else:
        messagebox.showerror("Error", "No file selected")

def Send():
    window = Toplevel(root)
    window.title("Send")
    window.geometry('450x560+500+200')
    window.config(bg="#f4fdfe")
    window.resizable(False, False)

    image_icon1 = load_image("Image/send.jpg", 32, 32)
    window.iconphoto(False, image_icon1)

    Sbackground = load_image("Image/sender.jpg", 450, 560)
    Label(window, image=Sbackground).place(x=-2, y=0)
    window.Sbackground = Sbackground  # Avoid garbage collection

    Button(window, text="+select file", width=10, height=1, font='arial 14 bold', bg="#fff", fg="#000", command=select_file).place(x=160, y=150)
    Button(window, text="SEND", width=8, height=1, font='arial 14 bold', bg='#000', fg="#fff", command=sender).place(x=300, y=150)

    window.mainloop()

def receiver():
    # Access the values entered in SenderID and incoming_file
    ID = SenderID.get()  # Use the Entry widget to get the Sender ID
    filename1 = incoming_file.get()  # Use the Entry widget to get the filename

    if not ID or not filename1:
        messagebox.showerror("Error", "Sender ID and Filename cannot be empty")
        return

    try:
        # Create a socket connection
        s = socket.socket()
        port = 8080
        s.connect((ID, port))  # Connect to the sender using the ID (hostname) and port
        
        def receive_file():
            with open(filename1, 'wb') as file:
                print("Receiving file...")
                while True:
                    file_data = s.recv(1024)
                    if not file_data:
                        break  # If no more data is received, exit the loop
                    file.write(file_data)  # Write received data to the file
                print("File has been received successfully.")
            
            s.close()

        # Run file receiving in a separate thread
        threading.Thread(target=receive_file, daemon=True).start()

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def Receive():
    main = Toplevel(root)
    main.title("Receive")
    main.geometry('450x560+500+200')
    main.configure(bg="#f4fdfe")
    main.resizable(False, False)

    image_icon1 = load_image("Image/receive.jpg", 32, 32)
    main.iconphoto(False, image_icon1)

    Hbackground = load_image("Image/receiver.jpg", 450, 560)
    Label(main, image=Hbackground).place(x=-2, y=0)
    main.Hbackground = Hbackground  # Avoid garbage collection

    Label(main, text="Receiver", font=('arial', 20), bg="#f4fdfe").place(x=100, y=280)

    # Sender ID field
    Label(main, text="Input sender ID", font=('arial', 10, 'bold'), bg="#f4fdfe").place(x=20, y=340)
    SenderID = Entry(main, width=25, fg="black", border=2, bg='white', font=('arial', 15))
    SenderID.place(x=20, y=370)
    SenderID.focus()

    # Incoming file name field
    Label(main, text="Filename for the incoming file: ", font=('arial', 10, 'bold'), bg="#f4fdfe").place(x=20, y=410)
    incoming_file = Entry(main, width=25, fg="black", border=2, bg='white', font=('arial', 15))
    incoming_file.place(x=20, y=450)

    # Receive button
    imageicon = load_image("Image/arrow.jpg", 20, 20)
    rr = Button(main, text="Receive", compound=LEFT, image=imageicon, width=130, bg="#39c790", font="arial 14 bold", command=receiver)
    rr.place(x=20, y=500)

    main.mainloop()


# Main window setup
background = load_image(r"C:\APP\FileTransferApp\Image\icon.jpg", 540, 560)  # Raw string literal for paths
Label(root, image=background).place(x=-2, y=0)

image_icon = load_image(r"C:\\APP\\FileTransferApp\\Image\\icon.jpg",32,32)  # Raw string literal for paths
root.iconphoto(False, image_icon)

Label(root, text="File Transfer", font=('Acumin Variable Concept', 20, 'bold'), bg="#f4fdfe").place(x=20, y=30)
Frame(root, width=400, height=2, bg="#f3f5f6").place(x=25, y=80)

send_image = load_image("Image/send.jpg", 100, 100)
send = Button(root, image=send_image, bg="#f4fdfe", bd=0, command=Send)
send.place(x=50, y=100)

receive_image = load_image("Image/receive.jpg", 100, 100)
receive = Button(root, image=receive_image, bg="#f4fdfe", bd=0, command=Receive)
receive.place(x=300, y=100)

Label(root, text="Send", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=65, y=200)
Label(root, text="Receive", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=300, y=200)


root.mainloop()
