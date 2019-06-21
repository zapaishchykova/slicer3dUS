# Slicer3D - Fast registration
Module for fast US 3d spatial registration. Made during SS2019 in [Lab Course / Praktikum: Project Management and Software Development for Medical Applications](http://campar.in.tum.de/Chair/TeachingSs19PMSD).

### Prerequisites

* SlicerIGT
* Sequences
* Sequence Registration

### Installing

[Tutorial](https://www.slicer.org/w/images/0/0f/Slicer4_ProgrammingTutorial_SPujol-SPieper.pdf)
1. Select Module Settings from the Edit -> Application Settings Dialog 
2. Open the side panel and click "Add"
3. Add the path to the directory containing USRegistration.py
(when selecting the directory, the .py file itself will not be displayed) 
4. Restart Slicer when prompted. Fast registration module is now in the Modules Menu, under the category Examples 

### Usage
1. Change path for extend.bat 
2. Install the module
3. Run steps from Slicer 1-4
4. After Loading the volume3.mha fiducial registration wizard will be displayed. Place 4 fiducials.
5. Press on "Change final transform" and check the RMS error.
6. Extract the matrix

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

