import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import subprocess
import os
from model import generate_response, vector_stores
import time

class RAGModelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RAG Model GUI") 

        self.root.state('zoomed')

        self.upper_frame = tk.Frame(root, bg="#282c34")
        self.upper_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.lower_frame = tk.Frame(root)
        self.lower_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.create_upper_frame()

        self.create_lower_frame()

    def create_upper_frame(self):
        
        self.description_label = tk.Label(self.upper_frame, text="This GUI provides build time, cost estimation with three materials, material properties, the frequency of usage of each material in specific industries, and access to a RAG model to enhance the decision-making process", bg="#282c34", fg="white", font=("Times New Roman", 13), wraplength=self.root.winfo_screenwidth()-20)
        self.description_label.grid(row=0, column=0, columnspan=6, padx=10, pady=5, sticky='ew')

        for i in range(6):
            self.upper_frame.grid_columnconfigure(i, weight=1)

        # Titles above the labels
        self.instances_title = tk.Label(self.upper_frame, text="Number of Instances", bg="#282c34", fg="white", font=("Bookman Old Style", 11))
        self.instances_title.grid(row=1, column=0, padx=10, pady=0)

        # title for the 3D model
        self.model_title = tk.Label(self.upper_frame, text="3D Model", bg="#282c34", fg="white", font=("Bookman Old Style", 11))
        self.model_title.grid(row=1, column=2, padx=10, pady=0)

        # Labels for the photos
        self.photo_left_label = tk.Label(self.upper_frame, text="Instances Photo", bg="#282c34", fg="white")
        self.photo_left_label.grid(row=2, column=0, padx=4, pady=5)

        self.photo_center_label = tk.Label(self.upper_frame, text="3D Model Photo", bg="#282c34", fg="white")
        self.photo_center_label.grid(row=2, column=2, padx=4, pady=5)

        self.diagram_label = tk.Label(self.upper_frame, text="Diagram Photo", bg="#282c34", fg="white")
        self.diagram_label.grid(row=2, column=4, padx=4, pady=5)

        # Buttons to load photos
        self.load_photo_left_button = tk.Button(self.upper_frame, text="Load Instances", command=self.load_photo_left)
        self.load_photo_left_button.grid(row=3, column=0, padx=10, pady=5)

        self.load_photo_center_button = tk.Button(self.upper_frame, text="Load 3D Model", command=self.load_photo_center)
        self.load_photo_center_button.grid(row=3, column=2, padx=10, pady=5)

        self.load_diagram_button = tk.Button(self.upper_frame, text="Load Diagram", command=self.load_diagram)
        self.load_diagram_button.grid(row=3, column=4, padx=10, pady=5)

    def create_lower_frame(self):
        
        self.left_frame = tk.Frame(self.lower_frame, bg="#282c34")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.right_frame = tk.Frame(self.lower_frame, bg="#282c34")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_left_frame()
        self.create_right_frame()

    def create_left_frame(self):
        # Title for Material Properties
        self.material_title_label = tk.Label(self.left_frame, text="Material Properties", bg="#282c34", fg="white", font=("Bookman Old Style", 12))
        self.material_title_label.pack(anchor=tk.N, padx=10, pady=0)

        # Replace text box with a label for displaying the photo
        self.material_photo_label = tk.Label(self.left_frame, text="No Photo of materials", bg="#282c34", fg="white")
        self.material_photo_label.pack(expand=True, padx=5, pady=0)

        # Button to load the material photo
        self.load_material_photo_button = tk.Button(self.left_frame, text="Load Material Photo", command=self.load_material_photo)
        self.load_material_photo_button.pack(anchor=tk.CENTER, padx=10, pady=3)
        
        # Label for T_build
        self.build_time_value = tk.Label(self.left_frame, text="", bg="#282c34", fg="white", font=("Bookman Old Style", 12))
        self.build_time_value.pack(anchor=tk.NW, padx=10, pady=4)

    def create_right_frame(self):

        # ChatBot label
        self.chatbot_label = tk.Label(self.right_frame, text="Chat Bot", bg="#282c34", fg="white", font=("Bookman Old Style", 12))
        self.chatbot_label.pack(anchor=tk.NW, padx=10, pady=0)

        # Chat bot text
        self.chatbot_text = tk.Text(self.right_frame, height=20)
        self.chatbot_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Chat entry
        self.chat_entry = tk.Entry(self.right_frame)
        self.chat_entry.pack(fill=tk.X, padx=10, pady=2)

        # Button for users to send the quetion
        self.chat_send_button = tk.Button(self.right_frame, text="Send", command=self.send_chat)
        self.chat_send_button.pack(anchor=tk.CENTER, padx=10, pady=5)

    def load_photo_left(self):
        file_path = filedialog.askopenfilename() 
        if file_path:
            image = Image.open(file_path) 
            image = image.resize((500, 280), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(image)
            self.photo_left_label.config(image=photo)
            self.photo_left_label.image = photo

    def load_photo_center(self):
        file_path = filedialog.askopenfilename() 
        if file_path:
            image = Image.open(file_path)
            image = image.resize((400, 280), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(image)
            self.photo_center_label.config(image=photo)
            self.photo_center_label.image = photo

    def load_material_photo(self):
        file_path = filedialog.askopenfilename() 
        if file_path:
            image = Image.open(file_path) 
            image = image.resize((500, 255), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(image)
            self.material_photo_label.config(image=photo)
            self.material_photo_label.image = photo

    def load_diagram(self):
        # Run the diagram.py script to generate the diagram
        subprocess.run(['python', 'diagram.py'], check=True)

        if os.path.exists('diagram.jpeg'):
            image = Image.open('diagram.jpeg') 
            image = image.resize((600, 280), Image.LANCZOS) 
            photo = ImageTk.PhotoImage(image)
            self.diagram_label.config(image=photo)
            self.diagram_label.image = photo

            try:
                with open('T_build_value.txt', 'r') as f: 
                    T_build = f.read().strip()
                    
                    try:
                        T_build = float(T_build)
                    except ValueError:
                        T_build = "Invalid value"

                    self.build_time_value.config(text=f"The build time based on the input variables is: {T_build} hours")

            except Exception as e:
               
                print(f"Error fetching T_build: {e}")
                self.build_time_value.config(text="Error fetching build time")

    def send_chat(self):

        user_input = self.chat_entry.get()

        # insert to the window
        self.chatbot_text.insert(tk.END, f"You: {user_input}\n", "user")
        self.chat_entry.delete(0, tk.END)

        # Measure the time taken to generate response
        start_time = time.time() 

        # Generate response from bot
        try:
            response = generate_response(user_input, vector_stores)
            
            end_time = time.time()

            elapsed_time = end_time - start_time

            print(f"Start time: {start_time}. Finish time: {end_time}. Time taken to generate response: {elapsed_time}")

            # Printing the response from the bot to the window
            self.chatbot_text.insert(tk.END, f"Bot: {response}\n", "bot")

        except Exception as e:
            self.chatbot_text.insert(tk.END, f"Error: {str(e)}\n")

        # Configure the text tags for different fonts
        self.chatbot_text.tag_config("user", font=("Bookman Old Style", 10, "bold"))
        self.chatbot_text.tag_config("bot", font=("Arial", 10))

# Create the root window
root = tk.Tk()
app = RAGModelGUI(root)
root.mainloop()
