import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# 自动加载 .env 文件
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 读取环境变量
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_port = int(os.getenv("DB_PORT", 3306))
db_name = os.getenv("DB_NAME")

print("DB_USER =", os.getenv("DB_USER"))
print("DB_NAME =", os.getenv("DB_NAME"))

def check_connection():
    url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
    print(f"尝试连接数据库：{url}")

    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            print("✅ 数据库连接成功！")
    except OperationalError as e:
        print("❌ 数据库连接失败！错误信息如下：\n")
        print(str(e))
        print("\n🔍 建议排查步骤：")
        print("- 检查用户名和密码是否正确")
        print("- 检查数据库是否正在运行")
        print("- 检查用户是否有权限连接该数据库")
        print("- 若使用 root 用户失败，建议新建用户测试")
    except Exception as e:
        print("❌ 出现未知错误：")
        print(str(e))

if __name__ == "__main__":
    check_connection()
