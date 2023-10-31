import re
from save_to import save_to

def extract_entry_information(entry_text):
    # Define regular expressions to extract relevant information
    title_pattern = re.compile(r'题 名:(.*)\n')
    authors_pattern = re.compile(r'作 者：(.*)\n')
    affiliation_pattern = re.compile(r'作者单位：(.*)\n')
    journal_pattern = re.compile(r'期刊名称：(.*)\n')
    keywords_pattern = re.compile(r'关键词：(.*)\n')
    source_pattern = re.compile(r'出 处：(.*)\n')
    abstract_pattern = re.compile(r'摘 要：(.*)\n')
    link_pattern = re.compile(r'链接地址：(.*)\n')
    citation_pattern = re.compile(r'引 证：(.*)\n')
    issn_pattern=re.compile(r'ISSN:(.*)\n')

    # Extract information using regular expressions
    title = re.search(title_pattern, entry_text).group()
    title_without_prefix = re.sub(r'^题 名:', '', title)
    final_title=re.sub(r'[\n]$','',title_without_prefix).replace('  ', '') # 去掉末尾的换行符和空白

    authors = re.search(authors_pattern, entry_text).group()
    authors_without_prefix=re.sub(r'^作 者：','',authors)
    authors_without_brackets=re.sub(r'（.*）','',authors_without_prefix)
    final_authors=re.sub(r'[\n]$','',authors_without_brackets).replace('  ', '')

    affiliation = re.search(affiliation_pattern, entry_text).group()
    affiliation_without_prefix=re.sub(r'^作者单位：','',affiliation)
    final_affiliation=re.sub(r'[\n]$','',affiliation_without_prefix).replace('  ', '')

    journal = re.search(journal_pattern, entry_text).group()
    journal_without_prefix=re.sub(r'^期刊名称：','',journal)
    final_journal=re.sub(r'[\n]$','',journal_without_prefix).replace('  ', '')

    keywords = re.search(keywords_pattern, entry_text)
    if keywords is None:
        final_keywords="none"
    else:
        keywords=keywords.group()
        keywords_without_prefix=re.sub(r'^关键词：','',keywords)
        final_keywords=re.sub(r'[\n]$','',keywords_without_prefix).replace('  ', '')

    source = re.search(source_pattern, entry_text).group()
    source_without_prefix=re.sub(r'^出 处：','',source)
    final_source=re.sub(r'[\n]$','',source_without_prefix)

    abstract = re.search(abstract_pattern, entry_text)
    if abstract is None:
        final_abstract="none"
    else:
        abstract=abstract.group()
        abstract_without_prefix=re.sub(r'^摘 要：','',abstract)
        final_abstract=re.sub(r'[\n]$','',abstract_without_prefix).replace('  ', '')

    link = re.search(link_pattern, entry_text).group()
    link_without_prefix=re.sub(r'^链接地址：','',link)
    final_link=re.sub(r'[\n]$','',link_without_prefix)

    citation = re.search(citation_pattern, entry_text).group()
    citation_without_prefix=re.sub(r'^引 证：','',citation)
    final_citation=re.sub(r'[\n]$','',citation_without_prefix).replace('  ', '')

    issn=re.search(issn_pattern,entry_text)
    if issn is None:
        final_issn = "none"
    else:
        issn = issn.group()
        issn_without_prefix=re.sub(r'^ISSN:','',issn)
        final_issn=re.sub(r'[\n]$','',issn_without_prefix).replace('  ', '')

    # Create a dictionary with the extracted information
    entry_dict = {
        'title': final_title,
        'authors': final_authors,
        'affiliations': final_affiliation,
        'journal': final_journal,
        'keywords': final_keywords,
        'source': final_source,
        'abstract': final_abstract,
        'link': final_link,
        'citation': final_citation,
        'ISSN':final_issn
    }

    return entry_dict

filename='上海2022.txt'
with open(filename,'r',encoding='utf-8') as f:
    input_string=f.read()

# 根据[期刊]进行分割条目并计数
entries = re.split(r'\d+\.\[期刊\]', input_string)[1:]
print(f"共有{len(entries)}条")
# 构建字典
entry_dicts = [extract_entry_information(entry) for entry in entries]

result_filename='result上海2022.json'
for entry_dict in entry_dicts:
    save_to(result_filename,entry_dict)
# # Print the result
# for i, entry_dict in enumerate(entry_dicts, start=1):
#     print(f"Entry {i}:\n{entry_dict}\n")
