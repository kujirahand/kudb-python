#!/usr/bin/env python3
"""
kudb set_keys_from_dict sample
複数のキー・値ペアを効率的に挿入するサンプル
"""

import kudb

def main():
    # データベースに接続
    kudb.connect()
    kudb.clear()
    
    print("=== set_keys_from_dict サンプル ===")
    
    # 1. 基本的な使用例
    print("\n1. 基本的な使用例")
    user_data = {
        'name': '田中太郎',
        'age': 30,
        'email': 'tanaka@example.com',
        'department': '開発部'
    }
    
    kudb.set_keys_from_dict(user_data)
    print(f"名前: {kudb.get_key('name')}")
    print(f"年齢: {kudb.get_key('age')}")
    print(f"部署: {kudb.get_key('department')}")
    
    # 2. 設定データの一括登録
    print("\n2. アプリケーション設定の一括登録")
    app_config = {
        'app_name': 'MyApp',
        'version': '1.2.3',
        'debug': True,
        'max_connections': 100,
        'timeout': 30.0,
        'features': ['auth', 'cache', 'logging'],
        'database': {
            'host': 'localhost',
            'port': 5432,
            'name': 'myapp_db'
        }
    }
    
    kudb.set_keys_from_dict(app_config)
    print(f"アプリ名: {kudb.get_key('app_name')}")
    print(f"バージョン: {kudb.get_key('version')}")
    print(f"デバッグモード: {kudb.get_key('debug')}")
    print(f"データベース設定: {kudb.get_key('database')}")
    
    # 3. 部分的な更新
    print("\n3. 部分的な設定更新")
    updates = {
        'version': '1.2.4',    # バージョンアップ
        'debug': False,        # デバッグモードを無効化
        'new_feature': 'AI'    # 新機能追加
    }
    
    kudb.set_keys_from_dict(updates)
    print(f"更新後バージョン: {kudb.get_key('version')}")
    print(f"デバッグモード: {kudb.get_key('debug')}")
    print(f"新機能: {kudb.get_key('new_feature')}")
    
    # 4. パフォーマンス比較
    print("\n4. パフォーマンス比較")
    import time
    
    # 個別設定での時間測定
    kudb.clear()
    large_data = {f'key_{i}': f'value_{i}' for i in range(500)}
    
    start_time = time.time()
    for key, value in large_data.items():
        kudb.set_key(key, value)
    individual_time = time.time() - start_time
    
    # 一括設定での時間測定
    kudb.clear()
    start_time = time.time()
    kudb.set_keys_from_dict(large_data)
    batch_time = time.time() - start_time
    
    print(f"500件のデータ挿入時間:")
    print(f"  個別挿入: {individual_time:.4f}秒")
    print(f"  一括挿入: {batch_time:.4f}秒")
    print(f"  速度向上: {individual_time/batch_time:.1f}倍")
    
    # 5. エラーハンドリング例
    print("\n5. エラーハンドリング")
    try:
        kudb.set_keys_from_dict("これは辞書ではありません")  # type: ignore
    except kudb.kudb.KudbError as e:
        print(f"エラーが正しく捕捉されました: {e}")
    
    print("\n=== サンプル終了 ===")

if __name__ == "__main__":
    main()