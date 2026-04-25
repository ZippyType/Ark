# Ark Language Integration Guide

## File Type Configuration

### VS Code Syntax Highlighting
To add `.ark` file support to VS Code, create or update `.vscode/settings.json`:

```json
{
  "files.associations": {
    "*.ark": "python"
  }
}
```

Or create a custom TextMate grammar (advanced):
```json
{
  "[ark]": {
    "editor.defaultFormatter": "custom.ark-formatter",
    "editor.formatOnSave": true
  }
}
```

### File Association (System Level)

#### Linux
```bash
# Add to ~/.config/mimeapps.list
text/x-ark=ark-editor.desktop;

# Or manually associate
xdg-mime default ark-editor.desktop text/x-ark
chmod +x script.ark
./script.ark
```

#### Windows
```batch
# In Command Prompt (Admin)
assoc .ark=arkfile
ftype arkfile="C:\Path\To\ark.exe" "%%1"
```

#### macOS
```bash
# Set default app for .ark files
duti -s com.arc.editor com.arc.ark all
chmod +x script.ark
./script.ark
```

## Command-Line Execution

### Scripts with Shebang
```bash
#!/usr/bin/env ark

fn main() (
    print("Hello from Ark!")
)

main()
```

Make executable:
```bash
chmod +x script.ark
./script.ark
```

### Direct Execution
```bash
ark script.ark
ark script.ark arg1 arg2
```

## MIME Type Registration

### Linux (Freedesktop Standard)
Create `/usr/share/mime/packages/ark.xml`:
```xml
<?xml version="1.0"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
  <mime-type type="text/x-ark">
    <comment>Ark source code</comment>
    <magic priority="50">
      <match type="string" offset="0" value="fn"/>
    </magic>
    <glob pattern="*.ark"/>
  </mime-type>
</mime-info>
```

Update MIME database:
```bash
sudo update-mime-database /usr/share/mime
```

## IDE/Editor Support

### VS Code Extension
Install the Ark bundle:
```
ext install arkLang.ark-syntax
```

### Vim/Neovim
Add to `~/.vim/ftdetect/ark.vim`:
```vim
au BufNewFile,BufRead *.ark setf ark
```

Create `~/.vim/syntax/ark.vim` with syntax highlighting rules.

### Emacs
Create `~/.emacs.d/ark-mode.el`:
```elisp
(define-derived-mode ark-mode fundamental-mode "Ark")
(add-to-list 'auto-mode-alist '("\\.ark\\'" . ark-mode))
```

## Compiler/Interpreter Integration

### PATH Configuration

#### Linux/macOS
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export PATH="/path/to/ark/bin:$PATH"
```

#### Windows
Add to System Environment Variables:
```
C:\Program Files\Ark\bin
```

### Shebang Support
The Ark runtime must support:
```bash
#!/usr/bin/env ark
```

This requires the `ark` executable to be in PATH with appropriate permissions.

## File Format Best Practices

### Encoding Declaration (Optional)
While UTF-8 is default, you can declare:
```ark
# coding: utf-8
// Ark code here
```

### File Header Template
```ark
#!/usr/bin/env ark
//
// Filename: example.ark
// Author: Your Name
// Version: 1.0.0
// Description: Brief description of what the script does
//

let VERSION = "1.0.0"

fn main() (
    print("Program started")
)

main()
```

## Troubleshooting

### Issue: "ark: command not found"
**Solution:** Add Ark to PATH
```bash
export PATH="$HOME/ark/bin:$PATH"
```

### Issue: Permission denied
**Solution:** Make file executable
```bash
chmod +x script.ark
```

### Issue: Encoding errors
**Solution:** Ensure file is saved as UTF-8
```bash
file -i script.ark  # Check encoding
iconv -f ISO-8859-1 -t UTF-8 script.ark > script_utf8.ark
```

---

**Integration Guide Version:** 0.1.0
**Last Updated:** 2026-04-25
