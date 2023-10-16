from edc_listboard.filters import ListboardFilter, ListboardViewFilters


class AppointmentListboardViewFilters(ListboardViewFilters):

    all = ListboardFilter(name="all", position=0, label="All", lookup={})

    not_dispensed = ListboardFilter(
        name="control", position=10, label="Control Arm", lookup={"rx": True}
    )

    dispensed = ListboardFilter(
        name="single_dose", label="Single Dose", position=20, lookup={"rx": True}
    )
