#!/usr/bin/env python3
#!/usr/bin/env python

import importlib
import __os as os

MODULES = {
    "crawl": "page",
    "images": "images",
    "search": "search",
    "videos": "videos",
    "facebook": "facebook"
}

def run_as_type():
    _type = os.environ.get("TYPE", "crawl")
    module_name = MODULES.get(_type, "page")

    try:
        module = importlib.import_module(module_name)
        # Gọi hàm crawl() nếu module và hàm tồn tại
        if hasattr(module, "crawl"):
            module.crawl()
        else:
            print(f"❌ Module '{module_name}' không có hàm crawl()")
    except ModuleNotFoundError:
        print(f"❌ Module '{module_name}' không tồn tại!")

if __name__ == "__main__":
    run_as_type()