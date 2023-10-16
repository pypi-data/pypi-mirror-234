from edc_listboard.filters import ListboardFilter, ListboardViewFilters


class WorklistListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(name="all", position=0, label="All", lookup={})

    missed = ListboardFilter(
        name="control", position=10, label="Control Arm", lookup={"rx": True}
    )

    previous = ListboardFilter(
        name="single_dose",
        label="Single Dose",
        position=20,
        lookup={"singledose": True},
    )
