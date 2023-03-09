$DebugPreference = "Continue"
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'Continue'
# Set-PSDebug -Strict -Trace 1
Set-PSDebug -Off
Set-StrictMode -Version 'Latest' -ErrorAction 'Stop' -Verbose

New-Variable -Name curdir  -Option Constant -Value $PSScriptRoot
Write-Host "[INFO] curdir: $curdir"

New-Variable -Name rmq_version -Option Constant -Value '3.11.10'
New-Variable -Name rmq_dir -Option Constant -Value (Join-Path -Path $curdir -ChildPath "rabbitmq_server-$rmq_version")
New-Variable -Name rmq_base_dir -Option Constant -Value (Join-Path -Path $curdir -ChildPath 'rabbitmq')

try
{
    $env:RABBITMQ_BASE = $rmq_base_dir
    & "$rmq_dir/sbin/rabbitmqctl.bat" shutdown
}
finally
{
    Remove-Item -Path env:\RABBITMQ_BASE
}
