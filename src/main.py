from dotenv import load_dotenv
load_dotenv()

try:
    from profile_parser import parse_user_description
    from retrieval import fetch_songs_from_llm
    from recommender import load_songs, recommend_songs, explain_recommendation_dict
except ModuleNotFoundError:
    from src.profile_parser import parse_user_description
    from src.retrieval import fetch_songs_from_llm
    from src.recommender import load_songs, recommend_songs, explain_recommendation_dict

def main() -> None:
    print("\nMusic Recommender — RAG Edition")
    print("=" * 45)
    user_input = input("Describe the music you're in the mood for:\n> ").strip()

    print("\n[1/3] Parsing your description...")
    profile = parse_user_description(user_input)
    print(f"      Detected: genre={profile['favorite_genre']}, "
          f"mood={profile['favorite_mood']}, "
          f"energy={profile['target_energy']}, "
          f"acoustic={profile['likes_acoustic']}")

    print("\n[2/3] Retrieving songs...")
    local_songs = load_songs("data/songs.csv")
    retrieved = fetch_songs_from_llm(user_input, limit=10)
    all_songs = local_songs + retrieved
    print(f"      Catalog size: {len(all_songs)} songs total")

    print("\n[3/3] Finding your top 5 and generating explanations...")
    recommendations = recommend_songs(profile, all_songs, k=5)

    print("\n" + "=" * 45)
    print("   Top 5 Recommendations For You")
    print("=" * 45)
    for rank, (song, score, score_reasons) in enumerate(recommendations, start=1):
        explanation = explain_recommendation_dict(user_input, profile, song)
        print(f"\n#{rank}  {song['title']} — {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Why   : {explanation}")
    print("\n" + "=" * 45)

if __name__ == "__main__":
    main()
