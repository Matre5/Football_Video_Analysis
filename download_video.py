from SoccerNet.Downloader import SoccerNetDownloader as SNdl

mySNdl = SNdl(LocalDirectory="input_video")
mySNdl.password = "s0cc3rn3t"

mySNdl.downloadGame(
    files=["1_720p.mkv", "2_720p.mkv"],
    game='england_epl\\2014-2015\\2015-02-21 - 18-00 Crystal Palace 1 - 2 Arsenal',)
