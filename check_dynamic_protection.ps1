# Dynamic Protection Verification Script
# Checks if all HTML files have complete dynamic code generation protection

$publicHtmlPath = "."

# Colors for output
$colorSuccess = "Green"
$colorWarning = "Yellow"
$colorError = "Red"
$colorInfo = "Cyan"
$colorHeader = "Magenta"

Write-Host "=== DYNAMIC PROTECTION STATUS CHECKER ===" -ForegroundColor $colorHeader
Write-Host "Scanning HTML files for dynamic code generation features..." -ForegroundColor $colorInfo
Write-Host ""

# Features to check for
$requiredFeatures = @{
    "generateDynamicCode" = "Dynamic Code Generation System"
    "checkIntegrity" = "Code Integrity Verification"
    "cleanup" = "Memory Cleanup System"
    "setInterval.*generateDynamicCode" = "Dynamic Code Execution Timer"
    "setInterval.*checkIntegrity" = "Integrity Check Timer"
    "setInterval.*cleanup" = "Cleanup Timer"
    "Advanced Protection.*All systems active" = "Initialization Confirmation"
}

# Get all HTML files
$htmlFiles = Get-ChildItem -Path $publicHtmlPath -Filter "*.html" | Where-Object { 
    $_.Name -notlike "*protection*" -and 
    $_.Name -notlike "*temp*"
}

$totalFiles = $htmlFiles.Count
$protectedFiles = 0
$goaFiles = 0

Write-Host "Found $totalFiles HTML files to check" -ForegroundColor $colorInfo
Write-Host ("=" * 80)

foreach ($file in $htmlFiles) {
    $fileName = $file.Name
    $isGoaFile = $fileName -match "goa|Goa|GOA"
    
    if ($isGoaFile) {
        $goaFiles++
        Write-Host "`n🌴 GOA FILE: $fileName" -ForegroundColor $colorHeader
    } else {
        Write-Host "`n📄 FILE: $fileName" -ForegroundColor White
    }
    
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        
        # Check basic protection first
        $hasBasicProtection = $content -match "Advanced source code protection"
        
        if (-not $hasBasicProtection) {
            Write-Host "  ❌ No basic protection found" -ForegroundColor $colorError
            continue
        }
        
        # Check each required feature
        $featureResults = @{}
        $allFeaturesPresent = $true
        
        foreach ($feature in $requiredFeatures.Keys) {
            $featureName = $requiredFeatures[$feature]
            $isPresent = $content -match $feature
            $featureResults[$featureName] = $isPresent
            
            if ($isPresent) {
                Write-Host "  ✅ $featureName" -ForegroundColor $colorSuccess
            } else {
                Write-Host "  ❌ $featureName" -ForegroundColor $colorError
                $allFeaturesPresent = $false
            }
        }
        
        # Overall status
        if ($allFeaturesPresent) {
            Write-Host "  🛡️  FULLY PROTECTED" -ForegroundColor $colorSuccess
            $protectedFiles++
        } else {
            Write-Host "  ⚠️  INCOMPLETE PROTECTION" -ForegroundColor $colorWarning
        }
        
        # Additional checks for Goa files
        if ($isGoaFile) {
            # Check for protection overlays
            $hasDevToolsWarning = $content -match "dev-tools-warning"
            $hasProtectionOverlay = $content -match "protectionOverlay"
            
            if ($hasDevToolsWarning -and $hasProtectionOverlay) {
                Write-Host "  ✅ Protection Overlays Present" -ForegroundColor $colorSuccess
            } else {
                Write-Host "  ❌ Missing Protection Overlays" -ForegroundColor $colorError
            }
            
            # Check CSS protection
            $hasCSSProtection = $content -match "user-select.*none"
            if ($hasCSSProtection) {
                Write-Host "  ✅ CSS Protection Active" -ForegroundColor $colorSuccess
            } else {
                Write-Host "  ❌ Missing CSS Protection" -ForegroundColor $colorError
            }
        }
        
    } catch {
        Write-Host "  ❌ Error reading file: $($_.Exception.Message)" -ForegroundColor $colorError
    }
}

# Summary Report
Write-Host "`n" + ("=" * 80)
Write-Host "📊 SUMMARY REPORT" -ForegroundColor $colorHeader
Write-Host ("=" * 80)
Write-Host "Total HTML files scanned: $totalFiles" -ForegroundColor $colorInfo
Write-Host "Goa-related files found: $goaFiles" -ForegroundColor $colorInfo
Write-Host "Fully protected files: $protectedFiles" -ForegroundColor $colorSuccess
Write-Host "Protection coverage: $(($protectedFiles / $totalFiles * 100).ToString('F1'))%" -ForegroundColor $colorInfo

if ($protectedFiles -eq $totalFiles) {
    Write-Host "`n🎉 ALL FILES ARE FULLY PROTECTED!" -ForegroundColor $colorSuccess
} elseif ($protectedFiles -gt 0) {
    Write-Host "`n⚠️  PARTIAL PROTECTION - Some files need upgrading" -ForegroundColor $colorWarning
} else {
    Write-Host "`n❌ NO PROTECTION FOUND - Run protection script first" -ForegroundColor $colorError
}

# Specific Goa files check
Write-Host "`n🌴 GOA FILES SPECIFIC CHECK:" -ForegroundColor $colorHeader
$goaFileNames = @(
    "goa-tour-packages.html",
    "goa-tour-package-4D-3N.html", 
    "goa-tour-package-4N-5D.html",
    "goa-weekend-trip.html",
    "Hot-Air-Balloon-Goa.html",
    "Watersport-Scuba-combo-goa.html"
)

foreach ($goaFileName in $goaFileNames) {
    $filePath = Join-Path $publicHtmlPath $goaFileName
    if (Test-Path $filePath) {
        $content = Get-Content $filePath -Raw -Encoding UTF8
        $hasComplete = ($content -match "generateDynamicCode") -and 
                      ($content -match "checkIntegrity") -and 
                      ($content -match "cleanup") -and
                      ($content -match "setInterval.*generateDynamicCode")
        
        if ($hasComplete) {
            Write-Host "  ✅ $goaFileName - COMPLETE" -ForegroundColor $colorSuccess
        } else {
            Write-Host "  ❌ $goaFileName - INCOMPLETE" -ForegroundColor $colorError
        }
    } else {
        Write-Host "  ⚠️  $goaFileName - FILE NOT FOUND" -ForegroundColor $colorWarning
    }
}

Write-Host "`n✨ Check completed!" -ForegroundColor $colorSuccess
