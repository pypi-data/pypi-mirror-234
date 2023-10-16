
#
# This script installs IOCBio gel program to python virtual environment iocbio-gel
#

$rname = 'iocbio-gel_requirements.txt'
Invoke-WebRequest -Uri 'https://gitlab.com/iocbio/gel/-/raw/main/requirements.txt' -OutFile $rname

python.exe -m venv iocbio-gel
Write-Output "Python virtual environment for iocbio-gel created"
Write-Output ""

# Upgrading pip
.\iocbio-gel\Scripts\python.exe -m pip install --upgrade pip

.\iocbio-gel\Scripts\pip install pip install msvc-runtime

.\iocbio-gel\Scripts\pip install -r $rname
Remove-Item $rname
.\iocbio-gel\Scripts\pip install iocbio.gel

Write-Output ""
Write-Output "IOCBio-gel installed"
Write-Output ""
Write-Output "To run the program use following commands"
Write-Output ".\iocbio-gel\Scripts\Activate.ps1"
Write-Output "iocbio-gel.exe"
