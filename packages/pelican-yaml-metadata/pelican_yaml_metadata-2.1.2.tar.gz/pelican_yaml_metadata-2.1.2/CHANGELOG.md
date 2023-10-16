CHANGELOG
=========

2.1.2 - 2023-10-10
------------------

- Strip all null entries from metadata to avoid returning empty tags and authors

Contributed by [Carey Metcalfe](https://github.com/pR0Ps) via [PR #7](https://github.com/pelican-plugins/yaml-metadata/pull/7/)


2.1.1 - 2023-06-13
------------------

- Ignore blank lines before the starting `---` marker
- Optimize Markdown parsing
- Small logging improvements

2.1.0 - 2023-06-09
------------------

Publish first package release to PyPI.

Contributed by [Justin Mayer](https://github.com/justinmayer) via [PR #2](https://github.com/pelican-plugins/yaml-metadata/pull/2/)


2.0.0 - 2021-06-08
------------------

- Convert to namespace package and enable installation via Pip
- Fall back to Markdown metadata parsing if the YAML block isn't found
- Use `yaml.safe_load` to load the data
- Metadata parsing now more closely matches Markdown metadata parsing
- Update dependency specifications

1.0.0 - 2017-08-21
------------------

Add support for ellipsis ending YAML header
