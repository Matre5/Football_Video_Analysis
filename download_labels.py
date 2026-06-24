from SoccerNet.Downloader import SoccerNetDownloader as SNdl

mySNdl = SNdl(LocalDirectory="input_video")


mySNdl.downloadGames(files=["Labels-v2.json"], split=["train", "valid", "test"])