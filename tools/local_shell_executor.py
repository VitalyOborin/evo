"""
Shell Command Tool for Windows System.

This module provides the execute_shell_command function tool for the AI agent
to perform any Windows system operations including:
- File operations (dir, copy, move, del, mkdir, rmdir)
- System information (systeminfo, tasklist, netstat)
- Network operations (ping, curl, wget)
- Package managers (pip, npm, choco)
- Git operations (git status, commit, push)
- Any other system commands available in Windows CMD or PowerShell
"""

import subprocess
from agents import function_tool


@function_tool
async def execute_shell_command(command: str) -> str:
    """
    Execute any shell/command line command on the Windows system.
    
    This function can execute ANY system commands including:
    - File operations: dir, copy, move, del, mkdir, rmdir
    - System information: systeminfo, tasklist, netstat
    - Network operations: ping, curl, wget
    - Package managers: pip, npm, choco
    - Git operations: git status, git commit, git push
    - PowerShell commands and scripts
    - Any executable programs available in PATH
    
    Args:
        command: Any valid Windows command line or PowerShell command
        
    Returns:
        str: The command output (stdout) or error message if command fails
        
    Examples:
        dir - list current directory contents
        pip list - show installed Python packages
        git status - show git repository status
        systeminfo - display system information
        netstat -an - show network connections
    """
    try:
        # Execute command with timeout to prevent hanging
        # Use shell=True to support both cmd and PowerShell commands
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,  # 30 seconds timeout
            encoding='utf-8',
            errors='replace'  # Handle encoding issues gracefully
        )
        
        # Combine stdout and stderr for complete output
        output = ""
        if result.stdout:
            output += f"Output:\n{result.stdout}"
        if result.stderr:
            output += f"\nError/Warning messages:\n{result.stderr}"
        
        # Add return code information
        if result.returncode != 0:
            output += f"\nCommand exited with return code: {result.returncode}"
        else:
            output += f"\nCommand executed successfully (return code: 0)"
            
        return output if output else "Command executed but produced no output."
        
    except subprocess.TimeoutExpired:
        return f"Command timed out after 30 seconds: {command}"
    except subprocess.CalledProcessError as e:
        return f"Command failed with return code {e.returncode}: {e.stderr or 'No error message'}"
    except Exception as e:
        return f"System error executing command: {str(e)}"

