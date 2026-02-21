import random

TIPS = [
    {
        "title": "Quick Jump to Last Argument",
        "content": "Use [bold cyan]!$[/] in your shell to quickly reference the last argument of your previous command. \nExample: [dim]mkdir my_folder && cd !$[/]"
    },
    {
        "title": "Reverse Search History",
        "content": "Press [bold cyan]Ctrl + R[/] to search through your command history instantly. It's much faster than pressing the up arrow!"
    },
    {
        "title": "The Magic of 'sudo !!'",
        "content": "Forgot to use sudo? Just type [bold cyan]sudo !![/] to run the previous command with root privileges."
    },
    {
        "title": "Empty a File Quickly",
        "content": "To clear all content from a file without deleting it, use: [bold cyan]> filename[/]"
    },
    {
        "title": "List by Size",
        "content": "Want to find the biggest files? Use [bold cyan]ls -lS[/] to sort the directory listing by file size."
    },
    {
        "title": "Check Your Disk Space",
        "content": "Use [bold cyan]df -h[/] to see how much space is left on your drives in a human-readable format."
    },
    {
        "title": "Monitor Logs in Real-Time",
        "content": "Use [bold cyan]tail -f /path/to/logfile[/] to watch new lines being added to a log file as they happen."
    },
    {
        "title": "Create Nested Directories",
        "content": "Use [bold cyan]mkdir -p path/to/deep/folder[/] to create all parent directories at once."
    },
    {
        "title": "Run in Background",
        "content": "Add an [bold cyan]&[/] at the end of a command to run it in the background. \nExample: [dim]gedit file.txt &[/]"
    },
    {
        "title": "Process Resource Map",
        "content": "Run [bold cyan]top[/] or [bold cyan]htop[/] to see exactly what is eating your CPU and RAM in real-time."
    }
]

def get_random_tip():
    """Returns a random tip dictionary."""
    return random.choice(TIPS)
