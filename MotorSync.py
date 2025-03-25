#synchronize

import conduitgui
def sync():

    varIntermediate = 1

    sm_intermediatePos = sm_axis.get(varIntermediate)*1.5/256/abs(sm_start.value-sm_end.value)
    big_intermediatePos =big_axis.get(varIntermediate)*1.5/256/4/abs(big_start.value-big_end.value)

    sm_pos_ratio = sm_intermediatePos*1.5/256/abs(sm_start.value-sm_end.value)
    big_pos_ratio = big_intermediatePos*1.5/256/4/abs(big_start.value-big_end.value)

    speedMult = sm_pos_ratio/big_pos_ratio
    print('position ratio = ',speedMult)
