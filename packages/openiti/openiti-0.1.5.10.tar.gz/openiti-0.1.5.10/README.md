# openiti

This is a first attempt to create a Python library that combines all often-used code in the OpenITI project. 
Full documentation and deescription can be found here: <https://openiti.readthedocs.io/>

# Installation

```{python}
pip install OpenITI
```

Alternatively, you might need to use `pip3 install OpenITI` or `python -m pip install OpenITI`.

## Change log: 


### v.0.1.5.10:
- `helper.ara`: 
    * Arabic-Indic digits and Extended Arabic-Indic digits are removed from the
      `ar_chars` liststring, and put into a new liststring: `ar_nums`. 
      This has the effect that numbers written written with these characters 
      are not considered Arabic tokens anymore
      (just like numbers written with Western Arabic numerals).
    * A large number of Greek, Coptic, Syriac and Latin characters are added to the
      `allowed_chars` stringlist, which means they should not be removed
      from texts before putting them into the corpus.
- `helper.funcs.text_cleaner`: this function, which removes all non-word-characters,
    numbers and Latin-script characters from the texts, now uses
    `helper.ara.transcription_chars` instead of `[A-z]` to define Latin-script letters.
    This means it will now also remove common transcription letters 
    (ā, ḥ, ...) instead of only ASCII letters.
- `helper.rgx`: 
    * add a list of Islamicate language codes
    * add regex for author (`author_uri`), book (`book_uri`) and version URIs
      (`version_uri`)
    * fix the page number related regexes to include PageBeg and PageEnd tags,
      and folio numbers that end with lower-case "a" or "b"
    * adapt the `section_tag` regex to include this new flavour: `### |5|` 
      (which is the same as a section tag with five pipes)
    * add an `all_tags` regex that can be used to remove all OpenITI mARkdown tags
    * add an `html_tags` regex that can be used to find html tags
- `helper.uri` :
    * `build_pth`: take into account the different repo name formats 
      for Arabic and other languages (Arabic: 0025AH, 0050AH, ...; 
      Persian: PER0025AH, PER0050AH, ...; Urdu: URD0025AH, ...)
    * `change_uri`: add a `non_25Y_folder` argument. Set this to True
      if you want to use the function for folders that do not have
      subfolders for each 25-year period.
    * `add_character_count`: idem
    * `move_yml`: idem
    * `make_folder`: idem
    * `move_to_new_uri_pth`: idem
    * `check_yml_files`: return list of paths to yml files where the checks failed
      instead of `None`
- `new_books.add.add_books`: implement `non_25Y_folder` argument in all functions 
  (see above in `helper.uri`)
- `new_books.convert.epub_converter_hindawi`: deal with possibility of 
  unavailable metadata
- `new_books.convert.helper.html2md`: improve named entity tagging
- `new_books.convert.helper.html2md_LAL`: various improvements for 
  formatting Library of Arabic Literature XML files
- `openiti.new_books.convert.tei_converter_LAL`: idem
- `new_books.convert.tei_converter_Wuerzburg`: small post-processing tweaks.

### v.0.1.5.9: 
* `helper.yml`: fix bug: pass `reflow` parameter in readYML function to ymlToDic
* `helper.funcs`: Add functions: 
  - `read_header`: read header of an OpenITI file (local path / URL)
  - `read_text`: read text of an OpenITI file (local path / URL)
  - `get_page_number`: get the page number of a token based on its offset
  - `get_semantic_tag_elements`: extract semantic tags (like @TOP, @PER) from an OpenITI text
  - `find_section_title`: get the section title of any location inside a text
  - `get_sections`: get a list of all sections in an OpenITI text
* `helper.ara`: 
  - Add a whitelist of characters that are allowed in OpenITI texts, with support for Hebrew and Cyrillic characters.
  - Add new characters (subscript alef, inverted damma, quranic sukun, small high madda) to the `noise` variable
* `new_books.convert.helper.html2md`: Add underscore to allowed characters in named entity tags and fix named entity count
* `new_books.convert.tei_converter_LAL`: add a new converter for TEI texts from the Library of Arabic Literature


