# unicodetext
Processing Unicode Text

🌍 [中文](README_cn.md)

## How To Use
1. Unicode's blocks (`unicodetext.UnicodeBlocks`), which can be quickly accessed through the IDE's auto-completion feature to obtain all the characters within the block.
```python
import unicodetext
print (unicodetext.UnicodeBlocks.Emoticons)
```
2. Unicode's categories (`unicodetext.UnicodeCategories`), which can be quickly accessed through the IDE's auto-completion feature to obtain all the characters within the category.
```python
import unicodetext
print (unicodetext.UnicodeCategories.Punctuation)
```
3. Character extraction.
```python
import unicodetext
text =  "i am here 237 .! 3 *。、！ +-23689068 发斯蒂芬改 23579 😄"
print (unicodetext.extract_emoticon(text))
```
Custom extraction can also be performed by providing specific Unicode blocks or categories:
```python
import unicodetext
text =  "i am here 237 .! 3 *。、！ +-23689068 发斯蒂芬改 23579 😄"
print (unicodetext.extract_chr(text, chrs=unicodetext.UnicodeCategories.Symbol))
```

4. Character removal
```python
import unicodetext
text =  "i am here 237 .! 3 *。、！ +-23689068 发斯蒂芬改 23579 😄"
print (unicodetext.remove_punctuation(text))
```
The removed characters can be replaced with specified characters by `replace_str`:
```python
import unicodetext
text =  "i am here 237 .! 3 *。、！ +-23689068 发斯蒂芬改 23579 😄"
print (unicodetext.remove_punctuation(text, replace_str = '[del]'))
```
Custom removal can also be performed by providing specific Unicode blocks or categories:
```python
import unicodetext
text =  "i am here 237 .! 3 *。、！ +-23689068 发斯蒂芬改 23579 😄"
print (unicodetext.remove_chr(text, chrs=unicodetext.UnicodeCategories.Symbol))
```

## Unicode character set
### unicodetext.UnicodeBlocks
  - Unicode 15.1 defines [328 blocks](https://en.wikipedia.org/wiki/Unicode_block#List_of_blocks). To enable automatic code completion for block names as variables, we remove all spaces and hyphens from their names.
### unicodetext.UnicodeCategories
  - Letter = Lu | Ll | Lt | Lm | Lo
  - Mark = Mn | Mc | Me
  - Number = Nd | Nl | No
  - Punctuation = Pc | Pd | Ps | Pe | Pi | Pf | Po
  - Symbol = Sm | Sc | Sk | So
  - Separator = Zs | Zl | Zp
  - Other = Cc | Cf | Cs | Co | Cn
  - Cased_Letter = Lu | Ll | Lt

| Abbr | Long                  | Description                                                        |
|:---- |:--------------------- | :------------------------------------------------------------------ |
| Lu   | Uppercase_Letter      | an uppercase letter                                                |
| Ll   | Lowercase_Letter      | a lowercase letter                                                 |
| Lt   | Titlecase_Letter      | a digraph encoded as a single character, with first part uppercase |
| Lm   | Modifier_Letter       | a modifier letter                                                  |
| Lo   | Other_Letter          | other letters, including syllables and ideographs                  |
| Mn   | Nonspacing_Mark       | a nonspacing combining mark (zero advance width)                   |
| Mc   | Spacing_Mark          | a spacing combining mark (positive advance width)                  |
| Me   | Enclosing_Mark        | an enclosing combining mark                                        |
| Nd   | Decimal_Number        | a decimal digit                                                    |
| Nl   | Letter_Number         | a letterlike numeric character                                     |
| No   | Other_Number          | a numeric character of other type                                  |
| Pc   | Connector_Punctuation | a connecting punctuation mark, like a tie                          |
| Pd   | Dash_Punctuation      | a dash or hyphen punctuation mark                                  |
| Ps   | Open_Punctuation      | an opening punctuation mark (of a pair)                            |
| Pe   | Close_Punctuation     | a closing punctuation mark (of a pair)                             |
| Pi   | Initial_Punctuation   | an initial quotation mark                                          |
| Pf   | Final_Punctuation     | a final quotation mark                                             |
| Po   | Other_Punctuation     | a punctuation mark of other type                                   |
| Sm   | Math_Symbol           | a symbol of mathematical use                                       |
| Sc   | Currency_Symbol       | a currency sign                                                    |
| Sk   | Modifier_Symbol       | a non-letterlike modifier symbol                                   |
| So   | Other_Symbol          | a symbol of other type                                             |
| Zs   | Space_Separator       | a space character (of various non-zero widths)                     |
| Zl   | Line_Separator        | U+2028 LINE SEPARATOR only                                         |
| Zp   | Paragraph_Separator   | U+2029 PARAGRAPH SEPARATOR only                                    |
| Cc   | Control               | a C0 or C1 control code                                            |
| Cf   | Format                | a format control character                                         |
| Cs   | Surrogate             | a surrogate code point                                             |
| Co   | Private_Use           | a private-use character                                            |
| Cn   | Unassigned            | a reserved unassigned code point or a noncharacter                 |


## Install
Install the library with:
```shell
pip install -U unicodetext
```
You can also clone this repository and install:
```shell
git clone https://github.com/huang22/unicodetext.git
cd unicodetext
pip install .
```
