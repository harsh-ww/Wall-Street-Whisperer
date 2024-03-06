import routes.track_routes as track

def test_already_tracked(clear_data):
    track.save_tracked_company("IBM", "International Business Machines", "IBM", "NYSE")

    isTrackedValid = track.check_already_tracked("IBM")
    isTrackedInvalid = track.check_already_tracked("TSCO.L")
    assert isTrackedValid
    assert not isTrackedInvalid

