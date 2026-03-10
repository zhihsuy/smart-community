@echo off
chcp 65001
title 垃圾分类AI服务

echo ========================================
echo   垃圾分类AI服务启动
echo ========================================
echo.

echo [1/3] 检查Python环境...
python --version
if %errorlevel% neq 0 (
    echo [错误] Python未安装或不在PATH中
    pause
    exit /b 1
)
echo [成功] Python环境正常
echo.

echo [2/3] 安装依赖包...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo [成功] 依赖安装完成
echo.

echo [3/3] 启动AI服务...
echo.
echo 服务信息:
echo   - 服务名称: 垃圾分类AI服务
echo   - 模型类型: YOLOv8
echo   - API地址: http://localhost:8082
echo   - 主要接口:
echo     * POST /api/v1/ai/garbage-classify (图片文件上传)
echo     * POST /api/v1/ai/garbage-classify-base64 (Base64编码)
echo     * GET  /api/v1/ai/model-info (模型信息)
echo.
echo ========================================
echo 按Ctrl+C停止服务
echo ========================================
echo.

python app.py

pause
