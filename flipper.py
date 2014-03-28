#!/usr/bin/python

import csv
from string import Template
import json

from optparse import OptionParser
parser = OptionParser()
parser.add_option('-f', '--file', action='store', dest='file')
parser.add_option('-t', '--tsv',
                  action='store_const', dest='delimiter', const='\t')
parser.add_option('-d', '--delimiter',
                  action='store', type='string', dest='delimiter')
parser.add_option('-c', '--column',
                  action='store', type='int', dest='column', default=1)
parser.add_option('-H', '--header',
                  action='store_true', dest='headers', default=False)
parser.add_option('--proxy', action='store_true', dest='proxy', default=False,
  help='proxy requests through a server, implies --server')
parser.add_option('-s', '--server',
  action='store_true', dest='server', default=False)
parser.add_option('-p', '--pattern',
                  action='append', type='string', dest='patterns', help='Specify a url pattern that looks like "http://xxx/yyy?q=${c0}&ll=${c1}" where the numbers are the column indexes, can be specified multiple times. If header mode is used, these can also be column names')
          
(options, args) = parser.parse_args()

def generateUrls(line):
  replacementDict = {}
  for colIndex, value in enumerate(line):
    replacementDict['c' + str(colIndex)] = value
  urls = [
    Template(pattern).substitute(replacementDict)
      for pattern in options.patterns
  ]
  return {
    'line': line,
    'urls': urls
  }

def generateUrlsFromDict(fieldnames, lineDict):
  replacementDict = {}
  fieldIndexes = {}
  for colIndex, fn in enumerate(fieldnames):
    fieldIndexes[fn] = colIndex

  for colName, value in lineDict.items():
    replacementDict[colName] = value
    replacementDict['c' + str(fieldIndexes[colName])] = value
  urls = [
    Template(pattern).substitute(replacementDict)
      for pattern in options.patterns
  ]
  return {
    'lineDict': line,
    'urls': urls
  }

if options.headers:
  reader = csv.DictReader(open(options.file), delimiter=(options.delimiter or ','))
  outputLines = [generateUrlsFromDict(reader.fieldnames, line) for line in reader]
else:
  outputLines = [generateUrls(line)
    for line in csv.reader(open(args[0]), delimiter=(options.delimiter or ','))]

### server deal

if options.server or options.proxy:
  from flask import Flask
  from flask import render_template
  import requests

  app = Flask(__name__)

  @app.route("/")
  def index():
    return render_template('flipper.html', data = outputLines, proxy = options.proxy)

  @app.route("/proxy/<path:other>")
  def proxy(other):
    r = requests.get(other)
    return r.content

  if __name__ == "__main__":
    app.run(debug=True)
else:
  from jinja2 import Environment, PackageLoader
  env = Environment(loader=PackageLoader(__name__, 'templates'))
  env.filters['tojson'] = json.dumps
  print env.get_template('flipper.html').render(data = outputLines, proxy = options.proxy)
