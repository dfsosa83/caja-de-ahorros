@echo off
echo 📦 Creating Income Prediction API Sharing Package...
echo.

REM Navigate to project root
cd /d "%~dp0\.."

REM Create sharing directory
if exist "sharing_package" rmdir /s /q sharing_package
mkdir sharing_package

echo ✅ Copying API service files...
xcopy /e /i api-service sharing_package\api-service

echo ✅ Copying production models...
mkdir sharing_package\models\production
copy models\production\final_production_model_nested_cv.pkl sharing_package\models\production\

echo ✅ Copying required data files...
mkdir sharing_package\data\processed
copy data\processed\*.csv sharing_package\data\processed\ 2>nul

echo ✅ Copying documentation...
copy README.md sharing_package\
copy api-service\SHARING_GUIDE.md sharing_package\

echo ✅ Creating partner setup script...
echo @echo off > sharing_package\START_API.bat
echo echo 🚀 Starting Income Prediction API... >> sharing_package\START_API.bat
echo echo. >> sharing_package\START_API.bat
echo cd api-service >> sharing_package\START_API.bat
echo docker-compose up --build >> sharing_package\START_API.bat
echo pause >> sharing_package\START_API.bat

echo ✅ Creating zip package...
powershell -command "Compress-Archive -Path 'sharing_package\*' -DestinationPath 'income-prediction-api-package.zip' -Force"

echo.
echo 🎉 Package created successfully!
echo 📁 File: income-prediction-api-package.zip
echo 📊 Size: 
dir income-prediction-api-package.zip | findstr /C:"income-prediction-api-package.zip"
echo.
echo 📋 Share this zip file with your partner
echo 💡 They just need to extract and run START_API.bat
echo.
pause
