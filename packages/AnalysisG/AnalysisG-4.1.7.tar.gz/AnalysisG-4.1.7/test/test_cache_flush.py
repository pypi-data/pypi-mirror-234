from AnalysisG import Analysis
from examples.Event import EventEx

def test_event_flush():

    ana = Analysis()
    ana.Event = EventEx
    ana.InputSample(None, "samples/dilepton/")
    ana.EventCache = True
    ana.ProjectName = "Project"
    ana.Launch()

    for i in ana: break

    hashes = [i.hash for i in ana.makelist()]
    assert len(hashes)
    ana.FlushEvents(hashes)

    ana.EventName = "EventEx"
    ana.GetEvent = True
    assert len(ana.makehashes()["event"])

    ana.GetEvent = False
    assert not len(ana.makehashes()["event"])
    assert not len([i for i in ana.makelist() if i.Event])

    ana.GetEvent = True
    ana.RestoreEvents(sum([i for i in ana.makehashes()["event"].values()], []))

    ana.GetEvent = True
    ana.EventName = "EventEx"
    hashes = [i.Event for i in ana.makelist() if i.Event]
    assert len(hashes)

    hashes = [i.Event for i in ana if i.Event]
    assert len(hashes)

if __name__ == "__main__":
    test_event_flush()
