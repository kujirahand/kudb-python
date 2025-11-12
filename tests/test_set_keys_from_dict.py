#!/usr/bin/env python3
"""
set_keys_from_dict function test script
"""

import kudb
import time

def test_basic_functionality():
    """基本機能のテスト"""
    print("=== 基本機能テスト ===")
    kudb.connect()
    kudb.clear()
    
    # 複数のキー・値ペアを一度に設定
    data = {
        'name': 'Taro',
        'age': 30,
        'city': 'Tokyo',
        'hobbies': ['reading', 'swimming']
    }
    
    kudb.set_keys_from_dict(data)
    
    # 各値を確認
    assert kudb.get_key('name') == 'Taro'
    assert kudb.get_key('age') == 30
    assert kudb.get_key('city') == 'Tokyo'
    assert kudb.get_key('hobbies') == ['reading', 'swimming']
    
    print("✓ 基本的な挿入が正常に動作")

def test_update_functionality():
    """更新機能のテスト"""
    print("=== 更新機能テスト ===")
    
    # 既存のキーを更新、新しいキーを追加
    update_data = {
        'name': 'Jiro',      # 更新
        'age': 25,           # 更新
        'job': 'engineer'    # 新規追加
    }
    
    kudb.set_keys_from_dict(update_data)
    
    # 更新を確認
    assert kudb.get_key('name') == 'Jiro'
    assert kudb.get_key('age') == 25
    assert kudb.get_key('job') == 'engineer'
    # 既存のキーも残っている
    assert kudb.get_key('city') == 'Tokyo'
    assert kudb.get_key('hobbies') == ['reading', 'swimming']
    
    print("✓ 更新機能が正常に動作")

def test_empty_dict():
    """空の辞書のテスト"""
    print("=== 空辞書テスト ===")
    
    keys_before = set(kudb.get_keys())
    kudb.set_keys_from_dict({})
    keys_after = set(kudb.get_keys())
    
    assert keys_before == keys_after
    print("✓ 空辞書の処理が正常に動作")

def test_error_handling():
    """エラーハンドリングのテスト"""
    print("=== エラーハンドリングテスト ===")
    
    try:
        kudb.set_keys_from_dict("not a dict")  # type: ignore
        assert False, "例外が発生すべき"
    except kudb.kudb.KudbError as e:
        assert "must be a dictionary" in str(e)
        print("✓ 非辞書型に対する例外処理が正常に動作")

def test_performance():
    """パフォーマンステスト"""
    print("=== パフォーマンステスト ===")
    
    # 大量データでのテスト
    kudb.clear()
    
    # 個別挿入
    start_time = time.time()
    for i in range(1000):
        kudb.set_key(f'individual_{i}', i * 2)
    individual_time = time.time() - start_time
    
    kudb.clear()
    
    # 一括挿入
    bulk_data = {f'bulk_{i}': i * 2 for i in range(1000)}
    start_time = time.time()
    kudb.set_keys_from_dict(bulk_data)
    bulk_time = time.time() - start_time
    
    print(f"個別挿入 (1000件): {individual_time:.4f}秒")
    print(f"一括挿入 (1000件): {bulk_time:.4f}秒")
    print(f"速度向上: {individual_time/bulk_time:.1f}倍")
    
    # データが正しく挿入されていることを確認
    assert kudb.get_key('bulk_500') == 1000
    assert len(list(kudb.get_keys())) == 1000
    
    print("✓ パフォーマンステストが正常に完了")

def test_data_types():
    """様々なデータ型のテスト"""
    print("=== データ型テスト ===")
    
    kudb.clear()
    
    complex_data = {
        'string': 'Hello World',
        'integer': 42,
        'float': 3.14159,
        'boolean': True,
        'none_value': None,
        'list': [1, 2, 3, 'four'],
        'dict': {'nested': 'value', 'number': 123},
        'unicode': '日本語テスト'
    }
    
    kudb.set_keys_from_dict(complex_data)
    
    # 各データ型を確認
    assert kudb.get_key('string') == 'Hello World'
    assert kudb.get_key('integer') == 42
    assert kudb.get_key('float') == 3.14159
    assert kudb.get_key('boolean') is True
    assert kudb.get_key('none_value') is None
    assert kudb.get_key('list') == [1, 2, 3, 'four']
    assert kudb.get_key('dict') == {'nested': 'value', 'number': 123}
    assert kudb.get_key('unicode') == '日本語テスト'
    
    print("✓ 様々なデータ型の処理が正常に動作")

if __name__ == "__main__":
    print("set_keys_from_dict 関数の包括的テストを開始")
    print("=" * 50)
    
    test_basic_functionality()
    test_update_functionality()
    test_empty_dict()
    test_error_handling()
    test_performance()
    test_data_types()
    
    print("=" * 50)
    print("すべてのテストが正常に完了しました！ ✓")