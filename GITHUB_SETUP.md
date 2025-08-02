# GitHub Backup Setup Commands

## After installing Git from https://git-scm.com/download/windows

# 1. Configure Git (replace with your info)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 2. Initialize repository
git init

# 3. Add all files
git add .

# 4. Create initial commit
git commit -m "Initial commit: FolderPulse v1.0 - Modern GUI with animated splash"

# 5. Create GitHub repo at https://github.com/new
# Repository name: FolderPulse
# Description: Intelligent folder management and cleanup tool
# Public or Private (your choice)
# Don't initialize with README

# 6. Connect to GitHub (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/FolderPulse.git
git branch -M main
git push -u origin main

## Future updates
# After making changes:
git add .
git commit -m "Description of changes"
git push

## To backup from another computer:
git clone https://github.com/yourusername/FolderPulse.git
