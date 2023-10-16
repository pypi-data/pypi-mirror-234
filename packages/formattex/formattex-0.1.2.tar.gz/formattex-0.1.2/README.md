# formattex: a simple and uncompromising Latex code formatter

I didn't find a Latex formatter that fits my needs... Let's try to write such
minimalist Latex formatter.

## Getting started

```
pip install formattex
formattex input/*.tex -i
```

`-i` is for `--inplace`. In this mode, a file
`input/tmp_saved_input_article.tex` is saved.

## Internal

I tried with https://github.com/alvinwan/TexSoup but
https://github.com/phfaist/pylatexenc/ could also be used.
