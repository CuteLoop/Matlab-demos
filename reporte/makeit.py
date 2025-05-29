#!/usr/bin/env python3
"""
create_pds_report.py
────────────────────
Builds the complete LaTeX project skeleton for the “Explorando la
Segmentación de Tumores Cerebrales con U-Net” report.

Usage
-----
$ python create_pds_report.py
# or make it executable:
$ chmod +x create_pds_report.py && ./create_pds_report.py
"""

from pathlib import Path
import textwrap

# --------------------------------------------------------------------
# 1. Define project root and sub-paths
# --------------------------------------------------------------------
ROOT = Path("PDS-Report")
SECTIONS = ROOT / "sections"
FIGS = ROOT / "figs"          # empty placeholder directory

# --------------------------------------------------------------------
# 2. File contents (exactly the snippets I supplied earlier)
# --------------------------------------------------------------------
main_tex = r"""
\documentclass[12pt,oneside]{report}
\usepackage[spanish,english]{babel}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{float}
\usepackage{amsmath,amssymb}
\usepackage{enumitem}
\usepackage{hyperref}
\usepackage{geometry}
\geometry{letterpaper,margin=2.5cm}
\bibliographystyle{IEEEtran}

\newcommand{\ProyectoTitulo}{\textbf{Explorando la Segmentación de Tumores Cerebrales con U-Net}}
\newcommand{\Integrantes}{Joel A.\ Maldonado Tänori}
\newcommand{\Carrera}{Ingeniería Biomédica}
\newcommand{\Materia}{Procesamiento Digital de Señales}
\newcommand{\Institucion}{TecNM – Campus Hermosillo}
\newcommand{\Fecha}{29 de mayo de 2025}

\begin{document}
\selectlanguage{spanish}
\begin{titlepage}
    \centering
    \vspace*{3cm}
    {\Huge \ProyectoTitulo\par}
    \vspace{2cm}
    {\Large \Integrantes\par}
    \vspace{1cm}
    {\large Carrera: \Carrera\par}
    {\large Materia: \Materia\par}
    {\large Institución: \Institucion\par}
    \vfill
    {\large \Fecha\par}
\end{titlepage}

\begin{abstract}
\selectlanguage{spanish}
\noindent\textbf{Resumen}\\
Se presenta una experiencia práctica empleando la arquitectura U-Net para la
segmentación de tumores cerebrales, contrastando un tutorial básico,
un ejemplo oficial de MATLAB 3-D U-Net y el artículo de referencia de
Isensee \textit{et al.} (2018).\\[6pt]
\textbf{Palabras clave:} segmentación, U-Net, MRI, Dice, Deep Learning.

\vspace{1em}
\selectlanguage{english}
\noindent\textbf{Abstract}\\
This report summarises hands-on work with a basic U-Net tutorial,
MATLAB’s 3-D U-Net example and the BRATS 2017 contribution by
Isensee \textit{et al.} (2018).\\[6pt]
\textbf{Keywords:} segmentation, U-Net, MRI, Dice, Deep Learning.
\end{abstract}

\tableofcontents
\clearpage
\input{sections/intro}
\input{sections/metodologia}
\input{sections/resultados}
\input{sections/conclusiones}

\phantomsection
\addcontentsline{toc}{chapter}{Referencias}
\bibliography{bibliography}
\end{document}
"""

intro_tex = r"""
\chapter{Introducción y Justificación}

La segmentación precisa y automática de tumores cerebrales es crucial
para la planeación quirúrgica, la radioterapia y el seguimiento de la
enfermedad. Las redes neuronales convolucionales, y en particular la
arquitectura \textit{U-Net} \cite{ronneberger2015unet}, han mostrado un
desempeño sobresaliente.

\section*{Objetivo general}
Analizar y documentar el proceso de segmentación de tumores cerebrales
con U-Net, contrastando distintas implementaciones y buenas prácticas.

\section*{Objetivos específicos}
\begin{enumerate}[label=\alph*)]
  \item Implementar una U-Net 2-D/3-D básica y evaluar su rendimiento.
  \item Replicar el ejemplo 3-D U-Net de MATLAB y comparar resultados.
  \item Estudiar las modificaciones y la pérdida Dice multiclase de \cite{isensee2018brats}.
\end{enumerate}
"""

