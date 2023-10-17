
ruamel.yaml.split
=================

.. image:: https://sourceforge.net/p/ruamel-yaml-split/code/ci/default/tree/_doc/_static/license.svg?format=raw
     :target: https://opensource.org/licenses/MIT
.. image:: https://sourceforge.net/p/ruamel-yaml-split/code/ci/default/tree/_doc/_static/pypi.svg?format=raw
     :target: https://pypi.org/project/ruamel.yaml.split
.. image:: https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw
     :target: https://pypi.org/project/oitnb/



This package provides a YAML document splitter, 
that allows you to iterate over a UTF-8 encoded file with YAML
documents, and that returns each  
document, start linenumber and optionally loaded data.

Using this has the advantage over using ``load_all()``, that you can skip individual documents
that you know don't load, or that you test/transform before proper loading. 
E.g. ``R`` markdown files have a YAML header followed by a non-YAML body
(of course it would have been much better if in ``R`` markdown,
the header had been followed by ``--- |`` instead of only a directory-end-marker (``---``),
that way you could use **any** compliant YAML parser to load both)

You can use the following to get to each document:

.. code:: python

    from pathlib import Path
    from ruamel.yaml.split import split

    for doc, line_nr in split(Path('input.yaml')): 
        print(doc.decode('utf-8'), line_nr)

The line_nr indicates the starting line of the document and can be used as an offset
for e.g. errors that are generated when parsing the document.

You can also provide a ``YAML()`` instance to get the document loaded for you:

.. code:: python

    import ruamel.yaml 

    for doc, data, line_nr in split(Path('input.yaml'), yaml=ruamel.yaml.YAML()): 
        print(doc.decode('utf-8'), data, line_nr)

the ``YAML()`` instance you provide is used to load all documents.

By default ``split()`` splits on the line-ending after the document-end-marker (``...``), so that any comment
on the line of the document-end-marker is part of the document before it. Using
some constants imported from ``ruamel.yaml.split`` that you provide to the  
the ``cmnt`` parameter of ``split()``, you can influence where the comments "between" documents
are split. ``C_PRE`` adds any such comments to the preceding document, ``C_POST`` to
the following document.
``C_SPLIT_ON_FIRST_BLANK``, splits after the first blank line and assigns to both.

.. code:: python

    from ruamel.yaml.split import C_SPLIT_ON_FIRST_BLANK 

    for doc, data, line_nr in split(Path('input.yaml'), cmnt=C_SPLIT_ON_FIRST_BLANK): 
        print(doc.decode('utf-8'), line_nr)

Comments at the end of the
document stream are all attached to the last document, independent of the ``cmnt`` parameter.
