<div align="center">

[![License](https://img.shields.io/github/license/MarcOrfilaCarreras/codebox-thefullstack-hackathon?style=for-the-badge)](https://github.com/MarcOrfilaCarreras/codebox-thefullstack-hackathon) &nbsp; ![The Full Stack Hackathon](https://img.shields.io/badge/-The_Full_Stack_Hackathon-000000?style=for-the-badge&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAMCAYAAABr5z2BAAAAAXNSR0IArs4c6QAAAXBJREFUKFN1kj1oVEEURs+8p6sLsbPSFQtxqxSCCGksBBGxELs0wUI7GwULGxHtbETShRQ2aheESES0EGyENCFNUhtTaZHCn12zvpljsTP4eOCBKeb77r1z78yQUtpQH6pDWqg9tcqr1/GG6iN1Hf/xU11T59U+HdTD2VtTf5Qk1D92SCntqIujkcfVgfpU/dKNUzeCKvCVlN4RwhVCONo6+B5wBLjf0vaAVWAF2Kmy2Iv6mhAuAXfVt1kPQA2gfgBuA5djjCvAdWAzqBEohbaA58BH4DSwDRyKMZ6o63o3pXS+qqoFYJZCnqXpzPZbfaPOqmfUVXXSifmlxlJgt2maBfVFNgoP1Cdlk0wj9Zl6U/2segBogJm6rgfAY2AJuMD0Ar/nRr8By4HwHtgHrgEzOn3GNnvqXB7tlHpsPB6fVAcAk8nknLrfTkC9o262tFv8B6etFz6pN9rmxZTSK/Vq3vfV4PQrHywx6kv1bMn7CxcVszQRA/C3AAAAAElFTkSuQmCC)

</div>

<div align="center">
    <h1>Codebox</h1>
    <h4>CLI for Saving and Sharing Code Snippets</h4>
</div>

## About The Project
Codebox is a command-line interface (CLI) program that allows you to easily save and share code snippets directly from your terminal. It provides a simple and efficient way to manage your code snippets with features like adding, listing, and deleting snippets.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Adding a Snippet](#adding-a-snippet)
  - [Listing Snippets](#listing-snippets)
  - [Deleting Snippets](#deleting-snippets)
  - [Sharing Snippets](#sharing-snippets)
- [License](#license)

## Installation

To use Codebox, you need to have Python installed on your system. You can install Codebox using pip:

```bash
pip install --editable .
```

## Usage
### Adding a Snippet
To add a code snippet, use the following command:

```bash
codebox add --name <snippet_name> --tags <tag1> <tag2> ...
```

### Listing Snippets
To list all saved snippets, use the following command:

```bash
codebox list
```

### Deleting Snippets
To delete one or more snippets, use the following command:

```bash
codebox delete <snippet_id> ...
```

### Sharing Snippets
To share one snippet, use the following command:

```bash
codebox share <snippet_id> ...
```

## License

Distributed under the MIT License. See `LICENSE` for more information.
