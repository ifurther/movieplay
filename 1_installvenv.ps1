$system_python = $(get-command -all python)[0]

## update pip to latest version
Write-Host "Upgrading pip"
python -m pip install --upgrade pip

## install virtualenv
Write-Host "Installing virtualenv"
python -m pip install virtualenv

## build venv
virtualenv venv -p ${system_python}

Write-Host "Reload environment variables"
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
Write-Host "Reloaded environment variables"

## If activate failed.
## set-executionpolicy RemoteSigned to allow scripts to run (mine was set to Restricted
## If you don't have admin privileges, you may need to run set-executionpolicy RemoteSigned -Scope CurrentUser
. .\venv\Scripts\activate.ps1

if ( $((get-command python)) -eq ${system_python}){
  Write-FormattedError -Message "The virtualenv activate failed, please see the file." -Space -Silent:(!$VerbosePreference)
  return
}

pip install -r requirements.txt
