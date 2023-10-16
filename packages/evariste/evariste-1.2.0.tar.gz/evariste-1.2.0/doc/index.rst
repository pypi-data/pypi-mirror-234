Welcome to `Évariste`'s documentation!
======================================

Given a git repository (or any directory), Évariste has two purposes:

- compile every file (*à la* make, with a different configuration);
- generate an HTML page presenting every file (both compiled file and source file), as an annotated directory tree.

For instance, Évariste turns `a git repository of hundreds of LaTeX files <https://framagit.org/lpaternault/cours-2-math>`__ into `an HTML page with annotated source and compiled files <https://lpaternault.frama.io/cours-2-math/>`__.

.. admonition:: Layout of this documentation

   - Installation is explained in :ref:`the next section <install>`.
   - The basic concepts of Évariste are explained in :ref:`quickstart`.
   - A more thorough user documentation is available in :ref:`user`.
   - Évariste is extensible. Learn about existing plugins, as well as how to write your own plugins, in :ref:`plugin`.
   - Évariste comes with a few helpers tools, which are described in :ref:`evs`.
   - Developers might want to have a glance at :ref:`lib`.

   Enjoy!

.. toctree::
   :maxdepth: 2

   usecase
   install
   user
   plugins
   evs
   lib


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

*Je ne sais pas le reste*
-------------------------

.. epigraph::

  C'est que malheureusement on ne se doute pas que le livre le plus précieux
  du plus savant serait celui où il dirait tout ce qu'il ne sait pas, c'est
  qu'on ne se doute pas qu'un auteur ne nuit jamais tant à ses lecteurs que
  quand il dissimule une difficulté. Quand la concurrence, c'est-à-dire
  l'égoïsme, ne règnera plus dans la science, quand on s'associera  pour
  étudier, au lieu d'envoyer aux Académies des paquets cachetés, on
  s'empressera de publier ses moindres observations pour peu qu'elles soient
  nouvelles et on ajoutera : « Je ne sais pas le reste. »

  -- Évariste Galois, Préface aux « Deux mémoires d'Analyse pure », décembre 1831
