imports = """// https://github.com/barryWhiteHat/baby_jubjub_ecc
import "./EC_primitives/baby_jubjub_curve_parameters.code" as parameters
import "./EC_primitives/baby_jubjub_curve_addition.code" as add
import "./EC_primitives/baby_jubjub_curve_multiply.code" as multiply
import "./EC_primitives/baby_jubjub_curve_assert_on_curve.code" as assertOnCurve

"""

constants = """
	field[2] H = [16540640123574156134436876038791482806971768689494387082833631921987005038935, 20819045374670962167435360035096875258406992893633759881276124905556507972311]

	field[2] Base = [15426188768614546009110669764256125036659837110196129316512211073986935525848, 15337024863912528215388680905061745238599231308771177065630214721650168688797]
	"""

def main(nb_private, nb_public):
	assert(nb_private + nb_public > 0 and nb_private >= 0 and nb_public >= 0)

	statement = imports + """def main("""

	if nb_private > 0 :
		for index in range(nb_private):
			statement += f"""private field[256] privateData{index}, private field[256] commitPrivateData{index}, """
	if nb_public > 0:
		for index in range(nb_public):
			statement += f"""field[256] publicData{index}, private field[256] commitPublicData{index}, """
	statement = statement.strip(', ')+")"

	statement += \
			f""" -> (field[2]):

	params = parameters()
	field[2] commitP = [params[2], params[3]]
	{constants}"""
	for index in range(nb_private):
		statement += \
		f"""
	//commit private data{index}
	params[4] = Base[0]
	params[5] = Base[1]
	tmpP = multiply(privateData{index}, params)
	commitP = add(commitP, tmpP, params)
	params[4] = H[0]
	params[5] = H[1]
	tmpP = multiply(commitPrivateData{index}, params)
	commitP = add(commitP, tmpP, params)
	"""

	for index in range(nb_public):
		statement += \
		f"""
	//commit public data{index}
	params[4] = Base[0]
	params[5] = Base[1]
	tmpP = multiply(publicData{index}, params)
	commitP = add(commitP, tmpP, params)
	params[4] = H[0]
	params[5] = H[1]
	tmpP = multiply(commitPublicData{index}, params)
	commitP = add(commitP, tmpP, params)
	"""

	statement += \
	"""
	return commitP"""

	with open("pedersen_commit.code", 'w+') as f:
		f.write(statement)

if __name__ == '__main__':
	main(0, 1)



