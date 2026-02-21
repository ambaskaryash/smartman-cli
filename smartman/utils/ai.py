import os
import requests
import re

def explain_command(command: str, raw_text: str) -> str:
    """
    Returns an AI-powered explanation of the command based on its manual page using Groq.
    Requires GROQ_API_KEY to be set in the environment.
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        return _mock_explanation(command)

    # Groq API endpoint for chat completions
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Clean the man text of control characters and backspaces
    cleaned_text = _clean_man_text(raw_text)
    truncated_text = cleaned_text[:12000] 

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system", 
                "content": "You are a Linux systems expert. Explain the following command based on its manual page. Keep it concise, practical, and easy for a beginner to understand. Focus on the core purpose and 2-3 most useful flags shown in the text. Use plain text formatting."
            },
            {
                "role": "user", 
                "content": f"Command: {command}\n\nManual Page Content:\n{truncated_text}"
            }
        ],
        "temperature": 0.5,
        "max_tokens": 500
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code != 200:
            error_msg = response.text
            return f"[bold red]AI Error (Groq {response.status_code}):[/bold red] {error_msg}\n\n{_mock_explanation(command, real_key_found=True)}"
        
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[bold red]AI Error (Groq):[/bold red] {str(e)}\n\n[dim]Falling back to offline summary...[/dim]\n\n{_mock_explanation(command, real_key_found=True)}"

def _clean_man_text(text: str) -> str:
    """Strips backspaces and other control characters used for man page formatting."""
    # Remove backspace overstrikes (e.g., 'a\ba' or '_\ba')
    text = re.sub(r'.\b', '', text)
    # Remove remaining non-printable characters except whitespace
    text = "".join(char for char in text if char.isprintable() or char in "\n\r\t")
    return text

def _mock_explanation(command: str, real_key_found: bool = False) -> str:
    """Provides high-quality mock explanations for common commands."""
    mocks = {
        "grep": "It's like a powerful search engine for your text. It looks through files line by line and shows you exactly where your pattern (a word or regex) matches. Useful for finding errors in logs or specific code sections.",
        "ls": "Shows you what's inside a folder. Think of it as 'opening' the folder to see the files and subdirectories. With flags like `-l`, it shows details like size, owner, and date.",
        "tar": "A tool for 'bundling' many files into one single archive (a .tar file). It's the standard way to package software on Linux. Often used with compression (like .tar.gz).",
        "find": "The ultimate detective. It searches through your whole system (or specific paths) to find files based on name, size, date, or even permissions.",
    }
    
    msg = mocks.get(command, f"A versatile Linux utility used for processing data or managing system tasks related to {command}.")
    
    if not real_key_found:
        msg = f"{msg}\n\n[dim](Note: To enable live AI, set your [b]GROQ_API_KEY[/b] in your shell environment.)[/dim]"
        
    return msg
