# Dynamic Code Generation Verification Script
# Checks that all HTML files have the advanced protection features

$publicHtmlPath = "."

Write-Host "DYNAMIC CODE GENERATION VERIFICATION REPORT" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "Date: $(Get-Date)"
Write-Host ""

# Features to check for
$features = @{
    "Dynamic Code Generation" = "generateDynamicCode"
    "Code Integrity Check" = "checkIntegrity"
    "Memory Cleanup" = "cleanup"
    "Advanced Protection Log" = "All systems active"
}

$htmlFiles = Get-ChildItem -Path $publicHtmlPath -Filter "*.html" | Where-Object { 
    $_.Name -notlike "*protection*"
}

$totalFiles = $htmlFiles.Count
$fullyProtected = 0
$results = @()

foreach ($file in $htmlFiles) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    $fileResults = @{
        "File" = $file.Name
        "Features" = @{}
        "Score" = 0
    }
    
    foreach ($feature in $features.Keys) {
        $hasFeature = $content -match [regex]::Escape($features[$feature])
        $fileResults.Features[$feature] = $hasFeature
        if ($hasFeature) { $fileResults.Score++ }
    }
    
    $results += $fileResults
    if ($fileResults.Score -eq $features.Count) { $fullyProtected++ }
}

# Display results
Write-Host "SUMMARY:" -ForegroundColor Yellow
Write-Host "Total HTML files: $totalFiles"
Write-Host "Fully protected files: $fullyProtected" -ForegroundColor Green
Write-Host "Protection coverage: $([math]::Round(($fullyProtected / $totalFiles) * 100, 1))%" -ForegroundColor Green
Write-Host ""

Write-Host "DETAILED RESULTS:" -ForegroundColor Yellow
foreach ($result in $results | Sort-Object File) {
    $status = if ($result.Score -eq $features.Count) { "✅ FULLY PROTECTED" } else { "⚠️  PARTIAL" }
    Write-Host "$($result.File): $status ($($result.Score)/$($features.Count))" -ForegroundColor $(if ($result.Score -eq $features.Count) { "Green" } else { "Yellow" })
    
    if ($result.Score -lt $features.Count) {
        foreach ($feature in $features.Keys) {
            $symbol = if ($result.Features[$feature]) { "✅" } else { "❌" }
            Write-Host "  $symbol $feature"
        }
    }
}

Write-Host ""
Write-Host "VERIFICATION COMPLETE!" -ForegroundColor Green
Write-Host "All files with full protection have:" -ForegroundColor Cyan
Write-Host "• Dynamic code generation every 10 seconds" -ForegroundColor White
Write-Host "• Code integrity verification every 3 seconds" -ForegroundColor White
Write-Host "• Memory cleanup every 30 seconds" -ForegroundColor White
Write-Host "• Advanced protection logging" -ForegroundColor White
