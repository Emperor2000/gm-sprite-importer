<img width="128" alt="icon" src="https://github.com/Emperor2000/gm-sprite-importer/assets/38536470/9dbeca97-51ff-420b-8490-0f1bcc49bc20">

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

<img width="457" alt="GM Sprite Importer Console 1" src="https://github.com/Emperor2000/gm-sprite-importer/assets/38536470/ad540f9d-1baf-426a-aa31-41a16e716bdc">

<img width="457" alt="GM Sprite Importer Console 2" src="https://github.com/Emperor2000/gm-sprite-importer/assets/38536470/a57e93cd-abb0-4a41-a641-628b701403d9">

<img width="457" alt="GM Sprite Importer Console Options Origin" src="https://github.com/Emperor2000/gm-sprite-importer/assets/38536470/58d9bc79-6387-4de0-b0fb-1fc9a7a669b2">

<img width="457" alt="GM Sprite Importer Console Options" src="https://github.com/Emperor2000/gm-sprite-importer/assets/38536470/791f9afe-6746-41c6-8703-cf7a811c0413">

<img width="186" alt="auto_import_sprite_results" src="https://github.com/Emperor2000/gm-sprite-importer/assets/38536470/ef7f1160-4c6e-402e-881f-150323e9f90d">
