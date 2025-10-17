"""
Local Shell Executor for Windows System.

This module provides the shell executor function for the LocalShellTool
from OpenAI Agents SDK. It handles execution of Windows CMD and PowerShell commands.
"""

import os
import subprocess
from agents import LocalShellCommandRequest


def shell_executor(request: LocalShellCommandRequest) -> str:
    """
    Execute shell commands on Windows system.
    
    This function is used by LocalShellTool from OpenAI Agents SDK
    to execute any Windows command line or PowerShell commands.
    
    Args:
        request: LocalShellCommandRequest containing the command details
        
    Returns:
        str: The command output (stdout + stderr) or error message
        
    Examples:
        Commands executed through this executor can include:
        - File operations: dir, copy, move, del, mkdir, rmdir
        - System information: systeminfo, tasklist, netstat
        - Network operations: ping, curl, wget
        - Package managers: pip, npm, choco
        - Git operations: git status, git commit, git push
        - PowerShell commands and scripts
    """
    args = request.data.action
    
    try:
        # Execute command with proper Windows support
        completed = subprocess.run(
            args.command,
            cwd=args.working_directory or os.getcwd(),
            env={**os.environ, **args.env} if args.env else os.environ,
            capture_output=True,
            text=True,
            timeout=(args.timeout_ms / 1000) if args.timeout_ms else 30,
            shell=True,  # Required for Windows CMD/PowerShell commands
            encoding='utf-8',
            errors='replace'  # Handle encoding issues gracefully
        )
        
        # Combine stdout and stderr for complete output
        output = ""
        if completed.stdout:
            output += completed.stdout
        if completed.stderr:
            if output:
                output += "\n"
            output += completed.stderr
        
        # Add return code information for non-zero exits
        if completed.returncode != 0:
            output += f"\n[Exit code: {completed.returncode}]"
        
        return output if output else "Command executed successfully with no output."
        
    except subprocess.TimeoutExpired:
        return f"⏰ Command execution timed out after {args.timeout_ms/1000 if args.timeout_ms else 30} seconds"
    except Exception as e:
        return f"❌ Error executing command: {str(e)}"

