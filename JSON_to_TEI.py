# This is the updated version
import json
import re

filename = "Korean_test_report.json"

# This opens and retrieves the text from the JSON file
with open(filename, 'r', encoding='utf-8') as json_file:
    json_load = json.load(json_file)
    # print(json_load)

# These are all the input questions
publisher = input("What is the publisher's name? ")
source_desc = input("Provide a brief description for this document: ")
source_lang = input("What is the language code of the source language? ")
target_lang = input("What is the language code of the target language? ")

# This creates the output file
filename = "korean-test-tei.xml"
file = open(filename, "w", encoding="utf-8")
file.write("")
file.close()

# This prints the header
project_name = json_load["projectName"]
print('<TEI xmlns="http://www.tei-c.org/ns/1.0">\n'
      '  <teiHeader xml:lang="en">\n'
      '\t<fileDesc>\n'
      '\t\t<titleStmt>\n'
      '\t\t\t<title>' + project_name + '</title>\n'
      '\t\t</titleStmt>\n'
      '\t\t<publicationStmt>\n'
      '\t\t\t<publisher>' + publisher + '</publisher>\n'
      '\t\t</publicationStmt>\n'
      '\t\t<sourceDesc>\n'
      '\t\t\t<p>' + source_desc + '</p>\n'
      '\t\t</sourceDesc>\n'
      '\t</fileDesc>\n'
      '  </teiHeader>\n'
      '  <text>\n'
      '   <body>\n'
      '\t<list>', file=open(filename, "a", encoding="utf-8"))

# This prints the key
key = json_load["key"]

seg_list = []
for k in key:
    key_value = '\t\t<item n="' + k + '">' + key[k] + '</item>'
    print(key_value,file=open(filename, "a", encoding="utf-8"))
    seg_list.append(key[k])

errors = json_load["errors"]

print('\t</list>\n'
      '\t<div type="errors">',
      file=open(filename,"a", encoding="utf-8"))


# This prints the error info
for error in errors:
    if error["note"][-1] == '\n':
          error["note"] = error["note"][:-1]
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


# This prints the metric
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


# This prints the composite score
score = json_load["scores"]

for k in score:
      comp_score = score[k]

print('\t<div type="scores">\n'
      '\t <list>\n'
      '\t \t<item n="compositeScore">' + comp_score + '</item>\n'
      '\t </list>\n'
      '\t</div>',
      file=open(filename, "a", encoding="utf-8"))


# This prints the bitext linkGrp
print('\t<linkGrp type="translation">', file=open(filename, "a", encoding="utf-8"))
for seg in seg_list:
      print('\t\t<link target =" #x' + seg + ' #y' + seg + ' "/>', file=open(filename, "a", encoding="utf-8"))
print('\t</linkGrp>', file=open(filename, "a", encoding="utf-8"))


# This prints the source and target texts
source_text = json_load["segments"]["source"]
target_text = json_load["segments"]["target"]
chars = '&<>\"ˋ'
chars_dict = {'&': '&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', 'ˋ': '&apos;'}

# Prints source text
print('\t<div type="volume" xml:id="x" xml:lang ="' + source_lang + '">\n'
      '\t  <p>', file=open(filename, "a", encoding="utf-8"))
for seg in seg_list:
      if source_text[int(seg) - 1][-1] == "\n" or source_text[int(seg) - 1][-1] == "\r":
            source_text[int(seg) - 1] = source_text[int(seg) - 1][:-1]
      segment = source_text[int(seg) - 1]
      for char in chars:
            if char in segment:
                  segment = re.sub(char, chars_dict[char], segment)
                  print(segment)
      print('\t\t<s xml:id="x' + seg + '">' + segment + '</s>', file=open(filename, "a", encoding="utf-8"))
print('\t  </p>\n'
      '\t</div>', file=open(filename, "a", encoding="utf-8"))

# Prints target text
print('\t<div type="volume" xml:id="y" xml:lang ="' + target_lang + '">\n'
      '\t  <p>', file=open(filename, "a", encoding="utf-8"))
for seg in seg_list:
      if target_text[int(seg) - 1][-1] == "\n" or target_text[int(seg) - 1][-1] == "\r":
            target_text[int(seg) - 1] = target_text[int(seg) - 1][:-1]
      segment = target_text[int(seg) - 1]
      for char in chars:
            if char in segment:
                  print("HERE: " + char)
                  segment = re.sub(char, chars_dict[char], segment)
                  print(segment)
      print('\t\t<s xml:id="x' + seg + '">' + segment + '</s>', file=open(filename, "a", encoding="utf-8"))
print('\t  </p>\n'
      '\t</div>', file=open(filename, "a", encoding="utf-8"))

# This prints out the closing tags at the end
print('   </body>\n'
      '  </text>\n'
      '</TEI>', file=open(filename, "a", encoding="utf-8"))
