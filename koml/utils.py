def split_wildcards(sent, wildcards):
    wildcards.sort(key=len, reverse=True)
    is_wc = []
    holder = []
    i = 0
    j = 0
    while i < len(sent):
        is_match = False
        for wc in wildcards:
            # print(sent[i:i+len(wc)], wc)
            # print(is_match)
            # print('--')
            if sent[i:i+len(wc)] == wc:
                is_match = True
                break
        if is_match:
            if i>j:
                holder.append(sent[j:i])
                is_wc.append(False)
            holder.append(wc)
            is_wc.append(True)
            i = j = i + len(wc)
        else:
            i += 1
    if i > j:
        holder.append(sent[j:i])
        is_wc.append(False)
    return holder, is_wc

def preprocess_sentence():
    # todo: word_sub, delete front back, korean sentence
    pass


        

if  __name__ == '__main__':
    from config import WILDCARDS
    wcs = WILDCARDS 
    sent = '너_x 나 좋아해>'
    result = split_wildcards(sent, wcs)
    print(result)
    