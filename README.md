# GameMaker Sprite Importer

This Python application facilitates batch importing of PNG's and GIF's into the GameMaker engine as sprites, supporting sprite sheet creation from GIFs, custom origin points, sprite sizes, and naming conventions.

## Features
- **Batch Import:** Import multiple GIFs/PNGs into GameMaker.
- **Sprite Sheets:** Convert GIFs to sprite sheets automatically.
- **Customization:** Set sprite origins, sizes, and naming conventions.
- **GameMaker Integration:** Update .yyp project files automatically.

## Requirements
- Python 3.6+
- Required Python packages are listed in `requirements.txt`.

## Installation
1. Clone the repository using "git clone https://github.com/Emperor2000/gm-sprite-importer.git".
2. Open the project folder: "cd gm-sprite-importer"
3. Run "pip install -r requirements.txt. It is recommended to use a virtual environment to do this: "python -m venv venv", powershell activate: "./venv/Scripts/Activate.ps1" or cmd "venv\Scripts\activate"
4. Run the app using "python importer.py".

## Usage
- **Select Source Directory:** Choose the directory containing GIFs and PNGs you want to import.
- **Select GameMaker Project Folder:** Select the folder containing your GameMaker project (.yyp file).
- **Configure Import Options:** Set naming conventions, sprite origins, and sizes as required.
- **Import Process:** The app will process each file, convert GIFs to sprite sheets if applicable, and update the GameMaker project files automatically.

## Notes
- Ensure your GameMaker project is backed up before running the importer.
- For GIF files, sprite sheets will be generated automatically during import.
- Modify `settings.py` to adjust default settings and behaviors.
