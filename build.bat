@echo off
chcp 65001 >nul
echo ========================================
echo   自动化工具箱 - 打包脚本 (customtkinter)
echo ========================================
echo.

echo [1/3] 清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
del *.spec 2>nul
echo.

echo [2/3] 检查依赖...
python -c "import customtkinter" 2>nul
if errorlevel 1 (
    echo 正在安装 customtkinter...
    pip install customtkinter -i https://pypi.tuna.tsinghua.edu.cn/simple
)
python -c "import CTkTable" 2>nul
if errorlevel 1 (
    echo 正在安装 CTkTable...
    pip install CTkTable -i https://pypi.tuna.tsinghua.edu.cn/simple
)
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
)
echo.

echo [3/3] 开始打包（包含 customtkinter 和 CTkTable）...
python -m PyInstaller --onefile --windowed --name="Toolbox" --hidden-import=customtkinter --hidden-import=CTkTable main.py

echo.
echo 重命名 exe 文件...
if exist "dist\Toolbox.exe" (
    ren "dist\Toolbox.exe" "自动化工具箱.exe"
    echo 重命名成功！
)

echo.
echo ========================================
echo   打包完成！exe 文件位于 dist/ 目录下
echo ========================================
pause