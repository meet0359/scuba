import os

base_dir = '/Users/meetshah/Downloads/public_html 2'

SW_SCRIPT_TEMPLATE = """
<script>
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('{sw_path}').then(function(registration) {
            console.log('ServiceWorker registration successful');
        }).catch(function(err) {
            console.log('ServiceWorker registration failed: ', err);
        });
    });
}
</script>
"""

for root_dir, dirs, files in os.walk(base_dir):
    if 'temp' in root_dir or '.git' in root_dir or 'node_modules' in root_dir:
        continue
    
    # Calculate relative depth to root
    rel_path = os.path.relpath(root_dir, base_dir)
    depth = 0 if rel_path == '.' else len(rel_path.split(os.sep))
    
    # Path to sw.js based on depth
    sw_path = 'sw.js' if depth == 0 else '../' * depth + 'sw.js'
    sw_script = SW_SCRIPT_TEMPLATE.replace('{sw_path}', sw_path)

    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root_dir, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            if "navigator.serviceWorker.register" in content:
                print(f"Already injected in {filepath}")
                continue
                
            # Inject before </body>
            if "</body>" in content:
                content = content.replace("</body>", sw_script + "\n</body>")
            elif "</html>" in content:
                content = content.replace("</html>", sw_script + "\n</html>")
            else:
                content += sw_script
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Injected SW script into {filepath}")

print("Done injecting Service Worker registration into HTML files.")