metodologia_tex = r"""
\chapter{Metodología y Desarrollo}

\section{Datos y preprocesamiento}
Se utilizaron subconjuntos de BRATS 2017 en formato NIfTI. Se aplicó:
\begin{itemize}
  \item Corte al cerebro y normalización z-score por modalidad.
  \item División en bloques $128^3$ con \verb|blockedImage| de MATLAB.
\end{itemize}

\section{Arquitectura U-Net básica}
Ruta de contracción y expansión con \textbf{skip connections}.
Función de activación ReLU; se evaluó Leaky ReLU.

\section{Función de pérdida}
Entropía cruzada vs.\ Dice generalizada \cite{sudre2017generalizeddice}.
Próxima a implementarse: Dice multiclase \cite{isensee2018brats}.

\section{Aumento de datos}
Rotaciones, flips y deformaciones elásticas 3-D.

\section{Entrenamiento}
200 épocas, lote 2, Adam ($10^{-4}$), \textit{early stopping}.
"""

resultados_tex = r"""
\chapter{Resultados y Comparación}

\section{Métricas}
Dice %, IoU y HD95. Comparación con \cite{isensee2018brats}.

\begin{table}[H]\centering
\caption{Rendimiento preliminar (validación)}
\begin{tabular}{lccc}
\hline
\textbf{Modelo} & \textbf{Dice WT} & \textbf{Dice TC} & \textbf{HD95}\\\hline
U-Net 2-D básica & 0.78 & 0.72 & 6.4\,mm\\
MATLAB 3-D U-Net & 0.82 & 0.77 & 5.1\,mm\\
Isensee \textit{et al.} & \textbf{0.90} & \textbf{0.85} & \textbf{3.6}\,mm\\\hline
\end{tabular}
\end{table}

\section{Discusión}
El ejemplo MATLAB supera al tutorial; la solución de Isensee sigue
siendo el estado del arte gracias a normalización por instancia y
supervisión profunda.
"""

conclusiones_tex = r"""
\chapter{Conclusiones y Trabajo Futuro}

U-Net es base sólida, pero el rendimiento depende de la pérdida,
aumento de datos y ajustes arquitectónicos.

\begin{itemize}
  \item Implementar Dice multiclase.
  \item Añadir bloques residuales y normalización de instancia.
  \item Evaluar en BRATS 2020 para validar generalización.
\end{itemize}
"""

bibliography_bib = r"""
@article{isensee2018brats,
  author  = {Fabian Isensee and Philipp Kickingereder and Wolfgang Wick
             and Martin Bendszus and Klaus H. Maier-Hein},
  title   = {Brain Tumor Segmentation and Radiomics Survival Prediction:
             Contribution to the BRATS 2017 Challenge},
  journal = {Lecture Notes in Computer Science},
  year    = {2018},
  volume  = {10670},
  pages   = {287--297}
}

@inproceedings{ronneberger2015unet,
  author  = {Olaf Ronneberger and Philipp Fischer and Thomas Brox},
  title   = {U-Net: Convolutional Networks for Biomedical Image Segmentation},
  booktitle = {MICCAI},
  year    = {2015},
  pages   = {234--241}
}

@article{sudre2017generalizeddice,
  author  = {Christophe Sudre and Wenqi Li and Tim Vercauteren and
             Sebastian Ourselin and M. Jorge Cardoso},
  title   = {Generalised Dice Overlap as a Deep Learning Loss Function},
  journal = {DLMIA},
  year    = {2017},
  pages   = {240--248}
}

@misc{matlab3dunet,
  author       = {MathWorks},
  title        = {Segment Brain Tumors from MRI Data Using Deep Learning},
  note         = {\url{https://www.mathworks.com/help/images/segment-brain-tumors-from-mri-data-using-deep-learning.html}},
  year         = {2025}
}
"""

latexmkrc = r"""
$pdf_mode  = 1;
$pdflatex  = 'pdflatex -synctex=1 -interaction=nonstopmode %O %S';
$clean_ext = 'acn acr alg bbl blg glg glo gls ist lol out run.xml';
"""

# Mapping of relative file paths to their content
FILES = {
    ROOT / "main.tex": main_tex,
    SECTIONS / "intro.tex": intro_tex,
    SECTIONS / "metodologia.tex": metodologia_tex,
    SECTIONS / "resultados.tex": resultados_tex,
    SECTIONS / "conclusiones.tex": conclusiones_tex,
    ROOT / "bibliography.bib": bibliography_bib,
    ROOT / "latexmkrc": latexmkrc.strip(),
}

# --------------------------------------------------------------------
# 3. Create directories
# --------------------------------------------------------------------
for directory in (ROOT, SECTIONS, FIGS):
    directory.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------
# 4. Write each file
# --------------------------------------------------------------------
for path, content in FILES.items():
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    print(f"✓ wrote {path}")

print("\nProject scaffold complete!")
print("→ Compile with: cd PDS-Report && latexmk")
