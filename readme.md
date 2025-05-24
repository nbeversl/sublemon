# Sublemon Text Editor

## About

This is a minimalistic text editor for [Pythonista](https://omz-software.com/pythonista/). Sublemon was originally part of the [Pythonista implementation](https://github.com/nbeversl/urtext_pythonista) of [Urtext](https://urtext.co/). It was created when the Urtext project outgrew the scope of [Editorial](https://omz-software.com/editorial/) and something fully scriptable was needed.

Sublemon is coyly named after [Sublime](https://www.sublimetext.com/). It replicates Sublime's multi-purpose fuzzy search dropdown. It provides a loose replication of Sublime's Python scriptability on iOS.

## Features

- Multi-purpose dropdown with autocomplete, similar to the one in [Sublime Text](https://www.sublimetext.com/)
- Syntax highlighting. Uses Objective-C bindings to provide highlighting for grammars expressible as nested regex. None are bundled as this editor was built mainly for a single project. See https://github.com/nbeversl/urtext_pythonista/blob/master/urtext_syntax.py. 
- Extensible theming
- Array of customizable keyboard buttons

## Usage

`BaseEditor.show()`
(see https://github.com/nbeversl/sublemon/blob/master/editor.py).

## Development

Sublemon was separated out for modularity and currently exists mostly as an Urtext dependency. PRs are welcome however. In particular:

- Native TextView updates used for syntax highlighting are not optimized
- Needs a status bar
- Multiple tabs
- Other syntaxes



