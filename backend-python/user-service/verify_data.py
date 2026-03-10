from config.database import execute_sql

print("验证测试数据...\n")

# 检查公告数据
notices = execute_sql("SELECT COUNT(*) as count FROM t_notice", commit=False)
print(f"公告通知数据: {notices[0]['count']} 条")

# 检查投诉数据
complaints = execute_sql("SELECT COUNT(*) as count FROM t_complaint", commit=False)
print(f"投诉建议数据: {complaints[0]['count']} 条")

# 检查报修数据
repairs = execute_sql("SELECT COUNT(*) as count FROM t_repair_order", commit=False)
print(f"报修管理数据: {repairs[0]['count']} 条")

# 检查门禁设备数据
access = execute_sql("SELECT COUNT(*) as count FROM t_access_control_device", commit=False)
print(f"门禁设备数据: {access[0]['count']} 条")

# 检查停车位数据
parking = execute_sql("SELECT COUNT(*) as count FROM t_parking_space", commit=False)
print(f"停车位数据: {parking[0]['count']} 条")

print("\n✅ 验证完成！")
