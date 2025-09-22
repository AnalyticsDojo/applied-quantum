# Quantum Setup to Work Locally

Follow these steps to get your environment ready using **Anaconda**, **GitHub Desktop**, and **VS Code**.  
You will **clone the repository** and install packages using **the `requirements.txt` in the repo** (do **not** use any other requirements file).

---

## 0) Install the tools

1. **Anaconda (Python 3.11 recommended)**
   - Download from: https://www.anaconda.com/download
   - Install with default options.
   - On Windows, you will use the **Anaconda Prompt** for all commands.

2. **GitHub Desktop**
   - Download from: https://desktop.github.com

3. **VS Code**
   - Download from: https://code.visualstudio.com/download
   - Recommended extensions (Microsoft): **Python**, **Pylance**, **Jupyter**, **Jupyter Notebook**.
   - Optional: **GitHub Copilot** (students can apply via https://education.github.com/students)

---

## 1) Clone the repository

- Open **GitHub Desktop** → **File → Clone repository…**
- URL: `https://github.com/AnalyticsDojo/applied-quantum`
- Choose a local path you’ll remember (e.g., `Documents/applied-quantum`)
- Click **Clone**

> You will use the **`requirements.txt` in this repo** for installation. Do **not** create a new one.

---

## 2) Create and activate a conda environment

Open the **Anaconda Prompt** (Windows) or a terminal (macOS/Linux), then navigate into the cloned repo folder:

```bash
cd path/to/applied-quantum
```

Create and activate a new environment:

```bash
conda create --name quantum python=3.13
conda activate quantum
```

---

## 3) Install dependencies (from the repo’s `requirements.txt`)

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 4) Install the Jupyter kernel (required)

You must register the environment so Jupyter can use it:

```bash
python -m ipykernel install --user --name quantum --display-name "Python 3.13 (quantum)"
```

After this, when you open a notebook in Jupyter or VS Code, select the kernel named:

```
Python 3.13 (quantum)
```

---

## 5) Open in VS Code and select interpreter

1. Open **VS Code** → **File → Open Folder…** → select your `applied-quantum` folder.
2. Press **Ctrl+Shift+P** (Win/Linux) or **Cmd+Shift+P** (macOS) → **Python: Select Interpreter**.
3. Choose **Python 3.13 (quantum)**.
4. For notebooks, the **Jupyter kernel** selector should also show **Python 3.13 (quantum)**.

---

## 6) Run a quick check

Create a new file `check.ipynb` and ad a new code cell:
```python
import qiskit, numpy, pandas, matplotlib
print("Environment OK")
```

Run:
```bash
python check.py
```

You should see: `Environment OK`

---

## Common hiccups & fixes

- **Conda command not found (macOS/Linux):** close and reopen your terminal, or ensure Anaconda is added to your PATH.
- **Environment not showing in Jupyter/VS Code:** re-run  
  `python -m ipykernel install --user --name quantum --display-name "Python 3.13 (quantum)"`.
- **VS Code using the wrong Python:** re-run **Python: Select Interpreter** and choose **quantum**.
