# Visual Mathematics – Python Practical Assignments

> Python practicals for visual mathematics, created as part of the engineering curriculum (Monde Virtuel / Virtual Worlds specialization).

---

## Table of contents
- [Overview](#overview)  
- [Repository structure](#repository-structure)  
- [Technologies & Requirements](#technologies--requirements)  
- [Installation](#installation)  
- [How to run (examples)](#how-to-run-examples)  
- [Expected outputs](#expected-outputs)  
- [Project goals & learning outcomes](#project-goals--learning-outcomes)  
- [Contributing](#contributing)  
- [License](#license)  
- [Author](#author)  

---

## Overview
This repository contains a set of Python practical assignments (TPs) that use programmatic visualizations to explore mathematical topics. The work was completed as part of my engineering studies in the **Monde Virtuel (Virtual Worlds)** specialization. Each practical includes a PDF with the problem description and a Python script implementing visual experiments and demonstrations.

---

## Repository structure

```
.
├── TP1_Groupe_Diedral_et_Transformations.pdf  
├── TP1_Groupe_Diedral_et_Transformations.py  
├── TP2_Fractales_et_Transformations_Geometriques.pdf  
├── TP2_Fractales_et_Transformations_Geometriques.py  
├── TP3_Quaternions_et_Rotations_Espace.pdf  
├── TP3_Quaternions_et_Rotations_Espace.py  
├── requirements.txt  
└── README.md
```

---

## Technologies & Requirements
This project assumes Python 3.8+ and uses common scientific / plotting libraries:

- Python 3.8 or newer  
- NumPy  
- Matplotlib  
- (Optional) Jupyter Notebook or JupyterLab for interactive exploration

A `requirements.txt` file is recommended. Example content:

```
numpy
matplotlib
```

---

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/victorpiana/tps-python-maths-visuelles.git
   cd tps-python-maths-visuelles
   ```
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate      # Windows (PowerShell)
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## How to run (examples)

### Run TP1 — Dihedral Group & Transformations
```bash
python TP1_Groupe_Diedral_et_Transformations.py
```
Expected behavior: script draws 2D figures and shows the effect of dihedral group actions (rotations/reflections) on the shapes.

### Run TP2 — Fractals & Geometric Transformations
```bash
python TP2_Fractales_et_Transformations_Geometriques.py
```
Expected behavior: generates fractal images or iterative function system visualizations.

### Run TP3 — Quaternions & Spatial Rotations
```bash
python TP3_Quaternions_et_Rotations_Espace.py
```
Expected behavior: demonstration of 3D rotations implemented with quaternions; may output 2D projections or animated sequences.

---

## Expected outputs
Each TP aims to produce one or more of:
- Static PNG/SVG visualizations saved to disk.  
- Interactive Matplotlib windows illustrating transforms.  
- Plots that demonstrate mathematical properties (symmetry, convergence, orientation-preserving rotations, etc.).

---

## Project goals & learning outcomes
- Understand symmetry groups and dihedral group actions (TP1).  
- Implement and visualize fractals and iterative geometric procedures (TP2).  
- Learn quaternion algebra and apply it to 3D rotations and orientation control (TP3).  
- Translate mathematical definitions into clear, testable Python code while producing explanatory visuals.

---

## Contributing
Contributions are welcome. Suggested ways to contribute:
- Fix bugs or tidy code structure.  
- Add new visual experiments or TPs (include a PDF description and the Python implementation).  
- Improve scripts to accept command-line parameters or to export results to `outputs/`.  
- Add unit tests where appropriate.

When contributing, please:
1. Fork the repository  
2. Create a feature branch (`git checkout -b feat/my-visual`)  
3. Commit changes and open a pull request

---

## License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## Author
**Victor Piana**  
Engineering student — *Monde Virtuel (Virtual Worlds)* specialization
