import pickle
from .tags import * 
from korean_rule_helper import KoreanRuleHelper, KoreanSentence

class PatternMatcherError(Exception):
    pass

class PatternMatcher:
    def __init__(self):
        self.cases = []
        self.case_map = {}
        self.ruler = KoreanRuleHelper()

    def save(self, path):
        memory = {
            'cases': self.cases,
            'case_map': self.case_map
        }
        with open(path, 'wb') as fw:
            pickle.dump(memory, fw)

    def load(self, path):
        with open(path, 'rb') as fr:
            memory = pickle.load(fr)
        self.cases = memory['cases']
        self.case_map = memory['case_map']

    def add(self, case):
        pattern = self._convert_pattern(case.pattern)

        if not case.subpat:
            subpat = []
        else:
            subpat = list(map(lambda x: self._convert_pattern(x), case.subpat.child))
        
        if not case.follow:
            follow = []
        else:
            follow = list(map(lambda x: self._convert_pattern(x), case.follow.child))
        
        if case.id:
            if case.id in self.case_map:
                raise PatternMatcherError(f'case id {case.id} is duplicated')
            self.case_map[case.id] = len(self.cases)


        pattern_priority = self._prioritize_pattern(case.pattern.child, case.follow)
        subpat_priority = []
        if case.subpat:
            subpat_priority = list(map(lambda sp: self._prioritize_pattern(sp.child, case.follow ), case.subpat.child))
        # print('pat', pattern)
        # print('subpat', subpat)
        # print('follow', follow)
        rule_case = RuleCase(case=case, pattern=pattern, subpat=subpat, follow=follow, \
            pattern_priority=pattern_priority, subpat_priority=subpat_priority)
        self.cases.append(rule_case)
        # print(rule_case)
        # print(self.case_map)
        # print('-----------')


    def match(self, sentence, context):
        sentence = KoreanSentence(sentence)
        holder = []
        for rcase in self.cases:
            # check follow
            follow = rcase.case.follow
            if follow and context.history:
                prev = context.history[0]
                # follow with cid
                if follow.cid:
                    try:
                        fcase_idx = self.case_map[follow.cid]
                        fcase = self.cases[fcase_idx]
                    except:
                        raise PatternMatcherError(f'cid {follow.cid} not in the scope')
                    prev_question = KoreanSentence(prev.question)
                    is_case_match, _, _ = self._is_case_match(prev_question, fcase)
                    if not is_case_match:
                        continue # give up the case
                # follow pattern match
                if follow.child:
                    matched_flag = False
                    for f_pat in rcase.follow :
                        prev_answer = KoreanSentence(prev.answer)
                        is_match, args = self.ruler.match(prev_answer, f_pat)
                        if is_match:
                            matched_flag = True
                            break
                    if not matched_flag:
                        continue # give up the case

            # check pattern/subpat 
            is_case_match, args, priority = self._is_case_match(sentence, rcase)
            if is_case_match:
                holder.append((rcase.case, args, priority))

        if holder:
            case, args, _ = max(holder, key=lambda x: x[2])
            return case, args 
        else:
            return None, None

    def _is_case_match(self, sentence, rule_case):
        # check pattern
        is_match, args = self.ruler.match(sentence, rule_case.pattern)
        if is_match:
            return True, args, rule_case.pattern_priority
        # check subpat
        for i in range(len(rule_case.subpat)):
            subpat = rule_case.subpat[i]
            is_match, args = self.ruler.match(sentence, subpat)
            if is_match:
                args = self._reorder_arg(args, rule_case.case.subpat.child[i].child)
                return True, args, rule_case.subpat_priority[i]
        return False, None, None

    def _reorder_arg(self, args, subpat: PatternT):
        if len(args) <= 1:
            return args
        order = []
        for item in subpat:
            if isinstance(item, PatStar):
                if not item.idx:
                    return args
                order.append(item.idx)
        assert len(args) == len(order)
        args = [x for _, x in sorted(zip(order, args))]
        return args

    def _prioritize_pattern(self, pattern: PatternT, follow: Optional[Follow]):
        score = 10 
        for pat in pattern:
            if isinstance(pat, Text):
                score += len(pat.val)
            elif isinstance(pat, WildCard) and pat.optional:
                score -= 2
            elif isinstance(pat, PatStar):
                score -= 5
        if follow:
            score += 10
            if follow.cid:
                score += 10
        return score

    def _convert_wildcard(self, wildcard):
        wc = wildcard.val 
        if wc == '*':
            return '*'
        if wc == '_?':
            return {'surface': '?', 'optional': True}
        if wc == '_s' or '_s!':
            pos = 'JKS'
        elif wc == '_c' or '_c!':
            pos = 'JKC'
        elif wc == '_x' or '_x!':
            pos = 'JX'
        elif wc == '_o' or '_o!':
            pos = 'JKO'
        elif wc == '_' or '_!':
            pos = 'J'
        elif wc == '_i':
            raise PatternMatcherError('wildcard _i is not allowed')
        else:
            raise PatternMatcherError(f'wildcard {wc} is not allowed')
        return {'pos': pos, 'optional': wildcard.optional}
    
    def resolve_wildcard(self, sent: str, wildcard):
        wc = wildcard.val
        sent = sent.strip()
        if wc == '_s':
            return self.ruler.add_josa(sent, 'I_GA')
        if wc == '_c':
            return self.ruler.add_josa(sent, 'I_GA')
        if wc == '_x':
            return self.ruler.add_josa(sent, 'EUN_NEUN')
        if wc == '_o':
            return self.ruler.add_josa(sent, 'EUL_REUL')
        if wc == '_i':
            return self.ruler.add_josa(sent, 'I_X')
        return sent

    def _convert_pattern(self, pattern):
        holder = []
        for item in pattern.child:
            if isinstance(item, Text):
                holder.append(item.val)
            elif isinstance(item, WildCard):
                rule = self._convert_wildcard(item)
                holder.append(rule)
            elif isinstance(item, PatStar):
                rule = {'return': True}
                if item.pos:
                    rule['pos'] = item.pos
                if item.npos:
                    rule['!pos'] = item.npos
                holder.append(rule)
            else:
                raise PatternMatcherError(f'{item} is not supported pattern item')
        return holder