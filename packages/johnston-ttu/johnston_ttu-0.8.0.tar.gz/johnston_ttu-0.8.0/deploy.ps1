Write-Host "==================================================================="
Write-Host "DEPLOYING JOHNSTON_TTU PACKAGE"
Write-Host "==================================================================="
Write-Host "BUILDING PACKAGE"
py -m build
Write-Host "==================================================================="
write-Host "UPLOADING PACKAGE"
py -m twine upload --repository pypi dist/*
Write-Host "==================================================================="
Write-Host "REMOVING DIST FOLDER"
Remove-Item -r -Force dist
Write-Host "==================================================================="