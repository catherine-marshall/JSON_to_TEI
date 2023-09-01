import json
import re
import os

# Working directory
os.chdir(r"C:\Users\cem327\Downloads\JSON")

# Defines the language codes
language_codes = {"A": "AR", "C": "ZH", "Cr": "HR", "D": "NL", "E": "EN", "Fi": "FI", "F": "FR", "G": "DE", "H": "HU", "I": "IT", "J": "JA", "L": "PL", "P": "PT", "R": "RU", "S": "ES", "U": "UK"}

# Gets all JSON files from a directory
filenames = [f for f in os.listdir() if f.endswith(".json")]

# Potential input questions
# publisher = input("What is the publisher's name? ")
# source_desc = input("Provide a brief description for this document: ")
year = input("What year are these exams? ")


for filename in filenames:
      print(filename)
      total_points = 0
      # This gets the language codes
      split = filename.split("-")
      split = split[0]
      if split[0] == "E":
            source_lang = language_codes[split[0]]
            target_lang = language_codes[split[1:]]
      else:
            source_lang = language_codes[split[:-1]]
            target_lang = language_codes[split[-1]]

      # This opens and retrieves the text from the JSON file
      with open(filename, 'r', encoding='utf-8') as json_file:
            json_load = json.load(json_file)

      # This creates the output file
      filename = re.sub(".json", "", filename)
      filename = filename + ".xml"
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
            # '\t\t<publicationStmt>\n'
            # '\t\t\t<publisher>' + publisher + '</publisher>\n'
            # '\t\t</publicationStmt>\n'
            # '\t\t<sourceDesc>\n'
            # '\t\t\t<p>' + source_desc + '</p>\n'
            # '\t\t</sourceDesc>\n'
            '\t</fileDesc>\n'
            '  </teiHeader>\n'
            '  <text>\n'
            '   <body>\n'
            '\t<list>\n'
            '\t\t<item n="year">' + year + '</item>\n'
            '\t\t<item n="comment"></item>\n'
            '\t\t<item n="keyword"></item>\n'
	        '\t</list>\n'
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
            repeated = False
            discontinuous = False
            semicolon_count = 0
            ata_code = ""
            ata_points = ""
            ata_note = ""
            other_code = ""
            if error["note"][-1] == '\n':
                  error["note"] = error["note"][:-1]
            if error["note"][2:5] =="@RE":
                  repeated = True
            if error["note"][2:5] =="@DE":
                  discontinuous = True
            for char in error["note"]:
                  if semicolon_count == 2:
                        ata_code += char
                  if semicolon_count == 3:
                        ata_points += char
                  if semicolon_count == 4:
                        ata_note += char
                  if semicolon_count == 5:
                        print("The filename is : " + filename)
                        print("THERE IS AN ERROR WITH THE NOTES IN THIS FILE.\nNote: " + error["note"])
                        exit()
                  if char == ";":
                        semicolon_count += 1
            if ";" in ata_code:
                  ata_code = re.sub(";", "", ata_code)
            if ata_code[0] == " ":
                  ata_code = ata_code[1:]
            if ";" in ata_points:
                  ata_points = re.sub(";", "", ata_points)
            if ata_points[0] == " ":
                  ata_points = ata_points[1:]
            if len(ata_note) > 0:
                  if ata_note[0] == " ":
                        ata_note = ata_note[1:]
            if "grader also labeled the error as" in ata_note:
                  i = -1
                  while ata_note[i] != " ":
                        other_code += ata_note[i]
                        i = i - 1
                  other_code = other_code[::-1]
                  ata_code += "/" + other_code
                  ata_note = re.sub(",? ?(T|t)he grader also labeled the error as .+", "", ata_note)
                  print("ATA code: " + ata_code)
                  print("ATA note: " + ata_note)

            print('\t <div type="error">\n'
                  '\t  <list>\n'
                  '\t\t<item n="segment">' + error["segment"] + '</item>\n'
                  '\t\t<item n="target">' + error["target"] + '</item>\n'
                  '\t\t<item n="name">' + error["name"] + '</item>\n'
                  '\t\t<item n="severity">' + error["severity"] + '</item>\n'
                  '\t\t<item n="issueReportId">' + error["issueReportId"] + '</item>\n'
                  '\t\t<item n="repeated_error">' + str(repeated) + '</item>\n'
                  '\t\t<item n="discontinuous_error">' + str(discontinuous) + '</item>\n'
                  '\t\t<item n="ata_code">' + ata_code + '</item>\n'
                  '\t\t<item n="ata_points">' + ata_points + '</item>\n'   
                  '\t\t<item n="ata_note">' + ata_note + '</item>\n'
                  '\t\t<item n="startIndex">' + str(error["highlighting"]["startIndex"]) + '</item>\n'
                  '\t\t<item n="endIndex">' + str(error["highlighting"]["endIndex"]) + '</item>\n'
                  '\t  </list>\n'
                  '\t </div>',
                  file=open(filename, "a", encoding="utf-8"))

            total_points += int(ata_points)
            print(total_points)
      if total_points <= 17:
            passed = True
      else:
            passed = False


      # This prints the metric
      metrics = json_load["metric"]

      print('\t</div>\n'
            '\t<div type="metrics">',
            file=open(filename, "a", encoding="utf-8"))

      # This gets rid of any line breaks in the metric
      for metric in metrics:
            if "\n" in metric["examples"]:
                  metric["examples"] = re.sub(("\n"), " ", metric["examples"])
            if "\r" in metric["examples"]:
                  metric["examples"] = re.sub(("\r"), " ", metric["examples"])
            if "\n" in metric["notes"]:
                  metric["notes"] = re.sub(("\n"), " ", metric["notes"])
            if "\r" in metric["notes"]:
                  metric["notes"] = re.sub(("\r"), " ", metric["notes"])

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
            '\t \t<item n="passed">' + str(passed) + '</item>\n'
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
                        segment = re.sub(char, chars_dict[char], segment)
            print('\t\t<s xml:id="y' + seg + '">' + segment + '</s>', file=open(filename, "a", encoding="utf-8"))
      print('\t  </p>\n'
            '\t</div>', file=open(filename, "a", encoding="utf-8"))

      # This prints out the closing tags at the end
      print('   </body>\n'
            '  </text>\n'
            '</TEI>', file=open(filename, "a", encoding="utf-8"))

      with open(filename, "r", encoding="utf-8") as infile:
            lines = infile.readlines()
            new_lines = []
            for line in lines:
                  line = re.sub("<em>", "<emph>", line)
                  line = re.sub("</em>", "</emph>", line)
                  new_lines.append(line)

      # This recreates the output file
      file = open(filename, "w", encoding="utf-8")
      file.write("")
      file.close()

      for line in new_lines:
            if line[-1] == "\n" or line[-1] == "\r":
                  line = line[:-1]
            print(line, file=open(filename, "a", encoding="utf-8"))
