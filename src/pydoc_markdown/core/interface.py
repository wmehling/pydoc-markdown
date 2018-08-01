# -*- coding: utf8 -*-
# The MIT License (MIT)
#
# Copyright (c) 2018 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

"""
This module provides the interfaces that are used to load, process and render
code documentation. The interfaces make no assumption about the programming
language or markup used in the documentation, however the docstrings often
refer to Python and Markdown as that is the main use case.
"""

__all__ = [
  'IConfigurable',
  'ILoader',
  'IPreprocessor',
  'ITextPreprocessor',
  'IRenderer'
]

import nr.interface

from pydoc_markdown.core.document import Text


class IConfigurable(nr.interface.Interface):
  """
  Base class for the interfaces in this module. Every one of these interfaces
  that is used by Pydoc Markdown will have a `config` attribute so it has
  access to the current site configuration.
  """

  config = nr.interface.attr(dict)


class ILoader(IConfigurable):
  """
  The #Loader interface is responsible for loading documents from a
  module spec. A module spec is any identifier followed by zero or more
  `+` characters, indicating the additional child levels of the module to
  take into account.
  """

  def load_document(self, modspec, doc):
    """
    Load the documentation content of a Python module from the
    specified *modspec* into the document *doc*.

    modspec (str): The identifier of the module to load.
    doc (Document): The document to add the contents to.
    """

    raise NotImplementedError


class IPreprocessor(IConfigurable):
  """
  The #Preprocessor interface is responsible for preprocessing the plain-text
  contents and modify the document structure.
  """

  def preprocess(self, root):
    """
    Process the nodes in the #DocumentRoot node *root* and modify it.
    """

    raise NotImplementedError


class ITextPreprocessor(IPreprocessor):
  """
  This interface allows you to implement the #preprocess_text() method
  that allows you to substitute a #Text node with one or many other nodes.
  """

  @nr.interface.default
  def preprocess(self, root):
    def recursion(node):
      if isinstance(node, Text):
        self.preprocess_text(node)
      for child in list(node.children):
        recursion(child)
    recursion(root)
    root.collapse_text()

  def preprocess_text(self, text_node):
    pass


class IRenderer(IConfigurable):
  """
  The renderer is ultimately responsible for rendering the Markdown documents
  to a file.
  """

  def render(self, directory, root):
    """
    Render documents to the directory.

    # Parameters
    directory (str): Path to the output directory.
    root (DocumentRoot): The collection of documents to render.
    """

  def render_document(self, fp, document):
    """
    Called to render a single document to a file. This is used in the
    Pydoc-Markdown plain mode.
    """

  def load_renderer_document(self, root, name, document):
    """
    Called to load a special document that can only be loaded by the renderer.
    Such document names are prefixed with two dollar signs. Renderers commonly
    support the `$$index` document which contains an index of all symbols
    in the document.
    """
