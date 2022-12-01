// upgrade pip to its latest version  
python -m pip install --upgrade pip   
  
// install virtualenv  
pip install virtualenv 

// build venv
system_python = $(get-command -all python)
virtualenv venv -p $system_python

// If activate failed.
// set-executionpolicy RemoteSigned to allow scripts to run (mine was set to Restricted
// If you don't have admin privileges, you may need to run set-executionpolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\activate.ps1

if ($(get-command -all python) == $system_python){
  Write-FormattedError -Message "The virtualenv activate failed, please see the file." -Space -Silent:(!$VerbosePreference)
  return
}

pip install -r requirements.txt
