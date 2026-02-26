@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ========================================
echo    Выполнение миграций Django
echo ========================================
echo.

REM Переходим в корневую папку проекта
cd /d "%~dp0.."
set PROJECT_ROOT=%CD%
echo Корень проекта: %PROJECT_ROOT%

REM Проверка наличия виртуального окружения
if not exist "%PROJECT_ROOT%\venv" (
    echo [ERROR] Виртуальное окружение не найдено!
    echo Сначала выполните scripts\setup.bat
    pause
    exit /b 1
)

REM Активация виртуального окружения
echo [1/4] Активация виртуального окружения...
call "%PROJECT_ROOT%\venv\Scripts\activate.bat"
if !errorlevel! neq 0 (
    echo [ERROR] Ошибка при активации виртуального окружения
    pause
    exit /b 1
)
echo [OK] Виртуальное окружение активировано

REM Проверка наличия manage.py
if not exist "%PROJECT_ROOT%\manage.py" (
    echo [ERROR] Файл manage.py не найден в корне проекта!
    pause
    exit /b 1
)

REM Применение миграций
echo [3/4] Применение миграций...
python manage.py migrate
if !errorlevel! neq 0 (
    echo [ERROR] Ошибка при применении миграций
    pause
    exit /b 1
)
echo [OK] Миграции применены

echo.
echo ========================================
echo    Миграции выполнены успешно!
echo ========================================
echo.