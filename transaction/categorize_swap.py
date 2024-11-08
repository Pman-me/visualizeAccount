from swap_enum import swap


def categorize_swap(src_dst: dict) -> list | None:
    swaps = []
    from_exist = to_exist = internal = False
    from_count = 0

    for inner_dict in src_dst.values():
        if 'from' in inner_dict:
            from_exist = True
            from_count += 1
        elif 'to' in inner_dict:
            to_exist = True
        else:
            internal = True

    if from_exist and to_exist:
        swaps.extend(from_count * [swap.ALT_TO_ALT])

    elif not from_exist:
        swaps.append(swap.ETH_TO_ALT)

    elif not to_exist:
        swaps.extend(from_count * [swap.ALT_TO_ETH])

    elif internal and from_count >= 1:

        if to_exist:
            swaps.append(swap.ETH_TO_ALT)

    return swaps
