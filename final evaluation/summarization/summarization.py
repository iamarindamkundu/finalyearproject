from collections import Counter
import nltk
import re

def commonprefix(m):
	if not m: return ''
	s1 = min(m)
	s2 = max(m)
	for i, c in enumerate(s1):
		if c != s2[i]:
			return s1[:i]
	return s1

def makesent(text):
	sents = filter(lambda x: x != '', [line.strip() for line in text.split('.')])
	tags, target_sents_NN, target_sents_VBG, req_lines = list(), list(), list(), list()
	dummylines, objects = list(), list()
	lookup, target = dict(), dict()

	for line in sents:
		parse = nltk.word_tokenize(line)
		tags.append(nltk.pos_tag(parse))
	counts = Counter([item for line in tags for item in line])

	for item in counts.most_common():
		 if item[0][1] == 'NN':
		 	targetNN = item[0][0]
		 	break

	for item in counts.most_common():
		 if item[0][1] == 'DT':
		 	targetDT = item[0][0]
		 	break

	for key, value in counts.items():
		lookup.setdefault(key[1], []).append(key[0])

	for line in tags:
		for word in line:
			if word[0] == targetNN:
				target_sents_NN.append(line)

	for item in Counter([item for line in target_sents_NN for item in line]).most_common():
		 if item[0][1] == 'VBG':
		 	targetVBG = item[0][0]
		 	break

	for line in target_sents_NN:
		if (targetNN, 'NN') in line and (targetVBG, 'VBG') in line:
			target_sents_VBG.append(line)

	VBZ_list = lookup['VBZ']
	print (VBZ_list, type(VBZ_list))
	target_prefix = [' '.join([targetNN, targetVBG])]
	target_prefix.append(' '.join([targetDT, targetNN, targetVBG]))
	for vbz in VBZ_list:
		target_prefix.append(' '.join([targetDT, targetNN, vbz, targetVBG]))

	for line in sents:
		for tp in target_prefix:
			if line.startswith(tp):
				req_lines.append(line)


	for line in req_lines:
		dummylines.append(line.replace(targetDT + ' ', ''))

	prefix = commonprefix(dummylines)

	for line in dummylines:
		line = re.sub(prefix, '', line)
		if 'and ' in line:
			diff = list()
			diff = line.split(' and ')
			for d in diff:
				objects.append(d)
				break
		else:
			objects.append(line)

	obj = list(set(objects))
	obj.sort()
	obj.sort(key=len)

	req_objects = filter(lambda x: [x for i in obj if x in i and x != i] == [], obj)
	final_text = ' '.join([targetDT, prefix]) + ', '.join(req_objects[:-1]) + ' and ' + req_objects[-1]

	print final_text.capitalize()

if __name__ == '__main__':
	# text = "a white box. a pair of brown pants. a man wearing a tie. the shirt is black. black hat on mans head. a person standing in the background. a wooden door. man has white shirt. a white door. a wooden table. a man wearing a white shirt. man wearing a black suit. the man has glasses. a man in a black shirt. a white shirt on a man. a man in a white shirt. man wearing a white shirt. the mans hair is black. man wearing a suit and tie. a pair of blue jeans. a glass of wine. a white box on the table. a picture of a woman. the man is wearing a tie. a white napkin in the background. a chair with a white seat."
	text = "the man has glasses. a man wearing a white shirt. a white door. a pair of blue jeans. the shirt is black. a white shirt on a man. man wearing a suit and tie. a man in a white shirt. a glass of wine. man has white shirt. a wooden table. a white box. a white box on the table. a man in a black shirt. a man wearing a tie. the mans hair is black. a wooden door. man wearing a black suit. a picture of a woman. a person standing in the background. a white napkin in the background. black hat on mans head. man wearing a white shirt. a chair with a white seat. a pair of brown pants. the man is wearing a tie. "
	makesent(text)
