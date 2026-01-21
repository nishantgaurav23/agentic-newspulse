@echo off
REM Activation script for NewsPulse AI (Windows)

echo 🚀 Setting up NewsPulse AI...
echo.

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

echo ✓ Virtual environment activated!
echo.

REM Install dependencies
echo 📦 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo You can now run:
echo   python main.py create-profile         # Create a user profile
echo   python main.py generate ^<user_id^>   # Generate a news report
echo.
echo To deactivate the virtual environment later, run: deactivate
