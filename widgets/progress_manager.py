import json
import os
import platform

def get_storage_path(filename='game_progress.json'):
    if platform.system() == 'Linux' and platform.machine().startswith('arm'):
        try:
            from android.storage import app_storage_path
            path = app_storage_path()
        except ImportError:
            raise Exception("This code must be run on an Android device.")
    else:
        # Используем стандартный путь к документам
        path = os.path.expanduser('~\\Documents')
        # Альтернативно, можно использовать Рабочий стол:
        # path = os.path.expanduser('~\\Desktop')

    storage_path = os.path.join(path, filename)
    print(f"[DEBUG] Storage path: {storage_path}")  # Отладочный принт
    return storage_path

def load_progress():
    filepath = get_storage_path()
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                progress = json.load(f)
            print(f"[DEBUG] Loaded progress: {progress}")  # Отладочный принт
            return progress
        except Exception as e:
            print(f"[DEBUG] Error loading progress file: {e}")  # Отладочный принт
            return {'last_unlocked_level': 1}
    print("[DEBUG] No progress file found. Returning default progress.")  # Отладочный принт
    return {'last_unlocked_level': 1}

def save_progress(progress):
    filepath = get_storage_path()
    print(f"[DEBUG] Attempting to save progress to: {filepath}")  # Отладочный принт
    try:
        # Пробуем создать файл вручную и записать туда тестовые данные
        with open(filepath, 'w') as f:
            f.write('{"test": "test_value"}')
        print("[DEBUG] Successfully wrote test data to the file.")  # Отладочный принт

        # Теперь сохраняем реальный прогресс
        with open(filepath, 'w') as f:
            json.dump(progress, f)
        print(f"[DEBUG] Saved progress: {progress}")  # Отладочный принт
    except Exception as e:
        print(f"[DEBUG] Failed to save progress: {e}")  # Отладочный принт

def update_level_progress(level, last_time):
    progress = load_progress()

    # Обновляем лучшее время для текущего уровня
    best_time_key = f'best_time_level_{level}'
    if best_time_key not in progress or (progress[best_time_key] is None or last_time < progress[best_time_key]):
        progress[best_time_key] = last_time

    # Сохраняем прогресс
    save_progress(progress)

def get_level_info(level):
    progress = load_progress()
    level_number = int(level[-1])
    info = {
        'unlocked': level_number <= progress.get('last_unlocked_level', 1),
        'best_time': progress.get(f'best_time_level_{level_number}', None)
    }
    print(f"[DEBUG] Level info for {level}: {info}")  # Отладочный принт
    return info
