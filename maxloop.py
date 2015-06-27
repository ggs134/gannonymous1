largest = None
print 'before:', largest
for itervar in [3,41,12,9,90,2,100]:
	if largest is None or itervar>largest:
		largest=itervar;
	print 'loop:',itervar, largest;
print 'Largest :', largest;
