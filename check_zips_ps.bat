@powershell -nologo -noprofile -command "$fd = '%~dp0'; $of = '%~dpn0.csv'; get-content '%~f0' | where {$_ -notlike '@*'} | invoke-expression"
@goto :EOF
#!powershell
$z7 = "$env:programfiles\7-zip\7z.exe"
$fl = get-childitem $fd -filter '*.zip' -file -recurse -ErrorAction silentlycontinue | select -expandproperty FullName
$ec = $fl | % {$ps = start-process -wait -NoNewWindow -passthru $z7 ('t', $_); $ps.ExitCode ; }
$rt = @( 'name,test' )
$fl | % { $i = 0 } { $rt += '{0},{1}' -f $fl[$i],$ec[$i] -replace 0,'pass' -replace 2,'fail' ; $i++ }
$rt
$rt | out-file -Encoding oem $of
Invoke-Item $of
pause