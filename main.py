import re, os, json

import requests

def cached_pull(url):
  url_filename = re.sub(r'[^A-Za-z0-9_\-]', '_', url)
  cache_dir_path = os.path.expanduser('~/spider_cache')
  cache_file_path = os.path.join(cache_dir_path, url_filename)[:100]
  if os.path.exists(cache_file_path):
    with open(cache_file_path) as f:
      return f.read()
  if not os.path.exists(cache_dir_path):
    os.mkdir(cache_dir_path)

  resp = requests.get(url)
  with open(cache_file_path, 'w') as f:
    f.write(resp.content)
  return resp.content

class Spider:
  def __init__(self):
    self.visited = set()
    self.links = []

  def spider(self, url):
    if url.startswith('//'):
      url = 'https:' + url
    if url in self.visited:
      return
    if url.startswith('mailto'):
      return
    for exten in 'pdf', 'zip', 'jpg':
      if url.endswith('.' + exten):
        return

    print 'spidering:', url

    self.visited.add(url)
    content = cached_pull(url)

    for href_match in re.finditer(r'"([^ ]+?\.com[^ ]*?)"', content):
      self.spider(href_match.group(1))

class Link:
  def __init__(self, url, text, parent_url):
    self.url = url
    self.text = text.strip()
    self.parent_url = parent_url

def main():
  spider = Spider()
  spider.spider('https://www.google.com/search?q=real+estate+san+francisco')

if __name__ == '__main__':
  main()
