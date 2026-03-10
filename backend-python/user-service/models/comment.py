# models/comment.py - 评价模型
from config.database import db
from datetime import datetime
import json

class Comment:
    def __init__(self, id=None, user_id=None, order_item_id=None, 
                 goods_id=None, rating=None, content=None, 
                 images=None, reply=None, status=None, 
                 created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.order_item_id = order_item_id
        self.goods_id = goods_id
        self.rating = rating
        self.content = content
        self.images = images
        self.reply = reply
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'userId': self.user_id,
            'orderItemId': self.order_item_id,
            'goodsId': self.goods_id,
            'rating': self.rating,
            'content': self.content,
            'images': json.loads(self.images) if isinstance(self.images, str) else self.images,
            'reply': self.reply,
            'status': self.status,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updatedAt': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @classmethod
    def find_by_id(cls, comment_id):
        """根据ID查找评价"""
        sql = "SELECT * FROM t_comment WHERE id = %s"
        result = db.query_one(sql, (comment_id,))
        if result:
            return cls(**result)
        return None
    
    @classmethod
    def list_by_goods(cls, goods_id, page=1, page_size=20, **filters):
        """获取商品评价列表"""
        where_clause = ["goods_id = %s"]
        params = [goods_id]
        
        # 构建过滤条件
        if filters.get('status') is not None:
            where_clause.append("status = %s")
            params.append(filters['status'])
        
        if filters.get('rating'):
            where_clause.append("rating = %s")
            params.append(filters['rating'])
        
        # 构建SQL语句
        base_sql = "SELECT * FROM t_comment"
        base_sql += " WHERE " + " AND ".join(where_clause)
        
        # 计算总数
        count_sql = f"SELECT COUNT(*) FROM t_comment WHERE { ' AND '.join(where_clause) }"
        total = db.query_one(count_sql, tuple(params))[0]
        
        # 排序和分页
        order_by = " ORDER BY created_at DESC"
        offset = (page - 1) * page_size
        base_sql += order_by + " LIMIT %s, %s"
        params.extend([offset, page_size])
        
        results = db.query_all(base_sql, tuple(params))
        comments = [cls(**row) for row in results]
        
        return {
            'list': [comment.to_dict() for comment in comments],
            'total': total,
            'page': page,
            'pageSize': page_size
        }
    
    @classmethod
    def list_by_user(cls, user_id, page=1, page_size=20, **filters):
        """获取用户评价列表"""
        where_clause = ["user_id = %s"]
        params = [user_id]
        
        # 构建过滤条件
        if filters.get('status') is not None:
            where_clause.append("status = %s")
            params.append(filters['status'])
        
        # 构建SQL语句
        base_sql = "SELECT * FROM t_comment"
        base_sql += " WHERE " + " AND ".join(where_clause)
        
        # 计算总数
        count_sql = f"SELECT COUNT(*) FROM t_comment WHERE { ' AND '.join(where_clause) }"
        total = db.query_one(count_sql, tuple(params))[0]
        
        # 排序和分页
        order_by = " ORDER BY created_at DESC"
        offset = (page - 1) * page_size
        base_sql += order_by + " LIMIT %s, %s"
        params.extend([offset, page_size])
        
        results = db.query_all(base_sql, tuple(params))
        comments = [cls(**row) for row in results]
        
        return {
            'list': [comment.to_dict() for comment in comments],
            'total': total,
            'page': page,
            'pageSize': page_size
        }
    
    def save(self):
        """保存评价信息"""
        if self.id:
            # 更新
            sql = """
            UPDATE t_comment SET 
                user_id = %s, order_item_id = %s, goods_id = %s, 
                rating = %s, content = %s, images = %s, 
                reply = %s, status = %s, updated_at = %s
            WHERE id = %s
            """
            params = (
                self.user_id, self.order_item_id, self.goods_id, 
                self.rating, self.content, 
                json.dumps(self.images) if isinstance(self.images, list) else self.images,
                self.reply, self.status, datetime.now(), 
                self.id
            )
            return db.execute(sql, params)
        else:
            # 新增
            sql = """
            INSERT INTO t_comment (
                user_id, order_item_id, goods_id, rating, 
                content, images, reply, status, 
                created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                self.user_id, self.order_item_id, self.goods_id, 
                self.rating, self.content, 
                json.dumps(self.images) if isinstance(self.images, list) else self.images,
                self.reply, self.status, 
                datetime.now(), datetime.now()
            )
            self.id = db.execute(sql, params)
            return self.id
    
    def update(self, **kwargs):
        """更新评价信息"""
        if not self.id:
            return False
        
        # 构建更新字段
        fields = []
        params = []
        
        for key, value in kwargs.items():
            if hasattr(self, key):
                # 特殊处理JSON字段
                if key == 'images' and isinstance(value, list):
                    value = json.dumps(value)
                setattr(self, key, value)
                fields.append(f"{key} = %s")
                params.append(value)
        
        if not fields:
            return False
        
        # 添加更新时间
        fields.append("updated_at = %s")
        params.append(datetime.now())
        params.append(self.id)
        
        # 构建SQL语句
        sql = f"UPDATE t_comment SET {', '.join(fields)} WHERE id = %s"
        return db.execute(sql, tuple(params)) > 0
    
    def delete(self):
        """删除评价"""
        if not self.id:
            return False
        
        sql = "DELETE FROM t_comment WHERE id = %s"
        return db.execute(sql, (self.id,)) > 0