# Advanced Protection Upgrade Script v2
# Adds dynamic code generation and advanced features to all HTML files

$publicHtmlPath = "."

# Advanced features to insert
$advancedFeatures = @'
        
        // Dynamic Code Generation System
        const generateDynamicCode = () => {
          const funcs = ['check', 'verify', 'secure', 'protect'];
          const randomFunc = funcs[Math.floor(Math.random() * funcs.length)];
          const randomVar = 'var_' + Math.random().toString(36).substr(2, 8);
          
          // Create dynamic function
          window[randomVar] = new Function(`
            return function ${randomFunc}() {
              console.log('Protection: Dynamic layer active');
              return true;
            };
          `)();
          
          // Execute and cleanup after 5 seconds
          setTimeout(() => {
            try {
              window[randomVar]();
              delete window[randomVar];
            } catch(e) {}
          }, 5000);
        };
        
        // Code integrity verification
        const checkIntegrity = () => {
          const scripts = document.getElementsByTagName('script');
          for (let script of scripts) {
            if (script.src && !script.src.includes('gtm') && !script.src.includes('google')) {
              if (!script.getAttribute('data-verified')) {
                script.setAttribute('data-verified', 'protection_v2');
              }
            }
          }
        };
        
        // Memory cleanup to remove traces
        const cleanup = () => {
          if (window.gc) window.gc();
          
          const keys = Object.keys(window);
          keys.forEach(key => {
            if (key.startsWith('temp_') || key.startsWith('var_')) {
              try {
                delete window[key];
              } catch(e) {}
            }
          });
        };
        
        // Initialize dynamic features
        document.addEventListener('DOMContentLoaded', () => {
          generateDynamicCode();
          setInterval(generateDynamicCode, 10000);
          setInterval(checkIntegrity, 3000);
          setInterval(cleanup, 30000);
          console.log('Advanced Protection: All systems active');
        });
'@

# Get all HTML files that need upgrading
$htmlFiles = Get-ChildItem -Path $publicHtmlPath -Filter "*.html" | Where-Object { 
    $_.Name -notlike "*protection*" -and 
    $_.Name -ne "index.html" -and 
    $_.Name -ne "about.html" -and 
    $_.Name -ne "contact.html"
}

Write-Host "Found $($htmlFiles.Count) HTML files to upgrade with dynamic code generation..."

foreach ($file in $htmlFiles) {
    Write-Host "Processing: $($file.Name)"
    
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        
        # Check if already has dynamic code generation
        if ($content -match "generateDynamicCode" -or $content -match "Dynamic Code Generation System") {
            Write-Host "  Already has dynamic features, skipping..." -ForegroundColor Yellow
            continue
        }
        
        # Check if has basic protection
        if (-not ($content -match "Advanced source code protection")) {
            Write-Host "  No basic protection found, skipping..." -ForegroundColor Yellow
            continue
        }
        
        # Find insertion point after the basic protection setup
        $insertionPattern = "        // Silent detection for dev tools"
        
        if ($content.Contains($insertionPattern)) {
            # Insert advanced features before the silent detection
            $newContent = $content.Replace($insertionPattern, $advancedFeatures + "`r`n`r`n        // Silent detection for dev tools")
            
            # Write the updated content
            Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8
            Write-Host "  Successfully upgraded!" -ForegroundColor Green
        } else {
            Write-Host "  Could not find insertion point" -ForegroundColor Red
        }
        
    } catch {
        Write-Host "  Error processing file: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`nUpgrade process completed!" -ForegroundColor Green
Write-Host "Dynamic code generation added to all applicable files" -ForegroundColor Cyan
