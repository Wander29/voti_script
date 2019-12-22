import pdftotext
import sys 
import requests
import os

def usage():
	print("USAGE: <nome.py> <matricola> <cognome> <url_pdf>")
	exit(1)

def print_voto(vet, i, surname):
	str = vet[i]
	i+=1
	while len(vet[i]) < 5:
		str = str + " " + vet[i]
		i+=1
		if (i >= len(vet)):
			break
	str += "\n\n{ next_2chars(to be sure): "
	if(i < len(vet)):
		str += vet[i][0] + vet[i][1] + " }"
	else:
		str += "END }"

	print("\n[" + surname.capitalize() + "] VOTO: " + str)

def main():
	if len(sys.argv) < 4:
		usage()
	if sys.argv[1].isdecimal() and len(sys.argv[1]) == 6:
		matricola = sys.argv[1]
	else:
		usage()
	if sys.argv[2].isalpha() and len(sys.argv[2]) > 1:
		cognome = sys.argv[2].lower()
	else:
		usage()
	if "http" in sys.argv[3]:
		url = sys.argv[3]
	else:
		usage()

	r = requests.get(url, allow_redirects=True)
	open("/tmp/gatto.pdf", "wb").write(r.content)

	with open("/tmp/gatto.pdf", "rb") as f:
		pdf = pdftotext.PDF(f)

	for page in pdf:
		words = page.split()

		for i in range(0, len(words)):
			if words[i] == matricola:
				print_voto(words, i+1, cognome)
			else:
				if words[i].lower() == cognome:
					print_voto(words, i+1, cognome)
	os.remove("/tmp/gatto.pdf")

main()