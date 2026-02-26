@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ========================================
echo    Установка виртуального окружения
echo ========================================
echo.

REM Переходим в корневую папку проекта (на уровень выше scripts)
cd /d "%~dp0.."
set PROJECT_ROOT=%CD%
echo Корень проекта: %PROJECT_ROOT%

REM Проверяем наличие папки venv
if exist "%PROJECT_ROOT%\venv" (
    echo [OK] Виртуальное окружение уже существует
) else (
    echo [1/3] Создание виртуального окружения...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo [ERROR] Ошибка при создании виртуального окружения
        pause
        exit /b 1
    )
    echo [OK] Виртуальное окружение создано
)

REM Активация виртуального окружения
echo [2/3] Активация виртуального окружения...
call "%PROJECT_ROOT%\venv\Scripts\activate.bat"
if !errorlevel! neq 0 (
    echo [ERROR] Ошибка при активации виртуального окружения
    pause
    exit /b 1
)
echo [OK] Виртуальное окружение активировано

REM Обновление pip
REM echo [3/3] Обновление pip...
REM python -m pip install --upgrade pip
REM if !errorlevel! neq 0 (
REM    echo [ERROR] Ошибка при обновлении pip
REM    pause
REM    exit /b 1
REM)

REM Установка зависимостей
echo.
echo ========================================
echo    Установка зависимостей
echo ========================================
echo.

if exist "%PROJECT_ROOT%\requirements.txt" (
    echo [1/1] Установка пакетов из requirements.txt...
    pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo [ERROR] Ошибка при установке зависимостей
        pause
        exit /b 1
    )
    echo [OK] Все зависимости установлены
) else (
    echo [WARNING] Файл requirements.txt не найден
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Установка завершена успешно!
echo ========================================
echo.
echo Для активации виртуального окружения вручную выполните:
echo %PROJECT_ROOT%\venv\Scripts\activate.bat
echo.