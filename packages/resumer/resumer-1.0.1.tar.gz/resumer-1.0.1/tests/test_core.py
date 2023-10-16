
from resumer.core.data import ResumerData, ResumerEntry
from resumer.core.filter import ResumerFilter, ResumerFilterUnit


def test_filter_init():
    f = ResumerFilter(
        tags=["a", "b"],
        x_mode="include",
        x_scope="any",
        entries={
            "example" : ResumerFilterUnit(
                check_a_gt_b = "a > b",
                check_has_www= "'www' in self"
            )
        },
        drills=["kkk"]
    )

    f1 = ResumerFilter.from_toml("examples/filter1.toml")
    assert f1 == f
    
    win = ResumerEntry(
        tags=["a"],
        data={
            "www" : 1,
            "a" : 3,
            "b" : 2
        }
    )

    ex = ResumerData(
        entries={
            "example" : [
                win,
                # ! fail: tag
                ResumerEntry(
                    tags=["g"],
                    data={}
                ),
                # ! fail: check
                ResumerEntry(
                    tags=["b"],
                    data={
                        "www" : 1,
                        "a" : 3,
                        "b" : 4
                    }
                ),
                # ! fail: no www
                ResumerEntry(
                    tags=["a"],
                    data={
                        "a" : 3,
                        "b" : 2
                    }
                )
            ],
            "other" : [
                ResumerEntry(
                    tags=["a"],
                    data={
                        "xx" : "{kkk:hi}"
                    }
                ),
                ResumerEntry(
                    tags=[],
                    data={}
                )
            ]
        }
    )

    ex1 = ResumerData.from_toml("examples/data1.toml")
    assert ex == ex1

    x = f.filter(ex)
    assert len(x.entries["example"]) == 1
