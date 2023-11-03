# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['TeiUtils']

# %% ../nbs/00_core.ipynb 3
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
import urllib.request
import os
from typing import Dict

# %% ../nbs/00_core.ipynb 4
class TeiUtils:
    """ Utility class for working with TEI files. """

    def __init__(self):
        self.tag_counts = defaultdict(int)
        self.df = None
        self.df_tag = None

    def download(self, url: str, path: str) -> None:
        """ Download a file from a specified URL to a local path.
        
        Args:
            url: The URL from which to download the file.
            path: The local file path to save the downloaded file.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        urllib.request.urlretrieve(url, path)

    def get_tag_freq(self, path: str) -> None:
        """ Read an XML file from a specified path and count the frequency of each tag.
        
        The frequencies are stored in an attribute `tag_counts`.
        A sorted DataFrame of tags and counts is stored in `df` and `df_tag`.
        
        Args:
            path: The file path of the XML file to parse.
        """
        with open(path, "r") as f:
            xml = f.read()

        soup = BeautifulSoup(xml, 'lxml-xml')

        for tag in soup.find_all(True):
            self.tag_counts[tag.name] += 1

        self.df = pd.DataFrame(list(self.tag_counts.items()), columns=["Tag", "Count"])
        self.df.sort_values(by="Count", ascending=False, inplace=True)

        self.df_tag = self.df.sort_values(by="Tag", ascending=True)

    def get_javascript(self) -> None:
        """ Print a JavaScript object containing the tag counts. """

        tags = []

        for i, row in self.df_tag.iterrows():
            tags.append(f"\"{row['Tag']}\"")

        javascript_code = f"""
function checkCheckboxesWithTextValues(textValues) {{
    // 存在しなかった要素名を格納する配列
    let notFound = [];

    // 指定されたテキスト値のリストをループ処理
    textValues.forEach(function(textToMatch) {{
        // テキストに一致する .mdc-list-item__primary-text 要素を取得
        let found = false;
        document.querySelectorAll('.mdc-list-item__primary-text').forEach(function(item) {{
            if (item.textContent.trim() === textToMatch) {{
                found = true;
                let checkbox = item.closest('.mdc-list-item').querySelector('.mdc-checkbox__native-control');
                if (checkbox) {{
                    checkbox.checked = true;
                }}
            }}
        }});

        // 要素が見つからなければ notFound 配列に追加
        if (!found) {{
            notFound.push(textToMatch);
        }}
    }});

    // 存在しなかった要素名を返す
    return notFound;
}}

// 指定したいテキスト値のリスト
const itemsToCheck = [{", ".join(tags)}];

// チェックしたい項目のリストを関数に渡し、存在しなかった項目を取得
const itemsNotFound = checkCheckboxesWithTextValues(itemsToCheck);

// 存在しなかった項目をコンソールに出力
if (itemsNotFound.length > 0) {{
    console.log('These items were not found:', itemsNotFound);
}} else {{
    console.log('All items were found and checked.');
}}
"""

        return javascript_code
