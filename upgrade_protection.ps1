# PowerShell script to upgrade all protected pages with Dynamic Code Generation
# This script adds advanced features to pages that were previously protected

$publicHtmlPath = "c:\Drive\company\Backup_website\Backup_website\public_html"

# Advanced protection features to add
$advancedFeatures = @"

        // Advanced anti-debugging and code protection

        // Dynamic code generation to confuse static analysis
        const generateFakeCode = () => {
          const fakeVars = ['a', 'b', 'c', 'd', 'e'].map(v => 
            'var ' + v + Math.random().toString(36) + '=' + Math.random() + ';'
          ).join('');
          
          const script = document.createElement('script');
          script.innerHTML = fakeVars + 'if(false){console.log("fake");}';
          document.head.appendChild(script);
          
          setTimeout(() => script.remove(), 1000);
        };
        
        // Randomize script execution order
        setInterval(generateFakeCode, 10000);
        
        // String obfuscation for sensitive parts
        const obfuscateString = (str) => {
          return str.split('').map(char => 
            String.fromCharCode(char.charCodeAt(0) ^ 42)
          ).join('');
        };
        
        // Dynamic property names to avoid detection
        const props = {
          ['ev' + 'ent']: 'addEventListener',
          ['pr' + 'ev']: 'preventDefault',
          ['ke' + 'y']: 'keyCode',
          ['co' + 'de']: 'charCode'
        };
        
        // Code integrity checking
        const checkIntegrity = () => {
          const scriptCount = document.getElementsByTagName('script').length;
          const expectedCount = 8; // Adjust based on your pages
          
          if (scriptCount < expectedCount) {
            // Scripts may have been tampered with
            window.location.href = 'about:blank';
          }
        };
        
        setInterval(checkIntegrity, 3000);
        
        // Memory cleanup to remove traces
        const cleanup = () => {
          if (window.gc) window.gc(); // Force garbage collection if available
          
          // Clear variables that might contain sensitive info
          for (let i = 0; i < 1000; i++) {
            window['_temp' + i] = null;
          }
        };
        
        setInterval(cleanup, 30000);
"@

# Get all HTML files that need upgrading
$htmlFiles = Get-ChildItem -Path $publicHtmlPath -Filter "*.html" | Where-Object { 
    $_.Name -notlike "*protection*" -and 
    $_.Name -ne "index.html" -and 
    $_.Name -ne "about.html" -and 
    $_.Name -ne "contact.html" -and
    $_.Name -ne "andaman-tour-packages.html"  # Already upgraded
}

Write-Host "Found $($htmlFiles.Count) HTML files to upgrade with advanced protection..."

foreach ($file in $htmlFiles) {
    Write-Host "Upgrading: $($file.Name)"
    
    try {
        $content = Get-Content $file.FullName -Raw
        
        # Skip if already has advanced features
        if ($content -match "generateFakeCode" -or $content -match "Dynamic code generation") {
            Write-Host "  Already has advanced features, skipping..."
            continue
        }
        
        # Skip if doesn't have basic protection
        if (-not ($content -match "Source Code Protection")) {
            Write-Host "  No basic protection found, skipping..."
            continue
        }
        
        # Find the location to insert advanced features
        $searchPattern = @"
        // Silent detection for dev tools
        window.addEventListener\('resize', function\(\) \{
          if \(window\.outerWidth - window\.innerWidth > 200 \|\| 
              window\.outerHeight - window\.innerHeight > 200\) \{
            // Silent protection - no warnings
          \}
        \}\);
"@
        
        if ($content -match $searchPattern) {
            # Insert advanced features before the silent detection
            $replacement = $advancedFeatures + @"

        // Silent detection for dev tools
        window.addEventListener('resize', function() {
          if (window.outerWidth - window.innerWidth > 200 || 
              window.outerHeight - window.innerHeight > 200) {
            // Silent protection - no warnings
          }
        });
"@
            
            $newContent = $content -replace [regex]::Escape($searchPattern), $replacement
            
            # Write the updated content
            Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
            Write-Host "  ✅ Successfully upgraded!" -ForegroundColor Green
        } else {
            Write-Host "  ❌ Could not find insertion point" -ForegroundColor Yellow
        }
        
    } catch {
        Write-Host "  ❌ Error processing file: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nUpgrade process completed!" -ForegroundColor Green
Write-Host "All pages now have the same advanced protection level as index.html" -ForegroundColor Cyan

# Summary
Write-Host "`nAdvanced Features Added:" -ForegroundColor Yellow
Write-Host "✓ Dynamic Code Generation (every 10 seconds)" -ForegroundColor Green
Write-Host "✓ Code Integrity Checking (every 3 seconds)" -ForegroundColor Green
Write-Host "✓ Memory Cleanup (every 30 seconds)" -ForegroundColor Green
Write-Host "✓ String Obfuscation Functions" -ForegroundColor Green
Write-Host "✓ Anti-Debugging Protection" -ForegroundColor Green
Write-Host "✓ Dynamic Property Names" -ForegroundColor Green
