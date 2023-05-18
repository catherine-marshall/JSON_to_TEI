# This is the updated version
import json

filename = "Korean_test_report.json"

with open(filename, 'r', encoding='utf-8') as json_file:
    json_load = json.load(json_file)
    # print(json_load)

project_name = json_load["projectName"]

publisher = input("What is the publisher's name?")
source_desc = input("Provide a brief description for this document:")

filename = "korean-test-tei.xml"
file = open(filename, "w", encoding="utf-8")
file.write("")
file.close()

print('<TEI xmlns="http://www.tei-c.org/ns/1.0">'
      '  <teiHeader xml:lang="en">'
      '\t<fileDesc>'
      '\t\t<titleStmt>'
      '\t\t\t<title>' + project_name + '</title>'
      '\t\t</titleStmt>'
      '\t\t<publicationStmt>'
      '\t\t\t<publisher>' + publisher + '</publisher>'
      '\t\t</publicationStmt>'
      '\t\t<sourceDesc>'
      '\t\t\t<p>' + source_desc + '</p>'
      '\t\t</sourceDesc>'
      '\t</fileDesc>'
      '  </teiHeader>'
      '  <text>'
      '   <body>'
      '\t<list>',
      file=open(filename,"a", encoding="utf-8"))

key = json_load["key"]

for k in key:
    key_value = '\t\t<item n="' + k + '">' + key[k] + '</item>'
    print(key_value,file=open(filename, "a", encoding="utf-8"))

errors = json_load["errors"]

print('\t</list>'
      '\t<div type="errors">',
      file=open(filename,"a", encoding="utf-8"))

for error in errors:
    print('\t <div type="error">\n'
          '\t  <list>\n'
          '\t\t<item n="segment">' + error["segment"] + '</item>\n'
          '\t\t<item n="target">' + error["target"] + '</item>\n'
          '\t\t<item n="name">' + error["name"] + '</item>\n'
          '\t\t<item n="severity">' + error["severity"] + '</item>\n'
          '\t\t<item n="issueReportId">' + error["issueReportId"] + '</item>\n'
          '\t\t<note>' + error["note"] + '</note>\n'
          '\t\t<item n="startIndex">' + str(error["highlighting"]["startIndex"]) + '</item>\n'
          '\t\t<item n="endIndex">' + str(error["highlighting"]["endIndex"]) + '</item>\n'
          '\t  </list>\n'
          '\t </div>',
          file=open(filename, "a", encoding="utf-8"))

metrics = json_load["metric"]

print('\t</div>\n'
      '\t<div type="metrics">',
      file=open(filename, "a", encoding="utf-8"))

for metric in metrics:
    print('\t <div type="metric">\n'
          '\t  <list>\n'
          '\t\t<item n="parent">' + str(metric["parent"]) + '</item>\n'
          '\t\t<item n="name">' + metric["name"] + '</item>\n'
          '\t\t<item n="description">' + metric["description"] + '</item>\n'
          '\t\t<note>' + metric["notes"] + '</note>\n'
          '\t\t<item n="examples">' + metric["examples"] + '</item>\n'
          '\t\t<item n="issueId">' + metric["issueId"] + '</item>\n'
          '\t  </list>\n'
          '\t </div>',
          file=open(filename, "a", encoding="utf-8"))

print('\t</div>',
      file=open(filename, "a", encoding="utf-8"))

