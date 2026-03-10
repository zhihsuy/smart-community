@echo off
chcp 65001 >nul
echo ==========================================
echo    智慧社区用户服务启动脚本
echo ==========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [1/3] Python版本:
python --version
echo.

REM 检查虚拟环境
if not exist "venv" (
    echo [2/3] 创建虚拟环境...
    python -m venv venv
) else (
    echo [2/3] 虚拟环境已存在
)

REM 激活虚拟环境
echo [2/3] 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo [3/3] 安装依赖...
pip install -r requirements.txt -q

echo.
echo ==========================================
echo    启动用户服务...
echo ==========================================
echo 服务地址: http://localhost:8081
echo.
echo API接口:
echo   - 健康检查: GET http://localhost:8081/health
echo   - 用户注册: POST http://localhost:8081/api/v1/pc/auth/register
echo   - 用户登录: POST http://localhost:8081/api/v1/pc/auth/login
echo   - 获取用户信息: GET http://localhost:8081/api/v1/pc/user/info
echo   - 更新用户信息: PUT http://localhost:8081/api/v1/pc/user/update
echo   - 获取楼栋列表: GET http://localhost:8081/api/v1/pc/building/list
echo.
echo 按 Ctrl+C 停止服务
echo ==========================================
python app.py

pause
