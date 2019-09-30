class matrix_to_csv ():
	def write(matrix,name):
		matrixcsv = open(name + ".csv","w") 
		for row in range(matrix.shape[0]):
			for column in range(matrix.shape[1]):
				if column < matrix.shape[1]-1 :
					matrixcsv.write(str(matrix[row][column])+";")
				if column == matrix.shape[1]-1 :
					matrixcsv.write(str(matrix[row][column])+"\n")
		matrixcsv.close()
		print("The matrix was successfully saved into a csv file called: " + name + ".csv")
