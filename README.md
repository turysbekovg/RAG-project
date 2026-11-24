Below there are description of each folder and each file:
1. venv, pycache, chroma -> are used to work with the RAG model, you should not touch them. (chromadb, virtual environment)
2. datasets -> this folder contains dataset of PDF articles from 3 fields: automotive, biomedical, aerospace. PDFs are divided by feilds and there are 25 more articles in the "addtional_new" folder. In case if you dont have the "datasets" folder in the main folder, move it in the main folder, because some py files use it to access the articles.
3. pictures -> this folder contains the pictures of 3D model, instances diagram, instances, and material properties. Thses photos then used in the GUI
4. diagram.png -> this png file is created due the execution of the "diagram.py" file. It is used in the GUI.
5. diagram.py -> the py file that creates the cost diagram. It is executed when running the GUI file and when pressing the "Load 3D model" button in the GUI. Inputs should be manually written in the "gui_rag.py" file
6. instances_diagram.py -> the py file that creates the instances diagram. 
7. model.ipynb -> the notebook file that was intially used to create and test the rag model, and also to add the additional articles.
8. model.py -> the py file of the rag model that is used in the GUI.
9. scraping.ipynb -> the notebook file that is used to count the number of instances.
10. T_build_value_txt -> the txt file that contains the T_build value that is obtained from the "diagram.py" file.
11. gui_rag.py -> the py file that creates the GUI. It uses "model.py", "diagram.py"

### You need to use python virtual environment and work from it, which is already been created. Using environments allow to avoid any conflict in library dependencies. In VsCode you can do this by following steps

1. In VsCode open the main folder.
2. VsCode will start to run automatically any code using this environment. 
