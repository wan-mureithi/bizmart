import facebook

access_token = "EAAfiVkmtayABAB9GELW7j7np7Xh3BY3yKKafMG8nvKrQYwTmATYGX1r4mLwco1x6sBHLsh4c4lAosZA3VPy5VEGMTDua2pCDI3joTQZB0ZChVLaZBj533ufgwDCTgiILTwpapZC5PjdtobpmUjp8InuKLOkgZAAm6dAZBRgpW1cFhltNfrO9w5ed7bcMLFgVOd9iXZAD3ku39QZDZD"

fb = facebook.GraphAPI(access_token)

fields = ['email, gender','picture']

profile = fb.get_object('me', fields=fields)

print(profile)
