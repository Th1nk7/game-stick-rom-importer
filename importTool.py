import sqlite3
import os
import shutil

MNT_PATH = '/mnt/games' # CHANGE THIS IF SD CARD IS NOT MOUNTED AT THIS PATH

EXTENSION_MAPPING = {
    '.zip': (0, 0, '/sdcard/game/cps'),
    '.gba': (3, 7, '/sdcard/game/gba'),
    '.gb':  (2, 7, '/sdcard/game/gb'),
    '.gbc': (2, 7, '/sdcard/game/gbc'),
    '.sfc': (6, 6, '/sdcard/game/sfc'),
    '.smc': (6, 6, '/sdcard/game/sfc'),
    '.bin': (0, 9, '/sdcard/game/ps1'),
    '.cue': (0, 9, '/sdcard/game/ps1'),
    '.iso': (0, 9, '/sdcard/game/ps1'),
    '.img': (0, 9, '/sdcard/game/ps1'),
    '.pbp': (0, 9, '/sdcard/game/ps1'),
    '.gen': (5, 8, '/sdcard/game/md'),
    '.smd': (5, 8, '/sdcard/game/md'),
    '.md':  (5, 8, '/sdcard/game/md'),
    '.nes': (2, 7, '/sdcard/game/fc'),
    '.fc':  (2, 7, '/sdcard/game/fc'),
    '.A26': (15, 15, '/sdcard/game/atari'),
    '.A78': (17, 17, '/sdcard/game/atari'),
}

LOWERCASE_ATARI_EXTENSIONS = {'.a26', '.a78'}

DB_PATH = MNT_PATH + '/game/games.db'

def get_game_info(filepath):
    ext = os.path.splitext(filepath)[1]
    if ext.lower() in LOWERCASE_ATARI_EXTENSIONS:
        ext = ext.upper()
    ext = ext.lower()
    if ext not in EXTENSION_MAPPING:
        raise ValueError(f"Unsupported file extension: {ext}")
    return ext, EXTENSION_MAPPING[ext]

def copy_rom(filepath, timer_path):
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1]
    if ext.lower() in LOWERCASE_ATARI_EXTENSIONS:
        name_no_ext = os.path.splitext(filename)[0]
        filename = f"{name_no_ext}{ext.upper()}"
    target_dir = timer_path.replace('/sdcard', MNT_PATH)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, filename)
    shutil.copy(filepath, target_path)
    return os.path.splitext(filename)[0], os.path.splitext(filename)[1]

def insert_game(db_path, game_id, game_name, suffix, class_type, game_type, timer):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = """
    INSERT INTO tbl_game (gameid, game, suffix, zh_id, en_id, ko_id, video_id, class_type, game_type, hard, timer)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    values = (game_id, game_name, suffix, game_id, game_id, game_id, game_id, class_type, game_type, 0, timer)

    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def main():
    if not os.path.exists(DB_PATH):
        print(f"Database file {DB_PATH} not found.")
        return
    
    filepath = input("Path to ROM file: ").strip()
    if not os.path.isfile(filepath):
        print(f"File does not exist: {filepath}")
        return

    game_id = input("Game ID (must be unique): ").strip()
    if not game_id.isdigit():
        print("Invalid Game ID. Must be an integer.")
        return
    game_id = int(game_id)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM tbl_game WHERE gameid = ?", (game_id,))
    if cursor.fetchone():
        print("Game ID already exists. Choose another.")
        conn.close()
        return
    conn.close()
    
    ext, (class_type, game_type, timer_path) = get_game_info(filepath)

    game_name, suffix = copy_rom(filepath, timer_path)

    insert_game(DB_PATH, game_id, game_name, suffix, class_type, game_type, timer_path)
    print(f"Inserted {game_name} as Game ID {game_id}.")

if __name__ == "__main__":
    main()
