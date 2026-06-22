from SoccerNet.Downloader import SoccerNetDownloader as SNdl

mySNdl = SNdl(LocalDirectory="Mitus_INT")


mySNdl.downloadGames(files=["Labels-v2.json"], split=["train", "valid", "test"])