Use case
========

TL;DR
-----

Évariste turns `a git repository of hundreds of LaTeX files <https://framagit.org/lpaternault/cours-2-math>`__ into `an HTML page with annotated source and compiled files <https://lpaternault.frama.io/cours-2-math/>`__.

More details, please?
---------------------

`Louis <https://framagit.org/lpaternault>`__ is a math teacher. He has every course material in several git repositories (one per course). Let's take a look at `this repository <https://framagit.org/lpaternault/cours-2-math>`__.

This repository contain tens or hundreds of LaTeX files (most of them being compiled with a single pass of LuaLaTeX, some of them require several passes, a few are compiled using LaTeX+dvipdf), a few LibreOffice documents, and probably a few other files.

Louis has two copies of this repository: one on his computer at home, and one on `his USB key <https://ababsurdo.fr/blog/20150615-clef-usb/>`__ thas is carried at work, and that he uses to print documents on the work printer, and to display them using a beamer during his lessons. Louis uses git to synchronize those copies.

Purpose #1
""""""""""

At home, Louis has (almost) finished working on some material for his students. He commits the LaTeX files in his git repository, pushes them to some server, and, on his USB key (the one he carries at work):

- he pulls the changes (so that this key contains the latest version of the LaTeX *source* files);
- he runs Évariste (so that the new or recently modified LaTeX source files are compiled to PDF files that he can print or show to his students).

Purpose #2
""""""""""

Louis would be happy if other teachers reused his course material, so he publishes his repository on a `public git repository <https://framagit.org/lpaternault/cours-2-math>`__. But this repository only contains source files (and some of Louis's colleagues have never heard about LaTeX), and navigating those files is not friendly. So, when Louis pushes his changes to this public repository, using continuous integration:

- Évariste compiles every single LateX file (at least, those which have changed);
- Évariste generates a `HTML page <https://lpaternault.frama.io/cours-2-math>`__ which displays every single file of this repository, together with its compiled (PDF) version, and, optionnaly, some annotation.

