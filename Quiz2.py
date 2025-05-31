import random
import csv
import os
import sys

def clear_console():
    """コンソール画面をクリアします。"""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_quiz_data(filename, n_columns):
    """
    CSVファイルからクイズデータを読み込みます。

    Args:
        filename (str): CSVファイルのパス。
        n_columns (int): 各行のデータ数（問題文、正解、選択肢、概要の合計）。

    Returns:
        list: クイズデータのリスト。各要素は辞書形式。
              ファイル未検出や読み込みエラー時は空リストを返す。
    """
    quiz_list = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if len(row) != n_columns:
                    print(f"警告: {filename} の {i+1} 行目のデータ数が不正です。スキップします。期待値: {n_columns}, 実際: {len(row)}")
                    continue

                question = row[0]
                correct_answer = row[1]
                # 選択肢は、列2～列(n_columns-1)まで
                choices = row[2 : n_columns - 1]
                # 最終列を「概要 (summary)」として扱う
                summary = row[n_columns - 1]

                # 正解が選択肢に含まれていない場合は追加
                if correct_answer not in choices:
                    choices.append(correct_answer)

                quiz_list.append({
                    "question": question,
                    "answer": correct_answer,
                    "choices": choices,
                    "summary": summary
                })
    except FileNotFoundError:
        print(f"エラー: ファイル '{filename}' が見つかりません。")
        return []
    except Exception as e:
        print(f"データの読み込み中にエラーが発生しました: {e}")
        return []

    return quiz_list

def run_quiz(quiz_list):
    """
    クイズを実行します。

    Args:
        quiz_list (list): クイズデータのリスト。
    """
    if not quiz_list:
        print("クイズデータがありません。プログラムを終了します。")
        return

    correct_count = 0
    total_questions = 0

    while True:
        clear_console()

        # ランダムに1件を取り出す
        quiz = random.choice(quiz_list)
        total_questions += 1

        print("------ 問題 ------")
        print(quiz["question"])
        print(f"\nこれは『{quiz['summary']}』の問題だよ！")
        print("\n選択肢:")

        # 選択肢をシャッフル
        shuffled_choices = quiz["choices"].copy()
        random.shuffle(shuffled_choices)

        for i, choice in enumerate(shuffled_choices):
            print(f"{i + 1}. {choice}")

        # プレイヤーの入力を受け付け
        try:
            user_input = input("\n答えの番号を入力してください (終了するには 'q' を入力): ").strip()
            # 'q' で終了
            if user_input.lower() == 'q':
                print("\nクイズを終了します。")
                break

            ans_index = int(user_input) - 1
            if 0 <= ans_index < len(shuffled_choices):
                selected_choice = shuffled_choices[ans_index]
                if selected_choice == quiz["answer"]:
                    print(f"\n✅ 正解！これは『{quiz['summary']}』の活用、意味は「{quiz['answer']}」だね!")
                    correct_count += 1
                else:
                    print(f"\n❌ 不正解... 正解は「{quiz['answer']}」でした。")
            else:
                print("\n⚠ 無効な番号です。表示されている選択肢の番号を入力してください。")
        except ValueError:
            print("\n⚠ 番号で入力するか、'q' で終了してください。")
        except Exception as e:
            print(f"エラーが発生しました: {e}")

        # 結果を表示
        print(f"\n現在の正解数: {correct_count} / {total_questions}問")

        next_action = input("\nEnterキーで次の問題へ、'q' で終了: ").strip()
        if next_action.lower() == 'q':
            print("\nクイズを終了します。ありがとうございました！")
            break

        # 出題済みの問題はリストから削除して重複を避ける
        quiz_list.remove(quiz)

        # 全問終了判定
        if not quiz_list:
            clear_console()
            print("すべてのクイズを解き終えました！")
            break

    # 最終結果の表示
    print(f"\n最終結果: {total_questions}問中 {correct_count}問正解でした。")
    if total_questions > 0:
        accuracy = (correct_count / total_questions) * 100
        print(f"正答率: {accuracy:.2f}%\n")

if __name__ == "__main__":
    # ==========================
    # ● ここから先は必要に応じて編集してください
    # ==========================
    # CSVファイルのパスをここで設定（必要に応じて絶対パスや相対パスに変更してください）
    csv_file_path = input("クイズデータのCSVファイルのパスを入力してください: ").strip()
    # CSVの1行あたりに入っている列数 (問題文1 + 正解1 + 選択肢X + 概要1 = 合計)
    # たとえば、問題文1列、正解1列、選択肢5列、概要1列の場合は 8
    data_columns_n = int(input("各行のデータ数を入力してください: ").strip())

    print(f"'{csv_file_path}' からクイズデータを読み込んでいます...")
    quiz_data = load_quiz_data(csv_file_path, data_columns_n)

    if quiz_data:
        print("クイズを開始します。")
        run_quiz(quiz_data)
    else:
        print("クイズデータを読み込めませんでした。CSVファイルのパス、または列数を確認してください。")
        sys.exit(1)