### v.0.1.5.8: 
* `helper.uri`: when a book URI changes, also change references to it in related books.
* `helper.yml`: add functions to check completeness of yml files

### v.0.1.5.7: 
* `helper.uri`: fix bug in the extension looping process of the `check_token_count` function

### v.0.1.5.6:
* `helper.funcs`: add `natural_sort` function to sort a list of strings
  that include numbers in natural order (e.g., ["1", "2", "10"] instead of ["1", "10", "2"] )
* `helper.uri`: give files without extension priority over files with ".inProgress"
  extension in deciding which text file to use to count characters and tokens
  for a specific version yml file.
* `new_books.convert.epub_converter_masaha.py` : remove superfluous backslash in EDITOR tag
* `new_books.convert.helper.html2md.py`: fix bug in token count
* `openiti.new_books.convert.helper.html2md_eShia.py`: fix bug in footnote conversion
* `openiti.new_books.convert.html_converter_eShia.py`: improve eShia conversion
* Add converters for Ghbook, Ghaemiyeh and Rafed files.

### v.0.1.5.5:
* `helper.uri`: add support for flat folders.

### v.0.1.5.4: bug fix
* `helper.yml`: fix remaining bugs with long lines.
* `helper.uri`: fix bugs in `check_yml_file` function.

### v.0.1.5.3: bug fix
* `helper.yml`: make sure that yml keys always contain a hashtag.

### v.0.1.5.2: bug fix
* `helper.uri`: Remove test that blocked the script.

### v.0.1.5.1: bug fix
* `helper.yml`: fix bug related to long lines in the `dicToYML` function.

