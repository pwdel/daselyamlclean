import subprocess

def dasel_read(manifest_file, selector=""):
    """
    Helper function to run a dasel get command and return the output.
    If selector is empty, the "--selector" flag is omitted.
    """
    cmd = [
        "dasel",
        "--file", manifest_file,
        "--read", "yaml"
    ]
    if selector:
        cmd.extend(["--selector", selector])
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()

def dasel_last_index_for_key(manifest_file, key):
    """
    Helper function to run a dasel get command that uses the count() function on the given key.
    For example, if key is "whateverThing", this function will run:
    
      dasel --file <manifest_file> --read yaml --selector 'whateverThing.all().count()' --type yaml
      
    and return the output.
    """
    selector = f"{key}.all().count()"
    cmd = [
        "dasel",
        "--file", manifest_file,
        "--read", "yaml",
        "--selector", selector,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout.strip()