Below there are description of each folder and each file:
1. venv, pycache, chroma -> are used to work with the RAG model, you should not touch them. (chromadb, virtual environment)
2. pictures -> this folder contains the pictures of 3D model, instances diagram, instances, and material properties. Thses photos then used in the GUI
3. diagram.png -> this png file is created due the execution of the "diagram.py" file. It is used in the GUI.
4. diagram.py -> the py file that creates the cost diagram. It is executed when running the GUI file and when pressing the "Load 3D model" button in the GUI. Inputs should be manually written in the "gui_rag.py" file
5. instances_diagram.py -> the py file that creates the instances diagram. 
6. model.ipynb -> the notebook file that was intially used to create and test the rag model, and also to add the additional articles.
7. model.py -> the py file of the rag model that is used in the GUI.
8. scraping.ipynb -> the notebook file that is used to count the number of instances.
9. T_build_value_txt -> the txt file that contains the T_build value that is obtained from the "diagram.py" file.
10. gui_rag.py -> the py file that creates the GUI. It uses "model.py", "diagram.py"

### You need to use python virtual environment and work from it. Using environments allow to avoid any conflict in library dependencies.