### v.0.1.5: 
* `helper.yml`: add `fix_broken_yml` function to fix yml files
that are unreadable due to indentation problems 
(or keys that don't end with a colon)
* `helper.uri`: rewrite the `check_yml_files` function to fix
a bug in the character count and add additional checks.
* `helper.funcs`: allow more than one `yml_type` in the function
`get_all_yml_files_in_folder`.
* `helper.ara`: 
  - Add missing EXTENDED ARABIC-INDIC DIGITS characters 67890
  - Add tokenize function
  - Fix typos in `normalize_per` doctest
* `new_books.convert`: add converter for Masāḥa Ḥurra epub files
(`epub_converter_masaha.py`, with helper file `html2md_masaha.py`)
* `new_books.convert.epub_converter_generic.py`: implement overwrite 
option for (dis)allowing overwriting existing converted files.

### v.0.1.4:
* `helper.templates`: replace the multiple book relations fields in the 
book yml file with a single field, `#40#BOOK#RELATED##:`.
* `helper.yml`: make not rearranging lines ("reflowing") in yml files the default,
and change the default line length to 80.
* `helper.funcs`: add a `get_all_yml_files_in_folder`, analogous to the existing
`get_all_text_files_in_folder` function

### v.0.1.3:

* `new_books.convert`: add converters for ALCorpus and Ptolemaeus texts
* `new_books.convert.helper.html2md`: tweaks to import of options + small tweaks
* `helper.ara`: Stop ar_cnt_file from raising exception if book misses splitter; instead, print warning
* `helper.funcs`: 
  - fix bug in `get_all_text_files_in_folder` function: missing periods in regex.
  - improve missing splitter message
  - use `ara.normalize_ara_light` function instead of `ara.normalize_ara_extra_light` in `text_cleaner` function
* `helper.uri`: 
  - make it possible to pass a specific `version_fp` to the `check_token_count` function; before, that function generated that path from the URI, but this created problems when files were not stored in the standard OpenITI folders. 
  - add `find_latest` parameter in `check_token_count` function; if ``False`, the function will count the tokens in the specific `version_fp` provided; if `True, the script will count tokens in the file with the most advanced extension (.mARkdown > .completed > .inProgress > [no extension])
* `helper.yml`: 
  - make it possible to pass a specific `yml_fp` to the `ymlToDic` function, so that the script can print the path (if provided) for signalling empty yml files.
  - Include possibility that yml key ends with more than one colon
  - `readYML`: add exception message when yml file could not be read.


### v.0.1.2:

* `openiti.helper.funcs`: Fixed bug in report_missing_numbers function.
* `openiti.new_books.convert`: added ShamAY converter and small updates to
    other shamela converters.

### v.0.1.1:

* `openiti.helper.funcs`: Added get_all_text_files_in_folder() generator
* `openiti.helper.uri`: Fix bug in `new_yml` function (URI used to have ".yml" in it)
* `openiti.new_books.convert.shamela_converter.py`: Improved formatting of the text and notes and added support for shamela collections in which the .mdb files contain more than one book.
* `openiti.new_books.convert.tei_converter_Thielen`, `new_books/convert/helper/html2md_Thielen`: added new converter for TEI files provided by Jan Thielen.
* `new_books/convert/tei_converter_generic.py`, `new_books/convert/helper/html2md.py`: Add the possibility to pass options to the `markdownify` function


### v.0.1.0:

* `openiti.helper.yml`: add support for empty lines and bullet lists in multiline values
* `openiti.new_books.convert.shamela_converter`: fix bugs in shamela converter

### v.0.0.9.post1 (patch): 

* `openiti.helper.ara`: fix bug in regex compilation

### v.0.0.9:

* `openiti.new_books.convert` : check and update all converters
* `openiti.helper.ara` : make counting characters in editorial sections optional (default: include Arabic characters in editorial sections)
* `openiti.helper.yml` : add custom error messages for broken and empty yml files
* `openiti.git.git_util` : add git utilities class, with `commit` method

### v.0.0.8: 

* `openiti.new_books.add.add_books`: fix import bug
* `openiti.new_books.convert`: add converter for Noorlib html files

### v.0.0.7: 

* `openiti.git.get_issues`: change authentication from username/password to GitHub token
* `openiti.helper.ara`: add function to normalize composite Arabic characters
* `openiti.helper.uri`: move functions for adding texts to the corpus to a new module, `openiti.new_books.add.add_books` 
* `openiti.helper.uri`: fix bug in the character count function (did not work if execute==True)
* `openiti.new_books.convert`: restructured folder and moved helper functions into a new subfolder called `helper`
* `openiti.new_books.convert.generic_converter`: 
    - reordered the main `convert_file` function and added inline documentation
    - made `convert_files_in_folder` function more flexible
* `openiti.new_books.convert`: added generic converters for shamela libraries, html and tei xml files, and custom converters for eShia and GRAR libraries
    - `openiti.new_books.convert.shamela_converter`
    - `openiti.new_books.convert.html_converter_generic`
    - `openiti.new_books.convert.html_converter_eShia`
    - `openiti.new_books.convert.tei_converter_generic`
    - `openiti.new_books.convert.tei_converter_GRAR`
* `openiti.new_books.convert.helper`: added helper functions for the new converters:
    - `openiti.new_books.convert.helper.html2md_eShia`
    - `openiti.new_books.convert.helper.html2md_GRAR`
    - `openiti.new_books.convert.helper.tei2md`
    - `openiti.new_books.convert.helper.bok`
 
### v.0.0.6: 

* `openiti.helper.uri`: use both Arabic character and token count in yml files
* `openiti.helper.uri`: add support for paths to files that are not in 25-years repos (e.g., for release)
* `openiti.helper.uri`: fix bugs
* added Sphinx documentation

### v.0.0.5:

* `openiti.helper.funcs`: added Arabic token count function
* `openiti.helper.uri`: use Arabic token count instead of Arabic character count for yml file revision. Also, revise token count for every version yml file instead of only for version yml files that do not contain a count.

### v.0.0.4: 

* `openiti.helper.uri`: removed the restriction on the use of digits in book titles
* `openiti.helper.uri`: added a check for empty yml files
* `openiti.helper.yml`: added documentation and doctests
* `openiti.helper.yml`: added check for empty yml files + changed splitting of yml files so that even unindented multi-line values can be correctly parsed.
