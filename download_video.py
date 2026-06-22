from SoccerNet.Downloader import SoccerNetDownloader as SNdl

mySNdl = SNdl(LocalDirectory="Mitus_INT")
mySNdl.password = "s0cc3rn3t"

mySNdl.downloadGame(
    files=["1_224p.mkv", "2_224p.mkv"],
    game='england_epl\\2014-2015\\2015-02-21 - 18-00 Crystal Palace 1 - 2 Arsenal',)
