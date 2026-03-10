# utils/permission_util.py - 权限验证工具
import re
from config.database import execute_sql, logger

class PermissionUtil:
    """权限验证工具类"""
    
    @staticmethod
    def get_role_permissions(role):
        """获取角色的所有权限"""
        try:
            sql = """
                SELECT p.code, p.resource, p.method 
                FROM t_permission p
                JOIN t_role_permission rp ON p.id = rp.permission_id
                WHERE rp.role = %s AND p.status = 1
            """
            results = execute_sql(sql, (role,))
            permissions = []
            for result in results:
                permissions.append({
                    'code': result[0],
                    'resource': result[1],
                    'method': result[2]
                })
            return permissions
        except Exception as e:
            logger.error(f"获取角色权限失败: {e}")
            return []
    
    @staticmethod
    def check_permission(role, resource, method):
        """检查角色是否有指定资源的访问权限"""
        # 管理员拥有所有权限
        if role == '管理员':
            return True
        
        # 获取角色的所有权限
        permissions = PermissionUtil.get_role_permissions(role)
        
        # 检查是否有权限
        for perm in permissions:
            # 检查HTTP方法
            if perm['method'] and perm['method'] != method:
                continue
            
            # 检查资源路径（支持通配符）
            resource_pattern = perm['resource'].replace('*', '.*')
            if re.match(resource_pattern, resource):
                return True
        
        return False
    
    @staticmethod
    def get_user_permissions(user_id):
        """获取用户的所有权限"""
        try:
            sql = """
                SELECT u.role 
                FROM t_user u 
                WHERE u.id = %s
            """
            result = execute_sql(sql, (user_id,))
            if not result:
                return []
            
            role = result[0][0]
            return PermissionUtil.get_role_permissions(role)
        except Exception as e:
            logger.error(f"获取用户权限失败: {e}")
            return []
