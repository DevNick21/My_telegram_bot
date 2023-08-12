# processed = input("put something ")
# football_keywords_standings = ["league position", "standings",
#                                "table", "top of the league", "teams", "first place", "bottom of the league", "bottom league"]
# for footy_table_response in football_keywords_standings:
#     if footy_table_response and "premier league" in processed:
#         print("hmm")


processed = input("put something ")
football_keywords_standings = ["league position", "standings",
                               "table", "top of the league", "teams", "first place", "bottom of the league", "bottom league"]
# for footy_table_response in football_keywords_standings:
#     if processed.any(footy_table_response + "premier league") != -1:
#         print("A ha")


res = any(footy_table_response in processed for footy_table_response in football_keywords_standings)
print(res)
