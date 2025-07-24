import pandas as pd
import numpy as np

# データ読み込み
characters = pd.read_csv('data/characters.csv')
anime_genres = pd.read_csv('data/anime_genres.csv')
anime_reviews = pd.read_csv('data/anime_reviews.csv')
user_history = pd.read_csv('data/user_history.csv')
similarity = pd.read_csv('data/similarity_results.csv')

USER_ID = 'user01'  # サンプルユーザー
SIMILARITY_THRESHOLD = 0.8  # 推し候補の閾値
ALPHA = 1.0  # 推し度の重み
BETA = 1.0   # レビュー評価の重み
GAMMA = 0.2  # 推しキャラ数の重み
DELTA = 0.5  # レビュー件数の重み
EPS = 1e-6   # 0除算防止

# 1. 類似キャラ抽出
similar_chars = similarity[(similarity['user_id'] == USER_ID) & (similarity['similarity'] >= SIMILARITY_THRESHOLD)]

# 2. キャラごとにアニメIDを紐付け
char_anime = pd.merge(similar_chars, characters, on='character_id')

# 3. 未視聴アニメのみ抽出
watched = user_history[(user_history['user_id'] == USER_ID) & (user_history['watched'] == 1)]['anime_id']
not_watched = char_anime[~char_anime['anime_id'].isin(watched)]

# 4. アニメごとに「推し度」（最大類似度・合計類似度・推しキャラ数）で集計
anime_push = not_watched.groupby(['anime_id', 'anime_title']).agg(
    push_score_max=('similarity', 'max'),
    push_score_sum=('similarity', 'sum'),
    push_score_mean=('similarity', 'mean'),
    push_characters=('character_name', lambda x: ','.join(sorted(set(x))))
).reset_index()
anime_push['push_char_count'] = anime_push['push_characters'].apply(lambda x: len(x.split(',')))

# 5. ジャンル・レビュー情報を付与
anime_push = pd.merge(anime_push, anime_genres, on=['anime_id', 'anime_title'], how='left')
anime_push = pd.merge(anime_push, anime_reviews, on=['anime_id', 'anime_title'], how='left')

# 6. 推し度・レビュー点の正規化
max_push = anime_push['push_score_sum'].max() or EPS
max_review = anime_push['review_score'].max() or EPS
anime_push['push_score_sum_norm'] = anime_push['push_score_sum'] / max_push
anime_push['review_score_norm'] = anime_push['review_score'] / max_review

# 7. レビュー件数の重み
anime_push['review_weight'] = np.log1p(anime_push['review_count'].fillna(0))

# 8. ジャンル好み反映（ユーザーがよく見るジャンルを加点）
# ユーザーが視聴済みアニメのジャンルを集計
watched_anime = anime_genres[anime_genres['anime_id'].isin(watched)]
user_genre_pref = watched_anime['genre'].value_counts().to_dict()
def genre_pref_score(genre):
    if pd.isna(genre):
        return 0
    score = 0
    for g in str(genre).split(','):
        score += user_genre_pref.get(g.strip(), 0)
    return score
anime_push['genre_pref'] = anime_push['genre'].apply(genre_pref_score)

# 9. 合成スコア
anime_push['total_score'] = (
    anime_push['push_score_sum_norm'] * ALPHA +
    anime_push['review_score_norm'] * BETA +
    anime_push['push_char_count'] * GAMMA +
    anime_push['review_weight'] * DELTA +
    anime_push['genre_pref'] * 0.3
)

anime_push = anime_push.sort_values(by='total_score', ascending=False)

print('--- 全部盛り！ハイブリッドレコメンド ---')
for _, row in anime_push.iterrows():
    print(f"アニメ: {row['anime_title']} / ジャンル: {row['genre']} / 合成スコア: {row['total_score']:.2f}\n  推し度合計: {row['push_score_sum']:.2f} (正規化: {row['push_score_sum_norm']:.2f}) / 最大: {row['push_score_max']:.2f} / 平均: {row['push_score_mean']:.2f}\n  推しキャラ数: {row['push_char_count']} / 推しキャラ: {row['push_characters']}\n  レビュー: {row['review_score']}点（{row['review_count']}件, log重み: {row['review_weight']:.2f}）\n  ジャンル好みスコア: {row['genre_pref']}\n") 