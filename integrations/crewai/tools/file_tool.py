"""File Operations Tool for CrewAI Agents"""

import os
import json
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class FileResult:
    """Represents a file operation result"""

    success: bool
    message: str
    path: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class FileTool:
    """Tool for file system operations"""

    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize FileTool

        Args:
            base_path: Base directory for file operations. Defaults to current directory
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()

    def read_file(self, file_path: str, encoding: str = "utf-8") -> FileResult:
        """
        Read content from a file

        Args:
            file_path: Path to the file (relative to base_path or absolute)
            encoding: File encoding

        Returns:
            FileResult with file content
        """
        try:
            path = self._resolve_path(file_path)

            if not path.exists():
                return FileResult(success=False, message=f"File not found: {path}")

            content = path.read_text(encoding=encoding)

            return FileResult(
                success=True,
                message=f"Successfully read {len(content)} characters",
                path=str(path),
                content=content,
                metadata={
                    "size": path.stat().st_size,
                    "modified": path.stat().st_mtime,
                    "encoding": encoding,
                },
            )

        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {str(e)}")
            return FileResult(success=False, message=f"Failed to read file: {str(e)}")

    def write_file(
        self,
        file_path: str,
        content: str,
        encoding: str = "utf-8",
        create_dirs: bool = True,
    ) -> FileResult:
        """
        Write content to a file

        Args:
            file_path: Path to the file (relative to base_path or absolute)
            content: Content to write
            encoding: File encoding
            create_dirs: Create parent directories if they don't exist

        Returns:
            FileResult with operation status
        """
        try:
            path = self._resolve_path(file_path)

            if create_dirs:
                path.parent.mkdir(parents=True, exist_ok=True)

            path.write_text(content, encoding=encoding)

            return FileResult(
                success=True,
                message=f"Successfully wrote {len(content)} characters",
                path=str(path),
                metadata={"size": path.stat().st_size, "encoding": encoding},
            )

        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {str(e)}")
            return FileResult(success=False, message=f"Failed to write file: {str(e)}")

    def append_file(
        self, file_path: str, content: str, encoding: str = "utf-8"
    ) -> FileResult:
        """
        Append content to a file

        Args:
            file_path: Path to the file
            content: Content to append
            encoding: File encoding

        Returns:
            FileResult with operation status
        """
        try:
            path = self._resolve_path(file_path)

            if not path.exists():
                return FileResult(success=False, message=f"File not found: {path}")

            with open(path, "a", encoding=encoding) as f:
                f.write(content)

            return FileResult(
                success=True,
                message=f"Successfully appended {len(content)} characters",
                path=str(path),
            )

        except Exception as e:
            logger.error(f"Failed to append to file {file_path}: {str(e)}")
            return FileResult(
                success=False, message=f"Failed to append to file: {str(e)}"
            )

    def delete_file(self, file_path: str) -> FileResult:
        """
        Delete a file

        Args:
            file_path: Path to the file

        Returns:
            FileResult with operation status
        """
        try:
            path = self._resolve_path(file_path)

            if not path.exists():
                return FileResult(success=False, message=f"File not found: {path}")

            path.unlink()

            return FileResult(
                success=True, message=f"Successfully deleted file", path=str(path)
            )

        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {str(e)}")
            return FileResult(success=False, message=f"Failed to delete file: {str(e)}")

    def list_directory(
        self,
        dir_path: str = ".",
        pattern: Optional[str] = None,
        recursive: bool = False,
    ) -> FileResult:
        """
        List files in a directory

        Args:
            dir_path: Path to the directory
            pattern: Glob pattern to filter files (e.g., "*.py")
            recursive: Whether to search recursively

        Returns:
            FileResult with list of files
        """
        try:
            path = self._resolve_path(dir_path)

            if not path.exists() or not path.is_dir():
                return FileResult(success=False, message=f"Directory not found: {path}")

            if recursive:
                files = list(path.rglob(pattern)) if pattern else list(path.rglob("*"))
            else:
                files = list(path.glob(pattern)) if pattern else list(path.glob("*"))

            file_list = []
            for f in files:
                if f.is_file():
                    file_list.append(
                        {
                            "name": f.name,
                            "path": str(f.relative_to(self.base_path)),
                            "size": f.stat().st_size,
                            "is_dir": False,
                        }
                    )
                elif f.is_dir():
                    file_list.append(
                        {
                            "name": f.name,
                            "path": str(f.relative_to(self.base_path)),
                            "is_dir": True,
                        }
                    )

            return FileResult(
                success=True,
                message=f"Found {len(file_list)} items",
                path=str(path),
                content=json.dumps(file_list, indent=2),
                metadata={"count": len(file_list)},
            )

        except Exception as e:
            logger.error(f"Failed to list directory {dir_path}: {str(e)}")
            return FileResult(
                success=False, message=f"Failed to list directory: {str(e)}"
            )

    def create_directory(self, dir_path: str, parents: bool = True) -> FileResult:
        """
        Create a directory

        Args:
            dir_path: Path to the directory
            parents: Create parent directories if needed

        Returns:
            FileResult with operation status
        """
        try:
            path = self._resolve_path(dir_path)
            path.mkdir(parents=parents, exist_ok=True)

            return FileResult(
                success=True, message=f"Successfully created directory", path=str(path)
            )

        except Exception as e:
            logger.error(f"Failed to create directory {dir_path}: {str(e)}")
            return FileResult(
                success=False, message=f"Failed to create directory: {str(e)}"
            )

    def copy_file(self, src_path: str, dst_path: str) -> FileResult:
        """
        Copy a file

        Args:
            src_path: Source file path
            dst_path: Destination file path

        Returns:
            FileResult with operation status
        """
        try:
            src = self._resolve_path(src_path)
            dst = self._resolve_path(dst_path)

            if not src.exists():
                return FileResult(
                    success=False, message=f"Source file not found: {src}"
                )

            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

            return FileResult(
                success=True, message=f"Successfully copied file", path=str(dst)
            )

        except Exception as e:
            logger.error(f"Failed to copy file {src_path} to {dst_path}: {str(e)}")
            return FileResult(success=False, message=f"Failed to copy file: {str(e)}")

    def move_file(self, src_path: str, dst_path: str) -> FileResult:
        """
        Move a file

        Args:
            src_path: Source file path
            dst_path: Destination file path

        Returns:
            FileResult with operation status
        """
        try:
            src = self._resolve_path(src_path)
            dst = self._resolve_path(dst_path)

            if not src.exists():
                return FileResult(
                    success=False, message=f"Source file not found: {src}"
                )

            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))

            return FileResult(
                success=True, message=f"Successfully moved file", path=str(dst)
            )

        except Exception as e:
            logger.error(f"Failed to move file {src_path} to {dst_path}: {str(e)}")
            return FileResult(success=False, message=f"Failed to move file: {str(e)}")

    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists"""
        path = self._resolve_path(file_path)
        return path.exists() and path.is_file()

    def directory_exists(self, dir_path: str) -> bool:
        """Check if a directory exists"""
        path = self._resolve_path(dir_path)
        return path.exists() and path.is_dir()

    def get_file_info(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Get file metadata"""
        try:
            path = self._resolve_path(file_path)
            if not path.exists():
                return None

            stat = path.stat()
            return {
                "name": path.name,
                "path": str(path),
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "is_file": path.is_file(),
                "is_dir": path.is_dir(),
            }
        except Exception:
            return None

    def _resolve_path(self, path_str: str) -> Path:
        """Resolve a path relative to base_path"""
        path = Path(path_str)
        if path.is_absolute():
            return path
        return self.base_path / path
