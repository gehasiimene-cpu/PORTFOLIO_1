from pathlib import Path
path = Path('c:/Users/Gehas/Desktop/web pt/2026 portfolio website/main_12.py')
text = path.read_text(encoding='utf-8')
lines = text.splitlines()
out = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.strip() == 'page.update()' and i + 1 < len(lines) and lines[i + 1].strip() == 'def blog(e):':
        out.append(line)
        out.append('        set_chat_visible(False, update_ui=False)')
        i += 1
        continue
    if line.strip() == 'page.update()' and i + 1 < len(lines) and lines[i + 1].strip() == 'def button_hover(e):':
        out.append(line)
        out.append('        set_chat_visible(False, update_ui=False)')
        i += 1
        continue
    out.append(line)
    i += 1
path.write_text('\n'.join(out) + '\n', encoding='utf-8')
print('patched')
