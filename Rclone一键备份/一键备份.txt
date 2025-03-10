@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM 定义源目录和备份目录路径（请根据实际情况修改）注意请先rclone登陆webdav;
REM 示例：
REM   set "SOURCE_DIR=Alist:/localDev"       -> 源目录
REM   set "BACKUP_DIR=Alist:/localDev_Backup" -> 备份目录
REM ============================================================
set "SOURCE_DIR=Alist:/localDev"
set "BACKUP_DIR=Alist:/localDev_Backup"

echo 正在访问Alist存储...
echo ----------------------------

REM 检查源目录是否存在
echo 正在检查源目录 %SOURCE_DIR%...
rclone lsf "%SOURCE_DIR%" --max-depth 1 >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 源目录 %SOURCE_DIR% 不存在！
    choice /m "是否创建源目录？(Y/N)"
    if %errorlevel% equ 1 (
        rclone mkdir "%SOURCE_DIR%"
        if %errorlevel% equ 0 (
            echo 源目录 %SOURCE_DIR% 已创建
        ) else (
            echo [错误] 无法创建源目录
            goto :eof
        )
    ) else (
        echo 用户取消操作，脚本退出
        goto :eof
    )
)

REM 检查目标目录是否存在
echo 正在检查目标目录 %BACKUP_DIR%...
rclone lsf "%BACKUP_DIR%" --max-depth 1 >nul 2>&1
if %errorlevel% neq 0 (
    echo [警告] 目标目录 %BACKUP_DIR% 不存在！
    choice /m "是否创建目标目录？(Y/N)"
    if %errorlevel% equ 1 (
        rclone mkdir "%BACKUP_DIR%"
        if %errorlevel% equ 0 (
            echo 目标目录 %BACKUP_DIR% 已创建
        ) else (
            echo [错误] 无法创建目标目录
            goto :eof
        )
    ) else (
        echo 用户取消操作，脚本退出
        goto :eof
    )
)

echo ----------------------------
echo 正在检测文件差异...

REM 使用rclone check检测文件差异
rclone check "%SOURCE_DIR%" "%BACKUP_DIR%" ^
    --size-only ^
    --one-way ^
    --combined - ^
    --error-on-no-transfer ^
    --progress

if %errorlevel% equ 0 (
    echo ----------------------------
    echo 检测完成：源和目标目录文件一致
    goto :eof
)

echo ----------------------------
echo 正在同步更新文件...

REM 同步更新文件（覆盖旧文件）
rclone sync "%SOURCE_DIR%" "%BACKUP_DIR%" ^
    --update ^
    --progress ^
    --transfers 10 ^
    --retries 3

if %errorlevel% equ 0 (
    echo ----------------------------
    echo 同步完成：已更新目标目录中的旧文件
) else (
    echo ----------------------------
    echo [警告] 同步过程中出现错误，请检查输出信息
)

endlocal
pause