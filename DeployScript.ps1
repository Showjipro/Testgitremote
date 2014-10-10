$server = 'server2-vm27.asl.mum.sst'
#Axway Server Name(target)
$Username = ''  
$Password = ''
#Username and Password of Jenkins/machine(host)
$command = 'C:\Axway-7.2.1\apiserver\samples\scripts\run.bat C:\Axway-7.2.1\apiserver\samples\scripts\deployFed.py --username admin --password changeme --fed C:\Fidelity-Automation\Group1.fed --url https://localhost:8090/api --group API-Server-Group-1'  
#Command to be executed on remote machine(deploy script with absolute path)
$cmd = "CMD.EXE /C " +$command
#Above command to hit the command prompt of the remote machine

$ph = "C:\deployLog.txt"  
$rph = "\\$server\C$\deployLog.txt"  
#Temporary File

$cmde = "$cmd  > $ph"  
$pass = ConvertTo-SecureString -AsPlainText $Password -Force  
$mycred = new-object -typename System.Management.Automation.PSCredential -argumentlist  "$Username",$pass  
$process = Invoke-WmiMethod win32_process -name create -ComputerName $server -ArgumentList $cmde  -Credential $mycred 
Invoke-Command -ComputerName $server -ScriptBlock { param($processId) Wait-Process -ProcessId $processId } -ArgumentList $process.ProcessId  -Credential $mycred 
cmd /c net use \\$server\C$ $password /USER:$username  
Get-Content $rph  
#Retrieve the script/command response from the temporary file
Remove-Item $rph  
#Remove the content
cmd /c net use \\$server\C$ /delete 
#Deletes the temporary file