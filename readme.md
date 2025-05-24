# Sublemon Text Editor

## About

This is a minimalistic text editor for Pythonista. It was originally part of the [Pythonista implementation](https://github.com/nbeversl/urtext_pythonista) of [Urtext](https://urtext.co/). It was separated out for modularity and is now maintained mostly as a dependency of Urtext.

## Features

- Multi-purpose dropdown with autocomplete, similar to the one in [Sublime Text](https://www.sublimetext.com/)
- Array of customizable keyboard buttons
- Syntax highlighting. Uses Objective-C bindings to provide highlighting for grammars expressible as nested regex. None are bundled as this editor was built mainly for a single project. See https://github.com/nbeversl/urtext_pythonista/blob/master/urtext_syntax.py. 
- Extensible theming

## Usage

`BaseEditor.show()`
(see https://github.com/nbeversl/sublemon/blob/master/editor.py).
