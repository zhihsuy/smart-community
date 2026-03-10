# models/building.py - 楼栋模型和数据操作
from config.database import execute_sql, logger

class Building:
    """楼栋模型类"""
    
    def __init__(self, data=None):
        """初始化楼栋对象"""
        if data:
            self.id = data.get('id')
            self.community_id = data.get('community_id')
            self.name = data.get('name')
            self.unit_count = data.get('unit_count', 1)
            self.floor_count = data.get('floor_count', 0)
            self.household_count = data.get('household_count', 0)
    
    @classmethod
    def find_by_id(cls, building_id):
        """根据ID查找楼栋"""
        sql = "SELECT * FROM t_building WHERE id = %s LIMIT 1"
        result = execute_sql(sql, (building_id,))
        if result and len(result) > 0:
            return cls(result[0])
        return None
    
    @classmethod
    def find_by_community(cls, community_id):
        """根据社区ID查找楼栋列表"""
        sql = "SELECT * FROM t_building WHERE community_id = %s ORDER BY id"
        result = execute_sql(sql, (community_id,))
        if result:
            return [cls(row) for row in result]
        return []
    
    @classmethod
    def list_all(cls):
        """获取所有楼栋"""
        sql = "SELECT * FROM t_building ORDER BY id"
        result = execute_sql(sql)
        if result:
            return [cls(row) for row in result]
        return []
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'community_id': self.community_id,
            'name': self.name,
            'unit_count': self.unit_count,
            'floor_count': self.floor_count,
            'household_count': self.household_count
        }
