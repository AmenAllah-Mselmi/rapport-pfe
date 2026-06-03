import sys
import re

pdf_path = 'main.pdf'
try:
    b = open(pdf_path, 'rb').read()
except Exception as e:
    print('ERROR: cannot open', pdf_path, e)
    sys.exit(1)

# extract sequences of printable unicode characters by attempting utf-8 decode on sliding windows
# simpler: replace non-printables with spaces using byte whitelist
printable = bytearray()
for byte in b:
    # allow common printable ASCII and Latin-1 extended letters (32..126, 160..255)
    if 32 <= byte <= 126 or 160 <= byte <= 255 or byte in (9,10,13):
        printable.append(byte)
    else:
        printable.append(32)

text = printable.decode('latin-1')
# collapse multiple spaces
text = re.sub(r'\s{2,}', ' ', text)

# markers
start_markers = ['Cadre du projet', '\\chapter{Cadre du projet}', 'Chapitre 1', '1 Cadre']
end_markers = ['Aper', 'Apercu', 'Aper\xc3\xa7u', 'Aper\xc3\xa7u conceptuel', 'Aperçu conceptuel', '\\chapter{Aperç', 'Chapitre 3']

start_idx = -1
for m in start_markers:
    i = text.find(m)
    if i != -1:
        start_idx = i + len(m)
        break

end_idx = -1
for m in end_markers:
    i = text.find(m)
    if i != -1 and (start_idx == -1 or i > start_idx):
        end_idx = i
        break

if start_idx == -1:
    print('START MARKER NOT FOUND; printing heuristic area around first occurrence of "Cadre" if any')
    start_idx = 0

if end_idx == -1:
    end_idx = len(text)

chapter2 = text[start_idx:end_idx].strip()

out = 'recovered_chapter2_strings.txt'
with open(out, 'w', encoding='utf-8') as f:
    f.write(chapter2)

print('WROTE', out)
print('\n---START---\n')
print(chapter2[:20000])
print('\n---END---')
