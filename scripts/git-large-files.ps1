Write-Output "Listing all blobs (object ids and paths) - may be heavy:" 
git rev-list --objects --all | Sort-Object -Property 2

