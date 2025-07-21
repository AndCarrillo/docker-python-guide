# 🛠️ Git Workflow Commands

This guide includes commands for both Unix/Linux/macOS (Bash) and Windows (PowerShell).

## 🏁 Initial Setup

### Unix/Linux/macOS (Bash):
```bash
# Clone the repository
git clone https://github.com/AndCarrillo/docker-python-guide.git
cd docker-python-guide

# Verify all branches exist
git branch -a
```

### Windows (PowerShell):
```powershell
# Clone the repository
git clone https://github.com/AndCarrillo/docker-python-guide.git
Set-Location docker-python-guide

# Verify all branches exist
git branch -a
```

---

## 📚 Working with Modules

### Starting a Module

#### Unix/Linux/macOS (Bash):
```bash
# Update main branch
git checkout main && git pull origin main

# Switch to module branch
git checkout module-01-containerize

# Verify you're on the correct branch
git branch --show-current
```

#### Windows (PowerShell):
```powershell
# Update main branch
git checkout main; git pull origin main

# Switch to module branch  
git checkout module-01-containerize

# Verify you're on the correct branch
git branch --show-current
```

### Creating Personal Experiments

#### Unix/Linux/macOS (Bash):
```bash
# Create personal branch from module branch
git checkout module-01-containerize
git checkout -b my-experiments-01

# Or create from main
git checkout main
git checkout -b my-feature-experiment
```

#### Windows (PowerShell):
```powershell
# Create personal branch from module branch
git checkout module-01-containerize
git checkout -b my-experiments-01

# Or create from main
git checkout main  
git checkout -b my-feature-experiment
```

---

## 🔄 Contributing Changes

### Before Making Changes

#### Unix/Linux/macOS (Bash):
```bash
# Always start with updated main
git checkout main && git pull origin main

# Create feature branch
git checkout -b feature/improve-module-01

# Or create from specific module
git checkout module-01-containerize
git checkout -b feature/fix-dockerfile-example
```

#### Windows (PowerShell):
```powershell
# Always start with updated main
git checkout main; git pull origin main

# Create feature branch
git checkout -b feature/improve-module-01

# Or create from specific module
git checkout module-01-containerize
git checkout -b feature/fix-dockerfile-example
```

### Making and Committing Changes

#### Unix/Linux/macOS (Bash):
```bash
# Check status
git status

# Add specific files
git add README.md examples/flask-app/

# Or add all changes (be careful)
git add .

# Commit with descriptive message
git commit -m "docs: improve Flask containerization examples

- Add production-ready Dockerfile
- Include security best practices  
- Update documentation with troubleshooting section"

# Push to your branch
git push origin feature/improve-module-01
```

#### Windows (PowerShell):
```powershell
# Check status
git status

# Add specific files
git add README.md examples/flask-app/

# Or add all changes (be careful)
git add .

# Commit with descriptive message
git commit -m "docs: improve Flask containerization examples

- Add production-ready Dockerfile
- Include security best practices
- Update documentation with troubleshooting section"

# Push to your branch
git push origin feature/improve-module-01
```

---

## 🎯 Branch Management

### List and Navigate Branches

#### Unix/Linux/macOS (Bash):
```bash
# List all local branches
git branch

# List all branches (including remote)
git branch -a

# Switch between branches
git checkout main
git checkout module-02-develop
git checkout module-03-linting-typing
```

#### Windows (PowerShell):
```powershell
# List all local branches
git branch

# List all branches (including remote)
git branch -a

# Switch between branches
git checkout main
git checkout module-02-develop  
git checkout module-03-linting-typing
```

### Clean Up Branches

#### Unix/Linux/macOS (Bash):
```bash
# Delete local branch (safe)
git branch -d feature/completed-feature

# Force delete local branch
git branch -D feature/unwanted-feature

# Delete remote branch
git push origin --delete feature/completed-feature

# Prune remote tracking branches
git remote prune origin
```

#### Windows (PowerShell):
```powershell
# Delete local branch (safe)
git branch -d feature/completed-feature

# Force delete local branch
git branch -D feature/unwanted-feature

# Delete remote branch
git push origin --delete feature/completed-feature

# Prune remote tracking branches
git remote prune origin
```

---

## 🔧 Useful Utilities

### PowerShell Functions (Windows Only)

Add these to your PowerShell profile for easier navigation:

