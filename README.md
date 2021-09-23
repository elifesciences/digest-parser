# digest-parser

Parse docx file containing digest content and produce output in other formats.

The contents of the `.docx` must follow a specific formatting scheme for it to be understood; each section of content is prefaced by a bold formatted title, such as `DIGEST TITLE`, and the content below it is used to populate the section of the output.

There are four types of output content which can be after parsing a `.docx` file:

1. DOCX output,
2. JATS XML output format,
3. JSON format, compatible with eLife API schema, or
4. Medium format, which can be used to create a new post at Medium service using their API, which can optionally overwrite some values if supplied a JATS XML research article file

Optionally, a `.zip` file can contain the `.docx` file and an optional graphic image file,. The image caption content can be included in the `.docx` and will be added to the `Image` object.

## Requirements

Parsing `.docx` files uses Python library dependency `python-docx`, as defined in the installation requirements files.

## Configuration

The `digest.cfg` configuration file provided in this repository can be changed in order to produce slightly different output, depending on the situation. It includes a way to change the Medium post content, `.docx` output file name, and to change IIIF image server URL paths.

## Example usage

This library is meant to be integrated into another operational system, however the following are examples using interactive Python:

Example 1 - Simple conversion of a `.docx` to JATS XML

```
>>> from digestparser import parse
>>> content = parse.parse_content("tests/test_data/DIGEST 99999.docx")
>>> print(content)
<b>AUTHOR</b>
Anonymous
<b>DIGEST TITLE</b>
```

Example 2 - Parse a `.docx` into Digest object and then output JSON

```
>>> from digestparser import build
>>> from digestparser import json_output
>>> from digestparser.conf import raw_config, parse_raw_config
>>> digest = build.build_digest("tests/test_data/DIGEST 99999.zip")
>>> digest_config = parse_raw_config(raw_config("elife"))
>>> print(json_output.digest_json(digest, digest_config))
OrderedDict([('id', 'None'), ('title', 'Fishing for errors in the\xa0tests'), ('impactStatement', ...
```

Example 3 - Parse a `.zip` and then output Medium post content

```
>>> from digestparser import medium_post
>>> from digestparser.conf import raw_config, parse_raw_config
>>> digest_config = parse_raw_config(raw_config("elife"))
>>> print(medium_post.build_medium_content("tests/test_data/DIGEST 99999.zip", digest_config=digest_config))
OrderedDict([('title', 'Fishing for errors in the\xa0tests'), ('contentFormat', 'html'), ...
```

## License

Licensed under [MIT](https://opensource.org/licenses/mit-license.php).
