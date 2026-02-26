@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ========================================
echo    Запуск Django сервера
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
echo [1/3] Активация виртуального окружения...
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

REM Запрос параметров запуска
set /p PORT="[2/3] Введите порт для запуска (по умолчанию 8000): "
if "%PORT%"=="" set PORT=8000

set /p HOST="[3/3] Введите хост для запуска (по умолчанию 127.0.0.1): "
if "%HOST%"=="" set HOST=127.0.0.1

echo.
echo ========================================
echo    Запуск сервера на %HOST%:%PORT%
echo ========================================
echo.
echo Для остановки сервера нажмите Ctrl+C
echo.

REM Запуск сервера
python manage.py runserver %HOST%:%PORT%

REM Этот код выполнится после остановки сервера
echo.
echo Сервер остановлен.