```powershell
# Add to $PROFILE (Microsoft.PowerShell_profile.ps1)

function Switch-DockerGuideModule {
    param([string]$ModuleNumber)
    
    $modules = @{
        "1" = "module-01-containerize"
        "2" = "module-02-develop"  
        "3" = "module-03-linting-typing"
        "4" = "module-04-cicd"
        "5" = "module-05-deployment"
    }
    
    if ($modules.ContainsKey($ModuleNumber)) {
        git checkout $modules[$ModuleNumber]
        Write-Host "Switched to module: $($modules[$ModuleNumber])" -ForegroundColor Green
    } else {
        Write-Host "Available modules: 1, 2, 3, 4, 5" -ForegroundColor Yellow
    }
}

# Usage: Switch-DockerGuideModule 1
Set-Alias -Name sgm -Value Switch-DockerGuideModule

function Update-DockerGuideMain {
    $currentBranch = git branch --show-current
    git checkout main
    git pull origin main
    git checkout $currentBranch
    Write-Host "Main branch updated. Back to: $currentBranch" -ForegroundColor Green
}

# Usage: Update-DockerGuideMain
Set-Alias -Name ugm -Value Update-DockerGuideMain
```

### Bash Functions (Unix/Linux/macOS Only)

Add these to your `.bashrc` or `.zshrc`:

```bash
# Docker Guide utilities

# Switch to module branch
sgm() {
    case $1 in
        1) git checkout module-01-containerize ;;
        2) git checkout module-02-develop ;;
        3) git checkout module-03-linting-typing ;;
        4) git checkout module-04-cicd ;;
        5) git checkout module-05-deployment ;;
        *) echo "Available modules: 1, 2, 3, 4, 5" ;;
    esac
    
    if [ $? -eq 0 ]; then
        echo "Switched to module: $(git branch --show-current)"
    fi
}

# Update main branch
ugm() {
    local current_branch=$(git branch --show-current)
    git checkout main && git pull origin main && git checkout "$current_branch"
    echo "Main branch updated. Back to: $current_branch"
}
```

---

## 📋 Common Workflows

### Daily Development Routine

#### Unix/Linux/macOS (Bash):
```bash
# 1. Start day: update main
git checkout main && git pull origin main

# 2. Continue work on feature
git checkout feature/my-work

# 3. Merge latest main (if needed)
git merge main

# 4. Work and commit
# ... make changes ...
git add . && git commit -m "feat: add new examples"

# 5. Push work
git push origin feature/my-work
```

#### Windows (PowerShell):
```powershell
# 1. Start day: update main
git checkout main; git pull origin main

# 2. Continue work on feature
git checkout feature/my-work

# 3. Merge latest main (if needed)
git merge main

# 4. Work and commit
# ... make changes ...
git add .; git commit -m "feat: add new examples"

# 5. Push work  
git push origin feature/my-work
```

### Module Review Routine

#### Unix/Linux/macOS (Bash):
```bash
# 1. Check out module
git checkout module-01-containerize

# 2. Create review branch
git checkout -b review/module-01-$(date +%Y%m%d)

# 3. Test examples
cd examples/basic-flask-app/
docker build -t test-app .

# 4. Document findings
# ... edit files ...

# 5. Commit review
git add . && git commit -m "review: test module 01 examples and update docs"
```

#### Windows (PowerShell):
```powershell
# 1. Check out module
git checkout module-01-containerize

# 2. Create review branch
$date = Get-Date -Format "yyyyMMdd"
git checkout -b "review/module-01-$date"

# 3. Test examples
Set-Location examples/basic-flask-app/
docker build -t test-app .

# 4. Document findings
# ... edit files ...

# 5. Commit review
git add .; git commit -m "review: test module 01 examples and update docs"
```

---

## 🚨 Emergency Commands

### Undo Last Commit (Before Push)

#### Unix/Linux/macOS (Bash):
```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, discard changes  
git reset --hard HEAD~1
```

#### Windows (PowerShell):
```powershell
# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, discard changes
git reset --hard HEAD~1
```

### Discard Local Changes

#### Unix/Linux/macOS (Bash):
```bash
# Discard changes to specific file
git checkout -- filename.txt

# Discard all changes
git reset --hard HEAD

# Clean untracked files
git clean -fd
```

#### Windows (PowerShell):
```powershell
# Discard changes to specific file
git checkout -- filename.txt

# Discard all changes
git reset --hard HEAD

# Clean untracked files
git clean -fd
```

### Sync Fork (If Repository is Forked)

#### Unix/Linux/macOS (Bash):
```bash
# Add upstream remote (once)
git remote add upstream https://github.com/AndCarrillo/docker-python-guide.git

# Sync with upstream
git checkout main
git fetch upstream
git merge upstream/main
git push origin main
```

#### Windows (PowerShell):
```powershell
# Add upstream remote (once)
git remote add upstream https://github.com/AndCarrillo/docker-python-guide.git

# Sync with upstream
git checkout main
git fetch upstream  
git merge upstream/main
git push origin main
```

---

## 📖 Additional Resources

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [PowerShell Git Integration](https://docs.microsoft.com/en-us/powershell/scripting/dev-cross-plat/vscode/using-vscode)
- [Bash Git Completion](https://github.com/git/git/blob/master/contrib/completion/git-completion.bash)
