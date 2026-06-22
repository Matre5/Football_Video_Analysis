from SoccerNet.Downloader import getListGames as gLG

games = gLG(split="train")
print(len(games))
print(games[:10])