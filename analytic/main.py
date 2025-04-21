#!/usr/bin/env python3
#!/usr/bin/env python

import importlib
import __os as os

def run_as_type():
    module_name = os.environ.get("TYPE", "page")

    try:
        module = importlib.import_module(module_name)
        # Gọi hàm crawl() nếu module và hàm tồn tại
        if hasattr(module, "crawl"):
            module.crawl()
        else:
            print(f"❌ Module '{module_name}' không có hàm crawl()")
    except ModuleNotFoundError as e: # Bắt exception vào biến 'e'
        # In ra thông báo lỗi cụ thể từ exception 'e'
        print(f"❌ Lỗi khi import module '{module_name}': {e}")
    except Exception as e_general: # (Tùy chọn) Bắt các lỗi khác có thể xảy ra
        print(f"❌ Đã xảy ra lỗi không mong muốn khác khi chạy module '{module_name}': {e_general}")


if __name__ == "__main__":
    run_as_type()