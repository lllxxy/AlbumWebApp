from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from album_app import app
from exts import db
# 导入模型
from models import *

manager = Manager(app)

# 绑定APP和db
migrate = Migrate(app, db)

# 迁移脚本
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()