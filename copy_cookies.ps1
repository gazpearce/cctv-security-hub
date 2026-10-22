$src = 'C:\Users\Gary\AppData\Local\Google\Chrome\User Data\Default\Network\Cookies'
$dst = 'C:\Users\Gary\.chrome_automated_agent\Default\Network\Cookies'
[System.IO.Directory]::CreateDirectory('C:\Users\Gary\.chrome_automated_agent\Default\Network') | Out-Null
$srcStream = [System.IO.File]::Open($src, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read, [System.IO.FileShare]::ReadWrite)
$dstStream = [System.IO.File]::Create($dst)
$srcStream.CopyTo($dstStream)
$srcStream.Close()
$dstStream.Close()
Write-Host "Copied locked Cookies successfully! Size: $((Get-Item $dst).Length) bytes"
