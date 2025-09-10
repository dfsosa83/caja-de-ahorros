@echo off
echo ================================================================================
echo 🚀 INCOME PREDICTION PRODUCTION ENVIRONMENT SETUP
echo ================================================================================
echo.
echo This script will create a clean environment for your production pipeline
echo.

echo 📋 Step 1: Creating mamba environment...
mamba create -n income-prediction python=3.9 -y

echo.
echo 📋 Step 2: Activating environment...
call mamba activate income-prediction

echo.
echo 📋 Step 3: Installing required packages...
pip install -r requirements_production_pipeline.txt

echo.
echo 📋 Step 4: Testing installation...
python -c "import pandas, numpy, sklearn, xgboost, joblib; print('✅ All packages installed successfully!')"

echo.
echo ================================================================================
echo 🎉 SETUP COMPLETE!
echo ================================================================================
echo.
echo 🚀 To run your production pipeline:
echo    1. mamba activate income-prediction
echo    2. python models/production/00_predictions_pipeline.py
echo.
echo 📋 Your environment is ready for production use!
echo ================================================================================
pause
