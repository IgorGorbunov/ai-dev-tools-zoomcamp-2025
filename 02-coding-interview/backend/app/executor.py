import subprocess
import time
from typing import Optional
from .schemas import ExecutionResult, Language


class CodeExecutor:
    """Execute code snippets in different languages"""
    
    def __init__(self):
        self.timeout = 10  # seconds
    
    async def execute(
        self,
        code: str,
        language: Language,
        stdin: Optional[str] = None
    ) -> ExecutionResult:
        """Execute code and return result"""
        
        if language == Language.PYTHON:
            return await self._execute_python(code, stdin)
        elif language == Language.JAVASCRIPT:
            return await self._execute_javascript(code, stdin)
        else:
            return ExecutionResult(
                success=False,
                output=f"Language {language} not supported",
                stdout="",
                stderr=f"Language {language} not supported",
                return_code=1,
                execution_time=0
            )
    
    async def _execute_python(self, code: str, stdin: Optional[str]) -> ExecutionResult:
        """Execute Python code"""
        try:
            start_time = time.time()
            result = subprocess.run(
                ["python", "-c", code],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            execution_time = time.time() - start_time
            
            output = result.stdout + result.stderr
            
            return ExecutionResult(
                success=result.returncode == 0,
                output=output,
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                execution_time=execution_time
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="Execution timeout",
                stdout="",
                stderr="Execution timeout",
                return_code=-1,
                execution_time=self.timeout
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output=str(e),
                stdout="",
                stderr=str(e),
                return_code=-1,
                execution_time=0
            )
    
    async def _execute_javascript(self, code: str, stdin: Optional[str]) -> ExecutionResult:
        """Execute JavaScript code"""
        try:
            start_time = time.time()
            result = subprocess.run(
                ["node", "-e", code],
                input=stdin,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            execution_time = time.time() - start_time
            
            output = result.stdout + result.stderr
            
            return ExecutionResult(
                success=result.returncode == 0,
                output=output,
                stdout=result.stdout,
                stderr=result.stderr,
                return_code=result.returncode,
                execution_time=execution_time
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                success=False,
                output="Execution timeout",
                stdout="",
                stderr="Execution timeout",
                return_code=-1,
                execution_time=self.timeout
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                output=str(e),
                stdout="",
                stderr=str(e),
                return_code=-1,
                execution_time=0
            )


# Global executor instance
code_executor = CodeExecutor()
