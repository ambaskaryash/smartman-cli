# VHS tape for SmartMan Demo 🎬
# Install vhs to run this: https://github.com/charmbracelet/vhs

Output demo.gif

Set Shell "bash"
Set FontSize 22
Set Width 1200
Set Height 600
Set Padding 20

# Start by showing the Tip of the Day
Type "smartman --tip"
Sleep 500ms
Enter
Sleep 3s

# Launch SmartMan with grep
Type "smartman grep"
Sleep 500ms
Enter
Sleep 2s

# Show off the Gallery and scrolling
Down 3
Sleep 500ms
Down 3
Sleep 1s
Type q
Sleep 3s

# Trigger Search
Type "smartman --explain awk"
Enter
Sleep 5s

# Quit
Type "q"
Sleep 1s
