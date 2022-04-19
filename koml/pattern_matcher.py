import pickle
from .tags import * 

class PatternMatcherError(Exception):
    pass

class PatternMatcher:
    def __init__(self):
        self.cases = []
        self.case_map = {}

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

    def _convert_wildcard(self, wildcard):
        wc = wildcard.val 
        if wc == '*':
            return '*'
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
                # todo: add pos, npos to param
                holder.append(rule)
            else:
                raise PatternMatcherError(f'{item} is not supported pattern item')
        return holder


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


        print('pat', pattern)
        print('subpat', subpat)
        print('follow', follow)
        rule_case = RuleCase(case=case, pattern=pattern, subpat=subpat, follow=follow)
        self.cases.append(rule_case)
        print(rule_case)
        print(self.case_map)
        print('-----------')
    
    def match(self, sentence):

        pass

